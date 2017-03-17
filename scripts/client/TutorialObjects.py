# Embedded file name: scripts/client/TutorialObjects.py
import math
import Math
import BigWorld
from MathExt import clamp
from debug_utils import LOG_ERROR, LOG_DEBUG
TUTORIAL_OBJECT_MATERIAL = 'mechTT_003_air_gate_02_mat'
g_instance = None

def Init():
    global g_instance
    if g_instance == None:
        g_instance = TutorialObjects()
    return g_instance


class ObjectRecord(object):

    def __init__(self, position, rotation, model, texture, scale, visible, onModelLoadedCallback):
        self.__visible = visible
        self.__position = position
        self.__rotation = rotation
        self.__scale = scale
        self.__texture = texture
        self.__modelName = model
        self.__model = None
        self.__onModelLoadedCallback = onModelLoadedCallback
        BigWorld.loadResourceListBG((model,), self.__onModelLoaded)
        return

    def lookAt(self, targetPos, rollAngle = 0.0):
        """
        Looks at target
        @param targetPos: target point
        @type targetPos: Math.Vector3
        @param rollAngle: roll angle value
        @type rollAngle: float
        """
        localPos = targetPos - self.__position
        localPos.normalise()
        yawOnTarget = math.atan2(localPos.x, localPos.z)
        pitchOnTarget = -math.asin(clamp(-1.0, localPos.y, 1.0))
        self.setRotation((yawOnTarget, pitchOnTarget, rollAngle))

    def setRotation(self, rotation):
        """
        Set rotation (yaw, pitch, roll)
        @param rotation:
        """
        self.__rotation = rotation
        if self.__model is not None:
            matrix = Math.Matrix()
            matrix.setRotateYPR(self.__rotation)
            matrix.translation = self.__position
            self.__model.worldMatrix = matrix
            self.setScale(self.__scale)
        return

    def __onModelLoaded(self, resourceRefs):
        if self.__modelName not in resourceRefs.failedIDs:
            self.__model = resourceRefs[self.__modelName]
            self.setTexture(self.__texture)
            BigWorld.addModel(self.__model)
            self.update(self.__position, self.__rotation)
            self.setScale(self.__scale)
            self.__model.visible = self.__visible
        else:
            LOG_ERROR("Can't load tutorialObject model", self.__modelName)
        if self.__onModelLoadedCallback is not None:
            self.__onModelLoadedCallback()
            self.__onModelLoadedCallback = None
        return

    def update(self, position, rotation):
        if position is not None:
            self.setPosition(position)
        if rotation is not None:
            self.setRotation(rotation)
        return

    def setTexture(self, texture, scale = None):
        self.setScale(scale)
        if self.__model:
            self.__model.addEffectTextureFashion('objectTexture', 'diffuseMap', TUTORIAL_OBJECT_MATERIAL, texture)
        self.__texture = texture

    def setScale(self, scale):
        if scale is not None:
            if self.__model:
                self.__model.scale = (scale, scale, scale)
            self.__scale = scale
        return

    def setPosition(self, position):
        if self.__model:
            self.__model.position = Math.Vector3(position)
        self.__position = position

    def getPosition(self):
        return self.__position

    def destroy(self):
        if self.__model is not None:
            BigWorld.delModel(self.__model)
            self.__model = None
        return

    def __getVisible(self):
        return self.__visible

    def __setVisible(self, visible):
        self.__visible = visible
        if self.__model:
            self.__model.visible = self.__visible

    visible = property(__getVisible, __setVisible)


class TutorialObjects:

    def __init__(self):
        self.__list = {}

    def remove(self, ID):
        if ID in self.__list:
            self.__list.pop(ID).destroy()
            return True
        return False

    def removeAll(self):
        for key in self.__list.keys():
            self.__list[key].destroy()

        self.__list = {}

    def add(self, ID, position, rotation, model, texture, scale = None, visible = False, onModelLoadedCallback = None):
        if ID is None:
            ID = len(self.__list)
        if ID not in self.__list:
            self.__list[ID] = ObjectRecord(position, rotation, model, texture, scale, visible, onModelLoadedCallback)
            return self.__list[ID]
        else:
            return

    def getObjectById(self, ID):
        if ID in self.__list:
            return self.__list[ID]
        else:
            return None