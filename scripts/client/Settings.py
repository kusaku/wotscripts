# Embedded file name: scripts/client/Settings.py
import inspect
import BigWorld
BigWorld.gameLoadingScreenSetProgress(0.1)
import InputMapping
import gui.GraphicsPresets
from debug_utils import *
from ContactInfo import ContactInfo
BigWorld.gameLoadingScreenSetProgress(0.116)
import db.DBLogic
import ResMgr
from consts import ZOOM_TYPES_KEYS, INPUT_SYSTEM_STATE, INPUT_SYSTEM_PROFILES_LIST, DB_PATH, MEASUREMENT_SYSTEMS
from clientConsts import KEY_RESEARCH_TREE_NATION, KEY_RESEARCH_TREE_NATION_LIST, KEY_RESEARCH_TREE_DEV_NATION_LIST, DEFAULT_RESEARCH_NATION, DEFAULT_RESEARCH_NATION_LIST, DEFAULT_RESEARCH_DEV_NATION_LIST, CLASTERS, CombatScreenNames, COUNT_SKIP_INTRO_FOR_DISABLED
from gui.HUDconsts import HUD_MINISCREEN_TARGET_INFO, HUD_RADAR_POSITION
BigWorld.gameLoadingScreenSetProgress(0.145)
from Event import Event
import GameEnvironment
from copy import deepcopy
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from Helpers.i18n import localizeOptions
import SystemInfo
from WWISE_ import setVolume
from WWISE_ import setQuality
from WWISE_ import setSpeakerPreset
from gui.Scaleform.GameOptions.vo import MarkerSettings
from ProfileDiffer import getDataSectionNodeByName
g_instance = None
KEY_UPDATE_URL = 'updateUrl'
KEY_FAKE_MODEL = 'fakeModel'
KEY_CONTROL_MODE = 'controlMode'
KEY_LOGIN_INFO = 'loginInfo'
KEY_SCREEN_SIZE = 'screenSize'
KEY_VIDEO_MODE = 'videoMode'
KEY_LOBBY_TOOLTIP_DELAY = 'lobbyTooltipDelay'
KEY_SOUND_PREFERENCES = 'soundPrefs/'
KEY_SOUND_PREFERENCES_ENABLED = 'soundPrefsEnabled/'
APPLICATION_CLOSE_DELAY = 'closeApplicationDelay'
KEY_MESSENGER_PREFERENCES = 'messengerPrefs'
KEY_ACCOUNT_SETTINGS = 'accounts'
KEY_SHOW_STARTUP_MOVIE = 'showStartupMovie'
KEY_SHOW_LANGUAGE_BAR = 'showLangugeBar'
KEY_ENABLE_VOIP = 'enableVoIP'
KEY_LOG_PARSER = 'logParser'
KEY_VIBRATION = 'vibration'
KEY_ENABLE_EDGE_DETECT_AA = 'enableEdgeDetectAA'
KEY_ENABLE_MORTEM_POST_EFFECT = 'enableMortemPostEffect'
KEY_CLIENT_LOGGING = 'clientLogging'
KEY_GAME_UI = 'gameUI/'
KEY_VOIP_SETTINGS = 'voip/'
KEY_TUTORIAL = 'isTutorialWelcome'
KEY_RESEARCH_TREE = 'researchTree/'
KEY_AIMS_PROFILE = KEY_GAME_UI + 'aims_%s/'
KEY_MARKERS = 'markers/'
KEY_INPUT_PROFILES_PRESETS = 'inputProfilesPresets/'
KEY_XMPP_CHAT_SETTINGS = 'xmppChat/'
KEY_REPLAY_PREFERENCES = 'replayPrefs/'
KEY_TIME_FORMATED = 'timeFormated/%s'
KEY_HANGAR_SETTINGS = 'hangarSettings'
DEFAULT_USER_PREFS_PATH = DB_PATH + 'preferences.xml'
INPUT_PROFILES_PRESETS_PATH = DB_PATH + 'input_profiles_presets.xml'
MIN_SCREEN_WIDTH = 1280
MIN_SCREEN_HEIGHT = 768
MIN_NBIT_PER_PIXEL = 32
MIN_KULBICH_WIDTH = 1366
GS_AUTODETECT_INITED_KEY = 'gsAutodetectInited2'
AIMS_KEYS = {'crosshairTransparency': 1.0,
 'crosshairShape': 0,
 'crosshairColor': 0,
 'targetAreaTransparency': 0.4,
 'targetAreaShape': 0,
 'targetAreaColor': 1,
 'externalAimTransparency': 0.0,
 'externalAimShape': 0,
 'dynamycAim': True}
GAME_UI_MAIN_KEYS = {'measurementSystem': 0,
 'measurementSystems': ','.join(MEASUREMENT_SYSTEMS),
 'battleChatUnVisible': False,
 'mainDevices': 1,
 'mainDevicesLocationList': 0,
 'horizon': 0,
 'horizonList': 0,
 'horizonLocationList': 0,
 'players': 1,
 'damageSchema': 1,
 'damageSchemaLocationList': 0,
 'damageSchemaInputDamageList': 0,
 'heightMode': 1,
 'targetWindow': 1,
 'targetWindowList': 0,
 'MiniScreenPosY': HUD_MINISCREEN_TARGET_INFO[1],
 'curPlayerListState': 1,
 'maxPlayerListState': 5,
 'minPlayerListState': 1,
 'MiniScreenPosX': HUD_MINISCREEN_TARGET_INFO[0],
 'combatInterfaceType': 1,
 'combatScreenName': CombatScreenNames.GENERAL,
 'navigationWindowRadar': True,
 'navigationWindowMinimap': True,
 'speedometerAndVariometer': False,
 'radarPosX': HUD_RADAR_POSITION[0],
 'radarPosY': HUD_RADAR_POSITION[1],
 'minimapSize': 100,
 'minimapSizeInBattleLoadingScreen': 100,
 'collisionWarningSystem': True,
 'alternativeColorMode': False,
 'battleLoadingTabIndex': 0,
 'isSniperMode': False,
 'navigationWindowRange': 250.0,
 'isChatEnabled': True,
 'fastFM': True,
 'deflectionTest1': False}
VOIP_KEYS = {'isVoipEnabled': False,
 'autoConnectArenaChannel': True,
 'masterVolume': 0.8,
 'micVolume': 0.1,
 'fadeVolume': 0.5,
 'captureDevice': ''}
MAIN_KEYS = {'inputLiningEnable': 1,
 'cinemaCamera': 0,
 'cameraZoomType': ZOOM_TYPES_KEYS[0],
 'cameraEffectsEnabled': True,
 'showAdvancePoint': 1,
 'blockAltTAB': False,
 'blockWinButton': False,
 'preIntroEnabled': True,
 'preIntroCount': COUNT_SKIP_INTRO_FOR_DISABLED,
 'camTargetSensitivity': 0.0,
 'camZoomIndex': 1,
 'hardwareHash': 0,
 'graphicsDetails': 'Low',
 KEY_TUTORIAL: False,
 'mouseSensitivity': 0.5,
 GS_AUTODETECT_INITED_KEY: False,
 'gsAutodetectEnabled': True,
 'maxMouseCombatFov': 90.0,
 'controlStatsHash': 0,
 'gameStatsHash': 0,
 'hudStatsHash': 0,
 'soundStatsHash': 0,
 'graphicStatsHash': 0,
 'isToBoundaryFP': True,
 'isSizeFP': True,
 'isBestTimeFP': True,
 'colorPointIndexFP': 0}
XMPP_CHAT_KEYS = {'notListenToAnonymous': False,
 'disableOfflineContacts': False,
 'displayIgnoredContatcs': False,
 'messageFilterEnabled': True,
 'displayMessageTime': True}
