# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/RootSettingsVO.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.vo.SettingsVO import SettingsVO
from gui.Scaleform.GameOptions.vo.Signals import SignalsVO

class RootSettingsVO:

    def __init__(self):
        self.isLazy = False
        self.settings = SettingsVO()
        self.settingsDefault = SettingsVO()
        self.settingsSource = SettingsVO()
        self.signals = SignalsVO()