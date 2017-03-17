# Embedded file name: scripts/client/_economics.py
import Math
import math
import consts
true = True
false = False

class Dummy:
    pass


isServerDatabase = False

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


class QUEST_POOL_GROUP:
    DEFAULT = 0
    NEW_YEAR = 1
    CELEBRATE = 2
    APRIL_1ST = 3
    ALL_TYPES = (DEFAULT,
     NEW_YEAR,
     CELEBRATE,
     APRIL_1ST)


Economics = Dummy()
Economics.creditsTicketSellPrice = 20000
Economics.crewSkillsDropCost = Dummy()
Economics.crewSkillsDropCost.dropCosts = Dummy()
Economics.crewSkillsDropCost.dropCosts.credits = 40000
Economics.crewSkillsDropCost.dropCosts.gold = 100
Economics.crewSkillsDropCost.items = []
Economics.crewSkillsDropCost.items.insert(0, None)
Economics.crewSkillsDropCost.items[0] = Dummy()
Economics.crewSkillsDropCost.items[0].level = 50
Economics.crewSkillsDropCost.items.insert(1, None)
Economics.crewSkillsDropCost.items[1] = Dummy()
Economics.crewSkillsDropCost.items[1].level = 90
Economics.crewSkillsDropCost.items.insert(2, None)
Economics.crewSkillsDropCost.items[2] = Dummy()
Economics.crewSkillsDropCost.items[2].level = 100
Economics.freeXPToCrewXPRate = 5.0
Economics.goldPerTicket = 50
Economics.goldPrice = 400
Economics.goldRateForCreditBuys = 400
Economics.planeBirthday = Dummy()
Economics.planeBirthday.birthday = []
Economics.planeBirthday.birthday.insert(0, None)
Economics.planeBirthday.birthday[0] = Dummy()
Economics.planeBirthday.birthday[0].bonus = []
Economics.planeBirthday.birthday[0].bonus.insert(0, None)
Economics.planeBirthday.birthday[0].bonus[0] = Dummy()
Economics.planeBirthday.birthday[0].bonus[0].level = 1
Economics.planeBirthday.birthday[0].bonus.insert(1, None)
Economics.planeBirthday.birthday[0].bonus[1] = Dummy()
Economics.planeBirthday.birthday[0].bonus[1].freeXP = 400
Economics.planeBirthday.birthday[0].bonus[1].level = 2
Economics.planeBirthday.birthday[0].bonus.insert(2, None)
Economics.planeBirthday.birthday[0].bonus[2] = Dummy()
Economics.planeBirthday.birthday[0].bonus[2].freeXP = 600
Economics.planeBirthday.birthday[0].bonus[2].level = 3
Economics.planeBirthday.birthday[0].bonus.insert(3, None)
Economics.planeBirthday.birthday[0].bonus[3] = Dummy()
Economics.planeBirthday.birthday[0].bonus[3].freeXP = 900
Economics.planeBirthday.birthday[0].bonus[3].level = 4
Economics.planeBirthday.birthday[0].bonus.insert(4, None)
Economics.planeBirthday.birthday[0].bonus[4] = Dummy()
Economics.planeBirthday.birthday[0].bonus[4].freeXP = 1200
Economics.planeBirthday.birthday[0].bonus[4].level = 5
Economics.planeBirthday.birthday[0].bonus.insert(5, None)
Economics.planeBirthday.birthday[0].bonus[5] = Dummy()
Economics.planeBirthday.birthday[0].bonus[5].freeXP = 1800
Economics.planeBirthday.birthday[0].bonus[5].level = 6
Economics.planeBirthday.birthday[0].bonus.insert(6, None)
Economics.planeBirthday.birthday[0].bonus[6] = Dummy()
Economics.planeBirthday.birthday[0].bonus[6].freeXP = 2500
Economics.planeBirthday.birthday[0].bonus[6].level = 7
Economics.planeBirthday.birthday[0].bonus.insert(7, None)
Economics.planeBirthday.birthday[0].bonus[7] = Dummy()
Economics.planeBirthday.birthday[0].bonus[7].freeXP = 3300
Economics.planeBirthday.birthday[0].bonus[7].level = 8
Economics.planeBirthday.birthday[0].bonus.insert(8, None)
Economics.planeBirthday.birthday[0].bonus[8] = Dummy()
Economics.planeBirthday.birthday[0].bonus[8].freeXP = 4300
Economics.planeBirthday.birthday[0].bonus[8].level = 9
Economics.planeBirthday.birthday[0].bonus.insert(9, None)
Economics.planeBirthday.birthday[0].bonus[9] = Dummy()
Economics.planeBirthday.birthday[0].bonus[9].freeXP = 6000
Economics.planeBirthday.birthday[0].bonus[9].level = 10
Economics.planeBirthday.birthday[0].index = 1
Economics.planeBirthday.birthday.insert(1, None)
Economics.planeBirthday.birthday[1] = Dummy()
Economics.planeBirthday.birthday[1].bonus = []
Economics.planeBirthday.birthday[1].bonus.insert(0, None)
Economics.planeBirthday.birthday[1].bonus[0] = Dummy()
Economics.planeBirthday.birthday[1].bonus[0].level = 1
Economics.planeBirthday.birthday[1].bonus.insert(1, None)
Economics.planeBirthday.birthday[1].bonus[1] = Dummy()
Economics.planeBirthday.birthday[1].bonus[1].battles = 7
Economics.planeBirthday.birthday[1].bonus[1].level = 2
Economics.planeBirthday.birthday[1].bonus[1].xpFactor = 2.0
Economics.planeBirthday.birthday[1].bonus.insert(2, None)
Economics.planeBirthday.birthday[1].bonus[2] = Dummy()
Economics.planeBirthday.birthday[1].bonus[2].battles = 9
Economics.planeBirthday.birthday[1].bonus[2].level = 3
Economics.planeBirthday.birthday[1].bonus[2].xpFactor = 2.0
Economics.planeBirthday.birthday[1].bonus.insert(3, None)
Economics.planeBirthday.birthday[1].bonus[3] = Dummy()
Economics.planeBirthday.birthday[1].bonus[3].battles = 10
Economics.planeBirthday.birthday[1].bonus[3].level = 4
Economics.planeBirthday.birthday[1].bonus[3].xpFactor = 2.0
Economics.planeBirthday.birthday[1].bonus.insert(4, None)
Economics.planeBirthday.birthday[1].bonus[4] = Dummy()
Economics.planeBirthday.birthday[1].bonus[4].battles = 11
Economics.planeBirthday.birthday[1].bonus[4].level = 5
Economics.planeBirthday.birthday[1].bonus[4].xpFactor = 2.0
Economics.planeBirthday.birthday[1].bonus.insert(5, None)
Economics.planeBirthday.birthday[1].bonus[5] = Dummy()
Economics.planeBirthday.birthday[1].bonus[5].battles = 13
Economics.planeBirthday.birthday[1].bonus[5].level = 6
Economics.planeBirthday.birthday[1].bonus[5].xpFactor = 2.0
Economics.planeBirthday.birthday[1].bonus.insert(6, None)
Economics.planeBirthday.birthday[1].bonus[6] = Dummy()
Economics.planeBirthday.birthday[1].bonus[6].battles = 14
Economics.planeBirthday.birthday[1].bonus[6].level = 7
Economics.planeBirthday.birthday[1].bonus[6].xpFactor = 2.0
Economics.planeBirthday.birthday[1].bonus.insert(7, None)
Economics.planeBirthday.birthday[1].bonus[7] = Dummy()
Economics.planeBirthday.birthday[1].bonus[7].battles = 16
Economics.planeBirthday.birthday[1].bonus[7].level = 8
Economics.planeBirthday.birthday[1].bonus[7].xpFactor = 2.0
Economics.planeBirthday.birthday[1].bonus.insert(8, None)
Economics.planeBirthday.birthday[1].bonus[8] = Dummy()
Economics.planeBirthday.birthday[1].bonus[8].battles = 18
Economics.planeBirthday.birthday[1].bonus[8].level = 9
Economics.planeBirthday.birthday[1].bonus[8].xpFactor = 2.0
Economics.planeBirthday.birthday[1].bonus.insert(9, None)
Economics.planeBirthday.birthday[1].bonus[9] = Dummy()
Economics.planeBirthday.birthday[1].bonus[9].battles = 20
Economics.planeBirthday.birthday[1].bonus[9].level = 10
Economics.planeBirthday.birthday[1].bonus[9].xpFactor = 2.0
Economics.planeBirthday.birthday[1].index = 2
Economics.planeBirthday.birthday.insert(2, None)
Economics.planeBirthday.birthday[2] = Dummy()
Economics.planeBirthday.birthday[2].bonus = []
Economics.planeBirthday.birthday[2].bonus.insert(0, None)
Economics.planeBirthday.birthday[2].bonus[0] = Dummy()
Economics.planeBirthday.birthday[2].bonus[0].level = 1
Economics.planeBirthday.birthday[2].bonus.insert(1, None)
Economics.planeBirthday.birthday[2].bonus[1] = Dummy()
Economics.planeBirthday.birthday[2].bonus[1].battles = 7
Economics.planeBirthday.birthday[2].bonus[1].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[1].level = 2
Economics.planeBirthday.birthday[2].bonus[1].xpFactor = 2.0
Economics.planeBirthday.birthday[2].bonus.insert(2, None)
Economics.planeBirthday.birthday[2].bonus[2] = Dummy()
Economics.planeBirthday.birthday[2].bonus[2].battles = 9
Economics.planeBirthday.birthday[2].bonus[2].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[2].level = 3
Economics.planeBirthday.birthday[2].bonus[2].xpFactor = 2.0
Economics.planeBirthday.birthday[2].bonus.insert(3, None)
Economics.planeBirthday.birthday[2].bonus[3] = Dummy()
Economics.planeBirthday.birthday[2].bonus[3].battles = 10
Economics.planeBirthday.birthday[2].bonus[3].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[3].level = 4
Economics.planeBirthday.birthday[2].bonus[3].xpFactor = 2.0
Economics.planeBirthday.birthday[2].bonus.insert(4, None)
Economics.planeBirthday.birthday[2].bonus[4] = Dummy()
Economics.planeBirthday.birthday[2].bonus[4].battles = 11
Economics.planeBirthday.birthday[2].bonus[4].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[4].level = 5
Economics.planeBirthday.birthday[2].bonus[4].xpFactor = 2.0
Economics.planeBirthday.birthday[2].bonus.insert(5, None)
Economics.planeBirthday.birthday[2].bonus[5] = Dummy()
Economics.planeBirthday.birthday[2].bonus[5].battles = 13
Economics.planeBirthday.birthday[2].bonus[5].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[5].level = 6
Economics.planeBirthday.birthday[2].bonus[5].xpFactor = 2.0
Economics.planeBirthday.birthday[2].bonus.insert(6, None)
Economics.planeBirthday.birthday[2].bonus[6] = Dummy()
Economics.planeBirthday.birthday[2].bonus[6].battles = 14
Economics.planeBirthday.birthday[2].bonus[6].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[6].level = 7
Economics.planeBirthday.birthday[2].bonus[6].xpFactor = 2.0
Economics.planeBirthday.birthday[2].bonus.insert(7, None)
Economics.planeBirthday.birthday[2].bonus[7] = Dummy()
Economics.planeBirthday.birthday[2].bonus[7].battles = 16
Economics.planeBirthday.birthday[2].bonus[7].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[7].level = 8
Economics.planeBirthday.birthday[2].bonus[7].xpFactor = 2.0
Economics.planeBirthday.birthday[2].bonus.insert(8, None)
Economics.planeBirthday.birthday[2].bonus[8] = Dummy()
Economics.planeBirthday.birthday[2].bonus[8].battles = 18
Economics.planeBirthday.birthday[2].bonus[8].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[8].level = 9
Economics.planeBirthday.birthday[2].bonus[8].xpFactor = 2.0
Economics.planeBirthday.birthday[2].bonus.insert(9, None)
Economics.planeBirthday.birthday[2].bonus[9] = Dummy()
Economics.planeBirthday.birthday[2].bonus[9].battles = 20
Economics.planeBirthday.birthday[2].bonus[9].creditsFactor = 2.0
Economics.planeBirthday.birthday[2].bonus[9].level = 10
Economics.planeBirthday.birthday[2].bonus[9].xpFactor = 2.0
Economics.planeBirthday.birthday[2].index = 3
Economics.planeBirthday.birthday.insert(3, None)
Economics.planeBirthday.birthday[3] = Dummy()
Economics.planeBirthday.birthday[3].bonus = []
Economics.planeBirthday.birthday[3].bonus.insert(0, None)
Economics.planeBirthday.birthday[3].bonus[0] = Dummy()
Economics.planeBirthday.birthday[3].bonus[0].level = 1
Economics.planeBirthday.birthday[3].bonus.insert(1, None)
Economics.planeBirthday.birthday[3].bonus[1] = Dummy()
Economics.planeBirthday.birthday[3].bonus[1].battles = 7
Economics.planeBirthday.birthday[3].bonus[1].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[1].level = 2
Economics.planeBirthday.birthday[3].bonus[1].xpFactor = 3.0
Economics.planeBirthday.birthday[3].bonus.insert(2, None)
Economics.planeBirthday.birthday[3].bonus[2] = Dummy()
Economics.planeBirthday.birthday[3].bonus[2].battles = 9
Economics.planeBirthday.birthday[3].bonus[2].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[2].level = 3
Economics.planeBirthday.birthday[3].bonus[2].xpFactor = 3.0
Economics.planeBirthday.birthday[3].bonus.insert(3, None)
Economics.planeBirthday.birthday[3].bonus[3] = Dummy()
Economics.planeBirthday.birthday[3].bonus[3].battles = 10
Economics.planeBirthday.birthday[3].bonus[3].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[3].level = 4
Economics.planeBirthday.birthday[3].bonus[3].xpFactor = 3.0
Economics.planeBirthday.birthday[3].bonus.insert(4, None)
Economics.planeBirthday.birthday[3].bonus[4] = Dummy()
Economics.planeBirthday.birthday[3].bonus[4].battles = 11
Economics.planeBirthday.birthday[3].bonus[4].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[4].level = 5
Economics.planeBirthday.birthday[3].bonus[4].xpFactor = 3.0
Economics.planeBirthday.birthday[3].bonus.insert(5, None)
Economics.planeBirthday.birthday[3].bonus[5] = Dummy()
Economics.planeBirthday.birthday[3].bonus[5].battles = 13
Economics.planeBirthday.birthday[3].bonus[5].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[5].level = 6
Economics.planeBirthday.birthday[3].bonus[5].xpFactor = 3.0
Economics.planeBirthday.birthday[3].bonus.insert(6, None)
Economics.planeBirthday.birthday[3].bonus[6] = Dummy()
Economics.planeBirthday.birthday[3].bonus[6].battles = 14
Economics.planeBirthday.birthday[3].bonus[6].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[6].level = 7
Economics.planeBirthday.birthday[3].bonus[6].xpFactor = 3.0
Economics.planeBirthday.birthday[3].bonus.insert(7, None)
Economics.planeBirthday.birthday[3].bonus[7] = Dummy()
Economics.planeBirthday.birthday[3].bonus[7].battles = 16
Economics.planeBirthday.birthday[3].bonus[7].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[7].level = 8
Economics.planeBirthday.birthday[3].bonus[7].xpFactor = 3.0
Economics.planeBirthday.birthday[3].bonus.insert(8, None)
Economics.planeBirthday.birthday[3].bonus[8] = Dummy()
Economics.planeBirthday.birthday[3].bonus[8].battles = 18
Economics.planeBirthday.birthday[3].bonus[8].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[8].level = 9
Economics.planeBirthday.birthday[3].bonus[8].xpFactor = 3.0
Economics.planeBirthday.birthday[3].bonus.insert(9, None)
Economics.planeBirthday.birthday[3].bonus[9] = Dummy()
Economics.planeBirthday.birthday[3].bonus[9].battles = 20
Economics.planeBirthday.birthday[3].bonus[9].creditsFactor = 3.0
Economics.planeBirthday.birthday[3].bonus[9].level = 10
Economics.planeBirthday.birthday[3].bonus[9].xpFactor = 3.0
Economics.planeBirthday.birthday[3].index = 4
Economics.planeBirthday.birthday.insert(4, None)
Economics.planeBirthday.birthday[4] = Dummy()
Economics.planeBirthday.birthday[4].bonus = []
Economics.planeBirthday.birthday[4].bonus.insert(0, None)
Economics.planeBirthday.birthday[4].bonus[0] = Dummy()
Economics.planeBirthday.birthday[4].bonus[0].level = 1
Economics.planeBirthday.birthday[4].bonus.insert(1, None)
Economics.planeBirthday.birthday[4].bonus[1] = Dummy()
Economics.planeBirthday.birthday[4].bonus[1].battles = 7
Economics.planeBirthday.birthday[4].bonus[1].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[1].freeXP = 1000
Economics.planeBirthday.birthday[4].bonus[1].level = 2
Economics.planeBirthday.birthday[4].bonus[1].xpFactor = 3.0
Economics.planeBirthday.birthday[4].bonus.insert(2, None)
Economics.planeBirthday.birthday[4].bonus[2] = Dummy()
Economics.planeBirthday.birthday[4].bonus[2].battles = 9
Economics.planeBirthday.birthday[4].bonus[2].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[2].freeXP = 1400
Economics.planeBirthday.birthday[4].bonus[2].level = 3
Economics.planeBirthday.birthday[4].bonus[2].xpFactor = 3.0
Economics.planeBirthday.birthday[4].bonus.insert(3, None)
Economics.planeBirthday.birthday[4].bonus[3] = Dummy()
Economics.planeBirthday.birthday[4].bonus[3].battles = 10
Economics.planeBirthday.birthday[4].bonus[3].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[3].freeXP = 1800
Economics.planeBirthday.birthday[4].bonus[3].level = 4
Economics.planeBirthday.birthday[4].bonus[3].xpFactor = 3.0
Economics.planeBirthday.birthday[4].bonus.insert(4, None)
Economics.planeBirthday.birthday[4].bonus[4] = Dummy()
Economics.planeBirthday.birthday[4].bonus[4].battles = 11
Economics.planeBirthday.birthday[4].bonus[4].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[4].freeXP = 2400
Economics.planeBirthday.birthday[4].bonus[4].level = 5
Economics.planeBirthday.birthday[4].bonus[4].xpFactor = 3.0
Economics.planeBirthday.birthday[4].bonus.insert(5, None)
Economics.planeBirthday.birthday[4].bonus[5] = Dummy()
Economics.planeBirthday.birthday[4].bonus[5].battles = 13
Economics.planeBirthday.birthday[4].bonus[5].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[5].freeXP = 3600
Economics.planeBirthday.birthday[4].bonus[5].level = 6
Economics.planeBirthday.birthday[4].bonus[5].xpFactor = 3.0
Economics.planeBirthday.birthday[4].bonus.insert(6, None)
Economics.planeBirthday.birthday[4].bonus[6] = Dummy()
Economics.planeBirthday.birthday[4].bonus[6].battles = 14
Economics.planeBirthday.birthday[4].bonus[6].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[6].freeXP = 5000
Economics.planeBirthday.birthday[4].bonus[6].level = 7
Economics.planeBirthday.birthday[4].bonus[6].xpFactor = 3.0
Economics.planeBirthday.birthday[4].bonus.insert(7, None)
Economics.planeBirthday.birthday[4].bonus[7] = Dummy()
Economics.planeBirthday.birthday[4].bonus[7].battles = 16
Economics.planeBirthday.birthday[4].bonus[7].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[7].freeXP = 7000
Economics.planeBirthday.birthday[4].bonus[7].level = 8
Economics.planeBirthday.birthday[4].bonus[7].xpFactor = 3.0
Economics.planeBirthday.birthday[4].bonus.insert(8, None)
Economics.planeBirthday.birthday[4].bonus[8] = Dummy()
Economics.planeBirthday.birthday[4].bonus[8].battles = 18
Economics.planeBirthday.birthday[4].bonus[8].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[8].freeXP = 10000
Economics.planeBirthday.birthday[4].bonus[8].level = 9
Economics.planeBirthday.birthday[4].bonus[8].xpFactor = 3.0
Economics.planeBirthday.birthday[4].bonus.insert(9, None)
Economics.planeBirthday.birthday[4].bonus[9] = Dummy()
Economics.planeBirthday.birthday[4].bonus[9].battles = 20
Economics.planeBirthday.birthday[4].bonus[9].camouflage = 1
Economics.planeBirthday.birthday[4].bonus[9].level = 10
Economics.planeBirthday.birthday[4].bonus[9].premium = 5
Economics.planeBirthday.birthday[4].bonus[9].xpFactor = 3.0
Economics.planeBirthday.birthday[4].index = 5
Economics.planeBirthday.birthday.insert(5, None)
Economics.planeBirthday.birthday[5] = Dummy()
Economics.planeBirthday.birthday[5].bonus = []
Economics.planeBirthday.birthday[5].bonus.insert(0, None)
Economics.planeBirthday.birthday[5].bonus[0] = Dummy()
Economics.planeBirthday.birthday[5].bonus[0].level = 1
Economics.planeBirthday.birthday[5].bonus.insert(1, None)
Economics.planeBirthday.birthday[5].bonus[1] = Dummy()
Economics.planeBirthday.birthday[5].bonus[1].battles = 7
Economics.planeBirthday.birthday[5].bonus[1].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[1].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[1].freeXP = 1000
Economics.planeBirthday.birthday[5].bonus[1].level = 2
Economics.planeBirthday.birthday[5].bonus[1].xpFactor = 2.0
Economics.planeBirthday.birthday[5].bonus.insert(2, None)
Economics.planeBirthday.birthday[5].bonus[2] = Dummy()
Economics.planeBirthday.birthday[5].bonus[2].battles = 9
Economics.planeBirthday.birthday[5].bonus[2].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[2].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[2].freeXP = 1400
Economics.planeBirthday.birthday[5].bonus[2].level = 3
Economics.planeBirthday.birthday[5].bonus[2].xpFactor = 2.0
Economics.planeBirthday.birthday[5].bonus.insert(3, None)
Economics.planeBirthday.birthday[5].bonus[3] = Dummy()
Economics.planeBirthday.birthday[5].bonus[3].battles = 10
Economics.planeBirthday.birthday[5].bonus[3].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[3].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[3].freeXP = 1800
Economics.planeBirthday.birthday[5].bonus[3].level = 4
Economics.planeBirthday.birthday[5].bonus[3].xpFactor = 2.0
Economics.planeBirthday.birthday[5].bonus.insert(4, None)
Economics.planeBirthday.birthday[5].bonus[4] = Dummy()
Economics.planeBirthday.birthday[5].bonus[4].battles = 11
Economics.planeBirthday.birthday[5].bonus[4].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[4].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[4].freeXP = 2400
Economics.planeBirthday.birthday[5].bonus[4].level = 5
Economics.planeBirthday.birthday[5].bonus[4].xpFactor = 2.0
Economics.planeBirthday.birthday[5].bonus.insert(5, None)
Economics.planeBirthday.birthday[5].bonus[5] = Dummy()
Economics.planeBirthday.birthday[5].bonus[5].battles = 13
Economics.planeBirthday.birthday[5].bonus[5].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[5].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[5].freeXP = 3600
Economics.planeBirthday.birthday[5].bonus[5].level = 6
Economics.planeBirthday.birthday[5].bonus[5].xpFactor = 2.0
Economics.planeBirthday.birthday[5].bonus.insert(6, None)
Economics.planeBirthday.birthday[5].bonus[6] = Dummy()
Economics.planeBirthday.birthday[5].bonus[6].battles = 14
Economics.planeBirthday.birthday[5].bonus[6].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[6].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[6].freeXP = 5000
Economics.planeBirthday.birthday[5].bonus[6].level = 7
Economics.planeBirthday.birthday[5].bonus[6].xpFactor = 2.0
Economics.planeBirthday.birthday[5].bonus.insert(7, None)
Economics.planeBirthday.birthday[5].bonus[7] = Dummy()
Economics.planeBirthday.birthday[5].bonus[7].battles = 16
Economics.planeBirthday.birthday[5].bonus[7].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[7].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[7].freeXP = 7000
Economics.planeBirthday.birthday[5].bonus[7].level = 8
Economics.planeBirthday.birthday[5].bonus[7].xpFactor = 2.0
Economics.planeBirthday.birthday[5].bonus.insert(8, None)
Economics.planeBirthday.birthday[5].bonus[8] = Dummy()
Economics.planeBirthday.birthday[5].bonus[8].battles = 18
Economics.planeBirthday.birthday[5].bonus[8].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[8].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[8].freeXP = 10000
Economics.planeBirthday.birthday[5].bonus[8].level = 9
Economics.planeBirthday.birthday[5].bonus[8].xpFactor = 2.0
Economics.planeBirthday.birthday[5].bonus.insert(9, None)
Economics.planeBirthday.birthday[5].bonus[9] = Dummy()
Economics.planeBirthday.birthday[5].bonus[9].battles = 20
Economics.planeBirthday.birthday[5].bonus[9].camouflage = 2
Economics.planeBirthday.birthday[5].bonus[9].creditsFactor = 2.0
Economics.planeBirthday.birthday[5].bonus[9].level = 10
Economics.planeBirthday.birthday[5].bonus[9].premium = 5
Economics.planeBirthday.birthday[5].bonus[9].xpFactor = 2.0
Economics.planeBirthday.birthday[5].index = 6
Economics.planeBirthday.birthday.insert(6, None)
Economics.planeBirthday.birthday[6] = Dummy()
Economics.planeBirthday.birthday[6].bonus = []
Economics.planeBirthday.birthday[6].bonus.insert(0, None)
Economics.planeBirthday.birthday[6].bonus[0] = Dummy()
Economics.planeBirthday.birthday[6].bonus[0].level = 1
Economics.planeBirthday.birthday[6].bonus.insert(1, None)
Economics.planeBirthday.birthday[6].bonus[1] = Dummy()
Economics.planeBirthday.birthday[6].bonus[1].battles = 7
Economics.planeBirthday.birthday[6].bonus[1].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[1].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[1].freeXP = 1000
Economics.planeBirthday.birthday[6].bonus[1].level = 2
Economics.planeBirthday.birthday[6].bonus[1].xpFactor = 2.0
Economics.planeBirthday.birthday[6].bonus.insert(2, None)
Economics.planeBirthday.birthday[6].bonus[2] = Dummy()
Economics.planeBirthday.birthday[6].bonus[2].battles = 9
Economics.planeBirthday.birthday[6].bonus[2].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[2].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[2].freeXP = 1400
Economics.planeBirthday.birthday[6].bonus[2].level = 3
Economics.planeBirthday.birthday[6].bonus[2].xpFactor = 2.0
Economics.planeBirthday.birthday[6].bonus.insert(3, None)
Economics.planeBirthday.birthday[6].bonus[3] = Dummy()
Economics.planeBirthday.birthday[6].bonus[3].battles = 10
Economics.planeBirthday.birthday[6].bonus[3].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[3].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[3].freeXP = 1800
Economics.planeBirthday.birthday[6].bonus[3].level = 4
Economics.planeBirthday.birthday[6].bonus[3].xpFactor = 2.0
Economics.planeBirthday.birthday[6].bonus.insert(4, None)
Economics.planeBirthday.birthday[6].bonus[4] = Dummy()
Economics.planeBirthday.birthday[6].bonus[4].battles = 11
Economics.planeBirthday.birthday[6].bonus[4].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[4].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[4].freeXP = 2400
Economics.planeBirthday.birthday[6].bonus[4].level = 5
Economics.planeBirthday.birthday[6].bonus[4].xpFactor = 2.0
Economics.planeBirthday.birthday[6].bonus.insert(5, None)
Economics.planeBirthday.birthday[6].bonus[5] = Dummy()
Economics.planeBirthday.birthday[6].bonus[5].battles = 13
Economics.planeBirthday.birthday[6].bonus[5].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[5].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[5].freeXP = 3600
Economics.planeBirthday.birthday[6].bonus[5].level = 6
Economics.planeBirthday.birthday[6].bonus[5].xpFactor = 2.0
Economics.planeBirthday.birthday[6].bonus.insert(6, None)
Economics.planeBirthday.birthday[6].bonus[6] = Dummy()
Economics.planeBirthday.birthday[6].bonus[6].battles = 14
Economics.planeBirthday.birthday[6].bonus[6].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[6].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[6].freeXP = 5000
Economics.planeBirthday.birthday[6].bonus[6].level = 7
Economics.planeBirthday.birthday[6].bonus[6].xpFactor = 2.0
Economics.planeBirthday.birthday[6].bonus.insert(7, None)
Economics.planeBirthday.birthday[6].bonus[7] = Dummy()
Economics.planeBirthday.birthday[6].bonus[7].battles = 16
Economics.planeBirthday.birthday[6].bonus[7].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[7].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[7].freeXP = 7000
Economics.planeBirthday.birthday[6].bonus[7].level = 8
Economics.planeBirthday.birthday[6].bonus[7].xpFactor = 2.0
Economics.planeBirthday.birthday[6].bonus.insert(8, None)
Economics.planeBirthday.birthday[6].bonus[8] = Dummy()
Economics.planeBirthday.birthday[6].bonus[8].battles = 18
Economics.planeBirthday.birthday[6].bonus[8].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[8].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[8].freeXP = 10000
Economics.planeBirthday.birthday[6].bonus[8].level = 9
Economics.planeBirthday.birthday[6].bonus[8].xpFactor = 2.0
Economics.planeBirthday.birthday[6].bonus.insert(9, None)
Economics.planeBirthday.birthday[6].bonus[9] = Dummy()
Economics.planeBirthday.birthday[6].bonus[9].battles = 20
Economics.planeBirthday.birthday[6].bonus[9].camouflage = 3
Economics.planeBirthday.birthday[6].bonus[9].creditsFactor = 2.0
Economics.planeBirthday.birthday[6].bonus[9].level = 10
Economics.planeBirthday.birthday[6].bonus[9].premium = 5
Economics.planeBirthday.birthday[6].bonus[9].xpFactor = 2.0
Economics.planeBirthday.birthday[6].index = 7
Economics.sellCoeff = 0.5
if isServerDatabase:
    import time
    RepairLevel = {}
    PlaneBirthday = {}
    Economics.LTO.ltoEndTimeInt = int(time.mktime(time.strptime(Economics.LTO.ltoEndTime, '%y%m%d-%H%M')))

    def initDB():
        for level in Economics.repair.level:
            RepairLevel[level.id] = level

        Economics.questPool.dictInfo = {}
        for info in Economics.questPool.info:
            Economics.questPool.dictInfo[info.id] = info

        for pb in Economics.planeBirthday.birthday:
            PlaneBirthday[pb.index] = {}
            for b in pb.bonus:
                PlaneBirthday[pb.index][b.level] = dict(((k, getattr(b, k)) for k in dir(b) if not k.startswith('_') and k != 'level'))


    initDB()
else:
    PlaneBirthday = {}

    def initDB():
        for pb in Economics.planeBirthday.birthday:
            PlaneBirthday[pb.index] = {}
            for b in pb.bonus:
                PlaneBirthday[pb.index][b.level] = dict(((k, getattr(b, k)) for k in dir(b) if not k.startswith('_') and k != 'level'))


    initDB()