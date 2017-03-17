# Embedded file name: scripts/client/VOIP/API.py
from BigWorld import VOIP as VoipEngine
from ChannelsMgr import ChannelsMgr
from PrivateConsts import ENGINE_PROTOCOL
import Event
from debug_utils import LOG_TRACE, LOG_WARNING, LOG_ERROR
import consts
import time
import random
from messenger import g_xmppChatHandler
import InputMapping
import GlobalEvents
from clientConsts import SWITCH_STYLES_BUTTONS

class API(object):

    @property
    def playerID(self):
        return self.__channelsMgr.playerID

    @property
    def enabled(self):
        """ Boolean property for global state of Voice Chat.
            When enabled, will send a request for initialization data to Game Server, if it has not been received yet.
            Response to this request must be fed to onReceiveInitData method.
        """
        return self.__channelsMgr.enabled

    @enabled.setter
    def enabled(self, value):
        self.__channelsMgr.enabled = bool(value)

    @property
    def localTestMode(self):
        """ Boolean property for toggling local testing mode.
            When enabled, user's voice is looped back to their own playback device.
            Can be used for tuning volume, voice activation threshold and other settings.
        
            Entering testing mode automatically disables push-to-talk for all channels.
        """
        return self.__testMode

    @localTestMode.setter
    def localTestMode(self, testMode):
        if testMode != self.__testMode:
            LOG_TRACE('VOIP localTestMode = %s' % testMode)
            self.__channelsMgr.pushToTalkForbidden = testMode
            self.__testMode = testMode
            self.__applyTestMode()

    def requestCaptureDevices(self):
        """ Request information about detected capture devices and currently selected device.
            Response will be sent through eventCaptureDevicesUpdated (args: device names list, current device name).
        """
        VoipEngine.command({ENGINE_PROTOCOL.KEY_COMMAND: ENGINE_PROTOCOL.CMD_REQUEST_CAPTURE_DEVICES})

    def updateSettings(self, voiceActivationLevel = None, voiceVolume = None, muffledMasterVolume = None, autoConnectArenaChannel = None, captureDevice = None):
        """ Change one or more settings.
            If None is passed for any argument, corresponding setting is not changed.
        
        @param voiceActivationLevel:    0.0 to 1.0; the higher this is, the louder you must speak for your voice
                                        to be captured and transmitted to other players.
                                        Used to suppress background noise.
        
        @param voiceVolume:             0.0 to 1.0; relative playback volume for other players' voice
                                        (or your own voice when in local test mode).
        
        @param muffledMasterVolume:     0.0 to 1.0; muffling factor applied to the game's master sound volume
                                        when anyone is speaking (including yourself).
        
        @param autoConnectArenaChannel: True to auto-connect to the arena channel when it is created by Game Server.
        
        @param captureDevice:           capture device name string
        """
        if captureDevice is not None and captureDevice != self.__captureDevice:
            self.__captureDevice = captureDevice
            self.__applyCaptureDevice()
        if autoConnectArenaChannel is not None and autoConnectArenaChannel != self.__autoConnectArenaChannel:
            self.__autoConnectArenaChannel = autoConnectArenaChannel
            self.setArenaChannelStatus(autoConnectArenaChannel)
        if voiceActivationLevel is not None:
            self.__voiceActivationLevel = voiceActivationLevel
        if voiceVolume is not None:
            self.__voiceVolume = voiceVolume
        if muffledMasterVolume is not None:
            self.__muffledMasterVolume = muffledMasterVolume
        self.__refreshVolume()
        return

    def _initialize(self):
        """ Performs VOIP engine pre-initialisation and requests init-data from server,
            if it is required, but hasn't been received yet.
            Called automatically as necessary - probably should never be called directly.
        """
        if not self.__channelsMgr.initialized:
            self.__channelsMgr.initialize(None, None)
            self.__channelsMgr.outbox.requestInitData(self.__onReceiveInitData)
        return

    @property
    def voipSupported(self):
        """ Returns True if voice chat is enabled on current game server.
            This flag is set after calling onReceiveInitData().
        """
        import BattleReplay
        if BattleReplay.isPlaying():
            return True
        return self.__voipSupported

    @property
    def arenaChannelSupported(self):
        """ Returns True if arena voice channels are enabled on current game server.
            This flag is set after calling onReceiveInitData().
        """
        import BattleReplay
        if BattleReplay.isPlaying():
            return True
        return self.__arenaChannelSupported

    def onServerMessage(self, msg, args):
        """ Must be called when a generic VOIP-specific message was received from Game Server.
        
        @param msg:  member of consts.VOIP.SERVER_MESSAGES
        @param args: dict with message-specific arguments
        """
        self.__channelsMgr.onServerMessage(msg, args)

    def onEnterSquadChannel(self, channel, clientIDs):
        """ Must be called when information about a squad voice channel is received from Game Server.
        
        @param channel:   unique channel name (used only for further communication with Game Server)
        @param clientIDs: list of database IDs of all players (including us) with access to this channel
        """
        LOG_TRACE('VOIP onEnterSquadChannel', channel, clientIDs)
        self.__channelsMgr.onCreateChannel(consts.VOIP.CHANNEL_TYPES.SQUAD, channel, clientIDs, self.__squadOwnerDbID)

    def updateSquad(self, squadID, squadInfo):
        """ Temporary method for receiving detailed info about our squad
            (regardless of whether a voice channel exists).
        
        @param squadID:   unique squad ID (used only for further communication with Game Server)
        @param squadInfo: dictionary with 'accountIDs' and 'ownerID' keys
        """
        if 'accountIDs' in squadInfo:
            self.__squadID = squadID
            self.__squadMembers = [ int(id) for id in squadInfo['accountIDs'] ]
            self.__squadOwnerDbID = int(squadInfo['ownerID'])
            LOG_TRACE('VOIP updateSquad: squad ID {0}, owner {1}'.format(self.__squadID, self.__squadOwnerDbID))
            self.__channelsMgr.updateChannel(consts.VOIP.CHANNEL_TYPES.SQUAD, self.__squadMembers, self.__squadOwnerDbID)
            for dbid in self.__squadMembers:
                self.__channelsMgr.refreshMemberState(dbid)

        else:
            LOG_TRACE('VOIP updateSquad: no squad')
            self.__squadID = None
            self.__squadMembers = []
            self.__squadOwnerDbID = None
        return

    def onLeaveSquadChannel(self):
        """  Must be called when our squad voice channel is destroyed by Game Server.
             We must leave it (if not kicked already) and cease any reconnection attempts.
        """
        LOG_TRACE('onLeaveSquadChannel')
        self.__channelsMgr.onDestroyChannel(consts.VOIP.CHANNEL_TYPES.SQUAD)

    def setSquadChannelStatus(self, channelEnabled):
        """ Request to create or delete current squad's voice channel (affects all squad members).
            Channel creation is allowed for any member of the squad, but only squad leader can delete the channel.
        
        @param channelEnabled: True to request creation of squad channel, False to request deletion
        """
        if self.__channelsMgr.isChannelSupported(consts.VOIP.CHANNEL_TYPES.SQUAD):
            if self.__squadID is not None:
                if channelEnabled or self.__squadOwnerDbID == self.__channelsMgr.playerID:
                    LOG_TRACE('VOIP setSquadChannelStatus: squad %s, status %s' % (self.__squadID, channelEnabled))
                    self.__channelsMgr.outbox.sendSquadChannelStatus(self.__squadID, channelEnabled)
                else:
                    LOG_ERROR('VOIP setSquadChannelStatus: only leader can delete the channel!')
            else:
                LOG_ERROR('VOIP setSquadChannelStatus: not a squad member!')
        else:
            LOG_ERROR('VOIP setSquadChannelStatus: channel not supported by server')
        return

    def onEnterSquadronChannel(self, channel, squadronID, memberIDs, leaderID):
        """ Must be called when information about a squadron voice channel is received from Game Server.
        
        @param channel:    unique channel name (used only for further communication with Game Server)
        @param squadronID: unique squadron ID (used only for further communication with Game Server)
        @param memberIDs:  list of database IDs of all players (including us) with access to this channel
        @param leaderID:   squadron leader database ID
        """
        LOG_TRACE('VOIP onEnterSquadronChannel', channel, squadronID, memberIDs, leaderID)
        self.__squadronID = squadronID
        self.__squadronMembers = memberIDs
        self.__squadronOwnerDbID = leaderID
        self.__channelsMgr.onCreateChannel(consts.VOIP.CHANNEL_TYPES.SQUADRON, channel, memberIDs, leaderID)

    def updateSquadron(self, squadronID, memberIDs):
        """ Temporary method for receiving detailed info about our squadron
            (regardless of whether a voice channel exists).
        
        @param squadronID: unique squadron ID (used only for further communication with Game Server)
        @param memberIDs:  list of database IDs of all players (including us) with access to this channel
        """
        LOG_TRACE('VOIP updateSquadron', squadronID, memberIDs)
        if squadronID != self.__squadronID:
            LOG_ERROR('VOIP updateSquadron: wrong squadron ID')
        elif self.__squadronOwnerDbID not in memberIDs:
            LOG_ERROR('VOIP updateSquadron: leader %s is not in new members list' % self.__squadronOwnerDbID)
        else:
            self.__squadronMembers = memberIDs
            self.__channelsMgr.updateChannel(consts.VOIP.CHANNEL_TYPES.SQUADRON, self.__squadronMembers, self.__squadronOwnerDbID)
            for dbid in self.__squadronMembers:
                self.__channelsMgr.refreshMemberState(dbid)

    def onLeaveSquadronChannel(self):
        """  Must be called when our squadron voice channel is destroyed by Game Server.
             We must leave it (if not kicked already) and cease any reconnection attempts.
        """
        LOG_TRACE('onLeaveSquadronChannel')
        self.__channelsMgr.onDestroyChannel(consts.VOIP.CHANNEL_TYPES.SQUADRON)

    def setSquadronChannelStatus(self, channelEnabled):
        """ Request to create or delete current squadron's voice channel (affects all squadron members).
            Channel creation is allowed for any member of the squadron, but only squadron leader can delete the channel.
        
        @param channelEnabled: True to request creation of squadron channel, False to request deletion
        """
        if self.__channelsMgr.isChannelSupported(consts.VOIP.CHANNEL_TYPES.SQUADRON):
            if self.__squadronID is not None:
                if channelEnabled or self.__squadronOwnerDbID == self.__channelsMgr.playerID:
                    LOG_TRACE('VOIP setSquadronChannelStatus: squadron %s, status %s' % (self.__squadronID, channelEnabled))
                    self.__channelsMgr.outbox.sendSquadronChannelStatus(self.__squadronID, channelEnabled)
                else:
                    LOG_ERROR('VOIP setSquadronChannelStatus: only leader can delete the channel!')
            else:
                LOG_ERROR('VOIP setSquadronChannelStatus: not a squadron member!')
        else:
            LOG_ERROR('VOIP setSquadronChannelStatus: channel not supported by server')
        return

    def onEnterArenaScreen(self):
        """ Must be called when user enters the arena screen.
            Talking-status UI must be fully initialized at this point.
            Connection to the arena channel can only be active when in arena screen,
            regardless of the status of the channel itself and any user settings.
        """
        LOG_TRACE('VOIP onEnterArenaScreen (auto-connect: %s)' % self.__autoConnectArenaChannel)
        self.__inArenaScreen = True
        self.__channelsMgr.setChannelEnabled(consts.VOIP.CHANNEL_TYPES.ARENA, self.__autoConnectArenaChannel)
        for dbid in self.__channelsMgr.getAllKnownMembers():
            self.__channelsMgr.refreshMemberState(dbid)

    def onLeaveArenaScreen(self):
        """ Must be called when user leaves the arena screen.
            Connection to the arena channel can only be active when in arena screen,
            regardless of the status of the channel itself and any user settings.
        """
        LOG_TRACE('VOIP onLeaveArenaScreen')
        self.__inArenaScreen = False
        self.__channelsMgr.setChannelEnabled(consts.VOIP.CHANNEL_TYPES.ARENA, False)

    def onEnterArenaChannel(self, channel, clientIDs):
        """ Must be called when information about an arena voice channel is received from Game Server.
        
        @param channel:   unique channel name (used only for further communication with Game Server)
        @param clientIDs: list of database IDs of all players (including us) with access to this channel
        """
        LOG_TRACE('VOIP onEnterArenaChannel %s %r' % (channel, clientIDs))
        if not self.__inArenaScreen:
            self.__channelsMgr.setChannelEnabled(consts.VOIP.CHANNEL_TYPES.ARENA, False)
        self.__channelsMgr.onCreateChannel(consts.VOIP.CHANNEL_TYPES.ARENA, channel, clientIDs, None)
        return

    def onLeaveArenaChannel(self):
        """  Must be called when our arena voice channel is destroyed by Game Server
             (or when this player is no longer allowed inside the channel).
             We must leave it (if not kicked already) and cease any reconnection attempts.
        """
        LOG_TRACE('VOIP onLeaveArenaChannel')
        self.__channelsMgr.onDestroyChannel(consts.VOIP.CHANNEL_TYPES.ARENA)

    def setArenaChannelStatus(self, channelEnabled):
        """ Connect or disconnect this player from current arena channel (if any).
            Does not affect channel itself. Other team members can see our connection status.
        
            When disconnected, we do not receive any voice from other players talking to this channel.
            This includes our squad members - to reach us, they will have to speak directly to the squad channel.
        
            Does not change global auto-connection preference. That is, when a new arena channel is received,
            we will automatically connect to it if our current settings say so, even if we explicitly
            disconnected from arena channel of an earlier battle.
        
        @param channelEnabled: True to connect, False to disconnect
        """
        LOG_TRACE('VOIP setArenaChannelStatus: status {0}'.format(channelEnabled))
        if self.__inArenaScreen:
            self.__channelsMgr.setChannelEnabled(consts.VOIP.CHANNEL_TYPES.ARENA, channelEnabled)
        else:
            LOG_WARNING('VOIP setArenaChannelStatus ignored - arena screen not loaded yet!')

    def toggleArenaChannelStatus(self):
        """ Connect to current arena channel if disconnected, disconnect if connected. """
        self.setArenaChannelStatus(not self.__channelsMgr.isChannelEnabled(consts.VOIP.CHANNEL_TYPES.ARENA))

    def subscribeMemberStateObserver(self, type, observer):
        """ Register a GUI observer for voice chat members' state changes (silent, talking, disconnected etc).
        
        @param type:     member of consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES
        @param observer: anything (specific to observer type; used by Outbox to visualize status changes)
        """
        LOG_TRACE('VOIP subscribeMemberStateObserver - type %s' % consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.getConstNameByValue(type))
        self.__memberStateObservers.append((type, observer))
        for dbid in self.__channelsMgr.getAllKnownMembers():
            self.__channelsMgr.refreshMemberState(dbid)

    def unsubscribeMemberStateObserver(self, type, observer):
        """ Unregister a previously registered GUI observer for voice chat members' state changes.
        
        @param type:     member of consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES
        @param observer: value previously passed to subscribeMemberStatusObserver together with the same type
        """
        LOG_TRACE('VOIP unsubscribeMemberStateObserver - type %s' % consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.getConstNameByValue(type))
        if (type, observer) in self.__memberStateObservers:
            self.__memberStateObservers.remove((type, observer))
        else:
            LOG_ERROR('VOIP unsubscribeMemberStateObserver: subscriber not found')

    def unsubscribeMemberStateObserversByType(self, type):
        """ Unregister all previously registered voice chat members' state observers of given type.
        
        @param type:     member of consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES
        """
        LOG_TRACE('VOIP unsubscribeMemberStateObserversByType - type %s' % consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.getConstNameByValue(type))
        self.__memberStateObservers[:] = [ (t, o) for t, o in self.__memberStateObservers if t != type ]

    def setPushToTalk(self, channelType, status, force = False):
        """ Activate or deactivate microphone for talking to a specific channel.
            Even when the microphone is active, actual voice transmission only occurs
            if its volume exceeds the "voice activation level" setting.
        
        @param channelType: Channel we want to talk to (member of consts.VOIP_CHANNEL_TYPES).
                            If push-to-talk is active for several different channels at the same time,
                            only one of them is chosen (e.g. arena has higher priority than squad).
        
                            Push-to-talk changes are ignored in the following cases:
                            - channel is not available or not connected;
                            - channel is explicitly disabled by player;
                            - VOIP module is currently in local test mode.
        
                            All of these cases can be overridden by force argument.
        
        @param status:      True to activate, False to deactivate talking to this channel.
        
        @param force:       True to change status regardless of channel availability and connection status.
                            This must be used for real "push-to-talk" behavior (in battle) when the corresponding
                            hot key must be held, as opposed to toggle-button behavior in lobby.
        """
        if status == self.__channelsMgr.getChannelPushToTalkStatus(channelType):
            return
        else:
            LOG_TRACE('VOIP setPushToTalk %s (force %s): channel %s' % (status, force, consts.VOIP.CHANNEL_TYPES.getConstNameByValue(channelType)))
            if self.__testMode and not force:
                LOG_WARNING('VOIP setPushToTalk ignored in local test mode')
            elif channelType == consts.VOIP.CHANNEL_TYPES.SQUAD and self.__squadID is not None and status == True and not self.__channelsMgr.isChannelAvailable(consts.VOIP.CHANNEL_TYPES.SQUAD) and self.__channelsMgr.enabled:
                LOG_TRACE('VOIP setPushToTalk: requesting squad channel creation on demand')
                self.setSquadChannelStatus(True)
                self.__channelsMgr.setPushToTalk(channelType, status, force)
            elif not status or force or self.__channelsMgr.canTalkToChannel(channelType):
                self.__channelsMgr.setPushToTalk(channelType, status, force)
            else:
                LOG_WARNING('VOIP setPushToTalk ignored for unavailable/unconnected channel')
            return

    def togglePushToTalk(self, channelType, force = False):
        """ Toggle microphone activation status for talking to a specific channel.
        
        @param channelType: Channel we want to talk to (member of consts.VOIP_CHANNEL_TYPES).
        @param force:       Same as for setPushToTalk method.
        """
        LOG_TRACE('VOIP togglePushToTalk: channel %s' % consts.VOIP.CHANNEL_TYPES.getConstNameByValue(channelType))
        self.setPushToTalk(channelType, not self.__channelsMgr.getChannelPushToTalkStatus(channelType), force)

    def setClientMuted(self, dbid, muted):
        """ Add or remove a specific player (by generic database ID) to our personal mute list.
        
        @param dbid:  database ID of a player
        @param muted: True to mute, False to unmute
        """
        self.__channelsMgr.setClientMuted(dbid, muted)

    def setAvatarMuted(self, avatarID, muted):
        """ Add or remove a specific player (by in-battle avatar ID) to our personal mute list.
        
        @param avatarID: avatar ID of a player
        @param muted:    True to mute, False to unmute
        """
        for type, observer in self.__memberStateObservers:
            if type == consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.ARENA_HUD:
                for dbid, avid in observer.iteritems():
                    if avid == avatarID:
                        self.__channelsMgr.setClientMuted(dbid, muted)
                        return

        LOG_ERROR('VOIP setAvatarMuted: unknown avatar ID {0}'.format(avatarID))

    def requestMuteList(self, callback):
        """ Returns a mute list in the form of a list of database IDs by passing it to provided callback.
            If mute list is not yet ready (i.e. not received from server),
            callback will be deferred until the necessary data arrives.
        
        @param callback: object to call when mute list is ready; must accept 1 argument (mute list)
        """
        if self.__channelsMgr.initialized:
            callback(self.__channelsMgr.muteList)
        else:
            self.__muteListRequests.append(callback)

    def __init__(self, playerID):
        self.eventCaptureDevicesUpdated = Event.Event()
        self.__voipSupported = False
        self.__arenaChannelSupported = False
        self.__channelsMgr = ChannelsMgr(playerID)
        self.__channelsMgr.eventEnabledFlagChanged += self.__onEnabledFlagChanged
        self.__channelsMgr.eventCaptureDevicesUpdated += self.eventCaptureDevicesUpdated
        self.__channelsMgr.eventMemberStateChanged += self.__onMemberStateChanged
        GlobalEvents.onKeyEvent += self.__handleKeyEvent
        VoipEngine.setHandler(self.__channelsMgr)
        self.__testMode = False
        self.__squadID = None
        self.__squadMembers = []
        self.__squadOwnerDbID = None
        self.__squadronID = None
        self.__squadronMembers = []
        self.__squadronOwnerDbID = None
        self.__memberStateObservers = []
        self.__voiceActivationLevel = 0.0
        self.__voiceVolume = 1.0
        self.__muffledMasterVolume = 1.0
        self.__autoConnectArenaChannel = True
        self.__captureDevice = ''
        self.__muteListRequests = []
        self.__inArenaScreen = False
        return

    def _shutdown(self):
        """ Called by VOIP.shutdown(). """
        LOG_TRACE('VOIP shutdown')
        self.__channelsMgr.eventEnabledFlagChanged -= self.__onEnabledFlagChanged
        self.__channelsMgr.eventCaptureDevicesUpdated -= self.eventCaptureDevicesUpdated
        self.__channelsMgr.eventMemberStateChanged -= self.__onMemberStateChanged
        GlobalEvents.onKeyEvent -= self.__handleKeyEvent
        self.clearEventCaptureDevicesUpdated()
        self.__channelsMgr.shutdown()
        VoipEngine.setHandler(None)
        return

    def clearEventCaptureDevicesUpdated(self):
        self.eventCaptureDevicesUpdated.clear()

    def __handleKeyEvent(self, event):
        switchingStyle = InputMapping.g_instance.getSwitchingStyle(InputMapping.CMD_PUSH_TO_TALK_SQUAD)
        if switchingStyle is not None and not event.isRepeatedEvent():
            isFired = InputMapping.g_instance.keyboardSettings.getCommand(InputMapping.CMD_PUSH_TO_TALK_SQUAD).isCommandActive()
            if switchingStyle == SWITCH_STYLES_BUTTONS.SWITCH:
                if isFired:
                    self.togglePushToTalk(consts.VOIP.CHANNEL_TYPES.SQUAD)
            else:
                self.setPushToTalk(consts.VOIP.CHANNEL_TYPES.SQUAD, isFired)
        return False

    def __onEnabledFlagChanged(self, enabled):
        self._initialize()
        self.__applyTestMode()

    def __onReceiveInitData(self, operation, returnCode, tsIdentities, muteList):
        """ Callback for receiving initialization data for client's VOIP module from Game Server.
        
        @param operation:    not used
        @param returnCode:   not used
        @param tsIdentities: list of TeamSpeak identities for specific channel types (consts.VOIP_CHANNEL_TYPES)
        @param muteList:     list of database IDs of players in our personal mute list
        """
        if self.__channelsMgr.initialized:
            LOG_WARNING('VOIP __onReceiveInitData: already initialized, ignoring')
            return
        g_xmppChatHandler.receiveMuteList([ str(id) for id in muteList ])
        self.__voipSupported = False
        self.__arenaChannelSupported = False
        for id in tsIdentities:
            if id:
                self.__voipSupported = True
                self.__arenaChannelSupported = bool(tsIdentities[consts.VOIP.CHANNEL_TYPES.ARENA])
                break

        LOG_TRACE('VOIP __onReceiveInitData: voice chat %s' % ('SUPPORTED' if self.__voipSupported else 'NOT SUPPORTED'))
        LOG_TRACE('VOIP __onReceiveInitData: arena channel %s' % ('SUPPORTED' if self.__arenaChannelSupported else 'NOT SUPPORTED'))
        self.__channelsMgr.initialize(tsIdentities, muteList)
        self.__applyCaptureDevice()
        self.__refreshVolume()
        for callback in self.__muteListRequests:
            callback(self.__channelsMgr.muteList)

        self.__muteListRequests = []

    def __onMemberStateChanged(self, dbid, iconID):
        self.__refreshVolume()
        for type, observer in self.__memberStateObservers:
            self.__channelsMgr.outbox.visualizeMemberState(dbid, iconID, dbid in self.__channelsMgr.muteList, type, observer)

    def __applyCaptureDevice(self):
        if self.__channelsMgr.initialized:
            VoipEngine.command({ENGINE_PROTOCOL.KEY_COMMAND: ENGINE_PROTOCOL.CMD_SELECT_CAPTURE_DEVICE,
             ENGINE_PROTOCOL.KEY_CURRENT_CAPTURE_DEVICE: self.__captureDevice})
            self.requestCaptureDevices()

    def __refreshVolume(self):
        if self.__channelsMgr.enabled:
            db = -50 + int(round(self.__voiceActivationLevel * 100))
            VoipEngine.setVoiceActivationLevel(db, {})
            db = -20.0 * (1.0 - self.__voiceVolume) + 30 * self.__voiceVolume
            VoipEngine.setMasterVolume(db, {})
            if self.__testMode or self.__channelsMgr.isAnyoneTalking():
                self.__channelsMgr.outbox.setMasterVolumeMultiplier(self.__muffledMasterVolume)
            else:
                self.__channelsMgr.outbox.setMasterVolumeMultiplier(1.0)

    def __applyTestMode(self):
        testMode = self.__testMode and self.__channelsMgr.enabled
        VoipEngine.command({ENGINE_PROTOCOL.KEY_COMMAND: ENGINE_PROTOCOL.CMD_TEST,
         ENGINE_PROTOCOL.KEY_STATE: str(testMode)})
        self.__refreshVolume()