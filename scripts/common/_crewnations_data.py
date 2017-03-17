# Embedded file name: scripts/common/_crewnations_data.py
import Math
import math
import consts
true = True
false = False

class Dummy:
    pass


isServerDatabase = True

class AMMO_TYPE:
    BALL = 0
    AP = 1
    APC = 2
    I = 3
    APHC = 4
    API = 5
    HEI = 6
    APHE = 7
    ALL_TYPES = (BALL,
     AP,
     APC,
     I,
     APHC,
     API,
     HEI,
     APHE)


class SpecializationEnum:
    PILOT = 0
    GUNNER = 1
    NAVIGATOR = 2
    ALL_TYPES = (PILOT, GUNNER, NAVIGATOR)


CrewNations = Dummy()
CrewNations.crewnation = []
CrewNations.crewnation.insert(0, None)
CrewNations.crewnation[0] = Dummy()
CrewNations.crewnation[0].bodyType = []
CrewNations.crewnation[0].bodyType.insert(0, None)
CrewNations.crewnation[0].bodyType[0] = Dummy()
CrewNations.crewnation[0].bodyType[0].bodyType = 'male'
CrewNations.crewnation[0].bodyType[0].firstNamesCount = 489
CrewNations.crewnation[0].bodyType[0].iconsCount = 10
CrewNations.crewnation[0].bodyType[0].lastNamesCount = 1756
CrewNations.crewnation[0].bodyType.insert(1, None)
CrewNations.crewnation[0].bodyType[1] = Dummy()
CrewNations.crewnation[0].bodyType[1].bodyType = 'female'
CrewNations.crewnation[0].bodyType[1].firstNamesCount = 0
CrewNations.crewnation[0].bodyType[1].iconsCount = 0
CrewNations.crewnation[0].bodyType[1].lastNamesCount = 0
CrewNations.crewnation[0].nation = 'GB'.lower()
CrewNations.crewnation.insert(1, None)
CrewNations.crewnation[1] = Dummy()
CrewNations.crewnation[1].bodyType = []
CrewNations.crewnation[1].bodyType.insert(0, None)
CrewNations.crewnation[1].bodyType[0] = Dummy()
CrewNations.crewnation[1].bodyType[0].bodyType = 'male'
CrewNations.crewnation[1].bodyType[0].firstNamesCount = 270
CrewNations.crewnation[1].bodyType[0].iconsCount = 10
CrewNations.crewnation[1].bodyType[0].lastNamesCount = 989
CrewNations.crewnation[1].bodyType.insert(1, None)
CrewNations.crewnation[1].bodyType[1] = Dummy()
CrewNations.crewnation[1].bodyType[1].bodyType = 'female'
CrewNations.crewnation[1].bodyType[1].firstNamesCount = 0
CrewNations.crewnation[1].bodyType[1].iconsCount = 0
CrewNations.crewnation[1].bodyType[1].lastNamesCount = 0
CrewNations.crewnation[1].bodyType.insert(2, None)
CrewNations.crewnation[1].bodyType[2] = Dummy()
CrewNations.crewnation[1].bodyType[2].bodyType = 'unique'
CrewNations.crewnation[1].bodyType[2].firstNamesCount = 1
CrewNations.crewnation[1].bodyType[2].iconsCount = 1
CrewNations.crewnation[1].bodyType[2].lastNamesCount = 1
CrewNations.crewnation[1].nation = 'Germany'.lower()
CrewNations.crewnation.insert(2, None)
CrewNations.crewnation[2] = Dummy()
CrewNations.crewnation[2].bodyType = []
CrewNations.crewnation[2].bodyType.insert(0, None)
CrewNations.crewnation[2].bodyType[0] = Dummy()
CrewNations.crewnation[2].bodyType[0].bodyType = 'male'
CrewNations.crewnation[2].bodyType[0].firstNamesCount = 231
CrewNations.crewnation[2].bodyType[0].iconsCount = 10
CrewNations.crewnation[2].bodyType[0].lastNamesCount = 231
CrewNations.crewnation[2].bodyType.insert(1, None)
CrewNations.crewnation[2].bodyType[1] = Dummy()
CrewNations.crewnation[2].bodyType[1].bodyType = 'female'
CrewNations.crewnation[2].bodyType[1].firstNamesCount = 0
CrewNations.crewnation[2].bodyType[1].iconsCount = 0
CrewNations.crewnation[2].bodyType[1].lastNamesCount = 0
CrewNations.crewnation[2].nation = 'Japan'.lower()
CrewNations.crewnation.insert(3, None)
CrewNations.crewnation[3] = Dummy()
CrewNations.crewnation[3].bodyType = []
CrewNations.crewnation[3].bodyType.insert(0, None)
CrewNations.crewnation[3].bodyType[0] = Dummy()
CrewNations.crewnation[3].bodyType[0].bodyType = 'male'
CrewNations.crewnation[3].bodyType[0].firstNamesCount = 481
CrewNations.crewnation[3].bodyType[0].iconsCount = 10
CrewNations.crewnation[3].bodyType[0].lastNamesCount = 1770
CrewNations.crewnation[3].bodyType.insert(1, None)
CrewNations.crewnation[3].bodyType[1] = Dummy()
CrewNations.crewnation[3].bodyType[1].bodyType = 'female'
CrewNations.crewnation[3].bodyType[1].firstNamesCount = 0
CrewNations.crewnation[3].bodyType[1].iconsCount = 0
CrewNations.crewnation[3].bodyType[1].lastNamesCount = 0
CrewNations.crewnation[3].bodyType.insert(2, None)
CrewNations.crewnation[3].bodyType[2] = Dummy()
CrewNations.crewnation[3].bodyType[2].bodyType = 'unique'
CrewNations.crewnation[3].bodyType[2].firstNamesCount = 1
CrewNations.crewnation[3].bodyType[2].iconsCount = 1
CrewNations.crewnation[3].bodyType[2].lastNamesCount = 1
CrewNations.crewnation[3].nation = 'USA'.lower()
CrewNations.crewnation.insert(4, None)
CrewNations.crewnation[4] = Dummy()
CrewNations.crewnation[4].bodyType = []
CrewNations.crewnation[4].bodyType.insert(0, None)
CrewNations.crewnation[4].bodyType[0] = Dummy()
CrewNations.crewnation[4].bodyType[0].bodyType = 'male'
CrewNations.crewnation[4].bodyType[0].firstNamesCount = 108
CrewNations.crewnation[4].bodyType[0].iconsCount = 10
CrewNations.crewnation[4].bodyType[0].lastNamesCount = 1073
CrewNations.crewnation[4].bodyType.insert(1, None)
CrewNations.crewnation[4].bodyType[1] = Dummy()
CrewNations.crewnation[4].bodyType[1].bodyType = 'female'
CrewNations.crewnation[4].bodyType[1].firstNamesCount = 0
CrewNations.crewnation[4].bodyType[1].iconsCount = 0
CrewNations.crewnation[4].bodyType[1].lastNamesCount = 0
CrewNations.crewnation[4].bodyType.insert(2, None)
CrewNations.crewnation[4].bodyType[2] = Dummy()
CrewNations.crewnation[4].bodyType[2].bodyType = 'unique'
CrewNations.crewnation[4].bodyType[2].firstNamesCount = 1
CrewNations.crewnation[4].bodyType[2].iconsCount = 1
CrewNations.crewnation[4].bodyType[2].lastNamesCount = 1
CrewNations.crewnation[4].nation = 'USSR'.lower()
CrewNations.crewnation.insert(5, None)
CrewNations.crewnation[5] = Dummy()
CrewNations.crewnation[5].bodyType = []
CrewNations.crewnation[5].bodyType.insert(0, None)
CrewNations.crewnation[5].bodyType[0] = Dummy()
CrewNations.crewnation[5].bodyType[0].bodyType = 'male'
CrewNations.crewnation[5].bodyType[0].firstNamesCount = 47
CrewNations.crewnation[5].bodyType[0].iconsCount = 10
CrewNations.crewnation[5].bodyType[0].lastNamesCount = 69
CrewNations.crewnation[5].bodyType.insert(1, None)
CrewNations.crewnation[5].bodyType[1] = Dummy()
CrewNations.crewnation[5].bodyType[1].bodyType = 'female'
CrewNations.crewnation[5].bodyType[1].firstNamesCount = 0
CrewNations.crewnation[5].bodyType[1].iconsCount = 0
CrewNations.crewnation[5].bodyType[1].lastNamesCount = 0
CrewNations.crewnation[5].nation = 'China'.lower()
CrewNations.crewnation.insert(6, None)
CrewNations.crewnation[6] = Dummy()
CrewNations.crewnation[6].bodyType = []
CrewNations.crewnation[6].bodyType.insert(0, None)
CrewNations.crewnation[6].bodyType[0] = Dummy()
CrewNations.crewnation[6].bodyType[0].bodyType = 'male'
CrewNations.crewnation[6].bodyType[0].firstNamesCount = 423
CrewNations.crewnation[6].bodyType[0].iconsCount = 5
CrewNations.crewnation[6].bodyType[0].lastNamesCount = 1077
CrewNations.crewnation[6].bodyType.insert(1, None)
CrewNations.crewnation[6].bodyType[1] = Dummy()
CrewNations.crewnation[6].bodyType[1].bodyType = 'female'
CrewNations.crewnation[6].bodyType[1].firstNamesCount = 0
CrewNations.crewnation[6].bodyType[1].iconsCount = 0
CrewNations.crewnation[6].bodyType[1].lastNamesCount = 0
CrewNations.crewnation[6].nation = 'France'.lower()
CrewNations.crewunique = []
CrewNations.crewunique.insert(0, None)
CrewNations.crewunique[0] = Dummy()
CrewNations.crewunique[0].aboveMainExp = 632000
CrewNations.crewunique[0].bodyType = 'unique'
CrewNations.crewunique[0].firstName = 1
CrewNations.crewunique[0].iconIndex = 1
CrewNations.crewunique[0].lastName = 1
CrewNations.crewunique[0].mainExp = 100000
CrewNations.crewunique[0].planeID = 1502
CrewNations.crewunique[0].rank = 5
CrewNations.crewunique[0].specialization = SpecializationEnum.PILOT
CrewNations.crewunique[0].subSpecialization = 1
CrewNations.crewunique[0].uniqueIndex = 1
CrewNations.crewunique.insert(1, None)
CrewNations.crewunique[1] = Dummy()
CrewNations.crewunique[1].aboveMainExp = 632000
CrewNations.crewunique[1].bodyType = 'unique'
CrewNations.crewunique[1].firstName = 1
CrewNations.crewunique[1].iconIndex = 1
CrewNations.crewunique[1].lastName = 1
CrewNations.crewunique[1].mainExp = 100000
CrewNations.crewunique[1].planeID = 2602
CrewNations.crewunique[1].rank = 5
CrewNations.crewunique[1].specialization = SpecializationEnum.PILOT
CrewNations.crewunique[1].subSpecialization = 2
CrewNations.crewunique[1].uniqueIndex = 2
CrewNations.crewunique.insert(2, None)
CrewNations.crewunique[2] = Dummy()
CrewNations.crewunique[2].aboveMainExp = 632000
CrewNations.crewunique[2].bodyType = 'unique'
CrewNations.crewunique[2].firstName = 1
CrewNations.crewunique[2].iconIndex = 1
CrewNations.crewunique[2].lastName = 1
CrewNations.crewunique[2].mainExp = 100000
CrewNations.crewunique[2].planeID = 3604
CrewNations.crewunique[2].rank = 5
CrewNations.crewunique[2].specialization = SpecializationEnum.PILOT
CrewNations.crewunique[2].subSpecialization = 3
CrewNations.crewunique[2].uniqueIndex = 3
CrewNationsDB = None
CrewUniqueDB = None

def initDB():
    global CrewUniqueDB
    global CrewNationsDB
    if CrewNationsDB is None:
        from consts import CREW_BODY_TYPE_PATH
        CrewNationsDB = {}
        d = {name:id for id, name in CREW_BODY_TYPE_PATH.iteritems()}
        for crewnation in CrewNations.crewnation:
            CrewNationsDB[crewnation.nation] = {}
            for bodyTypeData in crewnation.bodyType:
                CrewNationsDB[crewnation.nation][d[bodyTypeData.bodyType]] = bodyTypeData

    if CrewUniqueDB is None:
        CrewUniqueDB = {}
        for uniqueData in CrewNations.crewunique:
            CrewUniqueDB[uniqueData.uniqueIndex] = uniqueData

    return


initDB()