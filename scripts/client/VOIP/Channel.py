# Embedded file name: scripts/client/VOIP/Channel.py
from BigWorld import VOIP as VoipEngine
from PrivateConsts import ENGINE_PROTOCOL, CHANNEL_STATES, MEMBER_STATES
from Fsm import Fsm, StateBase
import consts
from debug_utils import verify, LOG_DEBUG, LOG_TRACE, LOG_WARNING, LOG_ERROR
import time
import random

def _chooseReconnectDelay():
    return random.randint(1, 3)


_MUFFLED_CLIENTS_VOLUME = '-15'
_NORMAL_CLIENTS_VOLUME = '0'

class _FSM_EVENTS():
    """ List of events supported by Channel's state machine. """
    TICK = 0
    CHANNEL_CREATED = 1
    CREDENTIALS_RECEIVED = 2
    SERVICE_UNAVAILABLE = 3
    SERVICE_CONNECTED = 4
    SERVICE_DISCONNECTED = 5
    SERVICE_ERROR = 6

    @staticmethod
    def getConstNameByValue(const):
        for k, v in _FSM_EVENTS.__dict__.items():
            if v == const:
                return k


class Channel(Fsm):
    """ Connection manager for a specific channel type (squad, arena etc). """

    def __init__(self, mgr, type):
        """
        @param mgr:  ChannelsMgr object owning this channel
        @param type: member of consts.VOIP.CHANNEL_TYPES
        """
        self.__mgr = mgr
        self.__type = type
        self.__enabled = True
        self.__name = None
        self.__members = {}
        self.__leaderDbID = None
        self.__voipServiceDown = False
        self._provisioningKey = None
        self._securityHash = None
        self._failureCount = 0
        self.pushToTalkStatus = False
        self.pushToTalkPreserve = False
        mgr.eventTick += self.__tick
        mgr.eventEnabledFlagChanged += self.__onGlobalEnabledFlagChanged
        states = {CHANNEL_STATES.DISCONNECTED: _StateDisconnected,
         CHANNEL_STATES.CONNECTING: _StateConnecting,
         CHANNEL_STATES.CONNECTED: _StateConnected,
         CHANNEL_STATES.DISCONNECTING: _StateDisconnecting}
        Fsm.__init__(self, states, _FSM_EVENTS, CHANNEL_STATES.DISCONNECTED)
        return

    def shutdown(self):
        Fsm.shutdown(self)
        self.__mgr.eventTick -= self.__tick
        self.__mgr.eventEnabledFlagChanged -= self.__onGlobalEnabledFlagChanged
        self.__mgr = None
        return

    @property
    def type(self):
        return self.__type

    @property
    def typeName(self):
        return consts.VOIP.CHANNEL_TYPES.getConstNameByValue(self.__type)

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        if value != self.__enabled:
            self.__enabled = value
            self._failureCount = 0

    def __onGlobalEnabledFlagChanged(self, enabled):
        self._failureCount = 0

    @property
    def available(self):
        return self.__name is not None

    @property
    def serviceError(self):
        return self.enabled and self.available and self.stateID != CHANNEL_STATES.CONNECTED

    @property
    def name(self):
        return self.__name

    @property
    def mustDisconnect(self):
        return not self.__mgr.initialized or not self.__mgr.enabled or not self.enabled or not self.available

    @property
    def connectable(self):
        return not self.mustDisconnect and not self.__voipServiceDown

    @property
    def hasCredentials(self):
        return self._provisioningKey is not None and self._securityHash is not None

    @property
    def stateName(self):
        return CHANNEL_STATES.getConstNameByValue(self.stateID)

    def onStateChange(self, oldStateID, newStateID):
        LOG_TRACE('VOIP channel %s state changed: %s -> %s' % (self.typeName, CHANNEL_STATES.getConstNameByValue(oldStateID), CHANNEL_STATES.getConstNameByValue(newStateID)))
        self.__mgr.eventChannelStateChanged(self.__type, newStateID)

    def onCreate(self, name, members, leaderDbID):
        """ Channel has been created by the Game Server.
        
        @param name:       unique channel name from Game Server; used only for further communication with server
        @param members:    list of players with access to this channel (database IDs)
        @param leaderDbID: database ID of channel leader or None if no leader
        """
        LOG_DEBUG('VOIP channel %s (%s) onCreate' % (self.typeName, self.stateName))
        LOG_DEBUG('verify')
        verify(not self.available)
        if self.__mgr.playerID not in members:
            LOG_ERROR('Wrong player ID: %s' % self.__mgr.playerID)
            return
        elif not (leaderDbID is None or leaderDbID in members):
            LOG_ERROR('Wrong leader channel ID: %s' % leaderDbID)
            return
        else:
            self.__name = name
            self.__members.clear()
            for DbID in members:
                self.__members[DbID] = MEMBER_STATES.DISCONNECTED

            self.__leaderDbID = leaderDbID
            self.__onMembersChanged()
            self.processEvent(_FSM_EVENTS.CHANNEL_CREATED)
            return

    def onDestroy(self):
        """ Channel has been deleted by the Game Server. """
        LOG_DEBUG('VOIP channel %s onDestroy' % self.typeName)
        LOG_DEBUG('verify')
        verify(self.available)
        if not self.pushToTalkPreserve:
            self.pushToTalkStatus = False
        self.__name = None
        self._failureCount = 0
        self._provisioningKey = None
        self._securityHash = None
        for dbid in self.__members:
            self.__members[dbid] = MEMBER_STATES.DISCONNECTED

        self.__onMembersChanged()
        self.__members.clear()
        self.__leaderDbID = None
        self.__onMembersChanged()
        return

    @property
    def memberDatabaseIDs(self):
        return self.__members.keys()

    def setMembers(self, dbIDs, leaderDbID):
        LOG_DEBUG('verify')
        verify(self.__mgr.playerID in dbIDs)
        LOG_DEBUG('verify')
        verify(leaderDbID is None or leaderDbID in dbIDs)
        newIDs = set(dbIDs)
        oldIDs = set(self.__members.keys())
        removedIDs = oldIDs - newIDs
        addedIDs = newIDs - oldIDs
        for dbID in removedIDs:
            del self.__members[dbID]

        for dbID in addedIDs:
            self.__members[dbID] = MEMBER_STATES.DISCONNECTED
            VoipEngine.command({ENGINE_PROTOCOL.KEY_COMMAND: ENGINE_PROTOCOL.CMD_REQUEST_CLIENT_STATUS,
             ENGINE_PROTOCOL.KEY_PLAYER_DATABASE_ID: str(dbID)})

        self.__leaderDbID = leaderDbID
        self.__onMembersChanged()
        return

    def getMemberState(self, dbid):
        if dbid in self.__members:
            return self.__members[dbid]
        else:
            return MEMBER_STATES.UNKNOWN

    def applyMemberMuteFlag(self, dbid, muted):
        if self.stateID == CHANNEL_STATES.CONNECTED:
            LOG_TRACE('VOIP channel %s (%s) - applyMemberMuteFlag(%s, %s)' % (self.typeName,
             self.stateName,
             dbid,
             muted))
            cmd = {ENGINE_PROTOCOL.KEY_COMMAND: ENGINE_PROTOCOL.CMD_SET_CLIENT_MUTE,
             ENGINE_PROTOCOL.KEY_CHANNEL_TYPE: self.typeName,
             ENGINE_PROTOCOL.KEY_PLAYER_DATABASE_ID: str(dbid),
             ENGINE_PROTOCOL.KEY_STATE: str(muted)}
            VoipEngine.command(cmd)

    def __tick(self):
        self.processEvent(_FSM_EVENTS.TICK)

    def onServerMessage(self, msg, args):
        if msg == consts.VOIP.SERVER_MESSAGES.CHAT_CREDENTIALS:
            LOG_TRACE('VOIP channel %s (%s) - received credentials' % (self.typeName, self.stateName))
            self.__voipServiceDown = False
            self._provisioningKey = args['key']
            self._securityHash = args['hash']
            self.processEvent(_FSM_EVENTS.CREDENTIALS_RECEIVED)
        elif msg == consts.VOIP.SERVER_MESSAGES.CHAT_UNAVAILABLE:
            LOG_TRACE('VOIP channel %s (%s) - service is down! ceasing reconnect attempts until further notice' % (self.typeName, self.stateName))
            self.__voipServiceDown = True
            self.processEvent(_FSM_EVENTS.SERVICE_UNAVAILABLE)

    def __onMembersChanged(self, affectedID = None):
        if affectedID == None:
            self.__mgr.onChannelMembersChanged(self.__type)
        else:
            self.__mgr.refreshMemberState(affectedID)
        if self.__leaderDbID is not None:
            leaderTalking = self.__members[self.__leaderDbID] == MEMBER_STATES.TALKING
            LOG_TRACE('VOIP channel %s (%s): leader talking? %s' % (self.typeName, self.stateName, leaderTalking))
            for dbid in self.__members:
                muffled = leaderTalking and dbid != self.__leaderDbID
                cmd = {ENGINE_PROTOCOL.KEY_COMMAND: ENGINE_PROTOCOL.CMD_SET_CLIENT_VOLUME,
                 ENGINE_PROTOCOL.KEY_CHANNEL_TYPE: self.typeName,
                 ENGINE_PROTOCOL.KEY_PLAYER_DATABASE_ID: str(dbid),
                 ENGINE_PROTOCOL.KEY_VOLUME: _MUFFLED_CLIENTS_VOLUME if muffled else _NORMAL_CLIENTS_VOLUME}
                VoipEngine.command(cmd)

        return

    def _sendRequest(self, requestID):
        if not self.__voipServiceDown:
            LOG_TRACE('VOIP channel %s (%s): sending request %s; channel name: %s' % (self.typeName,
             self.stateName,
             consts.VOIP.CLIENT_REQUESTS.getConstNameByValue(requestID),
             self.__name))
            self.__mgr.outbox.sendRequest(requestID, self.__type, self.__name)
        else:
            LOG_WARNING('VOIP channel %s (%s): service is down, ignoring request %s; channel name: %s' % (self.typeName,
             self.stateName,
             consts.VOIP.CLIENT_REQUESTS.getConstNameByValue(requestID),
             self.__name))

    def processMessage(self, message, data):
        LOG_TRACE('VOIP channel %s (%s) processMessage: %s' % (self.typeName, self.stateName, ENGINE_PROTOCOL.MESSAGES.getConstNameByValue(message)))
        if message == ENGINE_PROTOCOL.MESSAGES.vmLoggedIn:
            self.processEvent(_FSM_EVENTS.SERVICE_CONNECTED)
            self.__members[self.__mgr.playerID] = MEMBER_STATES.CONNECTED
            self.__onMembersChanged()
            for dbid in self.__mgr.muteList:
                self.applyMemberMuteFlag(dbid, True)

            self.__mgr.refreshVoiceTransmission()
        elif message == ENGINE_PROTOCOL.MESSAGES.vmLoginFailed:
            self.processEvent(_FSM_EVENTS.SERVICE_ERROR, error=int(data[ENGINE_PROTOCOL.KEY_STATUS_CODE]))
        elif message == ENGINE_PROTOCOL.MESSAGES.vmLoggedOut:
            self.processEvent(_FSM_EVENTS.SERVICE_DISCONNECTED, error=int(data[ENGINE_PROTOCOL.KEY_STATUS_CODE]))
            for dbid in self.__members:
                self.__members[dbid] = MEMBER_STATES.DISCONNECTED

            self.__onMembersChanged()
            self.__mgr.refreshVoiceTransmission()
        elif message == ENGINE_PROTOCOL.MESSAGES.vmClientTalkingStatus:
            clientID = int(data[ENGINE_PROTOCOL.KEY_PLAYER_DATABASE_ID])
            talking = data[ENGINE_PROTOCOL.KEY_STATE] == 'True'
            LOG_TRACE('client %d %s' % (clientID, 'TALKING' if talking else 'SILENT'))
            if clientID in self.__members:
                if talking:
                    if self.__members[clientID] != MEMBER_STATES.DISCONNECTED:
                        self.__members[clientID] = MEMBER_STATES.TALKING
                    else:
                        LOG_ERROR('client talking while not connected!')
                elif self.__members[clientID] == MEMBER_STATES.TALKING:
                    self.__members[clientID] = MEMBER_STATES.CONNECTED
                self.__onMembersChanged(clientID)
            elif talking:
                LOG_ERROR('unknown client!')
        elif message == ENGINE_PROTOCOL.MESSAGES.vmClientMoved:
            clientID = int(data[ENGINE_PROTOCOL.KEY_PLAYER_DATABASE_ID])
            LOG_DEBUG('verify')
            verify(clientID != self.__mgr.playerID)
            joined = data[ENGINE_PROTOCOL.KEY_TS_CHANNEL_ID] != '0'
            LOG_TRACE('client %d %s' % (clientID, 'JOINED' if joined else 'LEAVING'))
            if clientID in self.__members:
                if joined:
                    if self.__members[clientID] == MEMBER_STATES.DISCONNECTED:
                        self.__members[clientID] = MEMBER_STATES.CONNECTED
                    muted = clientID in self.__mgr.muteList
                    LOG_TRACE('re-applying mute status (%s) for joined client' % muted)
                    self.applyMemberMuteFlag(clientID, muted)
                else:
                    self.__members[clientID] = MEMBER_STATES.DISCONNECTED
                self.__onMembersChanged(clientID)
            elif joined:
                LOG_ERROR('unknown client joined!')


