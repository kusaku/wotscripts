# Embedded file name: scripts/client/modelManipulator/PartAnimator2.py
import BigWorld
import math, Math
from EntityHelpers import EntityStates, isTeamObject, isAvatar, isPlayerAvatar
from random import choice
from consts import HORIZONTAL_AXIS, VERTICAL_AXIS, ROLL_AXIS, FORCE_AXIS, FLAPS_AXIS, IS_EDITOR
from clientConsts import PROPELLOR_TRANSITION_TIME, SLATS_AXIS, TURRET_TRACKER_AXIS, SCENARIO_TRACKER_AXIS, FORCE_AXIS_FALL_VALUE, FORCE_AXIS_DEATH_VALUE, FLAPS_SWITCHING_BY_FORCE
import debug_utils
from functools import partial
import Event
import consts
from debug_utils import *
import db.DBLogic

class PartAnimatorBase:
    """Base class for animators"""
    SINGLE = True

    def __init__(self, settings):
        self.matrixProvider = None
        self.settings = settings
        self.axis = []
        self.triggers = []
        return

    def onLoaded(self, context):
        pass

    def destroy(self):
        pass

    def setValue(self, value, axis):
        pass

    def trigger(self, tigger, value):
        pass

    def onOwnerChanged(self, owner):
        pass


class AileronBaseController(PartAnimatorBase):

    def __init__(self, settings):
        PartAnimatorBase.__init__(self, settings)
        self.matrixProvider = BigWorld.AileronMatrixProvider()
        self.reversed = False
        self.maxAngle = self.settings.visualSettings.aileronMaxAngle

    def setValue(self, value, axis):
        self.matrixProvider.pitch = self.maxAngle * value
        if self.reversed:
            self.matrixProvider.pitch = -self.matrixProvider.pitch


