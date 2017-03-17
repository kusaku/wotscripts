# Embedded file name: scripts/common/EntityHelpers.py
import BigWorld
import Math
from consts import *
import db.DBLogic
import db.DBAirCrafts
from _airplanesConfigurations_db import airplanesConfigurations
from debug_utils import *
from MathExt import clampAngle2Pi
from debug_utils import LOG_ERROR
from db.DBEffects import Effects
from _consumables_data import ModsTypeEnum
from CrewHelpers import getCrewSkillsID
from SkillsHelper import getSpecializationSkillByID, calcMainSingleMod, calcNotMainSingleMod, calcNormalSkillValue
PLANE_TYPE_LETTER = dict(((v[0], k) for k, v in PLANE_TYPE_NAME.items()))

def getPlaneGeometryRadius(parts_only_list):
    wing_len = []
    available_component_type_list = ['LeftWing', 'RightWing']
    component_type = lambda p: p.getFirstPartType().componentType
    curr_part = lambda p: component_type(p) in available_component_type_list
    available_parts_list = dict([ (component_type(part), part) for part in parts_only_list if curr_part(part) ])
    for type_, part in available_parts_list.iteritems():
        for upgrade in part.upgrades.values():
            o = sorted(upgrade.bboxes.getList(), key=lambda e: e.size.length)
            if not len(o):
                default_wing_len = 10.0 * WORLD_SCALING
                return [default_wing_len, default_wing_len]
            obj = o[-1]
            wing = obj.size.length + obj.pos.length
            wing_eps = 1.0 * WORLD_SCALING
            wing_len.append(wing + wing_eps)

    return sorted(wing_len)[-1]


def getEntityBattleLevelProperty(entity, battleLevel, propertyID, defaultValue):
    settings = db.DBLogic.g_instance.getDestructibleObjectData(entity)
    if settings:
        if hasattr(settings, 'battleLevelsSettings'):
            return settings.battleLevelsSettings.getDataForLevel(battleLevel)[propertyID]
    return defaultValue


def isAvatar(entity):
    return getattr(entity, 'entityGroupMask', ENTITY_GROUPS.UNDEFINED) & ENTITY_GROUPS.AVATAR != 0


def isAvatarBot(entity):
    return getattr(entity, 'entityGroupMask', ENTITY_GROUPS.UNDEFINED) & ENTITY_GROUPS.AVATAR_BOT != 0


def isPlayerAvatar(entity):
    return getattr(entity, 'entityGroupMask', ENTITY_GROUPS.UNDEFINED) & ENTITY_GROUPS.AVATAR_PLAYER != 0


def isTeamObject(entity):
    return getattr(entity, 'entityGroupMask', ENTITY_GROUPS.UNDEFINED) & ENTITY_GROUPS.TEAM_OBJECT != 0


def isDestructibleObject(entity):
    return getattr(entity, 'entityGroupMask', ENTITY_GROUPS.UNDEFINED) & ENTITY_GROUPS.DESTRUCTIBLE_OBJECT != 0


class ENTITY_GROUPS:
    UNDEFINED = 0
    DESTRUCTIBLE_OBJECT = 1
    AVATAR = 2
    TEAM_OBJECT = 4
    AVATAR_BOT = 8
    AVATAR_PLAYER = 16


ENTITY_GROUPS_SET = set((v for k, v in ENTITY_GROUPS.__dict__.iteritems() if k.find('__') != 0))

class EntitySupportedClasses:
    INVALID = -1
    Avatar = 1
    AvatarBot = 2
    TeamTurret = 3
    TeamObject = 4
    TeamCannon = 5

    @staticmethod
    def getAvatarClassID(entity):
        """
        get numeric representation of entity class
        we can get it for Avatar classes only because we start to use same class TeamObject for all kind of team objects!
        
        @param entity:
        @type entity: BigWorld.Entity
        @return:
        """
        return EntitySupportedClasses.__dict__.get(entity.className, -1)

    @staticmethod
    def isAvatarClassID(classID):
        return classID == EntitySupportedClasses.Avatar or classID == EntitySupportedClasses.AvatarBot

    @staticmethod
    def isTeamObjectClassID(classID):
        return classID == EntitySupportedClasses.TeamTurret or classID == EntitySupportedClasses.TeamObject

    @staticmethod
    def getClassNameByID(classID):
        """
        get string representation of some of EntitySupportedClasses consts
        @param classID:
        @type classID: int
        @return:
        """
        for k, v in EntitySupportedClasses.__dict__.items():
            if v == classID:
                return k

    @staticmethod
    def getClassIDByName(className):
        """
        get numeric representation of entity class name
        @param className:
        @type className: str
        @rtype: int
        """
        return EntitySupportedClasses.__dict__.get(className, -1)


