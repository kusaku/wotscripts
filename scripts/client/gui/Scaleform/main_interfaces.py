# Embedded file name: scripts/client/gui/Scaleform/main_interfaces.py
import consts
from debug_utils import LOG_ERROR
from gui.Scaleform.BattleLoading import BattleLoading
from gui.Scaleform.Login import Login
from gui.Scaleform.Lobby import Lobby
from gui.Scaleform.GameOptions.GameOptions import GameOptions
from gui.Scaleform.UI import UI
from gui.Scaleform.BeforeStartScreen import BeforeStartScreen
from gui.Scaleform.BattleResult import BattleResult
from gui.Scaleform.Prebattle import Prebattle
from gui.Scaleform.Interview import Interview
import exceptions
GUI_SCREEN_LOGIN = 'login'
GUI_SCREEN_LOBBY = 'lobby'
GUI_SCREEN_OPTIONS = 'options'
GUI_SCREEN_UI = 'ui'
GUI_SCREEN_BEFORESTART = 'beforeStartScreen'
GUI_SCREEN_BATTLERESULT = 'battleResult'
GUI_SCREEN_PREBATTLE = 'prebattle'
GUI_SCREEN_BATTLELOADING = 'battleLoading'
GUI_SCREEN_INTERVIEW = 'interview'
idict = {GUI_SCREEN_LOGIN: Login,
 GUI_SCREEN_LOBBY: Lobby,
 GUI_SCREEN_OPTIONS: GameOptions,
 GUI_SCREEN_UI: UI,
 GUI_SCREEN_BEFORESTART: BeforeStartScreen,
 GUI_SCREEN_BATTLERESULT: BattleResult,
 GUI_SCREEN_PREBATTLE: Prebattle,
 GUI_SCREEN_BATTLELOADING: BattleLoading,
 GUI_SCREEN_INTERVIEW: Interview}