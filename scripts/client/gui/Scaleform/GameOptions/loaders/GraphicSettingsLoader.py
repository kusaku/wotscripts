# Embedded file name: scripts/client/gui/Scaleform/GameOptions/loaders/GraphicSettingsLoader.py
__author__ = 's_karchavets'
from Helpers.i18n import localizeOptions
import Settings
from gui.Scaleform.GameOptions.utils import BaseLoader, GRAPHICS_PRESET_KEYS, GRAPHICS_QUALITY_KEYS, VIDE_MODES_KEYS_LOC
from clientConsts import isLowMemory

class GraphicSettingsLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        graphicsDetails = settings.graphicsDetails
        src.isHDContent = settings.isHDContent()
        src.graphicsWin32 = isLowMemory()
        src.waitVSync = settings.isVideoVSync()
        src.videoMode.modes.data = list()
        for i, locID in VIDE_MODES_KEYS_LOC.iteritems():
            src.videoMode.modes.data.insert(i, localizeOptions(locID))

        src.videoMode.modes.index = settings.getWindowMode()
        src.graphicsGamma = settings.getGamma()
        src.gsAutodetectEnabled = settings.gsAutodetectEnabled
        graphicsPresetKeys = settings.getGraphicsPresetKeys()
        src.videoMode.resolutions.data, src.videoMode.resolutions.index = settings.getVideoResolutions()
        src.graphicsQuality.data = list(graphicsPresetKeys)
        for i in range(0, len(src.graphicsQuality.data)):
            src.graphicsQuality.data[i] = localizeOptions(src.graphicsQuality.data[i].upper().replace(' ', ''))

        src.graphicsQuality.index = Settings.g_instance.getIndexByValueGraphicsDetails(graphicsDetails)
        gdList = settings.graphicsPresets.getSettingValues()
        graphicsDetailsConfig = settings.graphicsPresets.getPresetValues()
        for key in graphicsPresetKeys:
            graphicsDetail = graphicsDetailsConfig.get(key, None)
            graphicsProfile = getattr(src.graphicProfiles, GRAPHICS_PRESET_KEYS.get(key))
            if graphicsDetail is not None:
                for graphicsDetailName, graphicsDetailValue in graphicsDetail.iteritems():
                    for detail in gdList:
                        detailID = detail[0]
                        if detailID == graphicsDetailName:
                            gSCommonVO = getattr(graphicsProfile, GRAPHICS_QUALITY_KEYS.get(detailID))
                            gSCommonVO.title = localizeOptions('SETTINGS_GS_%s' % settings.graphicsPresets.showGraphicsSettingLocalize[detailID])
                            gSCommonVO.setting.data = [ localizeOptions(label) for label in detail[1] ]
                            gSCommonVO.setting.index = graphicsDetailValue
                            break

        self._isLoaded = True
        return