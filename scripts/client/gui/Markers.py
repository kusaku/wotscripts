# Embedded file name: scripts/client/gui/Markers.py
import BigWorld
import GUI
import Settings
from gui.Scaleform.windows import CustomObject
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem
from gui.Scaleform.UIHelper import getTargetHealth, SQUAD_TYPES, getPlayerNameWithClan
from Helpers.i18n import localizeObject, localizeAirplane
from EntityHelpers import isAvatar, EntityStates
from clientConsts import CombatScreenNames, TEAM_OBJECTS_PARTS_TYPES, POS_OFFSET_Y
from consts import *
import GameEnvironment
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_TRACE, LOG_DEBUG, LOG_WARNING, LOG_INFO
from HUDconsts import DIST_FOR_SELECT_TARGETS, SMALL_MARKERS_STATE_DIST, ALT_MARKERS_VISIBILITY_STATE_DIST
from gui.Scaleform.GameOptions.vo.MarkerSettings import MARKERS_SUB_TYPES, MARKERS_ATTRIBUTES
from gui.Scaleform.GameOptions.vo.MarkerSettings import getTemplateIndexByPlaneType, AVAILABLE_MARKER_PROPERTIES, MARKERS_SUB_TYPES, OLD_MARKERS_ATTRIBUTES, getValueBySystem
ENTITY_GROUP_MARKER_OFFSET = (0.0, -75.0)
ENTITY_GROUP_DISTANCE_VISIBILITY = 1000.0
AVERAGE_DISTANCE_ATTACK_RANGE_K = 1.9
PART_MARKER_DISTANCE_ATTACK_RANGE_K = 1.5
MARKER_MIN_VISIBILITY_DISTANCE = 3000.0 * WORLD_SCALING
MARKER_ALPHA_DISTANCE_STATES = [{'alpha': 0.9 * 100.0,
  'dist': 0.0}, {'alpha': 0.1 * 100.0,
  'dist': MARKER_MIN_VISIBILITY_DISTANCE / WORLD_SCALING}]
PART_MARKER_ALPHA_STATES = [{'alpha': 1.0 * 100.0,
  'dist': 0.0}, {'alpha': 0.5 * 100.0,
  'dist': MARKER_MIN_VISIBILITY_DISTANCE / WORLD_SCALING}]
MARKER_ALPHA_DISTANCE_STATES_TEAM_OBJECTS = [{'alpha': 1.0 * 100.0,
  'dist': 0.0}, {'alpha': 0.1 * 100.0,
  'dist': MARKER_MIN_VISIBILITY_DISTANCE / WORLD_SCALING}]
GROUP_AVERAGE_DISTANCE_ATTACK_RANGE_K = 1.9
GROUP_FAR_DISTANCE_ATTACK_RANGE_K = 3000
GROUP_DISTANCE_VISIBILITY_MIN = 500.0
GROUP_DISTANCE_VISIBILITY_MAX = 1350.0
GROUP_DISTANCE_VISIBILITY_MIN_BASE = 0.0
GROUP_DISTANCE_VISIBILITY_MAX_BASE = 100000.0
ALPHA_BEHIND_OBSTACLE = 0.3 * 100.0
DIST_DELTA_ALPHA_BEHIND_OBSTACLE = 5.0
COLLIDE_OFFSET_POS_Y = 0.4
GROUP_NEAR_DISTANCE_SCALING = 100
GROUP_AVERAGE_DISTANCE_SCALING = 500
GROUP_FAR_DISTANCE_SCALING = 1350

class EntityPartMarker():
    proxy = None
    flashID = 0
    partID = -1
    partType = -1


class EntityType():
    AVATAR = 0
    TEAM_OBJECT = 1


_SETTINGS_ENTITY_TYPES = {EntityType.TEAM_OBJECT: 'groundMarker',
 EntityType.AVATAR: 'airMarker'}

