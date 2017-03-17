# Embedded file name: scripts/common/CrewHelpers.py
from _specializations_data import SpecializationEnum
import db
from _airplanesConfigurations_db import airplanesDefaultConfigurations, getAirplaneConfiguration
from consts import BARRACK_KEYS, CREW_BODY_TYPE, EXP_KEY, DAMAGED_CREW_MEMBER_EXP_PENALTY_K, MESSAGE_TYPE, PLANE_KEYS
from SkillsHelper import getCrewSP, BASE_SKILL_EXP, SP_COUNT_FROM_EXP
from _crewnations_data import CrewUniqueDB
from _skills_data import SpecializationSkillDB, SkillDB
import time
CREW_NAME_TO_CREW_SPECIALIZATION = {'PILOT': SpecializationEnum.PILOT,
 'GUNNER1': SpecializationEnum.GUNNER,
 'NAVIGATOR': SpecializationEnum.NAVIGATOR}
DEFAULT_CREW_SUBSPECIALIZATION = 0
DEFAULT_CREW_BODY_TYPE = CREW_BODY_TYPE.MALE
DEFAULT_BOT_AVATAR_BODY_TYPE = [{0: [DEFAULT_CREW_BODY_TYPE, 1]}]
MIN_RANK_FOR_PILOT = 9
MAX_RANK_FOR_GUNNER = 2
MAX_RANK_FOR_PILOT = 1
GUNNER_RANK_OFFSET = 1

def isCrewPart(partNameStr):
    return partNameStr.upper() in CREW_NAME_TO_CREW_SPECIALIZATION


def getDefaultRank(specialization, skillValue):
    rank = MIN_RANK_FOR_PILOT - (1 if skillValue == 100 else 0)
    if specialization == SpecializationEnum.GUNNER:
        rank += GUNNER_RANK_OFFSET
    return rank


def getRank(member):
    return getRankFromSP(getCrewSP(member), member[BARRACK_KEYS.SPECIALIZATION])


def getRankFromSP(sp, specialization):
    rank = MIN_RANK_FOR_PILOT
    rank -= 1 + int((sp - 1) / 2)
    if specialization == SpecializationEnum.GUNNER:
        rank = max(MAX_RANK_FOR_GUNNER, rank + GUNNER_RANK_OFFSET)
    return rank


def getNextRank(currentRank, specialization):
    maxRank = MAX_RANK_FOR_GUNNER if SpecializationEnum.GUNNER else MAX_RANK_FOR_PILOT
    return max(maxRank, currentRank - 1)


def updateRank(member):
    newRank = getRank(member)
    if newRank < member[BARRACK_KEYS.RANKS]:
        member[BARRACK_KEYS.RANKS] = newRank
        return True
    return False


def calculateCrewExperience(crewList, baseXP, totalXP, isCrewPumping):
    crewExpList = {}
    minExpMemberIndex = -1
    if isCrewPumping:
        expList = [ sum(m[BARRACK_KEYS.EXPERIENCE]) for m in crewList ]
        minExpMemberIndex = expList.index(min(expList))
    for i, member in enumerate(crewList):
        memberID = member[BARRACK_KEYS.MEMBER_ID]
        pumpXP = baseXP if minExpMemberIndex == i else 0
        crewExpList[memberID] = [totalXP, pumpXP]

    return crewExpList


def addCrewExperience(member, exp):
    mainExp = member[BARRACK_KEYS.EXPERIENCE][EXP_KEY.MAIN]
    isAnotherPlane, isPremiumPlane = planeFlags(member)
    memberSpAvailable = member[BARRACK_KEYS.SP_AVAILABLE]
    addedToMain, addedToAboveMain, spChanged = 0, 0, False
    if not filterCanAddExp(isAnotherPlane, isPremiumPlane, exp):
        return (addedToMain, addedToAboveMain, spChanged)
    if filterMemberExp(isAnotherPlane, isPremiumPlane, mainExp, memberSpAvailable):
        addedToMain = addToMain(member, exp)
    if member[BARRACK_KEYS.SP_AVAILABLE]:
        addedToAboveMain = addAboveMain(member, exp - addedToMain)
    spChanged = member[BARRACK_KEYS.SP_AVAILABLE] != memberSpAvailable
    return (addedToMain, addedToAboveMain, spChanged)


