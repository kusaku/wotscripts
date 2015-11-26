# Embedded file name: scripts/client/gui/battle_control/NotificationsController.py
import weakref
import BigWorld
from CTFManager import g_ctfManager
import FMOD
import SoundGroups
from gui.battle_control.arena_info import getIsMultiteam

class NotificationsController(object):

    def __init__(self, arenaDP):
        super(NotificationsController, self).__init__()
        self.__ui = None
        self.__arenaDP = weakref.proxy(arenaDP)
        self.__playerVehicleID = None
        self.__playerTeam = None
        self.__isTeamPlayer = False
        self.__captureSndName = 'take_flag'
        self.__deliveredSndName = 'deliver_flag'
        self.__consumedSndName = 'delivery_flag'
        self.__enemyCaptureSndName = 'enemy_take_flag'
        self.__allyCaptureSndName = 'ally_flag'
        self.__allyDroppedSndName = 'drop_flag'
        self.__allyDeliveredSndName = 'ally_captured'
        if FMOD.enabled:
            self.__captureSndName = '/ingame_voice/ingame_voice_flt/take_flag'
            self.__deliveredSndName = '/ingame_voice/ingame_voice_flt/deliver_flag'
            self.__consumedSndName = '/GUI/fallout/delivery_flag'
            self.__enemyCaptureSndName = '/ingame_voice/ingame_voice_flt/enemy_take_flag'
            self.__allyCaptureSndName = '/ingame_voice/ingame_voice_flt/ally_flag'
            self.__allyDroppedSndName = '/ingame_voice/ingame_voice_flt/drop_flag'
            self.__allyDeliveredSndName = '/ingame_voice/ingame_voice_flt/ally_captured'
        return

    def start(self, ui):
        self.__ui = weakref.proxy(ui)
        player = BigWorld.player()
        self.__playerVehicleID = player.playerVehicleID
        self.__playerTeam = player.team
        arena = player.arena
        arenaType = arena.arenaType
        self.__isTeamPlayer = self.__playerTeam in arenaType.squadTeamNumbers if getIsMultiteam(arenaType) else True
        g_ctfManager.onFlagCapturedByVehicle += self.__onFlagCapturedByVehicle
        g_ctfManager.onFlagAbsorbed += self.__onFlagAbsorbed
        g_ctfManager.onFlagDroppedToGround += self.__onFlagDroppedToGround
        if g_ctfManager.isFlagBearer(self.__playerVehicleID):
            self.__ui.showFlagCaptured()

    def stop(self):
        self.__ui = None
        self.__arenaDP = None
        g_ctfManager.onFlagCapturedByVehicle -= self.__onFlagCapturedByVehicle
        g_ctfManager.onFlagAbsorbed -= self.__onFlagAbsorbed
        g_ctfManager.onFlagDroppedToGround -= self.__onFlagDroppedToGround
        return

    def __onFlagCapturedByVehicle(self, flagID, flagTeam, vehicleID):
        vehInfo = self.__arenaDP.getVehicleInfo(vehicleID)
        if vehicleID == self.__playerVehicleID:
            SoundGroups.g_instance.playSound2D(self.__captureSndName)
            self.__ui.showFlagCaptured()
        elif vehInfo.team == self.__playerTeam:
            SoundGroups.g_instance.playSound2D(self.__allyCaptureSndName)
        else:
            SoundGroups.g_instance.playSound2D(self.__enemyCaptureSndName)

    def __onFlagAbsorbed(self, flagID, flagTeam, vehicleID, respawnTime):
        vehInfo = self.__arenaDP.getVehicleInfo(vehicleID)
        if vehicleID == self.__playerVehicleID:
            if self.__isTeamPlayer:
                SoundGroups.g_instance.playSound2D(self.__deliveredSndName)
                self.__ui.showFlagDelivered()
            else:
                SoundGroups.g_instance.playSound2D(self.__consumedSndName)
                self.__ui.showFlagAbsorbed()
        elif vehInfo.team == self.__playerTeam:
            SoundGroups.g_instance.playSound2D(self.__allyDeliveredSndName)

    def __onFlagDroppedToGround(self, flagID, flagTeam, loserVehicleID, flagPos, respawnTime):
        vehInfo = self.__arenaDP.getVehicleInfo(loserVehicleID)
        if loserVehicleID == BigWorld.player().playerVehicleID:
            self.__ui.showFlagDropped()
        elif vehInfo.team == self.__playerTeam:
            SoundGroups.g_instance.playSound2D(self.__allyDroppedSndName)