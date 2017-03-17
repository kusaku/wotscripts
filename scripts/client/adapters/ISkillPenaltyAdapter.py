# Embedded file name: scripts/client/adapters/ISkillPenaltyAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.cache import getFromCache
import db.DBLogic
from _specializations_data import SpecializationEnum
from SkillsHelper import getMainSpecializationLevel, calculateSkillPenalty, MAX_SKILL_SP, calculateEffectiveMainSkill
from _skills_data import SkillDB, SKILL_GROUP
from debug_utils import LOG_ERROR
from consts import INVALID_SPECIALIZATION_SKILL_PENALTY

class ISkillPenaltyAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        member = getFromCache([kw['idTypeList'][0]], 'ICrewMember')
        if member is None:
            LOG_ERROR('Try call ISkillPenalty for non-cached crew', [kw['idTypeList'][0]])
            return {'penaltyPrc': 100,
             'descriptions': [],
             'skills': [],
             'mainSpecLevel': 50,
             'mainSkillLock': False,
             'SPLock': False}
        else:
            planeTo = kw['idTypeList'][1][0]
            mainSpecLevel = getMainSpecializationLevel(member['mainExp'])
            specialization = SkillDB[member['specialization']].mainForSpecialization
            isGunner = specialization == SpecializationEnum.GUNNER
            planeSpecializedOn = member['planeSpecializedOn']
            mainSkillLock = self.__getMainSkillLock(member, planeTo)
            descriptions = []
            skills = member['skills'][:]
            if planeTo == -1:
                SPLock = self.__getSPLockInBarrack(member)
                descriptions.append(('LOBBY_GUNNER_DOES_NOT_GAIN_EXP', 'red', 'common') if isGunner else ('LOBBY_PILOT_DOES_NOT_GAIN_EXP', 'red', 'common'))
                return {'penaltyPrc': 0,
                 'descriptions': descriptions,
                 'skills': skills,
                 'mainSpecLevel': mainSpecLevel,
                 'mainSkillLock': mainSkillLock,
                 'SPLock': SPLock}
            curPlaneSettings = db.DBLogic.g_instance.getAircraftData(planeSpecializedOn)
            newPlaneSettings = db.DBLogic.g_instance.getAircraftData(planeTo)
            isPremium = db.DBLogic.g_instance.isPlanePremium(planeTo)
            sameType = curPlaneSettings.airplane.planeType == newPlaneSettings.airplane.planeType
            samePlane = planeSpecializedOn == planeTo
            specSkillPenalty = samePlane and member['expLeftToMain'] > 0 or not samePlane and not isPremium
            descriptions.extend(self.__getBonusDescription(member, isPremium, samePlane, isGunner))
            descriptions.extend(self.__getWarningDescription(member, isPremium, samePlane, sameType, specSkillPenalty))
            descriptions.extend(self.__getCriticalDescription(member, isPremium, samePlane, sameType, specSkillPenalty, isGunner))
            if specSkillPenalty and not isGunner and self.__hasUniqueSkill(member['skills']):
                skills = [ id for id in skills if SkillDB[id].group != SKILL_GROUP.UNIQUE ]
            descriptions = [ dict(text=t, color=c, tooltip=h == 'tooltip') for t, c, h in descriptions ]
            penalty = calculateSkillPenalty(planeSpecializedOn, planeTo)
            SPLock = self.__getSPLockInPlane(member, isPremium, samePlane)
            ret = {'penaltyPrc': penalty,
             'descriptions': descriptions,
             'mainSpecLevel': calculateEffectiveMainSkill(mainSpecLevel, planeSpecializedOn, planeTo),
             'skills': skills,
             'mainSkillLock': mainSkillLock,
             'SPLock': SPLock}
            return ret

    def __hasUniqueSkill(self, skills):
        return any((SkillDB[skillID].group == SKILL_GROUP.UNIQUE for skillID in skills))

    def __hasCommonSkill(self, skills):
        return any((SkillDB[skillID].group in [SKILL_GROUP.COMMON, SKILL_GROUP.IMPROVED] for skillID in skills))

    def __getSPLockInBarrack(self, member):
        if member['expLeftToMain'] == 0 and member['SP'] < MAX_SKILL_SP:
            return False
        return True

    def __getSPLockInPlane(self, member, isPremium, samePlane):
        if member['expLeftToMain'] == 0 and samePlane and member['SP'] < MAX_SKILL_SP:
            return False
        if not samePlane and isPremium and member['SP'] > 0 and member['SP'] < MAX_SKILL_SP:
            return False
        return True

    def __getMainSkillLock(self, member, planeTo):
        if member['planeSpecializedOn'] != planeTo:
            return True
        return False

    def __getBonusDescription(self, member, isPremium, samePlane, isGunner):
        descriptions = []
        if isPremium:
            if member['SP'] > 0 and member['SP'] < MAX_SKILL_SP or member['expLeftToMain'] > 0 and samePlane:
                descriptions.append(('LOBBY_CREW_BONUS_EXP', 'green', 'common'))
            if not samePlane:
                if isGunner:
                    descriptions.append(('LOBBY_GUNNER_EFFECTIVE_TURRET_INCREASED_100', 'green', 'tooltip'))
                else:
                    descriptions.append(('LOBBY_PILOT_EFFECTIVE_STATS_INCREASED_100', 'green', 'tooltip'))
        return descriptions

    def __getWarningDescription(self, member, isPremium, samePlane, sameType, specSkillPenalty):
        descriptions = []
        if not samePlane:
            descriptions.append(('LOBBY_CREW_ANOTHER_PLANE_FROZEN_EXP', 'yellow', 'common'))
        elif member['expLeftToMain'] > 0 and member['experience'] > 0:
            descriptions.append(('LOBBY_CREW_PROGRESS_OBTAIN_SKILL_POINT_SUSPENDED', 'yellow', 'common'))
        if specSkillPenalty:
            if self.__hasCommonSkill(member['skills']):
                sameClassSkillValue = 100 - INVALID_SPECIALIZATION_SKILL_PENALTY
                if sameType and member['skillValue'] >= sameClassSkillValue:
                    descriptions.append(('LOBBY_CREW_EFFECTIVE_STANDART_SKILLS_REDUCED_25', 'yellow', 'tooltip'))
                else:
                    descriptions.append(('LOBBY_CREW_EFFECTIVE_STANDART_SKILLS_REDUCED_50', 'yellow', 'tooltip'))
        return descriptions

    def __getCriticalDescription(self, member, isPremium, samePlane, sameType, specSkillPenalty, isGunner):
        descriptions = []
        if specSkillPenalty and not isGunner and self.__hasUniqueSkill(member['skills']):
            descriptions.append(('LOBBY_PILOT_SPETIALS_SKILLS_DOESNT_WORK', 'red', 'tooltip'))
        if not samePlane and not isPremium:
            if member['SP'] > 0 and member['SP'] < MAX_SKILL_SP:
                descriptions.append(('LOBBY_CREW_PROGRESS_SKILLPOINT_FROZEN', 'red', 'common'))
            sameClassSkillValue = 100 - INVALID_SPECIALIZATION_SKILL_PENALTY
            if sameType and member['skillValue'] >= sameClassSkillValue:
                if isGunner:
                    descriptions.append(('LOBBY_GUNNER_EFFECTIVE_TURRET_REDUCED_25', 'red', 'tooltip'))
                else:
                    descriptions.append(('LOBBY_PILOT_EFFECTIVE_STATS_REDUCED_25', 'red', 'tooltip'))
            elif isGunner:
                descriptions.append(('LOBBY_GUNNER_EFFECTIVE_TURRET_REDUCED_50', 'red', 'tooltip'))
            else:
                descriptions.append(('LOBBY_PILOT_EFFECTIVE_STATS_REDUCED_50', 'red', 'tooltip'))
        return descriptions