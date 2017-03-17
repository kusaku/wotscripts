# Embedded file name: scripts/common/SkillsHelper.py
from consts import SKILL_1PRC_BASE_EXP, SKILL_PRC_TO_PUMP, SKILL_MIN_PRC, SKILL_INCREMENT_BASE, BARRACK_KEYS, EXP_KEY, DAMAGE_REASON, WORLD_SCALING, GLOBAL_EFFECTS, FROM_SERVER_TO_CLIENT_EFFECT_PARAM
from consts import INVALID_SPECIALIZATION_SKILL_PENALTY_FOR_PREMIUM, INVALID_ANOTHER_CLASS_SPECIALIZATION_SKILL_PENALTY, INVALID_SPECIALIZATION_SKILL_PENALTY
import _skills_data
import math
BASE_SKILL_EXP = 100000
MAX_SKILL_SP = 15
EVENT_SHOW_MIN_LEVEL = 1.0
SP_COUNT_FROM_EXP = [0,
 20000,
 34000,
 56000,
 95000,
 159000,
 268000,
 450000,
 755000,
 1269000,
 2132000,
 3582000,
 6120000,
 10560000,
 14320000]
BASE_OLD_SKILL_EXP = 200000
validDeadReasonsForExplosiveCharacter = [DAMAGE_REASON.TERRAIN,
 DAMAGE_REASON.WATER,
 DAMAGE_REASON.TREES,
 DAMAGE_REASON.OBSTACLE]

def _getExplosiveCharacterData(maxHp):
    if maxHp <= 500:
        return (35, 75)
    if maxHp < 1500:
        return (35, 100)
    return (35, 125)


def trySpawnAfterDeathExplosion(owner, isDead, deadReason, author, explosionDamage):
    if isDead and deadReason in validDeadReasonsForExplosiveCharacter:
        explosionRadiusEffective, explosionRadius = _getExplosiveCharacterData(explosionDamage)
        from Weapons import Weapons
        Weapons.doExplosiveDamage(owner, owner.position, explosionRadius * WORLD_SCALING, explosionRadiusEffective * WORLD_SCALING, 2 * explosionDamage, DAMAGE_REASON.BOMB_EXPLOSION)
        owner.allClients.createWorldEffect(GLOBAL_EFFECTS.EXPLOSIVE_CHARACTER, FROM_SERVER_TO_CLIENT_EFFECT_PARAM.GROUNDED)


_FRONT_ATTACK_ANGLE = math.radians(15)

def isFrontAttack(ownerDir, targetDir):
    return ownerDir.angle(-targetDir) < _FRONT_ATTACK_ANGLE


def skillsHasModifier(crewSkills, modifier):
    for data in crewSkills:
        for sr in data['skills']:
            skill = getSkillByID(sr['key'])
            for mod in skill.mods:
                if mod.type == modifier:
                    return True

    return False


def calculateSkillPenalty(planeFrom, planeTo):
    import db.DBLogic
    if planeFrom != planeTo:
        curPlaneSettings = db.DBLogic.g_instance.getAircraftData(planeFrom)
        newPlaneSettings = db.DBLogic.g_instance.getAircraftData(planeTo)
        isPremium = db.DBLogic.g_instance.isPlanePremium(planeTo)
        if curPlaneSettings.airplane.planeType != newPlaneSettings.airplane.planeType:
            if isPremium:
                return INVALID_SPECIALIZATION_SKILL_PENALTY_FOR_PREMIUM
            else:
                return INVALID_ANOTHER_CLASS_SPECIALIZATION_SKILL_PENALTY
        elif not isPremium:
            return INVALID_SPECIALIZATION_SKILL_PENALTY
    return 0


def calculateEffectiveMainSkill(mainSkillValue, planeFrom, planeTo):
    import db.DBLogic
    if planeFrom == planeTo or planeTo == -1:
        return mainSkillValue
    isPremium = db.DBLogic.g_instance.isPlanePremium(planeTo)
    if isPremium:
        return 100
    curPlaneSettings = db.DBLogic.g_instance.getAircraftData(planeFrom)
    newPlaneSettings = db.DBLogic.g_instance.getAircraftData(planeTo)
    sameClassSkillValue = 100 - INVALID_SPECIALIZATION_SKILL_PENALTY
    minSkillValue = 50
    if curPlaneSettings.airplane.planeType == newPlaneSettings.airplane.planeType:
        if mainSkillValue > sameClassSkillValue:
            return sameClassSkillValue
        else:
            return mainSkillValue
    else:
        return minSkillValue


def calculateCommonAndImprovedSkillValue(mainSkillValue):
    if mainSkillValue == 100:
        return 100
    if mainSkillValue < 75:
        return 50
    return 75


def getCrewSP(member):
    if not member[BARRACK_KEYS.SP_AVAILABLE]:
        return 0
    aboveMainExp = member[BARRACK_KEYS.EXPERIENCE][EXP_KEY.ABOVE_MAIN]
    for n, exp in enumerate(SP_COUNT_FROM_EXP):
        aboveMainExp -= exp
        if aboveMainExp < 0:
            break

    if aboveMainExp < 0:
        return n
    return MAX_SKILL_SP