def possibleFarCellEntityCall(callerEntity, targetEntityID, functionName, paramsAsTupleOrArray = ()):
    objCell = BigWorld.entities.get(targetEntityID)
    if objCell:
        f = getattr(objCell, functionName)
        f(*paramsAsTupleOrArray)
    else:
        callerEntity.arenaBase.doFarCall(targetEntityID, functionName, paramsAsTupleOrArray)


def packPosition2DTuple(position, bounds):
    return (__packCoordinate(position.x, bounds[0].x, bounds[1].x), __packCoordinate(position.z, bounds[0].z, bounds[1].z))


def packPosition3DTuple(position, bounds):
    return (__packCoordinate(position.x, bounds[0].x, bounds[1].x), __packHeight(position.y), __packCoordinate(position.z, bounds[0].z, bounds[1].z))


def packAngle2Byte(angleInRadian):
    angle = clampAngle2Pi(angleInRadian) * 180.0 / math.pi
    return int(angle / 360.0 * 255.0)


def unpackAngleFromByte(packRotation):
    return packRotation / 255.0 * 2.0 * math.pi


def __packHeight(height):
    return __packCoordinate(height, -100, 1500)


def __unpackHeight(height):
    return __unpackCoordinate(height, -100, 1500)


def __packCoordinate(coordinate, bound0, bound1):
    minBound = min(bound0, bound1)
    translatedCoordinate = max(coordinate, minBound) - minBound
    delta = abs(bound0 - bound1)
    return int(min(translatedCoordinate / delta * 255.0, 255.0) + 0.5)


def unpackPositionFrom2DTuple(position, bounds):
    return (__unpackCoordinate(position[0], bounds[0].x, bounds[1].x), __unpackCoordinate(position[1], bounds[0].z, bounds[1].z))


def unpackPositionFrom3DTuple(position, bounds):
    return (__unpackCoordinate(position[0], bounds[0].x, bounds[1].x), __unpackHeight(position[1]), __unpackCoordinate(position[2], bounds[0].z, bounds[1].z))


def __unpackCoordinate(coordinate, bound0, bound1):
    delta = abs(bound0 - bound1)
    translatedCoordinate = coordinate / 255.0 * delta
    minBound = min(bound0, bound1)
    return translatedCoordinate + minBound


def speedAbsToMovement(speed):
    return speed * SPEED_SCALING


def movementAbsToSpeed(movement):
    return movement / SPEED_SCALING


def speedToMovement(speed):
    return speed * SPEED_SCALING


def movementToSpeed(movement):
    ort = Math.Vector3(movement)
    return ort / SPEED_SCALING


def isCorrectBombingAngle(entity, entityRotation):
    axisY = entityRotation.getAxisY()
    axisX = entityRotation.getAxisX()
    axisZ = entityRotation.getAxisZ()
    return axisY.y > 0 and abs(axisX.y) < math.sin(entity.settings.airplane.flightModel.weaponOptions.bombingMaxAngleRoll) and axisZ.y > math.sin(entity.settings.airplane.flightModel.weaponOptions.bombingMinAnglePitch) and axisZ.y < math.sin(entity.settings.airplane.flightModel.weaponOptions.bombingMaxAnglePitch)


def buildAndGetWeaponsInfo(weaponsSettings, weaponSlots, weaponSlotFMData = None):

    def generateList():
        for slotID, selectedType in weaponSlots:
            slotData = weaponsSettings.slots.get(slotID, None)
            if slotData:
                weaponType = slotData.types.get(selectedType, None)
                if weaponType:
                    for weapon in weaponType.weapons:
                        weapon.slotID = slotID
                        if weaponSlotFMData:
                            item = weaponSlotFMData[slotID][selectedType]
                            weapon.dispersionAngle = item.dispersionAngle
                            weapon.recoilDispersion = item.recoilDispersion
                            weapon.autoguiderAngle = item.autoguiderAngle
                            weapon.overheatingFullTime = item.overheatingFullTime
                            weapon.gunRestartTime = getattr(item, 'gunRestartTime', 0.0)
                            weapon.coolingCFC = getattr(item, 'coolingCFC', 1.0)
                        yield weapon

                else:
                    LOG_ERROR('Invalid weapon slot index', selectedType)
            else:
                LOG_ERROR('Invalid weapon slot id', slotID)

        return

    return list(generateList())