REPLAY_KEYS = {'saveBattleReplays': False,
 'removeBattleReplays': True,
 'daysForRemoveBattleReplays': 30}
SOUND_PARAMETERS = {'isMasterVolume': 'master',
 'isMusicVolume': 'music',
 'isVoiceVolume': 'voice',
 'isVehicleVolume': 'aircraft',
 'isEffectsVolume': 'sfx',
 'isInterfaceVolume': 'ui',
 'isAmbientVolume': 'ambient',
 'isEngineVolume': 'engine',
 'isGunsVolume': 'guns'}
SOUND_VOLUME_PARAMETERS = dict(master=0.5, music=0.5, ui=0.5, aircraft=0.5, sfx=0.5, ambient=0.5, voice=0.5, engine=0.5, guns=0.5)
SOUND_VOLUME_RTPC = {'master': 'VOLUME_Master_Menu_Percent',
 'music': 'VOLUME_Music_Menu_Percent',
 'voice': 'VOLUME_VO_Menu_Percent',
 'aircraft': 'VOLUME_Aircraft_SFX_Menu_Percent',
 'sfx': 'VOLUME_Battle_SFX_Menu_Percent'}
VOIP_PARAMETERS_DICT = dict(enableArenaVoiceChat='autoConnectArenaChannel', voiceChatVoiceVolume='masterVolume', voiceChatMicrophoneSensitivity='micVolume', voiceChatAmbientVolume='fadeVolume', enableVoiceChat='isVoipEnabled', voiceChatMicDevice='captureDevice')
GRAPHICS_QUALITY_NAMES = {0: 'Very High',
 1: 'High',
 2: 'Medium',
 3: 'Low',
 4: 'Very Low'}
GRAPHICS_QUALITY_LOC_ID = {'VERYHIGH': 'SETTINGS_GRAPH_SETTINGS_CONTEXT_HIGHEST',
 'HIGH': 'SETTINGS_GRAPH_SETTINGS_CONTEXT_HIGH',
 'MEDIUM': 'SETTINGS_GRAPH_SETTINGS_CONTEXT_MEDIUM',
 'LOW': 'SETTINGS_GRAPH_SETTINGS_CONTEXT_LOW',
 'VERYLOW': 'SETTINGS_GRAPH_SETTINGS_CONTEXT_LOWEST',
 gui.GraphicsPresets.GraphicsPresets.CUSTOM_PRESET_KEY.upper(): 'SETTINGS_GRAPH_SETTINGS_CONTEXT_PERSONAL'}
DEFAULT_GRAPHICS_DICT = {'graphicsGamma': 0.5}
_SOUND_CATEGORY_DEFAULT = {'quality': 1,
 'speakerPreset': 0}

def _getHangarDefaultSettings():
    return {'spaceID': '',
     'eventsHash': '',
     'ignoreEventHangar': False,
     'selectedSpaces': {}}


class SETTINGS_AUTODETECT_KEYS():
    GS = 0
    GS_RESOLUTION = 1


class SETTINGS_AUTODETECT_RESULT():
    ERROR = 0
    OK = 1
    HIGHER = 2
    LOWER = 3


