# Embedded file name: scripts/client/gui/MapEntry.py
import Math
from gui.HUDconsts import *
from EntityHelpers import EntitySupportedClasses
from debug_utils import LOG_DEBUG
import db.DBLogic
import BigWorld
from consts import *

class MapEntry:

    def __init__(self, objID, classID, teamIndex, position, isAlive, modelID):
        self.id = objID
        self.classID = classID
        self.teamIndex = teamIndex
        self.mapMatrix = Math.Matrix()
        self.mapMatrix.setTranslate(position)
        self.isAlive = isAlive
        self.addedToPlate = False
        self.inClientWorld = False
        if self.classID == EntitySupportedClasses.TeamTurret:
            self.mapTexture = HUD_MINIMAP_ENTITY_TYPE_TURRET
        elif self.classID == EntitySupportedClasses.TeamObject:
            settings = db.DBLogic.g_instance.getBaseData(modelID)
            if settings.turretName:
                self.mapTexture = HUD_MINIMAP_ENTITY_TYPE_TURRET
            else:
                self.mapTexture = settings.type == TYPE_TEAM_OBJECT.BIG and HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT_BASE or HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT
        elif self.classID == EntitySupportedClasses.Avatar or self.classID == EntitySupportedClasses.AvatarBot:
            self.mapTexture = HUD_MINIMAP_ENTITY_TYPE_AVATAR
        else:
            LOG_DEBUG('Unsupported class ID', self.classID)
            self.mapTexture = HUD_MINIMAP_ENTITY_TYPE_UNKNOWN
        self.superiorityPoints = 0
        if self.classID not in [EntitySupportedClasses.Avatar, EntitySupportedClasses.AvatarBot]:
            self.superiorityPoints = db.DBLogic.g_instance.getBaseData(modelID).superiorityPoints
            self.superiorityPointsMax = self.superiorityPoints

    def getMapTexture(self):
        return self.mapTexture

    def setPositionAndYaw(self, newPos, yaw):
        self.mapMatrix.setRotateYPR((yaw, 0, 0))
        self.mapMatrix.translation = newPos

    @property
    def position(self):
        return self.mapMatrix.translation