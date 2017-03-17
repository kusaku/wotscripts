# Embedded file name: scripts/common/_specializations_data.py
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


Specializations = Dummy()
Specializations.specialization = []
Specializations.specialization.insert(0, None)
Specializations.specialization[0] = Dummy()
Specializations.specialization[0].id = SpecializationEnum.PILOT
Specializations.specialization[0].startRank = 1
Specializations.specialization.insert(1, None)
Specializations.specialization[1] = Dummy()
Specializations.specialization[1].id = SpecializationEnum.GUNNER
Specializations.specialization[1].startRank = 1
Specializations.specialization.insert(2, None)
Specializations.specialization[2] = Dummy()
Specializations.specialization[2].id = SpecializationEnum.NAVIGATOR
Specializations.specialization[2].startRank = 1
SpecializationsDB = None

def initDB():
    global SpecializationsDB
    if SpecializationsDB is None:
        SpecializationsDB = {}
        for specialization in Specializations.specialization:
            SpecializationsDB[specialization.id] = specialization

    return


initDB()