class Settings(object):

    def __init__(self, scriptConfig, engineConfig, userPrefs, customGraphicPrefs):
        self.scriptConfig = ScriptConfig(scriptConfig)
        self.engineConfig = engineConfig
        self.cmdFilter = list()
        self.resolutions = None
        self.resolutionIndex = -1
        self.__defaultSettings = SettingsDefault(customGraphicPrefs)
        self.userPrefs = userPrefs
        self.contactInfo = ContactInfo(userPrefs)
        self.graphicsPresets = gui.GraphicsPresets.GraphicsPresets(customGraphicPrefs)
        self._loadMains()
        self.inputProfilesPresets = self.__loadInputProfilesPresets()
        self.inputProfilesPresetsCurrent = self._loadCurrentInputProfilesPresets()
        self.__defaultSettings.inputProfilesPresets = deepcopy(self.inputProfilesPresets)
        self.__defaultSettings.inputProfilesPresetsCurrent = self.__defaultSettings._loadCurrentInputProfilesPresets()
        self.setGraphicsDetails(self.graphicsDetails)
        self.__isNeedSaveMarkers = False
        self.countTemplates = 0
        self.selectedMarkers = MarkerSettings.SELECTED_MARKERS_LIST[:]
        self.markersBaseData = self._loadBaseDataMarkers()
        self.__defaultMarkerPrefs = None
        MarkerSettings.createAppMarkerPath()
        self.markersTemplates = self._loadMarkers(MarkerSettings.PATH_MODIFY_MARKER + MarkerSettings.MARKERS_MODIFY_XML)
        self.aims = self.loadAims()
        curInputProfileName = userPrefs.readString('curInputProfileName', '')
        InputMapping.initInput(curInputProfileName, self.inputProfilesPresetsCurrent)
        InputMapping.g_instance.onProfileLoaded += self.__inputProfileChanged
        self.gameUI = self.loadGameUI()
        self._voipPrefs = self._loadVoipSettings()
        self.voipCaptureDevices = list()
        self.researchTreePrefs = self.__loadResearchTreePrefs()
        self._soundPrefs = {}
        self.loadSoundPrefs()
        self._xmppChatPrefs = self._loadXmppChatSettings()
        self._hangarSpaceSettings = self.__loadHangarSpaceSettings()
        if self.clusterID == CLASTERS.CN:
            self._xmppChatPrefs['messageFilterEnabled'] = False
        self._battleRaplaysPrefs = self._loadReplaySettings()
        self.__sysInfo = SystemInfo.SystemInfo()
        self.onMeasurementSystemChanged = Event()
        self.onNavWindowListChanged = Event()
        self.eChangeMiniScreenPosition = Event()
        self.eChangeRadarPosition = Event()
        self.eCollisionWarningSystemEnabled = Event()
        self.eAlternativeColorModeEnabled = Event()
        self.eCombatInterfaceType = Event()
        self.eMainDevicesVisibility = Event()
        self.eAviaHorizonType = Event()
        self.ePlayerListType = Event()
        self.eSetSniperMode = Event()
        self.eBattleChatSetVisible = Event()
        self.eCameraEffectsSetEnabled = Event()
        self.eDetectBestSettingsAdvStart = Event()
        self.eDetectBestSettingsAdvEnd = Event()
        self.eChangedGraphicsDetails = Event()
        self.eMaxMouseCombatFovChanged = Event()
        self.eGameChatEnabled = Event()
        self.eFastFM = Event()
        self.__gameUIEvents = dict(alternativeColorMode=self.eAlternativeColorModeEnabled, collisionWarningSystem=self.eCollisionWarningSystemEnabled, navigationWindowRadar=self.onNavWindowListChanged, navigationWindowMinimap=self.onNavWindowListChanged, combatInterfaceType=self.eCombatInterfaceType, mainDevices=self.eMainDevicesVisibility, horizonList=self.eAviaHorizonType, curPlayerListState=self.ePlayerListType, isSniperMode=self.eSetSniperMode, measurementSystem=self.onMeasurementSystemChanged, battleChatUnVisible=self.eBattleChatSetVisible, isChatEnabled=self.eGameChatEnabled, fastFM=self.eFastFM)
        self.__mainEvents = dict(cameraEffectsEnabled=self.eCameraEffectsSetEnabled, maxMouseCombatFov=self.eMaxMouseCombatFovChanged)
        self.__isContentChanged = self.userPrefs.readBool('content/isHD', False) != BigWorld.isHDContent()
        self.__isHardwareChanged = False
        self.__getHardware()
        return

    def changeLanguage(self, lang):
        if self.language != lang:
            self.language = lang
            from gui.WindowsManager import g_windowsManager
            g_windowsManager.updateLocalizationTable()
            GameEnvironment.g_instance.eChangeLanguage()

    def _checkMarkersVerison(self, path, basePath):
        if path != MarkerSettings.MARKERS_BASE_XML:
            res = ResMgr.openSection(path)
            if res:
                resBase = ResMgr.openSection(basePath)
                if resBase:
                    defaultVersion = Settings.loadData(resBase, 'version', 0)
                    actualVersion = Settings.loadData(res, 'version', 0)
                    if defaultVersion > actualVersion:
                        import ProfileDiffer
                        differ = ProfileDiffer.MarkerSectionsDiffer(resBase, res)
                        differ.applyDiff()
                    ResMgr.purge(basePath)
                ResMgr.purge(path)

    def _loadMarkers(self, path, basePath = MarkerSettings.MARKERS_BASE_XML):
        """
        load current markers settings from markerPath
        @return: dict
        """
        preMarkers = None
        if path != MarkerSettings.MARKERS_BASE_XML:
            preMarkers = self.__loadPreviewMarker()
        self.markers = preMarkers
        selectedPath = path
        self._checkMarkersVerison(path, basePath)
        markers = dict()
        res = ResMgr.openSection(path)
        if res is None:
            self.__isNeedSaveMarkers = True
            selectedPath = basePath
            res = ResMgr.openSection(basePath)
            self.__defaultMarkerPrefs = res
        if res:
            base = getDataSectionNodeByName(res, 'base')
            lMarkers = Settings.loadData(res, 'select', ','.join([ str(v) for v in MarkerSettings.SELECTED_MARKERS_LIST ])).lstrip().split(',')
            try:
                for i, v in enumerate(lMarkers):
                    self.selectedMarkers[i] = int(float(v))

            except:
                self.__isNeedSaveMarkers = True
                self.selectedMarkers = MarkerSettings.SELECTED_MARKERS_LIST

            for targetMarker in base.values():
                markers[targetMarker.name] = dict()
                for typeMarker in targetMarker.values():
                    markers[targetMarker.name][typeMarker.name] = dict()
                    for altState in typeMarker.values():
                        markers[targetMarker.name][typeMarker.name][altState.name] = dict()
                        for param in altState.values():
                            value = Settings.loadData(altState, param.name, '')
                            arr = value.lstrip().split(',')
                            try:
                                arr = [ int(el) for el in arr ]
                            except:
                                LOG_ERROR('_loadMarkers', arr, value, targetMarker.name, typeMarker.name, altState.name)

                            if self.countTemplates == 0:
                                self.countTemplates = len(arr)
                            if preMarkers is not None:
                                arr = MarkerSettings.convertMarkersVersion(targetMarker.name, typeMarker.name, altState.name, param.name, preMarkers, arr)
                            markers[targetMarker.name][typeMarker.name][altState.name][param.name] = arr

            if preMarkers is not None:
                self.__isNeedSaveMarkers = True
                self.selectedMarkers = [4,
                 5,
                 6,
                 7]
            ResMgr.purge(selectedPath, True)
        return markers

    def __loadPreviewMarker(self):
        preMarkers = None
        if self.userPrefs.has_key(KEY_MARKERS) == 1:
            preMarkers = dict()
            for markersType in MarkerSettings.OLD_MARKERS_TYPES:
                preMarkers[markersType] = dict()
                for markersSubType in MarkerSettings.OLD_MARKERS_SUB_TYPES:
                    prePath = ''.join([KEY_MARKERS,
                     markersType,
                     '/',
                     markersSubType,
                     '/%s'])
                    preMarkers[markersType][markersSubType] = dict()
                    for markersKey, defaultValue in MarkerSettings.OLD_MARKERS_ATTRIBUTES.items():
                        preMarkers[markersType][markersSubType][markersKey] = Settings.loadData(self.userPrefs, prePath % markersKey, defaultValue)

            self.userPrefs.deleteSection('markers')
        return preMarkers

    def getOriginMarker(self, targetType, target, isFriend = False):
        pass

    def getAltMarker(self, typePlane, typeTarget, isFriend = False):
        pass

    def getMarkerSettings(self, indexPlane, entityTypeStr, markerType, altState):
        templateId = self.selectedMarkers[indexPlane]
        if templateId >= self.countTemplates:
            setting = self.markersTemplates
            templateId = templateId - self.countTemplates
        else:
            setting = self.defaultMain.markersTemplates
        attributeValueIndexes = setting[entityTypeStr][markerType][altState]
        measurementSystem = self.gameUI['measurementSystem']
        result = {}
        for attr, attrData in attributeValueIndexes.iteritems():
            attrBaseValues = self.markersBaseData.get(attr)
            if attrBaseValues is not None:
                attrMarkerValues = attrBaseValues[entityTypeStr]['list']
                attrDataIndex = int(attrData[templateId])
                if attrDataIndex < 0:
                    attrValue = -2
                else:
                    attrValue = MarkerSettings.getValueBySystem(measurementSystem, attrMarkerValues[attrDataIndex])
                result[attr] = attrValue
            else:
                LOG_WARNING('getMarkerSettings - attr not found in markersBaseData', attr, altState, entityTypeStr, markerType)

        return result

    def __setBaseMarkers(self, mDict, param):
        isDict = False
        mDict[param.name] = dict()
        data = param.child(0)
        if data.name in MarkerSettings.MARKER_TARGET_TYPE:
            isDict = True
            for prop in param.values():
                mDict[param.name][prop.name] = dict()
                mDict[param.name][prop.name]['label'] = Settings.loadData(prop, 'label', '__empty__')
                mDict[param.name][prop.name]['tooltip'] = Settings.loadData(prop, 'tooltip', '__empty__')
                mDict[param.name][prop.name]['list'] = prop.readStrings('num')

        if isDict == False:
            tLabel = Settings.loadData(param, 'label', '__empty__')
            tTootltip = Settings.loadData(param, 'tooltip', '__empty__')
            tList = param.readStrings('num')
            for typeTarget in MarkerSettings.MARKER_TARGET_TYPE:
                mDict[param.name][typeTarget] = dict()
                mDict[param.name][typeTarget]['label'] = tLabel
                mDict[param.name][typeTarget]['tooltip'] = tTootltip
                mDict[param.name][typeTarget]['list'] = tList

        return mDict

    def _loadBaseDataMarkers(self):
        markers = dict()
        res = ResMgr.openSection(MarkerSettings.MARKERS_DATA_XML)
        if res:
            stepsDistance = getDataSectionNodeByName(res, 'stepsDistance')
            sArrDistance = stepsDistance.readStrings('num')
            MarkerSettings.createMarkerParams(sArrDistance)
            base = getDataSectionNodeByName(res, 'base')
            metrMatrix = getDataSectionNodeByName(res, 'matrix_metr')
            footMatrix = getDataSectionNodeByName(res, 'matrix_foot')
            metrMatrixArr = dict()
            footMatrixArr = dict()
            for param in metrMatrix.values():
                metrMatrixArr[param.name] = Settings.loadData(metrMatrix, param.name, -1)

            for param in footMatrix.values():
                footMatrixArr[param.name] = Settings.loadData(footMatrix, param.name, -1)

            MarkerSettings.setMatrixSystem(metrMatrixArr, footMatrixArr)
            for param in base.values():
                markers = self.__setBaseMarkers(markers, param)

            ResMgr.purge(MarkerSettings.MARKERS_DATA_XML, True)
        return markers

    def saveMarkers(self, vehicleType, targetType, altState, key, indexTemplate, value):
        self.__isNeedSaveMarkers = True
        self.markersTemplates[vehicleType][targetType][altState][key][indexTemplate] = value

    def setMarkerSelectID(self, index, id):
        self.__isNeedSaveMarkers = True
        self.selectedMarkers[index] = id

    def __saveMarkers(self, path):
        if self.__isNeedSaveMarkers:
            res = ResMgr.openSection(path, True)
            if self.__defaultMarkerPrefs:
                res.copy(self.__defaultMarkerPrefs)
                res.save()
            if res:
                base = getDataSectionNodeByName(res, 'base')
                rMarker = ','.join(map(str, self.selectedMarkers))
                Settings.saveData(res, 'select', ','.join([ str(v) for v in MarkerSettings.SELECTED_MARKERS_LIST ]), rMarker)
                for targetMarker in base.values():
                    for typeMarker in targetMarker.values():
                        for altState in typeMarker.values():
                            for param in altState.values():
                                mTValues = list()
                                for mTValue in self.markersTemplates[targetMarker.name][typeMarker.name][altState.name][param.name]:
                                    mTValues.append(str(mTValue))

                                rStr = ','.join(mTValues)
                                Settings.saveData(altState, param.name, '__empty__', rStr)

                try:
                    res.save()
                    self.__isNeedSaveMarkers = False
                except IOError:
                    LOG_ERROR("Couldn't save:" + MarkerSettings.MARKERS_MODIFY_XML)

                if self.__defaultMarkerPrefs:
                    self.__defaultMarkerPrefs = None
            ResMgr.purge(path, True)
        return

    def __loadHangarSpaceSettings(self):
        hangarSpaceSettings = {}
        for item in next((pref for name, pref in self.userPrefs.items() if name == KEY_HANGAR_SETTINGS), {}).items():
            itemDict = _getHangarDefaultSettings()
            itemDict.update(dict(((k, v.asString if k != 'ignoreEventHangar' else v.asBool) for k, v in item[1].items())))
            if 'accID' in itemDict:
                hangarSpaceSettings[itemDict['accID']] = itemDict

        return hangarSpaceSettings

    def __saveHangarSpaceSettings(self):
        localSettings = self._hangarSpaceSettings.copy()
        for _, itemData in next((pref for name, pref in self.userPrefs.items() if name == KEY_HANGAR_SETTINGS), {}).items():
            data = localSettings.pop(itemData.readString('accID'))
            itemData.writeString('spaceID', data.get('spaceID', ''))
            itemData.writeString('eventsHash', data.get('eventsHash', ''))
            itemData.writeBool('ignoreEventHangar', data.get('ignoreEventHangar', False))

        for accID, newData in localSettings.iteritems():
            newsection = self.userPrefs.createSection('{0}/hangar'.format(KEY_HANGAR_SETTINGS))
            newsection.writeString('accID', accID)
            newsection.writeString('spaceID', newData.get('spaceID', ''))
            newsection.writeString('eventsHash', newData.get('eventsHash', ''))
            newsection.writeBool('ignoreEventHangar', newData.get('ignoreEventHangar', False))

    def getHangarSpaceSettings(self, accID):
        accIDstr = str(accID)
        defaultDict = _getHangarDefaultSettings()
        defaultDict['accID'] = accIDstr
        return self._hangarSpaceSettings.setdefault(accIDstr, defaultDict)

    def updatePointerVisibility(self):
        if hasattr(InputMapping.g_instance, 'primarySettings'):
            cameraType = getattr(InputMapping.g_instance.primarySettings, 'CAMERA_TYPE', None)
            if cameraType == 1:
                self.setAimsData('externalAimTransparency', 0.0)
            elif cameraType == 0:
                self.setAimsData('externalAimTransparency', 1.0)
            elif cameraType == 2:
                self.setAimsData('externalAimTransparency', 1.0)
            else:
                self.setAimsData('externalAimTransparency', 0.0)
        return

    def __inputProfileChanged(self):
        self.updatePointerVisibility()

    def fini(self):
        InputMapping.g_instance.saveControlls()
        InputMapping.g_instance.fini()
        InputMapping.g_instance.onProfileLoaded -= self.__inputProfileChanged
        self.__gameUIEvents = dict()
        self.__mainEvents = dict()
        self.save()

    def save(self):
        """
        Save preferences
        """
        import BattleReplay
        if not BattleReplay.isPlaying():
            self.__saveCurrentInputProfilesPresets()
        for key, defaultValue in MAIN_KEYS.items():
            Settings.saveData(self.userPrefs, key, defaultValue, getattr(self, key))

        self.userPrefs.writeBool('content/isHD', BigWorld.isHDContent())
        if not BattleReplay.isPlaying():
            self.userPrefs.writeString('curInputProfileName', InputMapping.g_instance.getCurProfileName())
            self.saveGameUI()
        self.saveAims()
        self.__saveVoipSettings()
        self.saveResearchTreePrefs()
        self.__saveSoundPrefs()
        self.__saveXmppChatSettings()
        self.__saveReplaySettings()
        self.__saveMarkers(MarkerSettings.PATH_MODIFY_MARKER + MarkerSettings.MARKERS_MODIFY_XML)
        self.__saveHangarSpaceSettings()
        LOG_DEBUG('Save settings')
        BigWorld.savePreferences()
        self.updateBlockSystemKeys()

    def setGraphicsDetailsSD(self):
        sdGraphicsSettings = dict()
        graphicsDetail = self.graphicsPresets.getPresetValues().get(self.defaultMain.graphicsDetails.lower(), None)
        if graphicsDetail is not None:
            for graphicsDetailName, graphicsDetailValue in graphicsDetail.iteritems():
                sdGraphicsSettings[graphicsDetailName] = graphicsDetailValue

        sdGraphicsSettings['TEXTURE_QUALITY'] = 1
        self.changeGraphicsDetails(self.graphicsPresets.CUSTOM_PRESET_KEY, sdGraphicsSettings)
        self.eChangedGraphicsDetails()
        return

    def changeGraphicsDetails(self, graphicsQualityName, customGraphicsSettings):
        self.graphicsDetails = graphicsQualityName
        LOG_DEBUG('Applying graphics details preset', graphicsQualityName)
        applyPresets = self.graphicsPresets.checkApplyGraphicsPreset(self.graphicsDetails, customGraphicsSettings)
        if applyPresets:
            if graphicsQualityName == self.graphicsPresets.CUSTOM_PRESET_KEY:
                self.graphicsPresets.setCustomGraphicsSettings(customGraphicsSettings)
            self.setGraphicsDetails(graphicsQualityName)

    def setGraphicsDetails(self, graphicsQualityName):
        self.graphicsPresets.applyGraphicsPresets(graphicsQualityName)
        BigWorld.commitPendingGraphicsSettings()
        BigWorld.savePreferences()

    def getGraphicsPresetKeys(self):
        return self.graphicsPresets.getPresetKeys()

    def _isVideoModeCorrect(self, videoMode):
        return videoMode[1] >= MIN_SCREEN_WIDTH and videoMode[2] >= MIN_SCREEN_HEIGHT and videoMode[3] >= MIN_NBIT_PER_PIXEL

    def getVideoResolutions(self):
        actualSize = BigWorld.windowSize()
        curVideoMode = BigWorld.videoModeIndex()
        modes = BigWorld.listVideoModes()
        width, height = int(actualSize[0]), int(actualSize[1])
        actualMode = '{0}x{1}x{2}'.format(width, height, MIN_NBIT_PER_PIXEL)
        list = []
        currentResolution = -1
        for i, mode in enumerate(filter(self._isVideoModeCorrect, modes)):
            list.append(mode[4])
            if mode[4] == actualMode:
                currentResolution = i

        if currentResolution == -1:
            list.append(actualMode)
            currentResolution = len(list) - 1
        return (list, currentResolution)

    def changeVideoMode(self, newResolutionId, isFullScreen, isBorderless = False):
        modeId = -1
        modes = BigWorld.listVideoModes()
        for i, mode in enumerate(filter(self._isVideoModeCorrect, modes)):
            if newResolutionId == i:
                modeId = mode[0]
                break

        from clientConsts import WINDOW_RENDER_MODE
        mode = WINDOW_RENDER_MODE.WRM_WINDOWED
        if isBorderless:
            mode = WINDOW_RENDER_MODE.WRM_BORDERLESS
        elif isFullScreen:
            mode = WINDOW_RENDER_MODE.WRM_FULLSCREEN
        BigWorld.changeVideoMode(modeId, mode)

    def isFullScreen(self):
        return not BigWorld.isVideoWindowed()

    def getWindowMode(self):
        return BigWorld.currentWindowMode()

    def setVideoVSync(self, waitVSync):
        if waitVSync != self.isVideoVSync():
            LOG_DEBUG('VideoVSync set to: %s' % str(waitVSync))
            BigWorld.setVideoVSync(waitVSync)
            BigWorld.changeVideoMode(-1, BigWorld.currentWindowMode())

    def isVideoVSync(self):
        return BigWorld.isVideoVSync()

    def setGamma(self, gamma):
        if gamma != self.getGamma():
            LOG_DEBUG('setGamma to: %s' % str(gamma))
            BigWorld.setGamma(gamma)

    def getGamma(self):
        return BigWorld.getGamma()

    def getMasterVolume(self):
        return self._soundPrefs['volume']['master']

    def getAvionicaState(self):
        return self.userPrefs.readInt('gameUI/avionica/state', 1)

    def setAvionicaState(self, state):
        self.userPrefs.writeInt('gameUI/avionica/state', state)

    def _loadMains(self):
        for key, defaultValue in MAIN_KEYS.items():
            setattr(self, key, Settings.loadData(self.userPrefs, key, defaultValue))

    @property
    def defaultMain(self):
        return self.__defaultSettings

    def setMain(self, key, value):
        if key in MAIN_KEYS.iterkeys() and getattr(self, key) != value:
            setattr(self, key, value)
            if key in self.__mainEvents:
                self.__mainEvents[key](value)
        else:
            LOG_ERROR('setMain - bad key or current value = new value', key, value)

    def __loadInputProfilesPresets(self):
        d = dict()
        res = ResMgr.openSection(INPUT_PROFILES_PRESETS_PATH)
        if res:
            for profilePresetObject in res.values():
                d[profilePresetObject.name] = list()
                for presetObject in profilePresetObject.values():
                    d[profilePresetObject.name].append(dict(name=presetObject.name, localizationID=presetObject.asString))

            ResMgr.purge(INPUT_PROFILES_PRESETS_PATH, True)
        return d

    def _loadCurrentInputProfilesPresets(self):
        return dict([ (profileName, Settings.loadData(self.userPrefs, KEY_INPUT_PROFILES_PRESETS + profileName, profileObject[0]['name'])) for profileName, profileObject in self.inputProfilesPresets.iteritems() ])

    def __saveCurrentInputProfilesPresets(self):
        for profileName, profileObject in self.inputProfilesPresets.iteritems():
            Settings.saveData(self.userPrefs, KEY_INPUT_PROFILES_PRESETS + profileName, profileObject[0]['name'], self.inputProfilesPresetsCurrent[profileName])

    def loadGameUI(self):
        return dict([ (key, Settings.loadData(self.userPrefs, KEY_GAME_UI + key, defaultValue)) for key, defaultValue in GAME_UI_MAIN_KEYS.items() ])

    def saveGameUI(self):
        for key, defaultValue in GAME_UI_MAIN_KEYS.items():
            Settings.saveData(self.userPrefs, KEY_GAME_UI + key, defaultValue, self.gameUI[key])

    def getGameUI(self):
        return self.gameUI

    def getFastFMEnabled(self):
        import BattleReplay
        return self.gameUI['fastFM'] and not BattleReplay.isPlaying()

    def getDefaultGameUI(self):
        return self.__defaultSettings.gameUI

    def setGameUIValue(self, key, val):
        if self.gameUI.has_key(key) and self.gameUI[key] != val:
            self.gameUI[key] = val
            if key in self.__gameUIEvents:
                self.__gameUIEvents[key](val)
        else:
            LOG_ERROR('Cannot set a game UI value', key, val)

    def loadAims(self):

        def readAimsData(root, sectionName, needCheck = False):
            array = {}
            for key, defaultValue in AIMS_KEYS.items():
                if needCheck and not root.has_key(sectionName % key):
                    continue
                array[key] = Settings.loadData(root, sectionName % key, defaultValue)

            return array

        mainAimsData = {}
        for profileName in INPUT_SYSTEM_PROFILES_LIST.keys():
            mainAimsData[profileName] = readAimsData(self.userPrefs, KEY_AIMS_PROFILE % profileName + '%s')

        return mainAimsData

    def saveAims(self):

        def saveAimsData(root, sectionName, container, needCheck = False):
            for key, defaultValue in AIMS_KEYS.items():
                if needCheck and key not in container:
                    continue
                Settings.saveData(root, sectionName % key, defaultValue, container[key])

        for profileName in INPUT_SYSTEM_PROFILES_LIST.keys():
            saveAimsData(self.userPrefs, KEY_AIMS_PROFILE % profileName + '%s', self.aims[profileName])

    def getAimsData(self):
        return self.getAimsDataByProfile(InputMapping.g_instance.getCurProfileName())

    def getAimsDataByProfile(self, profileName):
        if profileName in self.aims:
            return dict([ (key, self.aims[profileName][key]) for key in AIMS_KEYS.keys() ])
        else:
            LOG_ERROR('getAimsData - curProfileName(%s) not in self.aims' % profileName)
            return None
            return None

    def setAimsDataByProfile(self, key, value, profileName):
        if key in AIMS_KEYS.keys():
            if profileName in self.aims:
                self.aims[profileName][key] = value
            else:
                LOG_ERROR('setAimsData - curProfileName(%s) not in self.aims' % profileName)
        else:
            LOG_ERROR('setAimsData - error key=%s' % key)

    def setAimsData(self, key, value):
        self.setAimsDataByProfile(key, value, InputMapping.g_instance.getCurProfileName())

    def changeMiniScreenPosition(self, posX, posY):
        LOG_DEBUG('ChangeMiniScreenPosition', posX, posY)
        self.gameUI['MiniScreenPosX'], self.gameUI['MiniScreenPosY'] = posX, posY
        self.eChangeMiniScreenPosition()

    def changeRadarPosition(self, posX, posY):
        LOG_DEBUG('changeRadarPosition', posX, posY)
        self.gameUI['radarPosX'], self.gameUI['radarPosY'] = posX, posY
        self.eChangeRadarPosition()

    def _loadVoipSettings(self):
        return dict([ (key, Settings.loadData(self.userPrefs, KEY_VOIP_SETTINGS + key, defaultValue)) for key, defaultValue in VOIP_KEYS.items() ])

    def __saveVoipSettings(self):
        for key, defaultValue in VOIP_KEYS.items():
            Settings.saveData(self.userPrefs, KEY_VOIP_SETTINGS + key, defaultValue, self._voipPrefs[key])

    @staticmethod
    def loadData(root, sectionName, defaultValue):
        if root is None or not root.has_key(sectionName):
            LOG_DEBUG("loadData - root is None or sectionName not found '%s' = %s" % (sectionName, defaultValue))
            return defaultValue
        elif isinstance(defaultValue, float):
            return root.readFloat(sectionName, defaultValue)
        elif isinstance(defaultValue, bool):
            return root.readBool(sectionName, defaultValue)
        elif isinstance(defaultValue, str):
            return root.readString(sectionName, defaultValue)
        elif isinstance(defaultValue, int):
            return root.readInt(sectionName, defaultValue)
        else:
            LOG_ERROR('load - undefined type of defaultValue', defaultValue)
            return
            return

    @staticmethod
    def saveData(root, sectionName, defaultValue, value):
        if isinstance(defaultValue, float):
            root.writeFloat(sectionName, value)
        elif isinstance(defaultValue, bool):
            root.writeBool(sectionName, value)
        elif isinstance(defaultValue, str):
            root.writeString(sectionName, value)
        elif isinstance(defaultValue, int):
            root.writeInt(sectionName, value)
        else:
            LOG_ERROR('save - undefined type of defaultValue', defaultValue)

    def getVoipSettings(self):
        return self._voipPrefs

    def setVoipValue(self, key, val):
        if self._voipPrefs.has_key(key):
            self._voipPrefs[key] = val
        else:
            LOG_ERROR('Cannot set a voip value', key, val)

    def setSoundSpeakerPreset(self, value):
        """
        see values in enum SpeakerPresets
        """
        LOG_DEBUG('setSoundSpeakerPreset', value)
        self._soundPrefs['speakerPreset'] = value
        setSpeakerPreset(value)
        self.updateSoundCategories()

    def setQualitySound(self, quality):
        self._soundPrefs['quality'] = quality
        setQuality(quality)
        self.updateSoundCategories()

    def saveResearchTreePrefs(self):
        self.userPrefs.writeInt(''.join([KEY_RESEARCH_TREE, KEY_RESEARCH_TREE_NATION]), self.researchTreePrefs[KEY_RESEARCH_TREE_NATION])

    def __loadResearchTreePrefs(self):
        return {KEY_RESEARCH_TREE_NATION: self.userPrefs.readInt(''.join([KEY_RESEARCH_TREE, KEY_RESEARCH_TREE_NATION]), self.scriptConfig.researchTreePrefs[KEY_RESEARCH_TREE_NATION])}

    def getResearchTreeValue(self, key):
        if self.researchTreePrefs.has_key(key):
            return self.researchTreePrefs[key]
        elif self.scriptConfig.researchTreePrefs.has_key(key):
            return self.scriptConfig.researchTreePrefs[key]
        else:
            LOG_ERROR('Cannot find a researchTreePrefs value for', key)
            return None
            return None

    def setResearchTreeValue(self, key, val):
        if self.researchTreePrefs.has_key(key):
            self.researchTreePrefs[key] = val
        else:
            LOG_ERROR('Cannot set a researchTreePrefs value for', key)

    def loadSoundPrefs(self):
        self._soundPrefs['volume'] = dict([ (categoryName, self.userPrefs.readFloat(KEY_SOUND_PREFERENCES + categoryName, defaultValue)) for categoryName, defaultValue in SOUND_VOLUME_PARAMETERS.iteritems() ])
        self._soundPrefs['volumeEnabled'] = dict([ (volumeKey, self.userPrefs.readBool(KEY_SOUND_PREFERENCES_ENABLED + settKey, True)) for settKey, volumeKey in SOUND_PARAMETERS.iteritems() ])
        for categoryName, default in _SOUND_CATEGORY_DEFAULT.iteritems():
            self._soundPrefs[categoryName] = self.userPrefs.readInt(KEY_SOUND_PREFERENCES + categoryName, default)

        self._applySoundPrefs()

    def _applySoundPrefs(self):
        self.updateSoundCategories()
        speakerPreset = self._soundPrefs.get('speakerPreset', None)
        if speakerPreset is not None:
            setSpeakerPreset(speakerPreset)
            LOG_DEBUG('setSpeakerPreset', speakerPreset)
        return

    def __saveSoundPrefs(self):
        for categoryName, value in self._soundPrefs['volume'].iteritems():
            Settings.saveData(self.userPrefs, KEY_SOUND_PREFERENCES + categoryName, SOUND_VOLUME_PARAMETERS[categoryName], value)

        for settKey, volumeKey in SOUND_PARAMETERS.iteritems():
            self.userPrefs.writeBool(KEY_SOUND_PREFERENCES_ENABLED + settKey, self._soundPrefs['volumeEnabled'][volumeKey])

        for categoryName in _SOUND_CATEGORY_DEFAULT.keys():
            self.userPrefs.writeInt(KEY_SOUND_PREFERENCES + categoryName, self._soundPrefs[categoryName])

        self.updateSoundCategories()

    def updateSoundCategories(self):
        for category, value in self._soundPrefs['volume'].iteritems():
            self.__setSndSysCategoryVolume(category, value)

        for category, value in self._soundPrefs['volumeEnabled'].iteritems():
            self.__setSndSysCategoryEnabled(category, value)

    def setCategoryVolume(self, key, val):
        volumePrefs = self._soundPrefs['volume']
        if volumePrefs.has_key(key):
            if abs(volumePrefs[key] - val) > 0.0001:
                volumePrefs[key] = val
                self.__setSndSysCategoryVolume(key, val)
        else:
            LOG_ERROR('Cannot set a sound category volume', key, val)

    def setCategoryEnabled(self, key, val):
        enabledPrefs = self._soundPrefs['volumeEnabled']
        if enabledPrefs.has_key(key):
            if enabledPrefs[key] != val:
                enabledPrefs[key] = val
                self.__setSndSysCategoryEnabled(key, val)
        else:
            LOG_ERROR('Cannot switch a sound category', key, val)

    def getSoundSettings(self):
        return self._soundPrefs

    def __setSndSysCategoryVolume(self, categoryName, newValue):
        if categoryName in SOUND_VOLUME_RTPC:
            setVolume(categoryName, SOUND_VOLUME_RTPC[categoryName], 100.0 * newValue)

    def __setSndSysCategoryEnabled(self, categoryName, newValue):
        if categoryName in SOUND_VOLUME_RTPC:
            volumePrefs = self._soundPrefs['volume']
            setVolume(categoryName, SOUND_VOLUME_RTPC[categoryName], 100.0 * volumePrefs[categoryName] if newValue else 0)

    def _loadXmppChatSettings(self):
        return dict([ (key, Settings.loadData(self.userPrefs, KEY_XMPP_CHAT_SETTINGS + key, defaultValue)) for key, defaultValue in XMPP_CHAT_KEYS.iteritems() ])

    def __saveXmppChatSettings(self):
        for key, defaultValue in XMPP_CHAT_KEYS.iteritems():
            Settings.saveData(self.userPrefs, KEY_XMPP_CHAT_SETTINGS + key, defaultValue, self._xmppChatPrefs[key])

    def getXmppChatSettings(self):
        return self._xmppChatPrefs

    def setXmppChatValue(self, key, val):
        if self._xmppChatPrefs.has_key(key):
            self._xmppChatPrefs[key] = val
        else:
            LOG_ERROR('Cannot set a xmpp chat value', key, val)

    def getReplaysDirectory(self):
        return BigWorld.getReplaysDirectory()

    def setReplaysDirectory(self, path):
        pass

    def _loadReplaySettings(self):
        return dict([ (key, Settings.loadData(self.userPrefs, KEY_REPLAY_PREFERENCES + key, defaultValue)) for key, defaultValue in REPLAY_KEYS.iteritems() ])

    def __saveReplaySettings(self):
        for key, defaultValue in REPLAY_KEYS.iteritems():
            Settings.saveData(self.userPrefs, KEY_REPLAY_PREFERENCES + key, defaultValue, self._battleRaplaysPrefs[key])

    def getReplaySettings(self):
        return self._battleRaplaysPrefs

    def setReplayValue(self, key, val):
        if self._battleRaplaysPrefs.has_key(key):
            self._battleRaplaysPrefs[key] = val
        else:
            LOG_ERROR('Cannot set a battle Raplays value', key, val)

    def blockSystemKeys(self, block):
        if block:
            BigWorld.BlockSystemKeys(self.blockAltTAB, self.blockWinButton)
            LOG_DEBUG('Settings: blockSystemKeys(True)')
        else:
            BigWorld.BlockSystemKeys(False, False)
            LOG_DEBUG('Settings: blockSystemKeys(False)')

    def updateBlockSystemKeys(self):
        player = BigWorld.player()
        b = player is not None and player.__class__.__name__ == 'PlayerAvatar'
        self.blockSystemKeys(b)
        return

    @property
    def clusterID(self):
        return self.scriptConfig.clusterID

    @property
    def isCameraFreezEnabled(self):
        """
        used only for GAMEPAD and JOYSTICK
        @return: bool
        """
        if InputMapping.g_instance.currentProfileType in [INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL, INPUT_SYSTEM_STATE.JOYSTICK]:
            return InputMapping.g_instance.primarySettings.IS_CAMERA_FREEZ_ENABLED
        return False

    def getURLTokensHelp(self):
        return self.scriptConfig.urls['urlTokensHelp']

    def getIndexByValueGraphicsDetails(self, value):
        graphicsPresetKeys = list(self.getGraphicsPresetKeys())
        for i in range(0, len(graphicsPresetKeys)):
            if graphicsPresetKeys[i].lower() == value.lower():
                return i

        return None

    @property
    def graphicsDetailsBest(self):
        bestSettingsIndex = BigWorld.detectBestSettings()
        graphicsDetails = GRAPHICS_QUALITY_NAMES.get(bestSettingsIndex, None)
        if graphicsDetails is None:
            graphicsDetails = 'Very Low'
            LOG_WARNING('graphicsDetailsBest - index(%s) not in GRAPHICS_QUALITY_NAMES' % bestSettingsIndex)
        return graphicsDetails

    def getControlType(self):
        return 'current'

    def hardwaresRating(self):
        return self.__sysInfo.rating

    def __getHardware(self):
        self.hardwares = self.__sysInfo.hardwareInfo
        s = ''
        for hardware in self.hardwares:
            s += hardware

        hardwareHash = hash(s)
        self.__isHardwareChanged = self.hardwareHash != 0 and hardwareHash != self.hardwareHash
        self.hardwareHash = hardwareHash

    def isHardwareChanged(self):
        return self.__isHardwareChanged

    def isContentChanged(self):
        return self.__isContentChanged

    def detectBestSettingsAdv(self):
        self.eDetectBestSettingsAdvStart()
        self.__sysInfo.detect(self.__detectBestSettingsAdvCallback)

    def __detectBestSettingsAdvCallback(self, args = None):
        if args is not None:
            self.defaultMain.graphicsDetails = GRAPHICS_QUALITY_NAMES.get(args, 'Very Low')
            LOG_INFO('Recommended preset is: ' + self.defaultMain.graphicsDetails)
            if args >= len(GRAPHICS_QUALITY_NAMES):
                self.resolutions, self.resolutionIndex = self.getVideoResolutions()
                self.defaultMain.resolutionIndex = self.resolutionIndex
                resList = [ list(map(int, r.split('x'))) for r in self.resolutions ]
                minRes = resList[0]
                maxRes = resList[-1]
                if maxRes[0] > MIN_KULBICH_WIDTH:
                    self.defaultMain.resolutionIndex = 0
                    expectedHeight = minRes[0] * maxRes[1] / maxRes[0]
                    if expectedHeight > minRes[1]:
                        for i, res in enumerate(resList):
                            if res[1] == expectedHeight:
                                self.defaultMain.resolutionIndex = i
                                break

        self.eDetectBestSettingsAdvEnd()
        return

    def applyAutodetect(self, key):
        if key == SETTINGS_AUTODETECT_KEYS.GS:
            self.changeGraphicsDetails(self.defaultMain.graphicsDetails, {})
            self.eChangedGraphicsDetails()
        elif key == SETTINGS_AUTODETECT_KEYS.GS_RESOLUTION:
            resolutionIndex = getattr(self.defaultMain, 'resolutionIndex', None)
            if resolutionIndex is not None:
                self.changeVideoMode(resolutionIndex, not BigWorld.isVideoWindowed())
        return

    def getAutodetect(self, key):
        """
        @param key: <SETTINGS_AUTODETECT_KEYS>
        @return: object
        """
        if key == SETTINGS_AUTODETECT_KEYS.GS:
            return self.__gSAutodetect()
        elif key == SETTINGS_AUTODETECT_KEYS.GS_RESOLUTION:
            return self.__gSResolutionAutodetect()
        else:
            return (SETTINGS_AUTODETECT_RESULT.ERROR, None, None)

    def __gSResolutionAutodetect(self):
        if not self.resolutions or self.resolutionIndex < 0:
            return (SETTINGS_AUTODETECT_RESULT.ERROR, None, None)
        elif self.resolutionIndex > self.defaultMain.resolutionIndex:
            return (SETTINGS_AUTODETECT_RESULT.HIGHER, self.resolutions[self.resolutionIndex], self.resolutions[self.defaultMain.resolutionIndex])
        elif self.resolutionIndex < self.defaultMain.resolutionIndex:
            return (SETTINGS_AUTODETECT_RESULT.LOWER, self.resolutions[self.resolutionIndex], self.resolutions[self.defaultMain.resolutionIndex])
        else:
            return (SETTINGS_AUTODETECT_RESULT.OK, self.resolutions[self.resolutionIndex], self.resolutions[self.defaultMain.resolutionIndex])
            return None

    def __gSAutodetect(self):
        graphicsDetailsBest, graphicsDetails = self.defaultMain.graphicsDetails, self.graphicsDetails
        defaultGDetailsIndex, currentGDetailsIndex = self.getIndexByValueGraphicsDetails(graphicsDetailsBest), self.getIndexByValueGraphicsDetails(graphicsDetails)
        graphicsDetailsBestLoc, graphicsDetailsLoc = self.__getGraphicsDetailsLocalize(graphicsDetailsBest), self.__getGraphicsDetailsLocalize(graphicsDetails)
        if currentGDetailsIndex < defaultGDetailsIndex:
            return (SETTINGS_AUTODETECT_RESULT.HIGHER, graphicsDetailsLoc, graphicsDetailsBestLoc)
        elif currentGDetailsIndex > defaultGDetailsIndex:
            return (SETTINGS_AUTODETECT_RESULT.LOWER, graphicsDetailsLoc, graphicsDetailsBestLoc)
        else:
            return (SETTINGS_AUTODETECT_RESULT.OK, graphicsDetailsLoc, graphicsDetailsBestLoc)

    def __getGraphicsDetailsLocalize(self, detail):
        return localizeOptions(GRAPHICS_QUALITY_LOC_ID.get(detail.upper().replace(' ', '')))

    def isHDContent(self):
        return BigWorld.isHDContent()

    def getMarkerTemplateType(self):
        return 'SettingsMarker'