def buildAndGetDefaultWeaponsInfo(weaponsSettings):

    def generateList():
        for slotData in weaponsSettings.slots.itervalues():
            weaponType = slotData.types[slotData.types.keys()[0]]
            for weapon in weaponType.weapons:
                yield weapon

    return list(generateList())


def getSlotsByGunMask(aircraftID, weaponSlots, gunsMask):
    slots = []
    for slotID, slotConfiguration in weaponSlots:
        wInfo = db.DBLogic.g_instance.getWeaponInfo(aircraftID, slotID, slotConfiguration)
        if wInfo and wInfo[0] == UPGRADE_TYPE.GUN and gunsMask.get(wInfo[1], False):
            slots.append(slotID)

    return slots


def convertArray2Dictionary(array):
    return dict(((d['key'], d['value']) for d in array))


def getEntityVector(entity):
    if IS_CLIENT:
        return entity.getWorldVector()
    elif hasattr(entity, 'vector'):
        return entity.vector * WORLD_SCALING
    else:
        return Math.Vector3(0, 0, 0)


def getRotation(entity):
    if IS_CLIENT:
        res = Math.Quaternion()
        res.fromEuler(entity.roll, entity.pitch, entity.yaw)
        return res
    else:
        direction = entity.direction
        q = Math.Quaternion()
        q.fromEuler(direction[0], direction[1], direction[2])
        return q


def getEntityPartDataByID(entity, partID, entityData = None):
    entityData = entityData or db.DBLogic.g_instance.getDestructibleObjectData(entity)
    if entityData:
        partDB = next((pDB for pID, pDB in entityData.partsSettings.getPartsList() if pID == partID), None)
        if partDB:
            partData = next((partDB.getPartType(it['value']) for it in entity.partTypes if it['key'] == partID), None)
            return partData or partDB.getFirstPartType()
    return


def testGameMode(gameMode, v):
    return gameMode & 15 == v


def testGameFlag(gameMode, v):
    return gameMode & v != 0


def extractGameMode(gameMode):
    return gameMode & 15


def filterPivots(pivots, partTypes, slotTypes):
    """Select only correct pivots for current part types Ids"""
    res = {}
    partTypesMap = convertArray2Dictionary(partTypes)
    for pivot in pivots.mountPoints.values():
        nameParts = pivot.name.split('/', 4)
        partId = int(nameParts[0])
        partUpgradeId = int(nameParts[1])
        slotId = int(nameParts[2])
        slotTypeId = int(nameParts[3])
        if partTypesMap.get(partId, 1) == partUpgradeId and next((v for k, v in slotTypes if k == slotId), -1) == slotTypeId:
            newPivotName = nameParts[4]
            res[newPivotName] = pivot

    out = db.DBAirCrafts.PivotsTunes()
    out.mountPoints = res
    return out


def canControllEntity(entity):
    return entity.state == EntityStates.GAME_CONTROLLED


def canFireControllEntity(entity):
    return entity.state == EntityStates.GAME_CONTROLLED


def canAimToEntity(owner, entity):
    return entity.state & EntityStates.GAME and entity.teamIndex != owner.teamIndex


class EntityStates:
    ALL = 16777215
    UNDEFINED = 0
    CREATED = 1
    WAIT_START = 2
    PRE_START_INTRO = 4
    GAME_CONTROLLED = 8
    DESTROYED_FALL = 16
    DESTROYED = 32
    END_GAME = 64
    BOMBING = 128
    OBSERVER = 256
    OUTRO = 512
    GAME = GAME_CONTROLLED
    DEAD = DESTROYED | DESTROYED_FALL

    @staticmethod
    def getStateName(state):
        for i, v in EntityStates.__dict__.items():
            if type(v) == int and v == state and i[:6] != 'SIGNAL':
                return i

    @staticmethod
    def inState(entity, state):
        return entity.state & state != 0


