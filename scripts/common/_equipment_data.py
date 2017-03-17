# Embedded file name: scripts/common/_equipment_data.py
import Math
import math
import consts
true = True
false = False

class Dummy():
    pass


isServerDatabase = True

class AMMO_TYPE():
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


class ModsTypeEnum():
    AIR_AGILITY = 0
    MAX_SPEED = 1
    WEAPONS_HEATING = 2
    BOMB_MISSILE_FOCUS = 3
    TURRET_DELAY = 4
    GUNNER_ALIVE = 5
    WEAPONS_FOCUS = 6
    TURRET_FOCUS = 7
    TURRET_ANGLE = 8
    TURRET_RANGE = 9
    ENGINE_POWER = 10
    SPEED_AGILITY = 11
    DAMAGE_AGILITY = 12
    FIRE_DURATION = 13
    FIRE_DURATION_PILOT = 14
    FIRE_DURATION_GUNNER = 15
    FIRE_DURATION_NAVIGATOR = 16
    CREW_MEMBER_HP = 17
    SIGHT_RANGE_PILOT = 18
    SIGHT_ANGLE_PILOT = 19
    SIGHT_RANGE_GUNNER = 20
    SIGHT_ANGLE_GUNNER = 21
    SIGHT_RANGE_NAVIGATOR = 22
    SIGHT_ANGLE_NAVIGATOR = 23
    XP_MODIFIER = 24
    SYSTEM_HP = 25
    PILOT_REAR_ARMOR = 26
    CABIN_ARMOR = 27
    VITALS_ARMOR = 28
    FIRE_CHANCE = 29
    EMERGENCY_POWER = 30
    EMERGENCY_HEATING = 31
    HP_RESTORE = 32
    ENGINE_RESTORE = 33
    FIRE_EXTINGUISH_MANUAL = 34
    FIRE_EXTINGUISH_AUTO = 35
    TEMP_IMMORTAL_CREW = 36
    BOMB_DAMADGE_REDUCTION = 37
    FIRE_WORK = 38
    SPARKLERS = 39
    COLOR_PLUMES = 40
    CLEAR_ENGINE_OVERHEAT = 41
    FREE_FORSAGE = 42
    CLEAR_GUNS_OVERHEAT = 43
    FREE_GUNS_FIRING = 44
    FIRE_IMMUNITY = 45
    MAIN_HP = 46
    FIRE_DAMAGE_K = 47
    DIVE_ACCELERATION = 48
    ROLL_MAX_SPEED_CFG = 49
    YAW_MAX_SPEED_CFG = 50
    PITCH_MAX_SPEED_CFG = 51
    ACCEL_BRAKE_CFG = 52
    FAST_ENGINE_COOLING = 53
    LOCK_ENGINE_POWER = 54
    AUTO_ENGINE_RESTORE = 55
    AUTO_AIM = 56
    FIX_TAIL_AND_WINGS = 57
    AA_PLANE_DAMAGE_K = 58
    ECONOMIC_BONUS_XP = 59
    ECONOMIC_BONUS_FREEXP = 60
    ECONOMIC_BONUS_CREDITS = 61
    STEALTH = 62
    DAMAGE_K = 63
    ACTIVATE_ROCKET_DETONATOR = 64
    ROCKET_SPLASH = 65
    ROCKET_DAMAGE = 66
    BOMB_SPLASH = 67
    BOMB_DAMAGE = 68
    CRIT_WEAKNESS_PILOT = 69
    CRIT_WEAKNESS_GUNNER = 70
    EQUIPMENT_EFFECT = 71
    GUNS_INCFLICT_DAMAGE = 72
    GUNS_INFLICT_CRIT = 73
    GUNS_INFLICT_FIRE = 74
    TURRET_INFLICT_CRIT = 75
    GUNNER_ENEMYHP_WATCHER = 76
    GUNNER_BARRAGE_FIRE = 77
    AUTOAIM_ANGLE = 78
    GUNNER_BURST_TIME_MODIFIER = 79
    GUNNER_REDUCTION_TIME = 80
    VISIBILITY_FACTOR_TO_ENEMY = 81
    WEP_WORK_TIME = 82
    EXPLOSIVE_CHARACTER = 83
    TEAM_OBJ_GUNS_INFLICT_FIRE = 84
    ALL_TYPES = (AIR_AGILITY,
     MAX_SPEED,
     WEAPONS_HEATING,
     BOMB_MISSILE_FOCUS,
     TURRET_DELAY,
     GUNNER_ALIVE,
     WEAPONS_FOCUS,
     TURRET_FOCUS,
     TURRET_ANGLE,
     TURRET_RANGE,
     ENGINE_POWER,
     SPEED_AGILITY,
     DAMAGE_AGILITY,
     FIRE_DURATION,
     FIRE_DURATION_PILOT,
     FIRE_DURATION_GUNNER,
     FIRE_DURATION_NAVIGATOR,
     CREW_MEMBER_HP,
     SIGHT_RANGE_PILOT,
     SIGHT_ANGLE_PILOT,
     SIGHT_RANGE_GUNNER,
     SIGHT_ANGLE_GUNNER,
     SIGHT_RANGE_NAVIGATOR,
     SIGHT_ANGLE_NAVIGATOR,
     XP_MODIFIER,
     SYSTEM_HP,
     PILOT_REAR_ARMOR,
     CABIN_ARMOR,
     VITALS_ARMOR,
     FIRE_CHANCE,
     EMERGENCY_POWER,
     EMERGENCY_HEATING,
     HP_RESTORE,
     ENGINE_RESTORE,
     FIRE_EXTINGUISH_MANUAL,
     FIRE_EXTINGUISH_AUTO,
     TEMP_IMMORTAL_CREW,
     BOMB_DAMADGE_REDUCTION,
     FIRE_WORK,
     SPARKLERS,
     COLOR_PLUMES,
     CLEAR_ENGINE_OVERHEAT,
     FREE_FORSAGE,
     CLEAR_GUNS_OVERHEAT,
     FREE_GUNS_FIRING,
     FIRE_IMMUNITY,
     MAIN_HP,
     FIRE_DAMAGE_K,
     DIVE_ACCELERATION,
     ROLL_MAX_SPEED_CFG,
     YAW_MAX_SPEED_CFG,
     PITCH_MAX_SPEED_CFG,
     ACCEL_BRAKE_CFG,
     FAST_ENGINE_COOLING,
     LOCK_ENGINE_POWER,
     AUTO_ENGINE_RESTORE,
     AUTO_AIM,
     FIX_TAIL_AND_WINGS,
     AA_PLANE_DAMAGE_K,
     ECONOMIC_BONUS_XP,
     ECONOMIC_BONUS_FREEXP,
     ECONOMIC_BONUS_CREDITS,
     STEALTH,
     DAMAGE_K,
     ACTIVATE_ROCKET_DETONATOR,
     ROCKET_SPLASH,
     ROCKET_DAMAGE,
     BOMB_SPLASH,
     BOMB_DAMAGE,
     CRIT_WEAKNESS_PILOT,
     CRIT_WEAKNESS_GUNNER,
     EQUIPMENT_EFFECT,
     GUNS_INCFLICT_DAMAGE,
     GUNS_INFLICT_CRIT,
     GUNS_INFLICT_FIRE,
     TURRET_INFLICT_CRIT,
     GUNNER_ENEMYHP_WATCHER,
     GUNNER_BARRAGE_FIRE,
     AUTOAIM_ANGLE,
     GUNNER_BURST_TIME_MODIFIER,
     GUNNER_REDUCTION_TIME,
     VISIBILITY_FACTOR_TO_ENEMY,
     WEP_WORK_TIME,
     EXPLOSIVE_CHARACTER,
     TEAM_OBJ_GUNS_INFLICT_FIRE)