class _StateDisconnected(StateBase):

    def __init__(self, channel, **kwargs):
        super(_StateDisconnected, self).__init__(channel)
        LOG_TRACE('_StateDisconnected failure count %d, args: %r' % (channel._failureCount, kwargs))
        self.__disconnectTime = time.time()
        self.__reconnectDelay = kwargs.get('reconnectDelay', 0)
        self.__waitingForCredentials = False
        if channel.available:
            if not channel.hasCredentials:
                channel._sendRequest(consts.VOIP.CLIENT_REQUESTS.NEED_CHAT_CREDENTIALS)
                self.__waitingForCredentials = True
            elif kwargs.get('expired', False):
                channel._sendRequest(consts.VOIP.CLIENT_REQUESTS.CHAT_CREDENTIALS_EXPIRED)

    def onChannelCreated(self, channel, **kwargs):
        if not channel.hasCredentials:
            channel._sendRequest(consts.VOIP.CLIENT_REQUESTS.NEED_CHAT_CREDENTIALS)
            self.__waitingForCredentials = True

    def onTick(self, channel, **kwargs):
        if not self.__waitingForCredentials and channel.hasCredentials and channel.connectable:
            elapsedTime = time.time() - self.__disconnectTime
            if elapsedTime >= self.__reconnectDelay:
                channel._transit(CHANNEL_STATES.CONNECTING)

    def onCredentialsReceived(self, channel, **kwargs):
        self.__waitingForCredentials = False
        self.__reconnectDelay = 0