class EntitySignals:
    SIGNAL_CREATED = 1
    SIGNAL_START_GAME = 2
    SIGNAL_END_GAME = 4
    SIGNAL_ZERO_HEALTH = 8
    SIGNAL_INST_DESTROY = 16
    SIGNAL_TERRAIN_COLLIDE = 32
    SIGNAL_RESPAWN = 64
    SIGNAL_BOMBING = 128
    SIGNAL_OBSERVER = 256
    SIGNAL_INTRO = 512
    SIGNAL_OUTRO = 1024

    @staticmethod
    def getSignalName(state):
        for i, v in EntitySignals.__dict__.items():
            if type(v) == int and v == state and i[:6] == 'SIGNAL':
                return i


class BomberData:

    def __init__(self, teamIndex, initialDelay, startPoint, endPoint, rotation):
        self.teamIndex = teamIndex
        self.initialDelay = initialDelay
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.rotation = rotation


class AvatarFlags:
    EMPTY = 0
    DEAD = 1
    LOST = 2
    LOADED = 4
    TEAM_KILLER = 8


class PART_ENUM:
    HULL = 1
    ENGINE = 2
    LEFT_WING = 3
    RIGHT_WING = 4
    TAIL = 5
    GUNNER = 6
    COLLIDABLE = 7
    PILOT = 8
    FUEL_TANK = 9

    @staticmethod
    def getName(value):
        for k, v in PART_ENUM.__dict__.items():
            if v == value:
                return k


PART_NAME_TO_ENUM = {'Hull': PART_ENUM.HULL,
 'Engine': PART_ENUM.ENGINE,
 'LeftWing': PART_ENUM.LEFT_WING,
 'RightWing': PART_ENUM.RIGHT_WING,
 'Tail': PART_ENUM.TAIL,
 'Pilot': PART_ENUM.PILOT,
 'Gunner': PART_ENUM.GUNNER,
 'Gunner1': PART_ENUM.GUNNER,
 'Collidable': PART_ENUM.COLLIDABLE,
 'FuelTank': PART_ENUM.FUEL_TANK}

def getPartEnum(partTypeData):
    return PART_NAME_TO_ENUM.get(partTypeData.componentType, None)


class DummyPartBase(object):

    def __init__(self, partsSettings, partID, stateID):
        self.partID = partID
        self.stateID = stateID
        self.partTypeData = partsSettings.getPartByID(partID).getFirstPartType()
        self.isAlive = None
        return


LIST_TYPES = (list, tuple, set)

def processValueTypeRecursive(v, keyValuesDict):
    if isinstance(v, dict):
        return dict(((keyValuesDict.get(k, k), processValueTypeRecursive(v[k], keyValuesDict)) for k in v))
    elif v.__class__.__name__ == 'PyFixedDictDataInstance':
        return dict(((keyValuesDict.get(k, k), processValueTypeRecursive(dv, keyValuesDict)) for k, dv in v.items()))
    elif isinstance(v, LIST_TYPES) or v.__class__.__name__ == 'PyArrayDataInstance':
        return [ processValueTypeRecursive(lv, keyValuesDict) for lv in v ]
    else:
        return v


def processValueType(v, keyValuesDict):
    if isinstance(v, dict):
        return dict(((keyValuesDict.get(k, k), v[k]) for k in v))
    elif v.__class__.__name__ == 'PyFixedDictDataInstance':
        return dict(((keyValuesDict.get(k, k), dv) for k, dv in v.items()))
    elif isinstance(v, LIST_TYPES) or v.__class__.__name__ == 'PyArrayDataInstance':
        return [ lv for lv in v ]
    else:
        return v


def translateDictThroughAnother(d, keyValuesDict, recursive = True):
    if recursive:
        return processValueTypeRecursive(d, keyValuesDict)
    else:
        return processValueType(d, keyValuesDict)


def getDefaultSlotsData(globalID):
    shellsCount = []
    guns = {}
    config = airplanesConfigurations[globalID]
    for slotID, weaponConfig in config.weaponSlots:
        weaponInfo = db.DBLogic.g_instance.getWeaponInfo(config.planeID, slotID, weaponConfig)
        if weaponInfo is None:
            continue
        if weaponInfo[0] in (UPGRADE_TYPE.ROCKET, UPGRADE_TYPE.BOMB):
            shellsCount.append({'key': slotID,
             'value': weaponInfo[2]})
        elif weaponInfo[0] == UPGRADE_TYPE.GUN:
            gun = db.DBLogic.g_instance.getComponentByName(COMPONENT_TYPE.GUNS, weaponInfo[1])
            if gun is not None:
                guns[weaponInfo[1]] = gun.defaultBelt
            else:
                LOG_ERROR('No data for gun: ', weaponInfo[1], ' globalID is ', globalID)

    return (shellsCount, guns)


