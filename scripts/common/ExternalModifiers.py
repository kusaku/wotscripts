# Embedded file name: scripts/common/ExternalModifiers.py
from CrewHelpers import getCrewSpecializationByName, getCrewSkillsID
from AvatarControllerBase import AvatarControllerBase
import Event
from debug_utils import LOG_ERROR, LOG_DEBUG
from featuredObject import EquipmentFeaturedObject, ConsumableEquipmentFeaturedObject, ModsTypesToName, CamouflageFeatureObject
from CrewSkills.CrewSkills import CrewSkills
import db.DBLogic
from _consumables_data import ModsTypeEnum
from config_consts import IS_DEVELOPMENT
import BigWorld
from EntityHelpers import EntityStates, isPlayerAvatar
from CrewSkills.SkillConditions import SkillConditions
from consts import SKILL_EVENT, IS_CELLAPP
from CrewSkills.EnemySkillsObserver import EnemySkillObserver
import functools
from _skills_data import SpecializationEnum
_DebugConsumables = {}
_DebugEquipment = {}
_DebugCrewSkills = {SpecializationEnum.PILOT: [{'key': 1,
                             'value': 100.0}, {'key': 246,
                             'value': 50.0}, {'key': 247,
                             'value': 50.0}],
 SpecializationEnum.GUNNER: [{'key': 2,
                              'value': 50.0}, {'key': 248,
                              'value': 50.0}],
 SpecializationEnum.NAVIGATOR: []}

class OBJ_GROUPS:
    CREW = 0
    CONSUMABLES = 1
    EQUIPMENT = 2
    CAMOUFLAGE = 3


class Modifiers:

    def __init__(self):
        for modName in ModsTypesToName.values():
            setattr(self, modName, 1.0)

        self.reset()

    def dump(self):
        return {modName:getattr(self, modName) for modName in ModsTypesToName.values()}

    def reset(self):
        for modName in ModsTypesToName.values():
            self.__dict__[modName] = 1.0

    def debugPrint(self, ownerID):
        print (ownerID, 'Avatar Modifiers')
        l = ModsTypesToName.values()
        l.sort()
        for modName in l:
            print (modName, '=', self.__dict__[modName])

    def printDiff(self, otherModifiersDict):
        for modName in ModsTypesToName.values():
            rightValue = getattr(self, modName, 1.0)
            leftValue = otherModifiersDict.get(modName, 1.0)
            if leftValue != rightValue:
                print 'Modifier changed: {0} - {1} => {2}'.format(modName, leftValue, rightValue)

    def getByID(self, modTypeID):
        return self.__dict__[ModsTypesToName[modTypeID]]

    def getByName(self, modName):
        return self.__dict__[modName]


class ExternalModifiersTeamObject(AvatarControllerBase):
    DEFAULT_MODIFIERS = Modifiers()

    def __init__(self, owner):
        AvatarControllerBase.__init__(self, owner)
        self.modifiers = ExternalModifiersTeamObject.DEFAULT_MODIFIERS
        self.eModifiersChanged = Event.Event()

    @property
    def crew(self):
        return []

    def generateUsedConsumables(self):
        return []

    def tryToUseConsumable(self, name):
        pass


class TestExternalModifiers(object):

    def __init__(self, activate):
        self._activate = activate

    def _checkOnChange(self, old, new):
        if len(new):
            return new
        return old

    def _copySkills(self, skillsData):
        newData = []
        for obj in skillsData:
            newData.append({'specializationID': obj['specializationID'],
             'skills': obj['skills'][:]})

        return newData

    def _getNewSkills(self, skillsData):
        data = self._copySkills(skillsData)
        for obj in data:
            if obj.has_key('specializationID'):
                d = _DebugCrewSkills[obj['specializationID']]
                obj['skills'] = self._checkOnChange(obj['skills'], d)

        return data

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self._activate:
                args = [args[0],
                 args[1],
                 self._checkOnChange(args[-3], _DebugConsumables),
                 self._checkOnChange(args[-2], _DebugEquipment),
                 self._getNewSkills(args[-1])]
                LOG_DEBUG('TestExternalModifiers is enabled:', args[-3:])
            return func(*args, **kwargs)

        return wrapper