class SideType():
    ENEMY = 1
    FRIENDLY = 2
    SQUADS = 3
    TARGET = 4
    DEAD = 5


OBJECT_MARKER_TYPE = {CombatScreenNames.ENEMY: 1,
 CombatScreenNames.FRIENDLY: 2,
 CombatScreenNames.SQUADS: 3,
 CombatScreenNames.TARGET: 4,
 CombatScreenNames.DEAD: 5}

class Marker():
    proxy = None
    flashID = 0
    entityId = 0
    entityType = 0
    entityName = ''
    playerName = ''
    markerType = 0
    vehicleLevel = 0
    vehicleType = 0
    maxHealth = 0
    objectPartsType = TEAM_OBJECTS_PARTS_TYPES.SIMPLE
    superiorityPoints = 0
    superiorityPointsMax = 0


class MarkerGroup():
    proxy = None
    flashID = 0
    entities = list()
    iconIndex = 0


class Markers():

    def __init__(self):
        self.__markers = dict()
        self.__markersGroup = dict()
        self.__ui = None
        self.__target = None
        self.__targetMarker = None
        self.__initialized = False
        self.__toActivate = set()
        self.__markersParts = dict()
        self.__templateIndex = -1
        return

    def __registerTeamObjectsParts(self):
        gunAttackRange = MeasurementSystem().getMeters(BigWorld.player().controllers['weapons'].getWeaponGroupsMaxAttackRange() / WORLD_SCALING)
        attackDistance = round(gunAttackRange, 2)
        ms = MeasurementSystem()
        distScale = ms.getMeters(1.0 / WORLD_SCALING)
        partMarkersCount = 0
        for objData in GameEnvironment.getClientArena().allObjectsData.itervalues():
            partMarkersCount = max(partMarkersCount, len(objData['settings'].partsSettings.getPartsList()))

        if partMarkersCount:
            self.__ui.call_1('hud.createMarkersParts', partMarkersCount)
            LOG_DEBUG('__registerTeamObjectsParts - create markers part:', partMarkersCount)
            for i in range(partMarkersCount):
                entityPartMarker = EntityPartMarker()
                entityPartMarker.proxy = GUI.EntityPartMarker()
                entityPartMarker.proxy.load(self.__ui.movie, '_root.mcInfoEntities.markerPart{0}'.format(i))
                entityPartMarker.proxy.distanceScale = distScale
                entityPartMarker.proxy.attackDistance = attackDistance * PART_MARKER_DISTANCE_ATTACK_RANGE_K
                entityPartMarker.proxy.setAlphaDistanceStates(PART_MARKER_ALPHA_STATES)
                entityPartMarker.flashID = i
                self.__markersParts[i] = entityPartMarker

    def __registerTeamObjects(self):
        player = BigWorld.player()
        clientArena = GameEnvironment.getClientArena()
        LOG_INFO('__registerTeamObjects - ', clientArena.allObjectsData.keys())
        for objID, objData in clientArena.allObjectsData.iteritems():
            if not objData.get('valid', False):
                continue
            try:
                if SUPERIORITY2_BASE_HEALTH:
                    groupName = objData['groupName']
                    if groupName:
                        if groupName not in self.__markersGroup:
                            markerGroup = MarkerGroup()
                            sideType = SideType.ENEMY if objData['teamIndex'] != player.teamIndex else SideType.FRIENDLY
                            markerGroup.proxy = GUI.EntityGroupMarker(EntityType.TEAM_OBJECT, sideType)
                            self.__markersGroup[groupName] = markerGroup
                            self.__markersGroup[groupName].entities = list()
                        if objID not in self.__markersGroup[groupName].entities:
                            self.__markersGroup[groupName].entities.append(objID)
                marker = Marker()
                marker.entityType = EntityType.TEAM_OBJECT
                marker.objectPartsType = GameEnvironment.getHUD().getTeamObjectTypeByParts(objID)
                marker.entityId = objID
                marker.markerType = CombatScreenNames.ENEMY if objData['teamIndex'] != player.teamIndex else CombatScreenNames.FRIENDLY
                if objData['settings'].turretName:
                    marker.vehicleType = TYPE_TEAM_OBJECT.TURRET
                else:
                    marker.vehicleType = objData['settings'].type
                    if marker.vehicleType == TYPE_TEAM_OBJECT.VEHICLE:
                        marker.vehicleType = TYPE_TEAM_OBJECT.SMALL
                marker.entityName = self.__getTeamObjectName(objID, objData['teamIndex'])
                marker.maxHealth = objData['maxHealth']
                self.__registerEntity(marker)
            except KeyError:
                LOG_CURRENT_EXCEPTION()

    def __registerAvatars(self):
        player = BigWorld.player()
        clientArena = GameEnvironment.getClientArena()
        playerInfo = clientArena.getAvatarInfo(player.id)
        LOG_INFO('__registerAvatars - ', clientArena.avatarInfos.keys())
        for entityID, avatarData in clientArena.avatarInfos.iteritems():
            if entityID != player.id and avatarData['copyFromAvatarID'] == 0:
                marker = Marker()
                marker.entityType = EntityType.AVATAR
                marker.entityId = entityID
                if avatarData['teamIndex'] == player.teamIndex:
                    squadID = avatarData['squadID']
                    if squadID > 0 and squadID == playerInfo['squadID']:
                        marker.markerType = CombatScreenNames.SQUADS
                    else:
                        marker.markerType = CombatScreenNames.FRIENDLY
                else:
                    marker.markerType = CombatScreenNames.ENEMY
                marker.vehicleType = avatarData['settings'].airplane.planeType
                marker.vehicleLevel = avatarData['settings'].airplane.level
                marker.playerName = getPlayerNameWithClan(avatarData['playerName'], avatarData.get('clanAbbrev', '')) if not GameEnvironment.getHUD().isTutorial() else ''
                marker.entityName = localizeAirplane(avatarData['settings'].airplane.name)
                marker.maxHealth = avatarData['maxHealth']
                self.__registerEntity(marker)

    def __registerEntity(self, marker):
        marker.proxy = GUI.EntityMarker(marker.entityType, OBJECT_MARKER_TYPE[marker.markerType], marker.entityId)
        for altState in MARKERS_SUB_TYPES:
            self.__setSettings(altState, marker)

        self.__markers[marker.entityId] = marker

    def __setSettings(self, altState, marker, markerSettings = None):
        if markerSettings is None:
            markerSettings = GUI.EntityMarkerSettings()
            markerSettings.defaultDistanceVisible = MARKER_MIN_VISIBILITY_DISTANCE / WORLD_SCALING
        entityTypeStr = _SETTINGS_ENTITY_TYPES[marker.entityType]
        attrValues = Settings.g_instance.getMarkerSettings(self.__templateIndex, entityTypeStr, marker.markerType, altState)
        for attr in AVAILABLE_MARKER_PROPERTIES:
            attrData = attrValues.get(attr)
            if attrData is not None:
                setattr(markerSettings, attr, attrData)
            else:
                LOG_WARNING('__setSettings - attr not found in marker settings!', attr, altState, marker.entityType, marker.markerType)

        marker.proxy.setSettings(markerSettings, self.__isSettingsAlt(altState))
        return

    @property
    def initialized(self):
        return self.__initialized

    def destroy(self):
        self.__target = None
        self.__targetMarker = None
        self.__markers.clear()
        self.__toActivate.clear()
        self.__markersParts.clear()
        self.__markersGroup.clear()
        self.__ui = None
        return

    def load(self, ui):
        self.__templateIndex = getTemplateIndexByPlaneType(BigWorld.player().settings.airplane.planeType)
        self.__registerTeamObjects()
        self.__registerAvatars()
        self.__ui = ui
        self.__ui.call_1('hud.createEntities', len(self.__markers), POS_OFFSET_Y)
        gunAttackRange = BigWorld.player().controllers['weapons'].getWeaponGroupsMaxAttackRange()
        ms = MeasurementSystem()
        distUnits = ms.localizeHUD('ui_meter')
        distScale = ms.getMeters(1.0 / WORLD_SCALING)
        ownerInfo = GameEnvironment.getClientArena().getAvatarInfo(BigWorld.player().id)
        unitNumberFlag = 1 << ownerInfo['unitNumber'] - 1
        i = 0
        for entityID, marker in self.__markers.iteritems():
            marker.flashID = i
            self.__addMarker(marker)
            marker.proxy.load(self.__ui.movie, '_root.mcInfoEntities.entity{0}'.format(i), i)
            marker.proxy.distanceScale = distScale
            marker.proxy.distanceUnits = distUnits
            marker.proxy.unitNumberFlag = unitNumberFlag
            marker.proxy.alphaBehindObstacle = ALPHA_BEHIND_OBSTACLE
            marker.proxy.distDeltaAlphaBehindObstacle = DIST_DELTA_ALPHA_BEHIND_OBSTACLE
            marker.proxy.seaLevel = GameEnvironment.getHUD().getSeaLevel()
            if marker.entityType == EntityType.TEAM_OBJECT:
                marker.proxy.setAlphaDistanceStates(MARKER_ALPHA_DISTANCE_STATES_TEAM_OBJECTS)
                marker.proxy.collideOffsetPosY = COLLIDE_OFFSET_POS_Y
            else:
                marker.proxy.setAlphaDistanceStates(MARKER_ALPHA_DISTANCE_STATES)
            if self.__checkMarkerForActivate(marker) and marker.entityId in self.__toActivate:
                marker.proxy.activate(True)
                self.__toActivate.remove(marker.entityId)
            i += 1

        if SUPERIORITY2_BASE_HEALTH:
            self.__ui.call_1('hud.createEntitiesGroup', len(self.__markersGroup))
            distStates = (GROUP_NEAR_DISTANCE_SCALING, GROUP_AVERAGE_DISTANCE_SCALING, GROUP_FAR_DISTANCE_SCALING)
            j = 0
            for groupName, markerGroup in self.__markersGroup.iteritems():
                markerGroup.flashID = j
                data = CustomObject()
                data.iconIndex = markerGroup.iconIndex
                data.text = ''
                self.__ui.call_1('hud.addMarkerGroup', markerGroup.flashID, data)
                markerGroup.proxy.load(self.__ui.movie, '_root.mcInfoEntities.groupEntity{0}'.format(j), j)
                if groupName == ['', '']:
                    markerGroup.proxy.distanceVisibilityMin = GROUP_DISTANCE_VISIBILITY_MIN_BASE
                    markerGroup.proxy.distanceVisibilityMax = GROUP_DISTANCE_VISIBILITY_MAX_BASE
                else:
                    markerGroup.proxy.distanceVisibilityMin = GROUP_DISTANCE_VISIBILITY_MIN
                    markerGroup.proxy.distanceVisibilityMax = GROUP_DISTANCE_VISIBILITY_MAX
                markerGroup.proxy.iconIndex = data.iconIndex
                markerGroup.proxy.setEntities(tuple(markerGroup.entities))
                markerGroup.proxy.offset = ENTITY_GROUP_MARKER_OFFSET
                markerGroup.proxy.groupName = groupName
                j += 1

        self.__registerTeamObjectsParts()
        self.__target = GUI.EntityTarget()
        self.__target.load(self.__ui.movie, '_root.mcInfoEntities.marker')
        self.__initialized = True
        LOG_TRACE('Markers initialized')

    def setMatrix(self, groupName, entityID, mtxProvider):
        if groupName in self.__markersGroup:
            self.__markersGroup[groupName].proxy.setMatrix(entityID, mtxProvider)

    def activateGroup(self, groupName, iconIndex, text):
        if groupName in self.__markersGroup:
            data = CustomObject()
            data.iconIndex = iconIndex
            data.text = text
            self.__ui.call_1('hud.setGroupIcon', self.__markersGroup[groupName].flashID, data)
            self.__markersGroup[groupName].proxy.iconIndex = iconIndex
            self.__markersGroup[groupName].proxy.activate(bool(iconIndex))
        else:
            LOG_TRACE('activateGroup - groupName not in __markersGroup', groupName, iconIndex)

    def __addMarker(self, marker):
        targetInfoObject = CustomObject()
        targetInfoObject.entityType = marker.entityType
        targetInfoObject.sideType = OBJECT_MARKER_TYPE[marker.markerType]
        targetInfoObject.targetType = marker.vehicleType
        targetInfoObject.targetLevel = marker.vehicleLevel
        targetInfoObject.playerName = marker.playerName
        targetInfoObject.entityName = marker.entityName
        targetInfoObject.maxHealth = marker.maxHealth
        targetInfoObject.targetOutline = False
        targetInfoObject.entityId = marker.entityId
        targetInfoObject.health = marker.maxHealth
        targetInfoObject.objectPartsType = marker.objectPartsType
        self.__ui.call_1('hud.addEntity', marker.flashID, targetInfoObject)

    def rebuild(self):
        LOG_TRACE('Markers rebuild ')
        if self.initialized:
            ms = MeasurementSystem()
            distUnits = ms.localizeHUD('ui_meter')
            distScale = ms.getMeters(1.0 / WORLD_SCALING)
            for entityID, marker in self.__markers.iteritems():
                marker.proxy.distanceScale = distScale
                marker.proxy.distanceUnits = distUnits
                marker.proxy.setModuleState(-1, -1)
                for altState in MARKERS_SUB_TYPES:
                    self.__setSettings(altState, marker)

    def __isSettingsAlt(self, altState):
        return bool(altState == 'alt')

    def activateEntity(self, entity):
        if self.initialized:
            if entity.id in self.__markers:
                if entity.id != BigWorld.player().curVehicleID:
                    if self.__checkMarkerForActivate(self.__markers[entity.id]):
                        self.__markers[entity.id].proxy.activate(True)
                    else:
                        self.__toActivate.add(entity.id)
                    if self.__markers[entity.id].entityType == EntityType.TEAM_OBJECT:
                        self.changeTeamObjectPartGroup(entity)
        else:
            self.__toActivate.add(entity.id)

    def getRectangle(self, entityID):
        """
        @param entityID: <int>
        @return: (x:float, y:float, width:int, height:int)
        """
        if self.initialized:
            marker = self.__markers.get(entityID, None)
            if marker is not None:
                return marker.proxy.getMovieRectangle()
        return

    def __checkMarkerForActivate(self, marker):
        if EntityStates.inState(BigWorld.player(), EntityStates.PRE_START_INTRO):
            return marker.entityType == EntityType.AVATAR and marker.markerType != CombatScreenNames.ENEMY
        return True

    def activateAll(self):
        if self.initialized:
            for id in self.__toActivate:
                if id in self.__markers:
                    self.__markers[id].proxy.activate(True)

            self.__toActivate.clear()

    def deactivateEntity(self, entity):
        if self.initialized:
            if entity.id in self.__markers:
                self.__markers[entity.id].proxy.activate(False)
        if entity.id in self.__toActivate:
            self.__toActivate.remove(entity.id)

    def update(self):
        pass

    def __getTeamObjectName(self, ID, teamIndex):
        entityName = None
        objData = GameEnvironment.getClientArena().allObjectsData.get(ID, None)
        if objData is not None:
            entityName = localizeObject(objData['settings'].name)
        if not SUPERIORITY2_BASE_HEALTH and teamIndex != BigWorld.player().teamIndex and not GameEnvironment.getHUD().isTutorial():
            supPoints, supPointsMax = GameEnvironment.getClientArena().getSuperiorityPoints4TeamObject(ID)
            if supPoints is not None:
                entityName += ''.join([' (',
                 str(supPoints),
                 '/',
                 str(supPointsMax),
                 ')']) if not GameEnvironment.getHUD().isTutorial() else ''
        return entityName

    def changeTeamObjectPartGroup(self, en):
        if not SUPERIORITY2_BASE_HEALTH:
            self.__updateTeamObjectType(en.id)
            marker = self.__markers.get(en.id, None)
            if marker:
                data = CustomObject()
                data.entityName = self.__getTeamObjectName(en.id, en.teamIndex)
                if data.entityName is not None:
                    self.__ui.call_1('hud.updateEntityData', marker.flashID, data)
        return

    def changeTOPartState(self, id, partID):
        self.__updateTeamObjectType(id)
        if self.__targetMarker and self.__targetMarker.entityId == id:
            for marker in self.__markersParts.itervalues():
                if marker.partID == partID:
                    marker.proxy.isDestroyed = True
                    break

    def __activateEntityPartMarker(self, isActive):
        for marker in self.__markersParts.itervalues():
            marker.proxy.activate(False)
            marker.proxy.attachTo(None)

        if isActive:
            self.__updateTeamObjectType(self.__targetMarker.entityId)
            i = 0
            partsInfoDict = GameEnvironment.getHUD().getTeamObjectPartsTypes(self.__targetMarker.entityId, None, True)
            for partId, partData in partsInfoDict.iteritems():
                self.__markersParts[i].partID = partId
                self.__markersParts[i].partType = partData['type']
                self.__markersParts[i].proxy.attachTo(self.__targetMarker.proxy)
                self.__markersParts[i].proxy.updatePartData(partId, partData['type'], self.__markersParts[i].flashID)
                self.__markersParts[i].proxy.activate(True)
                self.__markersParts[i].proxy.isDestroyed = partData['isDead']
                i += 1

        return

    def __updateTeamObjectType(self, ID):
        marker = self.__markers.get(ID, None)
        if marker:
            objectPartsType = GameEnvironment.getHUD().getTeamObjectTypeByParts(ID)
            if objectPartsType != TEAM_OBJECTS_PARTS_TYPES.ERROR:
                targetInfoObject = CustomObject()
                targetInfoObject.objectPartsType = objectPartsType
                self.__ui.call_1('hud.setTeamObjectData', marker.flashID, targetInfoObject)
        return

    def selectTarget(self, entity):
        if self.initialized:
            try:
                if self.__targetMarker:
                    self.__targetMarker.markerType = CombatScreenNames.ENEMY
                    for altState in MARKERS_SUB_TYPES:
                        self.__setSettings(altState, self.__targetMarker)

                    self.__targetMarker = None
                if entity:
                    import config_consts
                    if config_consts.IS_DEVELOPMENT and config_consts.IS_QA_TESTING and __debug__ and entity.id not in self.__markers:
                        return
                    self.__targetMarker = self.__markers[entity.id]
                    self.__targetMarker.markerType = CombatScreenNames.TARGET
                    for altState in MARKERS_SUB_TYPES:
                        self.__setSettings(altState, self.__targetMarker)

                    self.__ui.call_1('hud.setMarker', self.__targetMarker.flashID)
                else:
                    self.__ui.call_1('hud.removeMarker')
            except KeyError:
                LOG_CURRENT_EXCEPTION()

            if self.__targetMarker and self.__targetMarker.entityType == EntityType.TEAM_OBJECT:
                self.__target.attachTo(self.__targetMarker.proxy)
                self.__activateEntityPartMarker(True)
            else:
                self.__target.attachTo(None)
                self.__activateEntityPartMarker(False)
        return

    def setModuleState(self, entityID, hudPartID, partState):
        marker = self.__markers.get(entityID, None)
        if marker and hudPartID is not None:
            marker.proxy.setModuleState(hudPartID, partState)
        return