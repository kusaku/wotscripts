# Embedded file name: scripts/common/ComponentModel/CameraComponents.py
import sys
import inspect
import BigWorld
import Math
import math
from db import DBLogic
from Component import Component, InputSlot, OutputSlot
from consts import IS_CLIENT, IS_EDITOR
from MathExt import clamp
if IS_CLIENT:
    from CameraStates import CameraState
    from gui.Scaleform.utils.HangarSpace import g_hangarSpace
hangarCameraOldMatrix = Math.Matrix()
isFreeHangarCamera = False

class FreeHangarCamera(Component):

    @classmethod
    def componentCategory(cls):
        return 'Camera'

    def slotDefinitions(self):
        return [InputSlot('input', Component.SLOT_EVENT, FreeHangarCamera._onInput), InputSlot('enable', Component.SLOT_BOOL, None), OutputSlot('out', Component.SLOT_EVENT, None)]

    def _onInput(self, enable):
        global isFreeHangarCamera
        global hangarCameraOldMatrix
        if IS_CLIENT:
            if g_hangarSpace is not None:
                clientHangarSpace = g_hangarSpace.space
                if clientHangarSpace:
                    if enable and not isFreeHangarCamera:
                        hangarCameraOldMatrix = BigWorld.camera().parentMatrix
                        clientHangarSpace.hangarCamera.setState(CameraState.SuperFree)
                        isFreeHangarCamera = True
                    if not enable and isFreeHangarCamera:
                        BigWorld.camera().parentMatrix = hangarCameraOldMatrix
                        clientHangarSpace.hangarCamera.leaveState()
                        isFreeHangarCamera = False
        return 'out'


class SetCameraPosAndTarget(Component):

    def __init__(self):
        self._source = Math.Matrix()
        self._target = Math.Matrix()
        self._parent = Math.Matrix()

    @classmethod
    def componentCategory(cls):
        return 'Camera'

    def slotDefinitions(self):
        return [InputSlot('input', Component.SLOT_EVENT, SetCameraPosAndTarget._onInput),
         InputSlot('position', Component.SLOT_VECTOR3, None),
         InputSlot('target', Component.SLOT_VECTOR3, None),
         OutputSlot('out', Component.SLOT_EVENT, None)]

    def _onInput(self, position, targetPos):
        localPos = targetPos - position
        localPos.normalise()
        yawOnTarget = math.atan2(localPos.x, localPos.z)
        pitchOnTarget = -math.asin(clamp(-1.0, localPos.y, 1.0))
        self._parent.setRotateYPR((yawOnTarget, pitchOnTarget, 0))
        self._parent.translation = position
        if IS_CLIENT:
            if g_hangarSpace is not None:
                clientHangarSpace = g_hangarSpace.space
                if clientHangarSpace:
                    strategy = clientHangarSpace.hangarCamera.getStateStrategy()
                    if strategy and isinstance(strategy, BigWorld.CameraStrategySuperFree):
                        self._source.setTranslate(position)
                        self._target.setTranslate(targetPos)
                        strategy.sourceProvider = self._source
                        strategy.targetProvider = self._target
                        BigWorld.camera().parentMatrix = self._parent
        else:
            import WorldEditor
            self._parent.invert()
            WorldEditor.camera(0).view = self._parent
        return 'out'


class SetCameraPosAndRotation(Component):

    def __init__(self):
        self._source = Math.Matrix()
        self._target = Math.Matrix()
        self._parent = Math.Matrix()

    @classmethod
    def componentCategory(cls):
        return 'Camera'

    def slotDefinitions(self):
        return [InputSlot('input', Component.SLOT_EVENT, SetCameraPosAndRotation._onInput),
         InputSlot('position', Component.SLOT_VECTOR3, None),
         InputSlot('yaw', Component.SLOT_ANGLE, None),
         InputSlot('pitch', Component.SLOT_ANGLE, None),
         InputSlot('roll', Component.SLOT_ANGLE, None),
         OutputSlot('out', Component.SLOT_EVENT, None)]

    def _onInput(self, position, yaw, pitch, roll):
        self._parent.setRotateYPR(Math.Vector3(yaw, pitch, roll))
        self._parent.translation = position
        if IS_CLIENT:
            if g_hangarSpace is not None:
                clientHangarSpace = g_hangarSpace.space
                if clientHangarSpace:
                    strategy = clientHangarSpace.hangarCamera.getStateStrategy()
                    if strategy and isinstance(strategy, BigWorld.CameraStrategySuperFree):
                        direction = Math.Vector3(self._parent.get(2, 0), self._parent.get(2, 1), self._parent.get(2, 2))
                        fakeTarget = Math.Vector3(position.x + direction.x, position.y + direction.y, position.z + direction.z)
                        self._source.setTranslate(position)
                        self._target.setTranslate(fakeTarget)
                        strategy.sourceProvider = self._source
                        strategy.targetProvider = self._target
                        BigWorld.camera().parentMatrix = self._parent
        else:
            import WorldEditor
            self._parent.invert()
            WorldEditor.camera(0).view = self._parent
        return 'out'


class SplinePoint(Component):

    def slotDefinitions(self):
        return [InputSlot('spline_id', Component.SLOT_STR, None),
         InputSlot('time', Component.SLOT_FLOAT, None),
         OutputSlot('position', Component.SLOT_VECTOR3, SplinePoint._getSplinePos),
         OutputSlot('yaw', Component.SLOT_ANGLE, SplinePoint._getSplineYaw),
         OutputSlot('pitch', Component.SLOT_ANGLE, SplinePoint._getSplinePitch),
         OutputSlot('roll', Component.SLOT_ANGLE, SplinePoint._getSplineRoll)]

    def _getSplinePos(self, splineId, time):
        return DBLogic.g_instance.getSpline(splineId).getPointForTime(time)

    def _getSplineYaw(self, splineId, time):
        spline = DBLogic.g_instance.getSpline(splineId)
        if IS_CLIENT:
            return spline.bwSpline.getYawForTime(time)
        A = spline.getPointForTime(time - 1.0)
        C = spline.getPointForTime(time + 1.0)
        return math.atan2(C.x - A.x, C.z - A.z)

    def _getSplineRoll(self, splineId, time):
        return 0.0

    def _getSplinePitch(self, splineId, time):
        return 0.0


def getModuleComponents():
    return list((value for key, value in inspect.getmembers(sys.modules[__name__], inspect.isclass) if issubclass(value, Component) and value is not Component))