class ScriptConfig():

    def __init__(self, data):
        debugPlanes = []
        self.debugViewPoints = []
        self.xmppChatConfig = {}
        self.clanEmblemsConfig = {}
        self.devArenaBotsCount = 0
        self.urls = {}
        self.debugSSRenderParams = {}
        LOG_DEBUG('Reading configuration ....')
        for sName, sData in data.items():
            if sData is not None:
                if sName == 'debugAirPlane':
                    LOG_DEBUG('debugMenu: planes:')
                    for plane in sData.values():
                        name = plane.readString('name')
                        LOG_DEBUG('   :', plane.readString('name'))
                        id = plane.readString('id')
                        if not db.DBLogic.g_instance.getAircraftIDbyName(id.lower()):
                            LOG_ERROR("   :Can't find ", id)
                        else:
                            debugPlanes.append((name, id, plane.readBool('isDev', False)))

                elif sName == 'debugViewPoints':
                    LOG_DEBUG('debugMenu: debugViewPoints:')
                    for point in sData.values():
                        LOG_DEBUG('   :', point.readString('name'))
                        self.debugViewPoints.append({'name': point.readString('name'),
                         'position': point.readVector3('position'),
                         'rotation': point.readVector3('rotation')})

                elif sName == 'xmppChatConfig':
                    LOG_DEBUG('xmppChatConfig: ')
                    for key in sData.keys():
                        sValue = sData.readString(key)
                        if sValue:
                            self.xmppChatConfig[key] = sValue
                            LOG_DEBUG('   : ' + key + ' = ' + sValue)

                elif sName == 'clanEmblems':
                    LOG_DEBUG('clanEmblems: ')
                    for key in sData.keys():
                        sValue = sData.readString(key)
                        if sValue:
                            self.clanEmblemsConfig[key] = sValue
                            LOG_DEBUG('   : ' + key + ' = ' + sValue)

                elif sName == 'devArena':
                    self.devArenaBotsCount = sData.readInt('botsCount')
                    self.devArenaBotsID = sData.readInt('botsID', 0)
                    LOG_DEBUG_DEV('Dev arena bots data - count: %d , id: %d' % (self.devArenaBotsCount, self.devArenaBotsID))
                elif sName == 'debugScreenShotRendering':
                    for key in sData.keys():
                        sValue = sData.readFloat(key)
                        if sValue:
                            self.debugSSRenderParams[key] = sValue

        self.debugPlanes = debugPlanes
        self.debugBot1AirPlane = data.readString('debugBot1AirPlane')
        self.debugBot2AirPlane = data.readString('debugBot2AirPlane')
        self.scriptData = data
        self.urls['urlForum'] = data.readString('url_forum', 'http://forum-ru.worldofwarplanes.com/')
        self.urls['urlSupport'] = data.readString('url_send_error', 'https://support.worldoftanks.ru/index.php?/Knowledgebase/List/Index/8/world-of-warplanes')
        self.urls['urlForgotPassword'] = data.readString('url_forgot_password', 'https://worldoftanks.ru/personal/password_reset/new/')
        self.urls['urlAchievements'] = data.readString('urlAchievements', 'http://worldofwarplanes.ru/community/accounts/%s/')
        self.urls['urlTokensHelp'] = data.readString('urlTokensHelp', 'http://worldofwarplanes.ru/')
        self.urls['buyGold'] = data.readString('urlBuyGold', 'https://ru.wargaming.net/shop/gold/?user=%(userEncoded)s')
        self.urls['buyQuestChips'] = data.readString('urlBuyQuestChips', 'https://ru.wargaming.net/shop/wowp/combat_task/')
        self.urls['urlKong'] = data.readString('urlKong', '')
        self.urls['urlRegistration'] = data.readString('url_registration', '')
        self.urls['rssUrl'] = data.readString('rssUrl', 'http://worldofwarplanes.ru/ru/rss/news/')
        self.clusterID = data.readString('clusterID', CLASTERS.RU)

        def _merge(s1, s2):
            a1 = s1.split(',')
            a2 = s2.split(',')
            for i in a2:
                if i not in a1:
                    a1.append(i)

            return ','.join(a1)

        self.researchTreePrefs = {KEY_RESEARCH_TREE_NATION: data.readInt(''.join([KEY_RESEARCH_TREE, KEY_RESEARCH_TREE_NATION]), DEFAULT_RESEARCH_NATION),
         KEY_RESEARCH_TREE_NATION_LIST: _merge(data.readString(''.join([KEY_RESEARCH_TREE, KEY_RESEARCH_TREE_NATION_LIST]), DEFAULT_RESEARCH_NATION_LIST), DEFAULT_RESEARCH_NATION_LIST),
         KEY_RESEARCH_TREE_DEV_NATION_LIST: _merge(data.readString(''.join([KEY_RESEARCH_TREE, KEY_RESEARCH_TREE_NATION_LIST]), DEFAULT_RESEARCH_DEV_NATION_LIST), DEFAULT_RESEARCH_DEV_NATION_LIST)}
        self.timeFormated = dict()
        self.timeFormated['dBAHMS'] = data.readString(KEY_TIME_FORMATED % 'dBAHMS', '%d %B, %A, %H:%M:%S')
        self.timeFormated['dmY'] = data.readString(KEY_TIME_FORMATED % 'dmY', '%d.%m.%Y')
        self.timeFormated['dBYAHMS'] = data.readString(KEY_TIME_FORMATED % 'dBYAHMS', '%d %B %Y %A, %H:%M:%S')
        self.timeFormated['dbYHMS'] = data.readString(KEY_TIME_FORMATED % 'dbYHMS', '%d %b %Y, %H:%M:%S')
        self.timeFormated['default'] = data.readString(KEY_TIME_FORMATED % 'default', '%d %B, %H:%M:%S')
        self.timeFormated['dmYHM'] = data.readString(KEY_TIME_FORMATED % 'dmYHM', '%d.%m.%Y %H:%M')
        return

    def __addSpace(self, title, sData):
        LOG_INFO(title)
        spaces = []
        for space in sData.values():
            arenaID = 1
            LOG_INFO('   :', arenaID, space.readString('name'), space.readString('space'))
            spaces.append((arenaID, space.readString('name'), space.readString('space')))

        return spaces


