# Embedded file name: scripts/common/featuredObject.py
import BigWorld
from _consumables_data import ModsTypeEnum
import db.DBLogic
from debug_utils import *
from consts import IS_CELLAPP
from _bonusSchemes_data import BonusSchemesDB
if IS_CELLAPP:
    from ConsumablesAction import ACTION_TABLE, ACTIVATION_TABLE
ModsTypesToName = dict(((v, k) for k, v in ModsTypeEnum.__dict__.items() if not k.startswith('__')))

class IEquipmentFeaturedObject(object):

    def applyObjMods(self, modifiers):
        pass


class CamouflageFeatureObject(IEquipmentFeaturedObject):

    def __init__(self, bonusSchemaName, isCamouflageSpecializedForCurMap):
        self.__mods = BonusSchemesDB[bonusSchemaName] if bonusSchemaName else []
        self.__isCamouflageSpecializedForCurMap = isCamouflageSpecializedForCurMap

    def applyObjMods(self, modifiers):
        for mod in self.__mods:
            if self.__isCamouflageSpecializedForCurMap or mod.isActiveForAllMapTypes:
                modifiers.__dict__[ModsTypesToName[mod.type]] *= mod.value_


class EquipmentFeaturedObject(IEquipmentFeaturedObject):

    def __init__(self, data, skillsID):
        self._crewSkillsID = skillsID
        self._equipmentModifierData = db.DBLogic.g_instance.getSkillWithRelations()
        if data != -1:
            self.__mods = db.DBLogic.g_instance.getEquipmentByID(data).mods
        else:
            self.__mods = []

    def _value(self, mod, modifiers):
        res = mod.value_
        for ID, value in self._equipmentModifierData.iteritems():
            key, relations = value
            if ID in self._crewSkillsID and mod.type in relations:
                res = (res - 1.0) * getattr(modifiers, ModsTypesToName[key], {}).get(ID, 1) + 1.0

        return res

    def applyObjMods(self, modifiers):
        for mod in self.__mods:
            modifiers.__dict__[ModsTypesToName[mod.type]] *= self._value(mod, modifiers)


class ConsumableEquipmentFeaturedObject(IEquipmentFeaturedObject):

    def __init__(self, data):
        self.__data = data
        if data['key'] != -1:
            self.__mods = db.DBLogic.g_instance.getConsumableByID(data['key']).mods
            LOG_DEBUG_DEV('found consumable', data, [ (mod.type, mod.value_) for mod in self.__mods ])
        else:
            self.__mods = []

    def applyObjMods(self, modifiers):
        if self.__data['activeTill'] != -1:
            LOG_DEBUG_DEV('applyObjMods', self.__data['key'])
            for mod in self.__mods:
                modifiers.__dict__[ModsTypesToName[mod.type]] *= mod.value_

    def use(self, owner):
        if IS_CELLAPP:
            couldBeActivated = self._isCouldBeActivated(owner)
            if couldBeActivated and self._isReady():
                LOG_DEBUG_DEV('use consumable', self.__data['key'])
                settings = db.DBLogic.g_instance.getConsumableByID(self.__data['key'])
                for i, mod in enumerate(self.__mods):
                    action = ACTION_TABLE.get(mod.type, None)
                    if action:
                        action(owner, mod, settings)

                self.__data['chargesCount'] -= 1
                self.__data['coolDownTill'] = BigWorld.time() + settings.coolDownTime
                self.__data['activeTill'] = BigWorld.time() + settings.effectTime
                return True
            else:
                LOG_DEBUG_DEV("can't use ", self.__data['key'], self.__data, couldBeActivated)
                return False
        else:
            LOG_ERROR("It's senselessly to call this function on client")
        return

    def _isCouldBeActivated(self, owner):
        for mod in self.__mods:
            if mod.activationRequired:
                if mod.type in ACTIVATION_TABLE:
                    if not ACTIVATION_TABLE[mod.type](owner, getattr(mod, 'activationValue', 0)):
                        return False
                else:
                    LOG_ERROR('Modifier was marked as required but not registered in ACTIVATION_TABLE')
                    return False

        return True

    def _isReady(self):
        return self.__data['coolDownTill'] == -1 and self.__data['activeTill'] == -1 and self.__data['chargesCount'] > 0

    def isUsable(self, owner):
        return self._isReady() and self._isCouldBeActivated(owner)

    def update1sec(self):
        t = BigWorld.time()
        if self.__data['coolDownTill'] != -1 and self.__data['coolDownTill'] < t:
            LOG_DEBUG_DEV('clear coolDown', self.__data['key'])
            self.__data['coolDownTill'] = -1
        if self.__data['activeTill'] != -1 and self.__data['activeTill'] < t:
            LOG_DEBUG_DEV('clear activity', self.__data['key'])
            self.__data['activeTill'] = -1
            return bool(self.__mods)
        return False