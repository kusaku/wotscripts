# Embedded file name: scripts/common/CrewSkills/CrewSkills.py
from functools import partial
import BigWorld
from consts import OBJ_STATES, IS_CELLAPP, IS_BASEAPP
from SkillsHelper import getSkillByID, getSkillWithRelations, getSpecializationSkillByID, calcNotMainSingleMod, calcMainSingleMod, calcNormalSkillValue
from featuredObject import IEquipmentFeaturedObject, ModsTypesToName
from debug_utils import LOG_DEBUG_DEV, LOG_ERROR
from SubscribedConditions import SubscribedConditions
from GameLogicEvents import SKILL_ACTIVATED, SKILL_DEACTIVATED
if IS_CELLAPP or IS_BASEAPP:
    from ConsumablesAction import ACTION_TABLE

class SkillRecord:

    def __init__(self, skillObj, skillValue, skillIndex = 0):
        self.obj = skillObj
        self.value = skillValue
        self.index = skillIndex


class CrewSkills(IEquipmentFeaturedObject):
    OFFSET = 5

    def __init__(self, owner, data, conditions, crewIndex):
        self._owner = owner
        self.state = OBJ_STATES.GOOD
        self.specializationID = data['specializationID']
        self._crewIndex = crewIndex
        self.__passiveSkills = []
        self.__activeSkills = {}
        self.__recalcRequired = False
        self.__timers = {}
        self.__allSkillConditions = conditions
        self.__subscribedConditions = SubscribedConditions()
        self.__skillsWithRelations = getSkillWithRelations()
        self.__passiveSkillsIDList = []
        for sr in data['skills']:
            skillObj = getSkillByID(sr['key'])
            if not skillObj:
                LOG_ERROR('Ignore missing skill', sr['key'])
                continue
            skillValue = calcNormalSkillValue(sr['value'])
            if skillObj.activation:
                self.__activeSkills[skillObj.id] = SkillRecord(skillObj, skillValue, skillIndex=len(self.__activeSkills))
            else:
                self.__passiveSkills.append(SkillRecord(skillObj, skillValue))
                self.__passiveSkillsIDList.append(skillObj.id)

    def restore(self, data):
        if data is None:
            return
        else:
            self.__timers = data.copy()
            return

    def afterRestore(self):
        for skillID in self.__activeSkills.iterkeys():
            if self.isSkillActive(skillID):
                self.__activateSkill(skillID)
            else:
                self.__deactivateSkill(skillID)

    def backup(self):
        if self.__timers:
            return self.__timers.copy()
        else:
            return None

    def _getSkillIndex(self, skillID):
        if skillID not in self.__activeSkills:
            LOG_ERROR('CrewSkills error. Wrong skillID ' + skillID)
            return 0
        return self._crewIndex * CrewSkills.OFFSET + self.__activeSkills[skillID].index

    def setSkillStatus(self, skillID, status):
        self._owner.activeUniqueSkills[self._getSkillIndex(skillID)] = skillID if status else 0

    def isSkillActive(self, skillID):
        if skillID in self.__passiveSkillsIDList:
            return True
        else:
            skill = self.__activeSkills.get(skillID)
            if skill is not None:
                return self._owner.activeUniqueSkills[self._getSkillIndex(skillID)] != 0
            return False

    def subscribe(self, eventID, callback, skillID):
        if self.__allSkillConditions is None:
            return
        else:
            condition_f = self.__allSkillConditions.getCondition(eventID)
            if not condition_f:
                return

            def subscribeWorker():
                self.__allSkillConditions.updateSkillState(self.__timers.get(skillID, None))
                return condition_f()

            self.__subscribedConditions.addSubscription(subscribeWorker, callback)
            return

    def onActivationEvent(self, skillID):
        if self._owner.activeUniqueSkills[self._getSkillIndex(skillID)] == 0:
            LOG_DEBUG_DEV('onActivationEvent', skillID)
            self.__activateSkill(skillID)

    def onDeactivationEvent(self, skillID):
        if self._owner.activeUniqueSkills[self._getSkillIndex(skillID)]:
            LOG_DEBUG_DEV('onDeactivationEvent', skillID)
            self.__deactivateSkill(skillID)

    def update1sec(self):
        self.__subscribedConditions.update1sec()
        if self.__recalcRequired:
            self.__recalcRequired = False
            return True
        return False

    def initGame(self):
        for skill in self.__activeSkills.values():
            self.__deactivateSkill(skill.obj.id)

    def __activateSkill(self, skillID):
        LOG_DEBUG_DEV('activateSkill', skillID)
        oldValue = self._owner.activeUniqueSkills[self._getSkillIndex(skillID)]
        self.setSkillStatus(skillID, True)
        self.__timers[skillID] = BigWorld.time()
        skillObj = self.__activeSkills[skillID].obj
        disableEventID = skillObj.activation.disableEvent.eventID
        self.subscribe(disableEventID, partial(self.onDeactivationEvent, skillID), skillID)
        if oldValue == 0:
            for modifier in skillObj.mods:
                handler = ACTION_TABLE.get(modifier.type, None)
                if handler is None:
                    continue
                modifier.value_ = modifier.states[0]
                handler(self._owner, modifier, None)

        self._owner.publish(SKILL_ACTIVATED, skillID)
        self.__recalcRequired = True
        return

    def __deactivateSkill(self, skillID):
        LOG_DEBUG_DEV('deactivateSkill', skillID)
        oldValue = self._owner.activeUniqueSkills[self._getSkillIndex(skillID)]
        self.setSkillStatus(skillID, False)
        activeTime = 0
        if skillID in self.__timers:
            activeTime = BigWorld.time() - self.__timers[skillID]
            del self.__timers[skillID]
        skillObj = self.__activeSkills[skillID].obj
        disableEventID = skillObj.activation.enableEvent.eventID
        self.subscribe(disableEventID, partial(self.onActivationEvent, skillID), skillID)
        if oldValue != 0:
            self._owner.publish(SKILL_DEACTIVATED, skillID, activeTime)
        self.__recalcRequired = True

    def generateTimerEventID(self, skillID):
        return skillID * 100

    def changeState(self, state):
        self.state = state

    def skillValue(self, skillID):
        skill = self.__activeSkills.get(skillID)
        if skill is not None:
            return skill.value
        else:
            for skillObj in self.__passiveSkills:
                if skillObj.obj.id == skillID:
                    return skillObj.value

            return

    def applyObjMods(self, modifiers):

        def applySingleMod(isMainSkill, modType, skillValue, skillBonus, stateMod):
            if isMainSkill:
                modifiers.__dict__[ModsTypesToName[modType]] *= calcMainSingleMod(skillValue, skillBonus, stateMod)
            else:
                modifiers.__dict__[ModsTypesToName[modType]] *= calcNotMainSingleMod(skillValue, skillBonus, stateMod)

        def applyModWithRelations(isMainSkill, modType, skillValue, skillBonus, stateMod, modID):
            if not isinstance(modifiers.__dict__[ModsTypesToName[modType]], dict):
                modifiers.__dict__[ModsTypesToName[modType]] = {}
            if isMainSkill:
                modifiers.__dict__[ModsTypesToName[modType]][modID] = calcMainSingleMod(skillValue, skillBonus, stateMod)
            else:
                modifiers.__dict__[ModsTypesToName[modType]][modID] = calcNotMainSingleMod(skillValue, skillBonus, stateMod)

        def applyModifiers(skillObj, skillValue):
            for mod in skillObj.mods:
                stateMod = mod.states[self.state] / mod.states[OBJ_STATES.GOOD]
                skillBonus = mod.states[self.state] - 1
                if mod.type == self.__skillsWithRelations.get(skillObj.id, [-1])[0]:
                    applyModWithRelations(skillObj.id == mainSkill.id, mod.type, skillValue, skillBonus, stateMod, skillObj.id)
                else:
                    applySingleMod(skillObj.id == mainSkill.id, mod.type, skillValue, skillBonus, stateMod)

        mainSkill = getSpecializationSkillByID(self.specializationID)
        for skill in self.__passiveSkills:
            applyModifiers(skill.obj, skill.value)

        for skill in self.__activeSkills.itervalues():
            if self.isSkillActive(skill.obj.id):
                applyModifiers(skill.obj, skill.value)

    def destroy(self):
        for skillID in self.__timers.keys():
            self.__deactivateSkill(skillID)

        self._owner = None
        self.__activeSkills = None
        self.__passiveSkills = None
        self.__conditions = None
        return

    def reload(self):
        import _skills_data
        LOG_DEBUG_DEV('active skills are', self.__activeSkills, self.__passiveSkills)
        for skill in self.__activeSkills.values():
            newSkillObj = _skills_data.SkillDB[skill.obj.id]
            self.__activeSkills[skill.obj.id] = SkillRecord(newSkillObj, skill.value, skill.index)

        for i, skill in enumerate(self.__passiveSkills):
            newSkillObj = _skills_data.SkillDB[skill.obj.id]
            self.__passiveSkills[i] = SkillRecord(newSkillObj, skill.value)