def getReductionPointVector(settings):
    value = settings.reductionPoint
    return Math.Vector3(0.0, 0.0, value)


def getBulletExplosionEffectFromMaterial(gd, materialName):
    if materialName == None:
        materialName = ''
    if hasattr(gd.explosionParticles, materialName):
        explosionEffectName = gd.explosionParticles.__dict__[materialName]
    else:
        explosionEffectName = gd.explosionParticles.default
    if explosionEffectName != '':
        return Effects.getEffectId(explosionEffectName)
    else:
        return


def calculateTeamObjectMaxHealth(arenaType, arenaObjID, battleLevel):
    arenaSettings = db.DBLogic.g_instance.getArenaData(arenaType)
    modelStrID = arenaSettings.getTeamObjectData(arenaObjID)['modelID']
    settings = db.DBLogic.g_instance.getEntityDataByName(db.DBLogic.DBEntities.BASES, modelStrID)
    parts = settings.partsSettings.getPartsList()
    totalHealth = 0
    for partID, part in parts:
        totalHealth += part.getFirstPartType().healthValue

    if settings.battleLevelsSettings:
        return int(totalHealth * settings.battleLevelsSettings.getDataForLevel(battleLevel)['hpK'] + 0.01)
    else:
        LOG_ERROR(modelStrID, 'has not battleLevel property')
        return 0


def isClientReadyToPlay():
    player = BigWorld.player()
    playerClassName = player.__class__.__name__
    return playerClassName == 'PlayerAvatar' and player.clientIsReady or playerClassName == 'PlayerAccount'


def createEmpyPartsSpecification():
    specification = [{}, {}]
    for folder in specification:
        folder[TEAM_OBLECTS_PART_TYPES.ARMORED] = 0
        folder[TEAM_OBLECTS_PART_TYPES.TURRET] = 0
        folder[TEAM_OBLECTS_PART_TYPES.SIMPLE] = 0

    return specification


def calcPlaneMaxHP(globalID, equipment = None, skills = None):
    equipment = equipment or []
    planeID = airplanesConfigurations[globalID].planeID
    logicalParts = airplanesConfigurations[globalID].logicalParts
    healthK = calcModifierForEquipment(equipment, ModsTypeEnum.MAIN_HP, skills)
    planeSettings = db.DBLogic.g_instance.getAircraftData(planeID)
    return round(planeSettings.airplane.calculateHP(logicalParts, healthK))


def calcModifierForEquipment(equipmentIDs, modifierID, skills):
    equipmentModifierData = db.DBLogic.g_instance.getSkillWithRelations()
    crewSkillsIDs = getCrewSkillsID(skills)
    calc = lambda is_main: (calcMainSingleMod if is_main else calcNotMainSingleMod)

    def get_curr_mod(skillID, skillBonus):
        curr_m = 1.0
        for obj in skills:
            for skill in obj['skills']:
                if skillID == skill['key']:
                    is_main = getSpecializationSkillByID(obj['specializationID']) == skillID
                    curr_m *= calc(is_main)(calcNormalSkillValue(skill['value']), skillBonus, 1)

        return curr_m

    def skill_mod_value(modifier):
        res = modifier.value_
        for ID, value in equipmentModifierData.iteritems():
            key, relations = value
            if ID in crewSkillsIDs and modifier.type in relations:
                skill = db.DBLogic.g_instance.getSkillByID(ID)
                if skill is not None:
                    skill_mod = filter(lambda mod_: mod_.type == key, skill.mods)[-1]
                    res = (res - 1.0) * get_curr_mod(ID, skill_mod.states[0] - 1) + 1.0

        return res

    k = 1
    for eqID in equipmentIDs:
        if eqID > 0:
            eq = db.DBLogic.g_instance.getEquipmentByID(eqID)
            if eq:
                for mod in eq.mods:
                    if mod.type == modifierID:
                        k *= skill_mod_value(mod)

            else:
                LOG_WARNING('invalid equipment id', eqID)

    return k


def hasSpectator(entity):
    avatars = entity.entitiesInRange(3, 'Avatar')
    for a in avatars:
        if a.vehicle is not None and a.vehicle.id == entity.id:
            return True

    return False