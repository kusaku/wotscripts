# Embedded file name: scripts/common/CrewSkills/SkillConditionSubObj.py
import BigWorld
import math
from consts import WORLD_SCALING
from EntityHelpers import EntityStates, isTeamObject, isAvatar
_HotChickSkillTargetHPCfc = 0.2

class HotChickSkillCondition(object):

    def __init__(self, owner):
        self._owner = owner
        self._lockTargetId = -1
        self._lockTargetDamage = 0
        self._owner.eBulletHitTarget += self._onBulletHitTarget
        self._owner.eSetLockTarget += self._onSetLockTarget

    def dispose(self):
        self._owner.eSetLockTarget -= self._onSetLockTarget
        self._owner.eBulletHitTarget -= self._onBulletHitTarget
        self._owner = None
        return

    def backup(self):
        return [self._lockTargetId, self._lockTargetDamage]

    def restore(self, data):
        self._lockTargetId, self._lockTargetDamage = data

    def _onBulletHitTarget(self, target, damage):
        if target.id == self._lockTargetId:
            self._lockTargetDamage += damage

    def _onSetLockTarget(self, newTargetId):
        if newTargetId != self._lockTargetId:
            self._lockTargetId = newTargetId
            self._lockTargetDamage = 0

    def isActive(self):
        if self._lockTargetId > 0:
            target = BigWorld.entities.get(self._lockTargetId)
            if target is not None and isTeamObject(target) and EntityStates.inState(target, EntityStates.GAME):
                return self._lockTargetDamage > _HotChickSkillTargetHPCfc * target.maxHealth
        self._lockTargetId = -1
        return False


_frontAttackAngle = math.radians(15)
_frontAttackSector = math.radians(20)

class FurySkillCondition(object):

    def __init__(self, owner):
        self._owner = owner
        self._lockTargetId = -1
        self._owner.eSetLockTarget += self._onSetLockTarget

    def dispose(self):
        self._owner.eSetLockTarget -= self._onSetLockTarget
        self._owner = None
        return

    def backup(self):
        return [self._lockTargetId]

    def restore(self, data):
        self._lockTargetId = data[-1]

    def _onSetLockTarget(self, newTargetId):
        if newTargetId != self._lockTargetId:
            self._lockTargetId = newTargetId

    def _isFrontAttack(self, target):
        planeDir = self._owner.vector
        targetDir = target.vector
        onTargetDir = target.position - self._owner.position
        inDist = onTargetDir.length <= 3000 * WORLD_SCALING
        inSector = planeDir.angle(onTargetDir) < _frontAttackSector
        isFront = planeDir.angle(-targetDir) < _frontAttackAngle
        return inSector and inDist and isFront

    def isActive(self):
        if self._lockTargetId > 0:
            target = BigWorld.entities.get(self._lockTargetId)
            if target is not None and isAvatar(target) and EntityStates.inState(target, EntityStates.GAME):
                return self._isFrontAttack(target)
        self._lockTargetId = -1
        return False