class _StateConnecting(StateBase):

    def __init__(self, channel, **kwargs):
        super(_StateConnecting, self).__init__(channel)
        LOG_DEBUG('verify')
        verify(channel.hasCredentials)
        LOG_TRACE("VOIP channel %s (%s) trying to connect: key '%s', hash '%s'" % (channel.typeName,
         channel.stateName,
         channel._provisioningKey,
         channel._securityHash))
        VoipEngine.login('', '', {ENGINE_PROTOCOL.KEY_CHANNEL_TYPE: channel.typeName,
         ENGINE_PROTOCOL.KEY_PROVISIONING_KEY: channel._provisioningKey,
         ENGINE_PROTOCOL.KEY_SECURITY_HASH: channel._securityHash})

    def onServiceConnected(self, channel, **kwargs):
        LOG_TRACE('VOIP channel %s (%s) connected successfully' % (channel.typeName, channel.stateName))
        channel._transit(CHANNEL_STATES.CONNECTED)

    def onServiceUnavailable(self, channel, **kwargs):
        self.__onFailure(channel, 'service unavailable')

    def onServiceDisconnected(self, channel, **kwargs):
        self.__onFailure(channel, 'error 0x%x' % kwargs['error'])

    def onServiceError(self, channel, **kwargs):
        self.__onFailure(channel, 'error 0x%x' % kwargs['error'])

    def __onFailure(self, channel, errorMessage):
        LOG_ERROR('VOIP channel %s (%s) login failed! %s' % (channel.typeName, channel.stateName, errorMessage))
        reconnectDelay = 0 if channel._failureCount == 0 else _chooseReconnectDelay()
        channel._failureCount += 1
        channel._transit(CHANNEL_STATES.DISCONNECTED, reconnectDelay=reconnectDelay, expired=True)


