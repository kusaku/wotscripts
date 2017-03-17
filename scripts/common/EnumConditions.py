# Embedded file name: scripts/common/EnumConditions.py
import math
from inspect import getmembers, ismethod
from CrewSkills.SkillConditionSubObj import HotChickSkillCondition, FurySkillCondition
import BigWorld
import consts
from EntityHelpers import EntityStates, canAimToEntity

class EnumConditions(object):

    def __init__(self, owner, enum):
        self._owner = owner
        self.__enum = enum
        if consts.IS_CELLAPP:
            self._fm = self._owner.fm
            self._sap = self._owner.controllers['staticAttributesProxy']
            self._dap = self._owner.controllers['dynAttributesProxy']
            self._hotChickCondition = HotChickSkillCondition(owner)
            self._furyCondition = FurySkillCondition(owner)

    def destroy(self):
        if consts.IS_CELLAPP:
            self._hotChickCondition.dispose()
            self._furyCondition.dispose()
        self._owner = None
        self.__enum = None
        self._fm = None
        self._sap = None
        self._dap = None
        return

    def backup(self):
        if consts.IS_CELLAPP:
            return [self._hotChickCondition.backup(), self._furyCondition.backup()]
        return []

    def restore(self, data):
        if consts.IS_CELLAPP and data is not None:
            self._furyCondition.restore(data.pop())
            self._hotChickCondition.restore(data.pop())
        return

    def updateSkillState(self, startTime):
        self._workTime = BigWorld.time() - startTime if startTime is not None else 0
        return

    def getCondition(self, enum_value):
        if not consts.IS_CELLAPP:
            return None
        else:
            enum_value_id = self.__enum.getName(enum_value)
            if enum_value_id:
                function_name = enum_value_id
                return next((f for name, f in getmembers(self, ismethod) if name == function_name), None)
            return None

    @property
    def IS_FURY_ACTIVE(self):
        return self._furyCondition.isActive()

    @property
    def IS_HOT_CHICK_ACTIVE(self):
        return self._hotChickCondition.isActive()

    @property
    def PLANE_DIRECTION(self):
        return self._owner.vector.getNormalized()

    @property
    def WORK_TIME(self):
        return self._workTime

    @property
    def SPEED(self):
        return self._fm.speed.length

    @property
    def DIVE_SPEED(self):
        return self._sap.diveSpeed

    @property
    def SPEED_NORM(self):
        return self._fm.speed.length / self._sap.diveSpeed

    @property
    def IS_ON_FIRE(self):
        return self._owner.controllers['damageSystem'].isFire()

    @property
    def PITCH(self):
        return self._owner.pitch

    @property
    def VERTICAL_ANGLE(self):
        return math.degrees(math.asin(self._owner.vector.getNormalized().y))

    @property
    def MAX_PITCH_SPEED(self):
        return self._dap.maxPitchRotationSpeed

    @property
    def MAX_ROLL_SPEED(self):
        return self._dap.maxRollRotationSpeed

    @property
    def MAX_YAW_SPEED(self):
        return self._dap.maxYawRotationSpeed

    @property
    def PITCH_SPEED_NORM(self):
        return math.fabs(self._fm.rotationSpeed.z / self.MAX_PITCH_SPEED)

    @property
    def ROLL_SPEED_NORM(self):
        return math.fabs(self._fm.rotationSpeed.y / self.MAX_ROLL_SPEED)

    @property
    def MIN_ROLL_SPEED_NORM(self):
        return math.radians(30) / self.MAX_ROLL_SPEED

    @property
    def YAW_SPEED_NORM(self):
        return math.fabs(self._fm.rotationSpeed.x / self.MAX_YAW_SPEED)

    @property
    def HEALTH_NORM(self):
        return self._owner.health / self._owner.maxHealth

    @property
    def IS_DEAD(self):
        return EntityStates.inState(self._owner, EntityStates.DEAD)

    @property
    def TIME_GET_NO_DAMAGE(self):
        return BigWorld.time() - self._owner.lastDamageTime

    @property
    def TIME_LAST_INFLICT_DAMAGE(self):
        return BigWorld.time() - self._owner.lastInflictDamageTime

    @property
    def TIME_LAST_KILL_PLANE(self):
        return BigWorld.time() - self._owner.lastPlaneKillTime

    @property
    def TIME_LAST_GUN_FIRE(self):
        if self._owner.lastFireTime == 0:
            return 0
        return BigWorld.time() - self._owner.lastFireTime

    @property
    def TIME_LAST_TURRET_FIRE(self):
        if self._owner._lastTurretFireTime == 0:
            return 0
        return BigWorld.time() - self._owner._lastTurretFireTime

    @property
    def IS_TURRET_FIRING(self):
        return self._owner.isTurretFiring