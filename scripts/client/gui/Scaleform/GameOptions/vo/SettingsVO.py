# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/SettingsVO.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.vo.GameSettingsVO import GameSettingsVO
from gui.Scaleform.GameOptions.vo.HUDSettingsVO import HUDSettingsVO
from gui.Scaleform.GameOptions.vo.SoundSettingsVO import SoundSettingsVO
from gui.Scaleform.GameOptions.vo.GraphicSettingsVO import GraphicSettingsVO
from gui.Scaleform.GameOptions.vo.ControlSettingsVO import ControlSettingsVO

class SettingsVO:

    def __init__(self):
        self.isLazy = False
        self.gameSettings = GameSettingsVO()
        self.hudSettings = HUDSettingsVO()
        self.soundSettings = SoundSettingsVO()
        self.graphicSettings = GraphicSettingsVO()
        self.controlSettings = ControlSettingsVO()