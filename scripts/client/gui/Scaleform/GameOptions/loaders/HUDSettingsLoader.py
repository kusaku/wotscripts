# Embedded file name: scripts/client/gui/Scaleform/GameOptions/loaders/HUDSettingsLoader.py
__author__ = 's_karchavets'
import BigWorld
from Helpers.i18n import localizeOptions, localizeTooltips
from clientConsts import AIMS_LOC, FP_COLORS_LOC
from consts import ZOOM_TYPES_KEYS
import Settings
from gui.Scaleform.GameOptions.utils import BaseLoader, DEVICES_MAIN_UI_DATA, GENERAL_MAIN_UI_DATA, GENERAL_MAIN_SETTINGS_DATA, FP_SETTINGS
from gui.Scaleform.GameOptions.vo.MarkerSettings import AVAILABLE_MARKER_PROPERTIES, localizeMarkerValues, getValueBySystem, localizeMarkerByPlane, MARKER_TARGET_TYPE, g_instaceMarkerDistance
import InputMapping
from gui.Scaleform.GameOptions.utils import AIMS_KEYS

class DevicesLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        src.aviaHorizonType.index = settings.getGameUI()['horizonList']
        src.aviaHorizonType.data = [localizeOptions('battleui/horizon_v1'),
         localizeOptions('battleui/horizon_v2'),
         localizeOptions('battleui/horizon_v3'),
         localizeOptions('battleui/horizon_v4'),
         localizeOptions('battleui/horizon_v5'),
         localizeOptions('battleui/horizon_v6')]
        src.playerListType.index = settings.getGameUI()['curPlayerListState'] - 1
        src.playerListType.data = [localizeOptions('SETTINGS_MAXIMAL'),
         localizeOptions('SETTINGS_ENLARGED'),
         localizeOptions('SETTINGS_STANDART'),
         localizeOptions('SETTINGS_SMALL'),
         localizeOptions('SETTINGS_MINIMAL')]
        for fKey, sKey in DEVICES_MAIN_UI_DATA.iteritems():
            setattr(src, fKey, settings.getGameUI()[sKey])

        src.heightMode.index = settings.getGameUI()['heightMode']
        src.heightMode.data = [localizeOptions('battleui/schema_height_v1'), localizeOptions('battleui/schema_height_v2'), localizeOptions('SETTINGS_ALTIMETER_DROPDOWN_MENU_VARIANT_BOTH')]
        self._isLoaded = True


class GeneralLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        for fKey, sKey in GENERAL_MAIN_UI_DATA.iteritems():
            setattr(src, fKey, settings.getGameUI()[sKey])

        for fKey, sKey in GENERAL_MAIN_SETTINGS_DATA.iteritems():
            if 'cameraZoomType' == sKey:
                setattr(src, fKey, ZOOM_TYPES_KEYS.index(getattr(settings, sKey)))
            else:
                setattr(src, fKey, getattr(settings, sKey))

        self._isLoaded = True


class AimLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        for key, profileName in AIMS_KEYS.iteritems():
            aims = settings.getAimsDataByProfile(profileName)
            if aims is not None and hasattr(src, key):
                self._fillData(getattr(src, key), aims)

        self._isLoaded = True
        return

    def _fillData(self, src, aims):
        for key, locData in AIMS_LOC.iteritems():
            getattr(src, key).index = aims[key]
            getattr(src, key).data = [ locID for locID in locData ]

        src.crosshairTransparency = aims['crosshairTransparency']
        src.targetAreaTransparency = aims['targetAreaTransparency']
        src.externalAimTransparency = aims['externalAimTransparency']
        src.dynamycAim = aims['dynamycAim']


class MarkerLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        from gui.Scaleform.GameOptions.vo.HUDSettingsVO import MarkerTargetsVO, MarkerListVO, MarkerTypeVO
        baseData = Settings.g_instance.markersBaseData
        markers = settings.markersTemplates
        src.selectedSystemType = Settings.g_instance.gameUI['measurementSystem']
        src.systemType = list()
        for systemType in [0, 1]:
            systemVo = MarkerTypeVO()
            stDistance = list()
            for key in g_instaceMarkerDistance().stepsDistance:
                stDistance.append(getValueBySystem(systemType, key))

            systemVo.stepsDistance = stDistance
            systemVo.altCmd = InputMapping.CMD_SHOW_PLAYERS_INFO
            for targetType in MARKER_TARGET_TYPE:
                target = getattr(systemVo.data, targetType)
                for key in AVAILABLE_MARKER_PROPERTIES:
                    addVO = getattr(target, key)
                    addVO.title = localizeOptions(baseData[key][targetType]['label'])
                    addVO.tooltip = localizeTooltips(baseData[key][targetType]['tooltip'])
                    addVO.data = list()
                    listData = baseData[key][targetType]['list']
                    for value in listData:
                        markerListVO = MarkerListVO()
                        num = getValueBySystem(systemType, value)
                        markerListVO.label = localizeOptions(localizeMarkerValues(key, num))
                        markerListVO.num = num
                        addVO.data.append(markerListVO)

            src.systemType.append(systemVo)

        src.templates = list()
        for i in range(Settings.g_instance.countTemplates):
            vo = MarkerTargetsVO()
            isDefault = settings.getMarkerTemplateType() == 'SettingsDefaultMarker'
            loc = localizeOptions(localizeMarkerByPlane(isDefault, i))
            vo.label = loc
            for vehicleType in ('airMarker', 'groundMarker'):
                voVehicleType = getattr(vo, vehicleType)
                for targetType in ('enemy', 'target', 'friendly', 'squads'):
                    voTargetType = getattr(voVehicleType, targetType)
                    for altState in ('basic', 'alt'):
                        voAltState = getattr(voTargetType, altState)
                        for key in AVAILABLE_MARKER_PROPERTIES:
                            setattr(voAltState, key, markers[vehicleType][targetType][altState][key][i])

            src.templates.append(vo)

        src.selectIDS = settings.selectedMarkers[:]
        self._isLoaded = True


class ForestallingPointLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        for fKey, sKey in FP_SETTINGS.iteritems():
            setattr(src, fKey, getattr(settings, sKey))

        src.colorPoint.data = FP_COLORS_LOC[:]
        src.colorPoint.index = getattr(settings, 'colorPointIndexFP')
        src.isEnabled = True
        self._isLoaded = True


class HUDSettingsLoader(BaseLoader):

    def _buildLoaders(self):
        return dict(general=GeneralLoader, devices=DevicesLoader, aim=AimLoader, markers=MarkerLoader, forestallingPoint=ForestallingPointLoader)

    def isLoaded(self):
        return self._isLoadedAll()