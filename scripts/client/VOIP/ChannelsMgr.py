# Embedded file name: scripts/client/VOIP/ChannelsMgr.py
from BigWorld import VOIP as VoipEngine
from Outbox import Outbox, DisabledOutbox
from Channel import Channel
from PrivateConsts import ENGINE_PROTOCOL, MEMBER_STATES, CHANNEL_STATES
import consts
from clientConsts import VOIP_ICON_TYPES
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_TRACE, LOG_WARNING, verify
from wofdecorators import noexcept
import Event
from copy import deepcopy
from itertools import chain

class ChannelsMgr(object):
    """ Manages interpretation between channels of different types.
    Set as callback for BigWorld.VOIP and receives responses from it. """

    def __init__(self, playerID):
        self.playerID = playerID
        self.outbox = Outbox()
        self.__initialized = False
        self.__enabled = None
        self.__tsIdentities = [None] * consts.VOIP.CHANNEL_TYPES.QUANTITY
        self.__muteList = None
        self.eventEnabledFlagChanged = Event.Event()
        self.eventCaptureDevicesUpdated = Event.Event()
        self.eventChannelStateChanged = Event.Event()
        self.eventMemberStateChanged = Event.Event()
        self.eventTick = Event.Event()
        self.eventChannelStateChanged += self.__onChannelStateChanged
        self.__channels = [ Channel(self, type) for type in xrange(consts.VOIP.CHANNEL_TYPES.QUANTITY) ]
        self.__activeChannel = None
        self.__deferredActions = []
        self.__pushToTalkForbidden = False
        LOG_TRACE('VOIP.ChannelsMgr.__init__: player ID is {0}'.format(self.playerID))
        return

    @property
    def initialized(self):
        return self.__initialized

    def initialize(self, tsIdentities, muteList):
        if self.__initialized:
            LOG_ERROR('Already initialized!')
            return
        elif tsIdentities is None or muteList is None:
            VoipEngine.initialise({})
            return
        else:
            self.__tsIdentities = tsIdentities
            self.__muteList = set(muteList)
            LOG_TRACE('Initialized with TS3 identities: {0}'.format(self.__tsIdentities))
            LOG_TRACE('Initialized with mute list: {0}'.format(self.__muteList))
            numChannelTypes = len(self.__tsIdentities)
            LOG_DEBUG('verify')
            verify(numChannelTypes == consts.VOIP.CHANNEL_TYPES.QUANTITY)
            args = {ENGINE_PROTOCOL.KEY_PLAYER_DATABASE_ID: str(self.playerID)}
            numSupportedChannels = 0
            for type in xrange(numChannelTypes):
                if self.__tsIdentities[type]:
                    args[ENGINE_PROTOCOL.KEY_CHANNEL_TYPE_INDEXED % numSupportedChannels] = consts.VOIP.CHANNEL_TYPES.getConstNameByValue(type)
                    args[ENGINE_PROTOCOL.KEY_TS_IDENTITY_INDEXED % numSupportedChannels] = self.__tsIdentities[type]
                numSupportedChannels += 1

            args[ENGINE_PROTOCOL.KEY_NUM_CHANNEL_TYPES] = str(numSupportedChannels)
            VoipEngine.initialise(args)
            self.__initialized = True
            LOG_TRACE('Calling deferred actions...')
            for action in self.__deferredActions:
                action()

            self.__deferredActions = []
            LOG_TRACE('Deferred actions finished.')
            return

    def shutdown(self):
        self.outbox = DisabledOutbox()
        self.eventChannelStateChanged -= self.__onChannelStateChanged
        for channel in self.__channels:
            channel.shutdown()

        VoipEngine.finalise()
        self.__deferredActions = []

    @property
    def enabled(self):
        return bool(self.__enabled)

    @enabled.setter
    def enabled(self, enabled):
        if self.__enabled != enabled:
            LOG_TRACE('VOIP: enabled = %s' % enabled)
            self.__enabled = enabled
            self.eventEnabledFlagChanged(self.__enabled)
            for dbid in self.getAllKnownMembers():
                self.refreshMemberState(dbid)

    @property
    def muteList(self):
        return deepcopy(self.__muteList)

    @property
    def connectedAnywhere(self):
        for channel in self.__channels:
            if channel.stateID == CHANNEL_STATES.CONNECTED:
                return True

        return False

    @property
    def pushToTalkForbidden(self):
        return self.__pushToTalkForbidden

    @pushToTalkForbidden.setter
    def pushToTalkForbidden(self, value):
        if bool(value) != self.__pushToTalkForbidden:
            self.__pushToTalkForbidden = bool(value)
            self.refreshVoiceTransmission()

    def setClientMuted(self, dbid, muted):
        muted = bool(muted)
        LOG_TRACE('setClientMuted: client %d, muted = %s' % (dbid, muted))
        if dbid == self.playerID:
            LOG_ERROR('cannot mute/unmute self!')
            return
        if muted == (dbid in self.__muteList):
            return
        if muted:
            self.__muteList.add(dbid)
        else:
            self.__muteList.discard(dbid)
        self.outbox.sendMuteListChange(dbid, muted)
        for channel in self.__channels:
            channel.applyMemberMuteFlag(dbid, muted)

        self.refreshMemberState(dbid)

    def onCreateChannel(self, type, name, members, leader):
        if not self.initialized:
            LOG_TRACE('NOT INITIALIZED - deferring onCreateChannel()...')
            self.__deferredActions.append(lambda : self.onCreateChannel(type, name, members, leader))
            return
        LOG_TRACE('onCreateChannel: type %s, name %s, members: %r, leader: %r' % (consts.VOIP.CHANNEL_TYPES.getConstNameByValue(type),
         name,
         members,
         leader))
        if not self.__tsIdentities[type]:
            LOG_ERROR('unsupported channel type - ignoring')
            return
        channel = self.__channels[type]
        if not channel.available:
            channel.onCreate(name, members, leader)
            self.refreshVoiceTransmission()
        else:
            LOG_ERROR('channel already exists!')

    def onDestroyChannel(self, type):
        if not self.initialized:
            LOG_TRACE('NOT INITIALIZED - deferring onDestroyChannel()...')
            self.__deferredActions.append(lambda : self.onDestroyChannel(type))
            return
        LOG_TRACE('onDestroyChannel: type {0}'.format(consts.VOIP.CHANNEL_TYPES.getConstNameByValue(type)))
        if not self.__tsIdentities[type]:
            LOG_ERROR('unsupported channel type - ignoring')
            return
        channel = self.__channels[type]
        if channel.available:
            channel.onDestroy()
            self.refreshVoiceTransmission()
        else:
            LOG_ERROR('channel does not exist!')

    def updateChannel(self, type, members, leader):
        if not self.initialized:
            LOG_TRACE('NOT INITIALIZED - deferring updateChannel()...')
            self.__deferredActions.append(lambda : self.updateChannel(type, members, leader))
            return
        LOG_TRACE('updateChannel: type %s, members: %r, leader: %r' % (consts.VOIP.CHANNEL_TYPES.getConstNameByValue(type), members, leader))
        if not self.__tsIdentities[type]:
            LOG_ERROR('unsupported channel type - ignoring')
            return
        channel = self.__channels[type]
        if channel.available:
            channel.setMembers(members, leader)
        else:
            LOG_ERROR('channel not registered!')

    def setChannelEnabled(self, type, enabled):
        if not self.initialized:
            LOG_TRACE('NOT INITIALIZED - deferring setChannelEnabled()...')
            self.__deferredActions.append(lambda : self.setChannelEnabled(type, enabled))
            return
        if not self.__tsIdentities[type]:
            LOG_ERROR('unsupported channel type - ignoring')
            return
        self.__channels[type].enabled = enabled
        self.refreshVoiceTransmission()

    def isChannelSupported(self, type):
        return bool(self.__tsIdentities[type])

    def isChannelEnabled(self, type):
        return self.__tsIdentities[type] and self.__channels[type].enabled

    def isChannelAvailable(self, type):
        return self.__tsIdentities[type] and self.__channels[type].available

    def getAllKnownMembers(self):
        return set(chain(*[ channel.memberDatabaseIDs for channel in self.__channels ]))

    def refreshMemberState(self, dbid):
        channels = dict()
        talkingToChannel = None
        for channelType in xrange(consts.VOIP.CHANNEL_TYPES.QUANTITY):
            stateInChannel = self.__channels[channelType].getMemberState(dbid)
            if stateInChannel != MEMBER_STATES.UNKNOWN:
                channels[channelType] = stateInChannel > MEMBER_STATES.DISCONNECTED
            if talkingToChannel is None and stateInChannel == MEMBER_STATES.TALKING:
                talkingToChannel = channelType

        LOG_TRACE('refreshMemberState: db ID %d, channels %r, talking to channel %s, active channel %s' % (dbid,
         channels,
         consts.VOIP.CHANNEL_TYPES.getConstNameByValue(talkingToChannel),
         consts.VOIP.CHANNEL_TYPES.getConstNameByValue(self.__activeChannel)))
        serviceError = False
        if self.enabled:
            if self.__activeChannel is not None and self.__channels[self.__activeChannel].serviceError:
                serviceError = True
            elif any((channel.serviceError for channel in self.__channels)):
                serviceError = True
        if serviceError and dbid == self.playerID:
            iconID = VOIP_ICON_TYPES.UNAVAILABLE
        else:
            iconID = VOIP_ICON_TYPES.NONE
        if not serviceError and self.connectedAnywhere:
            if self.muteList is not None and dbid in self.muteList:
                iconID = VOIP_ICON_TYPES.MUTED
            elif talkingToChannel == consts.VOIP.CHANNEL_TYPES.ARENA:
                iconID = VOIP_ICON_TYPES.ARENA_CHANNEL_TALKING
            elif talkingToChannel == consts.VOIP.CHANNEL_TYPES.SQUAD:
                iconID = VOIP_ICON_TYPES.SQUAD_CHANNEL_TALKING
            elif talkingToChannel == consts.VOIP.CHANNEL_TYPES.SQUADRON:
                iconID = VOIP_ICON_TYPES.SQUAD_CHANNEL_TALKING
            elif dbid == self.playerID and talkingToChannel is None:
                if self.__activeChannel == consts.VOIP.CHANNEL_TYPES.ARENA:
                    iconID = VOIP_ICON_TYPES.ARENA_CHANNEL
                elif self.__activeChannel == consts.VOIP.CHANNEL_TYPES.SQUAD:
                    iconID = VOIP_ICON_TYPES.SQUAD_CHANNEL
                elif self.__activeChannel == consts.VOIP.CHANNEL_TYPES.SQUADRON:
                    iconID = VOIP_ICON_TYPES.SQUAD_CHANNEL
                else:
                    iconID = VOIP_ICON_TYPES.LISTENING
            elif dbid != self.playerID and self.__activeChannel is not None and self.__activeChannel in channels and not channels[self.__activeChannel]:
                iconID = VOIP_ICON_TYPES.DISCONNECTED
        LOG_TRACE('refreshMemberState: icon %s' % VOIP_ICON_TYPES.getConstNameByValue(iconID))
        self.eventMemberStateChanged(dbid, iconID)
        return

    def __onChannelStateChanged(self, channelType, newState):
        for dbid in self.getAllKnownMembers():
            self.refreshMemberState(dbid)

    def onChannelMembersChanged(self, channelType):
        LOG_TRACE('onChannelMembersChanged: %s' % consts.VOIP.CHANNEL_TYPES.getConstNameByValue(channelType))
        for dbid in self.__channels[channelType].memberDatabaseIDs:
            self.refreshMemberState(dbid)

    def isAnyoneTalking(self):
        for channel in self.__channels:
            for dbid in channel.memberDatabaseIDs:
                if channel.getMemberState(dbid) == MEMBER_STATES.TALKING:
                    return True

        return False

    def canTalkToChannel(self, channelType):
        return self.initialized and self.__channels[channelType].connectable

    def setPushToTalk(self, channelType, status, force):
        if not self.initialized:
            LOG_ERROR('NOT INITIALIZED YET')
            return
        if not self.__tsIdentities[channelType]:
            LOG_ERROR('unsupported channel type - ignoring')
            return
        LOG_TRACE('setPushToTalk {0} (force {1}): channel {2}'.format(status, force, channelType))
        if not force:
            if not self.__enabled:
                LOG_TRACE('VOIP disabled - ignoring setPushToTalk')
                return
            if not self.__channels[channelType].enabled:
                LOG_TRACE('channel disabled - ignoring setPushToTalk')
                return
        if force != self.__channels[channelType].pushToTalkPreserve:
            self.__channels[channelType].pushToTalkPreserve = force
        if status != self.__channels[channelType].pushToTalkStatus:
            self.__channels[channelType].pushToTalkStatus = status
            self.refreshVoiceTransmission()

    def getChannelPushToTalkStatus(self, channelType):
        return self.initialized and self.__tsIdentities[channelType] and self.__channels[channelType].pushToTalkStatus

    def refreshVoiceTransmission(self):
        if not self.initialized:
            return
        else:
            prevActiveChannel = self.__activeChannel
            talking = False
            if self.enabled and not self.pushToTalkForbidden:
                for type, channel in enumerate(self.__channels):
                    if channel.enabled and channel.connectable and channel.pushToTalkStatus:
                        if channel.stateID == CHANNEL_STATES.CONNECTED:
                            self.__activeChannel = channel.type
                            LOG_TRACE('refreshVoiceTransmission: talking to %s channel' % channel.typeName)
                        else:
                            self.__activeChannel = None
                            LOG_WARNING('refreshVoiceTransmission: talking to unconnected %s channel' % channel.typeName)
                        cmd = {ENGINE_PROTOCOL.KEY_COMMAND: ENGINE_PROTOCOL.CMD_SET_ACTIVE_CHANNEL,
                         ENGINE_PROTOCOL.KEY_CHANNEL_TYPE: channel.typeName}
                        VoipEngine.command(cmd)
                        VoipEngine.enableMicrophone({})
                        talking = True
                        break

            if not talking:
                LOG_TRACE('refreshVoiceTransmission: not talking to any channel')
                self.__activeChannel = None
                VoipEngine.disableMicrophone({})
            if self.__activeChannel != prevActiveChannel:
                for dbid in self.getAllKnownMembers():
                    self.refreshMemberState(dbid)

            return

    @noexcept
    def onServerMessage(self, msg, args):
        if consts.VOIP.SERVER_MESSAGES.isValidConst(msg):
            LOG_TRACE('onServerMessage {0}, args: {1}'.format(consts.VOIP.SERVER_MESSAGES.getConstNameByValue(msg), args))
        else:
            LOG_ERROR('onServerMessage {0} (unknown message!), args: {1}'.format(msg, args))
            return
        if 'channel' not in args:
            LOG_ERROR('channel not specified')
        for channel in self.__channels:
            if channel.name == args['channel']:
                channel.onServerMessage(msg, args)
                break
        else:
            LOG_ERROR('unknown channel {0}'.format(args['channel']))

    @noexcept
    def __call__(self, message, data = None):
        """ Handler for messages from C++ part (BigWorld.VOIP) """
        if data is None:
            data = {}
        if message != ENGINE_PROTOCOL.MESSAGES.vmTick:
            LOG_TRACE('__call__: {0} {1}'.format(ENGINE_PROTOCOL.MESSAGES.getConstNameByValue(message), data))
        if ENGINE_PROTOCOL.KEY_CHANNEL_TYPE in data:
            for channel in self.__channels:
                if channel.typeName == data[ENGINE_PROTOCOL.KEY_CHANNEL_TYPE]:
                    channel.processMessage(message, data)
                    break
            else:
                LOG_ERROR('invalid channel type %s' % data[ENGINE_PROTOCOL.KEY_CHANNEL_TYPE])

        elif message == ENGINE_PROTOCOL.MESSAGES.vmCaptureDevices:
            numDevices = int(data[ENGINE_PROTOCOL.KEY_COUNT])
            devices = [ str(data[ENGINE_PROTOCOL.KEY_CAPTURE_DEVICE_INDEXED % i]) for i in xrange(numDevices) ]
            currentDevice = str(data[ENGINE_PROTOCOL.KEY_CURRENT_CAPTURE_DEVICE])
            self.eventCaptureDevicesUpdated(devices, currentDevice)
        elif message == ENGINE_PROTOCOL.MESSAGES.vmTick:
            self.eventTick()
        else:
            LOG_ERROR('unrecognized non-channel-specific message')
        return