def getExpForMainSkill(skillValue = 50):
    return int(round(BASE_SKILL_EXP * skillValue / 100))


def getMainSpecializationLevel(mainExp):
    return max(50, 100 * mainExp / BASE_SKILL_EXP)


def getLeftExpForSP(aboveMainExp):
    for exp in SP_COUNT_FROM_EXP:
        aboveMainExp -= exp
        if aboveMainExp < 0:
            return -aboveMainExp

    return 0


def getFullExpCurrentSP(member):
    currentSP = getCrewSP(member)
    if currentSP < MAX_SKILL_SP:
        return SP_COUNT_FROM_EXP[currentSP]
    return 0


def getMaxExp():
    return sum(SP_COUNT_FROM_EXP)


def getFreeSP(member):
    if not member[BARRACK_KEYS.SP_AVAILABLE]:
        return 0
    else:
        spSpent = sum((_skills_data.SkillDB[skillID].cost for skillID in member[BARRACK_KEYS.SKILLS]))
        return getCrewSP(member) - spSpent


def skillHelperExpBaseConvertion(exp):
    return int(exp * BASE_SKILL_EXP / BASE_OLD_SKILL_EXP)


def skillHelperExpConvertion(oldExp, oldSkill, aboveExpLimit):

    def getOldExpForMainSkill(skillValue = 50):
        return int(round(BASE_OLD_SKILL_EXP * skillValue / 100))

    mainExp = getOldExpForMainSkill(oldSkill[0][1])
    oldExp -= min(oldExp, mainExp - BASE_OLD_SKILL_EXP / 2)
    extraExp = min(oldExp, aboveExpLimit)
    return [int(round(mainExp)), int(round(extraExp))]


def skillHelperSkillsConvertion(skills):
    return [skills[0][0]]


def skillHelperIsSPAvailable(exp, oldSkillCount):
    return exp[EXP_KEY.MAIN] == BASE_OLD_SKILL_EXP or exp[EXP_KEY.ABOVE_MAIN] > 0 or oldSkillCount > 1


def getSkillsCountForExp(exp):
    n = 0
    while exp >= 0:
        exp -= getExpForSkillN(n)
        n += 1

    return n - 1


def getSkillNPrcForExpAdding(n, exp):
    return exp / (SKILL_1PRC_BASE_EXP * SKILL_INCREMENT_BASE ** n * 1.0)


def getSkillNPrcForExp(n, exp):
    return SKILL_MIN_PRC + min(getSkillNPrcForExpAdding(n, exp), SKILL_PRC_TO_PUMP * 1.0)


def getExpForSkillN(n, skillLevel = 100):
    return int(SKILL_1PRC_BASE_EXP * (skillLevel - SKILL_MIN_PRC) * SKILL_INCREMENT_BASE ** n + 0.5)


def getExpForNSkills(n, withoutMain = False):
    return SKILL_1PRC_BASE_EXP * SKILL_PRC_TO_PUMP * sum((SKILL_INCREMENT_BASE ** i for i in xrange(1 if withoutMain else 0, n + 1)))


def getExpForNSkillsWithoutMain(n, lastSkillLevel = 100):
    if n == 0:
        return 0
    return int(SKILL_1PRC_BASE_EXP * (lastSkillLevel - SKILL_MIN_PRC) * SKILL_INCREMENT_BASE ** n + 0.5) + getExpForNSkills(n - 1, True)


def getSkillsExp(member):
    """it's correct to use this function on server side only!!!"""
    return member[BARRACK_KEYS.EXPERIENCE] - getExpForSkillN(0, member[BARRACK_KEYS.SKILLS][0][1])


def getSkillByID(skillID):
    return _skills_data.SkillDB.get(skillID, None)


def getSkillIDByName(skillName):
    for skill in _skills_data.Skills.skill:
        if skill.localizeTag == skillName:
            return skill.id

    return None


def getSpecializationSkillByID(skillID):
    return _skills_data.SpecializationSkillDB.get(skillID, None)


def getSkillWithRelations():
    return _skills_data.SkillWithRelationsDB.copy()


def getTargetSkillIDList(targetModsList):
    res = []
    for skillID, skill in _skills_data.SkillDB.iteritems():
        for mod in skill.mods:
            if mod.type in targetModsList:
                res.append(skillID)
                break

    return res


def calcNotMainSingleMod(skillValue, skillBonus, stateMod):
    return (1 + (0.5 + 0.5 * skillValue) * skillBonus) * stateMod


def calcMainSingleMod(skillValue, skillBonus, stateMod):
    return (1 + (1 - skillValue) * skillBonus) * stateMod


def calcNormalSkillValue(value):
    freeLevel = 50
    return (value - freeLevel) / (100.0 - freeLevel)