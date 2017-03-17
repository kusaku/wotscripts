# Embedded file name: scripts/client/gui/Scaleform/GameOptions/GameOptionsStats.py
__author__ = 's_karchavets'
from consts import GAME_OPTIONS_STATS_TYPE, GAME_OPTIONS_STATS, CLIENT_STATS_TYPE, MAX_SEND_DATA_SIZE
import BigWorld
from debug_utils import LOG_WARNING, LOG_INFO, LOG_ERROR, LOG_DEBUG
from gui.Scaleform.GameOptions.GameOptionsStatsConsts import STATS_SEPARATOR, HASH_IDS, SETTINGS_GAME_UI_DICT, SETTINGS_MAIN_DICT, SETTINGS_AIMS_DICT
from functools import partial
import wgPickle

class _SettingsStatsBase(object):

    def __init__(self):
        self.container = list()

    def _submit(self, stats):
        if stats:

            def __getPlayer():
                from Account import PlayerAccount
                from PlayerAvatar import PlayerAvatar
                player = BigWorld.player()
                if player is not None and player.__class__ in [PlayerAccount, PlayerAvatar]:
                    return player
                else:
                    return

            player = __getPlayer()
            if player is not None:
                self.container = stats.items()
        return

    def fill(self):
        raise NotImplementedError

    def _getStatType(self):
        raise NotImplementedError

    def _getHashName(self):
        return HASH_IDS.get(self._getStatType(), '')

    def _checkForSubmit(self, container):
        newHash = self._checkHash(container)
        if newHash:
            LOG_INFO('fill', newHash, self._getStatType(), self._getHashName())
            self._submit(container)

    def _checkHash(self, container):
        return True

    def destroy(self):
        pass


class _ControlSettingsStats(_SettingsStatsBase):

    def _getStatType(self):
        return GAME_OPTIONS_STATS_TYPE.GAME_OPTIONS_STATS_INPUT

    def fill(self):
        import InputMapping
        container = {GAME_OPTIONS_STATS.PRESET: InputMapping.g_instance.getCurPresetName()}
        self._fillPrimary(container, InputMapping.g_instance.primarySettings)
        self._fillKeyboard(container, InputMapping.g_instance.getCurCommandsKeys())
        self._checkForSubmit(container)

    def _fillPrimary(self, container, data):
        """
        @param container: <dict>
        @param data: <class object>
        """
        from Curve import Curve
        for key, id in GAME_OPTIONS_STATS.__dict__.iteritems():
            if isinstance(id, int):
                value = getattr(data, key, None)
                if value is not None:
                    if isinstance(value, Curve):
                        value = value.p[:]
                    container[id] = value

        return

    def _fillKeyboard(self, container, mapping):
        """
        @param container: <dict>
        """
        for commandID, commandData in mapping.iteritems():
            id, switchingStyle, keyCodes = commandData
            if id in GAME_OPTIONS_STATS.__dict__.keys():
                tId = getattr(GAME_OPTIONS_STATS, id)
                commandData = [ keyCode['name'] for keyCode in keyCodes ]
                commandData.extend(['KEY_NONE'] * (2 - len(keyCodes)))
                commandData.extend([str(switchingStyle)])
                container[tId] = STATS_SEPARATOR.join(commandData)
            else:
                LOG_WARNING('_fillKeyboard - skip command:', id, keyCodes)


