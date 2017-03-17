# Embedded file name: scripts/client/HintsManager.py
import math
from AvatarControllerBase import AvatarControllerBase
from EntityHelpers import isTeamObject
from consts import DAMAGE_REASON, MIN_CALIBER, HEAVY_OBJECT_ABSORPTION, MAX_USELESS_SHOOT_TIME, PLANE_TYPE
import BigWorld
from gui.WindowsManager import g_windowsManager
_PLANES_TYPES_FOR_SKIP = [PLANE_TYPE.ASSAULT]

class HintsManager(AvatarControllerBase):

    def __init__(self, avatar):
        AvatarControllerBase.__init__(self, avatar)
        self.__uselessShootTimeStart = 0
        self.__uselessShootTargetId = 0

    def update(self, dt):
        pass

    def destroy(self):
        AvatarControllerBase.destroy(self)

    def onEntityChangeHealth(self, entity, lastHealth):
        if entity.lastDamagerID == self._owner.id and isTeamObject(entity) and self._owner.settings.airplane.planeType not in _PLANES_TYPES_FOR_SKIP:
            if self.__uselessShootTargetId != entity.id or entity.lastDamageReason != DAMAGE_REASON.BULLET:
                self.__uselessShootTimeStart = 0
                self.__uselessShootTargetId = entity.id
            damagedPartId = entity.lastDamagedPartID
            partSettings = entity.settings.partsSettings.getPartByID(damagedPartId)
            partTypeData = partSettings.getFirstPartType() if partSettings else None
            absorption = partTypeData.bboxes.list[0].absorption if partTypeData else None
            ownerMaxCaliber = self._owner.controllers['weapons'].maxCaliber
            if not self.__uselessShootTimeStart and self.__uselessShootTargetId == entity.id and entity.lastDamageReason == DAMAGE_REASON.BULLET and absorption and math.fabs(absorption - HEAVY_OBJECT_ABSORPTION) < 0.001 and ownerMaxCaliber < MIN_CALIBER:
                self.__uselessShootTimeStart = BigWorld.time()
            if not (absorption and math.fabs(absorption - HEAVY_OBJECT_ABSORPTION) < 0.001):
                self.__uselessShootTimeStart = 0
                self.__uselessShootTargetId = entity.id
            if self.__uselessShootTimeStart and BigWorld.time() - self.__uselessShootTimeStart > MAX_USELESS_SHOOT_TIME:
                g_windowsManager.getBattleUI().call_1('hud.showUselessShootMessage', '')
                self.__uselessShootTimeStart = 0
                self.__uselessShootTargetId = 0
        return