class _StateConnected(StateBase):

    def __init__(self, channel, **kwargs):
        super(_StateConnected, self).__init__(channel)
        channel._failureCount = 0

    def onTick(self, channel, **kwargs):
        if channel.mustDisconnect:
            channel._transit(CHANNEL_STATES.DISCONNECTING)

    def onServiceError(self, channel, **kwargs):
        LOG_ERROR('VOIP channel %s (%s) service error 0x%x' % (channel.typeName, channel.stateName, kwargs['error']))
        channel._transit(CHANNEL_STATES.DISCONNECTING)

    def onServiceDisconnected(self, channel, **kwargs):
        LOG_WARNING('VOIP channel %s (%s) connection lost, error 0x%x' % (channel.typeName, channel.stateName, kwargs['error']))
        channel._transit(CHANNEL_STATES.DISCONNECTED, reconnectDelay=_chooseReconnectDelay())


class _StateDisconnecting(StateBase):

    def __init__(self, channel, **kwargs):
        super(_StateDisconnecting, self).__init__(channel)
        channel._failureCount = 0
        VoipEngine.logout({ENGINE_PROTOCOL.KEY_CHANNEL_TYPE: channel.typeName})

    def onServiceError(self, channel, **kwargs):
        LOG_ERROR('VOIP channel %s (%s) service error 0x%x' % (channel.typeName, channel.stateName, kwargs['error']))
        channel._transit(CHANNEL_STATES.DISCONNECTING)

    def onServiceDisconnected(self, channel, **kwargs):
        LOG_TRACE('VOIP channel %s (%s) disconnected, error 0x%x' % (channel.typeName, channel.stateName, kwargs['error']))
        channel._transit(CHANNEL_STATES.DISCONNECTED)