class _BattleSettingsStats(_SettingsStatsBase):

    def _fillSettingsGameUI(self, container):
        import Settings
        s = Settings.g_instance
        for id, sKey in SETTINGS_GAME_UI_DICT.iteritems():
            value = s.getGameUI().get(sKey, None)
            if value is not None:
                container[id] = value
            else:
                LOG_WARNING('_fillSettingsGameUI - skip:', id, sKey)

        return

    def _fillSettingsMain(self, container):
        import Settings
        s = Settings.g_instance
        for id, sKey in SETTINGS_MAIN_DICT.iteritems():
            value = getattr(s, sKey, None)
            if value is not None:
                container[id] = value
            else:
                LOG_WARNING('_fillSettingsMain - skip:', id, sKey)

        return

    def _fillAims(self, container):
        import Settings
        aims = Settings.g_instance.getAimsData()
        for id, sKey in SETTINGS_AIMS_DICT.iteritems():
            value = aims.get(sKey, None)
            if value is not None:
                container[id] = value
            else:
                LOG_WARNING('_fillAims - skip:', id, sKey)

        return

    def _fillMarkers(self, container):
        import Settings
        s = Settings.g_instance
        from gui.Scaleform.GameOptions.vo.MarkerSettings import AVAILABLE_MARKER_PROPERTIES
        for vehicleType in ('airMarker', 'groundMarker'):
            for targetType in ('enemy', 'target', 'friendly', 'squads'):
                for altState in ('basic', 'alt'):
                    for key in AVAILABLE_MARKER_PROPERTIES:
                        sKey = '_'.join([vehicleType,
                         targetType,
                         altState,
                         key]).upper()
                        id = GAME_OPTIONS_STATS.__dict__.get(sKey, None)
                        if id is not None:
                            container[id] = STATS_SEPARATOR.join([ str(v) for v in s.markersTemplates[vehicleType][targetType][altState][key] ])

        return

    def fill(self):
        container = dict()
        self._fillSettingsGameUI(container)
        self._fillSettingsMain(container)
        self._fillAims(container)
        self._fillMarkers(container)
        self._checkForSubmit(container)

    def _getStatType(self):
        return GAME_OPTIONS_STATS_TYPE.GAME_OPTIONS_STATS_BATTLE


class _GraphicsSettingsStats(_SettingsStatsBase):

    def fill(self):
        container = dict()
        import Settings
        settings = Settings.g_instance
        from clientConsts import isLowMemory
        container[GAME_OPTIONS_STATS.IS_HD_CONTENT] = settings.isHDContent()
        container[GAME_OPTIONS_STATS.IS_VIDEO_VSYNC] = settings.isVideoVSync()
        container[GAME_OPTIONS_STATS.GRAPHICS_WIN32] = isLowMemory()
        container[GAME_OPTIONS_STATS.GS_AUTODETECT_ENABLED] = settings.gsAutodetectEnabled
        container[GAME_OPTIONS_STATS.WINDOW_MODE] = settings.getWindowMode()
        container[GAME_OPTIONS_STATS.GRAPHICS_GAMMA] = settings.getGamma()
        _, container[GAME_OPTIONS_STATS.VIDEO_RESOLUTION] = settings.getVideoResolutions()
        container[GAME_OPTIONS_STATS.GRAPHICS_QUALITY_INDEX] = Settings.g_instance.getIndexByValueGraphicsDetails(settings.graphicsDetails)
        gdList = settings.graphicsPresets.getSettingValues()
        graphicsDetailsConfig = settings.graphicsPresets.getPresetValues()
        graphicsDetail = graphicsDetailsConfig.get(settings.graphicsDetails, None)
        if graphicsDetail is not None:
            for graphicsDetailName, graphicsDetailValue in graphicsDetail.iteritems():
                for detail in gdList:
                    detailID = detail[0]
                    if detailID == graphicsDetailName:
                        id = GAME_OPTIONS_STATS.__dict__.get(graphicsDetailName, None)
                        if id is not None:
                            container[id] = graphicsDetailValue
                        break

        self._checkForSubmit(container)
        return

    def _getStatType(self):
        return GAME_OPTIONS_STATS_TYPE.GAME_OPTIONS_STATS_GRAPHICS