def addCrewExperienceWithoutFilters(member, exp):
    added = addToMain(member, exp)
    above = 0
    if member[BARRACK_KEYS.SP_AVAILABLE]:
        above = addAboveMain(member, exp - added)
    return (added, above)


def addToMain(member, exp):
    memberExp = member[BARRACK_KEYS.EXPERIENCE]
    mainExp = memberExp[EXP_KEY.MAIN]
    addExp = min(exp, BASE_SKILL_EXP - mainExp)
    memberExp[EXP_KEY.MAIN] += addExp
    if memberExp[EXP_KEY.MAIN] >= BASE_SKILL_EXP:
        member[BARRACK_KEYS.SP_AVAILABLE] = True
    return addExp


def addAboveMain(member, exp):
    memberExp = member[BARRACK_KEYS.EXPERIENCE]
    aboveMain = memberExp[EXP_KEY.ABOVE_MAIN]
    addExp = min(exp, sum(SP_COUNT_FROM_EXP) - aboveMain)
    memberExp[EXP_KEY.ABOVE_MAIN] += addExp
    updateRank(member)
    return addExp


def planeFlags(member):
    planeID = member[BARRACK_KEYS.CURRENT_PLANE]
    isAnotherPlane = planeID != member[BARRACK_KEYS.PLANE_SPECIALIZED_ON]
    isPremiumPlane = db.DBLogic.g_instance.isPlanePremium(planeID)
    return (isAnotherPlane, isPremiumPlane)


def filterCanAddExp(isAnotherPlane, isPremiumPlane, exp):
    skipMainExp = isAnotherPlane and isPremiumPlane
    if not (exp < 0 or isAnotherPlane and not skipMainExp):
        return True


def filterMemberExp(isAnotherPlane, isPremiumPlane, mainExp, memberSpAvailable):
    skipMainExp = isAnotherPlane and isPremiumPlane
    if not skipMainExp and (mainExp < BASE_SKILL_EXP or not memberSpAvailable):
        return True


def sendSystemMessageOnCrewUpdateSP(account, member, oldSP):
    """Send system message of gain fist/new Skill point."""
    newSP = getCrewSP(member)
    memberID = member[BARRACK_KEYS.MEMBER_ID]
    planeID = member[BARRACK_KEYS.CURRENT_PLANE]

    def sendSystemMessage(msgType):
        import wgPickle
        account.sendSystemMessage(time.time(), '', wgPickle.dumps(wgPickle.FromServerToServer, {'memberID': memberID,
         'planeID': planeID,
         'specializationID': member[BARRACK_KEYS.SPECIALIZATION]}), msgType)

    if oldSP == 0 and newSP == 1:
        sendSystemMessage(MESSAGE_TYPE.GOT_FIRST_SP)
    elif oldSP < newSP:
        sendSystemMessage(MESSAGE_TYPE.GOT_NEW_SP)


def getPilotBodyType(crewBodyType):
    if crewBodyType is None:
        return DEFAULT_CREW_BODY_TYPE
    else:
        for crewBody in crewBodyType:
            for spec, (bodyType, iconIndex) in crewBody.iteritems():
                if spec == SpecializationEnum.PILOT:
                    return bodyType

        return DEFAULT_CREW_BODY_TYPE