class LeftAileronController(AileronBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [ROLL_AXIS]
        self.matrixProvider.speed = math.radians(settings.visualSettings.aileronSpeed)


class RightAileronController(AileronBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [ROLL_AXIS]
        self.reversed = True
        self.matrixProvider.speed = math.radians(settings.visualSettings.aileronSpeed)


class ElevatorController(AileronBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [VERTICAL_AXIS]
        self.maxAngle = self.settings.visualSettings.elevatorMaxAngle
        self.matrixProvider.speed = math.radians(settings.visualSettings.elevatorSpeed)


class ElevatorReversedController(AileronBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [VERTICAL_AXIS]
        self.reversed = True
        self.maxAngle = self.settings.visualSettings.elevatorMaxAngle
        self.matrixProvider.speed = math.radians(settings.visualSettings.elevatorSpeed)


class RudderController(AileronBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [HORIZONTAL_AXIS]
        self.maxAngle = self.settings.visualSettings.rudderMaxAngle
        self.matrixProvider.speed = math.radians(settings.visualSettings.rudderSpeed)

    def setValue(self, value, axis):
        self.matrixProvider.yaw = -self.maxAngle * value


class MixedBaseController(AileronBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axisValues = {}

    def setValue(self, value, axis):
        self.axisValues[axis] = value
        self.animateValues()


class PilotHeadController(AileronBaseController):
    PASSIVE_TIME = 3
    CALLBACK_TIME = 0.1

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [HORIZONTAL_AXIS, VERTICAL_AXIS]
        self.axisValues = {HORIZONTAL_AXIS: 0.0,
         VERTICAL_AXIS: 0.0}
        self.maxAngle = self.settings.visualSettings.rudderMaxAngle
        self.__callback = BigWorld.callback(PilotHeadController.CALLBACK_TIME, self.__idleAnimate)
        self.__passiveTime = PilotHeadController.PASSIVE_TIME
        self.matrixProvider.speed = math.radians(settings.visualSettings.rudderSpeed)

    def setValue(self, value, axis):
        if abs(value) > 0.1 and self.axisValues[axis] != value:
            self.axisValues[axis] = value
            self.animateValues()

    def animateValues(self):
        rudder_h = self.axisValues[HORIZONTAL_AXIS] if not self.reversed else -self.axisValues[HORIZONTAL_AXIS]
        rudder = max(0, self.axisValues[VERTICAL_AXIS])
        rudder_v = -rudder if not self.reversed else rudder
        self.matrixProvider.yaw = self.maxAngle * rudder_h
        self.matrixProvider.pitch = self.maxAngle * rudder_v
        self.__passiveTime = PilotHeadController.PASSIVE_TIME

    def __idleAnimate(self):
        if self.__callback is not None:
            BigWorld.cancelCallback(self.__callback)
        if not IS_EDITOR and isAvatar(BigWorld.player()) and EntityStates.inState(BigWorld.player(), EntityStates.GAME):
            if self.__passiveTime > 0:
                self.__passiveTime -= PilotHeadController.CALLBACK_TIME
            else:
                rudderY = choice([-1, 0, 1])
                self.matrixProvider.yaw = self.maxAngle * rudderY
                rudderP = choice([0, -1]) * (1 if not self.reversed else -1)
                self.matrixProvider.pitch = self.maxAngle * rudderP
                self.__passiveTime = PilotHeadController.PASSIVE_TIME
        self.__callback = BigWorld.callback(PilotHeadController.CALLBACK_TIME, self.__idleAnimate)
        return

    def destroy(self):
        AileronBaseController.destroy(self)
        if self.__callback is not None:
            BigWorld.cancelCallback(self.__callback)
        return


class PilotHeadControllerIdle(PilotHeadController):

    def __init__(self, settings):
        PilotHeadController.__init__(self, settings)
        self.reversed = True

    def setValue(self, value, axis):
        pass


class MixedRudderElevatorBaseController(MixedBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [HORIZONTAL_AXIS, VERTICAL_AXIS]
        self.axisValues = {HORIZONTAL_AXIS: 0.0,
         VERTICAL_AXIS: 0.0}
        self.matrixProvider.speed = math.radians(settings.visualSettings.elevatorSpeed)

    def animateValues(self):
        rudder = self.settings.visualSettings.rudderMaxAngle * self.axisValues[HORIZONTAL_AXIS]
        if self.reversed:
            rudder = -rudder
        self.matrixProvider.pitch = (rudder + self.settings.visualSettings.elevatorMaxAngle * self.axisValues[VERTICAL_AXIS]) / 2


class LeftMixedRudderElevatorController(MixedRudderElevatorBaseController):

    def __init__(self, settings):
        MixedRudderElevatorBaseController.__init__(self, settings)
        self.reversed = False


class RightMixedRudderElevatorController(MixedRudderElevatorBaseController):

    def __init__(self, settings):
        MixedRudderElevatorBaseController.__init__(self, settings)
        self.reversed = True


class MixedAileronElevatorBaseController(MixedBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [ROLL_AXIS, VERTICAL_AXIS]
        self.axisValues = {ROLL_AXIS: 0.0,
         VERTICAL_AXIS: 0.0}
        self.matrixProvider.speed = math.radians(settings.visualSettings.aileronSpeed)

    def animateValues(self):
        aileron = self.settings.visualSettings.aileronMaxAngle * self.axisValues[ROLL_AXIS]
        if self.reversed:
            aileron = -aileron
        self.matrixProvider.pitch = (aileron + self.settings.visualSettings.elevatorMaxAngle * self.axisValues[VERTICAL_AXIS]) / 2


class LeftMixedAileronElevatorController(MixedAileronElevatorBaseController):

    def __init__(self, settings):
        MixedAileronElevatorBaseController.__init__(self, settings)
        self.reversed = False


class RightMixedAileronElevatorController(MixedAileronElevatorBaseController):

    def __init__(self, settings):
        MixedAileronElevatorBaseController.__init__(self, settings)
        self.reversed = True


class FlapsController(MixedBaseController):

    def __init__(self, settings):
        MixedBaseController.__init__(self, settings)
        if FLAPS_SWITCHING_BY_FORCE:
            self.axis = [FLAPS_AXIS, FORCE_AXIS]
        else:
            self.axis = [FLAPS_AXIS]
        for axis in self.axis:
            self.axisValues[axis] = 0.0

        self.matrixProvider.speed = math.radians(settings.visualSettings.flapperSpeed)
        self.reversed = True

    def animateValues(self):
        self.matrixProvider.pitch = self.settings.visualSettings.flapperMaxAngle if self.axisValues[FLAPS_AXIS] != 0 or self.axisValues.get(FORCE_AXIS, 0) == -1 else 0
        if self.reversed:
            self.matrixProvider.pitch = -self.matrixProvider.pitch


class UpperFlapsController(FlapsController):

    def __init__(self, settings):
        FlapsController.__init__(self, settings)
        self.reversed = False


class LowerFlapsController(FlapsController):

    def __init__(self, settings):
        FlapsController.__init__(self, settings)
        self.reversed = True


class BrakeController(AileronBaseController):

    def __init__(self, settings):
        AileronBaseController.__init__(self, settings)
        self.axis = [FORCE_AXIS]
        self.matrixProvider.speed = math.radians(settings.visualSettings.brakeSpeed)
        self.reversed = True

    def setValue(self, value, axis):
        self.matrixProvider.yaw = self.settings.visualSettings.brakeMaxAngle if value == -1 else 0
        if self.reversed:
            self.matrixProvider.yaw = -self.matrixProvider.yaw


class LeftBrakeController(BrakeController):

    def __init__(self, settings):
        BrakeController.__init__(self, settings)
        self.reversed = False


class RightBrakeController(BrakeController):

    def __init__(self, settings):
        BrakeController.__init__(self, settings)
        self.reversed = True


class UpBrakeController(BrakeController):

    def __init__(self, settings):
        BrakeController.__init__(self, settings)
        self.reversed = False

    def setValue(self, value, axis):
        self.matrixProvider.pitch = self.settings.visualSettings.brakeMaxAngle if value == -1 else 0
        if self.reversed:
            self.matrixProvider.pitch = -self.matrixProvider.pitch


class DownBrakeController(BrakeController):

    def __init__(self, settings):
        BrakeController.__init__(self, settings)
        self.reversed = True

    def setValue(self, value, axis):
        self.matrixProvider.pitch = self.settings.visualSettings.brakeMaxAngle if value == -1 else 0
        if self.reversed:
            self.matrixProvider.pitch = -self.matrixProvider.pitch


class OffsetUpBrakeController(PartAnimatorBase):

    def __init__(self, settings):
        PartAnimatorBase.__init__(self, settings)
        self.axis = [FORCE_AXIS]
        self.reversed = False
        self.matrixProvider = BigWorld.VectorOffsetProvider((0, 0, 0))
        self.maxAngle = self.settings.visualSettings.brakeOffset
        self.speed = math.radians(settings.visualSettings.brakeOffsetSpeed)
        self.__callback = None
        self.__target = None
        self.__currentValue = 0
        return

    def setValue(self, value, axis):
        if self.__callback != None:
            BigWorld.cancelCallback(self.__callback)
        self.__update((-self.maxAngle if self.reversed else self.maxAngle) if value == -1 else 0)
        return

    def __update(self, target = None):
        self.__callback = None
        if target != None:
            self.__target = target
        self.__currentValue += self.speed if self.__target > self.__currentValue else -self.speed
        if abs(self.__currentValue - self.__target) <= self.speed:
            self.__currentValue = self.__target
        self.matrixProvider.offset = (0, self.__currentValue, 0)
        if self.__currentValue != self.__target:
            self.__callback = BigWorld.callback(0.05, self.__update)
        return

    def destroy(self):
        PartAnimatorBase.destroy(self)
        if self.__callback != None:
            BigWorld.cancelCallback(self.__callback)
        return


class OffsetDownBrakeController(OffsetUpBrakeController):

    def __init__(self, settings):
        OffsetUpBrakeController.__init__(self, settings)
        self.reversed = True


class SlatsController(PartAnimatorBase):

    def __init__(self, settings):
        PartAnimatorBase.__init__(self, settings)
        self.axis = [SLATS_AXIS]
        self.reversed = False
        self.matrixProvider = BigWorld.VectorOffsetProvider((0, 0, 0))
        self.maxAngle = self.settings.visualSettings.slateOffset
        self.slateOnAngle = self.settings.visualSettings.slateOnAngle
        self.speed = math.radians(settings.visualSettings.slateSpeed)
        self.__callback = None
        self.__target = None
        self.__currentValue = 0
        self.__slateOn = False
        self.__lastActiveTime = 0
        self.minWorkingTime = 2
        return

    def setValue(self, value, axis):
        if self.__callback != None:
            BigWorld.cancelCallback(self.__callback)
        if value >= self.slateOnAngle:
            self.__slateOn = True
            self.__lastActiveTime = BigWorld.time()
        elif self.__slateOn:
            if self.__lastActiveTime + self.minWorkingTime < BigWorld.time():
                self.__slateOn = False
        self.__update((-self.maxAngle if self.reversed else self.maxAngle) if self.__slateOn else 0)
        return

    def __update(self, target = None):
        self.__callback = None
        if target != None:
            self.__target = target
        if abs(self.__currentValue - self.__target) <= self.speed:
            self.__currentValue = self.__target
        else:
            self.__currentValue += self.speed if self.__target > self.__currentValue else -self.speed
        self.matrixProvider.offset = (0, 0, self.__currentValue)
        if self.__currentValue != self.__target:
            self.__callback = BigWorld.callback(0.05, self.__update)
        return

    def destroy(self):
        PartAnimatorBase.destroy(self)
        if self.__callback != None:
            BigWorld.cancelCallback(self.__callback)
        return


class SlatsAileronController(PartAnimatorBase):

    def __init__(self, settings):
        PartAnimatorBase.__init__(self, settings)
        self.axis = [SLATS_AXIS]
        self.matrixProvider = BigWorld.AileronMatrixProvider()
        self.maxAngle = self.settings.visualSettings.slateOffset
        self.slateOnAngle = self.settings.visualSettings.slateOnAngle
        self.speed = math.radians(settings.visualSettings.slateSpeed)

    def setValue(self, value, axis):
        self.matrixProvider.pitch = self.maxAngle if value >= self.slateOnAngle else 0


class DummyTurretTracker:

    def __init__(self, nodeId, turretSettings):
        self.nodeId = -1
        self.settings = None
        self.tracker = None
        return

    def attachToCompound(self, cid):
        pass

    def setDefaultDirection(self):
        pass

    def setAlive(self, value):
        pass

    def rotate(self, yaw, pitch):
        pass

    def destroy(self):
        pass

    def setTargetMatrix(self, targetMatrix):
        pass

    def onOwnerChanged(self, owner):
        pass

    def canShoot(self):
        return True

    def onShoot(self):
        pass


class TurretTracker:

    def __init__(self, nodeId, turretSettings, path = ''):
        self.haveTarget = False
        self.isAlive = True
        self.nodeId = nodeId
        if consts.IS_EDITOR:
            self.mountPoint = path
        self.settings = turretSettings
        for key, settings in turretSettings.visualSettings.iteritems():
            keyPath = key.split('/')
            if len(keyPath) > 0 and keyPath[-1] == path:
                path = key
                break

        self.visualSettings = turretSettings.visualSettings[path if path in turretSettings.visualSettings else '']
        self.__owner = None
        self.compoundMatrix = None
        self.tracker = BigWorld.Tracker()
        self.tracker.maxLod = 0
        self.tracker.directionProvider = BigWorld.TurretDirectionProvider(None, None, None, self.visualSettings.trackYawMin, self.visualSettings.trackYawMax, -self.visualSettings.trackPitchMin, -self.visualSettings.trackPitchMax, False)
        self.tracker.directionProvider.canLostTarget = False
        self.tracker.relativeProvider = True
        self.setDefaultDirection()
        return

    def onOwnerChanged(self, owner):
        self.__owner = owner
        if owner is None:
            self.tracker.directionProvider.gunnerPos = None
            self.tracker.directionProvider.enabled = False
        else:
            self.tracker.directionProvider.gunnerPos = self.__owner.matrix
        return

    def attachToCompound(self, cid):
        self.compoundMatrix = BigWorld.CompoundNodeMP()
        self.compoundMatrix.handle = cid
        self.compoundMatrix.nodeIdx = self.nodeId
        self.tracker.mParentMp = self.compoundMatrix
        self.tracker.directionProvider.source = self.compoundMatrix
        try:
            trackerNodeInfo = BigWorld.TurretNodeAnimator(cid, self.visualSettings.pitchNodeName, self.visualSettings.yawNodeName, self.visualSettings.directionNodeName, self.visualSettings.shootingNodeName, -self.visualSettings.pitchMin, -self.visualSettings.pitchMax, self.visualSettings.yawMin, self.visualSettings.yawMax, int(self.visualSettings.axisDirections.x), int(self.visualSettings.axisDirections.y), self.visualSettings.angularVelocity, self.visualSettings.angularThreshold, self.visualSettings.angularHalflife)
        except Exception as e:
            LOG_DEBUG('Failed to create TurretNodeAnimator!', e)
            return

        trackerNodeInfo.idleFrequencyScalerX = self.visualSettings.idleFrequencyScalerX
        trackerNodeInfo.idleAmplitudeScalerX = self.visualSettings.idleAmplitudeScalerX
        trackerNodeInfo.idleFrequencyScalerY = self.visualSettings.idleFrequencyScalerY
        trackerNodeInfo.idleAmplitudeScalerY = self.visualSettings.idleAmplitudeScalerY
        trackerNodeInfo.shootCooldownTime = self.visualSettings.shootCooldownTime
        trackerNodeInfo.enableIdleAnimation = self.visualSettings.enableIdleAnimation
        gunProfile = db.DBLogic.g_instance.getGunData(self.settings.gunName)
        if self.visualSettings.useGunProfile and gunProfile is not None:
            trackerNodeInfo.shootTime = 2.0 / (gunProfile.RPM / 60.0)
        else:
            trackerNodeInfo.shootTime = self.visualSettings.shootTime
        trackerNodeInfo.setShotRecoilCurve(list(self.visualSettings.recoilCurve.p))
        self.tracker.nodeInfo = trackerNodeInfo
        return

    def setTargetMatrix(self, targetMatrix):
        self.haveTarget = targetMatrix is not None
        if self.haveTarget:
            if self.visualSettings.enableIdleAnimation:
                self.tracker.nodeInfo.enableIdleAnimation = False
            self.tracker.directionProvider.target = targetMatrix
            if self.isAlive:
                self.tracker.directionProvider.enabled = True
        elif self.isAlive:
            if self.visualSettings.enableIdleAnimation:
                self.tracker.nodeInfo.enableIdleAnimation = True
            self.setDefaultDirection()
        return

    def setAlive(self, value):
        self.isAlive = value
        if value:
            self.tracker.nodeInfo.enableIdleAnimation = self.visualSettings.enableIdleAnimation
            if not self.haveTarget:
                self.setDefaultDirection()
            else:
                self.tracker.directionProvider.enabled = True
        else:
            self.tracker.directionProvider.enabled = False
            self.tracker.nodeInfo.enableIdleAnimation = False
            q = Math.Quaternion()
            q.fromEuler(0.0, math.radians(self.visualSettings.animatorDirectionOffset[1] + self.visualSettings.animatorDieDirection[1]), math.radians(self.visualSettings.animatorDirectionOffset[0] + self.visualSettings.animatorDieDirection[0]))
            self.tracker.directionProvider.staticOrientation = q

    def setDefaultDirection(self):
        q = Math.Quaternion()
        q.fromEuler(0.0, math.radians(self.visualSettings.animatorDirectionOffset[1] + self.visualSettings.animatorDirectionDefault[1]), math.radians(self.visualSettings.animatorDirectionOffset[0] + self.visualSettings.animatorDirectionDefault[0]))
        self.tracker.directionProvider.enabled = False
        self.tracker.directionProvider.staticOrientation = q

    def canShoot(self):
        return not self.tracker.directionProvider.clipped

    def onShoot(self, delay):
        if self.tracker.nodeInfo:
            self.tracker.nodeInfo.playShootAnimation(delay)

    def destroy(self):
        self.compoundMatrix = None
        self.__owner = None
        if self.tracker is not None:
            self.tracker.directionProvider.source = Math.Matrix()
            self.tracker.directionProvider.target = Math.Matrix()
            self.tracker.directionProvider = None
            self.tracker = None
        return


class TurretController(PartAnimatorBase):

    def __init__(self, settings):
        PartAnimatorBase.__init__(self, settings)
        self.axis = [TURRET_TRACKER_AXIS]
        self.__trackers = dict()
        self.__nodeForGunLookup = {}
        self._isAttachToCompound = False
        self._lazySetTarget = None
        self._lazySetGunnerState = {}
        self.__owner = None
        return

    def createTracker(self, nodeId, gunnerId, turretSettings, gunIds = -1, path = '', entityId = -1):
        for gunner, trackers in self.__trackers.iteritems():
            tracker = trackers.get(nodeId, None)
            if tracker is not None:
                return tracker

        if gunnerId not in self.__trackers:
            self.__trackers[gunnerId] = {}
        if not IS_EDITOR:
            from gui.Scaleform.utils.HangarSpace import g_hangarSpace
            isInHangar = g_hangarSpace is not None
            self.__owner = BigWorld.entities.get(entityId, None)
            tracker = TurretTracker(nodeId, turretSettings, path=path)
        else:
            tracker = TurretTracker(nodeId, turretSettings, path=path)
        for i, gunId in enumerate(gunIds):
            if gunId in self.__nodeForGunLookup:
                LOG_WARNING('createTracker: gun already added!')
            self.__nodeForGunLookup[gunId] = (nodeId, gunnerId)

        self.__trackers[gunnerId][nodeId] = tracker
        return tracker

    @property
    def trackers(self):
        return [ tracker for trackers in self.__trackers.itervalues() for tracker in trackers.itervalues() ]

    def onOwnerChanged(self, owner):
        if self.__owner != owner:
            for trackers in self.__trackers.itervalues():
                for tracker in trackers.itervalues():
                    tracker.onOwnerChanged(owner)

            if owner is not None:
                turretController = owner.controllers.get('turretsLogic', None)
                if turretController is not None:
                    turretController.eTurretTargetChanged += self.onTurretTargetChanged
                    turretController.eGunnerStateChanged += self.onGunnerStateChanged
            elif self.__owner is not None:
                turretController = self.__owner.controllers.get('turretsLogic', None)
                if turretController is not None:
                    turretController.eTurretTargetChanged -= self.onTurretTargetChanged
                    turretController.eGunnerStateChanged -= self.onGunnerStateChanged
            self.__owner = owner
        return

    def canShoot(self, gunId):
        if gunId in self.__nodeForGunLookup:
            nodeId, gunnerId = self.__nodeForGunLookup[gunId]
            return self.__trackers[gunnerId][nodeId].canShoot()
        return True

    def onGunnerStateChanged(self, gunnerId, isAlive):
        if self._isAttachToCompound:
            trackers = self.__trackers.get(gunnerId, None)
            if trackers is not None:
                for tracker in trackers.itervalues():
                    tracker.setAlive(isAlive)

        else:
            self._lazySetGunnerState[gunnerId] = isAlive
        return

    def onTurretTargetChanged(self, targetId):
        if self._isAttachToCompound:
            for trackers in self.__trackers.itervalues():
                for tracker in trackers.itervalues():
                    if targetId is not None:
                        if not consts.IS_EDITOR:
                            targetEntity = BigWorld.entities.get(targetId, None)
                            tracker.setTargetMatrix(targetEntity.matrix if targetEntity else None)

        else:
            self._lazySetTarget = targetId
        return

    def onTurretShoot(self, gunId, delay):
        if gunId in self.__nodeForGunLookup:
            nodeId, gunnerId = self.__nodeForGunLookup[gunId]
            self.__trackers[gunnerId][nodeId].onShoot(delay)

    def destroy(self):
        for trackers in self.__trackers.itervalues():
            for item in trackers.itervalues():
                item.destroy()

            trackers.clear()

        self.__trackers.clear()
        self.__owner = None
        PartAnimatorBase.destroy(self)
        return

    def _tryLazyUpdateTrackers(self):
        self._isAttachToCompound = True
        if self._lazySetTarget is not None:
            self.onTurretTargetChanged(self._lazySetTarget)
            self._lazySetTarget = None
        if self._lazySetGunnerState:
            for gunnerId, isAlive in self._lazySetGunnerState.iteritems():
                self.onGunnerStateChanged(gunnerId, isAlive)

            self._lazySetGunnerState = {}
        return

    def onLoaded(self, context):
        for trackers in self.__trackers.itervalues():
            for item in trackers.itervalues():
                item.attachToCompound(context.cidProxy.handle)

        self._tryLazyUpdateTrackers()
        if self.__owner is not None:
            turretController = self.__owner.controllers.get('turretsLogic', None)
            if turretController is not None:
                turretController.eTurretTargetChanged += self.onTurretTargetChanged
                turretController.eGunnerStateChanged += self.onGunnerStateChanged
        return


class GunnerHeadTracker:

    def __init__(self, nodeId, modelId, settings):
        self.haveTarget = False
        self.isAlive = True
        self.nodeId = nodeId
        self.modelId = modelId
        self.settings = settings
        self.__enableIdle = False
        self._cid = None
        self.tracker = BigWorld.Tracker()
        self.tracker.maxLod = 0
        self.tracker.directionProvider = BigWorld.TurretDirectionProvider(None, None, None, self.settings.yawMin, self.settings.yawMax, -self.settings.pitchMin, -self.settings.pitchMax)
        self.tracker.directionProvider.canLostTarget = False
        self.tracker.relativeProvider = True
        self.setDefaultDirection()
        return

    def attachToCompound(self, cid):
        self._cid = cid
        nodeMatrixProvider = BigWorld.CompoundNodeMP()
        nodeMatrixProvider.handle = cid
        nodeMatrixProvider.nodeIdx = self.nodeId
        self.tracker.directionProvider.source = nodeMatrixProvider
        self.tracker.mParentMp = nodeMatrixProvider
        trackerNodeInfo = BigWorld.TrackerNodeInfo(cid, self.modelId, self.settings.nodeName, [], self.settings.nodeName, -self.settings.pitchMin, -self.settings.pitchMax, self.settings.yawMin, self.settings.yawMax, self.settings.angularVelocity, self.settings.angularThreshold, self.settings.angularHalflife)
        trackerNodeInfo.idleFrequencyScalerX = self.settings.idleFrequencyScalerX
        trackerNodeInfo.idleAmplitudeScalerX = self.settings.idleAmplitudeScalerX
        trackerNodeInfo.idleFrequencyScalerY = self.settings.idleFrequencyScalerY
        trackerNodeInfo.idleAmplitudeScalerY = self.settings.idleAmplitudeScalerY
        trackerNodeInfo.enableIdleAnimation = self.settings.enableIdleAnimation
        self.tracker.nodeInfo = trackerNodeInfo

    def setAlive(self, value):
        self.isAlive = value
        if value:
            self.tracker.nodeInfo.enableIdleAnimation = self.settings.enableIdleAnimation
            if not self.haveTarget:
                self.setDefaultDirection()
            else:
                self.tracker.directionProvider.enabled = True
        else:
            self.tracker.nodeInfo.enableIdleAnimation = False
            self.rotate(math.radians(self.settings.animatorDieDirection[0]), math.radians(self.settings.animatorDieDirection[1]))

    def setDefaultDirection(self):
        self.rotate(math.radians(self.settings.animatorDirectionDefault[0]), math.radians(self.settings.animatorDirectionDefault[1]))

    def rotate(self, yaw, pitch):
        self.tracker.directionProvider.enabled = False
        q = Math.Quaternion()
        q.fromEuler(0.0, math.radians(self.settings.animatorDirectionOffset[1]) + pitch, math.radians(self.settings.animatorDirectionOffset[0]) + yaw)
        self.tracker.directionProvider.staticOrientation = q

    def setTargetMatrix(self, targetMatrix):
        self.haveTarget = targetMatrix is not None
        if self.haveTarget:
            self.tracker.directionProvider.target = targetMatrix
            if self.isAlive:
                self.tracker.directionProvider.enabled = True
            self.tracker.nodeInfo.enableIdleAnimation = False
        elif self.isAlive:
            self.setDefaultDirection()
            self.tracker.nodeInfo.enableIdleAnimation = self.settings.enableIdleAnimation
        return

    def destroy(self):
        if self.tracker is not None:
            self.tracker.directionProvider = None
            self.tracker = None
        return


class GunnerHeadController(PartAnimatorBase):

    def __init__(self, settings):
        PartAnimatorBase.__init__(self, settings)
        self.__trackers = dict()
        self._isAttachToCompound = False
        self._lazySetTarget = None
        self._lazySetGunnerState = {}
        self.__owner = None
        return

    def createTracker(self, nodeId, modelId, settings, entityId):
        for id, tracker in self.__trackers.iteritems():
            if id == modelId:
                return tracker

        if not IS_EDITOR:
            self.__owner = BigWorld.entities.get(entityId)
        else:
            self.__owner = None
        tracker = GunnerHeadTracker(nodeId, modelId, settings)
        self.__trackers[modelId] = tracker
        return tracker

    @property
    def trackers(self):
        return self.__trackers.itervalues()

    def onGunnerStateChanged(self, gunnerId, isAlive):
        if self._isAttachToCompound:
            for tracker in self.__trackers.itervalues():
                tracker.setAlive(isAlive)

        else:
            self._lazySetGunnerState[gunnerId] = isAlive

    def onTurretTargetChanged(self, targetId):
        if self._isAttachToCompound:
            for tracker in self.__trackers.itervalues():
                if targetId is not None:
                    if not consts.IS_EDITOR:
                        targetEntity = BigWorld.entities.get(targetId, None)
                        tracker.setTargetMatrix(targetEntity.matrix if targetEntity else None)
                else:
                    tracker.setTargetMatrix(None)

        else:
            self._lazySetTarget = targetId
        return

    def onOwnerChanged(self, owner):
        if self.__owner != owner:
            if owner is not None:
                turretController = owner.controllers.get('turretsLogic', None)
                if turretController is not None:
                    turretController.eTurretTargetChanged += self.onTurretTargetChanged
                    turretController.eGunnerStateChanged += self.onGunnerStateChanged
            self.__owner = owner
        return

    def destroy(self):
        for item in self.__trackers.itervalues():
            item.destroy()

        self.__trackers.clear()
        self.__owner = None
        PartAnimatorBase.destroy(self)
        return

    def _tryLazyUpdateTrackers(self):
        self._isAttachToCompound = True
        if self._lazySetTarget is not None:
            self.onTurretTargetChanged(self._lazySetTarget)
            self._lazySetTarget = None
        if self._lazySetGunnerState:
            for gunnerId, isAlive in self._lazySetGunnerState.iteritems():
                self.onGunnerStateChanged(gunnerId, isAlive)

            self._lazySetGunnerState = {}
        return

    def onLoaded(self, context):
        for item in self.__trackers.itervalues():
            item.attachToCompound(context.cidProxy.handle)

        self._tryLazyUpdateTrackers()
        if self.__owner is not None and isAvatar(self.__owner):
            turretController = self.__owner.controllers.get('turretsLogic', None)
            if turretController is not None:
                turretController.eTurretTargetChanged += self.onTurretTargetChanged
                turretController.eGunnerStateChanged += self.onGunnerStateChanged
        return


class GearController(PartAnimatorBase):

    def __init__(self, settings):
        pass


class SimplePropellorBase(PartAnimatorBase):
    SINGLE = False

    def __init__(self, settings, direction):
        PartAnimatorBase.__init__(self, settings)
        self.matrixProvider = BigWorld.PropellorMatrixProvider(1.0 / PROPELLOR_TRANSITION_TIME * 2.0, direction)
        self.axis = [FORCE_AXIS]

    def setValue(self, value, axis):
        settings = self.settings.visualSettings
        if value == FORCE_AXIS_DEATH_VALUE:
            speed = 0.0
        elif value >= FORCE_VALUE_FOSAGE:
            speed = settings.rotorSpeedFosage
        elif value >= FORCE_VALUE_LOW:
            speed = settings.rotorSpeedLow + (settings.rotorSpeedNormal - settings.rotorSpeedLow) * (1 + value)
        elif value == FORCE_AXIS_FALL_VALUE:
            speed = settings.rotorSpeedFalling
        else:
            speed = 0.0
        self.matrixProvider.speed = speed


class SimplePropellorL(SimplePropellorBase):

    def __init__(self, settings):
        SimplePropellorBase.__init__(self, settings, 1)


class SimplePropellorR(SimplePropellorBase):

    def __init__(self, settings):
        SimplePropellorBase.__init__(self, settings, -1)


FORCE_VALUE_LOW = -1
FORCE_VALUE_NORMAL = 0
FORCE_VALUE_FOSAGE = 1
PROPELLER_SOLID = 0
PROPELLER_NORMAL = 1
PROPELLER_FORSAGE = 2

class PropellorControllerBase(PartAnimatorBase):
    SINGLE = False

    def __init__(self, settings, direction):
        PartAnimatorBase.__init__(self, settings)
        self.__isBroken = False
        self.__lastValue = -1
        self.__lastState = -1
        self.matrixProvider = BigWorld.PropellorMatrixProvider(1.0 / PROPELLOR_TRANSITION_TIME * 2.0, direction)
        self.axis = [FORCE_AXIS]
        self.fashions = [ BigWorld.PyAlphaTransitionFashion(1.0 / PROPELLOR_TRANSITION_TIME, 1.0 if i == 0 else 0.0) for i in range(3) ]
        self.callback = Event.Event()
        for idFashion, fashion in enumerate(self.fashions):
            fashion.callback = partial(self.callback, idFashion + 1)

        self.setValue(self.matrixProvider.speed, FORCE_AXIS)

    def setAngle(self, angle):
        self.matrixProvider.angle = angle

    def setValue(self, value, axis):
        settings = self.settings.visualSettings
        self.__lastValue = value
        if value == FORCE_AXIS_DEATH_VALUE:
            state, speed = PROPELLER_SOLID, 0.0
        elif self.__isBroken:
            state, speed = PROPELLER_SOLID, settings.rotorSpeedBroken
        elif value >= FORCE_VALUE_FOSAGE:
            state, speed = PROPELLER_FORSAGE, settings.rotorSpeedFosage
        elif value >= FORCE_VALUE_LOW:
            state, speed = PROPELLER_NORMAL, settings.rotorSpeedLow + (settings.rotorSpeedNormal - settings.rotorSpeedLow) * (1 + value)
        elif value == FORCE_AXIS_FALL_VALUE:
            state, speed = PROPELLER_SOLID, settings.rotorSpeedFalling
        else:
            state, speed = PROPELLER_SOLID, 0.0
        self.__setState(state)
        self.matrixProvider.speed = speed

    def __setState(self, newState):
        if self.__lastState != newState:
            for i in range(len(self.fashions)):
                self.fashions[i].start(1.0 if newState == i else 0.0)

            self.__lastState = newState

    def setBroken(self, broken):
        if self.__isBroken != broken:
            self.__isBroken = broken
            self.setValue(self.__lastValue, FORCE_AXIS)


class PropellorControllerL(PropellorControllerBase):

    def __init__(self, settings):
        PropellorControllerBase.__init__(self, settings, 1)


class PropellorControllerR(PropellorControllerBase):

    def __init__(self, settings):
        PropellorControllerBase.__init__(self, settings, -1)


class ANIMATION_TRIGGERS:
    BOMB_HATCH_OPEN = 1


class HatchControllerBase(PartAnimatorBase):

    def __init__(self, settings):
        PartAnimatorBase.__init__(self, settings)
        self.matrixProvider = BigWorld.AileronMatrixProvider()
        self.reversed = False


class BombHatchControllerR(HatchControllerBase):

    def __init__(self, settings):
        HatchControllerBase.__init__(self, settings)
        self.triggers = [ANIMATION_TRIGGERS.BOMB_HATCH_OPEN]
        self.bombHatchOpenSpeed = math.radians(self.settings.visualSettings.bombHatchOpenSpeed) if hasattr(self.settings.visualSettings, 'bombHatchOpenSpeed') else 1.0
        self.bombHatchCloseSpeed = math.radians(self.settings.visualSettings.bombHatchCloseSpeed) if hasattr(self.settings.visualSettings, 'bombHatchCloseSpeed') else 5.0
        self.bombHatchMaxAngle = math.radians(self.settings.visualSettings.bombHatchMaxAngle) if hasattr(self.settings.visualSettings, 'bombHatchMaxAngle') else 90

    def trigger(self, tigger, value):
        if value > 0.0:
            self.matrixProvider.speed = self.bombHatchOpenSpeed
        else:
            self.matrixProvider.speed = self.bombHatchCloseSpeed
        angle = self.bombHatchMaxAngle * value
        self.matrixProvider.roll = -angle if self.reversed else angle


class BombHatchControllerL(BombHatchControllerR):

    def __init__(self, settings):
        BombHatchControllerR.__init__(self, settings)
        self.reversed = True


CONTROLLERS = [LeftAileronController,
 RightAileronController,
 ElevatorController,
 ElevatorReversedController,
 RudderController,
 PilotHeadController,
 PilotHeadControllerIdle,
 LeftMixedRudderElevatorController,
 RightMixedRudderElevatorController,
 LeftMixedAileronElevatorController,
 RightMixedAileronElevatorController,
 FlapsController,
 UpperFlapsController,
 LowerFlapsController,
 UpBrakeController,
 DownBrakeController,
 LeftBrakeController,
 RightBrakeController,
 OffsetUpBrakeController,
 OffsetDownBrakeController,
 SlatsController,
 SlatsAileronController,
 TurretController,
 GunnerHeadController,
 PropellorControllerL,
 PropellorControllerR,
 SimplePropellorL,
 SimplePropellorR,
 BombHatchControllerR,
 BombHatchControllerL]
_CONTROLLERS_MAP = dict(((controllerCls.__name__, controllerCls) for controllerCls in CONTROLLERS))

class PartAnimatorController:
    """Create and control life time of animation controllers"""

    def __init__(self, settings, entityId):
        self.__controllerByAxis = {}
        self.__controllersByClass = {}
        self.__controllerByTrigger = {}
        self.__controllers = []
        self.__axisValues = {}
        self.__triggerValues = {}
        self.__settings = settings
        self.__triggerValues = {}
        self.__entityId = entityId

    def __createController(self, controllerClass):
        if controllerClass not in self.__controllersByClass or not controllerClass.SINGLE:
            controller = controllerClass(self.__settings)
            self.__controllersByClass[controllerClass] = controller
            self.__controllers.append(controller)
            self.__registerAxises(controller)
            self.__registerTriggers(controller)
            return controller
        else:
            return self.__controllersByClass[controllerClass]

    def __registerAxises(self, controller):
        for axis in controller.axis:
            if axis in self.__controllerByAxis:
                self.__controllerByAxis[axis].append(controller)
            else:
                self.__controllerByAxis[axis] = [controller]
            if axis in self.__axisValues:
                controller.setValue(self.__axisValues[axis], axis)

    def __registerTriggers(self, controller):
        for trigger in controller.triggers:
            if trigger in self.__controllerByTrigger:
                self.__controllerByTrigger[trigger].append(controller)
            else:
                self.__controllerByTrigger[trigger] = [controller]
            if trigger in self.__triggerValues:
                controller.setValue(self.__triggerValues[trigger], trigger)

    def onLoaded(self, context):
        for controller in self.__controllers:
            controller.onLoaded(context)

    def destroy(self):
        for controller in self.__controllers:
            controller.destroy()

        self.__settings = None
        self.__controllers = []
        self.__controllersByClass.clear()
        self.__controllerByAxis.clear()
        self.__controllerByTrigger.clear()
        return

    def getController(self, controllerName):
        controllerClass = _CONTROLLERS_MAP.get(controllerName, None)
        if controllerClass:
            return self.__createController(controllerClass)
        else:
            return

    def setAxisValue(self, axis, value):
        self.__axisValues[axis] = value
        if axis in self.__controllerByAxis:
            for controller in self.__controllerByAxis[axis]:
                controller.setValue(value, axis)

    def setTriggerValue(self, trigger, value):
        self.__triggerValues[trigger] = value
        if trigger in self.__controllerByTrigger:
            for controller in self.__controllerByTrigger[trigger]:
                controller.trigger(trigger, value)

    def setPropellorAngle(self, left, right):
        angles = [left, right]
        id = 0
        for controller in self.__controllers:
            if controller.__class__ is PropellorControllerL or controller.__class__ is PropellorControllerR:
                controller.setAngle(angles[id % len(angles)])
                id += 1

    def onOwnerChanged(self, owner):
        for controller in self.__controllers:
            controller.onOwnerChanged(owner)