class _SoundSettingsStats(_SettingsStatsBase):

    def fill(self):
        from clientConsts import SOUND_QUALITY_IDX_DICT, SOUND_SETTINGS_DICT
        import VOIP
        import Settings
        settings = Settings.g_instance
        container = dict()
        container[GAME_OPTIONS_STATS.IS_VOICE_CHAT_VISIBLE] = VOIP.api().voipSupported
        container[GAME_OPTIONS_STATS.IS_ARENA_VOICE_CHAT_VISIBLE] = VOIP.api().arenaChannelSupported
        container[GAME_OPTIONS_STATS.QUALITY_SOUND_INDEX] = SOUND_QUALITY_IDX_DICT[settings.getSoundSettings()['quality']]
        for flashKey, SettingsKey in SOUND_SETTINGS_DICT.iteritems():
            id = GAME_OPTIONS_STATS.__dict__.get('SOUND_SETTINGS_' + SettingsKey.upper(), None)
            if id is not None:
                container[id] = settings.getSoundSettings()['volume'][SettingsKey]

        for flashKey, SettingsKey in Settings.SOUND_PARAMETERS.iteritems():
            id = GAME_OPTIONS_STATS.__dict__.get('SOUND_PARAMETERS_' + SettingsKey.upper(), None)
            if id is not None:
                container[id] = settings.getSoundSettings()['volumeEnabled'][SettingsKey]

        voipPrefs = settings.getVoipSettings()
        for flashKey, SettingsKey in Settings.VOIP_PARAMETERS_DICT.iteritems():
            if SettingsKey == 'isVoipEnabled':
                container[GAME_OPTIONS_STATS.ENABLE_VOICE_CHAT] = voipPrefs[SettingsKey] and VOIP.api().voipSupported
            elif SettingsKey == 'captureDevice':
                pass
            else:
                id = GAME_OPTIONS_STATS.__dict__.get('VOIP_PARAMETERS_' + SettingsKey.upper(), None)
                if id is not None:
                    container[id] = voipPrefs[SettingsKey]

        self._checkForSubmit(container)
        return

    def _getStatType(self):
        return GAME_OPTIONS_STATS_TYPE.GAME_OPTIONS_STATS_SOUND


class _GameSettingsStats(_SettingsStatsBase):

    def _fillChat(self, container):
        from gui.Scaleform.GameOptions.utils import XMPP_CHAT_KEYS
        import Settings
        for flashKey, SettingsKey in XMPP_CHAT_KEYS.iteritems():
            id = GAME_OPTIONS_STATS.__dict__.get(SettingsKey.upper(), None)
            if id is not None:
                container[id] = Settings.g_instance.getXmppChatSettings()[SettingsKey]

        return

    def _fillReplays(self, container):
        import Settings
        for key in Settings.REPLAY_KEYS.iterkeys():
            id = GAME_OPTIONS_STATS.__dict__.get(key.upper(), None)
            if id is not None:
                container[id] = Settings.g_instance.getReplaySettings()[key]

        return

    def fill(self):
        container = dict()
        self._fillChat(container)
        self._fillReplays(container)
        self._checkForSubmit(container)

    def _getStatType(self):
        return GAME_OPTIONS_STATS_TYPE.GAME_OPTIONS_STATS_GAME


class SettingsStatsManager(_SettingsStatsBase):
    MAX_SEND_STATS_COUNT = 80
    MAX_SEND_STATS_LENGTH = 1536

    def __init__(self):
        _SettingsStatsBase.__init__(self)
        self.__data = list()
        self.__pendingData = list()
        self.__sendCallback = None
        self.__stats = [_ControlSettingsStats(),
         _BattleSettingsStats(),
         _GameSettingsStats(),
         _GraphicsSettingsStats(),
         _SoundSettingsStats()]
        return

    def fill(self):
        for stat in self.__stats:
            stat.fill()
            self.__data.extend(stat.container)

        self.destroy()

    def destroy(self):
        for stat in self.__stats:
            stat.destroy()

        self.__stats = []
        if self.__sendCallback is not None:
            BigWorld.cancelCallback(self.__sendCallback)
            self.__sendCallback = None
        return

    @property
    def data(self):
        return self.__data

    def sendStatsData(self, player):
        self.__pendingData.extend(self.data)
        self.__proccessSending(player)

    def __proccessSending(self, player):
        LOG_DEBUG('Send stats data', len(self.__pendingData), self.__pendingData)
        lenToSend = 0
        if not self.__pendingData:
            self.__sendCallback = None
            return
        else:
            for i, sData in enumerate(self.__pendingData):
                lenToSend += len(str(sData[1]))
                if i > self.MAX_SEND_STATS_COUNT or lenToSend > self.MAX_SEND_STATS_LENGTH:
                    break

            data = wgPickle.dumps(wgPickle.FromClientToServer, self.__pendingData[:i + 1])
            if len(data) > MAX_SEND_DATA_SIZE:
                LOG_ERROR('wrong stats data is to long, ingorred', len(data))
                self.__sendCallback = None
                return
            try:
                player.base.updateClientStats(CLIENT_STATS_TYPE.CLIENT_CONTROL, data)
            except:
                pass

            self.__pendingData = self.__pendingData[i + 1:]
            if self.__pendingData:
                self.__sendCallback = BigWorld.callback(0.25, partial(self.__proccessSending, player))
            else:
                self.__sendCallback = None
            return