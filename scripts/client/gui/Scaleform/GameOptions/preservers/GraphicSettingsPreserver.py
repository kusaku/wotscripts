# Embedded file name: scripts/client/gui/Scaleform/GameOptions/preservers/GraphicSettingsPreserver.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import BasePreserver
import Settings
from debug_utils import LOG_WARNING
from clientConsts import WINDOW_RENDER_MODE

class VideoModePreserver(BasePreserver):

    def save(self, value):
        isFullScreen = WINDOW_RENDER_MODE.WRM_FULLSCREEN == value.modes.index
        isBorderless = WINDOW_RENDER_MODE.WRM_BORDERLESS == value.modes.index
        Settings.g_instance.changeVideoMode(value.resolutions.index, isFullScreen, isBorderless)


class VideoVSyncPreserver(BasePreserver):

    def save(self, value):
        Settings.g_instance.setVideoVSync(value)


class GammaPreserver(BasePreserver):

    def save(self, value):
        Settings.g_instance.setGamma(value)


class GraphicsQualityPreserver(BasePreserver):

    def save(self, value):
        Settings.g_instance.changeGraphicsDetails(self.__getValueByIndexGraphicsDetails(value), {})

    def __getValueByIndexGraphicsDetails(self, index):
        graphicsPresetKeys = list(Settings.g_instance.getGraphicsPresetKeys())
        try:
            index = int(index)
        except TypeError:
            LOG_WARNING("__getValueByIndexGraphicsDetails() - Argument don't convert to int %s", index)
            return None

        return graphicsPresetKeys[index]


class GraphicsDetailPreserver(BasePreserver):

    def __init__(self, presetKey, qualityKey):
        self.__presetKey = presetKey
        self.__qualityKey = qualityKey

    def save(self, value):
        Settings.g_instance.changeGraphicsDetails(self.__presetKey, {self.__qualityKey: value})