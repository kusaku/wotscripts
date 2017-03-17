# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/GraphicSettingsVO.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import ArrayIndex, GRAPHICS_PRESET_KEYS, GRAPHICS_QUALITY_KEYS

class GSCommonVO:

    def __init__(self, id):
        self.isLazy = False
        self.id = id
        self.title = ''
        self.setting = ArrayIndex()


class GraphicsProfileVO:

    def __init__(self, id):
        self.isLazy = True
        self.id = id
        for value in GRAPHICS_QUALITY_KEYS.itervalues():
            setattr(self, value, GSCommonVO(value))


class GraphicProfilesList:

    def __init__(self):
        self.isLazy = False
        for value in GRAPHICS_PRESET_KEYS.itervalues():
            setattr(self, value, GraphicsProfileVO(value))


class VideoModeVO:

    def __init__(self):
        self.resolutions = ArrayIndex()
        self.modes = ArrayIndex()


class GraphicSettingsVO:

    def __init__(self):
        self.isLazy = False
        self.gsAutodetectEnabled = True
        self.videoMode = VideoModeVO()
        self.graphicsWin32 = True
        self.isHDContent = True
        self.waitVSync = True
        self.graphicsGamma = 0.1
        self.graphicsQuality = ArrayIndex()
        self.graphicProfiles = GraphicProfilesList()