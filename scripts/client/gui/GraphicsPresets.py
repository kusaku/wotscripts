# Embedded file name: scripts/client/gui/GraphicsPresets.py
import BigWorld
import ResMgr
from MemoryCriticalController import g_critMemHandler
from debug_utils import LOG_ERROR, LOG_INFO
from gui import SystemMessages
from debug_utils import LOG_CURRENT_EXCEPTION
from copy import deepcopy
graphicsPresetsResource = 'system/data/graphics_settings_presets.xml'
showGraphicsSetting = ('TEXTURE_QUALITY', 'TEXTURE_FILTERING', 'BACKBUFER_QUALITY', 'OBJECT_CLIP', 'OBJECT_LOD', 'WATER_QUALITY', 'FXAA', 'POSTFX', 'MOTIONBLUR', 'VOLUMETRICCLOUDS', 'PARTICLES_QUALITY', 'SHADOWS_QUALITY', 'TREES', 'DIRTY_LENS')

class GraphicsPresetsTuple(tuple):
    pass


class GraphicsPresets:
    CUSTOM_PRESET_KEY = 'custom'
    DEFAULT_PRESET_KEY = 'medium'
    GRAPHICS_QUALITY_SETTINGS = {'MRT_DEPTH': (True, False, True),
     'TEXTURE_QUALITY': (False, True, True),
     'TEXTURE_COMPRESSION': (False, True, True),
     'TEXTURE_FILTERING': (False, False, True),
     'SHADOWS_QUALITY': (False, True, True),
     'WG_SHADOWS_ENABLED': (False, False, True),
     'SPEEDTREE_QUALITY': (False, False, True),
     'WATER_QUALITY': (False, False, True),
     'FAR_PLANE': (False, False, True),
     'OBJECT_LOD': (False, False, True),
     'POST_PROCESSING': (False, False, True),
     'VEHICLE_DUST_ENABLED': (False, False, True),
     'VEHICLE_TRACES_ENABLED': (False, False, True),
     'SNIPER_MODE_SWINGING_ENABLED': (False, False, True),
     'FXAA': (False, False, True),
     'POSTFX': (False, False, True),
     'MOTIONBLUR': (False, False, True),
     'VOLUMETRICCLOUDS': (False, False, True),
     'TREES': (False, False, True),
     'OBJECT_CLIP': (False, False, True),
     'PARTICLES_QUALITY': (False, False, True),
     'BACKBUFER_QUALITY': (False, True, True)}

    def __init__(self, customGraphicPrefs):
        section = ResMgr.openSection(graphicsPresetsResource)
        self.__presets = {}
        self.__presetsKeys = []
        self.showGraphicsSettingLocalize = dict([ (key, key) for key in showGraphicsSetting ])
        self.showGraphicsSettingLocalize['TREES'] = 'SPEEDTREE_QUALITY'
        for group in section.values():
            presetKey = group.asString.lower()
            self.__presetsKeys.append(presetKey)
            self.__presets[presetKey] = {}
            for setting in group.values():
                label = setting.readString('label')
                if label:
                    self.__presets[presetKey][label] = setting.readInt('activeOption')

        self.__presetsKeys.append(GraphicsPresets.CUSTOM_PRESET_KEY)
        self.__presets[GraphicsPresets.CUSTOM_PRESET_KEY] = deepcopy(self.__presets[GraphicsPresets.DEFAULT_PRESET_KEY])
        for setting in customGraphicPrefs.values():
            label = setting.readString('label')
            if label:
                self.__presets[GraphicsPresets.CUSTOM_PRESET_KEY][label] = setting.readInt('activeOption')

    @staticmethod
    def getSettingElem(graphQualitySettings, setting):
        for label, index, values, description in graphQualitySettings:
            if label == setting:
                valueLabels = []
                for valueLabel, supportFlag, desc in values:
                    valueLabel = valueLabel.upper()
                    valueLabel = valueLabel.replace(' ', '')
                    valueLabels.append(valueLabel)

                return valueLabels

        return None

    def getSettingValues(self):
        result = []
        graphQualitySettings = BigWorld.graphicsSettings()
        for setting in showGraphicsSetting:
            elem = self.getSettingElem(graphQualitySettings, setting)
            if elem != None:
                result.append(GraphicsPresetsTuple([setting, elem]))

        return result

    def getPresetValues(self):
        return self.__presets

    def getCurrentSettingsMap(self):
        graphQualitySettings = BigWorld.graphicsSettings()
        qualitySettings = {}
        for label, index, values, description in graphQualitySettings:
            qualitySettings[label] = index

        return qualitySettings

    def applyGraphicsPresets(self, newPresetKey):
        newPresetKey = newPresetKey.lower()
        newPreset = self.__presets[newPresetKey]
        for key, value in newPreset.items():
            try:
                if not BigWorld.isHDContent() and key == 'TEXTURE_QUALITY':
                    if value < 1:
                        value = 1
                BigWorld.setGraphicsSetting(key, value)
                if key == 'TEXTURE_QUALITY':
                    if g_critMemHandler.originQuality != -1:
                        g_critMemHandler.originQuality = value
            except Exception as inst:
                LOG_CURRENT_EXCEPTION()
                LOG_ERROR("selectGraphicsOptions: unable to set value '%s' for option '%s'" % (value, key))

        self.selectedPresetKey = newPresetKey

    def checkApplyGraphicsPreset(self, newPresetKey, customSettings):
        newPresetKey = newPresetKey.lower()
        if newPresetKey == self.CUSTOM_PRESET_KEY.lower():
            presetForApply = customSettings
        elif newPresetKey != self.selectedPresetKey and newPresetKey != None:
            presetForApply = self.__presets[newPresetKey]
        else:
            return False
        currentPreset = self.getCurrentSettingsMap()
        delayedSettings = False
        for key, value in presetForApply.items():
            restartNeeded, delayed, visibleInGUI = GraphicsPresets.GRAPHICS_QUALITY_SETTINGS.get(key, (False, False, False))
            if value != currentPreset.get(key):
                if restartNeeded:
                    return 'restartNeeded'
                if delayed and not delayedSettings:
                    delayedSettings = True

        if delayedSettings:
            return 'hasPendingSettings'
        else:
            return 'apply'

    def setCustomGraphicsSettings(self, customGraphicsSettings):
        customPreset = self.__presets[GraphicsPresets.CUSTOM_PRESET_KEY]
        for k, v in customGraphicsSettings.items():
            customPreset[k] = v

    def getPresetKeys(self):
        return self.__presetsKeys