class SettingsDefault(Settings):

    def __init__(self, customGraphicPrefs, userPrefs = None):
        self.userPrefs = userPrefs
        if self.userPrefs is None:
            res = ResMgr.openSection(DEFAULT_USER_PREFS_PATH)
            if res:
                ResMgr.purge(DEFAULT_USER_PREFS_PATH, True)
                self.userPrefs = res.child(1)
        if self.userPrefs is None:
            LOG_ERROR('Default preferences is Empty!', DEFAULT_USER_PREFS_PATH)
        self.graphicsPresets = gui.GraphicsPresets.GraphicsPresets(customGraphicPrefs)
        self.gameUI = self.loadGameUI()
        self._loadMains()
        self.aims = self.loadAims()
        self.countTemplates = 0
        self.selectedMarkers = MarkerSettings.SELECTED_MARKERS_LIST[:]
        self.markers = None
        self.markersTemplates = self._loadMarkers(MarkerSettings.MARKERS_BASE_XML)
        self._soundPrefs = {}
        self.loadSoundPrefs()
        self._voipPrefs = self._loadVoipSettings()
        self._xmppChatPrefs = self._loadXmppChatSettings()
        self._battleRaplaysPrefs = self._loadReplaySettings()
        self.graphicsDetails = GRAPHICS_QUALITY_NAMES.get(2, None)
        return

    def getMarkerTemplateType(self):
        return 'SettingsDefaultMarker'

    def getControlType(self):
        return 'default'

    def getGamma(self):
        return DEFAULT_GRAPHICS_DICT['graphicsGamma']

    def _applySoundPrefs(self):
        pass


class PreferencesAPI(object):

    def __init__(self, root, subRootSectionName):
        """
        @param root: <ResMgr.DataSection>
        @param subRootSectionName: <str>
        """
        self.__root = root
        self.__subRootSectionName = subRootSectionName
        if not self.__root.has_key(subRootSectionName):
            self.__root.createSection(subRootSectionName)

    def writeNode(self, node_name, node_value):
        """
        write node to preferences.xml
        @param node_name: <str>
        @param node_value: <int> or <str> or <bool> or <float> or <None>
        """
        if node_value is None:
            self.__root.createSection(self.__subRootSectionName + node_name)
        else:
            Settings.saveData(self.__root, self.__subRootSectionName + node_name, node_value, node_value)
        return

    def readNode(self, node_name, default_node_value):
        """
        read node to preferences.xml
        @param node_name: <str>
        @param default_node_value: <int> or <str> or <bool> or <float> or <None>
        @return: real node value if success else default_node_value
        """
        if not self.__root.has_key(self.__subRootSectionName + node_name):
            return default_node_value
        else:
            res = Settings.loadData(self.__root, self.__subRootSectionName + node_name, default_node_value)
            if res is not None:
                return res
            return default_node_value

    def __del__(self):
        self.__root = None
        return