def validateCrew(account):
    inventory = account.pdata['inventory']
    barrack = inventory['barrack']
    planeCrew = {}
    for planeData in inventory['planes']:
        planeCrew[planeData[PLANE_KEYS.PLANE]] = planeData[PLANE_KEYS.CREW]

    for m in barrack.itervalues():
        planeID = m[BARRACK_KEYS.CURRENT_PLANE]
        if planeID != -1:
            if planeID not in planeCrew:
                m[BARRACK_KEYS.CURRENT_PLANE] = -1
            else:
                founded = False
                for spec, memberID in planeCrew[planeID]:
                    if memberID == m[BARRACK_KEYS.MEMBER_ID]:
                        if m[BARRACK_KEYS.SPECIALIZATION] != spec:
                            m[BARRACK_KEYS.CURRENT_PLANE] = -1
                        else:
                            founded = True

                if not founded:
                    m[BARRACK_KEYS.CURRENT_PLANE] = -1

    for aircraftData in inventory['planes']:
        for i, data in enumerate(aircraftData[PLANE_KEYS.CREW]):
            spec, memberID = data
            planeID = aircraftData[PLANE_KEYS.PLANE]
            if memberID != -1 and (memberID not in barrack or barrack[memberID][BARRACK_KEYS.CURRENT_PLANE] != planeID):
                aircraftData[PLANE_KEYS.CREW][i] = [spec, -1]

    usedSlot = len([ 1 for m in barrack.itervalues() if m[BARRACK_KEYS.CURRENT_PLANE] == -1 ])
    inventory['barrackSlotsFree'] = inventory['barrackSlotsTotal'] - usedSlot


def applyUniqueCrewData(crewData, uniqueID):
    uniqueData = CrewUniqueDB[uniqueID]
    skills = [SpecializationSkillDB[uniqueData.specialization].id]
    isLocked = lambda skID: (SkillDB[skID].locked if hasattr(SkillDB[skID], 'locked') else False)
    lockedSkills = [ skillID for skillID in SkillDB.keys() if isLocked(skillID) and uniqueData.subSpecialization in SkillDB[skillID].crewMemberSubTypes ]
    skills.extend(lockedSkills)
    crewData[BARRACK_KEYS.MEMBER_ID] = uniqueID
    crewData[BARRACK_KEYS.BODY_TYPE] = CREW_BODY_TYPE.UNIQUE
    crewData[BARRACK_KEYS.FIRST_NAME] = uniqueData.firstName
    crewData[BARRACK_KEYS.LAST_NAME] = uniqueData.lastName
    crewData[BARRACK_KEYS.PICTURE_INDEX] = uniqueData.iconIndex
    crewData[BARRACK_KEYS.PLANE_SPECIALIZED_ON] = uniqueData.planeID
    crewData[BARRACK_KEYS.SPECIALIZATION] = uniqueData.specialization
    crewData[BARRACK_KEYS.SUB_SPECIALIZATION] = uniqueData.subSpecialization
    crewData[BARRACK_KEYS.EXPERIENCE] = [uniqueData.mainExp, uniqueData.aboveMainExp]
    crewData[BARRACK_KEYS.RANKS] = uniqueData.rank
    crewData[BARRACK_KEYS.SKILLS] = skills
    if uniqueData.mainExp >= BASE_SKILL_EXP or uniqueData.aboveMainExp > 0:
        crewData[BARRACK_KEYS.SP_AVAILABLE] = True


def getCrewSpecializationByName(name):
    return CREW_NAME_TO_CREW_SPECIALIZATION.get(name.upper(), None)


def getCrewSpecialization(partsSettings, partTypes):

    def listGenerator():
        partsList = partsSettings.getPartsList()
        for partTuple in partsList:
            partType = None
            partID = partTuple[0]
            partDB = partTuple[1]
            for it in partTypes:
                if it['key'] == partID:
                    partType = partDB.getPartType(it['value'])
                    break

            if not partType:
                partType = partDB.getFirstPartType()
            if partType:
                partName = partType.componentType
                specialization = getCrewSpecializationByName(partName)
                if specialization is not None:
                    yield specialization

        return

    return list(listGenerator())


def previewCrewSpecList(aircraftID):
    settings = db.DBLogic.g_instance.getAircraftData(aircraftID)
    globalID = airplanesDefaultConfigurations[aircraftID]
    config = getAirplaneConfiguration(globalID)
    return getCrewSpecialization(settings.airplane.partsSettings, config.partTypes)


def getSpecializationName(id):
    return dict(((v, k) for k, v in SpecializationEnum.__dict__.iteritems())).get(id, '')


def getCrewSkillsID(crewSkills):
    res = []
    if crewSkills is not None:
        for obj in crewSkills:
            for skill in obj['skills']:
                res.append(skill['key'])

    return res