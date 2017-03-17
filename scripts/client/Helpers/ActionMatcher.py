# Embedded file name: scripts/client/Helpers/ActionMatcher.py
import BigWorld
import math
import Math
from consts import *
from clientConsts import SLATS_AXIS, ACTIONMATCHER_ANIMATION_DISTANCE
from MathExt import *
from EntityHelpers import movementToSpeed
from _performanceCharacteristics_db import airplanes as airplanes_PC
ACTON_MATCH_TIME = 0.25
LOFT_MIN_TIME = 0.5
LOFT_MIN_ROTATION_DEVIATION = 0.15
INTRO_LOFT_MIN_ROTATION_DEVIATION = 0.02
AILERON_LOFT_ANGLE = 19
AILERON_LOFT_SPEED_K = 0.65
YAW_MAX_SPEED = 10.0
PITCH_MAX_SPEED = 10.0
ROLL_MAX_SPEED = 10.0

class ActionMatcher:

    def __init__(self, owner, isPlayer, minLoftRotationDeviation = LOFT_MIN_ROTATION_DEVIATION):
        self.__owner = owner
        self.__isPlayer = isPlayer
        self.__updateCallBack = None
        self.__oldRotate = Math.Vector3(owner.roll, owner.pitch, owner.yaw)
        self.__loftTime = 0
        self.__isSlate = owner.settings.airplane.visualSettings.slateOffset > 0
        self.__slateOnAngle = owner.settings.airplane.visualSettings.slateOnAngle
        self.__minLoftSpeed = 1.4 * airplanes_PC[owner.globalID].stallSpeed / 3.6
        self.__minLoftRotationDeviation = minLoftRotationDeviation
        self.__minAileronLoftSpeed = AILERON_LOFT_SPEED_K * airplanes_PC[owner.globalID].maxSpeed / 3.6
        self.__minAileronLoftAngle = math.radians(AILERON_LOFT_ANGLE)
        self.__update()
        return

    def __update(self):
        modelManipulator = self.__owner.controllers['modelManipulator']
        if self.__isPlayer:
            newRotate = Math.Vector3(self.__owner.roll, self.__owner.pitch, self.__owner.yaw)
            if (newRotate - self.__oldRotate).length > self.__minLoftRotationDeviation and self.__owner.getSpeed() > self.__minLoftSpeed:
                self.__loftTime += ACTON_MATCH_TIME
                if self.__loftTime > LOFT_MIN_TIME:
                    modelManipulator.setEffectVisible('LOFT', True)
            else:
                modelManipulator.setEffectVisible('LOFT', False)
            self.__oldRotate = newRotate
        self.__updateAileronEffects()
        self.__updateCallBack = BigWorld.callback(ACTON_MATCH_TIME, self.__update)
        updateAvatarAnimation = not self.__isPlayer and (self.__owner.position - BigWorld.player().position).length / WORLD_SCALING < ACTIONMATCHER_ANIMATION_DISTANCE
        if self.__isPlayer and self.__owner.autopilot or updateAvatarAnimation:
            yaw = -math.degrees(self.__owner.filter.rotationSpeed[0]) / YAW_MAX_SPEED
            pitch = -math.degrees(self.__owner.filter.rotationSpeed[1]) / PITCH_MAX_SPEED
            roll = math.degrees(self.__owner.filter.rotationSpeed[2]) / ROLL_MAX_SPEED
            modelManipulator.setAxisValue(HORIZONTAL_AXIS, clamp(-1.0, yaw, 1.0))
            modelManipulator.setAxisValue(VERTICAL_AXIS, clamp(-1.0, pitch, 1.0))
            modelManipulator.setAxisValue(ROLL_AXIS, clamp(-1.0, roll, 1.0))
        if self.__slateOnAngle and (self.__isPlayer or updateAvatarAnimation):
            rotation = Math.Quaternion(self.__owner.getRotation())
            speed = movementToSpeed(self.__owner.getWorldVector())
            invRotation = Math.Quaternion(rotation)
            invRotation.invert()
            localSpeed = invRotation.rotateVec(speed)
            airFlowAnglePitch = math.degrees(-math.atan2(localSpeed.y, localSpeed.z))
            if self.__isSlate:
                modelManipulator.setAxisValue(SLATS_AXIS, airFlowAnglePitch)
            modelManipulator.setEffectVisible('ATTACKANGLE', airFlowAnglePitch >= self.__slateOnAngle)

    def __updateAileronEffects(self):
        modelManipulator = self.__owner.controllers['modelManipulator']
        doAileronLoft = self.__owner.getSpeed() > self.__minAileronLoftSpeed and (abs(modelManipulator.getLeftAileronAngle()) > self.__minAileronLoftAngle or abs(modelManipulator.getRightAileronAngle()) > self.__minAileronLoftAngle)
        if self.__isPlayer and doAileronLoft:
            modelManipulator.setEffectVisible('AILERON_LOFT', True)
        else:
            modelManipulator.setEffectVisible('AILERON_LOFT', False)

    def destroy(self):
        if self.__updateCallBack is not None:
            BigWorld.cancelCallback(self.__updateCallBack)
        self.__owner = None
        return

    def setVector(self, old):
        pass