class ExternalModifiers(AvatarControllerBase):

    def __init__(self, owner, consumables, equipment, crewSkills):
        AvatarControllerBase.__init__(self, owner)
        self.__skillConditions = SkillConditions(owner, SKILL_EVENT)
        self.__objects = {OBJ_GROUPS.CREW: [ CrewSkills(owner, obj, self.__skillConditions, index) for index, obj in enumerate(crewSkills) ],
         OBJ_GROUPS.CONSUMABLES: [ ConsumableEquipmentFeaturedObject(obj) for obj in consumables ],
         OBJ_GROUPS.EQUIPMENT: [ EquipmentFeaturedObject(obj, getCrewSkillsID(crewSkills)) for obj in equipment ],
         OBJ_GROUPS.CAMOUFLAGE: [CamouflageFeatureObject(owner.camouflageBonusSchemeName, owner.isCamouflageSpecializedForCurMap)]}
        self.__specializationIdToObj = {}
        for crewMember in self.__objects[OBJ_GROUPS.CREW]:
            self.__specializationIdToObj[crewMember.specializationID] = crewMember

        self.eModifiersChanged = Event.Event()
        self.modifiers = Modifiers()

    def getFeatureObjects(self, featureObjectClass):
        return self.__objects.get(featureObjectClass, None)

    def destroy(self):
        AvatarControllerBase.destroy(self)
        for crewMember in self.__objects[OBJ_GROUPS.CREW]:
            crewMember.destroy()

        self.__objects.clear()
        self.__specializationIdToObj.clear()
        self.eModifiersChanged.clear()
        self.__skillConditions.destroy()

    def onPartStateChanged(self, part):
        self.onPartsStateChanged([part])

    def onPartsStateChanged(self, parts):
        reCalc = False
        for part in parts:
            specID = getCrewSpecializationByName(part.partTypeData.componentType)
            if specID in self.__specializationIdToObj:
                self.__specializationIdToObj[specID].changeState(part.logicalState)
                reCalc = True

        if reCalc:
            self.reCalc()

    def __findSlotIDByConsumableName(self, name):
        for slotID, slot in enumerate(self._owner.consumables):
            if slot['key'] != -1:
                consumable = db.DBLogic.g_instance.getConsumableByID(slot['key'])
                if consumable:
                    if consumable.localizeTag == name:
                        return slotID
                else:
                    LOG_ERROR("Can't find consumable {c} description".format(c=slot['key']))

    def isConsumablePresent(self, name):
        slotID = self.__findSlotIDByConsumableName(name)
        if slotID is not None:
            return self._owner.consumables[slotID]['chargesCount'] > 0
        else:
            return False

    def tryToUseConsumable(self, name):
        slotID = self.__findSlotIDByConsumableName(name)
        if slotID is not None:
            self.onUseConsumable(slotID)
        return

    def onUseConsumable(self, slotID):
        slot = self._owner.consumables[slotID]
        if slot['key'] != -1:
            consumable = self.__objects[OBJ_GROUPS.CONSUMABLES][slotID]
            from debug_utils import LOG_DEBUG_DEV
            LOG_DEBUG_DEV('onUseConsumable', slotID)
            if consumable.use(self._owner):
                self.reCalc()

    def generateUsedConsumables(self):
        for i, slot in enumerate(self._owner.consumables):
            if slot['key'] != -1:
                consumable = db.DBLogic.g_instance.getConsumableByID(slot['key'])
                if consumable.chargesCount != slot['chargesCount']:
                    yield i
                elif consumable.behaviour == 1:
                    slot['chargesCount'] = 0
                    yield i

    def generateUsableConsumables(self):
        for slotID, consumableData in enumerate(self._owner.consumables):
            if consumableData['key'] != -1:
                consumable = self.__objects[OBJ_GROUPS.CONSUMABLES][slotID]
                if not consumable.isUsable(self._owner):
                    continue
                consumableDb = db.DBLogic.g_instance.getConsumableByID(consumableData['key'])
                if consumableDb.behaviour == 1:
                    consumableData['chargesCount'] = 0
                    continue
                yield slotID

    def onControllersCreated(self):
        crew = self.__objects.get(OBJ_GROUPS.CREW, [])
        for c in crew:
            c.afterRestore()

    def restart(self):
        pass

    @property
    def crew(self):
        return self.__objects[OBJ_GROUPS.CREW]

    def reCalc(self):
        if __debug__ and IS_DEVELOPMENT:
            oldModifiers = self.modifiers.dump()
        self.modifiers.reset()
        for objGroup in self.__objects.values():
            for obj in objGroup:
                obj.applyObjMods(self.modifiers)

        self._owner.disguise = (self.modifiers.STEALTH - 1) * 100
        if __debug__ and IS_DEVELOPMENT:
            self.modifiers.printDiff(oldModifiers)
        self.eModifiersChanged(self.modifiers)

    def update1sec(self, ms):
        if not EntityStates.inState(self._owner, EntityStates.GAME):
            return
        if IS_DEVELOPMENT and BigWorld.globalData.get('modifiersUpdateRequired', False) and self._owner.__class__.__name__ == 'Avatar':
            LOG_DEBUG(self._owner.id, 'reload request')
            BigWorld.globalData['modifiersUpdateRequired'] = False
            for crewMember in self.__objects[OBJ_GROUPS.CREW]:
                crewMember.reload()

            wasChanged = True
        else:
            wasChanged = False
        for c in self.__objects[OBJ_GROUPS.CONSUMABLES]:
            if c.update1sec():
                wasChanged = True

        for crewMember in self.__objects[OBJ_GROUPS.CREW]:
            if crewMember.update1sec():
                wasChanged = True

        if wasChanged:
            self.reCalc()

    def onParentSetState(self, stateID, data):
        LOG_DEBUG('Mods.onParentSetState', EntityStates.getStateName(stateID))
        if stateID == EntityStates.GAME:
            for crewMember in self.__objects[OBJ_GROUPS.CREW]:
                crewMember.initGame()

    def getTargetSkillModsActivity(self, crew_member):
        return EnemySkillObserver.get_target_skill_mods_activity(self, crew_member)

    @staticmethod
    def getTargetSkillModValue(crew_member, modsActivity):
        return EnemySkillObserver.get_target_skill_mod_value(crew_member, modsActivity)

    def backup(self):
        if OBJ_GROUPS.CREW not in self.__objects:
            return None
        else:
            res = [ c.backup() for c in self.__objects[OBJ_GROUPS.CREW] ]
            res.append(self.__skillConditions.backup())
            return res

    def restore(self, container):
        if container is None:
            return
        else:
            self.__skillConditions.restore(container.pop())
            crew = self.__objects.get(OBJ_GROUPS.CREW)
            if not crew:
                return
            for c, crewMember in zip(container, crew):
                crewMember.restore(c)

            return


class ExternalModifiersBot(ExternalModifiers):

    def __init__(self, owner, consumables, equipment, crewSkills):
        ExternalModifiers.__init__(self, owner, consumables, equipment, crewSkills)

    def modifyWeaponFocus(self, val):
        self.modifiers.__dict__[ModsTypesToName[ModsTypeEnum.WEAPONS_FOCUS]] = val
        self.eModifiersChanged(self.modifiers)