Equipment = Dummy()
Equipment.equipment = []
Equipment.equipment.insert(0, None)
Equipment.equipment[0] = Dummy()
Equipment.equipment[0].buyAvailable = true
Equipment.equipment[0].credits = 50000
Equipment.equipment[0].detachPrice = 0
Equipment.equipment[0].excludeList = []
Equipment.equipment[0].excludeList.insert(0, None)
Equipment.equipment[0].excludeList[0] = 1304
Equipment.equipment[0].excludeList.insert(1, None)
Equipment.equipment[0].excludeList[1] = 1399
Equipment.equipment[0].icoPath = 'icons/modules/equipBetterOpticalSight.png'
Equipment.equipment[0].id = 1
Equipment.equipment[0].includeList = []
Equipment.equipment[0].isDiscount = false
Equipment.equipment[0].isNew = false
Equipment.equipment[0].localizeTag = 'BETTER_OPTICAL_SIGHT'
Equipment.equipment[0].mass = 0
Equipment.equipment[0].maxLevel = 3
Equipment.equipment[0].minLevel = 1
Equipment.equipment[0].mods = []
Equipment.equipment[0].mods.insert(0, None)
Equipment.equipment[0].mods[0] = Dummy()
Equipment.equipment[0].mods[0].type = ModsTypeEnum.WEAPONS_FOCUS
Equipment.equipment[0].mods[0].value_ = 1.1
Equipment.equipment[0].nations = []
Equipment.equipment[0].nations.insert(0, None)
Equipment.equipment[0].nations[0] = 'GB'.lower()
Equipment.equipment[0].nations.insert(1, None)
Equipment.equipment[0].nations[1] = 'Germany'.lower()
Equipment.equipment[0].nations.insert(2, None)
Equipment.equipment[0].nations[2] = 'USA'.lower()
Equipment.equipment[0].nations.insert(3, None)
Equipment.equipment[0].nations[3] = 'Japan'.lower()
Equipment.equipment[0].nations.insert(4, None)
Equipment.equipment[0].nations[4] = 'USSR'.lower()
Equipment.equipment[0].nations.insert(5, None)
Equipment.equipment[0].nations[5] = 'China'.lower()
Equipment.equipment[0].nations.insert(6, None)
Equipment.equipment[0].nations[6] = 'France'.lower()
Equipment.equipment[0].planeType = []
Equipment.equipment[0].tickets = 0
Equipment.equipment[0].uiIndex = 25
Equipment.equipment.insert(1, None)
Equipment.equipment[1] = Dummy()
Equipment.equipment[1].buyAvailable = true
Equipment.equipment[1].credits = 250000
Equipment.equipment[1].detachPrice = 0
Equipment.equipment[1].excludeList = []
Equipment.equipment[1].excludeList.insert(0, None)
Equipment.equipment[1].excludeList[0] = 1304
Equipment.equipment[1].excludeList.insert(1, None)
Equipment.equipment[1].excludeList[1] = 1399
Equipment.equipment[1].icoPath = 'icons/modules/equipBetterReflectorSight.png'
Equipment.equipment[1].id = 2
Equipment.equipment[1].includeList = []
Equipment.equipment[1].isDiscount = false
Equipment.equipment[1].isNew = false
Equipment.equipment[1].localizeTag = 'BETTER_REFLECTOR_SIGHT'
Equipment.equipment[1].mass = 0
Equipment.equipment[1].maxLevel = 6
Equipment.equipment[1].minLevel = 4
Equipment.equipment[1].mods = []
Equipment.equipment[1].mods.insert(0, None)
Equipment.equipment[1].mods[0] = Dummy()
Equipment.equipment[1].mods[0].type = ModsTypeEnum.WEAPONS_FOCUS
Equipment.equipment[1].mods[0].value_ = 1.1
Equipment.equipment[1].nations = []
Equipment.equipment[1].nations.insert(0, None)
Equipment.equipment[1].nations[0] = 'GB'.lower()
Equipment.equipment[1].nations.insert(1, None)
Equipment.equipment[1].nations[1] = 'Germany'.lower()
Equipment.equipment[1].nations.insert(2, None)
Equipment.equipment[1].nations[2] = 'USA'.lower()
Equipment.equipment[1].nations.insert(3, None)
Equipment.equipment[1].nations[3] = 'Japan'.lower()
Equipment.equipment[1].nations.insert(4, None)
Equipment.equipment[1].nations[4] = 'USSR'.lower()
Equipment.equipment[1].nations.insert(5, None)
Equipment.equipment[1].nations[5] = 'China'.lower()
Equipment.equipment[1].nations.insert(6, None)
Equipment.equipment[1].nations[6] = 'France'.lower()
Equipment.equipment[1].planeType = []
Equipment.equipment[1].tickets = 0
Equipment.equipment[1].uiIndex = 27
Equipment.equipment.insert(2, None)
Equipment.equipment[2] = Dummy()
Equipment.equipment[2].buyAvailable = true
Equipment.equipment[2].credits = 500000
Equipment.equipment[2].detachPrice = 0
Equipment.equipment[2].excludeList = []
Equipment.equipment[2].excludeList.insert(0, None)
Equipment.equipment[2].excludeList[0] = 1304
Equipment.equipment[2].excludeList.insert(1, None)
Equipment.equipment[2].excludeList[1] = 1399
Equipment.equipment[2].icoPath = 'icons/modules/equipBetterGyroSight.png'
Equipment.equipment[2].id = 3
Equipment.equipment[2].includeList = []
Equipment.equipment[2].isDiscount = false
Equipment.equipment[2].isNew = false
Equipment.equipment[2].localizeTag = 'BETTER_GYRO_SIGHT'
Equipment.equipment[2].mass = 0
Equipment.equipment[2].maxLevel = 8
Equipment.equipment[2].minLevel = 7
Equipment.equipment[2].mods = []
Equipment.equipment[2].mods.insert(0, None)
Equipment.equipment[2].mods[0] = Dummy()
Equipment.equipment[2].mods[0].type = ModsTypeEnum.WEAPONS_FOCUS
Equipment.equipment[2].mods[0].value_ = 1.1
Equipment.equipment[2].nations = []
Equipment.equipment[2].nations.insert(0, None)
Equipment.equipment[2].nations[0] = 'GB'.lower()
Equipment.equipment[2].nations.insert(1, None)
Equipment.equipment[2].nations[1] = 'Germany'.lower()
Equipment.equipment[2].nations.insert(2, None)
Equipment.equipment[2].nations[2] = 'USA'.lower()
Equipment.equipment[2].nations.insert(3, None)
Equipment.equipment[2].nations[3] = 'France'.lower()
Equipment.equipment[2].planeType = []
Equipment.equipment[2].tickets = 0
Equipment.equipment[2].uiIndex = 28
Equipment.equipment.insert(3, None)
Equipment.equipment[3] = Dummy()
Equipment.equipment[3].buyAvailable = true
Equipment.equipment[3].credits = 600000
Equipment.equipment[3].detachPrice = 0
Equipment.equipment[3].excludeList = []
Equipment.equipment[3].excludeList.insert(0, None)
Equipment.equipment[3].excludeList[0] = 1304
Equipment.equipment[3].excludeList.insert(1, None)
Equipment.equipment[3].excludeList[1] = 1399
Equipment.equipment[3].icoPath = 'icons/modules/equipBetterRadioSight.png'
Equipment.equipment[3].id = 4
Equipment.equipment[3].includeList = []
Equipment.equipment[3].isDiscount = false
Equipment.equipment[3].isNew = false
Equipment.equipment[3].localizeTag = 'BETTER_RADIO_SIGHT'
Equipment.equipment[3].mass = 0
Equipment.equipment[3].maxLevel = 10
Equipment.equipment[3].minLevel = 9
Equipment.equipment[3].mods = []
Equipment.equipment[3].mods.insert(0, None)
Equipment.equipment[3].mods[0] = Dummy()
Equipment.equipment[3].mods[0].type = ModsTypeEnum.WEAPONS_FOCUS
Equipment.equipment[3].mods[0].value_ = 1.15
Equipment.equipment[3].nations = []
Equipment.equipment[3].nations.insert(0, None)
Equipment.equipment[3].nations[0] = 'GB'.lower()
Equipment.equipment[3].nations.insert(1, None)
Equipment.equipment[3].nations[1] = 'USA'.lower()
Equipment.equipment[3].planeType = []
Equipment.equipment[3].tickets = 0
Equipment.equipment[3].uiIndex = 30
Equipment.equipment.insert(4, None)
Equipment.equipment[4] = Dummy()
Equipment.equipment[4].buyAvailable = true
Equipment.equipment[4].credits = 150000
Equipment.equipment[4].detachPrice = 10
Equipment.equipment[4].excludeList = []
Equipment.equipment[4].excludeList.insert(0, None)
Equipment.equipment[4].excludeList[0] = 1304
Equipment.equipment[4].excludeList.insert(1, None)
Equipment.equipment[4].excludeList[1] = 1399
Equipment.equipment[4].icoPath = 'icons/modules/equipDopeCoating.png'
Equipment.equipment[4].id = 5
Equipment.equipment[4].includeList = []
Equipment.equipment[4].isDiscount = false
Equipment.equipment[4].isNew = false
Equipment.equipment[4].localizeTag = 'DOPE_COATING'
Equipment.equipment[4].mass = 0
Equipment.equipment[4].maxLevel = 5
Equipment.equipment[4].minLevel = 4
Equipment.equipment[4].mods = []
Equipment.equipment[4].mods.insert(0, None)
Equipment.equipment[4].mods[0] = Dummy()
Equipment.equipment[4].mods[0].type = ModsTypeEnum.MAX_SPEED
Equipment.equipment[4].mods[0].value_ = 1.05
Equipment.equipment[4].nations = []
Equipment.equipment[4].nations.insert(0, None)
Equipment.equipment[4].nations[0] = 'GB'.lower()
Equipment.equipment[4].nations.insert(1, None)
Equipment.equipment[4].nations[1] = 'Germany'.lower()
Equipment.equipment[4].nations.insert(2, None)
Equipment.equipment[4].nations[2] = 'USA'.lower()
Equipment.equipment[4].nations.insert(3, None)
Equipment.equipment[4].nations[3] = 'Japan'.lower()
Equipment.equipment[4].nations.insert(4, None)
Equipment.equipment[4].nations[4] = 'USSR'.lower()
Equipment.equipment[4].nations.insert(5, None)
Equipment.equipment[4].nations[5] = 'France'.lower()
Equipment.equipment[4].nations.insert(6, None)
Equipment.equipment[4].nations[6] = 'China'.lower()
Equipment.equipment[4].planeType = []
Equipment.equipment[4].planeType.insert(0, None)
Equipment.equipment[4].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[4].planeType.insert(1, None)
Equipment.equipment[4].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[4].tickets = 0
Equipment.equipment[4].uiIndex = 47
Equipment.equipment.insert(5, None)
Equipment.equipment[5] = Dummy()
Equipment.equipment[5].buyAvailable = false
Equipment.equipment[5].credits = 25000
Equipment.equipment[5].detachPrice = 10
Equipment.equipment[5].excludeList = []
Equipment.equipment[5].excludeList.insert(0, None)
Equipment.equipment[5].excludeList[0] = 1304
Equipment.equipment[5].excludeList.insert(1, None)
Equipment.equipment[5].excludeList[1] = 1399
Equipment.equipment[5].icoPath = 'icons/modules/equipBetterClothCoating.png'
Equipment.equipment[5].id = 6
Equipment.equipment[5].includeList = []
Equipment.equipment[5].isDiscount = false
Equipment.equipment[5].isNew = false
Equipment.equipment[5].localizeTag = 'BETTER_CLOTH_COATING'
Equipment.equipment[5].mass = 5
Equipment.equipment[5].maxLevel = 3
Equipment.equipment[5].minLevel = 1
Equipment.equipment[5].mods = []
Equipment.equipment[5].mods.insert(0, None)
Equipment.equipment[5].mods[0] = Dummy()
Equipment.equipment[5].mods[0].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[5].mods[0].value_ = 0.9
Equipment.equipment[5].nations = []
Equipment.equipment[5].nations.insert(0, None)
Equipment.equipment[5].nations[0] = 'GB'.lower()
Equipment.equipment[5].nations.insert(1, None)
Equipment.equipment[5].nations[1] = 'Germany'.lower()
Equipment.equipment[5].nations.insert(2, None)
Equipment.equipment[5].nations[2] = 'USA'.lower()
Equipment.equipment[5].nations.insert(3, None)
Equipment.equipment[5].nations[3] = 'Japan'.lower()
Equipment.equipment[5].nations.insert(4, None)
Equipment.equipment[5].nations[4] = 'USSR'.lower()
Equipment.equipment[5].nations.insert(5, None)
Equipment.equipment[5].nations[5] = 'France'.lower()
Equipment.equipment[5].nations.insert(6, None)
Equipment.equipment[5].nations[6] = 'China'.lower()
Equipment.equipment[5].planeType = []
Equipment.equipment[5].tickets = 0
Equipment.equipment[5].uiIndex = 16
Equipment.equipment.insert(6, None)
Equipment.equipment[6] = Dummy()
Equipment.equipment[6].buyAvailable = false
Equipment.equipment[6].credits = 125000
Equipment.equipment[6].detachPrice = 10
Equipment.equipment[6].excludeList = []
Equipment.equipment[6].excludeList.insert(0, None)
Equipment.equipment[6].excludeList[0] = 1304
Equipment.equipment[6].excludeList.insert(1, None)
Equipment.equipment[6].excludeList[1] = 1399
Equipment.equipment[6].icoPath = 'icons/modules/equipBetterClothCoating.png'
Equipment.equipment[6].id = 7
Equipment.equipment[6].includeList = []
Equipment.equipment[6].isDiscount = false
Equipment.equipment[6].isNew = false
Equipment.equipment[6].localizeTag = 'BETTER_WOODEN_COATING'
Equipment.equipment[6].mass = 10
Equipment.equipment[6].maxLevel = 6
Equipment.equipment[6].minLevel = 4
Equipment.equipment[6].mods = []
Equipment.equipment[6].mods.insert(0, None)
Equipment.equipment[6].mods[0] = Dummy()
Equipment.equipment[6].mods[0].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[6].mods[0].value_ = 0.9
Equipment.equipment[6].nations = []
Equipment.equipment[6].nations.insert(0, None)
Equipment.equipment[6].nations[0] = 'GB'.lower()
Equipment.equipment[6].nations.insert(1, None)
Equipment.equipment[6].nations[1] = 'Germany'.lower()
Equipment.equipment[6].nations.insert(2, None)
Equipment.equipment[6].nations[2] = 'USA'.lower()
Equipment.equipment[6].nations.insert(3, None)
Equipment.equipment[6].nations[3] = 'Japan'.lower()
Equipment.equipment[6].nations.insert(4, None)
Equipment.equipment[6].nations[4] = 'USSR'.lower()
Equipment.equipment[6].nations.insert(5, None)
Equipment.equipment[6].nations[5] = 'France'.lower()
Equipment.equipment[6].nations.insert(6, None)
Equipment.equipment[6].nations[6] = 'China'.lower()
Equipment.equipment[6].planeType = []
Equipment.equipment[6].tickets = 0
Equipment.equipment[6].uiIndex = 17
Equipment.equipment.insert(7, None)
Equipment.equipment[7] = Dummy()
Equipment.equipment[7].buyAvailable = false
Equipment.equipment[7].credits = 350000
Equipment.equipment[7].detachPrice = 10
Equipment.equipment[7].excludeList = []
Equipment.equipment[7].excludeList.insert(0, None)
Equipment.equipment[7].excludeList[0] = 1304
Equipment.equipment[7].excludeList.insert(1, None)
Equipment.equipment[7].excludeList[1] = 1399
Equipment.equipment[7].icoPath = 'icons/modules/equipBetterClothCoating.png'
Equipment.equipment[7].id = 8
Equipment.equipment[7].includeList = []
Equipment.equipment[7].isDiscount = false
Equipment.equipment[7].isNew = false
Equipment.equipment[7].localizeTag = 'FULL_METALL_JACKET'
Equipment.equipment[7].mass = 25
Equipment.equipment[7].maxLevel = 8
Equipment.equipment[7].minLevel = 7
Equipment.equipment[7].mods = []
Equipment.equipment[7].mods.insert(0, None)
Equipment.equipment[7].mods[0] = Dummy()
Equipment.equipment[7].mods[0].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[7].mods[0].value_ = 0.9
Equipment.equipment[7].nations = []
Equipment.equipment[7].nations.insert(0, None)
Equipment.equipment[7].nations[0] = 'GB'.lower()
Equipment.equipment[7].nations.insert(1, None)
Equipment.equipment[7].nations[1] = 'Germany'.lower()
Equipment.equipment[7].nations.insert(2, None)
Equipment.equipment[7].nations[2] = 'USA'.lower()
Equipment.equipment[7].nations.insert(3, None)
Equipment.equipment[7].nations[3] = 'Japan'.lower()
Equipment.equipment[7].nations.insert(4, None)
Equipment.equipment[7].nations[4] = 'USSR'.lower()
Equipment.equipment[7].nations.insert(5, None)
Equipment.equipment[7].nations[5] = 'France'.lower()
Equipment.equipment[7].nations.insert(6, None)
Equipment.equipment[7].nations[6] = 'China'.lower()
Equipment.equipment[7].planeType = []
Equipment.equipment[7].tickets = 0
Equipment.equipment[7].uiIndex = 18
Equipment.equipment.insert(8, None)
Equipment.equipment[8] = Dummy()
Equipment.equipment[8].buyAvailable = true
Equipment.equipment[8].credits = 300000
Equipment.equipment[8].detachPrice = 10
Equipment.equipment[8].excludeList = []
Equipment.equipment[8].excludeList.insert(0, None)
Equipment.equipment[8].excludeList[0] = 1304
Equipment.equipment[8].excludeList.insert(1, None)
Equipment.equipment[8].excludeList[1] = 1399
Equipment.equipment[8].icoPath = 'icons/modules/equipHullPolishing.png'
Equipment.equipment[8].id = 9
Equipment.equipment[8].includeList = []
Equipment.equipment[8].isDiscount = false
Equipment.equipment[8].isNew = false
Equipment.equipment[8].localizeTag = 'HULL_POLISHING'
Equipment.equipment[8].mass = 0
Equipment.equipment[8].maxLevel = 10
Equipment.equipment[8].minLevel = 9
Equipment.equipment[8].mods = []
Equipment.equipment[8].mods.insert(0, None)
Equipment.equipment[8].mods[0] = Dummy()
Equipment.equipment[8].mods[0].type = ModsTypeEnum.MAX_SPEED
Equipment.equipment[8].mods[0].value_ = 1.03
Equipment.equipment[8].nations = []
Equipment.equipment[8].nations.insert(0, None)
Equipment.equipment[8].nations[0] = 'GB'.lower()
Equipment.equipment[8].nations.insert(1, None)
Equipment.equipment[8].nations[1] = 'Germany'.lower()
Equipment.equipment[8].nations.insert(2, None)
Equipment.equipment[8].nations[2] = 'USA'.lower()
Equipment.equipment[8].nations.insert(3, None)
Equipment.equipment[8].nations[3] = 'Japan'.lower()
Equipment.equipment[8].nations.insert(4, None)
Equipment.equipment[8].nations[4] = 'USSR'.lower()
Equipment.equipment[8].nations.insert(5, None)
Equipment.equipment[8].nations[5] = 'France'.lower()
Equipment.equipment[8].nations.insert(6, None)
Equipment.equipment[8].nations[6] = 'China'.lower()
Equipment.equipment[8].planeType = []
Equipment.equipment[8].planeType.insert(0, None)
Equipment.equipment[8].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[8].planeType.insert(1, None)
Equipment.equipment[8].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[8].tickets = 0
Equipment.equipment[8].uiIndex = 48
Equipment.equipment.insert(9, None)
Equipment.equipment[9] = Dummy()
Equipment.equipment[9].buyAvailable = true
Equipment.equipment[9].credits = 250000
Equipment.equipment[9].detachPrice = 0
Equipment.equipment[9].excludeList = []
Equipment.equipment[9].excludeList.insert(0, None)
Equipment.equipment[9].excludeList[0] = 1304
Equipment.equipment[9].excludeList.insert(1, None)
Equipment.equipment[9].excludeList[1] = 1399
Equipment.equipment[9].icoPath = 'icons/modules/equipBetterTankProtector.png'
Equipment.equipment[9].id = 10
Equipment.equipment[9].includeList = []
Equipment.equipment[9].isDiscount = false
Equipment.equipment[9].isNew = false
Equipment.equipment[9].localizeTag = 'NEUTRAL_GAS'
Equipment.equipment[9].mass = 0
Equipment.equipment[9].maxLevel = 7
Equipment.equipment[9].minLevel = 6
Equipment.equipment[9].mods = []
Equipment.equipment[9].mods.insert(0, None)
Equipment.equipment[9].mods[0] = Dummy()
Equipment.equipment[9].mods[0].type = ModsTypeEnum.FIRE_CHANCE
Equipment.equipment[9].mods[0].value_ = 1.5
Equipment.equipment[9].mods.insert(1, None)
Equipment.equipment[9].mods[1] = Dummy()
Equipment.equipment[9].mods[1].type = ModsTypeEnum.FIRE_DAMAGE_K
Equipment.equipment[9].mods[1].value_ = 0.5
Equipment.equipment[9].nations = []
Equipment.equipment[9].nations.insert(0, None)
Equipment.equipment[9].nations[0] = 'GB'.lower()
Equipment.equipment[9].nations.insert(1, None)
Equipment.equipment[9].nations[1] = 'Germany'.lower()
Equipment.equipment[9].nations.insert(2, None)
Equipment.equipment[9].nations[2] = 'USA'.lower()
Equipment.equipment[9].nations.insert(3, None)
Equipment.equipment[9].nations[3] = 'Japan'.lower()
Equipment.equipment[9].nations.insert(4, None)
Equipment.equipment[9].nations[4] = 'USSR'.lower()
Equipment.equipment[9].nations.insert(5, None)
Equipment.equipment[9].nations[5] = 'France'.lower()
Equipment.equipment[9].nations.insert(6, None)
Equipment.equipment[9].nations[6] = 'China'.lower()
Equipment.equipment[9].planeType = []
Equipment.equipment[9].tickets = 0
Equipment.equipment[9].uiIndex = 19
Equipment.equipment.insert(10, None)
Equipment.equipment[10] = Dummy()
Equipment.equipment[10].buyAvailable = true
Equipment.equipment[10].credits = 50000
Equipment.equipment[10].detachPrice = 10
Equipment.equipment[10].excludeList = []
Equipment.equipment[10].excludeList.insert(0, None)
Equipment.equipment[10].excludeList[0] = 1304
Equipment.equipment[10].excludeList.insert(1, None)
Equipment.equipment[10].excludeList[1] = 1399
Equipment.equipment[10].icoPath = 'icons/modules/equipAdditionalArmor.png'
Equipment.equipment[10].id = 11
Equipment.equipment[10].includeList = []
Equipment.equipment[10].isDiscount = false
Equipment.equipment[10].isNew = false
Equipment.equipment[10].localizeTag = 'ADDITIONAL_ARMOR'
Equipment.equipment[10].mass = 150
Equipment.equipment[10].maxLevel = 4
Equipment.equipment[10].minLevel = 2
Equipment.equipment[10].mods = []
Equipment.equipment[10].mods.insert(0, None)
Equipment.equipment[10].mods[0] = Dummy()
Equipment.equipment[10].mods[0].type = ModsTypeEnum.VITALS_ARMOR
Equipment.equipment[10].mods[0].value_ = 0.8
Equipment.equipment[10].nations = []
Equipment.equipment[10].nations.insert(0, None)
Equipment.equipment[10].nations[0] = 'GB'.lower()
Equipment.equipment[10].nations.insert(1, None)
Equipment.equipment[10].nations[1] = 'Germany'.lower()
Equipment.equipment[10].nations.insert(2, None)
Equipment.equipment[10].nations[2] = 'USA'.lower()
Equipment.equipment[10].nations.insert(3, None)
Equipment.equipment[10].nations[3] = 'Japan'.lower()
Equipment.equipment[10].nations.insert(4, None)
Equipment.equipment[10].nations[4] = 'USSR'.lower()
Equipment.equipment[10].nations.insert(5, None)
Equipment.equipment[10].nations[5] = 'France'.lower()
Equipment.equipment[10].nations.insert(6, None)
Equipment.equipment[10].nations[6] = 'China'.lower()
Equipment.equipment[10].planeType = []
Equipment.equipment[10].planeType.insert(0, None)
Equipment.equipment[10].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[10].planeType.insert(1, None)
Equipment.equipment[10].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[10].tickets = 0
Equipment.equipment[10].uiIndex = 20
Equipment.equipment.insert(11, None)
Equipment.equipment[11] = Dummy()
Equipment.equipment[11].buyAvailable = false
Equipment.equipment[11].credits = 75000
Equipment.equipment[11].detachPrice = 10
Equipment.equipment[11].excludeList = []
Equipment.equipment[11].excludeList.insert(0, None)
Equipment.equipment[11].excludeList[0] = 1304
Equipment.equipment[11].excludeList.insert(1, None)
Equipment.equipment[11].excludeList[1] = 1399
Equipment.equipment[11].icoPath = 'icons/modules/equipGlassArmor.png'
Equipment.equipment[11].id = 12
Equipment.equipment[11].includeList = []
Equipment.equipment[11].isDiscount = false
Equipment.equipment[11].isNew = false
Equipment.equipment[11].localizeTag = 'GLASS_ARMOR'
Equipment.equipment[11].mass = 10
Equipment.equipment[11].maxLevel = 5
Equipment.equipment[11].minLevel = 4
Equipment.equipment[11].mods = []
Equipment.equipment[11].mods.insert(0, None)
Equipment.equipment[11].mods[0] = Dummy()
Equipment.equipment[11].mods[0].type = ModsTypeEnum.CREW_MEMBER_HP
Equipment.equipment[11].mods[0].value_ = 0.5
Equipment.equipment[11].nations = []
Equipment.equipment[11].nations.insert(0, None)
Equipment.equipment[11].nations[0] = 'GB'.lower()
Equipment.equipment[11].nations.insert(1, None)
Equipment.equipment[11].nations[1] = 'Germany'.lower()
Equipment.equipment[11].nations.insert(2, None)
Equipment.equipment[11].nations[2] = 'USA'.lower()
Equipment.equipment[11].nations.insert(3, None)
Equipment.equipment[11].nations[3] = 'Japan'.lower()
Equipment.equipment[11].nations.insert(4, None)
Equipment.equipment[11].nations[4] = 'USSR'.lower()
Equipment.equipment[11].nations.insert(5, None)
Equipment.equipment[11].nations[5] = 'France'.lower()
Equipment.equipment[11].nations.insert(6, None)
Equipment.equipment[11].nations[6] = 'China'.lower()
Equipment.equipment[11].planeType = []
Equipment.equipment[11].planeType.insert(0, None)
Equipment.equipment[11].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[11].planeType.insert(1, None)
Equipment.equipment[11].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[11].tickets = 0
Equipment.equipment[11].uiIndex = 21
Equipment.equipment.insert(12, None)
Equipment.equipment[12] = Dummy()
Equipment.equipment[12].buyAvailable = true
Equipment.equipment[12].credits = 300000
Equipment.equipment[12].detachPrice = 0
Equipment.equipment[12].excludeList = []
Equipment.equipment[12].excludeList.insert(0, None)
Equipment.equipment[12].excludeList[0] = 1304
Equipment.equipment[12].excludeList.insert(1, None)
Equipment.equipment[12].excludeList[1] = 1399
Equipment.equipment[12].icoPath = 'icons/modules/equipBetterTankProtector.png'
Equipment.equipment[12].id = 13
Equipment.equipment[12].includeList = []
Equipment.equipment[12].isDiscount = false
Equipment.equipment[12].isNew = false
Equipment.equipment[12].localizeTag = 'FIRE-FIGHTING_SYSTEM'
Equipment.equipment[12].mass = 50
Equipment.equipment[12].maxLevel = 10
Equipment.equipment[12].minLevel = 8
Equipment.equipment[12].mods = []
Equipment.equipment[12].mods.insert(0, None)
Equipment.equipment[12].mods[0] = Dummy()
Equipment.equipment[12].mods[0].type = ModsTypeEnum.FIRE_CHANCE
Equipment.equipment[12].mods[0].value_ = 1.5
Equipment.equipment[12].mods.insert(1, None)
Equipment.equipment[12].mods[1] = Dummy()
Equipment.equipment[12].mods[1].type = ModsTypeEnum.FIRE_DAMAGE_K
Equipment.equipment[12].mods[1].value_ = 0.5
Equipment.equipment[12].nations = []
Equipment.equipment[12].nations.insert(0, None)
Equipment.equipment[12].nations[0] = 'GB'.lower()
Equipment.equipment[12].nations.insert(1, None)
Equipment.equipment[12].nations[1] = 'Germany'.lower()
Equipment.equipment[12].nations.insert(2, None)
Equipment.equipment[12].nations[2] = 'USA'.lower()
Equipment.equipment[12].nations.insert(3, None)
Equipment.equipment[12].nations[3] = 'Japan'.lower()
Equipment.equipment[12].nations.insert(4, None)
Equipment.equipment[12].nations[4] = 'USSR'.lower()
Equipment.equipment[12].nations.insert(5, None)
Equipment.equipment[12].nations[5] = 'France'.lower()
Equipment.equipment[12].nations.insert(6, None)
Equipment.equipment[12].nations[6] = 'China'.lower()
Equipment.equipment[12].planeType = []
Equipment.equipment[12].tickets = 0
Equipment.equipment[12].uiIndex = 22
Equipment.equipment.insert(13, None)
Equipment.equipment[13] = Dummy()
Equipment.equipment[13].buyAvailable = true
Equipment.equipment[13].credits = 450000
Equipment.equipment[13].detachPrice = 0
Equipment.equipment[13].excludeList = []
Equipment.equipment[13].excludeList.insert(0, None)
Equipment.equipment[13].excludeList[0] = 1304
Equipment.equipment[13].excludeList.insert(1, None)
Equipment.equipment[13].excludeList[1] = 1399
Equipment.equipment[13].icoPath = 'icons/modules/equipBetterReflectorSight.png'
Equipment.equipment[13].id = 14
Equipment.equipment[13].includeList = []
Equipment.equipment[13].isDiscount = false
Equipment.equipment[13].isNew = false
Equipment.equipment[13].localizeTag = 'REFLECTOR_SIGHT_II'
Equipment.equipment[13].mass = 0
Equipment.equipment[13].maxLevel = 8
Equipment.equipment[13].minLevel = 7
Equipment.equipment[13].mods = []
Equipment.equipment[13].mods.insert(0, None)
Equipment.equipment[13].mods[0] = Dummy()
Equipment.equipment[13].mods[0].type = ModsTypeEnum.WEAPONS_FOCUS
Equipment.equipment[13].mods[0].value_ = 1.1
Equipment.equipment[13].nations = []
Equipment.equipment[13].nations.insert(0, None)
Equipment.equipment[13].nations[0] = 'Japan'.lower()
Equipment.equipment[13].nations.insert(1, None)
Equipment.equipment[13].nations[1] = 'USSR'.lower()
Equipment.equipment[13].nations.insert(2, None)
Equipment.equipment[13].nations[2] = 'China'.lower()
Equipment.equipment[13].planeType = []
Equipment.equipment[13].tickets = 0
Equipment.equipment[13].uiIndex = 29
Equipment.equipment.insert(14, None)
Equipment.equipment[14] = Dummy()
Equipment.equipment[14].buyAvailable = true
Equipment.equipment[14].credits = 550000
Equipment.equipment[14].detachPrice = 0
Equipment.equipment[14].excludeList = []
Equipment.equipment[14].excludeList.insert(0, None)
Equipment.equipment[14].excludeList[0] = 1304
Equipment.equipment[14].excludeList.insert(1, None)
Equipment.equipment[14].excludeList[1] = 1399
Equipment.equipment[14].icoPath = 'icons/modules/equipBetterGyroSight.png'
Equipment.equipment[14].id = 15
Equipment.equipment[14].includeList = []
Equipment.equipment[14].isDiscount = false
Equipment.equipment[14].isNew = false
Equipment.equipment[14].localizeTag = 'GYRO_SIGHT_II'
Equipment.equipment[14].mass = 0
Equipment.equipment[14].maxLevel = 10
Equipment.equipment[14].minLevel = 9
Equipment.equipment[14].mods = []
Equipment.equipment[14].mods.insert(0, None)
Equipment.equipment[14].mods[0] = Dummy()
Equipment.equipment[14].mods[0].type = ModsTypeEnum.WEAPONS_FOCUS
Equipment.equipment[14].mods[0].value_ = 1.1
Equipment.equipment[14].nations = []
Equipment.equipment[14].nations.insert(0, None)
Equipment.equipment[14].nations[0] = 'Germany'.lower()
Equipment.equipment[14].nations.insert(1, None)
Equipment.equipment[14].nations[1] = 'Japan'.lower()
Equipment.equipment[14].nations.insert(2, None)
Equipment.equipment[14].nations[2] = 'USSR'.lower()
Equipment.equipment[14].nations.insert(3, None)
Equipment.equipment[14].nations[3] = 'France'.lower()
Equipment.equipment[14].nations.insert(4, None)
Equipment.equipment[14].nations[4] = 'China'.lower()
Equipment.equipment[14].planeType = []
Equipment.equipment[14].tickets = 0
Equipment.equipment[14].uiIndex = 26
Equipment.equipment.insert(15, None)
Equipment.equipment[15] = Dummy()
Equipment.equipment[15].buyAvailable = true
Equipment.equipment[15].credits = 250000
Equipment.equipment[15].detachPrice = 10
Equipment.equipment[15].excludeList = []
Equipment.equipment[15].excludeList.insert(0, None)
Equipment.equipment[15].excludeList[0] = 1304
Equipment.equipment[15].excludeList.insert(1, None)
Equipment.equipment[15].excludeList[1] = 1399
Equipment.equipment[15].icoPath = 'icons/modules/equipDopeCoating.png'
Equipment.equipment[15].id = 16
Equipment.equipment[15].includeList = []
Equipment.equipment[15].isDiscount = false
Equipment.equipment[15].isNew = false
Equipment.equipment[15].localizeTag = 'DOPE_COATING_II'
Equipment.equipment[15].mass = 0
Equipment.equipment[15].maxLevel = 8
Equipment.equipment[15].minLevel = 6
Equipment.equipment[15].mods = []
Equipment.equipment[15].mods.insert(0, None)
Equipment.equipment[15].mods[0] = Dummy()
Equipment.equipment[15].mods[0].type = ModsTypeEnum.MAX_SPEED
Equipment.equipment[15].mods[0].value_ = 1.05
Equipment.equipment[15].nations = []
Equipment.equipment[15].nations.insert(0, None)
Equipment.equipment[15].nations[0] = 'GB'.lower()
Equipment.equipment[15].nations.insert(1, None)
Equipment.equipment[15].nations[1] = 'Germany'.lower()
Equipment.equipment[15].nations.insert(2, None)
Equipment.equipment[15].nations[2] = 'USA'.lower()
Equipment.equipment[15].nations.insert(3, None)
Equipment.equipment[15].nations[3] = 'Japan'.lower()
Equipment.equipment[15].nations.insert(4, None)
Equipment.equipment[15].nations[4] = 'USSR'.lower()
Equipment.equipment[15].nations.insert(5, None)
Equipment.equipment[15].nations[5] = 'France'.lower()
Equipment.equipment[15].nations.insert(6, None)
Equipment.equipment[15].nations[6] = 'China'.lower()
Equipment.equipment[15].planeType = []
Equipment.equipment[15].planeType.insert(0, None)
Equipment.equipment[15].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[15].planeType.insert(1, None)
Equipment.equipment[15].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[15].tickets = 0
Equipment.equipment[15].uiIndex = 46
Equipment.equipment.insert(16, None)
Equipment.equipment[16] = Dummy()
Equipment.equipment[16].buyAvailable = false
Equipment.equipment[16].credits = 500000
Equipment.equipment[16].detachPrice = 10
Equipment.equipment[16].excludeList = []
Equipment.equipment[16].excludeList.insert(0, None)
Equipment.equipment[16].excludeList[0] = 1304
Equipment.equipment[16].excludeList.insert(1, None)
Equipment.equipment[16].excludeList[1] = 1399
Equipment.equipment[16].icoPath = 'icons/modules/equipBetterClothCoating.png'
Equipment.equipment[16].id = 17
Equipment.equipment[16].includeList = []
Equipment.equipment[16].isDiscount = false
Equipment.equipment[16].isNew = false
Equipment.equipment[16].localizeTag = 'BETTER_COMBY_COATING'
Equipment.equipment[16].mass = 50
Equipment.equipment[16].maxLevel = 10
Equipment.equipment[16].minLevel = 9
Equipment.equipment[16].mods = []
Equipment.equipment[16].mods.insert(0, None)
Equipment.equipment[16].mods[0] = Dummy()
Equipment.equipment[16].mods[0].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[16].mods[0].value_ = 0.9
Equipment.equipment[16].nations = []
Equipment.equipment[16].nations.insert(0, None)
Equipment.equipment[16].nations[0] = 'GB'.lower()
Equipment.equipment[16].nations.insert(1, None)
Equipment.equipment[16].nations[1] = 'Germany'.lower()
Equipment.equipment[16].nations.insert(2, None)
Equipment.equipment[16].nations[2] = 'USA'.lower()
Equipment.equipment[16].nations.insert(3, None)
Equipment.equipment[16].nations[3] = 'Japan'.lower()
Equipment.equipment[16].nations.insert(4, None)
Equipment.equipment[16].nations[4] = 'USSR'.lower()
Equipment.equipment[16].nations.insert(5, None)
Equipment.equipment[16].nations[5] = 'France'.lower()
Equipment.equipment[16].nations.insert(6, None)
Equipment.equipment[16].nations[6] = 'China'.lower()
Equipment.equipment[16].planeType = []
Equipment.equipment[16].tickets = 0
Equipment.equipment[16].uiIndex = 11
Equipment.equipment.insert(17, None)
Equipment.equipment[17] = Dummy()
Equipment.equipment[17].buyAvailable = true
Equipment.equipment[17].credits = 200000
Equipment.equipment[17].detachPrice = 10
Equipment.equipment[17].excludeList = []
Equipment.equipment[17].excludeList.insert(0, None)
Equipment.equipment[17].excludeList[0] = 1304
Equipment.equipment[17].excludeList.insert(1, None)
Equipment.equipment[17].excludeList[1] = 1399
Equipment.equipment[17].icoPath = 'icons/modules/equipAdditionalArmor.png'
Equipment.equipment[17].id = 18
Equipment.equipment[17].includeList = []
Equipment.equipment[17].isDiscount = false
Equipment.equipment[17].isNew = false
Equipment.equipment[17].localizeTag = 'ADDITIONAL_ARMOR_II'
Equipment.equipment[17].mass = 250
Equipment.equipment[17].maxLevel = 7
Equipment.equipment[17].minLevel = 5
Equipment.equipment[17].mods = []
Equipment.equipment[17].mods.insert(0, None)
Equipment.equipment[17].mods[0] = Dummy()
Equipment.equipment[17].mods[0].type = ModsTypeEnum.VITALS_ARMOR
Equipment.equipment[17].mods[0].value_ = 0.8
Equipment.equipment[17].nations = []
Equipment.equipment[17].nations.insert(0, None)
Equipment.equipment[17].nations[0] = 'GB'.lower()
Equipment.equipment[17].nations.insert(1, None)
Equipment.equipment[17].nations[1] = 'Germany'.lower()
Equipment.equipment[17].nations.insert(2, None)
Equipment.equipment[17].nations[2] = 'USA'.lower()
Equipment.equipment[17].nations.insert(3, None)
Equipment.equipment[17].nations[3] = 'Japan'.lower()
Equipment.equipment[17].nations.insert(4, None)
Equipment.equipment[17].nations[4] = 'USSR'.lower()
Equipment.equipment[17].nations.insert(5, None)
Equipment.equipment[17].nations[5] = 'France'.lower()
Equipment.equipment[17].nations.insert(6, None)
Equipment.equipment[17].nations[6] = 'China'.lower()
Equipment.equipment[17].planeType = []
Equipment.equipment[17].planeType.insert(0, None)
Equipment.equipment[17].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[17].planeType.insert(1, None)
Equipment.equipment[17].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[17].tickets = 0
Equipment.equipment[17].uiIndex = 12
Equipment.equipment.insert(18, None)
Equipment.equipment[18] = Dummy()
Equipment.equipment[18].buyAvailable = true
Equipment.equipment[18].credits = 500000
Equipment.equipment[18].detachPrice = 10
Equipment.equipment[18].excludeList = []
Equipment.equipment[18].excludeList.insert(0, None)
Equipment.equipment[18].excludeList[0] = 1304
Equipment.equipment[18].excludeList.insert(1, None)
Equipment.equipment[18].excludeList[1] = 1399
Equipment.equipment[18].icoPath = 'icons/modules/equipAdditionalArmor.png'
Equipment.equipment[18].id = 19
Equipment.equipment[18].includeList = []
Equipment.equipment[18].isDiscount = false
Equipment.equipment[18].isNew = false
Equipment.equipment[18].localizeTag = 'ADDITIONAL_ARMOR_III'
Equipment.equipment[18].mass = 500
Equipment.equipment[18].maxLevel = 10
Equipment.equipment[18].minLevel = 8
Equipment.equipment[18].mods = []
Equipment.equipment[18].mods.insert(0, None)
Equipment.equipment[18].mods[0] = Dummy()
Equipment.equipment[18].mods[0].type = ModsTypeEnum.VITALS_ARMOR
Equipment.equipment[18].mods[0].value_ = 0.8
Equipment.equipment[18].nations = []
Equipment.equipment[18].nations.insert(0, None)
Equipment.equipment[18].nations[0] = 'GB'.lower()
Equipment.equipment[18].nations.insert(1, None)
Equipment.equipment[18].nations[1] = 'Germany'.lower()
Equipment.equipment[18].nations.insert(2, None)
Equipment.equipment[18].nations[2] = 'USA'.lower()
Equipment.equipment[18].nations.insert(3, None)
Equipment.equipment[18].nations[3] = 'Japan'.lower()
Equipment.equipment[18].nations.insert(4, None)
Equipment.equipment[18].nations[4] = 'USSR'.lower()
Equipment.equipment[18].nations.insert(5, None)
Equipment.equipment[18].nations[5] = 'France'.lower()
Equipment.equipment[18].nations.insert(6, None)
Equipment.equipment[18].nations[6] = 'China'.lower()
Equipment.equipment[18].planeType = []
Equipment.equipment[18].planeType.insert(0, None)
Equipment.equipment[18].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[18].planeType.insert(1, None)
Equipment.equipment[18].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[18].tickets = 0
Equipment.equipment[18].uiIndex = 13
Equipment.equipment.insert(19, None)
Equipment.equipment[19] = Dummy()
Equipment.equipment[19].buyAvailable = false
Equipment.equipment[19].credits = 250000
Equipment.equipment[19].detachPrice = 10
Equipment.equipment[19].excludeList = []
Equipment.equipment[19].excludeList.insert(0, None)
Equipment.equipment[19].excludeList[0] = 1304
Equipment.equipment[19].excludeList.insert(1, None)
Equipment.equipment[19].excludeList[1] = 1399
Equipment.equipment[19].icoPath = 'icons/modules/equipGlassArmor.png'
Equipment.equipment[19].id = 20
Equipment.equipment[19].includeList = []
Equipment.equipment[19].isDiscount = false
Equipment.equipment[19].isNew = false
Equipment.equipment[19].localizeTag = 'GLASS_ARMOR_II'
Equipment.equipment[19].mass = 25
Equipment.equipment[19].maxLevel = 8
Equipment.equipment[19].minLevel = 6
Equipment.equipment[19].mods = []
Equipment.equipment[19].mods.insert(0, None)
Equipment.equipment[19].mods[0] = Dummy()
Equipment.equipment[19].mods[0].type = ModsTypeEnum.CREW_MEMBER_HP
Equipment.equipment[19].mods[0].value_ = 0.5
Equipment.equipment[19].nations = []
Equipment.equipment[19].nations.insert(0, None)
Equipment.equipment[19].nations[0] = 'GB'.lower()
Equipment.equipment[19].nations.insert(1, None)
Equipment.equipment[19].nations[1] = 'Germany'.lower()
Equipment.equipment[19].nations.insert(2, None)
Equipment.equipment[19].nations[2] = 'USA'.lower()
Equipment.equipment[19].nations.insert(3, None)
Equipment.equipment[19].nations[3] = 'Japan'.lower()
Equipment.equipment[19].nations.insert(4, None)
Equipment.equipment[19].nations[4] = 'USSR'.lower()
Equipment.equipment[19].nations.insert(5, None)
Equipment.equipment[19].nations[5] = 'France'.lower()
Equipment.equipment[19].nations.insert(6, None)
Equipment.equipment[19].nations[6] = 'China'.lower()
Equipment.equipment[19].planeType = []
Equipment.equipment[19].planeType.insert(0, None)
Equipment.equipment[19].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[19].planeType.insert(1, None)
Equipment.equipment[19].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[19].tickets = 0
Equipment.equipment[19].uiIndex = 14
Equipment.equipment.insert(20, None)
Equipment.equipment[20] = Dummy()
Equipment.equipment[20].buyAvailable = false
Equipment.equipment[20].credits = 400000
Equipment.equipment[20].detachPrice = 10
Equipment.equipment[20].excludeList = []
Equipment.equipment[20].excludeList.insert(0, None)
Equipment.equipment[20].excludeList[0] = 1304
Equipment.equipment[20].excludeList.insert(1, None)
Equipment.equipment[20].excludeList[1] = 1399
Equipment.equipment[20].icoPath = 'icons/modules/equipGlassArmor.png'
Equipment.equipment[20].id = 21
Equipment.equipment[20].includeList = []
Equipment.equipment[20].isDiscount = false
Equipment.equipment[20].isNew = false
Equipment.equipment[20].localizeTag = 'ARMORED_CABIN'
Equipment.equipment[20].mass = 50
Equipment.equipment[20].maxLevel = 10
Equipment.equipment[20].minLevel = 9
Equipment.equipment[20].mods = []
Equipment.equipment[20].mods.insert(0, None)
Equipment.equipment[20].mods[0] = Dummy()
Equipment.equipment[20].mods[0].type = ModsTypeEnum.CREW_MEMBER_HP
Equipment.equipment[20].mods[0].value_ = 0.5
Equipment.equipment[20].nations = []
Equipment.equipment[20].nations.insert(0, None)
Equipment.equipment[20].nations[0] = 'GB'.lower()
Equipment.equipment[20].nations.insert(1, None)
Equipment.equipment[20].nations[1] = 'Germany'.lower()
Equipment.equipment[20].nations.insert(2, None)
Equipment.equipment[20].nations[2] = 'USA'.lower()
Equipment.equipment[20].nations.insert(3, None)
Equipment.equipment[20].nations[3] = 'Japan'.lower()
Equipment.equipment[20].nations.insert(4, None)
Equipment.equipment[20].nations[4] = 'USSR'.lower()
Equipment.equipment[20].nations.insert(5, None)
Equipment.equipment[20].nations[5] = 'France'.lower()
Equipment.equipment[20].nations.insert(6, None)
Equipment.equipment[20].nations[6] = 'China'.lower()
Equipment.equipment[20].planeType = []
Equipment.equipment[20].planeType.insert(0, None)
Equipment.equipment[20].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[20].planeType.insert(1, None)
Equipment.equipment[20].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[20].tickets = 0
Equipment.equipment[20].uiIndex = 15
Equipment.equipment.insert(21, None)
Equipment.equipment[21] = Dummy()
Equipment.equipment[21].buyAvailable = true
Equipment.equipment[21].credits = 150000
Equipment.equipment[21].detachPrice = 0
Equipment.equipment[21].excludeList = []
Equipment.equipment[21].excludeList.insert(0, None)
Equipment.equipment[21].excludeList[0] = 1304
Equipment.equipment[21].excludeList.insert(1, None)
Equipment.equipment[21].excludeList[1] = 1399
Equipment.equipment[21].icoPath = 'icons/modules/equipBetterTankProtector.png'
Equipment.equipment[21].id = 22
Equipment.equipment[21].includeList = []
Equipment.equipment[21].isDiscount = false
Equipment.equipment[21].isNew = false
Equipment.equipment[21].localizeTag = 'BETTER_TANK_PROTECTOR_I'
Equipment.equipment[21].mass = 10
Equipment.equipment[21].maxLevel = 5
Equipment.equipment[21].minLevel = 4
Equipment.equipment[21].mods = []
Equipment.equipment[21].mods.insert(0, None)
Equipment.equipment[21].mods[0] = Dummy()
Equipment.equipment[21].mods[0].type = ModsTypeEnum.FIRE_CHANCE
Equipment.equipment[21].mods[0].value_ = 1.5
Equipment.equipment[21].mods.insert(1, None)
Equipment.equipment[21].mods[1] = Dummy()
Equipment.equipment[21].mods[1].type = ModsTypeEnum.FIRE_DAMAGE_K
Equipment.equipment[21].mods[1].value_ = 0.5
Equipment.equipment[21].nations = []
Equipment.equipment[21].nations.insert(0, None)
Equipment.equipment[21].nations[0] = 'GB'.lower()
Equipment.equipment[21].nations.insert(1, None)
Equipment.equipment[21].nations[1] = 'Germany'.lower()
Equipment.equipment[21].nations.insert(2, None)
Equipment.equipment[21].nations[2] = 'USA'.lower()
Equipment.equipment[21].nations.insert(3, None)
Equipment.equipment[21].nations[3] = 'Japan'.lower()
Equipment.equipment[21].nations.insert(4, None)
Equipment.equipment[21].nations[4] = 'USSR'.lower()
Equipment.equipment[21].nations.insert(5, None)
Equipment.equipment[21].nations[5] = 'France'.lower()
Equipment.equipment[21].nations.insert(6, None)
Equipment.equipment[21].nations[6] = 'China'.lower()
Equipment.equipment[21].planeType = []
Equipment.equipment[21].tickets = 0
Equipment.equipment[21].uiIndex = 23
Equipment.equipment.insert(22, None)
Equipment.equipment[22] = Dummy()
Equipment.equipment[22].buyAvailable = true
Equipment.equipment[22].credits = 30000
Equipment.equipment[22].detachPrice = 0
Equipment.equipment[22].excludeList = []
Equipment.equipment[22].excludeList.insert(0, None)
Equipment.equipment[22].excludeList[0] = 1304
Equipment.equipment[22].excludeList.insert(1, None)
Equipment.equipment[22].excludeList[1] = 1399
Equipment.equipment[22].icoPath = 'icons/modules/equipEngineTweak.png'
Equipment.equipment[22].id = 23
Equipment.equipment[22].includeList = []
Equipment.equipment[22].isDiscount = false
Equipment.equipment[22].isNew = false
Equipment.equipment[22].localizeTag = 'ENGINE_TWEAK_I'
Equipment.equipment[22].mass = 0
Equipment.equipment[22].maxLevel = 3
Equipment.equipment[22].minLevel = 1
Equipment.equipment[22].mods = []
Equipment.equipment[22].mods.insert(0, None)
Equipment.equipment[22].mods[0] = Dummy()
Equipment.equipment[22].mods[0].type = ModsTypeEnum.ENGINE_POWER
Equipment.equipment[22].mods[0].value_ = 1.05
Equipment.equipment[22].nations = []
Equipment.equipment[22].nations.insert(0, None)
Equipment.equipment[22].nations[0] = 'GB'.lower()
Equipment.equipment[22].nations.insert(1, None)
Equipment.equipment[22].nations[1] = 'Germany'.lower()
Equipment.equipment[22].nations.insert(2, None)
Equipment.equipment[22].nations[2] = 'USA'.lower()
Equipment.equipment[22].nations.insert(3, None)
Equipment.equipment[22].nations[3] = 'Japan'.lower()
Equipment.equipment[22].nations.insert(4, None)
Equipment.equipment[22].nations[4] = 'USSR'.lower()
Equipment.equipment[22].nations.insert(5, None)
Equipment.equipment[22].nations[5] = 'France'.lower()
Equipment.equipment[22].nations.insert(6, None)
Equipment.equipment[22].nations[6] = 'China'.lower()
Equipment.equipment[22].planeType = []
Equipment.equipment[22].tickets = 0
Equipment.equipment[22].uiIndex = 39
Equipment.equipment.insert(23, None)
Equipment.equipment[23] = Dummy()
Equipment.equipment[23].buyAvailable = true
Equipment.equipment[23].credits = 150000
Equipment.equipment[23].detachPrice = 0
Equipment.equipment[23].excludeList = []
Equipment.equipment[23].excludeList.insert(0, None)
Equipment.equipment[23].excludeList[0] = 1304
Equipment.equipment[23].excludeList.insert(1, None)
Equipment.equipment[23].excludeList[1] = 1399
Equipment.equipment[23].icoPath = 'icons/modules/equipEngineTweak.png'
Equipment.equipment[23].id = 24
Equipment.equipment[23].includeList = []
Equipment.equipment[23].isDiscount = false
Equipment.equipment[23].isNew = false
Equipment.equipment[23].localizeTag = 'ENGINE_TWEAK_II'
Equipment.equipment[23].mass = 0
Equipment.equipment[23].maxLevel = 6
Equipment.equipment[23].minLevel = 4
Equipment.equipment[23].mods = []
Equipment.equipment[23].mods.insert(0, None)
Equipment.equipment[23].mods[0] = Dummy()
Equipment.equipment[23].mods[0].type = ModsTypeEnum.ENGINE_POWER
Equipment.equipment[23].mods[0].value_ = 1.05
Equipment.equipment[23].nations = []
Equipment.equipment[23].nations.insert(0, None)
Equipment.equipment[23].nations[0] = 'GB'.lower()
Equipment.equipment[23].nations.insert(1, None)
Equipment.equipment[23].nations[1] = 'Germany'.lower()
Equipment.equipment[23].nations.insert(2, None)
Equipment.equipment[23].nations[2] = 'USA'.lower()
Equipment.equipment[23].nations.insert(3, None)
Equipment.equipment[23].nations[3] = 'Japan'.lower()
Equipment.equipment[23].nations.insert(4, None)
Equipment.equipment[23].nations[4] = 'USSR'.lower()
Equipment.equipment[23].nations.insert(5, None)
Equipment.equipment[23].nations[5] = 'France'.lower()
Equipment.equipment[23].nations.insert(6, None)
Equipment.equipment[23].nations[6] = 'China'.lower()
Equipment.equipment[23].planeType = []
Equipment.equipment[23].tickets = 0
Equipment.equipment[23].uiIndex = 40
Equipment.equipment.insert(24, None)
Equipment.equipment[24] = Dummy()
Equipment.equipment[24].buyAvailable = true
Equipment.equipment[24].credits = 375000
Equipment.equipment[24].detachPrice = 0
Equipment.equipment[24].excludeList = []
Equipment.equipment[24].excludeList.insert(0, None)
Equipment.equipment[24].excludeList[0] = 1304
Equipment.equipment[24].excludeList.insert(1, None)
Equipment.equipment[24].excludeList[1] = 1399
Equipment.equipment[24].excludeList.insert(2, None)
Equipment.equipment[24].excludeList[2] = 4891
Equipment.equipment[24].excludeList.insert(3, None)
Equipment.equipment[24].excludeList[3] = 2792
Equipment.equipment[24].icoPath = 'icons/modules/equipEngineTweak.png'
Equipment.equipment[24].id = 25
Equipment.equipment[24].includeList = []
Equipment.equipment[24].isDiscount = false
Equipment.equipment[24].isNew = false
Equipment.equipment[24].localizeTag = 'ENGINE_TWEAK_III'
Equipment.equipment[24].mass = 0
Equipment.equipment[24].maxLevel = 8
Equipment.equipment[24].minLevel = 7
Equipment.equipment[24].mods = []
Equipment.equipment[24].mods.insert(0, None)
Equipment.equipment[24].mods[0] = Dummy()
Equipment.equipment[24].mods[0].type = ModsTypeEnum.ENGINE_POWER
Equipment.equipment[24].mods[0].value_ = 1.05
Equipment.equipment[24].nations = []
Equipment.equipment[24].nations.insert(0, None)
Equipment.equipment[24].nations[0] = 'GB'.lower()
Equipment.equipment[24].nations.insert(1, None)
Equipment.equipment[24].nations[1] = 'Germany'.lower()
Equipment.equipment[24].nations.insert(2, None)
Equipment.equipment[24].nations[2] = 'USA'.lower()
Equipment.equipment[24].nations.insert(3, None)
Equipment.equipment[24].nations[3] = 'Japan'.lower()
Equipment.equipment[24].nations.insert(4, None)
Equipment.equipment[24].nations[4] = 'France'.lower()
Equipment.equipment[24].nations.insert(5, None)
Equipment.equipment[24].nations[5] = 'USSR'.lower()
Equipment.equipment[24].nations.insert(6, None)
Equipment.equipment[24].nations[6] = 'China'.lower()
Equipment.equipment[24].planeType = []
Equipment.equipment[24].tickets = 0
Equipment.equipment[24].uiIndex = 41
Equipment.equipment.insert(25, None)
Equipment.equipment[25] = Dummy()
Equipment.equipment[25].buyAvailable = true
Equipment.equipment[25].credits = 550000
Equipment.equipment[25].detachPrice = 0
Equipment.equipment[25].excludeList = []
Equipment.equipment[25].excludeList.insert(0, None)
Equipment.equipment[25].excludeList[0] = 1304
Equipment.equipment[25].excludeList.insert(1, None)
Equipment.equipment[25].excludeList[1] = 1399
Equipment.equipment[25].icoPath = 'icons/modules/equipEngineTweak.png'
Equipment.equipment[25].id = 26
Equipment.equipment[25].includeList = []
Equipment.equipment[25].isDiscount = false
Equipment.equipment[25].isNew = false
Equipment.equipment[25].localizeTag = 'ENGINE_TWEAK_IV'
Equipment.equipment[25].mass = 0
Equipment.equipment[25].maxLevel = 10
Equipment.equipment[25].minLevel = 9
Equipment.equipment[25].mods = []
Equipment.equipment[25].mods.insert(0, None)
Equipment.equipment[25].mods[0] = Dummy()
Equipment.equipment[25].mods[0].type = ModsTypeEnum.ENGINE_POWER
Equipment.equipment[25].mods[0].value_ = 1.04
Equipment.equipment[25].nations = []
Equipment.equipment[25].nations.insert(0, None)
Equipment.equipment[25].nations[0] = 'GB'.lower()
Equipment.equipment[25].nations.insert(1, None)
Equipment.equipment[25].nations[1] = 'Germany'.lower()
Equipment.equipment[25].nations.insert(2, None)
Equipment.equipment[25].nations[2] = 'USA'.lower()
Equipment.equipment[25].nations.insert(3, None)
Equipment.equipment[25].nations[3] = 'Japan'.lower()
Equipment.equipment[25].nations.insert(4, None)
Equipment.equipment[25].nations[4] = 'USSR'.lower()
Equipment.equipment[25].nations.insert(5, None)
Equipment.equipment[25].nations[5] = 'France'.lower()
Equipment.equipment[25].nations.insert(6, None)
Equipment.equipment[25].nations[6] = 'China'.lower()
Equipment.equipment[25].planeType = []
Equipment.equipment[25].tickets = 0
Equipment.equipment[25].uiIndex = 42
Equipment.equipment.insert(26, None)
Equipment.equipment[26] = Dummy()
Equipment.equipment[26].buyAvailable = true
Equipment.equipment[26].credits = 50000
Equipment.equipment[26].detachPrice = 0
Equipment.equipment[26].excludeList = []
Equipment.equipment[26].excludeList.insert(0, None)
Equipment.equipment[26].excludeList[0] = 1304
Equipment.equipment[26].excludeList.insert(1, None)
Equipment.equipment[26].excludeList[1] = 1399
Equipment.equipment[26].icoPath = 'icons/modules/equipImprovedFlaps.png'
Equipment.equipment[26].id = 27
Equipment.equipment[26].includeList = []
Equipment.equipment[26].isDiscount = false
Equipment.equipment[26].isNew = false
Equipment.equipment[26].localizeTag = 'IMPROVED_FLAPS_I'
Equipment.equipment[26].mass = 0
Equipment.equipment[26].maxLevel = 4
Equipment.equipment[26].minLevel = 2
Equipment.equipment[26].mods = []
Equipment.equipment[26].mods.insert(0, None)
Equipment.equipment[26].mods[0] = Dummy()
Equipment.equipment[26].mods[0].type = ModsTypeEnum.ACCEL_BRAKE_CFG
Equipment.equipment[26].mods[0].value_ = 1.2
Equipment.equipment[26].mods.insert(1, None)
Equipment.equipment[26].mods[1] = Dummy()
Equipment.equipment[26].mods[1].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[26].mods[1].value_ = 1.01
Equipment.equipment[26].nations = []
Equipment.equipment[26].nations.insert(0, None)
Equipment.equipment[26].nations[0] = 'GB'.lower()
Equipment.equipment[26].nations.insert(1, None)
Equipment.equipment[26].nations[1] = 'Germany'.lower()
Equipment.equipment[26].nations.insert(2, None)
Equipment.equipment[26].nations[2] = 'USA'.lower()
Equipment.equipment[26].nations.insert(3, None)
Equipment.equipment[26].nations[3] = 'Japan'.lower()
Equipment.equipment[26].nations.insert(4, None)
Equipment.equipment[26].nations[4] = 'USSR'.lower()
Equipment.equipment[26].nations.insert(5, None)
Equipment.equipment[26].nations[5] = 'France'.lower()
Equipment.equipment[26].nations.insert(6, None)
Equipment.equipment[26].nations[6] = 'China'.lower()
Equipment.equipment[26].planeType = []
Equipment.equipment[26].planeType.insert(0, None)
Equipment.equipment[26].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[26].planeType.insert(1, None)
Equipment.equipment[26].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[26].tickets = 0
Equipment.equipment[26].uiIndex = 57
Equipment.equipment.insert(27, None)
Equipment.equipment[27] = Dummy()
Equipment.equipment[27].buyAvailable = true
Equipment.equipment[27].credits = 200000
Equipment.equipment[27].detachPrice = 0
Equipment.equipment[27].excludeList = []
Equipment.equipment[27].excludeList.insert(0, None)
Equipment.equipment[27].excludeList[0] = 1304
Equipment.equipment[27].excludeList.insert(1, None)
Equipment.equipment[27].excludeList[1] = 1399
Equipment.equipment[27].icoPath = 'icons/modules/equipImprovedFlaps.png'
Equipment.equipment[27].id = 28
Equipment.equipment[27].includeList = []
Equipment.equipment[27].isDiscount = false
Equipment.equipment[27].isNew = false
Equipment.equipment[27].localizeTag = 'IMPROVED_FLAPS_II'
Equipment.equipment[27].mass = 0
Equipment.equipment[27].maxLevel = 7
Equipment.equipment[27].minLevel = 5
Equipment.equipment[27].mods = []
Equipment.equipment[27].mods.insert(0, None)
Equipment.equipment[27].mods[0] = Dummy()
Equipment.equipment[27].mods[0].type = ModsTypeEnum.ACCEL_BRAKE_CFG
Equipment.equipment[27].mods[0].value_ = 1.2
Equipment.equipment[27].mods.insert(1, None)
Equipment.equipment[27].mods[1] = Dummy()
Equipment.equipment[27].mods[1].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[27].mods[1].value_ = 1.01
Equipment.equipment[27].nations = []
Equipment.equipment[27].nations.insert(0, None)
Equipment.equipment[27].nations[0] = 'GB'.lower()
Equipment.equipment[27].nations.insert(1, None)
Equipment.equipment[27].nations[1] = 'Germany'.lower()
Equipment.equipment[27].nations.insert(2, None)
Equipment.equipment[27].nations[2] = 'USA'.lower()
Equipment.equipment[27].nations.insert(3, None)
Equipment.equipment[27].nations[3] = 'Japan'.lower()
Equipment.equipment[27].nations.insert(4, None)
Equipment.equipment[27].nations[4] = 'USSR'.lower()
Equipment.equipment[27].nations.insert(5, None)
Equipment.equipment[27].nations[5] = 'France'.lower()
Equipment.equipment[27].nations.insert(6, None)
Equipment.equipment[27].nations[6] = 'China'.lower()
Equipment.equipment[27].planeType = []
Equipment.equipment[27].planeType.insert(0, None)
Equipment.equipment[27].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[27].planeType.insert(1, None)
Equipment.equipment[27].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[27].tickets = 0
Equipment.equipment[27].uiIndex = 58
Equipment.equipment.insert(28, None)
Equipment.equipment[28] = Dummy()
Equipment.equipment[28].buyAvailable = true
Equipment.equipment[28].credits = 450000
Equipment.equipment[28].detachPrice = 0
Equipment.equipment[28].excludeList = []
Equipment.equipment[28].excludeList.insert(0, None)
Equipment.equipment[28].excludeList[0] = 1304
Equipment.equipment[28].excludeList.insert(1, None)
Equipment.equipment[28].excludeList[1] = 1399
Equipment.equipment[28].icoPath = 'icons/modules/equipImprovedFlaps.png'
Equipment.equipment[28].id = 29
Equipment.equipment[28].includeList = []
Equipment.equipment[28].isDiscount = false
Equipment.equipment[28].isNew = false
Equipment.equipment[28].localizeTag = 'IMPROVED_FLAPS_III'
Equipment.equipment[28].mass = 0
Equipment.equipment[28].maxLevel = 10
Equipment.equipment[28].minLevel = 8
Equipment.equipment[28].mods = []
Equipment.equipment[28].mods.insert(0, None)
Equipment.equipment[28].mods[0] = Dummy()
Equipment.equipment[28].mods[0].type = ModsTypeEnum.ACCEL_BRAKE_CFG
Equipment.equipment[28].mods[0].value_ = 1.2
Equipment.equipment[28].mods.insert(1, None)
Equipment.equipment[28].mods[1] = Dummy()
Equipment.equipment[28].mods[1].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[28].mods[1].value_ = 1.01
Equipment.equipment[28].nations = []
Equipment.equipment[28].nations.insert(0, None)
Equipment.equipment[28].nations[0] = 'GB'.lower()
Equipment.equipment[28].nations.insert(1, None)
Equipment.equipment[28].nations[1] = 'Germany'.lower()
Equipment.equipment[28].nations.insert(2, None)
Equipment.equipment[28].nations[2] = 'USA'.lower()
Equipment.equipment[28].nations.insert(3, None)
Equipment.equipment[28].nations[3] = 'Japan'.lower()
Equipment.equipment[28].nations.insert(4, None)
Equipment.equipment[28].nations[4] = 'USSR'.lower()
Equipment.equipment[28].nations.insert(5, None)
Equipment.equipment[28].nations[5] = 'France'.lower()
Equipment.equipment[28].nations.insert(6, None)
Equipment.equipment[28].nations[6] = 'China'.lower()
Equipment.equipment[28].planeType = []
Equipment.equipment[28].planeType.insert(0, None)
Equipment.equipment[28].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[28].planeType.insert(1, None)
Equipment.equipment[28].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[28].tickets = 0
Equipment.equipment[28].uiIndex = 59
Equipment.equipment.insert(29, None)
Equipment.equipment[29] = Dummy()
Equipment.equipment[29].buyAvailable = true
Equipment.equipment[29].credits = 15000
Equipment.equipment[29].detachPrice = 10
Equipment.equipment[29].excludeList = []
Equipment.equipment[29].excludeList.insert(0, None)
Equipment.equipment[29].excludeList[0] = 1304
Equipment.equipment[29].excludeList.insert(1, None)
Equipment.equipment[29].excludeList[1] = 1399
Equipment.equipment[29].icoPath = 'icons/modules/equipAdaptCamo.png'
Equipment.equipment[29].id = 30
Equipment.equipment[29].includeList = []
Equipment.equipment[29].isDiscount = false
Equipment.equipment[29].isNew = false
Equipment.equipment[29].localizeTag = 'ADAPT_CAMO_I'
Equipment.equipment[29].mass = 0
Equipment.equipment[29].maxLevel = 4
Equipment.equipment[29].minLevel = 2
Equipment.equipment[29].mods = []
Equipment.equipment[29].mods.insert(0, None)
Equipment.equipment[29].mods[0] = Dummy()
Equipment.equipment[29].mods[0].type = ModsTypeEnum.AA_PLANE_DAMAGE_K
Equipment.equipment[29].mods[0].value_ = 0.7
Equipment.equipment[29].nations = []
Equipment.equipment[29].nations.insert(0, None)
Equipment.equipment[29].nations[0] = 'GB'.lower()
Equipment.equipment[29].nations.insert(1, None)
Equipment.equipment[29].nations[1] = 'Germany'.lower()
Equipment.equipment[29].nations.insert(2, None)
Equipment.equipment[29].nations[2] = 'USA'.lower()
Equipment.equipment[29].nations.insert(3, None)
Equipment.equipment[29].nations[3] = 'Japan'.lower()
Equipment.equipment[29].nations.insert(4, None)
Equipment.equipment[29].nations[4] = 'USSR'.lower()
Equipment.equipment[29].nations.insert(5, None)
Equipment.equipment[29].nations[5] = 'France'.lower()
Equipment.equipment[29].nations.insert(6, None)
Equipment.equipment[29].nations[6] = 'China'.lower()
Equipment.equipment[29].planeType = []
Equipment.equipment[29].planeType.insert(0, None)
Equipment.equipment[29].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[29].planeType.insert(1, None)
Equipment.equipment[29].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[29].tickets = 0
Equipment.equipment[29].uiIndex = 1
Equipment.equipment.insert(30, None)
Equipment.equipment[30] = Dummy()
Equipment.equipment[30].buyAvailable = true
Equipment.equipment[30].credits = 200000
Equipment.equipment[30].detachPrice = 10
Equipment.equipment[30].excludeList = []
Equipment.equipment[30].excludeList.insert(0, None)
Equipment.equipment[30].excludeList[0] = 1304
Equipment.equipment[30].excludeList.insert(1, None)
Equipment.equipment[30].excludeList[1] = 1399
Equipment.equipment[30].icoPath = 'icons/modules/equipAdaptCamo.png'
Equipment.equipment[30].id = 31
Equipment.equipment[30].includeList = []
Equipment.equipment[30].isDiscount = false
Equipment.equipment[30].isNew = false
Equipment.equipment[30].localizeTag = 'ADAPT_CAMO_II'
Equipment.equipment[30].mass = 0
Equipment.equipment[30].maxLevel = 7
Equipment.equipment[30].minLevel = 5
Equipment.equipment[30].mods = []
Equipment.equipment[30].mods.insert(0, None)
Equipment.equipment[30].mods[0] = Dummy()
Equipment.equipment[30].mods[0].type = ModsTypeEnum.AA_PLANE_DAMAGE_K
Equipment.equipment[30].mods[0].value_ = 0.7
Equipment.equipment[30].nations = []
Equipment.equipment[30].nations.insert(0, None)
Equipment.equipment[30].nations[0] = 'GB'.lower()
Equipment.equipment[30].nations.insert(1, None)
Equipment.equipment[30].nations[1] = 'Germany'.lower()
Equipment.equipment[30].nations.insert(2, None)
Equipment.equipment[30].nations[2] = 'USA'.lower()
Equipment.equipment[30].nations.insert(3, None)
Equipment.equipment[30].nations[3] = 'Japan'.lower()
Equipment.equipment[30].nations.insert(4, None)
Equipment.equipment[30].nations[4] = 'USSR'.lower()
Equipment.equipment[30].nations.insert(5, None)
Equipment.equipment[30].nations[5] = 'France'.lower()
Equipment.equipment[30].nations.insert(6, None)
Equipment.equipment[30].nations[6] = 'China'.lower()
Equipment.equipment[30].planeType = []
Equipment.equipment[30].planeType.insert(0, None)
Equipment.equipment[30].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[30].planeType.insert(1, None)
Equipment.equipment[30].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[30].tickets = 0
Equipment.equipment[30].uiIndex = 2
Equipment.equipment.insert(31, None)
Equipment.equipment[31] = Dummy()
Equipment.equipment[31].buyAvailable = true
Equipment.equipment[31].credits = 400000
Equipment.equipment[31].detachPrice = 10
Equipment.equipment[31].excludeList = []
Equipment.equipment[31].excludeList.insert(0, None)
Equipment.equipment[31].excludeList[0] = 1304
Equipment.equipment[31].excludeList.insert(1, None)
Equipment.equipment[31].excludeList[1] = 1399
Equipment.equipment[31].icoPath = 'icons/modules/equipAdaptCamo.png'
Equipment.equipment[31].id = 32
Equipment.equipment[31].includeList = []
Equipment.equipment[31].isDiscount = false
Equipment.equipment[31].isNew = false
Equipment.equipment[31].localizeTag = 'ADAPT_CAMO_III'
Equipment.equipment[31].mass = 0
Equipment.equipment[31].maxLevel = 10
Equipment.equipment[31].minLevel = 8
Equipment.equipment[31].mods = []
Equipment.equipment[31].mods.insert(0, None)
Equipment.equipment[31].mods[0] = Dummy()
Equipment.equipment[31].mods[0].type = ModsTypeEnum.AA_PLANE_DAMAGE_K
Equipment.equipment[31].mods[0].value_ = 0.7
Equipment.equipment[31].nations = []
Equipment.equipment[31].nations.insert(0, None)
Equipment.equipment[31].nations[0] = 'GB'.lower()
Equipment.equipment[31].nations.insert(1, None)
Equipment.equipment[31].nations[1] = 'Germany'.lower()
Equipment.equipment[31].nations.insert(2, None)
Equipment.equipment[31].nations[2] = 'USA'.lower()
Equipment.equipment[31].nations.insert(3, None)
Equipment.equipment[31].nations[3] = 'Japan'.lower()
Equipment.equipment[31].nations.insert(4, None)
Equipment.equipment[31].nations[4] = 'USSR'.lower()
Equipment.equipment[31].nations.insert(5, None)
Equipment.equipment[31].nations[5] = 'France'.lower()
Equipment.equipment[31].nations.insert(6, None)
Equipment.equipment[31].nations[6] = 'China'.lower()
Equipment.equipment[31].planeType = []
Equipment.equipment[31].planeType.insert(0, None)
Equipment.equipment[31].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[31].planeType.insert(1, None)
Equipment.equipment[31].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[31].tickets = 0
Equipment.equipment[31].uiIndex = 3
Equipment.equipment.insert(32, None)
Equipment.equipment[32] = Dummy()
Equipment.equipment[32].buyAvailable = true
Equipment.equipment[32].credits = 20000
Equipment.equipment[32].detachPrice = 10
Equipment.equipment[32].excludeList = []
Equipment.equipment[32].excludeList.insert(0, None)
Equipment.equipment[32].excludeList[0] = 1304
Equipment.equipment[32].excludeList.insert(1, None)
Equipment.equipment[32].excludeList[1] = 1399
Equipment.equipment[32].icoPath = 'icons/modules/equipGravityCenter.png'
Equipment.equipment[32].id = 33
Equipment.equipment[32].includeList = []
Equipment.equipment[32].isDiscount = false
Equipment.equipment[32].isNew = false
Equipment.equipment[32].localizeTag = 'GRAVITY_CENTER_I'
Equipment.equipment[32].mass = 0
Equipment.equipment[32].maxLevel = 3
Equipment.equipment[32].minLevel = 2
Equipment.equipment[32].mods = []
Equipment.equipment[32].mods.insert(0, None)
Equipment.equipment[32].mods[0] = Dummy()
Equipment.equipment[32].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[32].mods[0].value_ = 1.008
Equipment.equipment[32].nations = []
Equipment.equipment[32].nations.insert(0, None)
Equipment.equipment[32].nations[0] = 'GB'.lower()
Equipment.equipment[32].nations.insert(1, None)
Equipment.equipment[32].nations[1] = 'Germany'.lower()
Equipment.equipment[32].nations.insert(2, None)
Equipment.equipment[32].nations[2] = 'USA'.lower()
Equipment.equipment[32].nations.insert(3, None)
Equipment.equipment[32].nations[3] = 'Japan'.lower()
Equipment.equipment[32].nations.insert(4, None)
Equipment.equipment[32].nations[4] = 'USSR'.lower()
Equipment.equipment[32].nations.insert(5, None)
Equipment.equipment[32].nations[5] = 'France'.lower()
Equipment.equipment[32].nations.insert(6, None)
Equipment.equipment[32].nations[6] = 'China'.lower()
Equipment.equipment[32].planeType = []
Equipment.equipment[32].planeType.insert(0, None)
Equipment.equipment[32].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[32].planeType.insert(1, None)
Equipment.equipment[32].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[32].tickets = 0
Equipment.equipment[32].uiIndex = 64
Equipment.equipment.insert(33, None)
Equipment.equipment[33] = Dummy()
Equipment.equipment[33].buyAvailable = true
Equipment.equipment[33].credits = 150000
Equipment.equipment[33].detachPrice = 10
Equipment.equipment[33].excludeList = []
Equipment.equipment[33].excludeList.insert(0, None)
Equipment.equipment[33].excludeList[0] = 1304
Equipment.equipment[33].excludeList.insert(1, None)
Equipment.equipment[33].excludeList[1] = 1399
Equipment.equipment[33].icoPath = 'icons/modules/equipGravityCenter.png'
Equipment.equipment[33].id = 34
Equipment.equipment[33].includeList = []
Equipment.equipment[33].isDiscount = false
Equipment.equipment[33].isNew = false
Equipment.equipment[33].localizeTag = 'GRAVITY_CENTER_II'
Equipment.equipment[33].mass = 0
Equipment.equipment[33].maxLevel = 6
Equipment.equipment[33].minLevel = 4
Equipment.equipment[33].mods = []
Equipment.equipment[33].mods.insert(0, None)
Equipment.equipment[33].mods[0] = Dummy()
Equipment.equipment[33].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[33].mods[0].value_ = 1.008
Equipment.equipment[33].nations = []
Equipment.equipment[33].nations.insert(0, None)
Equipment.equipment[33].nations[0] = 'GB'.lower()
Equipment.equipment[33].nations.insert(1, None)
Equipment.equipment[33].nations[1] = 'Germany'.lower()
Equipment.equipment[33].nations.insert(2, None)
Equipment.equipment[33].nations[2] = 'USA'.lower()
Equipment.equipment[33].nations.insert(3, None)
Equipment.equipment[33].nations[3] = 'Japan'.lower()
Equipment.equipment[33].nations.insert(4, None)
Equipment.equipment[33].nations[4] = 'USSR'.lower()
Equipment.equipment[33].nations.insert(5, None)
Equipment.equipment[33].nations[5] = 'France'.lower()
Equipment.equipment[33].nations.insert(6, None)
Equipment.equipment[33].nations[6] = 'China'.lower()
Equipment.equipment[33].planeType = []
Equipment.equipment[33].planeType.insert(0, None)
Equipment.equipment[33].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[33].planeType.insert(1, None)
Equipment.equipment[33].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[33].tickets = 0
Equipment.equipment[33].uiIndex = 65
Equipment.equipment.insert(34, None)
Equipment.equipment[34] = Dummy()
Equipment.equipment[34].buyAvailable = true
Equipment.equipment[34].credits = 300000
Equipment.equipment[34].detachPrice = 10
Equipment.equipment[34].excludeList = []
Equipment.equipment[34].excludeList.insert(0, None)
Equipment.equipment[34].excludeList[0] = 1304
Equipment.equipment[34].excludeList.insert(1, None)
Equipment.equipment[34].excludeList[1] = 1399
Equipment.equipment[34].icoPath = 'icons/modules/equipGravityCenter.png'
Equipment.equipment[34].id = 35
Equipment.equipment[34].includeList = []
Equipment.equipment[34].isDiscount = false
Equipment.equipment[34].isNew = false
Equipment.equipment[34].localizeTag = 'GRAVITY_CENTER_III'
Equipment.equipment[34].mass = 0
Equipment.equipment[34].maxLevel = 8
Equipment.equipment[34].minLevel = 7
Equipment.equipment[34].mods = []
Equipment.equipment[34].mods.insert(0, None)
Equipment.equipment[34].mods[0] = Dummy()
Equipment.equipment[34].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[34].mods[0].value_ = 1.008
Equipment.equipment[34].nations = []
Equipment.equipment[34].nations.insert(0, None)
Equipment.equipment[34].nations[0] = 'GB'.lower()
Equipment.equipment[34].nations.insert(1, None)
Equipment.equipment[34].nations[1] = 'Germany'.lower()
Equipment.equipment[34].nations.insert(2, None)
Equipment.equipment[34].nations[2] = 'USA'.lower()
Equipment.equipment[34].nations.insert(3, None)
Equipment.equipment[34].nations[3] = 'Japan'.lower()
Equipment.equipment[34].nations.insert(4, None)
Equipment.equipment[34].nations[4] = 'USSR'.lower()
Equipment.equipment[34].nations.insert(5, None)
Equipment.equipment[34].nations[5] = 'France'.lower()
Equipment.equipment[34].nations.insert(6, None)
Equipment.equipment[34].nations[6] = 'China'.lower()
Equipment.equipment[34].planeType = []
Equipment.equipment[34].planeType.insert(0, None)
Equipment.equipment[34].planeType[0] = consts.PLANE_TYPE.NAVY
Equipment.equipment[34].planeType.insert(1, None)
Equipment.equipment[34].planeType[1] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[34].tickets = 0
Equipment.equipment[34].uiIndex = 66
Equipment.equipment.insert(35, None)
Equipment.equipment[35] = Dummy()
Equipment.equipment[35].buyAvailable = true
Equipment.equipment[35].credits = 400000
Equipment.equipment[35].detachPrice = 10
Equipment.equipment[35].excludeList = []
Equipment.equipment[35].excludeList.insert(0, None)
Equipment.equipment[35].excludeList[0] = 1304
Equipment.equipment[35].excludeList.insert(1, None)
Equipment.equipment[35].excludeList[1] = 1399
Equipment.equipment[35].icoPath = 'icons/modules/equipGravityCenter.png'
Equipment.equipment[35].id = 36
Equipment.equipment[35].includeList = []
Equipment.equipment[35].isDiscount = false
Equipment.equipment[35].isNew = false
Equipment.equipment[35].localizeTag = 'GRAVITY_CENTER_IV'
Equipment.equipment[35].mass = 0
Equipment.equipment[35].maxLevel = 10
Equipment.equipment[35].minLevel = 9
Equipment.equipment[35].mods = []
Equipment.equipment[35].mods.insert(0, None)
Equipment.equipment[35].mods[0] = Dummy()
Equipment.equipment[35].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[35].mods[0].value_ = 1.008
Equipment.equipment[35].nations = []
Equipment.equipment[35].nations.insert(0, None)
Equipment.equipment[35].nations[0] = 'GB'.lower()
Equipment.equipment[35].nations.insert(1, None)
Equipment.equipment[35].nations[1] = 'Germany'.lower()
Equipment.equipment[35].nations.insert(2, None)
Equipment.equipment[35].nations[2] = 'USA'.lower()
Equipment.equipment[35].nations.insert(3, None)
Equipment.equipment[35].nations[3] = 'Japan'.lower()
Equipment.equipment[35].nations.insert(4, None)
Equipment.equipment[35].nations[4] = 'USSR'.lower()
Equipment.equipment[35].nations.insert(5, None)
Equipment.equipment[35].nations[5] = 'France'.lower()
Equipment.equipment[35].nations.insert(6, None)
Equipment.equipment[35].nations[6] = 'China'.lower()
Equipment.equipment[35].planeType = []
Equipment.equipment[35].planeType.insert(0, None)
Equipment.equipment[35].planeType[0] = consts.PLANE_TYPE.NAVY
Equipment.equipment[35].planeType.insert(1, None)
Equipment.equipment[35].planeType[1] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[35].tickets = 0
Equipment.equipment[35].uiIndex = 67
Equipment.equipment.insert(36, None)
Equipment.equipment[36] = Dummy()
Equipment.equipment[36].buyAvailable = true
Equipment.equipment[36].credits = 150000
Equipment.equipment[36].detachPrice = 10
Equipment.equipment[36].excludeList = []
Equipment.equipment[36].excludeList.insert(0, None)
Equipment.equipment[36].excludeList[0] = 1304
Equipment.equipment[36].excludeList.insert(1, None)
Equipment.equipment[36].excludeList[1] = 1399
Equipment.equipment[36].icoPath = 'icons/modules/equipImprovedDope.png'
Equipment.equipment[36].id = 37
Equipment.equipment[36].includeList = []
Equipment.equipment[36].isDiscount = false
Equipment.equipment[36].isNew = false
Equipment.equipment[36].localizeTag = 'IMPROVED_DOPE_II'
Equipment.equipment[36].mass = 0
Equipment.equipment[36].maxLevel = 5
Equipment.equipment[36].minLevel = 4
Equipment.equipment[36].mods = []
Equipment.equipment[36].mods.insert(0, None)
Equipment.equipment[36].mods[0] = Dummy()
Equipment.equipment[36].mods[0].type = ModsTypeEnum.MAX_SPEED
Equipment.equipment[36].mods[0].value_ = 1.05
Equipment.equipment[36].mods.insert(1, None)
Equipment.equipment[36].mods[1] = Dummy()
Equipment.equipment[36].mods[1].type = ModsTypeEnum.DIVE_ACCELERATION
Equipment.equipment[36].mods[1].value_ = 1.25
Equipment.equipment[36].nations = []
Equipment.equipment[36].nations.insert(0, None)
Equipment.equipment[36].nations[0] = 'GB'.lower()
Equipment.equipment[36].nations.insert(1, None)
Equipment.equipment[36].nations[1] = 'Germany'.lower()
Equipment.equipment[36].nations.insert(2, None)
Equipment.equipment[36].nations[2] = 'USA'.lower()
Equipment.equipment[36].nations.insert(3, None)
Equipment.equipment[36].nations[3] = 'Japan'.lower()
Equipment.equipment[36].nations.insert(4, None)
Equipment.equipment[36].nations[4] = 'USSR'.lower()
Equipment.equipment[36].nations.insert(5, None)
Equipment.equipment[36].nations[5] = 'France'.lower()
Equipment.equipment[36].nations.insert(6, None)
Equipment.equipment[36].nations[6] = 'China'.lower()
Equipment.equipment[36].planeType = []
Equipment.equipment[36].planeType.insert(0, None)
Equipment.equipment[36].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[36].tickets = 0
Equipment.equipment[36].uiIndex = 43
Equipment.equipment.insert(37, None)
Equipment.equipment[37] = Dummy()
Equipment.equipment[37].buyAvailable = true
Equipment.equipment[37].credits = 300000
Equipment.equipment[37].detachPrice = 10
Equipment.equipment[37].excludeList = []
Equipment.equipment[37].excludeList.insert(0, None)
Equipment.equipment[37].excludeList[0] = 1304
Equipment.equipment[37].excludeList.insert(1, None)
Equipment.equipment[37].excludeList[1] = 1399
Equipment.equipment[37].icoPath = 'icons/modules/equipImprovedDope.png'
Equipment.equipment[37].id = 38
Equipment.equipment[37].includeList = []
Equipment.equipment[37].isDiscount = false
Equipment.equipment[37].isNew = false
Equipment.equipment[37].localizeTag = 'IMPROVED_DOPE_III'
Equipment.equipment[37].mass = 0
Equipment.equipment[37].maxLevel = 8
Equipment.equipment[37].minLevel = 6
Equipment.equipment[37].mods = []
Equipment.equipment[37].mods.insert(0, None)
Equipment.equipment[37].mods[0] = Dummy()
Equipment.equipment[37].mods[0].type = ModsTypeEnum.MAX_SPEED
Equipment.equipment[37].mods[0].value_ = 1.05
Equipment.equipment[37].mods.insert(1, None)
Equipment.equipment[37].mods[1] = Dummy()
Equipment.equipment[37].mods[1].type = ModsTypeEnum.DIVE_ACCELERATION
Equipment.equipment[37].mods[1].value_ = 1.25
Equipment.equipment[37].nations = []
Equipment.equipment[37].nations.insert(0, None)
Equipment.equipment[37].nations[0] = 'GB'.lower()
Equipment.equipment[37].nations.insert(1, None)
Equipment.equipment[37].nations[1] = 'Germany'.lower()
Equipment.equipment[37].nations.insert(2, None)
Equipment.equipment[37].nations[2] = 'USA'.lower()
Equipment.equipment[37].nations.insert(3, None)
Equipment.equipment[37].nations[3] = 'Japan'.lower()
Equipment.equipment[37].nations.insert(4, None)
Equipment.equipment[37].nations[4] = 'USSR'.lower()
Equipment.equipment[37].nations.insert(5, None)
Equipment.equipment[37].nations[5] = 'France'.lower()
Equipment.equipment[37].nations.insert(6, None)
Equipment.equipment[37].nations[6] = 'China'.lower()
Equipment.equipment[37].planeType = []
Equipment.equipment[37].planeType.insert(0, None)
Equipment.equipment[37].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[37].tickets = 0
Equipment.equipment[37].uiIndex = 44
Equipment.equipment.insert(38, None)
Equipment.equipment[38] = Dummy()
Equipment.equipment[38].buyAvailable = true
Equipment.equipment[38].credits = 400000
Equipment.equipment[38].detachPrice = 10
Equipment.equipment[38].excludeList = []
Equipment.equipment[38].excludeList.insert(0, None)
Equipment.equipment[38].excludeList[0] = 1304
Equipment.equipment[38].excludeList.insert(1, None)
Equipment.equipment[38].excludeList[1] = 1399
Equipment.equipment[38].icoPath = 'icons/modules/equipImprovedDope.png'
Equipment.equipment[38].id = 39
Equipment.equipment[38].includeList = []
Equipment.equipment[38].isDiscount = false
Equipment.equipment[38].isNew = false
Equipment.equipment[38].localizeTag = 'IMPROVED_DOPE_IV'
Equipment.equipment[38].mass = 0
Equipment.equipment[38].maxLevel = 10
Equipment.equipment[38].minLevel = 9
Equipment.equipment[38].mods = []
Equipment.equipment[38].mods.insert(0, None)
Equipment.equipment[38].mods[0] = Dummy()
Equipment.equipment[38].mods[0].type = ModsTypeEnum.MAX_SPEED
Equipment.equipment[38].mods[0].value_ = 1.05
Equipment.equipment[38].mods.insert(1, None)
Equipment.equipment[38].mods[1] = Dummy()
Equipment.equipment[38].mods[1].type = ModsTypeEnum.DIVE_ACCELERATION
Equipment.equipment[38].mods[1].value_ = 1.25
Equipment.equipment[38].nations = []
Equipment.equipment[38].nations.insert(0, None)
Equipment.equipment[38].nations[0] = 'GB'.lower()
Equipment.equipment[38].nations.insert(1, None)
Equipment.equipment[38].nations[1] = 'Germany'.lower()
Equipment.equipment[38].nations.insert(2, None)
Equipment.equipment[38].nations[2] = 'USA'.lower()
Equipment.equipment[38].nations.insert(3, None)
Equipment.equipment[38].nations[3] = 'Japan'.lower()
Equipment.equipment[38].nations.insert(4, None)
Equipment.equipment[38].nations[4] = 'USSR'.lower()
Equipment.equipment[38].nations.insert(5, None)
Equipment.equipment[38].nations[5] = 'France'.lower()
Equipment.equipment[38].nations.insert(6, None)
Equipment.equipment[38].nations[6] = 'China'.lower()
Equipment.equipment[38].planeType = []
Equipment.equipment[38].planeType.insert(0, None)
Equipment.equipment[38].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[38].tickets = 0
Equipment.equipment[38].uiIndex = 45
Equipment.equipment.insert(39, None)
Equipment.equipment[39] = Dummy()
Equipment.equipment[39].buyAvailable = true
Equipment.equipment[39].credits = 25000
Equipment.equipment[39].detachPrice = 10
Equipment.equipment[39].excludeList = []
Equipment.equipment[39].excludeList.insert(0, None)
Equipment.equipment[39].excludeList[0] = 1304
Equipment.equipment[39].excludeList.insert(1, None)
Equipment.equipment[39].excludeList[1] = 1399
Equipment.equipment[39].icoPath = 'icons/modules/equipImprovedCoating.png'
Equipment.equipment[39].id = 40
Equipment.equipment[39].includeList = []
Equipment.equipment[39].isDiscount = false
Equipment.equipment[39].isNew = false
Equipment.equipment[39].localizeTag = 'IMPROVED_COATING_I'
Equipment.equipment[39].mass = 5
Equipment.equipment[39].maxLevel = 3
Equipment.equipment[39].minLevel = 1
Equipment.equipment[39].mods = []
Equipment.equipment[39].mods.insert(0, None)
Equipment.equipment[39].mods[0] = Dummy()
Equipment.equipment[39].mods[0].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[39].mods[0].value_ = 0.8
Equipment.equipment[39].mods.insert(1, None)
Equipment.equipment[39].mods[1] = Dummy()
Equipment.equipment[39].mods[1].type = ModsTypeEnum.MAIN_HP
Equipment.equipment[39].mods[1].value_ = 1.05
Equipment.equipment[39].nations = []
Equipment.equipment[39].nations.insert(0, None)
Equipment.equipment[39].nations[0] = 'GB'.lower()
Equipment.equipment[39].nations.insert(1, None)
Equipment.equipment[39].nations[1] = 'Germany'.lower()
Equipment.equipment[39].nations.insert(2, None)
Equipment.equipment[39].nations[2] = 'USA'.lower()
Equipment.equipment[39].nations.insert(3, None)
Equipment.equipment[39].nations[3] = 'Japan'.lower()
Equipment.equipment[39].nations.insert(4, None)
Equipment.equipment[39].nations[4] = 'USSR'.lower()
Equipment.equipment[39].nations.insert(5, None)
Equipment.equipment[39].nations[5] = 'France'.lower()
Equipment.equipment[39].nations.insert(6, None)
Equipment.equipment[39].nations[6] = 'China'.lower()
Equipment.equipment[39].planeType = []
Equipment.equipment[39].tickets = 0
Equipment.equipment[39].uiIndex = 4
Equipment.equipment.insert(40, None)
Equipment.equipment[40] = Dummy()
Equipment.equipment[40].buyAvailable = true
Equipment.equipment[40].credits = 125000
Equipment.equipment[40].detachPrice = 10
Equipment.equipment[40].excludeList = []
Equipment.equipment[40].excludeList.insert(0, None)
Equipment.equipment[40].excludeList[0] = 1304
Equipment.equipment[40].excludeList.insert(1, None)
Equipment.equipment[40].excludeList[1] = 1399
Equipment.equipment[40].icoPath = 'icons/modules/equipImprovedCoating.png'
Equipment.equipment[40].id = 41
Equipment.equipment[40].includeList = []
Equipment.equipment[40].isDiscount = false
Equipment.equipment[40].isNew = false
Equipment.equipment[40].localizeTag = 'IMPROVED_COATING_II'
Equipment.equipment[40].mass = 10
Equipment.equipment[40].maxLevel = 6
Equipment.equipment[40].minLevel = 4
Equipment.equipment[40].mods = []
Equipment.equipment[40].mods.insert(0, None)
Equipment.equipment[40].mods[0] = Dummy()
Equipment.equipment[40].mods[0].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[40].mods[0].value_ = 0.8
Equipment.equipment[40].mods.insert(1, None)
Equipment.equipment[40].mods[1] = Dummy()
Equipment.equipment[40].mods[1].type = ModsTypeEnum.MAIN_HP
Equipment.equipment[40].mods[1].value_ = 1.05
Equipment.equipment[40].nations = []
Equipment.equipment[40].nations.insert(0, None)
Equipment.equipment[40].nations[0] = 'GB'.lower()
Equipment.equipment[40].nations.insert(1, None)
Equipment.equipment[40].nations[1] = 'Germany'.lower()
Equipment.equipment[40].nations.insert(2, None)
Equipment.equipment[40].nations[2] = 'USA'.lower()
Equipment.equipment[40].nations.insert(3, None)
Equipment.equipment[40].nations[3] = 'Japan'.lower()
Equipment.equipment[40].nations.insert(4, None)
Equipment.equipment[40].nations[4] = 'USSR'.lower()
Equipment.equipment[40].nations.insert(5, None)
Equipment.equipment[40].nations[5] = 'France'.lower()
Equipment.equipment[40].nations.insert(6, None)
Equipment.equipment[40].nations[6] = 'China'.lower()
Equipment.equipment[40].planeType = []
Equipment.equipment[40].tickets = 0
Equipment.equipment[40].uiIndex = 5
Equipment.equipment.insert(41, None)
Equipment.equipment[41] = Dummy()
Equipment.equipment[41].buyAvailable = true
Equipment.equipment[41].credits = 350000
Equipment.equipment[41].detachPrice = 10
Equipment.equipment[41].excludeList = []
Equipment.equipment[41].excludeList.insert(0, None)
Equipment.equipment[41].excludeList[0] = 1304
Equipment.equipment[41].excludeList.insert(1, None)
Equipment.equipment[41].excludeList[1] = 1399
Equipment.equipment[41].icoPath = 'icons/modules/equipImprovedCoating.png'
Equipment.equipment[41].id = 42
Equipment.equipment[41].includeList = []
Equipment.equipment[41].isDiscount = false
Equipment.equipment[41].isNew = false
Equipment.equipment[41].localizeTag = 'IMPROVED_COATING_III'
Equipment.equipment[41].mass = 25
Equipment.equipment[41].maxLevel = 8
Equipment.equipment[41].minLevel = 7
Equipment.equipment[41].mods = []
Equipment.equipment[41].mods.insert(0, None)
Equipment.equipment[41].mods[0] = Dummy()
Equipment.equipment[41].mods[0].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[41].mods[0].value_ = 0.8
Equipment.equipment[41].mods.insert(1, None)
Equipment.equipment[41].mods[1] = Dummy()
Equipment.equipment[41].mods[1].type = ModsTypeEnum.MAIN_HP
Equipment.equipment[41].mods[1].value_ = 1.05
Equipment.equipment[41].nations = []
Equipment.equipment[41].nations.insert(0, None)
Equipment.equipment[41].nations[0] = 'GB'.lower()
Equipment.equipment[41].nations.insert(1, None)
Equipment.equipment[41].nations[1] = 'Germany'.lower()
Equipment.equipment[41].nations.insert(2, None)
Equipment.equipment[41].nations[2] = 'USA'.lower()
Equipment.equipment[41].nations.insert(3, None)
Equipment.equipment[41].nations[3] = 'Japan'.lower()
Equipment.equipment[41].nations.insert(4, None)
Equipment.equipment[41].nations[4] = 'USSR'.lower()
Equipment.equipment[41].nations.insert(5, None)
Equipment.equipment[41].nations[5] = 'France'.lower()
Equipment.equipment[41].nations.insert(6, None)
Equipment.equipment[41].nations[6] = 'China'.lower()
Equipment.equipment[41].planeType = []
Equipment.equipment[41].tickets = 0
Equipment.equipment[41].uiIndex = 6
Equipment.equipment.insert(42, None)
Equipment.equipment[42] = Dummy()
Equipment.equipment[42].buyAvailable = true
Equipment.equipment[42].credits = 500000
Equipment.equipment[42].detachPrice = 10
Equipment.equipment[42].excludeList = []
Equipment.equipment[42].excludeList.insert(0, None)
Equipment.equipment[42].excludeList[0] = 1304
Equipment.equipment[42].excludeList.insert(1, None)
Equipment.equipment[42].excludeList[1] = 1399
Equipment.equipment[42].icoPath = 'icons/modules/equipImprovedCoating.png'
Equipment.equipment[42].id = 43
Equipment.equipment[42].includeList = []
Equipment.equipment[42].isDiscount = false
Equipment.equipment[42].isNew = false
Equipment.equipment[42].localizeTag = 'IMPROVED_COATING_IV'
Equipment.equipment[42].mass = 40
Equipment.equipment[42].maxLevel = 10
Equipment.equipment[42].minLevel = 9
Equipment.equipment[42].mods = []
Equipment.equipment[42].mods.insert(0, None)
Equipment.equipment[42].mods[0] = Dummy()
Equipment.equipment[42].mods[0].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[42].mods[0].value_ = 0.8
Equipment.equipment[42].mods.insert(1, None)
Equipment.equipment[42].mods[1] = Dummy()
Equipment.equipment[42].mods[1].type = ModsTypeEnum.MAIN_HP
Equipment.equipment[42].mods[1].value_ = 1.05
Equipment.equipment[42].nations = []
Equipment.equipment[42].nations.insert(0, None)
Equipment.equipment[42].nations[0] = 'GB'.lower()
Equipment.equipment[42].nations.insert(1, None)
Equipment.equipment[42].nations[1] = 'Germany'.lower()
Equipment.equipment[42].nations.insert(2, None)
Equipment.equipment[42].nations[2] = 'USA'.lower()
Equipment.equipment[42].nations.insert(3, None)
Equipment.equipment[42].nations[3] = 'Japan'.lower()
Equipment.equipment[42].nations.insert(4, None)
Equipment.equipment[42].nations[4] = 'USSR'.lower()
Equipment.equipment[42].nations.insert(5, None)
Equipment.equipment[42].nations[5] = 'France'.lower()
Equipment.equipment[42].nations.insert(6, None)
Equipment.equipment[42].nations[6] = 'China'.lower()
Equipment.equipment[42].planeType = []
Equipment.equipment[42].tickets = 0
Equipment.equipment[42].uiIndex = 7
Equipment.equipment.insert(43, None)
Equipment.equipment[43] = Dummy()
Equipment.equipment[43].buyAvailable = true
Equipment.equipment[43].credits = 15000
Equipment.equipment[43].detachPrice = 0
Equipment.equipment[43].excludeList = []
Equipment.equipment[43].excludeList.insert(0, None)
Equipment.equipment[43].excludeList[0] = 1304
Equipment.equipment[43].excludeList.insert(1, None)
Equipment.equipment[43].excludeList[1] = 1399
Equipment.equipment[43].excludeList.insert(2, None)
Equipment.equipment[43].excludeList[2] = 3893
Equipment.equipment[43].excludeList.insert(3, None)
Equipment.equipment[43].excludeList[3] = 5002
Equipment.equipment[43].excludeList.insert(4, None)
Equipment.equipment[43].excludeList[4] = 1504
Equipment.equipment[43].excludeList.insert(5, None)
Equipment.equipment[43].excludeList[5] = 1605
Equipment.equipment[43].excludeList.insert(6, None)
Equipment.equipment[43].excludeList[6] = 1403
Equipment.equipment[43].excludeList.insert(7, None)
Equipment.equipment[43].excludeList[7] = 2603
Equipment.equipment[43].excludeList.insert(8, None)
Equipment.equipment[43].excludeList[8] = 2705
Equipment.equipment[43].excludeList.insert(9, None)
Equipment.equipment[43].excludeList[9] = 2892
Equipment.equipment[43].excludeList.insert(10, None)
Equipment.equipment[43].excludeList[10] = 1098
Equipment.equipment[43].excludeList.insert(11, None)
Equipment.equipment[43].excludeList[11] = 2202
Equipment.equipment[43].excludeList.insert(12, None)
Equipment.equipment[43].excludeList[12] = 2204
Equipment.equipment[43].excludeList.insert(13, None)
Equipment.equipment[43].excludeList[13] = 2596
Equipment.equipment[43].excludeList.insert(14, None)
Equipment.equipment[43].excludeList[14] = 5504
Equipment.equipment[43].icoPath = 'icons/modules/equipBetterAttackSight.png'
Equipment.equipment[43].id = 44
Equipment.equipment[43].includeList = []
Equipment.equipment[43].isDiscount = false
Equipment.equipment[43].isNew = false
Equipment.equipment[43].localizeTag = 'BOMB_SIGHT_I'
Equipment.equipment[43].mass = 0
Equipment.equipment[43].maxLevel = 3
Equipment.equipment[43].minLevel = 1
Equipment.equipment[43].mods = []
Equipment.equipment[43].mods.insert(0, None)
Equipment.equipment[43].mods[0] = Dummy()
Equipment.equipment[43].mods[0].type = ModsTypeEnum.BOMB_MISSILE_FOCUS
Equipment.equipment[43].mods[0].value_ = 2.0
Equipment.equipment[43].nations = []
Equipment.equipment[43].nations.insert(0, None)
Equipment.equipment[43].nations[0] = 'GB'.lower()
Equipment.equipment[43].nations.insert(1, None)
Equipment.equipment[43].nations[1] = 'Germany'.lower()
Equipment.equipment[43].nations.insert(2, None)
Equipment.equipment[43].nations[2] = 'USA'.lower()
Equipment.equipment[43].nations.insert(3, None)
Equipment.equipment[43].nations[3] = 'Japan'.lower()
Equipment.equipment[43].nations.insert(4, None)
Equipment.equipment[43].nations[4] = 'USSR'.lower()
Equipment.equipment[43].nations.insert(5, None)
Equipment.equipment[43].nations[5] = 'France'.lower()
Equipment.equipment[43].nations.insert(6, None)
Equipment.equipment[43].nations[6] = 'China'.lower()
Equipment.equipment[43].planeType = []
Equipment.equipment[43].planeType.insert(0, None)
Equipment.equipment[43].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[43].planeType.insert(1, None)
Equipment.equipment[43].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[43].planeType.insert(2, None)
Equipment.equipment[43].planeType[2] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[43].tickets = 0
Equipment.equipment[43].uiIndex = 31
Equipment.equipment.insert(44, None)
Equipment.equipment[44] = Dummy()
Equipment.equipment[44].buyAvailable = true
Equipment.equipment[44].credits = 100000
Equipment.equipment[44].detachPrice = 0
Equipment.equipment[44].excludeList = []
Equipment.equipment[44].excludeList.insert(0, None)
Equipment.equipment[44].excludeList[0] = 1304
Equipment.equipment[44].excludeList.insert(1, None)
Equipment.equipment[44].excludeList[1] = 1399
Equipment.equipment[44].excludeList.insert(2, None)
Equipment.equipment[44].excludeList[2] = 3893
Equipment.equipment[44].excludeList.insert(3, None)
Equipment.equipment[44].excludeList[3] = 5002
Equipment.equipment[44].excludeList.insert(4, None)
Equipment.equipment[44].excludeList[4] = 1504
Equipment.equipment[44].excludeList.insert(5, None)
Equipment.equipment[44].excludeList[5] = 1605
Equipment.equipment[44].excludeList.insert(6, None)
Equipment.equipment[44].excludeList[6] = 1403
Equipment.equipment[44].excludeList.insert(7, None)
Equipment.equipment[44].excludeList[7] = 2603
Equipment.equipment[44].excludeList.insert(8, None)
Equipment.equipment[44].excludeList[8] = 2705
Equipment.equipment[44].excludeList.insert(9, None)
Equipment.equipment[44].excludeList[9] = 2892
Equipment.equipment[44].excludeList.insert(10, None)
Equipment.equipment[44].excludeList[10] = 1098
Equipment.equipment[44].excludeList.insert(11, None)
Equipment.equipment[44].excludeList[11] = 2202
Equipment.equipment[44].excludeList.insert(12, None)
Equipment.equipment[44].excludeList[12] = 2204
Equipment.equipment[44].excludeList.insert(13, None)
Equipment.equipment[44].excludeList[13] = 2596
Equipment.equipment[44].excludeList.insert(14, None)
Equipment.equipment[44].excludeList[14] = 5504
Equipment.equipment[44].excludeList.insert(15, None)
Equipment.equipment[44].excludeList[15] = 7592
Equipment.equipment[44].icoPath = 'icons/modules/equipBetterAttackSight.png'
Equipment.equipment[44].id = 45
Equipment.equipment[44].includeList = []
Equipment.equipment[44].isDiscount = false
Equipment.equipment[44].isNew = false
Equipment.equipment[44].localizeTag = 'BOMB_SIGHT_II'
Equipment.equipment[44].mass = 0
Equipment.equipment[44].maxLevel = 6
Equipment.equipment[44].minLevel = 4
Equipment.equipment[44].mods = []
Equipment.equipment[44].mods.insert(0, None)
Equipment.equipment[44].mods[0] = Dummy()
Equipment.equipment[44].mods[0].type = ModsTypeEnum.BOMB_MISSILE_FOCUS
Equipment.equipment[44].mods[0].value_ = 2.0
Equipment.equipment[44].nations = []
Equipment.equipment[44].nations.insert(0, None)
Equipment.equipment[44].nations[0] = 'GB'.lower()
Equipment.equipment[44].nations.insert(1, None)
Equipment.equipment[44].nations[1] = 'Germany'.lower()
Equipment.equipment[44].nations.insert(2, None)
Equipment.equipment[44].nations[2] = 'USA'.lower()
Equipment.equipment[44].nations.insert(3, None)
Equipment.equipment[44].nations[3] = 'Japan'.lower()
Equipment.equipment[44].nations.insert(4, None)
Equipment.equipment[44].nations[4] = 'USSR'.lower()
Equipment.equipment[44].nations.insert(5, None)
Equipment.equipment[44].nations[5] = 'France'.lower()
Equipment.equipment[44].nations.insert(6, None)
Equipment.equipment[44].nations[6] = 'China'.lower()
Equipment.equipment[44].planeType = []
Equipment.equipment[44].planeType.insert(0, None)
Equipment.equipment[44].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[44].planeType.insert(1, None)
Equipment.equipment[44].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[44].planeType.insert(2, None)
Equipment.equipment[44].planeType[2] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[44].tickets = 0
Equipment.equipment[44].uiIndex = 32
Equipment.equipment.insert(45, None)
Equipment.equipment[45] = Dummy()
Equipment.equipment[45].buyAvailable = true
Equipment.equipment[45].credits = 200000
Equipment.equipment[45].detachPrice = 0
Equipment.equipment[45].excludeList = []
Equipment.equipment[45].excludeList.insert(0, None)
Equipment.equipment[45].excludeList[0] = 1304
Equipment.equipment[45].excludeList.insert(1, None)
Equipment.equipment[45].excludeList[1] = 1399
Equipment.equipment[45].excludeList.insert(2, None)
Equipment.equipment[45].excludeList[2] = 3893
Equipment.equipment[45].excludeList.insert(3, None)
Equipment.equipment[45].excludeList[3] = 5002
Equipment.equipment[45].excludeList.insert(4, None)
Equipment.equipment[45].excludeList[4] = 1504
Equipment.equipment[45].excludeList.insert(5, None)
Equipment.equipment[45].excludeList[5] = 1605
Equipment.equipment[45].excludeList.insert(6, None)
Equipment.equipment[45].excludeList[6] = 1403
Equipment.equipment[45].excludeList.insert(7, None)
Equipment.equipment[45].excludeList[7] = 2603
Equipment.equipment[45].excludeList.insert(8, None)
Equipment.equipment[45].excludeList[8] = 2705
Equipment.equipment[45].excludeList.insert(9, None)
Equipment.equipment[45].excludeList[9] = 2892
Equipment.equipment[45].excludeList.insert(10, None)
Equipment.equipment[45].excludeList[10] = 1098
Equipment.equipment[45].excludeList.insert(11, None)
Equipment.equipment[45].excludeList[11] = 2202
Equipment.equipment[45].excludeList.insert(12, None)
Equipment.equipment[45].excludeList[12] = 2204
Equipment.equipment[45].excludeList.insert(13, None)
Equipment.equipment[45].excludeList[13] = 2596
Equipment.equipment[45].excludeList.insert(14, None)
Equipment.equipment[45].excludeList[14] = 5504
Equipment.equipment[45].excludeList.insert(15, None)
Equipment.equipment[45].excludeList[15] = 7791
Equipment.equipment[45].icoPath = 'icons/modules/equipBetterAttackSight.png'
Equipment.equipment[45].id = 46
Equipment.equipment[45].includeList = []
Equipment.equipment[45].isDiscount = false
Equipment.equipment[45].isNew = false
Equipment.equipment[45].localizeTag = 'BOMB_SIGHT_III'
Equipment.equipment[45].mass = 0
Equipment.equipment[45].maxLevel = 8
Equipment.equipment[45].minLevel = 7
Equipment.equipment[45].mods = []
Equipment.equipment[45].mods.insert(0, None)
Equipment.equipment[45].mods[0] = Dummy()
Equipment.equipment[45].mods[0].type = ModsTypeEnum.BOMB_MISSILE_FOCUS
Equipment.equipment[45].mods[0].value_ = 2.0
Equipment.equipment[45].nations = []
Equipment.equipment[45].nations.insert(0, None)
Equipment.equipment[45].nations[0] = 'GB'.lower()
Equipment.equipment[45].nations.insert(1, None)
Equipment.equipment[45].nations[1] = 'Germany'.lower()
Equipment.equipment[45].nations.insert(2, None)
Equipment.equipment[45].nations[2] = 'USA'.lower()
Equipment.equipment[45].nations.insert(3, None)
Equipment.equipment[45].nations[3] = 'Japan'.lower()
Equipment.equipment[45].nations.insert(4, None)
Equipment.equipment[45].nations[4] = 'USSR'.lower()
Equipment.equipment[45].nations.insert(5, None)
Equipment.equipment[45].nations[5] = 'France'.lower()
Equipment.equipment[45].nations.insert(6, None)
Equipment.equipment[45].nations[6] = 'China'.lower()
Equipment.equipment[45].planeType = []
Equipment.equipment[45].planeType.insert(0, None)
Equipment.equipment[45].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[45].planeType.insert(1, None)
Equipment.equipment[45].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[45].planeType.insert(2, None)
Equipment.equipment[45].planeType[2] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[45].tickets = 0
Equipment.equipment[45].uiIndex = 33
Equipment.equipment.insert(46, None)
Equipment.equipment[46] = Dummy()
Equipment.equipment[46].buyAvailable = true
Equipment.equipment[46].credits = 300000
Equipment.equipment[46].detachPrice = 0
Equipment.equipment[46].excludeList = []
Equipment.equipment[46].excludeList.insert(0, None)
Equipment.equipment[46].excludeList[0] = 1304
Equipment.equipment[46].excludeList.insert(1, None)
Equipment.equipment[46].excludeList[1] = 1399
Equipment.equipment[46].excludeList.insert(2, None)
Equipment.equipment[46].excludeList[2] = 3893
Equipment.equipment[46].excludeList.insert(3, None)
Equipment.equipment[46].excludeList[3] = 5002
Equipment.equipment[46].excludeList.insert(4, None)
Equipment.equipment[46].excludeList[4] = 1504
Equipment.equipment[46].excludeList.insert(5, None)
Equipment.equipment[46].excludeList[5] = 1605
Equipment.equipment[46].excludeList.insert(6, None)
Equipment.equipment[46].excludeList[6] = 1403
Equipment.equipment[46].excludeList.insert(7, None)
Equipment.equipment[46].excludeList[7] = 2603
Equipment.equipment[46].excludeList.insert(8, None)
Equipment.equipment[46].excludeList[8] = 2705
Equipment.equipment[46].excludeList.insert(9, None)
Equipment.equipment[46].excludeList[9] = 2892
Equipment.equipment[46].excludeList.insert(10, None)
Equipment.equipment[46].excludeList[10] = 1098
Equipment.equipment[46].excludeList.insert(11, None)
Equipment.equipment[46].excludeList[11] = 2202
Equipment.equipment[46].excludeList.insert(12, None)
Equipment.equipment[46].excludeList[12] = 2204
Equipment.equipment[46].excludeList.insert(13, None)
Equipment.equipment[46].excludeList[13] = 2596
Equipment.equipment[46].excludeList.insert(14, None)
Equipment.equipment[46].excludeList[14] = 5504
Equipment.equipment[46].icoPath = 'icons/modules/equipBetterAttackSight.png'
Equipment.equipment[46].id = 47
Equipment.equipment[46].includeList = []
Equipment.equipment[46].isDiscount = false
Equipment.equipment[46].isNew = false
Equipment.equipment[46].localizeTag = 'BOMB_SIGHT_IV'
Equipment.equipment[46].mass = 0
Equipment.equipment[46].maxLevel = 10
Equipment.equipment[46].minLevel = 9
Equipment.equipment[46].mods = []
Equipment.equipment[46].mods.insert(0, None)
Equipment.equipment[46].mods[0] = Dummy()
Equipment.equipment[46].mods[0].type = ModsTypeEnum.BOMB_MISSILE_FOCUS
Equipment.equipment[46].mods[0].value_ = 2.0
Equipment.equipment[46].nations = []
Equipment.equipment[46].nations.insert(0, None)
Equipment.equipment[46].nations[0] = 'GB'.lower()
Equipment.equipment[46].nations.insert(1, None)
Equipment.equipment[46].nations[1] = 'Germany'.lower()
Equipment.equipment[46].nations.insert(2, None)
Equipment.equipment[46].nations[2] = 'USA'.lower()
Equipment.equipment[46].nations.insert(3, None)
Equipment.equipment[46].nations[3] = 'Japan'.lower()
Equipment.equipment[46].nations.insert(4, None)
Equipment.equipment[46].nations[4] = 'USSR'.lower()
Equipment.equipment[46].nations.insert(5, None)
Equipment.equipment[46].nations[5] = 'France'.lower()
Equipment.equipment[46].nations.insert(6, None)
Equipment.equipment[46].nations[6] = 'China'.lower()
Equipment.equipment[46].planeType = []
Equipment.equipment[46].planeType.insert(0, None)
Equipment.equipment[46].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[46].planeType.insert(1, None)
Equipment.equipment[46].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[46].planeType.insert(2, None)
Equipment.equipment[46].planeType[2] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[46].tickets = 0
Equipment.equipment[46].uiIndex = 34
Equipment.equipment.insert(47, None)
Equipment.equipment[47] = Dummy()
Equipment.equipment[47].buyAvailable = true
Equipment.equipment[47].credits = 30000
Equipment.equipment[47].detachPrice = 10
Equipment.equipment[47].excludeList = []
Equipment.equipment[47].excludeList.insert(0, None)
Equipment.equipment[47].excludeList[0] = 1304
Equipment.equipment[47].excludeList.insert(1, None)
Equipment.equipment[47].excludeList[1] = 1399
Equipment.equipment[47].icoPath = 'icons/modules/equipLightConstruction.png'
Equipment.equipment[47].id = 48
Equipment.equipment[47].includeList = []
Equipment.equipment[47].isDiscount = false
Equipment.equipment[47].isNew = false
Equipment.equipment[47].localizeTag = 'LIGHT_HULL_I'
Equipment.equipment[47].mass = 0
Equipment.equipment[47].maxLevel = 3
Equipment.equipment[47].minLevel = 1
Equipment.equipment[47].mods = []
Equipment.equipment[47].mods.insert(0, None)
Equipment.equipment[47].mods[0] = Dummy()
Equipment.equipment[47].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[47].mods[0].value_ = 1.007
Equipment.equipment[47].mods.insert(1, None)
Equipment.equipment[47].mods[1] = Dummy()
Equipment.equipment[47].mods[1].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Equipment.equipment[47].mods[1].value_ = 1.03
Equipment.equipment[47].mods.insert(2, None)
Equipment.equipment[47].mods[2] = Dummy()
Equipment.equipment[47].mods[2].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Equipment.equipment[47].mods[2].value_ = 1.02
Equipment.equipment[47].nations = []
Equipment.equipment[47].nations.insert(0, None)
Equipment.equipment[47].nations[0] = 'GB'.lower()
Equipment.equipment[47].nations.insert(1, None)
Equipment.equipment[47].nations[1] = 'Germany'.lower()
Equipment.equipment[47].nations.insert(2, None)
Equipment.equipment[47].nations[2] = 'USA'.lower()
Equipment.equipment[47].nations.insert(3, None)
Equipment.equipment[47].nations[3] = 'Japan'.lower()
Equipment.equipment[47].nations.insert(4, None)
Equipment.equipment[47].nations[4] = 'USSR'.lower()
Equipment.equipment[47].nations.insert(5, None)
Equipment.equipment[47].nations[5] = 'France'.lower()
Equipment.equipment[47].nations.insert(6, None)
Equipment.equipment[47].nations[6] = 'China'.lower()
Equipment.equipment[47].planeType = []
Equipment.equipment[47].planeType.insert(0, None)
Equipment.equipment[47].planeType[0] = consts.PLANE_TYPE.NAVY
Equipment.equipment[47].planeType.insert(1, None)
Equipment.equipment[47].planeType[1] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[47].tickets = 0
Equipment.equipment[47].uiIndex = 60
Equipment.equipment.insert(48, None)
Equipment.equipment[48] = Dummy()
Equipment.equipment[48].buyAvailable = true
Equipment.equipment[48].credits = 200000
Equipment.equipment[48].detachPrice = 10
Equipment.equipment[48].excludeList = []
Equipment.equipment[48].excludeList.insert(0, None)
Equipment.equipment[48].excludeList[0] = 1304
Equipment.equipment[48].excludeList.insert(1, None)
Equipment.equipment[48].excludeList[1] = 1399
Equipment.equipment[48].icoPath = 'icons/modules/equipLightConstruction.png'
Equipment.equipment[48].id = 49
Equipment.equipment[48].includeList = []
Equipment.equipment[48].isDiscount = false
Equipment.equipment[48].isNew = false
Equipment.equipment[48].localizeTag = 'LIGHT_HULL_II'
Equipment.equipment[48].mass = 0
Equipment.equipment[48].maxLevel = 6
Equipment.equipment[48].minLevel = 4
Equipment.equipment[48].mods = []
Equipment.equipment[48].mods.insert(0, None)
Equipment.equipment[48].mods[0] = Dummy()
Equipment.equipment[48].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[48].mods[0].value_ = 1.007
Equipment.equipment[48].mods.insert(1, None)
Equipment.equipment[48].mods[1] = Dummy()
Equipment.equipment[48].mods[1].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Equipment.equipment[48].mods[1].value_ = 1.03
Equipment.equipment[48].mods.insert(2, None)
Equipment.equipment[48].mods[2] = Dummy()
Equipment.equipment[48].mods[2].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Equipment.equipment[48].mods[2].value_ = 1.02
Equipment.equipment[48].nations = []
Equipment.equipment[48].nations.insert(0, None)
Equipment.equipment[48].nations[0] = 'GB'.lower()
Equipment.equipment[48].nations.insert(1, None)
Equipment.equipment[48].nations[1] = 'Germany'.lower()
Equipment.equipment[48].nations.insert(2, None)
Equipment.equipment[48].nations[2] = 'USA'.lower()
Equipment.equipment[48].nations.insert(3, None)
Equipment.equipment[48].nations[3] = 'Japan'.lower()
Equipment.equipment[48].nations.insert(4, None)
Equipment.equipment[48].nations[4] = 'USSR'.lower()
Equipment.equipment[48].nations.insert(5, None)
Equipment.equipment[48].nations[5] = 'France'.lower()
Equipment.equipment[48].nations.insert(6, None)
Equipment.equipment[48].nations[6] = 'China'.lower()
Equipment.equipment[48].planeType = []
Equipment.equipment[48].planeType.insert(0, None)
Equipment.equipment[48].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[48].planeType.insert(1, None)
Equipment.equipment[48].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[48].tickets = 0
Equipment.equipment[48].uiIndex = 61
Equipment.equipment.insert(49, None)
Equipment.equipment[49] = Dummy()
Equipment.equipment[49].buyAvailable = true
Equipment.equipment[49].credits = 400000
Equipment.equipment[49].detachPrice = 10
Equipment.equipment[49].excludeList = []
Equipment.equipment[49].excludeList.insert(0, None)
Equipment.equipment[49].excludeList[0] = 1304
Equipment.equipment[49].excludeList.insert(1, None)
Equipment.equipment[49].excludeList[1] = 1399
Equipment.equipment[49].icoPath = 'icons/modules/equipLightConstruction.png'
Equipment.equipment[49].id = 50
Equipment.equipment[49].includeList = []
Equipment.equipment[49].isDiscount = false
Equipment.equipment[49].isNew = false
Equipment.equipment[49].localizeTag = 'LIGHT_HULL_III'
Equipment.equipment[49].mass = 0
Equipment.equipment[49].maxLevel = 8
Equipment.equipment[49].minLevel = 7
Equipment.equipment[49].mods = []
Equipment.equipment[49].mods.insert(0, None)
Equipment.equipment[49].mods[0] = Dummy()
Equipment.equipment[49].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[49].mods[0].value_ = 1.007
Equipment.equipment[49].mods.insert(1, None)
Equipment.equipment[49].mods[1] = Dummy()
Equipment.equipment[49].mods[1].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Equipment.equipment[49].mods[1].value_ = 1.03
Equipment.equipment[49].mods.insert(2, None)
Equipment.equipment[49].mods[2] = Dummy()
Equipment.equipment[49].mods[2].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Equipment.equipment[49].mods[2].value_ = 1.02
Equipment.equipment[49].nations = []
Equipment.equipment[49].nations.insert(0, None)
Equipment.equipment[49].nations[0] = 'GB'.lower()
Equipment.equipment[49].nations.insert(1, None)
Equipment.equipment[49].nations[1] = 'Germany'.lower()
Equipment.equipment[49].nations.insert(2, None)
Equipment.equipment[49].nations[2] = 'USA'.lower()
Equipment.equipment[49].nations.insert(3, None)
Equipment.equipment[49].nations[3] = 'Japan'.lower()
Equipment.equipment[49].nations.insert(4, None)
Equipment.equipment[49].nations[4] = 'USSR'.lower()
Equipment.equipment[49].nations.insert(5, None)
Equipment.equipment[49].nations[5] = 'France'.lower()
Equipment.equipment[49].nations.insert(6, None)
Equipment.equipment[49].nations[6] = 'China'.lower()
Equipment.equipment[49].planeType = []
Equipment.equipment[49].planeType.insert(0, None)
Equipment.equipment[49].planeType[0] = consts.PLANE_TYPE.NAVY
Equipment.equipment[49].planeType.insert(1, None)
Equipment.equipment[49].planeType[1] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[49].tickets = 0
Equipment.equipment[49].uiIndex = 62
Equipment.equipment.insert(50, None)
Equipment.equipment[50] = Dummy()
Equipment.equipment[50].buyAvailable = true
Equipment.equipment[50].credits = 550000
Equipment.equipment[50].detachPrice = 10
Equipment.equipment[50].excludeList = []
Equipment.equipment[50].excludeList.insert(0, None)
Equipment.equipment[50].excludeList[0] = 1304
Equipment.equipment[50].excludeList.insert(1, None)
Equipment.equipment[50].excludeList[1] = 1399
Equipment.equipment[50].icoPath = 'icons/modules/equipLightConstruction.png'
Equipment.equipment[50].id = 51
Equipment.equipment[50].includeList = []
Equipment.equipment[50].isDiscount = false
Equipment.equipment[50].isNew = false
Equipment.equipment[50].localizeTag = 'LIGHT_HULL_IV'
Equipment.equipment[50].mass = 0
Equipment.equipment[50].maxLevel = 10
Equipment.equipment[50].minLevel = 9
Equipment.equipment[50].mods = []
Equipment.equipment[50].mods.insert(0, None)
Equipment.equipment[50].mods[0] = Dummy()
Equipment.equipment[50].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Equipment.equipment[50].mods[0].value_ = 1.007
Equipment.equipment[50].mods.insert(1, None)
Equipment.equipment[50].mods[1] = Dummy()
Equipment.equipment[50].mods[1].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Equipment.equipment[50].mods[1].value_ = 1.03
Equipment.equipment[50].mods.insert(2, None)
Equipment.equipment[50].mods[2] = Dummy()
Equipment.equipment[50].mods[2].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Equipment.equipment[50].mods[2].value_ = 1.02
Equipment.equipment[50].nations = []
Equipment.equipment[50].nations.insert(0, None)
Equipment.equipment[50].nations[0] = 'GB'.lower()
Equipment.equipment[50].nations.insert(1, None)
Equipment.equipment[50].nations[1] = 'Germany'.lower()
Equipment.equipment[50].nations.insert(2, None)
Equipment.equipment[50].nations[2] = 'USA'.lower()
Equipment.equipment[50].nations.insert(3, None)
Equipment.equipment[50].nations[3] = 'Japan'.lower()
Equipment.equipment[50].nations.insert(4, None)
Equipment.equipment[50].nations[4] = 'USSR'.lower()
Equipment.equipment[50].nations.insert(5, None)
Equipment.equipment[50].nations[5] = 'France'.lower()
Equipment.equipment[50].nations.insert(6, None)
Equipment.equipment[50].nations[6] = 'China'.lower()
Equipment.equipment[50].planeType = []
Equipment.equipment[50].planeType.insert(0, None)
Equipment.equipment[50].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[50].planeType.insert(1, None)
Equipment.equipment[50].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[50].tickets = 0
Equipment.equipment[50].uiIndex = 63
Equipment.equipment.insert(51, None)
Equipment.equipment[51] = Dummy()
Equipment.equipment[51].buyAvailable = true
Equipment.equipment[51].credits = 15000
Equipment.equipment[51].detachPrice = 0
Equipment.equipment[51].excludeList = []
Equipment.equipment[51].excludeList.insert(0, None)
Equipment.equipment[51].excludeList[0] = 1304
Equipment.equipment[51].excludeList.insert(1, None)
Equipment.equipment[51].excludeList[1] = 1399
Equipment.equipment[51].icoPath = 'icons/modules/equipBetterRadiator.png'
Equipment.equipment[51].id = 52
Equipment.equipment[51].includeList = []
Equipment.equipment[51].isDiscount = false
Equipment.equipment[51].isNew = false
Equipment.equipment[51].localizeTag = 'IMPROVED_RAD_I'
Equipment.equipment[51].mass = 0
Equipment.equipment[51].maxLevel = 3
Equipment.equipment[51].minLevel = 1
Equipment.equipment[51].mods = []
Equipment.equipment[51].mods.insert(0, None)
Equipment.equipment[51].mods[0] = Dummy()
Equipment.equipment[51].mods[0].type = ModsTypeEnum.FAST_ENGINE_COOLING
Equipment.equipment[51].mods[0].value_ = 1.43
Equipment.equipment[51].nations = []
Equipment.equipment[51].nations.insert(0, None)
Equipment.equipment[51].nations[0] = 'GB'.lower()
Equipment.equipment[51].nations.insert(1, None)
Equipment.equipment[51].nations[1] = 'Germany'.lower()
Equipment.equipment[51].nations.insert(2, None)
Equipment.equipment[51].nations[2] = 'USA'.lower()
Equipment.equipment[51].nations.insert(3, None)
Equipment.equipment[51].nations[3] = 'Japan'.lower()
Equipment.equipment[51].nations.insert(4, None)
Equipment.equipment[51].nations[4] = 'USSR'.lower()
Equipment.equipment[51].nations.insert(5, None)
Equipment.equipment[51].nations[5] = 'France'.lower()
Equipment.equipment[51].nations.insert(6, None)
Equipment.equipment[51].nations[6] = 'China'.lower()
Equipment.equipment[51].planeType = []
Equipment.equipment[51].planeType.insert(0, None)
Equipment.equipment[51].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[51].planeType.insert(1, None)
Equipment.equipment[51].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[51].tickets = 0
Equipment.equipment[51].uiIndex = 53
Equipment.equipment.insert(52, None)
Equipment.equipment[52] = Dummy()
Equipment.equipment[52].buyAvailable = true
Equipment.equipment[52].credits = 100000
Equipment.equipment[52].detachPrice = 0
Equipment.equipment[52].excludeList = []
Equipment.equipment[52].excludeList.insert(0, None)
Equipment.equipment[52].excludeList[0] = 1304
Equipment.equipment[52].excludeList.insert(1, None)
Equipment.equipment[52].excludeList[1] = 1399
Equipment.equipment[52].icoPath = 'icons/modules/equipBetterRadiator.png'
Equipment.equipment[52].id = 53
Equipment.equipment[52].includeList = []
Equipment.equipment[52].isDiscount = false
Equipment.equipment[52].isNew = false
Equipment.equipment[52].localizeTag = 'IMPROVED_RAD_II'
Equipment.equipment[52].mass = 0
Equipment.equipment[52].maxLevel = 6
Equipment.equipment[52].minLevel = 4
Equipment.equipment[52].mods = []
Equipment.equipment[52].mods.insert(0, None)
Equipment.equipment[52].mods[0] = Dummy()
Equipment.equipment[52].mods[0].type = ModsTypeEnum.FAST_ENGINE_COOLING
Equipment.equipment[52].mods[0].value_ = 1.43
Equipment.equipment[52].nations = []
Equipment.equipment[52].nations.insert(0, None)
Equipment.equipment[52].nations[0] = 'GB'.lower()
Equipment.equipment[52].nations.insert(1, None)
Equipment.equipment[52].nations[1] = 'Germany'.lower()
Equipment.equipment[52].nations.insert(2, None)
Equipment.equipment[52].nations[2] = 'USA'.lower()
Equipment.equipment[52].nations.insert(3, None)
Equipment.equipment[52].nations[3] = 'Japan'.lower()
Equipment.equipment[52].nations.insert(4, None)
Equipment.equipment[52].nations[4] = 'USSR'.lower()
Equipment.equipment[52].nations.insert(5, None)
Equipment.equipment[52].nations[5] = 'France'.lower()
Equipment.equipment[52].nations.insert(6, None)
Equipment.equipment[52].nations[6] = 'China'.lower()
Equipment.equipment[52].planeType = []
Equipment.equipment[52].planeType.insert(0, None)
Equipment.equipment[52].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[52].planeType.insert(1, None)
Equipment.equipment[52].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[52].tickets = 0
Equipment.equipment[52].uiIndex = 54
Equipment.equipment.insert(53, None)
Equipment.equipment[53] = Dummy()
Equipment.equipment[53].buyAvailable = true
Equipment.equipment[53].credits = 200000
Equipment.equipment[53].detachPrice = 0
Equipment.equipment[53].excludeList = []
Equipment.equipment[53].excludeList.insert(0, None)
Equipment.equipment[53].excludeList[0] = 1304
Equipment.equipment[53].excludeList.insert(1, None)
Equipment.equipment[53].excludeList[1] = 1399
Equipment.equipment[53].icoPath = 'icons/modules/equipBetterRadiator.png'
Equipment.equipment[53].id = 54
Equipment.equipment[53].includeList = []
Equipment.equipment[53].isDiscount = false
Equipment.equipment[53].isNew = false
Equipment.equipment[53].localizeTag = 'IMPROVED_RAD_III'
Equipment.equipment[53].mass = 0
Equipment.equipment[53].maxLevel = 8
Equipment.equipment[53].minLevel = 7
Equipment.equipment[53].mods = []
Equipment.equipment[53].mods.insert(0, None)
Equipment.equipment[53].mods[0] = Dummy()
Equipment.equipment[53].mods[0].type = ModsTypeEnum.FAST_ENGINE_COOLING
Equipment.equipment[53].mods[0].value_ = 1.43
Equipment.equipment[53].nations = []
Equipment.equipment[53].nations.insert(0, None)
Equipment.equipment[53].nations[0] = 'GB'.lower()
Equipment.equipment[53].nations.insert(1, None)
Equipment.equipment[53].nations[1] = 'Germany'.lower()
Equipment.equipment[53].nations.insert(2, None)
Equipment.equipment[53].nations[2] = 'USA'.lower()
Equipment.equipment[53].nations.insert(3, None)
Equipment.equipment[53].nations[3] = 'Japan'.lower()
Equipment.equipment[53].nations.insert(4, None)
Equipment.equipment[53].nations[4] = 'USSR'.lower()
Equipment.equipment[53].nations.insert(5, None)
Equipment.equipment[53].nations[5] = 'France'.lower()
Equipment.equipment[53].nations.insert(6, None)
Equipment.equipment[53].nations[6] = 'China'.lower()
Equipment.equipment[53].planeType = []
Equipment.equipment[53].planeType.insert(0, None)
Equipment.equipment[53].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[53].planeType.insert(1, None)
Equipment.equipment[53].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[53].tickets = 0
Equipment.equipment[53].uiIndex = 55
Equipment.equipment.insert(54, None)
Equipment.equipment[54] = Dummy()
Equipment.equipment[54].buyAvailable = true
Equipment.equipment[54].credits = 300000
Equipment.equipment[54].detachPrice = 0
Equipment.equipment[54].excludeList = []
Equipment.equipment[54].excludeList.insert(0, None)
Equipment.equipment[54].excludeList[0] = 1304
Equipment.equipment[54].excludeList.insert(1, None)
Equipment.equipment[54].excludeList[1] = 1399
Equipment.equipment[54].icoPath = 'icons/modules/equipBetterRadiator.png'
Equipment.equipment[54].id = 55
Equipment.equipment[54].includeList = []
Equipment.equipment[54].isDiscount = false
Equipment.equipment[54].isNew = false
Equipment.equipment[54].localizeTag = 'IMPROVED_RAD_IV'
Equipment.equipment[54].mass = 0
Equipment.equipment[54].maxLevel = 10
Equipment.equipment[54].minLevel = 9
Equipment.equipment[54].mods = []
Equipment.equipment[54].mods.insert(0, None)
Equipment.equipment[54].mods[0] = Dummy()
Equipment.equipment[54].mods[0].type = ModsTypeEnum.FAST_ENGINE_COOLING
Equipment.equipment[54].mods[0].value_ = 1.43
Equipment.equipment[54].nations = []
Equipment.equipment[54].nations.insert(0, None)
Equipment.equipment[54].nations[0] = 'GB'.lower()
Equipment.equipment[54].nations.insert(1, None)
Equipment.equipment[54].nations[1] = 'Germany'.lower()
Equipment.equipment[54].nations.insert(2, None)
Equipment.equipment[54].nations[2] = 'USA'.lower()
Equipment.equipment[54].nations.insert(3, None)
Equipment.equipment[54].nations[3] = 'Japan'.lower()
Equipment.equipment[54].nations.insert(4, None)
Equipment.equipment[54].nations[4] = 'USSR'.lower()
Equipment.equipment[54].nations.insert(5, None)
Equipment.equipment[54].nations[5] = 'France'.lower()
Equipment.equipment[54].nations.insert(6, None)
Equipment.equipment[54].nations[6] = 'China'.lower()
Equipment.equipment[54].planeType = []
Equipment.equipment[54].planeType.insert(0, None)
Equipment.equipment[54].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[54].planeType.insert(1, None)
Equipment.equipment[54].planeType[1] = consts.PLANE_TYPE.NAVY
Equipment.equipment[54].tickets = 0
Equipment.equipment[54].uiIndex = 56
Equipment.equipment.insert(55, None)
Equipment.equipment[55] = Dummy()
Equipment.equipment[55].buyAvailable = true
Equipment.equipment[55].credits = 50000
Equipment.equipment[55].detachPrice = 10
Equipment.equipment[55].excludeList = []
Equipment.equipment[55].excludeList.insert(0, None)
Equipment.equipment[55].excludeList[0] = 1304
Equipment.equipment[55].excludeList.insert(1, None)
Equipment.equipment[55].excludeList[1] = 1399
Equipment.equipment[55].icoPath = 'icons/modules/equipImprovedFrame.png'
Equipment.equipment[55].id = 56
Equipment.equipment[55].includeList = []
Equipment.equipment[55].isDiscount = false
Equipment.equipment[55].isNew = false
Equipment.equipment[55].localizeTag = 'REINFORCED_FRAME_I'
Equipment.equipment[55].mass = 0
Equipment.equipment[55].maxLevel = 4
Equipment.equipment[55].minLevel = 2
Equipment.equipment[55].mods = []
Equipment.equipment[55].mods.insert(0, None)
Equipment.equipment[55].mods[0] = Dummy()
Equipment.equipment[55].mods[0].type = ModsTypeEnum.VITALS_ARMOR
Equipment.equipment[55].mods[0].value_ = 0.9
Equipment.equipment[55].mods.insert(1, None)
Equipment.equipment[55].mods[1] = Dummy()
Equipment.equipment[55].mods[1].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[55].mods[1].value_ = 0.9
Equipment.equipment[55].mods.insert(2, None)
Equipment.equipment[55].mods[2] = Dummy()
Equipment.equipment[55].mods[2].type = ModsTypeEnum.MAIN_HP
Equipment.equipment[55].mods[2].value_ = 1.15
Equipment.equipment[55].nations = []
Equipment.equipment[55].nations.insert(0, None)
Equipment.equipment[55].nations[0] = 'GB'.lower()
Equipment.equipment[55].nations.insert(1, None)
Equipment.equipment[55].nations[1] = 'Germany'.lower()
Equipment.equipment[55].nations.insert(2, None)
Equipment.equipment[55].nations[2] = 'USA'.lower()
Equipment.equipment[55].nations.insert(3, None)
Equipment.equipment[55].nations[3] = 'Japan'.lower()
Equipment.equipment[55].nations.insert(4, None)
Equipment.equipment[55].nations[4] = 'USSR'.lower()
Equipment.equipment[55].nations.insert(5, None)
Equipment.equipment[55].nations[5] = 'France'.lower()
Equipment.equipment[55].nations.insert(6, None)
Equipment.equipment[55].nations[6] = 'China'.lower()
Equipment.equipment[55].planeType = []
Equipment.equipment[55].planeType.insert(0, None)
Equipment.equipment[55].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[55].planeType.insert(1, None)
Equipment.equipment[55].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[55].tickets = 0
Equipment.equipment[55].uiIndex = 8
Equipment.equipment.insert(56, None)
Equipment.equipment[56] = Dummy()
Equipment.equipment[56].buyAvailable = true
Equipment.equipment[56].credits = 350000
Equipment.equipment[56].detachPrice = 10
Equipment.equipment[56].excludeList = []
Equipment.equipment[56].excludeList.insert(0, None)
Equipment.equipment[56].excludeList[0] = 1304
Equipment.equipment[56].excludeList.insert(1, None)
Equipment.equipment[56].excludeList[1] = 1399
Equipment.equipment[56].icoPath = 'icons/modules/equipImprovedFrame.png'
Equipment.equipment[56].id = 57
Equipment.equipment[56].includeList = []
Equipment.equipment[56].isDiscount = false
Equipment.equipment[56].isNew = false
Equipment.equipment[56].localizeTag = 'REINFORCED_FRAME_II'
Equipment.equipment[56].mass = 0
Equipment.equipment[56].maxLevel = 7
Equipment.equipment[56].minLevel = 5
Equipment.equipment[56].mods = []
Equipment.equipment[56].mods.insert(0, None)
Equipment.equipment[56].mods[0] = Dummy()
Equipment.equipment[56].mods[0].type = ModsTypeEnum.VITALS_ARMOR
Equipment.equipment[56].mods[0].value_ = 0.9
Equipment.equipment[56].mods.insert(1, None)
Equipment.equipment[56].mods[1] = Dummy()
Equipment.equipment[56].mods[1].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[56].mods[1].value_ = 0.9
Equipment.equipment[56].mods.insert(2, None)
Equipment.equipment[56].mods[2] = Dummy()
Equipment.equipment[56].mods[2].type = ModsTypeEnum.MAIN_HP
Equipment.equipment[56].mods[2].value_ = 1.15
Equipment.equipment[56].nations = []
Equipment.equipment[56].nations.insert(0, None)
Equipment.equipment[56].nations[0] = 'GB'.lower()
Equipment.equipment[56].nations.insert(1, None)
Equipment.equipment[56].nations[1] = 'Germany'.lower()
Equipment.equipment[56].nations.insert(2, None)
Equipment.equipment[56].nations[2] = 'USA'.lower()
Equipment.equipment[56].nations.insert(3, None)
Equipment.equipment[56].nations[3] = 'Japan'.lower()
Equipment.equipment[56].nations.insert(4, None)
Equipment.equipment[56].nations[4] = 'USSR'.lower()
Equipment.equipment[56].nations.insert(5, None)
Equipment.equipment[56].nations[5] = 'France'.lower()
Equipment.equipment[56].nations.insert(6, None)
Equipment.equipment[56].nations[6] = 'China'.lower()
Equipment.equipment[56].planeType = []
Equipment.equipment[56].planeType.insert(0, None)
Equipment.equipment[56].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[56].planeType.insert(1, None)
Equipment.equipment[56].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[56].tickets = 0
Equipment.equipment[56].uiIndex = 9
Equipment.equipment.insert(57, None)
Equipment.equipment[57] = Dummy()
Equipment.equipment[57].buyAvailable = true
Equipment.equipment[57].credits = 600000
Equipment.equipment[57].detachPrice = 10
Equipment.equipment[57].excludeList = []
Equipment.equipment[57].excludeList.insert(0, None)
Equipment.equipment[57].excludeList[0] = 1304
Equipment.equipment[57].excludeList.insert(1, None)
Equipment.equipment[57].excludeList[1] = 1399
Equipment.equipment[57].icoPath = 'icons/modules/equipImprovedFrame.png'
Equipment.equipment[57].id = 58
Equipment.equipment[57].includeList = []
Equipment.equipment[57].isDiscount = false
Equipment.equipment[57].isNew = false
Equipment.equipment[57].localizeTag = 'REINFORCED_FRAME_III'
Equipment.equipment[57].mass = 0
Equipment.equipment[57].maxLevel = 10
Equipment.equipment[57].minLevel = 8
Equipment.equipment[57].mods = []
Equipment.equipment[57].mods.insert(0, None)
Equipment.equipment[57].mods[0] = Dummy()
Equipment.equipment[57].mods[0].type = ModsTypeEnum.VITALS_ARMOR
Equipment.equipment[57].mods[0].value_ = 0.9
Equipment.equipment[57].mods.insert(1, None)
Equipment.equipment[57].mods[1] = Dummy()
Equipment.equipment[57].mods[1].type = ModsTypeEnum.SYSTEM_HP
Equipment.equipment[57].mods[1].value_ = 0.9
Equipment.equipment[57].mods.insert(2, None)
Equipment.equipment[57].mods[2] = Dummy()
Equipment.equipment[57].mods[2].type = ModsTypeEnum.MAIN_HP
Equipment.equipment[57].mods[2].value_ = 1.15
Equipment.equipment[57].nations = []
Equipment.equipment[57].nations.insert(0, None)
Equipment.equipment[57].nations[0] = 'GB'.lower()
Equipment.equipment[57].nations.insert(1, None)
Equipment.equipment[57].nations[1] = 'Germany'.lower()
Equipment.equipment[57].nations.insert(2, None)
Equipment.equipment[57].nations[2] = 'USA'.lower()
Equipment.equipment[57].nations.insert(3, None)
Equipment.equipment[57].nations[3] = 'Japan'.lower()
Equipment.equipment[57].nations.insert(4, None)
Equipment.equipment[57].nations[4] = 'USSR'.lower()
Equipment.equipment[57].nations.insert(5, None)
Equipment.equipment[57].nations[5] = 'France'.lower()
Equipment.equipment[57].nations.insert(6, None)
Equipment.equipment[57].nations[6] = 'China'.lower()
Equipment.equipment[57].planeType = []
Equipment.equipment[57].planeType.insert(0, None)
Equipment.equipment[57].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[57].planeType.insert(1, None)
Equipment.equipment[57].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[57].tickets = 0
Equipment.equipment[57].uiIndex = 10
Equipment.equipment.insert(58, None)
Equipment.equipment[58] = Dummy()
Equipment.equipment[58].buyAvailable = true
Equipment.equipment[58].credits = 50000
Equipment.equipment[58].detachPrice = 0
Equipment.equipment[58].excludeList = []
Equipment.equipment[58].excludeList.insert(0, None)
Equipment.equipment[58].excludeList[0] = 1304
Equipment.equipment[58].excludeList.insert(1, None)
Equipment.equipment[58].excludeList[1] = 1399
Equipment.equipment[58].excludeList.insert(2, None)
Equipment.equipment[58].excludeList[2] = 2191
Equipment.equipment[58].excludeList.insert(3, None)
Equipment.equipment[58].excludeList[3] = 1394
Equipment.equipment[58].excludeList.insert(4, None)
Equipment.equipment[58].excludeList[4] = 2291
Equipment.equipment[58].excludeList.insert(5, None)
Equipment.equipment[58].excludeList[5] = 1392
Equipment.equipment[58].excludeList.insert(6, None)
Equipment.equipment[58].excludeList[6] = 1393
Equipment.equipment[58].excludeList.insert(7, None)
Equipment.equipment[58].excludeList[7] = 1098
Equipment.equipment[58].excludeList.insert(8, None)
Equipment.equipment[58].excludeList[8] = 1292
Equipment.equipment[58].icoPath = 'icons/modules/equipTurret.png'
Equipment.equipment[58].id = 59
Equipment.equipment[58].includeList = []
Equipment.equipment[58].isDiscount = false
Equipment.equipment[58].isNew = false
Equipment.equipment[58].localizeTag = 'IMPROVED_GUNNER_RANGE_I'
Equipment.equipment[58].mass = 0
Equipment.equipment[58].maxLevel = 3
Equipment.equipment[58].minLevel = 2
Equipment.equipment[58].mods = []
Equipment.equipment[58].mods.insert(0, None)
Equipment.equipment[58].mods[0] = Dummy()
Equipment.equipment[58].mods[0].type = ModsTypeEnum.TURRET_RANGE
Equipment.equipment[58].mods[0].value_ = 1.15
Equipment.equipment[58].nations = []
Equipment.equipment[58].nations.insert(0, None)
Equipment.equipment[58].nations[0] = 'GB'.lower()
Equipment.equipment[58].nations.insert(1, None)
Equipment.equipment[58].nations[1] = 'Germany'.lower()
Equipment.equipment[58].nations.insert(2, None)
Equipment.equipment[58].nations[2] = 'USA'.lower()
Equipment.equipment[58].nations.insert(3, None)
Equipment.equipment[58].nations[3] = 'Japan'.lower()
Equipment.equipment[58].nations.insert(4, None)
Equipment.equipment[58].nations[4] = 'USSR'.lower()
Equipment.equipment[58].nations.insert(5, None)
Equipment.equipment[58].nations[5] = 'France'.lower()
Equipment.equipment[58].nations.insert(6, None)
Equipment.equipment[58].nations[6] = 'China'.lower()
Equipment.equipment[58].planeType = []
Equipment.equipment[58].planeType.insert(0, None)
Equipment.equipment[58].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[58].planeType.insert(1, None)
Equipment.equipment[58].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[58].tickets = 0
Equipment.equipment[58].uiIndex = 35
Equipment.equipment.insert(59, None)
Equipment.equipment[59] = Dummy()
Equipment.equipment[59].buyAvailable = true
Equipment.equipment[59].credits = 200000
Equipment.equipment[59].detachPrice = 0
Equipment.equipment[59].excludeList = []
Equipment.equipment[59].excludeList.insert(0, None)
Equipment.equipment[59].excludeList[0] = 1304
Equipment.equipment[59].excludeList.insert(1, None)
Equipment.equipment[59].excludeList[1] = 1399
Equipment.equipment[59].excludeList.insert(2, None)
Equipment.equipment[59].excludeList[2] = 2405
Equipment.equipment[59].excludeList.insert(3, None)
Equipment.equipment[59].excludeList[3] = 3504
Equipment.equipment[59].excludeList.insert(4, None)
Equipment.equipment[59].excludeList[4] = 1505
Equipment.equipment[59].excludeList.insert(5, None)
Equipment.equipment[59].excludeList[5] = 2502
Equipment.equipment[59].excludeList.insert(6, None)
Equipment.equipment[59].excludeList[6] = 5602
Equipment.equipment[59].excludeList.insert(7, None)
Equipment.equipment[59].excludeList[7] = 3603
Equipment.equipment[59].excludeList.insert(8, None)
Equipment.equipment[59].excludeList[8] = 6691
Equipment.equipment[59].excludeList.insert(9, None)
Equipment.equipment[59].excludeList[9] = 3691
Equipment.equipment[59].excludeList.insert(10, None)
Equipment.equipment[59].excludeList[10] = 1491
Equipment.equipment[59].icoPath = 'icons/modules/equipTurret.png'
Equipment.equipment[59].id = 60
Equipment.equipment[59].includeList = []
Equipment.equipment[59].isDiscount = false
Equipment.equipment[59].isNew = false
Equipment.equipment[59].localizeTag = 'IMPROVED_GUNNER_RANGE_II'
Equipment.equipment[59].mass = 0
Equipment.equipment[59].maxLevel = 6
Equipment.equipment[59].minLevel = 4
Equipment.equipment[59].mods = []
Equipment.equipment[59].mods.insert(0, None)
Equipment.equipment[59].mods[0] = Dummy()
Equipment.equipment[59].mods[0].type = ModsTypeEnum.TURRET_RANGE
Equipment.equipment[59].mods[0].value_ = 1.15
Equipment.equipment[59].nations = []
Equipment.equipment[59].nations.insert(0, None)
Equipment.equipment[59].nations[0] = 'GB'.lower()
Equipment.equipment[59].nations.insert(1, None)
Equipment.equipment[59].nations[1] = 'Germany'.lower()
Equipment.equipment[59].nations.insert(2, None)
Equipment.equipment[59].nations[2] = 'USA'.lower()
Equipment.equipment[59].nations.insert(3, None)
Equipment.equipment[59].nations[3] = 'Japan'.lower()
Equipment.equipment[59].nations.insert(4, None)
Equipment.equipment[59].nations[4] = 'USSR'.lower()
Equipment.equipment[59].nations.insert(5, None)
Equipment.equipment[59].nations[5] = 'France'.lower()
Equipment.equipment[59].nations.insert(6, None)
Equipment.equipment[59].nations[6] = 'China'.lower()
Equipment.equipment[59].planeType = []
Equipment.equipment[59].planeType.insert(0, None)
Equipment.equipment[59].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[59].planeType.insert(1, None)
Equipment.equipment[59].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[59].tickets = 0
Equipment.equipment[59].uiIndex = 36
Equipment.equipment.insert(60, None)
Equipment.equipment[60] = Dummy()
Equipment.equipment[60].buyAvailable = true
Equipment.equipment[60].credits = 350000
Equipment.equipment[60].detachPrice = 0
Equipment.equipment[60].excludeList = []
Equipment.equipment[60].excludeList.insert(0, None)
Equipment.equipment[60].excludeList[0] = 1304
Equipment.equipment[60].excludeList.insert(1, None)
Equipment.equipment[60].excludeList[1] = 1399
Equipment.equipment[60].excludeList.insert(2, None)
Equipment.equipment[60].excludeList[2] = 1702
Equipment.equipment[60].excludeList.insert(3, None)
Equipment.equipment[60].excludeList[3] = 3704
Equipment.equipment[60].excludeList.insert(4, None)
Equipment.equipment[60].excludeList[4] = 5702
Equipment.equipment[60].excludeList.insert(5, None)
Equipment.equipment[60].excludeList[5] = 3791
Equipment.equipment[60].excludeList.insert(6, None)
Equipment.equipment[60].excludeList[6] = 3804
Equipment.equipment[60].excludeList.insert(7, None)
Equipment.equipment[60].excludeList[7] = 1801
Equipment.equipment[60].excludeList.insert(8, None)
Equipment.equipment[60].excludeList[8] = 5802
Equipment.equipment[60].excludeList.insert(9, None)
Equipment.equipment[60].excludeList[9] = 3894
Equipment.equipment[60].excludeList.insert(10, None)
Equipment.equipment[60].excludeList[10] = 7791
Equipment.equipment[60].excludeList.insert(11, None)
Equipment.equipment[60].excludeList[11] = 1892
Equipment.equipment[60].excludeList.insert(12, None)
Equipment.equipment[60].excludeList[12] = 4792
Equipment.equipment[60].icoPath = 'icons/modules/equipTurret.png'
Equipment.equipment[60].id = 61
Equipment.equipment[60].includeList = []
Equipment.equipment[60].isDiscount = false
Equipment.equipment[60].isNew = false
Equipment.equipment[60].localizeTag = 'IMPROVED_GUNNER_RANGE_III'
Equipment.equipment[60].mass = 0
Equipment.equipment[60].maxLevel = 8
Equipment.equipment[60].minLevel = 7
Equipment.equipment[60].mods = []
Equipment.equipment[60].mods.insert(0, None)
Equipment.equipment[60].mods[0] = Dummy()
Equipment.equipment[60].mods[0].type = ModsTypeEnum.TURRET_RANGE
Equipment.equipment[60].mods[0].value_ = 1.15
Equipment.equipment[60].nations = []
Equipment.equipment[60].nations.insert(0, None)
Equipment.equipment[60].nations[0] = 'GB'.lower()
Equipment.equipment[60].nations.insert(1, None)
Equipment.equipment[60].nations[1] = 'Germany'.lower()
Equipment.equipment[60].nations.insert(2, None)
Equipment.equipment[60].nations[2] = 'USA'.lower()
Equipment.equipment[60].nations.insert(3, None)
Equipment.equipment[60].nations[3] = 'Japan'.lower()
Equipment.equipment[60].nations.insert(4, None)
Equipment.equipment[60].nations[4] = 'USSR'.lower()
Equipment.equipment[60].nations.insert(5, None)
Equipment.equipment[60].nations[5] = 'France'.lower()
Equipment.equipment[60].nations.insert(6, None)
Equipment.equipment[60].nations[6] = 'China'.lower()
Equipment.equipment[60].planeType = []
Equipment.equipment[60].planeType.insert(0, None)
Equipment.equipment[60].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[60].planeType.insert(1, None)
Equipment.equipment[60].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[60].tickets = 0
Equipment.equipment[60].uiIndex = 37
Equipment.equipment.insert(61, None)
Equipment.equipment[61] = Dummy()
Equipment.equipment[61].buyAvailable = true
Equipment.equipment[61].credits = 500000
Equipment.equipment[61].detachPrice = 0
Equipment.equipment[61].excludeList = []
Equipment.equipment[61].excludeList.insert(0, None)
Equipment.equipment[61].excludeList[0] = 1304
Equipment.equipment[61].excludeList.insert(1, None)
Equipment.equipment[61].excludeList[1] = 1399
Equipment.equipment[61].excludeList.insert(2, None)
Equipment.equipment[61].excludeList[2] = 3904
Equipment.equipment[61].excludeList.insert(3, None)
Equipment.equipment[61].excludeList[3] = 5902
Equipment.equipment[61].excludeList.insert(4, None)
Equipment.equipment[61].excludeList[4] = 1904
Equipment.equipment[61].excludeList.insert(5, None)
Equipment.equipment[61].excludeList[5] = 3004
Equipment.equipment[61].excludeList.insert(6, None)
Equipment.equipment[61].excludeList[6] = 5002
Equipment.equipment[61].excludeList.insert(7, None)
Equipment.equipment[61].excludeList[7] = 1001
Equipment.equipment[61].icoPath = 'icons/modules/equipTurret.png'
Equipment.equipment[61].id = 62
Equipment.equipment[61].includeList = []
Equipment.equipment[61].isDiscount = false
Equipment.equipment[61].isNew = false
Equipment.equipment[61].localizeTag = 'IMPROVED_GUNNER_RANGE_IV'
Equipment.equipment[61].mass = 0
Equipment.equipment[61].maxLevel = 10
Equipment.equipment[61].minLevel = 9
Equipment.equipment[61].mods = []
Equipment.equipment[61].mods.insert(0, None)
Equipment.equipment[61].mods[0] = Dummy()
Equipment.equipment[61].mods[0].type = ModsTypeEnum.TURRET_RANGE
Equipment.equipment[61].mods[0].value_ = 1.15
Equipment.equipment[61].nations = []
Equipment.equipment[61].nations.insert(0, None)
Equipment.equipment[61].nations[0] = 'GB'.lower()
Equipment.equipment[61].nations.insert(1, None)
Equipment.equipment[61].nations[1] = 'Germany'.lower()
Equipment.equipment[61].nations.insert(2, None)
Equipment.equipment[61].nations[2] = 'USA'.lower()
Equipment.equipment[61].nations.insert(3, None)
Equipment.equipment[61].nations[3] = 'Japan'.lower()
Equipment.equipment[61].nations.insert(4, None)
Equipment.equipment[61].nations[4] = 'USSR'.lower()
Equipment.equipment[61].nations.insert(5, None)
Equipment.equipment[61].nations[5] = 'France'.lower()
Equipment.equipment[61].nations.insert(6, None)
Equipment.equipment[61].nations[6] = 'China'.lower()
Equipment.equipment[61].planeType = []
Equipment.equipment[61].planeType.insert(0, None)
Equipment.equipment[61].planeType[0] = consts.PLANE_TYPE.ASSAULT
Equipment.equipment[61].planeType.insert(1, None)
Equipment.equipment[61].planeType[1] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[61].tickets = 0
Equipment.equipment[61].uiIndex = 38
Equipment.equipment.insert(62, None)
Equipment.equipment[62] = Dummy()
Equipment.equipment[62].buyAvailable = true
Equipment.equipment[62].credits = 30000
Equipment.equipment[62].detachPrice = 0
Equipment.equipment[62].excludeList = []
Equipment.equipment[62].excludeList.insert(0, None)
Equipment.equipment[62].excludeList[0] = 1304
Equipment.equipment[62].excludeList.insert(1, None)
Equipment.equipment[62].excludeList[1] = 1399
Equipment.equipment[62].icoPath = 'icons/modules/equipBetterTankProtector.png'
Equipment.equipment[62].id = 63
Equipment.equipment[62].includeList = []
Equipment.equipment[62].isDiscount = false
Equipment.equipment[62].isNew = false
Equipment.equipment[62].localizeTag = 'BETTER_TANK_PROTECTOR'
Equipment.equipment[62].mass = 10
Equipment.equipment[62].maxLevel = 3
Equipment.equipment[62].minLevel = 1
Equipment.equipment[62].mods = []
Equipment.equipment[62].mods.insert(0, None)
Equipment.equipment[62].mods[0] = Dummy()
Equipment.equipment[62].mods[0].type = ModsTypeEnum.FIRE_CHANCE
Equipment.equipment[62].mods[0].value_ = 1.5
Equipment.equipment[62].mods.insert(1, None)
Equipment.equipment[62].mods[1] = Dummy()
Equipment.equipment[62].mods[1].type = ModsTypeEnum.FIRE_DAMAGE_K
Equipment.equipment[62].mods[1].value_ = 0.5
Equipment.equipment[62].nations = []
Equipment.equipment[62].nations.insert(0, None)
Equipment.equipment[62].nations[0] = 'GB'.lower()
Equipment.equipment[62].nations.insert(1, None)
Equipment.equipment[62].nations[1] = 'Germany'.lower()
Equipment.equipment[62].nations.insert(2, None)
Equipment.equipment[62].nations[2] = 'USA'.lower()
Equipment.equipment[62].nations.insert(3, None)
Equipment.equipment[62].nations[3] = 'Japan'.lower()
Equipment.equipment[62].nations.insert(4, None)
Equipment.equipment[62].nations[4] = 'USSR'.lower()
Equipment.equipment[62].nations.insert(5, None)
Equipment.equipment[62].nations[5] = 'France'.lower()
Equipment.equipment[62].nations.insert(6, None)
Equipment.equipment[62].nations[6] = 'China'.lower()
Equipment.equipment[62].planeType = []
Equipment.equipment[62].tickets = 0
Equipment.equipment[62].uiIndex = 24
Equipment.equipment.insert(63, None)
Equipment.equipment[63] = Dummy()
Equipment.equipment[63].buyAvailable = true
Equipment.equipment[63].credits = 30000
Equipment.equipment[63].detachPrice = 10
Equipment.equipment[63].excludeList = []
Equipment.equipment[63].excludeList.insert(0, None)
Equipment.equipment[63].excludeList[0] = 1304
Equipment.equipment[63].excludeList.insert(1, None)
Equipment.equipment[63].excludeList[1] = 1399
Equipment.equipment[63].icoPath = 'icons/modules/equipImprovedDope.png'
Equipment.equipment[63].id = 64
Equipment.equipment[63].includeList = []
Equipment.equipment[63].isDiscount = false
Equipment.equipment[63].isNew = false
Equipment.equipment[63].localizeTag = 'IMPROVED_DOPE_I'
Equipment.equipment[63].mass = 0
Equipment.equipment[63].maxLevel = 3
Equipment.equipment[63].minLevel = 2
Equipment.equipment[63].mods = []
Equipment.equipment[63].mods.insert(0, None)
Equipment.equipment[63].mods[0] = Dummy()
Equipment.equipment[63].mods[0].type = ModsTypeEnum.MAX_SPEED
Equipment.equipment[63].mods[0].value_ = 1.05
Equipment.equipment[63].mods.insert(1, None)
Equipment.equipment[63].mods[1] = Dummy()
Equipment.equipment[63].mods[1].type = ModsTypeEnum.DIVE_ACCELERATION
Equipment.equipment[63].mods[1].value_ = 1.25
Equipment.equipment[63].nations = []
Equipment.equipment[63].nations.insert(0, None)
Equipment.equipment[63].nations[0] = 'GB'.lower()
Equipment.equipment[63].nations.insert(1, None)
Equipment.equipment[63].nations[1] = 'Germany'.lower()
Equipment.equipment[63].nations.insert(2, None)
Equipment.equipment[63].nations[2] = 'USA'.lower()
Equipment.equipment[63].nations.insert(3, None)
Equipment.equipment[63].nations[3] = 'Japan'.lower()
Equipment.equipment[63].nations.insert(4, None)
Equipment.equipment[63].nations[4] = 'USSR'.lower()
Equipment.equipment[63].nations.insert(5, None)
Equipment.equipment[63].nations[5] = 'France'.lower()
Equipment.equipment[63].nations.insert(6, None)
Equipment.equipment[63].nations[6] = 'China'.lower()
Equipment.equipment[63].planeType = []
Equipment.equipment[63].planeType.insert(0, None)
Equipment.equipment[63].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Equipment.equipment[63].tickets = 0
Equipment.equipment[63].uiIndex = 43
Equipment.equipment.insert(64, None)
Equipment.equipment[64] = Dummy()
Equipment.equipment[64].buyAvailable = false
Equipment.equipment[64].credits = 250000
Equipment.equipment[64].detachPrice = 0
Equipment.equipment[64].excludeList = []
Equipment.equipment[64].excludeList.insert(0, None)
Equipment.equipment[64].excludeList[0] = 2001
Equipment.equipment[64].excludeList.insert(1, None)
Equipment.equipment[64].excludeList[1] = 2004
Equipment.equipment[64].excludeList.insert(2, None)
Equipment.equipment[64].excludeList[2] = 2005
Equipment.equipment[64].excludeList.insert(3, None)
Equipment.equipment[64].excludeList[3] = 2203
Equipment.equipment[64].excludeList.insert(4, None)
Equipment.equipment[64].excludeList[4] = 2292
Equipment.equipment[64].excludeList.insert(5, None)
Equipment.equipment[64].excludeList[5] = 2403
Equipment.equipment[64].excludeList.insert(6, None)
Equipment.equipment[64].excludeList[6] = 2501
Equipment.equipment[64].excludeList.insert(7, None)
Equipment.equipment[64].excludeList[7] = 2503
Equipment.equipment[64].excludeList.insert(8, None)
Equipment.equipment[64].excludeList[8] = 2504
Equipment.equipment[64].excludeList.insert(9, None)
Equipment.equipment[64].excludeList[9] = 2592
Equipment.equipment[64].excludeList.insert(10, None)
Equipment.equipment[64].excludeList[10] = 2601
Equipment.equipment[64].excludeList.insert(11, None)
Equipment.equipment[64].excludeList[11] = 2604
Equipment.equipment[64].excludeList.insert(12, None)
Equipment.equipment[64].excludeList[12] = 2605
Equipment.equipment[64].excludeList.insert(13, None)
Equipment.equipment[64].excludeList[13] = 2691
Equipment.equipment[64].excludeList.insert(14, None)
Equipment.equipment[64].excludeList[14] = 2701
Equipment.equipment[64].excludeList.insert(15, None)
Equipment.equipment[64].excludeList[15] = 2703
Equipment.equipment[64].excludeList.insert(16, None)
Equipment.equipment[64].excludeList[16] = 2704
Equipment.equipment[64].excludeList.insert(17, None)
Equipment.equipment[64].excludeList[17] = 2706
Equipment.equipment[64].excludeList.insert(18, None)
Equipment.equipment[64].excludeList[18] = 2791
Equipment.equipment[64].excludeList.insert(19, None)
Equipment.equipment[64].excludeList[19] = 2792
Equipment.equipment[64].excludeList.insert(20, None)
Equipment.equipment[64].excludeList[20] = 2803
Equipment.equipment[64].excludeList.insert(21, None)
Equipment.equipment[64].excludeList[21] = 2804
Equipment.equipment[64].excludeList.insert(22, None)
Equipment.equipment[64].excludeList[22] = 2891
Equipment.equipment[64].excludeList.insert(23, None)
Equipment.equipment[64].excludeList[23] = 2901
Equipment.equipment[64].excludeList.insert(24, None)
Equipment.equipment[64].excludeList[24] = 2903
Equipment.equipment[64].excludeList.insert(25, None)
Equipment.equipment[64].excludeList[25] = 2904
Equipment.equipment[64].icoPath = 'icons/modules/econGunCameraUniq.png'
Equipment.equipment[64].id = 65
Equipment.equipment[64].includeList = []
Equipment.equipment[64].isDiscount = false
Equipment.equipment[64].isNew = true
Equipment.equipment[64].localizeTag = 'GUN_CAM_UNIQ'
Equipment.equipment[64].mass = 0
Equipment.equipment[64].maxLevel = 5
Equipment.equipment[64].minLevel = 5
Equipment.equipment[64].mods = []
Equipment.equipment[64].mods.insert(0, None)
Equipment.equipment[64].mods[0] = Dummy()
Equipment.equipment[64].mods[0].type = ModsTypeEnum.ECONOMIC_BONUS_CREDITS
Equipment.equipment[64].mods[0].value_ = 1.15
Equipment.equipment[64].mods.insert(1, None)
Equipment.equipment[64].mods[1] = Dummy()
Equipment.equipment[64].mods[1].type = ModsTypeEnum.ECONOMIC_BONUS_XP
Equipment.equipment[64].mods[1].value_ = 1.15
Equipment.equipment[64].nations = []
Equipment.equipment[64].nations.insert(0, None)
Equipment.equipment[64].nations[0] = 'USSR'.lower()
Equipment.equipment[64].planeType = []
Equipment.equipment[64].planeType.insert(0, None)
Equipment.equipment[64].planeType[0] = consts.PLANE_TYPE.FIGHTER
Equipment.equipment[64].tickets = 0
Equipment.equipment[64].uiIndex = 68
Equipment.equipment.insert(65, None)
Equipment.equipment[65] = Dummy()
Equipment.equipment[65].buyAvailable = false
Equipment.equipment[65].credits = 0
Equipment.equipment[65].detachPrice = 0
Equipment.equipment[65].excludeList = []
Equipment.equipment[65].excludeList.insert(0, None)
Equipment.equipment[65].excludeList[0] = 1304
Equipment.equipment[65].excludeList.insert(1, None)
Equipment.equipment[65].excludeList[1] = 1399
Equipment.equipment[65].icoPath = 'icons/modules/econGunCamera.png'
Equipment.equipment[65].id = 66
Equipment.equipment[65].includeList = []
Equipment.equipment[65].isDiscount = false
Equipment.equipment[65].isNew = false
Equipment.equipment[65].localizeTag = 'GUN_CAM_I'
Equipment.equipment[65].mass = 0
Equipment.equipment[65].maxLevel = 10
Equipment.equipment[65].minLevel = 1
Equipment.equipment[65].mods = []
Equipment.equipment[65].mods.insert(0, None)
Equipment.equipment[65].mods[0] = Dummy()
Equipment.equipment[65].mods[0].type = ModsTypeEnum.ECONOMIC_BONUS_CREDITS
Equipment.equipment[65].mods[0].value_ = 1.05
Equipment.equipment[65].nations = []
Equipment.equipment[65].nations.insert(0, None)
Equipment.equipment[65].nations[0] = 'GB'.lower()
Equipment.equipment[65].nations.insert(1, None)
Equipment.equipment[65].nations[1] = 'Germany'.lower()
Equipment.equipment[65].nations.insert(2, None)
Equipment.equipment[65].nations[2] = 'USA'.lower()
Equipment.equipment[65].nations.insert(3, None)
Equipment.equipment[65].nations[3] = 'Japan'.lower()
Equipment.equipment[65].nations.insert(4, None)
Equipment.equipment[65].nations[4] = 'USSR'.lower()
Equipment.equipment[65].nations.insert(5, None)
Equipment.equipment[65].nations[5] = 'France'.lower()
Equipment.equipment[65].nations.insert(6, None)
Equipment.equipment[65].nations[6] = 'China'.lower()
Equipment.equipment[65].planeType = []
Equipment.equipment[65].tickets = 90
Equipment.equipment[65].uiIndex = 69
Equipment.equipment.insert(66, None)
Equipment.equipment[66] = Dummy()
Equipment.equipment[66].buyAvailable = false
Equipment.equipment[66].credits = 0
Equipment.equipment[66].detachPrice = 0
Equipment.equipment[66].excludeList = []
Equipment.equipment[66].excludeList.insert(0, None)
Equipment.equipment[66].excludeList[0] = 1304
Equipment.equipment[66].excludeList.insert(1, None)
Equipment.equipment[66].excludeList[1] = 1399
Equipment.equipment[66].icoPath = 'icons/modules/econFof1.png'
Equipment.equipment[66].id = 67
Equipment.equipment[66].includeList = []
Equipment.equipment[66].isDiscount = false
Equipment.equipment[66].isNew = false
Equipment.equipment[66].localizeTag = 'FOF_I'
Equipment.equipment[66].mass = 0
Equipment.equipment[66].maxLevel = 10
Equipment.equipment[66].minLevel = 1
Equipment.equipment[66].mods = []
Equipment.equipment[66].mods.insert(0, None)
Equipment.equipment[66].mods[0] = Dummy()
Equipment.equipment[66].mods[0].type = ModsTypeEnum.ECONOMIC_BONUS_XP
Equipment.equipment[66].mods[0].value_ = 1.05
Equipment.equipment[66].nations = []
Equipment.equipment[66].nations.insert(0, None)
Equipment.equipment[66].nations[0] = 'GB'.lower()
Equipment.equipment[66].nations.insert(1, None)
Equipment.equipment[66].nations[1] = 'Germany'.lower()
Equipment.equipment[66].nations.insert(2, None)
Equipment.equipment[66].nations[2] = 'USA'.lower()
Equipment.equipment[66].nations.insert(3, None)
Equipment.equipment[66].nations[3] = 'Japan'.lower()
Equipment.equipment[66].nations.insert(4, None)
Equipment.equipment[66].nations[4] = 'USSR'.lower()
Equipment.equipment[66].nations.insert(5, None)
Equipment.equipment[66].nations[5] = 'France'.lower()
Equipment.equipment[66].nations.insert(6, None)
Equipment.equipment[66].nations[6] = 'China'.lower()
Equipment.equipment[66].planeType = []
Equipment.equipment[66].tickets = 90
Equipment.equipment[66].uiIndex = 70
EquipmentDB = None
Filter = None

def initDB():
    global Filter
    global EquipmentDB
    if EquipmentDB is None:
        EquipmentDB = {}
        Filter = {'nation': {},
         'level': {},
         'include': {},
         'exclude': {},
         'planeType': {}}
        for equipment in Equipment.equipment:
            EquipmentDB[equipment.id] = equipment
            for nation in equipment.nations:
                Filter['nation'].setdefault(nation, set()).add(equipment.id)

            for level in xrange(equipment.minLevel, equipment.maxLevel + 1):
                Filter['level'].setdefault(level, set()).add(equipment.id)

            for include in equipment.includeList:
                Filter['include'].setdefault(include, set()).add(equipment.id)

            for exclude in equipment.excludeList:
                Filter['exclude'].setdefault(exclude, set()).add(equipment.id)

            if not equipment.planeType:
                equipment.planeType = filter(lambda x: isinstance(x, int), consts.PLANE_TYPE.__dict__.values())
            for planeType in equipment.planeType:
                Filter['planeType'].setdefault(planeType, set()).add(equipment.id)

            equipment.name = 'LOBBY_EQUIPMENT_NAME_' + equipment.localizeTag
            equipment.description = 'LOBBY_EQUIPMENT_EFFECT_' + equipment.localizeTag

    return


initDB()