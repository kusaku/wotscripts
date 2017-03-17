# Embedded file name: scripts/client/audio/SoundObjects/UI.py
from WwiseGameObject import WwiseGameObject, GS
import BigWorld
import db.DBLogic
from WWISE_ import setState

class UI(WwiseGameObject):

    def __init__(self):
        self.__bpTime = {}
        self.__battleResultsPlayed = True
        WwiseGameObject.__init__(self, 'UI')

    def onBattleStart(self):
        self.__battleResultsPlayed = False
        self.play('UISoundTimerClockLast')

    def onPlaneBlocked(self, aircraftID):
        self.__bpTime[aircraftID] = BigWorld.time()

    def onPlaneUnlocked(self, aircraftID):
        if aircraftID not in self.__bpTime:
            return
        if BigWorld.time() - self.__bpTime[aircraftID] < 2.0:
            self.__bpTime.pop(aircraftID)

    def onPLaneReturnFromBattle(self, aircraftID):
        if aircraftID not in self.__bpTime:
            return
        self.play('UISoundVehicleBack')
        self.__bpTime.pop(aircraftID)

    def toggleInGameMenu(self, visible):
        setState('STATE_GUI_Screen_Appear', 'GUI_Screen_On' if visible else 'GUI_Screen_Off')

    def play(self, tag):
        events = db.DBLogic.g_instance.getUI()
        if tag not in events:
            return
        self.postEvent(events[tag])

    def playGameResults(self):
        if self.__battleResultsPlayed:
            return
        self.__battleResultsPlayed = True
        if GS().isWinner:
            self.postEvent('Play_hud_win')
        elif GS().isDraw:
            self.postEvent('Play_hud_draw')
        else:
            self.postEvent('Play_hud_loss')

    def playLobbyResults(self):
        played = self.__battleResultsPlayed
        self.__battleResultsPlayed = True
        if played:
            return
        if GS().isWinner:
            GS().ui.play('UISoundResultWin')
        elif GS().isDraw:
            GS().ui.play('UISoundResultDraw')
        else:
            GS().ui.play('UISoundResultLoose')

    def setHoverButtonRadius(self, r):
        self.setRTPC('RTPC_UI_Hover_Battle_Volume', min(100.0, max(0.0, r)), 100.0)