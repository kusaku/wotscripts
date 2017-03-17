# Embedded file name: scripts/common/_consumables_data.py
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


Consumables = Dummy()
Consumables.consumable = []
Consumables.consumable.insert(0, None)
Consumables.consumable[0] = Dummy()
Consumables.consumable[0].affectedModules = Dummy()
Consumables.consumable[0].affectedModules.isAnimationEquipment = true
Consumables.consumable[0].affectedModules.module = []
Consumables.consumable[0].affectedModules.module.insert(0, None)
Consumables.consumable[0].affectedModules.module[0] = 'Pilot'
Consumables.consumable[0].affectedModules.module.insert(1, None)
Consumables.consumable[0].affectedModules.module[1] = 'Gunner1'
Consumables.consumable[0].behaviour = 0
Consumables.consumable[0].buyAvailable = true
Consumables.consumable[0].chargesCount = 1
Consumables.consumable[0].coolDownTime = 15
Consumables.consumable[0].credits = 3000
Consumables.consumable[0].effectTime = 2
Consumables.consumable[0].excludeList = []
Consumables.consumable[0].excludeList.insert(0, None)
Consumables.consumable[0].excludeList[0] = 1304
Consumables.consumable[0].excludeList.insert(1, None)
Consumables.consumable[0].excludeList[1] = 1399
Consumables.consumable[0].gold = 0
Consumables.consumable[0].group = 1
Consumables.consumable[0].icoPath = 'icons/modules/supBondPack.png'
Consumables.consumable[0].icoPathBig = 'icons/modules/hud/supBondPack.png'
Consumables.consumable[0].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[0].icoPathSmall = 'icons/quests/supBondPack.png'
Consumables.consumable[0].id = 1
Consumables.consumable[0].includeList = []
Consumables.consumable[0].isDiscount = false
Consumables.consumable[0].isNew = false
Consumables.consumable[0].localizeTag = 'BOND_PACK'
Consumables.consumable[0].maxLevel = 10
Consumables.consumable[0].minLevel = 1
Consumables.consumable[0].mods = []
Consumables.consumable[0].mods.insert(0, None)
Consumables.consumable[0].mods[0] = Dummy()
Consumables.consumable[0].mods[0].activationRequired = 1
Consumables.consumable[0].mods[0].type = ModsTypeEnum.HP_RESTORE
Consumables.consumable[0].mods[0].value_ = 1.0
Consumables.consumable[0].mods.insert(1, None)
Consumables.consumable[0].mods[1] = Dummy()
Consumables.consumable[0].mods[1].activationRequired = 0
Consumables.consumable[0].mods[1].type = ModsTypeEnum.TEMP_IMMORTAL_CREW
Consumables.consumable[0].mods[1].value_ = 2.0
Consumables.consumable[0].nations = []
Consumables.consumable[0].nations.insert(0, None)
Consumables.consumable[0].nations[0] = 'USSR'.lower()
Consumables.consumable[0].nations.insert(1, None)
Consumables.consumable[0].nations[1] = 'USA'.lower()
Consumables.consumable[0].nations.insert(2, None)
Consumables.consumable[0].nations[2] = 'Germany'.lower()
Consumables.consumable[0].nations.insert(3, None)
Consumables.consumable[0].nations[3] = 'GB'.lower()
Consumables.consumable[0].nations.insert(4, None)
Consumables.consumable[0].nations[4] = 'Japan'.lower()
Consumables.consumable[0].nations.insert(5, None)
Consumables.consumable[0].nations[5] = 'China'.lower()
Consumables.consumable[0].nations.insert(6, None)
Consumables.consumable[0].nations[6] = 'France'.lower()
Consumables.consumable[0].planeType = []
Consumables.consumable[0].planeType.insert(0, None)
Consumables.consumable[0].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[0].planeType.insert(1, None)
Consumables.consumable[0].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[0].planeType.insert(2, None)
Consumables.consumable[0].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[0].planeType.insert(3, None)
Consumables.consumable[0].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[0].soundEffects = Dummy()
Consumables.consumable[0].soundEffects.finishSound = ''
Consumables.consumable[0].soundEffects.initSound = 'HudMedicineChest'
Consumables.consumable[0].soundEffects.tickInterval = 0.0
Consumables.consumable[0].soundEffects.tickSound = ''
Consumables.consumable[0].tickets = 0
Consumables.consumable[0].uiIndex = 4
Consumables.consumable.insert(1, None)
Consumables.consumable[1] = Dummy()
Consumables.consumable[1].affectedModules = Dummy()
Consumables.consumable[1].affectedModules.isAnimationEquipment = true
Consumables.consumable[1].affectedModules.module = []
Consumables.consumable[1].affectedModules.module.insert(0, None)
Consumables.consumable[1].affectedModules.module[0] = 'Fire'
Consumables.consumable[1].behaviour = 0
Consumables.consumable[1].buyAvailable = true
Consumables.consumable[1].chargesCount = 1
Consumables.consumable[1].coolDownTime = 1
Consumables.consumable[1].credits = 5000
Consumables.consumable[1].effectTime = 2
Consumables.consumable[1].excludeList = []
Consumables.consumable[1].excludeList.insert(0, None)
Consumables.consumable[1].excludeList[0] = 1304
Consumables.consumable[1].excludeList.insert(1, None)
Consumables.consumable[1].excludeList[1] = 1399
Consumables.consumable[1].gold = 0
Consumables.consumable[1].group = 2
Consumables.consumable[1].icoPath = 'icons/modules/supExtinguisher.png'
Consumables.consumable[1].icoPathBig = 'icons/modules/hud/supExtinguisher.png'
Consumables.consumable[1].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[1].icoPathSmall = 'icons/quests/supExtinguisher.png'
Consumables.consumable[1].id = 2
Consumables.consumable[1].includeList = []
Consumables.consumable[1].isDiscount = false
Consumables.consumable[1].isNew = false
Consumables.consumable[1].localizeTag = 'EXTINGUISHER'
Consumables.consumable[1].maxLevel = 10
Consumables.consumable[1].minLevel = 1
Consumables.consumable[1].mods = []
Consumables.consumable[1].mods.insert(0, None)
Consumables.consumable[1].mods[0] = Dummy()
Consumables.consumable[1].mods[0].activationRequired = 1
Consumables.consumable[1].mods[0].type = ModsTypeEnum.FIRE_EXTINGUISH_MANUAL
Consumables.consumable[1].mods[0].value_ = 1.0
Consumables.consumable[1].mods.insert(1, None)
Consumables.consumable[1].mods[1] = Dummy()
Consumables.consumable[1].mods[1].activationRequired = 0
Consumables.consumable[1].mods[1].type = ModsTypeEnum.FIRE_IMMUNITY
Consumables.consumable[1].mods[1].value_ = 2.0
Consumables.consumable[1].nations = []
Consumables.consumable[1].nations.insert(0, None)
Consumables.consumable[1].nations[0] = 'USSR'.lower()
Consumables.consumable[1].nations.insert(1, None)
Consumables.consumable[1].nations[1] = 'USA'.lower()
Consumables.consumable[1].nations.insert(2, None)
Consumables.consumable[1].nations[2] = 'Germany'.lower()
Consumables.consumable[1].nations.insert(3, None)
Consumables.consumable[1].nations[3] = 'GB'.lower()
Consumables.consumable[1].nations.insert(4, None)
Consumables.consumable[1].nations[4] = 'Japan'.lower()
Consumables.consumable[1].nations.insert(5, None)
Consumables.consumable[1].nations[5] = 'China'.lower()
Consumables.consumable[1].nations.insert(6, None)
Consumables.consumable[1].nations[6] = 'France'.lower()
Consumables.consumable[1].planeType = []
Consumables.consumable[1].planeType.insert(0, None)
Consumables.consumable[1].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[1].planeType.insert(1, None)
Consumables.consumable[1].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[1].planeType.insert(2, None)
Consumables.consumable[1].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[1].planeType.insert(3, None)
Consumables.consumable[1].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[1].soundEffects = Dummy()
Consumables.consumable[1].soundEffects.finishSound = ''
Consumables.consumable[1].soundEffects.initSound = 'HUDFireExtinguishing'
Consumables.consumable[1].soundEffects.tickInterval = 0.0
Consumables.consumable[1].soundEffects.tickSound = ''
Consumables.consumable[1].tickets = 0
Consumables.consumable[1].uiIndex = 1
Consumables.consumable.insert(2, None)
Consumables.consumable[2] = Dummy()
Consumables.consumable[2].behaviour = 0
Consumables.consumable[2].buyAvailable = false
Consumables.consumable[2].chargesCount = 1
Consumables.consumable[2].coolDownTime = 2
Consumables.consumable[2].credits = 5000
Consumables.consumable[2].effectTime = 2
Consumables.consumable[2].excludeList = []
Consumables.consumable[2].excludeList.insert(0, None)
Consumables.consumable[2].excludeList[0] = 1304
Consumables.consumable[2].excludeList.insert(1, None)
Consumables.consumable[2].excludeList[1] = 1399
Consumables.consumable[2].excludeList.insert(2, None)
Consumables.consumable[2].excludeList[2] = 2803
Consumables.consumable[2].excludeList.insert(3, None)
Consumables.consumable[2].excludeList[3] = 4891
Consumables.consumable[2].excludeList.insert(4, None)
Consumables.consumable[2].excludeList[4] = 6891
Consumables.consumable[2].gold = 0
Consumables.consumable[2].group = 0
Consumables.consumable[2].icoPath = 'icons/modules/modulesIconOutfitGasoline100.png'
Consumables.consumable[2].icoPathBig = 'icons/quests/iconSlotModGasoline100.png'
Consumables.consumable[2].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[2].icoPathSmall = 'icons/quests/iconSlotModGasoline100.png'
Consumables.consumable[2].id = 3
Consumables.consumable[2].includeList = []
Consumables.consumable[2].isDiscount = false
Consumables.consumable[2].isNew = false
Consumables.consumable[2].localizeTag = 'FUEL100'
Consumables.consumable[2].maxLevel = 8
Consumables.consumable[2].minLevel = 1
Consumables.consumable[2].mods = []
Consumables.consumable[2].mods.insert(0, None)
Consumables.consumable[2].mods[0] = Dummy()
Consumables.consumable[2].mods[0].activationRequired = 0
Consumables.consumable[2].mods[0].type = ModsTypeEnum.FREE_FORSAGE
Consumables.consumable[2].mods[0].value_ = 2.0
Consumables.consumable[2].nations = []
Consumables.consumable[2].nations.insert(0, None)
Consumables.consumable[2].nations[0] = 'USSR'.lower()
Consumables.consumable[2].nations.insert(1, None)
Consumables.consumable[2].nations[1] = 'Japan'.lower()
Consumables.consumable[2].nations.insert(2, None)
Consumables.consumable[2].nations[2] = 'China'.lower()
Consumables.consumable[2].planeType = []
Consumables.consumable[2].planeType.insert(0, None)
Consumables.consumable[2].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[2].planeType.insert(1, None)
Consumables.consumable[2].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[2].planeType.insert(2, None)
Consumables.consumable[2].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[2].planeType.insert(3, None)
Consumables.consumable[2].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[2].tickets = 0
Consumables.consumable[2].uiIndex = 25
Consumables.consumable.insert(3, None)
Consumables.consumable[3] = Dummy()
Consumables.consumable[3].behaviour = 0
Consumables.consumable[3].buyAvailable = false
Consumables.consumable[3].chargesCount = 1
Consumables.consumable[3].coolDownTime = 2
Consumables.consumable[3].credits = 5000
Consumables.consumable[3].effectTime = 2
Consumables.consumable[3].excludeList = []
Consumables.consumable[3].excludeList.insert(0, None)
Consumables.consumable[3].excludeList[0] = 1304
Consumables.consumable[3].excludeList.insert(1, None)
Consumables.consumable[3].excludeList[1] = 1399
Consumables.consumable[3].excludeList.insert(2, None)
Consumables.consumable[3].excludeList[2] = 1801
Consumables.consumable[3].excludeList.insert(3, None)
Consumables.consumable[3].excludeList[3] = 1891
Consumables.consumable[3].excludeList.insert(4, None)
Consumables.consumable[3].excludeList[4] = 5802
Consumables.consumable[3].excludeList.insert(5, None)
Consumables.consumable[3].excludeList[5] = 5791
Consumables.consumable[3].gold = 0
Consumables.consumable[3].group = 0
Consumables.consumable[3].icoPath = 'icons/modules/modulesIconOutfitGasoline120.png'
Consumables.consumable[3].icoPathBig = 'icons/quests/iconSlotModGasoline120.png'
Consumables.consumable[3].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[3].icoPathSmall = 'icons/quests/iconSlotModGasoline120.png'
Consumables.consumable[3].id = 4
Consumables.consumable[3].includeList = []
Consumables.consumable[3].isDiscount = false
Consumables.consumable[3].isNew = false
Consumables.consumable[3].localizeTag = 'FUEL120'
Consumables.consumable[3].maxLevel = 8
Consumables.consumable[3].minLevel = 1
Consumables.consumable[3].mods = []
Consumables.consumable[3].mods.insert(0, None)
Consumables.consumable[3].mods[0] = Dummy()
Consumables.consumable[3].mods[0].activationRequired = 0
Consumables.consumable[3].mods[0].type = ModsTypeEnum.FREE_FORSAGE
Consumables.consumable[3].mods[0].value_ = 2.0
Consumables.consumable[3].nations = []
Consumables.consumable[3].nations.insert(0, None)
Consumables.consumable[3].nations[0] = 'USA'.lower()
Consumables.consumable[3].nations.insert(1, None)
Consumables.consumable[3].nations[1] = 'Germany'.lower()
Consumables.consumable[3].nations.insert(2, None)
Consumables.consumable[3].nations[2] = 'GB'.lower()
Consumables.consumable[3].nations.insert(3, None)
Consumables.consumable[3].nations[3] = 'France'.lower()
Consumables.consumable[3].planeType = []
Consumables.consumable[3].planeType.insert(0, None)
Consumables.consumable[3].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[3].planeType.insert(1, None)
Consumables.consumable[3].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[3].planeType.insert(2, None)
Consumables.consumable[3].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[3].planeType.insert(3, None)
Consumables.consumable[3].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[3].tickets = 0
Consumables.consumable[3].uiIndex = 26
Consumables.consumable.insert(4, None)
Consumables.consumable[4] = Dummy()
Consumables.consumable[4].behaviour = 0
Consumables.consumable[4].buyAvailable = false
Consumables.consumable[4].chargesCount = 1
Consumables.consumable[4].coolDownTime = 2
Consumables.consumable[4].credits = 10000
Consumables.consumable[4].effectTime = 2
Consumables.consumable[4].excludeList = []
Consumables.consumable[4].excludeList.insert(0, None)
Consumables.consumable[4].excludeList[0] = 1304
Consumables.consumable[4].excludeList.insert(1, None)
Consumables.consumable[4].excludeList[1] = 1399
Consumables.consumable[4].gold = 0
Consumables.consumable[4].group = 0
Consumables.consumable[4].icoPath = 'icons/modules/modulesIconOutfitKerosene.png'
Consumables.consumable[4].icoPathBig = 'icons/quests/iconSlotModKerosene.png'
Consumables.consumable[4].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[4].icoPathSmall = 'icons/quests/iconSlotModKerosene.png'
Consumables.consumable[4].id = 5
Consumables.consumable[4].includeList = []
Consumables.consumable[4].includeList.insert(0, None)
Consumables.consumable[4].includeList[0] = 1801
Consumables.consumable[4].includeList.insert(1, None)
Consumables.consumable[4].includeList[1] = 1891
Consumables.consumable[4].includeList.insert(2, None)
Consumables.consumable[4].includeList[2] = 2803
Consumables.consumable[4].includeList.insert(3, None)
Consumables.consumable[4].includeList[3] = 5802
Consumables.consumable[4].includeList.insert(4, None)
Consumables.consumable[4].includeList[4] = 5791
Consumables.consumable[4].includeList.insert(5, None)
Consumables.consumable[4].includeList[5] = 6891
Consumables.consumable[4].isDiscount = false
Consumables.consumable[4].isNew = false
Consumables.consumable[4].localizeTag = 'JET_FUEL'
Consumables.consumable[4].maxLevel = 10
Consumables.consumable[4].minLevel = 9
Consumables.consumable[4].mods = []
Consumables.consumable[4].mods.insert(0, None)
Consumables.consumable[4].mods[0] = Dummy()
Consumables.consumable[4].mods[0].activationRequired = 0
Consumables.consumable[4].mods[0].type = ModsTypeEnum.FREE_FORSAGE
Consumables.consumable[4].mods[0].value_ = 2.0
Consumables.consumable[4].nations = []
Consumables.consumable[4].nations.insert(0, None)
Consumables.consumable[4].nations[0] = 'USSR'.lower()
Consumables.consumable[4].nations.insert(1, None)
Consumables.consumable[4].nations[1] = 'USA'.lower()
Consumables.consumable[4].nations.insert(2, None)
Consumables.consumable[4].nations[2] = 'Germany'.lower()
Consumables.consumable[4].nations.insert(3, None)
Consumables.consumable[4].nations[3] = 'GB'.lower()
Consumables.consumable[4].nations.insert(4, None)
Consumables.consumable[4].nations[4] = 'Japan'.lower()
Consumables.consumable[4].nations.insert(5, None)
Consumables.consumable[4].nations[5] = 'China'.lower()
Consumables.consumable[4].nations.insert(6, None)
Consumables.consumable[4].nations[6] = 'France'.lower()
Consumables.consumable[4].planeType = []
Consumables.consumable[4].planeType.insert(0, None)
Consumables.consumable[4].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[4].planeType.insert(1, None)
Consumables.consumable[4].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[4].planeType.insert(2, None)
Consumables.consumable[4].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[4].planeType.insert(3, None)
Consumables.consumable[4].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[4].tickets = 0
Consumables.consumable[4].uiIndex = 26
Consumables.consumable.insert(5, None)
Consumables.consumable[5] = Dummy()
Consumables.consumable[5].affectedModules = Dummy()
Consumables.consumable[5].affectedModules.isAnimationEquipment = false
Consumables.consumable[5].affectedModules.module = []
Consumables.consumable[5].affectedModules.module.insert(0, None)
Consumables.consumable[5].affectedModules.module[0] = 'Fire'
Consumables.consumable[5].behaviour = 2
Consumables.consumable[5].buyAvailable = true
Consumables.consumable[5].chargesCount = 1
Consumables.consumable[5].coolDownTime = 1
Consumables.consumable[5].credits = 0
Consumables.consumable[5].effectTime = 2
Consumables.consumable[5].excludeList = []
Consumables.consumable[5].excludeList.insert(0, None)
Consumables.consumable[5].excludeList[0] = 1304
Consumables.consumable[5].excludeList.insert(1, None)
Consumables.consumable[5].excludeList[1] = 1399
Consumables.consumable[5].gold = 25
Consumables.consumable[5].group = 2
Consumables.consumable[5].icoPath = 'icons/modules/supAutoExtinguisher.png'
Consumables.consumable[5].icoPathBig = 'icons/modules/hud/supImprovedExtinguisher.png'
Consumables.consumable[5].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[5].icoPathSmall = 'icons/quests/supAutoExtinguisher.png'
Consumables.consumable[5].id = 6
Consumables.consumable[5].includeList = []
Consumables.consumable[5].isDiscount = true
Consumables.consumable[5].isNew = false
Consumables.consumable[5].localizeTag = 'AUTO_EXTINGUISHER'
Consumables.consumable[5].maxLevel = 10
Consumables.consumable[5].minLevel = 1
Consumables.consumable[5].mods = []
Consumables.consumable[5].mods.insert(0, None)
Consumables.consumable[5].mods[0] = Dummy()
Consumables.consumable[5].mods[0].activationRequired = 0
Consumables.consumable[5].mods[0].type = ModsTypeEnum.FIRE_IMMUNITY
Consumables.consumable[5].mods[0].value_ = 2.0
Consumables.consumable[5].mods.insert(1, None)
Consumables.consumable[5].mods[1] = Dummy()
Consumables.consumable[5].mods[1].activationRequired = 0
Consumables.consumable[5].mods[1].type = ModsTypeEnum.FIRE_EXTINGUISH_AUTO
Consumables.consumable[5].mods[1].value_ = 1.0
Consumables.consumable[5].nations = []
Consumables.consumable[5].nations.insert(0, None)
Consumables.consumable[5].nations[0] = 'USSR'.lower()
Consumables.consumable[5].nations.insert(1, None)
Consumables.consumable[5].nations[1] = 'USA'.lower()
Consumables.consumable[5].nations.insert(2, None)
Consumables.consumable[5].nations[2] = 'Germany'.lower()
Consumables.consumable[5].nations.insert(3, None)
Consumables.consumable[5].nations[3] = 'GB'.lower()
Consumables.consumable[5].nations.insert(4, None)
Consumables.consumable[5].nations[4] = 'Japan'.lower()
Consumables.consumable[5].nations.insert(5, None)
Consumables.consumable[5].nations[5] = 'China'.lower()
Consumables.consumable[5].nations.insert(6, None)
Consumables.consumable[5].nations[6] = 'France'.lower()
Consumables.consumable[5].planeType = []
Consumables.consumable[5].planeType.insert(0, None)
Consumables.consumable[5].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[5].planeType.insert(1, None)
Consumables.consumable[5].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[5].planeType.insert(2, None)
Consumables.consumable[5].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[5].planeType.insert(3, None)
Consumables.consumable[5].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[5].soundEffects = Dummy()
Consumables.consumable[5].soundEffects.finishSound = ''
Consumables.consumable[5].soundEffects.initSound = 'HUDFireExtinguishing'
Consumables.consumable[5].soundEffects.tickInterval = 0.0
Consumables.consumable[5].soundEffects.tickSound = ''
Consumables.consumable[5].tickets = 0
Consumables.consumable[5].uiIndex = 2
Consumables.consumable.insert(6, None)
Consumables.consumable[6] = Dummy()
Consumables.consumable[6].affectedModules = Dummy()
Consumables.consumable[6].affectedModules.isAnimationEquipment = true
Consumables.consumable[6].affectedModules.module = []
Consumables.consumable[6].affectedModules.module.insert(0, None)
Consumables.consumable[6].affectedModules.module[0] = 'Pilot'
Consumables.consumable[6].affectedModules.module.insert(1, None)
Consumables.consumable[6].affectedModules.module[1] = 'Gunner1'
Consumables.consumable[6].behaviour = 0
Consumables.consumable[6].buyAvailable = true
Consumables.consumable[6].chargesCount = 1
Consumables.consumable[6].coolDownTime = 15
Consumables.consumable[6].credits = 0
Consumables.consumable[6].effectTime = 15
Consumables.consumable[6].excludeList = []
Consumables.consumable[6].excludeList.insert(0, None)
Consumables.consumable[6].excludeList[0] = 1304
Consumables.consumable[6].excludeList.insert(1, None)
Consumables.consumable[6].excludeList[1] = 1399
Consumables.consumable[6].gold = 25
Consumables.consumable[6].group = 1
Consumables.consumable[6].icoPath = 'icons/modules/supBleedStopper.png'
Consumables.consumable[6].icoPathBig = 'icons/modules/hud/supBleedStopper.png'
Consumables.consumable[6].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[6].icoPathSmall = 'icons/quests/supBleedStopper.png'
Consumables.consumable[6].id = 7
Consumables.consumable[6].includeList = []
Consumables.consumable[6].isDiscount = true
Consumables.consumable[6].isNew = false
Consumables.consumable[6].localizeTag = 'BLEED-STOPPER'
Consumables.consumable[6].maxLevel = 10
Consumables.consumable[6].minLevel = 1
Consumables.consumable[6].mods = []
Consumables.consumable[6].mods.insert(0, None)
Consumables.consumable[6].mods[0] = Dummy()
Consumables.consumable[6].mods[0].activationRequired = 1
Consumables.consumable[6].mods[0].type = ModsTypeEnum.HP_RESTORE
Consumables.consumable[6].mods[0].value_ = 1.0
Consumables.consumable[6].mods.insert(1, None)
Consumables.consumable[6].mods[1] = Dummy()
Consumables.consumable[6].mods[1].activationRequired = 0
Consumables.consumable[6].mods[1].type = ModsTypeEnum.TEMP_IMMORTAL_CREW
Consumables.consumable[6].mods[1].value_ = 2.0
Consumables.consumable[6].nations = []
Consumables.consumable[6].nations.insert(0, None)
Consumables.consumable[6].nations[0] = 'USSR'.lower()
Consumables.consumable[6].nations.insert(1, None)
Consumables.consumable[6].nations[1] = 'USA'.lower()
Consumables.consumable[6].nations.insert(2, None)
Consumables.consumable[6].nations[2] = 'Germany'.lower()
Consumables.consumable[6].nations.insert(3, None)
Consumables.consumable[6].nations[3] = 'GB'.lower()
Consumables.consumable[6].nations.insert(4, None)
Consumables.consumable[6].nations[4] = 'Japan'.lower()
Consumables.consumable[6].nations.insert(5, None)
Consumables.consumable[6].nations[5] = 'China'.lower()
Consumables.consumable[6].nations.insert(6, None)
Consumables.consumable[6].nations[6] = 'France'.lower()
Consumables.consumable[6].planeType = []
Consumables.consumable[6].planeType.insert(0, None)
Consumables.consumable[6].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[6].planeType.insert(1, None)
Consumables.consumable[6].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[6].planeType.insert(2, None)
Consumables.consumable[6].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[6].planeType.insert(3, None)
Consumables.consumable[6].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[6].soundEffects = Dummy()
Consumables.consumable[6].soundEffects.finishSound = ''
Consumables.consumable[6].soundEffects.initSound = 'HudMedicineChest'
Consumables.consumable[6].soundEffects.tickInterval = 0.0
Consumables.consumable[6].soundEffects.tickSound = ''
Consumables.consumable[6].tickets = 0
Consumables.consumable[6].uiIndex = 5
Consumables.consumable.insert(7, None)
Consumables.consumable[7] = Dummy()
Consumables.consumable[7].affectedModules = Dummy()
Consumables.consumable[7].affectedModules.isAnimationEquipment = true
Consumables.consumable[7].affectedModules.module = []
Consumables.consumable[7].affectedModules.module.insert(0, None)
Consumables.consumable[7].affectedModules.module[0] = 'Engine'
Consumables.consumable[7].behaviour = 0
Consumables.consumable[7].buyAvailable = true
Consumables.consumable[7].chargesCount = 1
Consumables.consumable[7].coolDownTime = 0
Consumables.consumable[7].credits = 3000
Consumables.consumable[7].effectTime = 0
Consumables.consumable[7].excludeList = []
Consumables.consumable[7].excludeList.insert(0, None)
Consumables.consumable[7].excludeList[0] = 1304
Consumables.consumable[7].excludeList.insert(1, None)
Consumables.consumable[7].excludeList[1] = 1399
Consumables.consumable[7].gold = 0
Consumables.consumable[7].group = 3
Consumables.consumable[7].icoPath = 'icons/modules/supAirRestarter.png'
Consumables.consumable[7].icoPathBig = 'icons/modules/hud/supAirRestarter.png'
Consumables.consumable[7].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[7].icoPathSmall = 'icons/quests/supAirRestarter.png'
Consumables.consumable[7].id = 8
Consumables.consumable[7].includeList = []
Consumables.consumable[7].isDiscount = false
Consumables.consumable[7].isNew = false
Consumables.consumable[7].localizeTag = 'AIR-RESTARTER'
Consumables.consumable[7].maxLevel = 10
Consumables.consumable[7].minLevel = 1
Consumables.consumable[7].mods = []
Consumables.consumable[7].mods.insert(0, None)
Consumables.consumable[7].mods[0] = Dummy()
Consumables.consumable[7].mods[0].activationRequired = 1
Consumables.consumable[7].mods[0].type = ModsTypeEnum.ENGINE_RESTORE
Consumables.consumable[7].mods[0].value_ = 1.0
Consumables.consumable[7].nations = []
Consumables.consumable[7].nations.insert(0, None)
Consumables.consumable[7].nations[0] = 'USSR'.lower()
Consumables.consumable[7].nations.insert(1, None)
Consumables.consumable[7].nations[1] = 'USA'.lower()
Consumables.consumable[7].nations.insert(2, None)
Consumables.consumable[7].nations[2] = 'Germany'.lower()
Consumables.consumable[7].nations.insert(3, None)
Consumables.consumable[7].nations[3] = 'GB'.lower()
Consumables.consumable[7].nations.insert(4, None)
Consumables.consumable[7].nations[4] = 'Japan'.lower()
Consumables.consumable[7].nations.insert(5, None)
Consumables.consumable[7].nations[5] = 'China'.lower()
Consumables.consumable[7].nations.insert(6, None)
Consumables.consumable[7].nations[6] = 'France'.lower()
Consumables.consumable[7].planeType = []
Consumables.consumable[7].planeType.insert(0, None)
Consumables.consumable[7].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[7].planeType.insert(1, None)
Consumables.consumable[7].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[7].planeType.insert(2, None)
Consumables.consumable[7].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[7].planeType.insert(3, None)
Consumables.consumable[7].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[7].soundEffects = Dummy()
Consumables.consumable[7].soundEffects.finishSound = ''
Consumables.consumable[7].soundEffects.initSound = 'HUDRestartTheEngine'
Consumables.consumable[7].soundEffects.tickInterval = 0.0
Consumables.consumable[7].soundEffects.tickSound = ''
Consumables.consumable[7].tickets = 0
Consumables.consumable[7].uiIndex = 7
Consumables.consumable.insert(8, None)
Consumables.consumable[8] = Dummy()
Consumables.consumable[8].behaviour = 0
Consumables.consumable[8].buyAvailable = false
Consumables.consumable[8].chargesCount = 1
Consumables.consumable[8].coolDownTime = 2
Consumables.consumable[8].credits = 1000
Consumables.consumable[8].effectTime = 0
Consumables.consumable[8].excludeList = []
Consumables.consumable[8].excludeList.insert(0, None)
Consumables.consumable[8].excludeList[0] = 1304
Consumables.consumable[8].excludeList.insert(1, None)
Consumables.consumable[8].excludeList[1] = 1399
Consumables.consumable[8].gold = 0
Consumables.consumable[8].group = 0
Consumables.consumable[8].icoPath = 'icons/modules/supSpecialFirework.png'
Consumables.consumable[8].icoPathBig = 'icons/quests/supSpecialFirework.png'
Consumables.consumable[8].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[8].icoPathSmall = 'icons/quests/supSpecialFirework.png'
Consumables.consumable[8].id = 9
Consumables.consumable[8].includeList = []
Consumables.consumable[8].isDiscount = false
Consumables.consumable[8].isNew = false
Consumables.consumable[8].localizeTag = 'FIRE_WORK'
Consumables.consumable[8].maxLevel = 10
Consumables.consumable[8].minLevel = 1
Consumables.consumable[8].mods = []
Consumables.consumable[8].mods.insert(0, None)
Consumables.consumable[8].mods[0] = Dummy()
Consumables.consumable[8].mods[0].activationRequired = 0
Consumables.consumable[8].mods[0].type = ModsTypeEnum.FIRE_WORK
Consumables.consumable[8].mods[0].value_ = 1.0
Consumables.consumable[8].nations = []
Consumables.consumable[8].nations.insert(0, None)
Consumables.consumable[8].nations[0] = 'USSR'.lower()
Consumables.consumable[8].nations.insert(1, None)
Consumables.consumable[8].nations[1] = 'USA'.lower()
Consumables.consumable[8].nations.insert(2, None)
Consumables.consumable[8].nations[2] = 'Germany'.lower()
Consumables.consumable[8].nations.insert(3, None)
Consumables.consumable[8].nations[3] = 'GB'.lower()
Consumables.consumable[8].nations.insert(4, None)
Consumables.consumable[8].nations[4] = 'Japan'.lower()
Consumables.consumable[8].nations.insert(5, None)
Consumables.consumable[8].nations[5] = 'China'.lower()
Consumables.consumable[8].nations.insert(6, None)
Consumables.consumable[8].nations[6] = 'France'.lower()
Consumables.consumable[8].planeType = []
Consumables.consumable[8].planeType.insert(0, None)
Consumables.consumable[8].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[8].planeType.insert(1, None)
Consumables.consumable[8].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[8].planeType.insert(2, None)
Consumables.consumable[8].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[8].planeType.insert(3, None)
Consumables.consumable[8].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[8].tickets = 0
Consumables.consumable[8].uiIndex = 22
Consumables.consumable.insert(9, None)
Consumables.consumable[9] = Dummy()
Consumables.consumable[9].behaviour = 1
Consumables.consumable[9].buyAvailable = false
Consumables.consumable[9].chargesCount = 1
Consumables.consumable[9].coolDownTime = 2
Consumables.consumable[9].credits = 1000
Consumables.consumable[9].effectTime = 0
Consumables.consumable[9].excludeList = []
Consumables.consumable[9].excludeList.insert(0, None)
Consumables.consumable[9].excludeList[0] = 1304
Consumables.consumable[9].excludeList.insert(1, None)
Consumables.consumable[9].excludeList[1] = 1399
Consumables.consumable[9].gold = 0
Consumables.consumable[9].group = 0
Consumables.consumable[9].icoPath = 'icons/modules/supSpecialSparklers.png'
Consumables.consumable[9].icoPathBig = 'icons/quests/supSpecialSparklers.png'
Consumables.consumable[9].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[9].icoPathSmall = 'icons/quests/supSpecialSparklers.png'
Consumables.consumable[9].id = 10
Consumables.consumable[9].includeList = []
Consumables.consumable[9].isDiscount = false
Consumables.consumable[9].isNew = false
Consumables.consumable[9].localizeTag = 'SPARKLERS'
Consumables.consumable[9].maxLevel = 10
Consumables.consumable[9].minLevel = 1
Consumables.consumable[9].mods = []
Consumables.consumable[9].mods.insert(0, None)
Consumables.consumable[9].mods[0] = Dummy()
Consumables.consumable[9].mods[0].activationRequired = 0
Consumables.consumable[9].mods[0].type = ModsTypeEnum.SPARKLERS
Consumables.consumable[9].mods[0].value_ = 1.0
Consumables.consumable[9].nations = []
Consumables.consumable[9].nations.insert(0, None)
Consumables.consumable[9].nations[0] = 'USSR'.lower()
Consumables.consumable[9].nations.insert(1, None)
Consumables.consumable[9].nations[1] = 'USA'.lower()
Consumables.consumable[9].nations.insert(2, None)
Consumables.consumable[9].nations[2] = 'Germany'.lower()
Consumables.consumable[9].nations.insert(3, None)
Consumables.consumable[9].nations[3] = 'GB'.lower()
Consumables.consumable[9].nations.insert(4, None)
Consumables.consumable[9].nations[4] = 'Japan'.lower()
Consumables.consumable[9].nations.insert(5, None)
Consumables.consumable[9].nations[5] = 'China'.lower()
Consumables.consumable[9].nations.insert(6, None)
Consumables.consumable[9].nations[6] = 'France'.lower()
Consumables.consumable[9].planeType = []
Consumables.consumable[9].planeType.insert(0, None)
Consumables.consumable[9].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[9].planeType.insert(1, None)
Consumables.consumable[9].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[9].planeType.insert(2, None)
Consumables.consumable[9].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[9].planeType.insert(3, None)
Consumables.consumable[9].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[9].tickets = 0
Consumables.consumable[9].uiIndex = 23
Consumables.consumable.insert(10, None)
Consumables.consumable[10] = Dummy()
Consumables.consumable[10].behaviour = 1
Consumables.consumable[10].buyAvailable = false
Consumables.consumable[10].chargesCount = 1
Consumables.consumable[10].coolDownTime = 2
Consumables.consumable[10].credits = 1000
Consumables.consumable[10].effectTime = 0
Consumables.consumable[10].excludeList = []
Consumables.consumable[10].excludeList.insert(0, None)
Consumables.consumable[10].excludeList[0] = 1304
Consumables.consumable[10].excludeList.insert(1, None)
Consumables.consumable[10].excludeList[1] = 1399
Consumables.consumable[10].gold = 0
Consumables.consumable[10].group = 0
Consumables.consumable[10].icoPath = 'icons/modules/supSpecialSmokeFlare.png'
Consumables.consumable[10].icoPathBig = 'icons/quests/supSpecialSmokeFlare.png'
Consumables.consumable[10].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[10].icoPathSmall = 'icons/quests/supSpecialSmokeFlare.png'
Consumables.consumable[10].id = 11
Consumables.consumable[10].includeList = []
Consumables.consumable[10].isDiscount = false
Consumables.consumable[10].isNew = false
Consumables.consumable[10].localizeTag = 'COLOR_PLUMES'
Consumables.consumable[10].maxLevel = 10
Consumables.consumable[10].minLevel = 1
Consumables.consumable[10].mods = []
Consumables.consumable[10].mods.insert(0, None)
Consumables.consumable[10].mods[0] = Dummy()
Consumables.consumable[10].mods[0].activationRequired = 0
Consumables.consumable[10].mods[0].type = ModsTypeEnum.COLOR_PLUMES
Consumables.consumable[10].mods[0].value_ = 1.0
Consumables.consumable[10].nations = []
Consumables.consumable[10].nations.insert(0, None)
Consumables.consumable[10].nations[0] = 'USSR'.lower()
Consumables.consumable[10].nations.insert(1, None)
Consumables.consumable[10].nations[1] = 'USA'.lower()
Consumables.consumable[10].nations.insert(2, None)
Consumables.consumable[10].nations[2] = 'Germany'.lower()
Consumables.consumable[10].nations.insert(3, None)
Consumables.consumable[10].nations[3] = 'GB'.lower()
Consumables.consumable[10].nations.insert(4, None)
Consumables.consumable[10].nations[4] = 'Japan'.lower()
Consumables.consumable[10].nations.insert(5, None)
Consumables.consumable[10].nations[5] = 'China'.lower()
Consumables.consumable[10].nations.insert(6, None)
Consumables.consumable[10].nations[6] = 'France'.lower()
Consumables.consumable[10].planeType = []
Consumables.consumable[10].planeType.insert(0, None)
Consumables.consumable[10].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[10].planeType.insert(1, None)
Consumables.consumable[10].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[10].planeType.insert(2, None)
Consumables.consumable[10].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[10].planeType.insert(3, None)
Consumables.consumable[10].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[10].tickets = 0
Consumables.consumable[10].uiIndex = 24
Consumables.consumable.insert(11, None)
Consumables.consumable[11] = Dummy()
Consumables.consumable[11].affectedModules = Dummy()
Consumables.consumable[11].affectedModules.isAnimationEquipment = false
Consumables.consumable[11].affectedModules.module = []
Consumables.consumable[11].affectedModules.module.insert(0, None)
Consumables.consumable[11].affectedModules.module[0] = 'CLEAR_TEMPERATURE_ENGINE'
Consumables.consumable[11].behaviour = 0
Consumables.consumable[11].buyAvailable = true
Consumables.consumable[11].chargesCount = 1
Consumables.consumable[11].coolDownTime = 0
Consumables.consumable[11].credits = 10000
Consumables.consumable[11].effectTime = 0
Consumables.consumable[11].excludeList = []
Consumables.consumable[11].excludeList.insert(0, None)
Consumables.consumable[11].excludeList[0] = 1304
Consumables.consumable[11].excludeList.insert(1, None)
Consumables.consumable[11].excludeList[1] = 1399
Consumables.consumable[11].gold = 0
Consumables.consumable[11].group = 4
Consumables.consumable[11].icoPath = 'icons/modules/supEngineHeatsink.png'
Consumables.consumable[11].icoPathBig = 'icons/quests/iconSlotModSmokeFlare.png'
Consumables.consumable[11].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[11].icoPathSmall = 'icons/quests/supEngineHeatsink.png'
Consumables.consumable[11].id = 12
Consumables.consumable[11].includeList = []
Consumables.consumable[11].isDiscount = false
Consumables.consumable[11].isNew = false
Consumables.consumable[11].localizeTag = 'ENGINE_HEATSINK'
Consumables.consumable[11].maxLevel = 10
Consumables.consumable[11].minLevel = 1
Consumables.consumable[11].mods = []
Consumables.consumable[11].mods.insert(0, None)
Consumables.consumable[11].mods[0] = Dummy()
Consumables.consumable[11].mods[0].activationRequired = 1
Consumables.consumable[11].mods[0].activationValue = 80.0
Consumables.consumable[11].mods[0].type = ModsTypeEnum.CLEAR_ENGINE_OVERHEAT
Consumables.consumable[11].mods[0].value_ = 0.264
Consumables.consumable[11].mods.insert(1, None)
Consumables.consumable[11].mods[1] = Dummy()
Consumables.consumable[11].mods[1].activationRequired = 0
Consumables.consumable[11].mods[1].type = ModsTypeEnum.FREE_FORSAGE
Consumables.consumable[11].mods[1].value_ = 0.0
Consumables.consumable[11].nations = []
Consumables.consumable[11].nations.insert(0, None)
Consumables.consumable[11].nations[0] = 'USSR'.lower()
Consumables.consumable[11].nations.insert(1, None)
Consumables.consumable[11].nations[1] = 'USA'.lower()
Consumables.consumable[11].nations.insert(2, None)
Consumables.consumable[11].nations[2] = 'Germany'.lower()
Consumables.consumable[11].nations.insert(3, None)
Consumables.consumable[11].nations[3] = 'GB'.lower()
Consumables.consumable[11].nations.insert(4, None)
Consumables.consumable[11].nations[4] = 'Japan'.lower()
Consumables.consumable[11].nations.insert(5, None)
Consumables.consumable[11].nations[5] = 'China'.lower()
Consumables.consumable[11].nations.insert(6, None)
Consumables.consumable[11].nations[6] = 'France'.lower()
Consumables.consumable[11].planeType = []
Consumables.consumable[11].planeType.insert(0, None)
Consumables.consumable[11].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[11].soundEffects = Dummy()
Consumables.consumable[11].soundEffects.finishSound = ''
Consumables.consumable[11].soundEffects.initSound = 'HUDEngineCooling'
Consumables.consumable[11].soundEffects.tickInterval = 0.0
Consumables.consumable[11].soundEffects.tickSound = ''
Consumables.consumable[11].tickets = 0
Consumables.consumable[11].uiIndex = 13
Consumables.consumable.insert(12, None)
Consumables.consumable[12] = Dummy()
Consumables.consumable[12].affectedModules = Dummy()
Consumables.consumable[12].affectedModules.isAnimationEquipment = false
Consumables.consumable[12].affectedModules.module = []
Consumables.consumable[12].affectedModules.module.insert(0, None)
Consumables.consumable[12].affectedModules.module[0] = 'CLEAR_TEMPERATURE_GUN'
Consumables.consumable[12].behaviour = 0
Consumables.consumable[12].buyAvailable = true
Consumables.consumable[12].chargesCount = 2
Consumables.consumable[12].coolDownTime = 90
Consumables.consumable[12].credits = 5000
Consumables.consumable[12].effectTime = 1
Consumables.consumable[12].excludeList = []
Consumables.consumable[12].excludeList.insert(0, None)
Consumables.consumable[12].excludeList[0] = 1304
Consumables.consumable[12].excludeList.insert(1, None)
Consumables.consumable[12].excludeList[1] = 1399
Consumables.consumable[12].gold = 0
Consumables.consumable[12].group = 5
Consumables.consumable[12].icoPath = 'icons/modules/supGunHeatsink.png'
Consumables.consumable[12].icoPathBig = 'icons/quests/iconSlotModSmokeFlare.png'
Consumables.consumable[12].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[12].icoPathSmall = 'icons/quests/supGunHeatsink.png'
Consumables.consumable[12].id = 13
Consumables.consumable[12].includeList = []
Consumables.consumable[12].isDiscount = false
Consumables.consumable[12].isNew = false
Consumables.consumable[12].localizeTag = 'GUN_HEATSINK'
Consumables.consumable[12].maxLevel = 10
Consumables.consumable[12].minLevel = 1
Consumables.consumable[12].mods = []
Consumables.consumable[12].mods.insert(0, None)
Consumables.consumable[12].mods[0] = Dummy()
Consumables.consumable[12].mods[0].activationRequired = 1
Consumables.consumable[12].mods[0].activationValue = 30.0
Consumables.consumable[12].mods[0].type = ModsTypeEnum.CLEAR_GUNS_OVERHEAT
Consumables.consumable[12].mods[0].value_ = 1.0
Consumables.consumable[12].mods.insert(1, None)
Consumables.consumable[12].mods[1] = Dummy()
Consumables.consumable[12].mods[1].activationRequired = 0
Consumables.consumable[12].mods[1].type = ModsTypeEnum.FREE_GUNS_FIRING
Consumables.consumable[12].mods[1].value_ = 2.0
Consumables.consumable[12].nations = []
Consumables.consumable[12].nations.insert(0, None)
Consumables.consumable[12].nations[0] = 'USSR'.lower()
Consumables.consumable[12].nations.insert(1, None)
Consumables.consumable[12].nations[1] = 'USA'.lower()
Consumables.consumable[12].nations.insert(2, None)
Consumables.consumable[12].nations[2] = 'Germany'.lower()
Consumables.consumable[12].nations.insert(3, None)
Consumables.consumable[12].nations[3] = 'GB'.lower()
Consumables.consumable[12].nations.insert(4, None)
Consumables.consumable[12].nations[4] = 'Japan'.lower()
Consumables.consumable[12].nations.insert(5, None)
Consumables.consumable[12].nations[5] = 'France'.lower()
Consumables.consumable[12].nations.insert(6, None)
Consumables.consumable[12].nations[6] = 'China'.lower()
Consumables.consumable[12].planeType = []
Consumables.consumable[12].planeType.insert(0, None)
Consumables.consumable[12].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[12].soundEffects = Dummy()
Consumables.consumable[12].soundEffects.finishSound = 'HUDGainRuddersTimerLast'
Consumables.consumable[12].soundEffects.initSound = 'HUDWeaponCooling'
Consumables.consumable[12].soundEffects.tickInterval = 1.0
Consumables.consumable[12].soundEffects.tickSound = 'HUDGainRuddersTimer'
Consumables.consumable[12].tickets = 0
Consumables.consumable[12].uiIndex = 19
Consumables.consumable.insert(13, None)
Consumables.consumable[13] = Dummy()
Consumables.consumable[13].affectedModules = Dummy()
Consumables.consumable[13].affectedModules.isAnimationEquipment = false
Consumables.consumable[13].affectedModules.module = []
Consumables.consumable[13].affectedModules.module.insert(0, None)
Consumables.consumable[13].affectedModules.module[0] = 'CLEAR_TEMPERATURE_ENGINE'
Consumables.consumable[13].behaviour = 0
Consumables.consumable[13].buyAvailable = true
Consumables.consumable[13].chargesCount = 1
Consumables.consumable[13].coolDownTime = 0
Consumables.consumable[13].credits = 0
Consumables.consumable[13].effectTime = 0
Consumables.consumable[13].excludeList = []
Consumables.consumable[13].excludeList.insert(0, None)
Consumables.consumable[13].excludeList[0] = 1304
Consumables.consumable[13].excludeList.insert(1, None)
Consumables.consumable[13].excludeList[1] = 1399
Consumables.consumable[13].gold = 25
Consumables.consumable[13].group = 4
Consumables.consumable[13].icoPath = 'icons/modules/supGoldEngineHeatsink.png'
Consumables.consumable[13].icoPathBig = 'icons/quests/iconSlotModSmokeFlare.png'
Consumables.consumable[13].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[13].icoPathSmall = 'icons/quests/supGoldEngineHeatsink.png'
Consumables.consumable[13].id = 14
Consumables.consumable[13].includeList = []
Consumables.consumable[13].isDiscount = true
Consumables.consumable[13].isNew = false
Consumables.consumable[13].localizeTag = 'GOLD_ENGINE_HEATSINK'
Consumables.consumable[13].maxLevel = 10
Consumables.consumable[13].minLevel = 1
Consumables.consumable[13].mods = []
Consumables.consumable[13].mods.insert(0, None)
Consumables.consumable[13].mods[0] = Dummy()
Consumables.consumable[13].mods[0].activationRequired = 1
Consumables.consumable[13].mods[0].activationValue = 80.0
Consumables.consumable[13].mods[0].type = ModsTypeEnum.CLEAR_ENGINE_OVERHEAT
Consumables.consumable[13].mods[0].value_ = 0.462
Consumables.consumable[13].mods.insert(1, None)
Consumables.consumable[13].mods[1] = Dummy()
Consumables.consumable[13].mods[1].activationRequired = 0
Consumables.consumable[13].mods[1].type = ModsTypeEnum.FREE_FORSAGE
Consumables.consumable[13].mods[1].value_ = 0.0
Consumables.consumable[13].nations = []
Consumables.consumable[13].nations.insert(0, None)
Consumables.consumable[13].nations[0] = 'USSR'.lower()
Consumables.consumable[13].nations.insert(1, None)
Consumables.consumable[13].nations[1] = 'USA'.lower()
Consumables.consumable[13].nations.insert(2, None)
Consumables.consumable[13].nations[2] = 'Germany'.lower()
Consumables.consumable[13].nations.insert(3, None)
Consumables.consumable[13].nations[3] = 'GB'.lower()
Consumables.consumable[13].nations.insert(4, None)
Consumables.consumable[13].nations[4] = 'Japan'.lower()
Consumables.consumable[13].nations.insert(5, None)
Consumables.consumable[13].nations[5] = 'France'.lower()
Consumables.consumable[13].nations.insert(6, None)
Consumables.consumable[13].nations[6] = 'China'.lower()
Consumables.consumable[13].planeType = []
Consumables.consumable[13].planeType.insert(0, None)
Consumables.consumable[13].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[13].soundEffects = Dummy()
Consumables.consumable[13].soundEffects.finishSound = ''
Consumables.consumable[13].soundEffects.initSound = 'HUDEngineCooling'
Consumables.consumable[13].soundEffects.tickInterval = 0.0
Consumables.consumable[13].soundEffects.tickSound = ''
Consumables.consumable[13].tickets = 0
Consumables.consumable[13].uiIndex = 14
Consumables.consumable.insert(14, None)
Consumables.consumable[14] = Dummy()
Consumables.consumable[14].affectedModules = Dummy()
Consumables.consumable[14].affectedModules.isAnimationEquipment = false
Consumables.consumable[14].affectedModules.module = []
Consumables.consumable[14].affectedModules.module.insert(0, None)
Consumables.consumable[14].affectedModules.module[0] = 'CLEAR_TEMPERATURE_GUN'
Consumables.consumable[14].behaviour = 0
Consumables.consumable[14].buyAvailable = true
Consumables.consumable[14].chargesCount = 3
Consumables.consumable[14].coolDownTime = 90
Consumables.consumable[14].credits = 0
Consumables.consumable[14].effectTime = 2
Consumables.consumable[14].excludeList = []
Consumables.consumable[14].excludeList.insert(0, None)
Consumables.consumable[14].excludeList[0] = 1304
Consumables.consumable[14].excludeList.insert(1, None)
Consumables.consumable[14].excludeList[1] = 1399
Consumables.consumable[14].gold = 25
Consumables.consumable[14].group = 5
Consumables.consumable[14].icoPath = 'icons/modules/supGoldGunHeatsink.png'
Consumables.consumable[14].icoPathBig = 'icons/quests/iconSlotModSmokeFlare.png'
Consumables.consumable[14].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[14].icoPathSmall = 'icons/quests/supGoldGunHeatsink.png'
Consumables.consumable[14].id = 15
Consumables.consumable[14].includeList = []
Consumables.consumable[14].isDiscount = true
Consumables.consumable[14].isNew = false
Consumables.consumable[14].localizeTag = 'GOLD_GUN_HEATSINK'
Consumables.consumable[14].maxLevel = 10
Consumables.consumable[14].minLevel = 1
Consumables.consumable[14].mods = []
Consumables.consumable[14].mods.insert(0, None)
Consumables.consumable[14].mods[0] = Dummy()
Consumables.consumable[14].mods[0].activationRequired = 1
Consumables.consumable[14].mods[0].activationValue = 30.0
Consumables.consumable[14].mods[0].type = ModsTypeEnum.CLEAR_GUNS_OVERHEAT
Consumables.consumable[14].mods[0].value_ = 1.0
Consumables.consumable[14].mods.insert(1, None)
Consumables.consumable[14].mods[1] = Dummy()
Consumables.consumable[14].mods[1].activationRequired = 0
Consumables.consumable[14].mods[1].type = ModsTypeEnum.FREE_GUNS_FIRING
Consumables.consumable[14].mods[1].value_ = 2.0
Consumables.consumable[14].nations = []
Consumables.consumable[14].nations.insert(0, None)
Consumables.consumable[14].nations[0] = 'USSR'.lower()
Consumables.consumable[14].nations.insert(1, None)
Consumables.consumable[14].nations[1] = 'USA'.lower()
Consumables.consumable[14].nations.insert(2, None)
Consumables.consumable[14].nations[2] = 'Germany'.lower()
Consumables.consumable[14].nations.insert(3, None)
Consumables.consumable[14].nations[3] = 'GB'.lower()
Consumables.consumable[14].nations.insert(4, None)
Consumables.consumable[14].nations[4] = 'Japan'.lower()
Consumables.consumable[14].nations.insert(5, None)
Consumables.consumable[14].nations[5] = 'France'.lower()
Consumables.consumable[14].nations.insert(6, None)
Consumables.consumable[14].nations[6] = 'China'.lower()
Consumables.consumable[14].planeType = []
Consumables.consumable[14].planeType.insert(0, None)
Consumables.consumable[14].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[14].soundEffects = Dummy()
Consumables.consumable[14].soundEffects.finishSound = 'HUDGainRuddersTimerLast'
Consumables.consumable[14].soundEffects.initSound = 'HUDWeaponCooling'
Consumables.consumable[14].soundEffects.tickInterval = 1.0
Consumables.consumable[14].soundEffects.tickSound = 'HUDGainRuddersTimer'
Consumables.consumable[14].tickets = 0
Consumables.consumable[14].uiIndex = 20
Consumables.consumable.insert(15, None)
Consumables.consumable[15] = Dummy()
Consumables.consumable[15].behaviour = 0
Consumables.consumable[15].buyAvailable = true
Consumables.consumable[15].chargesCount = 2
Consumables.consumable[15].coolDownTime = 90
Consumables.consumable[15].credits = 5000
Consumables.consumable[15].effectTime = 10
Consumables.consumable[15].excludeList = []
Consumables.consumable[15].excludeList.insert(0, None)
Consumables.consumable[15].excludeList[0] = 1304
Consumables.consumable[15].excludeList.insert(1, None)
Consumables.consumable[15].excludeList[1] = 1399
Consumables.consumable[15].gold = 0
Consumables.consumable[15].group = 6
Consumables.consumable[15].icoPath = 'icons/modules/supElevatorBoost.png'
Consumables.consumable[15].icoPathBig = 'icons/quests/iconSlotModSmokeFlare.png'
Consumables.consumable[15].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[15].icoPathSmall = 'icons/quests/supElevatorBoost.png'
Consumables.consumable[15].id = 16
Consumables.consumable[15].includeList = []
Consumables.consumable[15].isDiscount = false
Consumables.consumable[15].isNew = false
Consumables.consumable[15].localizeTag = 'ADRENALIN'
Consumables.consumable[15].maxLevel = 10
Consumables.consumable[15].minLevel = 1
Consumables.consumable[15].mods = []
Consumables.consumable[15].mods.insert(0, None)
Consumables.consumable[15].mods[0] = Dummy()
Consumables.consumable[15].mods[0].activationRequired = 0
Consumables.consumable[15].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Consumables.consumable[15].mods[0].value_ = 1.09
Consumables.consumable[15].mods.insert(1, None)
Consumables.consumable[15].mods[1] = Dummy()
Consumables.consumable[15].mods[1].activationRequired = 0
Consumables.consumable[15].mods[1].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Consumables.consumable[15].mods[1].value_ = 1.08
Consumables.consumable[15].mods.insert(2, None)
Consumables.consumable[15].mods[2] = Dummy()
Consumables.consumable[15].mods[2].activationRequired = 0
Consumables.consumable[15].mods[2].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Consumables.consumable[15].mods[2].value_ = 1.08
Consumables.consumable[15].nations = []
Consumables.consumable[15].nations.insert(0, None)
Consumables.consumable[15].nations[0] = 'USSR'.lower()
Consumables.consumable[15].nations.insert(1, None)
Consumables.consumable[15].nations[1] = 'USA'.lower()
Consumables.consumable[15].nations.insert(2, None)
Consumables.consumable[15].nations[2] = 'Germany'.lower()
Consumables.consumable[15].nations.insert(3, None)
Consumables.consumable[15].nations[3] = 'GB'.lower()
Consumables.consumable[15].nations.insert(4, None)
Consumables.consumable[15].nations[4] = 'Japan'.lower()
Consumables.consumable[15].nations.insert(5, None)
Consumables.consumable[15].nations[5] = 'France'.lower()
Consumables.consumable[15].nations.insert(6, None)
Consumables.consumable[15].nations[6] = 'China'.lower()
Consumables.consumable[15].planeType = []
Consumables.consumable[15].planeType.insert(0, None)
Consumables.consumable[15].planeType[0] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[15].planeType.insert(1, None)
Consumables.consumable[15].planeType[1] = consts.PLANE_TYPE.NAVY
Consumables.consumable[15].soundEffects = Dummy()
Consumables.consumable[15].soundEffects.finishSound = 'HUDGainRuddersTimerLast'
Consumables.consumable[15].soundEffects.initSound = 'HUDGainRudders'
Consumables.consumable[15].soundEffects.tickInterval = 1.0
Consumables.consumable[15].soundEffects.tickSound = 'HUDGainRuddersTimer'
Consumables.consumable[15].tickets = 0
Consumables.consumable[15].uiIndex = 16
Consumables.consumable.insert(16, None)
Consumables.consumable[16] = Dummy()
Consumables.consumable[16].behaviour = 0
Consumables.consumable[16].buyAvailable = true
Consumables.consumable[16].chargesCount = 3
Consumables.consumable[16].coolDownTime = 90
Consumables.consumable[16].credits = 0
Consumables.consumable[16].effectTime = 10
Consumables.consumable[16].excludeList = []
Consumables.consumable[16].excludeList.insert(0, None)
Consumables.consumable[16].excludeList[0] = 1304
Consumables.consumable[16].excludeList.insert(1, None)
Consumables.consumable[16].excludeList[1] = 1399
Consumables.consumable[16].gold = 25
Consumables.consumable[16].group = 6
Consumables.consumable[16].icoPath = 'icons/modules/supGoldElevatorBoost.png'
Consumables.consumable[16].icoPathBig = 'icons/quests/iconSlotModSmokeFlare.png'
Consumables.consumable[16].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[16].icoPathSmall = 'icons/quests/supGoldElevatorBoost.png'
Consumables.consumable[16].id = 17
Consumables.consumable[16].includeList = []
Consumables.consumable[16].isDiscount = true
Consumables.consumable[16].isNew = false
Consumables.consumable[16].localizeTag = 'GOLD_ADRENALIN'
Consumables.consumable[16].maxLevel = 10
Consumables.consumable[16].minLevel = 1
Consumables.consumable[16].mods = []
Consumables.consumable[16].mods.insert(0, None)
Consumables.consumable[16].mods[0] = Dummy()
Consumables.consumable[16].mods[0].activationRequired = 0
Consumables.consumable[16].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Consumables.consumable[16].mods[0].value_ = 1.09
Consumables.consumable[16].mods.insert(1, None)
Consumables.consumable[16].mods[1] = Dummy()
Consumables.consumable[16].mods[1].activationRequired = 0
Consumables.consumable[16].mods[1].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Consumables.consumable[16].mods[1].value_ = 1.08
Consumables.consumable[16].mods.insert(2, None)
Consumables.consumable[16].mods[2] = Dummy()
Consumables.consumable[16].mods[2].activationRequired = 0
Consumables.consumable[16].mods[2].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Consumables.consumable[16].mods[2].value_ = 1.08
Consumables.consumable[16].nations = []
Consumables.consumable[16].nations.insert(0, None)
Consumables.consumable[16].nations[0] = 'USSR'.lower()
Consumables.consumable[16].nations.insert(1, None)
Consumables.consumable[16].nations[1] = 'USA'.lower()
Consumables.consumable[16].nations.insert(2, None)
Consumables.consumable[16].nations[2] = 'Germany'.lower()
Consumables.consumable[16].nations.insert(3, None)
Consumables.consumable[16].nations[3] = 'GB'.lower()
Consumables.consumable[16].nations.insert(4, None)
Consumables.consumable[16].nations[4] = 'Japan'.lower()
Consumables.consumable[16].nations.insert(5, None)
Consumables.consumable[16].nations[5] = 'France'.lower()
Consumables.consumable[16].nations.insert(6, None)
Consumables.consumable[16].nations[6] = 'China'.lower()
Consumables.consumable[16].planeType = []
Consumables.consumable[16].planeType.insert(0, None)
Consumables.consumable[16].planeType[0] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[16].planeType.insert(1, None)
Consumables.consumable[16].planeType[1] = consts.PLANE_TYPE.NAVY
Consumables.consumable[16].soundEffects = Dummy()
Consumables.consumable[16].soundEffects.finishSound = 'HUDGainRuddersTimerLast'
Consumables.consumable[16].soundEffects.initSound = 'HUDGainRudders'
Consumables.consumable[16].soundEffects.tickInterval = 1.0
Consumables.consumable[16].soundEffects.tickSound = 'HUDGainRuddersTimer'
Consumables.consumable[16].tickets = 0
Consumables.consumable[16].uiIndex = 17
Consumables.consumable.insert(17, None)
Consumables.consumable[17] = Dummy()
Consumables.consumable[17].affectedModules = Dummy()
Consumables.consumable[17].affectedModules.isAnimationEquipment = true
Consumables.consumable[17].affectedModules.module = []
Consumables.consumable[17].affectedModules.module.insert(0, None)
Consumables.consumable[17].affectedModules.module[0] = 'Fire'
Consumables.consumable[17].behaviour = 0
Consumables.consumable[17].buyAvailable = false
Consumables.consumable[17].chargesCount = 2
Consumables.consumable[17].coolDownTime = 15
Consumables.consumable[17].credits = 5000
Consumables.consumable[17].effectTime = 15
Consumables.consumable[17].excludeList = []
Consumables.consumable[17].excludeList.insert(0, None)
Consumables.consumable[17].excludeList[0] = 1304
Consumables.consumable[17].excludeList.insert(1, None)
Consumables.consumable[17].excludeList[1] = 1399
Consumables.consumable[17].gold = 0
Consumables.consumable[17].group = 2
Consumables.consumable[17].icoPath = 'icons/modules/supDailyImprovedExtinguisher.png'
Consumables.consumable[17].icoPathBig = 'icons/modules/hud/supDailyImprovedExtinguisher.png'
Consumables.consumable[17].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[17].icoPathSmall = 'icons/quests/supDailyImprovedExtinguisher.png'
Consumables.consumable[17].id = 18
Consumables.consumable[17].includeList = []
Consumables.consumable[17].isDiscount = false
Consumables.consumable[17].isNew = false
Consumables.consumable[17].localizeTag = 'IMPROVED_EXTINGUISHER'
Consumables.consumable[17].maxLevel = 10
Consumables.consumable[17].minLevel = 1
Consumables.consumable[17].mods = []
Consumables.consumable[17].mods.insert(0, None)
Consumables.consumable[17].mods[0] = Dummy()
Consumables.consumable[17].mods[0].activationRequired = 1
Consumables.consumable[17].mods[0].type = ModsTypeEnum.FIRE_EXTINGUISH_MANUAL
Consumables.consumable[17].mods[0].value_ = 1.0
Consumables.consumable[17].mods.insert(1, None)
Consumables.consumable[17].mods[1] = Dummy()
Consumables.consumable[17].mods[1].activationRequired = 0
Consumables.consumable[17].mods[1].type = ModsTypeEnum.FIRE_IMMUNITY
Consumables.consumable[17].mods[1].value_ = 2.0
Consumables.consumable[17].nations = []
Consumables.consumable[17].nations.insert(0, None)
Consumables.consumable[17].nations[0] = 'USSR'.lower()
Consumables.consumable[17].nations.insert(1, None)
Consumables.consumable[17].nations[1] = 'USA'.lower()
Consumables.consumable[17].nations.insert(2, None)
Consumables.consumable[17].nations[2] = 'Germany'.lower()
Consumables.consumable[17].nations.insert(3, None)
Consumables.consumable[17].nations[3] = 'GB'.lower()
Consumables.consumable[17].nations.insert(4, None)
Consumables.consumable[17].nations[4] = 'Japan'.lower()
Consumables.consumable[17].nations.insert(5, None)
Consumables.consumable[17].nations[5] = 'China'.lower()
Consumables.consumable[17].nations.insert(6, None)
Consumables.consumable[17].nations[6] = 'France'.lower()
Consumables.consumable[17].planeType = []
Consumables.consumable[17].planeType.insert(0, None)
Consumables.consumable[17].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[17].planeType.insert(1, None)
Consumables.consumable[17].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[17].planeType.insert(2, None)
Consumables.consumable[17].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[17].planeType.insert(3, None)
Consumables.consumable[17].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[17].soundEffects = Dummy()
Consumables.consumable[17].soundEffects.finishSound = 'HUDGainRuddersTimerLast'
Consumables.consumable[17].soundEffects.initSound = 'HUDFireExtinguishing'
Consumables.consumable[17].soundEffects.tickInterval = 1.0
Consumables.consumable[17].soundEffects.tickSound = 'HUDGainRuddersTimer'
Consumables.consumable[17].tickets = 0
Consumables.consumable[17].uiIndex = 3
Consumables.consumable.insert(18, None)
Consumables.consumable[18] = Dummy()
Consumables.consumable[18].behaviour = 2
Consumables.consumable[18].buyAvailable = true
Consumables.consumable[18].chargesCount = 1
Consumables.consumable[18].coolDownTime = 0
Consumables.consumable[18].credits = 0
Consumables.consumable[18].effectTime = 0
Consumables.consumable[18].excludeList = []
Consumables.consumable[18].excludeList.insert(0, None)
Consumables.consumable[18].excludeList[0] = 1304
Consumables.consumable[18].excludeList.insert(1, None)
Consumables.consumable[18].excludeList[1] = 1399
Consumables.consumable[18].gold = 25
Consumables.consumable[18].group = 3
Consumables.consumable[18].icoPath = 'icons/modules/supEngineRestarter.png'
Consumables.consumable[18].icoPathBig = 'icons/quests/iconSlotModSmokeFlare.png'
Consumables.consumable[18].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[18].icoPathSmall = 'icons/quests/supEngineRestarter.png'
Consumables.consumable[18].id = 19
Consumables.consumable[18].includeList = []
Consumables.consumable[18].isDiscount = true
Consumables.consumable[18].isNew = false
Consumables.consumable[18].localizeTag = 'AUTO_RESTARTER'
Consumables.consumable[18].maxLevel = 10
Consumables.consumable[18].minLevel = 1
Consumables.consumable[18].mods = []
Consumables.consumable[18].mods.insert(0, None)
Consumables.consumable[18].mods[0] = Dummy()
Consumables.consumable[18].mods[0].activationRequired = 1
Consumables.consumable[18].mods[0].type = ModsTypeEnum.AUTO_ENGINE_RESTORE
Consumables.consumable[18].mods[0].value_ = 1.0
Consumables.consumable[18].nations = []
Consumables.consumable[18].nations.insert(0, None)
Consumables.consumable[18].nations[0] = 'USSR'.lower()
Consumables.consumable[18].nations.insert(1, None)
Consumables.consumable[18].nations[1] = 'USA'.lower()
Consumables.consumable[18].nations.insert(2, None)
Consumables.consumable[18].nations[2] = 'Germany'.lower()
Consumables.consumable[18].nations.insert(3, None)
Consumables.consumable[18].nations[3] = 'GB'.lower()
Consumables.consumable[18].nations.insert(4, None)
Consumables.consumable[18].nations[4] = 'Japan'.lower()
Consumables.consumable[18].nations.insert(5, None)
Consumables.consumable[18].nations[5] = 'China'.lower()
Consumables.consumable[18].nations.insert(6, None)
Consumables.consumable[18].nations[6] = 'France'.lower()
Consumables.consumable[18].planeType = []
Consumables.consumable[18].planeType.insert(0, None)
Consumables.consumable[18].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[18].planeType.insert(1, None)
Consumables.consumable[18].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[18].planeType.insert(2, None)
Consumables.consumable[18].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[18].planeType.insert(3, None)
Consumables.consumable[18].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[18].soundEffects = Dummy()
Consumables.consumable[18].soundEffects.finishSound = ''
Consumables.consumable[18].soundEffects.initSound = 'HudAutoRestarter'
Consumables.consumable[18].soundEffects.tickInterval = 0.0
Consumables.consumable[18].soundEffects.tickSound = ''
Consumables.consumable[18].tickets = 0
Consumables.consumable[18].uiIndex = 8
Consumables.consumable.insert(19, None)
Consumables.consumable[19] = Dummy()
Consumables.consumable[19].behaviour = 0
Consumables.consumable[19].buyAvailable = false
Consumables.consumable[19].chargesCount = 1
Consumables.consumable[19].coolDownTime = 120
Consumables.consumable[19].credits = 5000
Consumables.consumable[19].effectTime = 11
Consumables.consumable[19].excludeList = []
Consumables.consumable[19].excludeList.insert(0, None)
Consumables.consumable[19].excludeList[0] = 1304
Consumables.consumable[19].excludeList.insert(1, None)
Consumables.consumable[19].excludeList[1] = 1399
Consumables.consumable[19].excludeList.insert(2, None)
Consumables.consumable[19].excludeList[2] = 4891
Consumables.consumable[19].gold = 0
Consumables.consumable[19].group = 4
Consumables.consumable[19].icoPath = 'icons/modules/supForsageMix.png'
Consumables.consumable[19].icoPathBig = 'icons/quests/iconSlotModSmokeFlare.png'
Consumables.consumable[19].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[19].icoPathSmall = 'icons/quests/supForsageMix.png'
Consumables.consumable[19].id = 20
Consumables.consumable[19].includeList = []
Consumables.consumable[19].isDiscount = false
Consumables.consumable[19].isNew = false
Consumables.consumable[19].localizeTag = 'WEP_BOOSTER'
Consumables.consumable[19].maxLevel = 10
Consumables.consumable[19].minLevel = 1
Consumables.consumable[19].mods = []
Consumables.consumable[19].mods.insert(0, None)
Consumables.consumable[19].mods[0] = Dummy()
Consumables.consumable[19].mods[0].activationRequired = 0
Consumables.consumable[19].mods[0].type = ModsTypeEnum.LOCK_ENGINE_POWER
Consumables.consumable[19].mods[0].value_ = 1.85
Consumables.consumable[19].mods.insert(1, None)
Consumables.consumable[19].mods[1] = Dummy()
Consumables.consumable[19].mods[1].activationRequired = 0
Consumables.consumable[19].mods[1].type = ModsTypeEnum.MAX_SPEED
Consumables.consumable[19].mods[1].value_ = 1.65
Consumables.consumable[19].nations = []
Consumables.consumable[19].nations.insert(0, None)
Consumables.consumable[19].nations[0] = 'USSR'.lower()
Consumables.consumable[19].nations.insert(1, None)
Consumables.consumable[19].nations[1] = 'USA'.lower()
Consumables.consumable[19].nations.insert(2, None)
Consumables.consumable[19].nations[2] = 'Germany'.lower()
Consumables.consumable[19].nations.insert(3, None)
Consumables.consumable[19].nations[3] = 'GB'.lower()
Consumables.consumable[19].nations.insert(4, None)
Consumables.consumable[19].nations[4] = 'Japan'.lower()
Consumables.consumable[19].nations.insert(5, None)
Consumables.consumable[19].nations[5] = 'France'.lower()
Consumables.consumable[19].nations.insert(6, None)
Consumables.consumable[19].nations[6] = 'China'.lower()
Consumables.consumable[19].planeType = []
Consumables.consumable[19].planeType.insert(0, None)
Consumables.consumable[19].planeType[0] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[19].planeType.insert(1, None)
Consumables.consumable[19].planeType[1] = consts.PLANE_TYPE.NAVY
Consumables.consumable[19].soundEffects = Dummy()
Consumables.consumable[19].soundEffects.finishSound = 'HUDGainRuddersTimerLast'
Consumables.consumable[19].soundEffects.initSound = 'HudWebBooster'
Consumables.consumable[19].soundEffects.tickInterval = 1.0
Consumables.consumable[19].soundEffects.tickSound = 'HUDGainRuddersTimer'
Consumables.consumable[19].tickets = 0
Consumables.consumable[19].uiIndex = 90
Consumables.consumable.insert(20, None)
Consumables.consumable[20] = Dummy()
Consumables.consumable[20].behaviour = 2
Consumables.consumable[20].buyAvailable = true
Consumables.consumable[20].chargesCount = 1
Consumables.consumable[20].coolDownTime = 0
Consumables.consumable[20].credits = 0
Consumables.consumable[20].effectTime = 0
Consumables.consumable[20].excludeList = []
Consumables.consumable[20].excludeList.insert(0, None)
Consumables.consumable[20].excludeList[0] = 1304
Consumables.consumable[20].excludeList.insert(1, None)
Consumables.consumable[20].excludeList[1] = 1399
Consumables.consumable[20].gold = 25
Consumables.consumable[20].group = 7
Consumables.consumable[20].icoPath = 'icons/modules/supTrimmingGold.png'
Consumables.consumable[20].icoPathBig = 'icons/modules/hud/supImprovedExtinguisher.png'
Consumables.consumable[20].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[20].icoPathSmall = 'icons/quests/supTrimmingGold.png'
Consumables.consumable[20].id = 21
Consumables.consumable[20].includeList = []
Consumables.consumable[20].isDiscount = true
Consumables.consumable[20].isNew = false
Consumables.consumable[20].localizeTag = 'AUTO_FIX_TAIL_AND_WINGS'
Consumables.consumable[20].maxLevel = 10
Consumables.consumable[20].minLevel = 1
Consumables.consumable[20].mods = []
Consumables.consumable[20].mods.insert(0, None)
Consumables.consumable[20].mods[0] = Dummy()
Consumables.consumable[20].mods[0].activationRequired = 1
Consumables.consumable[20].mods[0].type = ModsTypeEnum.FIX_TAIL_AND_WINGS
Consumables.consumable[20].mods[0].value_ = 1.0
Consumables.consumable[20].nations = []
Consumables.consumable[20].nations.insert(0, None)
Consumables.consumable[20].nations[0] = 'USSR'.lower()
Consumables.consumable[20].nations.insert(1, None)
Consumables.consumable[20].nations[1] = 'USA'.lower()
Consumables.consumable[20].nations.insert(2, None)
Consumables.consumable[20].nations[2] = 'Germany'.lower()
Consumables.consumable[20].nations.insert(3, None)
Consumables.consumable[20].nations[3] = 'GB'.lower()
Consumables.consumable[20].nations.insert(4, None)
Consumables.consumable[20].nations[4] = 'Japan'.lower()
Consumables.consumable[20].nations.insert(5, None)
Consumables.consumable[20].nations[5] = 'China'.lower()
Consumables.consumable[20].nations.insert(6, None)
Consumables.consumable[20].nations[6] = 'France'.lower()
Consumables.consumable[20].planeType = []
Consumables.consumable[20].planeType.insert(0, None)
Consumables.consumable[20].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[20].planeType.insert(1, None)
Consumables.consumable[20].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[20].planeType.insert(2, None)
Consumables.consumable[20].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[20].planeType.insert(3, None)
Consumables.consumable[20].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[20].soundEffects = Dummy()
Consumables.consumable[20].soundEffects.finishSound = ''
Consumables.consumable[20].soundEffects.initSound = 'HUDFireExtinguishing'
Consumables.consumable[20].soundEffects.tickInterval = 0.0
Consumables.consumable[20].soundEffects.tickSound = ''
Consumables.consumable[20].tickets = 0
Consumables.consumable[20].uiIndex = 11
Consumables.consumable.insert(21, None)
Consumables.consumable[21] = Dummy()
Consumables.consumable[21].affectedModules = Dummy()
Consumables.consumable[21].affectedModules.isAnimationEquipment = true
Consumables.consumable[21].affectedModules.module = []
Consumables.consumable[21].affectedModules.module.insert(0, None)
Consumables.consumable[21].affectedModules.module[0] = 'LeftWing'
Consumables.consumable[21].affectedModules.module.insert(1, None)
Consumables.consumable[21].affectedModules.module[1] = 'RightWing'
Consumables.consumable[21].affectedModules.module.insert(2, None)
Consumables.consumable[21].affectedModules.module[2] = 'Tail'
Consumables.consumable[21].behaviour = 0
Consumables.consumable[21].buyAvailable = true
Consumables.consumable[21].chargesCount = 1
Consumables.consumable[21].coolDownTime = 0
Consumables.consumable[21].credits = 3000
Consumables.consumable[21].effectTime = 0
Consumables.consumable[21].excludeList = []
Consumables.consumable[21].excludeList.insert(0, None)
Consumables.consumable[21].excludeList[0] = 1304
Consumables.consumable[21].excludeList.insert(1, None)
Consumables.consumable[21].excludeList[1] = 1399
Consumables.consumable[21].gold = 0
Consumables.consumable[21].group = 7
Consumables.consumable[21].icoPath = 'icons/modules/supTrimming.png'
Consumables.consumable[21].icoPathBig = 'icons/modules/hud/supTrimming.png'
Consumables.consumable[21].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[21].icoPathSmall = 'icons/quests/supTrimming.png'
Consumables.consumable[21].id = 22
Consumables.consumable[21].includeList = []
Consumables.consumable[21].isDiscount = false
Consumables.consumable[21].isNew = false
Consumables.consumable[21].localizeTag = 'FIX_TAIL_AND_WINGS'
Consumables.consumable[21].maxLevel = 10
Consumables.consumable[21].minLevel = 1
Consumables.consumable[21].mods = []
Consumables.consumable[21].mods.insert(0, None)
Consumables.consumable[21].mods[0] = Dummy()
Consumables.consumable[21].mods[0].activationRequired = 1
Consumables.consumable[21].mods[0].type = ModsTypeEnum.FIX_TAIL_AND_WINGS
Consumables.consumable[21].mods[0].value_ = 1.0
Consumables.consumable[21].nations = []
Consumables.consumable[21].nations.insert(0, None)
Consumables.consumable[21].nations[0] = 'USSR'.lower()
Consumables.consumable[21].nations.insert(1, None)
Consumables.consumable[21].nations[1] = 'USA'.lower()
Consumables.consumable[21].nations.insert(2, None)
Consumables.consumable[21].nations[2] = 'Germany'.lower()
Consumables.consumable[21].nations.insert(3, None)
Consumables.consumable[21].nations[3] = 'GB'.lower()
Consumables.consumable[21].nations.insert(4, None)
Consumables.consumable[21].nations[4] = 'Japan'.lower()
Consumables.consumable[21].nations.insert(5, None)
Consumables.consumable[21].nations[5] = 'China'.lower()
Consumables.consumable[21].nations.insert(6, None)
Consumables.consumable[21].nations[6] = 'France'.lower()
Consumables.consumable[21].planeType = []
Consumables.consumable[21].planeType.insert(0, None)
Consumables.consumable[21].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[21].planeType.insert(1, None)
Consumables.consumable[21].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[21].planeType.insert(2, None)
Consumables.consumable[21].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[21].planeType.insert(3, None)
Consumables.consumable[21].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[21].soundEffects = Dummy()
Consumables.consumable[21].soundEffects.finishSound = ''
Consumables.consumable[21].soundEffects.initSound = 'HUDFireExtinguishing'
Consumables.consumable[21].soundEffects.tickInterval = 0.0
Consumables.consumable[21].soundEffects.tickSound = ''
Consumables.consumable[21].tickets = 0
Consumables.consumable[21].uiIndex = 10
Consumables.consumable.insert(22, None)
Consumables.consumable[22] = Dummy()
Consumables.consumable[22].affectedModules = Dummy()
Consumables.consumable[22].affectedModules.isAnimationEquipment = true
Consumables.consumable[22].affectedModules.module = []
Consumables.consumable[22].affectedModules.module.insert(0, None)
Consumables.consumable[22].affectedModules.module[0] = 'Pilot'
Consumables.consumable[22].affectedModules.module.insert(1, None)
Consumables.consumable[22].affectedModules.module[1] = 'Gunner1'
Consumables.consumable[22].behaviour = 0
Consumables.consumable[22].buyAvailable = false
Consumables.consumable[22].chargesCount = 2
Consumables.consumable[22].coolDownTime = 15
Consumables.consumable[22].credits = 5000
Consumables.consumable[22].effectTime = 15
Consumables.consumable[22].excludeList = []
Consumables.consumable[22].excludeList.insert(0, None)
Consumables.consumable[22].excludeList[0] = 1304
Consumables.consumable[22].excludeList.insert(1, None)
Consumables.consumable[22].excludeList[1] = 1399
Consumables.consumable[22].gold = 0
Consumables.consumable[22].group = 1
Consumables.consumable[22].icoPath = 'icons/modules/supDailyBleedStopper.png'
Consumables.consumable[22].icoPathBig = 'icons/modules/hud/supDailyBleedStopper.png'
Consumables.consumable[22].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[22].icoPathSmall = 'icons/quests/supDailyBleedStopper.png'
Consumables.consumable[22].id = 23
Consumables.consumable[22].includeList = []
Consumables.consumable[22].isDiscount = false
Consumables.consumable[22].isNew = false
Consumables.consumable[22].localizeTag = 'DAILY_BLEED_STOPPER'
Consumables.consumable[22].maxLevel = 10
Consumables.consumable[22].minLevel = 1
Consumables.consumable[22].mods = []
Consumables.consumable[22].mods.insert(0, None)
Consumables.consumable[22].mods[0] = Dummy()
Consumables.consumable[22].mods[0].activationRequired = 1
Consumables.consumable[22].mods[0].type = ModsTypeEnum.HP_RESTORE
Consumables.consumable[22].mods[0].value_ = 1.0
Consumables.consumable[22].mods.insert(1, None)
Consumables.consumable[22].mods[1] = Dummy()
Consumables.consumable[22].mods[1].activationRequired = 0
Consumables.consumable[22].mods[1].type = ModsTypeEnum.TEMP_IMMORTAL_CREW
Consumables.consumable[22].mods[1].value_ = 2.0
Consumables.consumable[22].nations = []
Consumables.consumable[22].nations.insert(0, None)
Consumables.consumable[22].nations[0] = 'USSR'.lower()
Consumables.consumable[22].nations.insert(1, None)
Consumables.consumable[22].nations[1] = 'USA'.lower()
Consumables.consumable[22].nations.insert(2, None)
Consumables.consumable[22].nations[2] = 'Germany'.lower()
Consumables.consumable[22].nations.insert(3, None)
Consumables.consumable[22].nations[3] = 'GB'.lower()
Consumables.consumable[22].nations.insert(4, None)
Consumables.consumable[22].nations[4] = 'Japan'.lower()
Consumables.consumable[22].nations.insert(5, None)
Consumables.consumable[22].nations[5] = 'China'.lower()
Consumables.consumable[22].nations.insert(6, None)
Consumables.consumable[22].nations[6] = 'France'.lower()
Consumables.consumable[22].planeType = []
Consumables.consumable[22].planeType.insert(0, None)
Consumables.consumable[22].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[22].planeType.insert(1, None)
Consumables.consumable[22].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[22].planeType.insert(2, None)
Consumables.consumable[22].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[22].planeType.insert(3, None)
Consumables.consumable[22].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[22].soundEffects = Dummy()
Consumables.consumable[22].soundEffects.finishSound = ''
Consumables.consumable[22].soundEffects.initSound = 'HudMedicineChest'
Consumables.consumable[22].soundEffects.tickInterval = 0.0
Consumables.consumable[22].soundEffects.tickSound = ''
Consumables.consumable[22].tickets = 0
Consumables.consumable[22].uiIndex = 6
Consumables.consumable.insert(23, None)
Consumables.consumable[23] = Dummy()
Consumables.consumable[23].affectedModules = Dummy()
Consumables.consumable[23].affectedModules.isAnimationEquipment = false
Consumables.consumable[23].affectedModules.module = []
Consumables.consumable[23].affectedModules.module.insert(0, None)
Consumables.consumable[23].affectedModules.module[0] = 'CLEAR_TEMPERATURE_ENGINE'
Consumables.consumable[23].behaviour = 0
Consumables.consumable[23].buyAvailable = false
Consumables.consumable[23].chargesCount = 1
Consumables.consumable[23].coolDownTime = 0
Consumables.consumable[23].credits = 5000
Consumables.consumable[23].effectTime = 0
Consumables.consumable[23].excludeList = []
Consumables.consumable[23].excludeList.insert(0, None)
Consumables.consumable[23].excludeList[0] = 1304
Consumables.consumable[23].excludeList.insert(1, None)
Consumables.consumable[23].excludeList[1] = 1399
Consumables.consumable[23].gold = 0
Consumables.consumable[23].group = 4
Consumables.consumable[23].icoPath = 'icons/modules/supDailyEngineHeatsink.png'
Consumables.consumable[23].icoPathBig = 'icons/quests/supDailyEngineHeatsink.png'
Consumables.consumable[23].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[23].icoPathSmall = 'icons/quests/supDailyEngineHeatsink.png'
Consumables.consumable[23].id = 24
Consumables.consumable[23].includeList = []
Consumables.consumable[23].isDiscount = false
Consumables.consumable[23].isNew = false
Consumables.consumable[23].localizeTag = 'DAILY_ENGINE_HEATSINK'
Consumables.consumable[23].maxLevel = 10
Consumables.consumable[23].minLevel = 1
Consumables.consumable[23].mods = []
Consumables.consumable[23].mods.insert(0, None)
Consumables.consumable[23].mods[0] = Dummy()
Consumables.consumable[23].mods[0].activationRequired = 1
Consumables.consumable[23].mods[0].activationValue = 80.0
Consumables.consumable[23].mods[0].type = ModsTypeEnum.CLEAR_ENGINE_OVERHEAT
Consumables.consumable[23].mods[0].value_ = 0.333
Consumables.consumable[23].mods.insert(1, None)
Consumables.consumable[23].mods[1] = Dummy()
Consumables.consumable[23].mods[1].activationRequired = 0
Consumables.consumable[23].mods[1].type = ModsTypeEnum.FREE_FORSAGE
Consumables.consumable[23].mods[1].value_ = 0.0
Consumables.consumable[23].nations = []
Consumables.consumable[23].nations.insert(0, None)
Consumables.consumable[23].nations[0] = 'USSR'.lower()
Consumables.consumable[23].nations.insert(1, None)
Consumables.consumable[23].nations[1] = 'USA'.lower()
Consumables.consumable[23].nations.insert(2, None)
Consumables.consumable[23].nations[2] = 'Germany'.lower()
Consumables.consumable[23].nations.insert(3, None)
Consumables.consumable[23].nations[3] = 'GB'.lower()
Consumables.consumable[23].nations.insert(4, None)
Consumables.consumable[23].nations[4] = 'Japan'.lower()
Consumables.consumable[23].nations.insert(5, None)
Consumables.consumable[23].nations[5] = 'China'.lower()
Consumables.consumable[23].nations.insert(6, None)
Consumables.consumable[23].nations[6] = 'France'.lower()
Consumables.consumable[23].planeType = []
Consumables.consumable[23].planeType.insert(0, None)
Consumables.consumable[23].planeType[0] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[23].soundEffects = Dummy()
Consumables.consumable[23].soundEffects.finishSound = ''
Consumables.consumable[23].soundEffects.initSound = 'HUDEngineCooling'
Consumables.consumable[23].soundEffects.tickInterval = 0.0
Consumables.consumable[23].soundEffects.tickSound = ''
Consumables.consumable[23].tickets = 0
Consumables.consumable[23].uiIndex = 15
Consumables.consumable.insert(24, None)
Consumables.consumable[24] = Dummy()
Consumables.consumable[24].affectedModules = Dummy()
Consumables.consumable[24].affectedModules.isAnimationEquipment = false
Consumables.consumable[24].affectedModules.module = []
Consumables.consumable[24].affectedModules.module.insert(0, None)
Consumables.consumable[24].affectedModules.module[0] = 'CLEAR_TEMPERATURE_GUN'
Consumables.consumable[24].behaviour = 0
Consumables.consumable[24].buyAvailable = false
Consumables.consumable[24].chargesCount = 2
Consumables.consumable[24].coolDownTime = 90
Consumables.consumable[24].credits = 5000
Consumables.consumable[24].effectTime = 5
Consumables.consumable[24].excludeList = []
Consumables.consumable[24].excludeList.insert(0, None)
Consumables.consumable[24].excludeList[0] = 1304
Consumables.consumable[24].excludeList.insert(1, None)
Consumables.consumable[24].excludeList[1] = 1399
Consumables.consumable[24].gold = 0
Consumables.consumable[24].group = 5
Consumables.consumable[24].icoPath = 'icons/modules/supDailyGunHeatsink.png'
Consumables.consumable[24].icoPathBig = 'icons/quests/supDailyGunHeatsink.png'
Consumables.consumable[24].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[24].icoPathSmall = 'icons/quests/supDailyGunHeatsink.png'
Consumables.consumable[24].id = 25
Consumables.consumable[24].includeList = []
Consumables.consumable[24].isDiscount = false
Consumables.consumable[24].isNew = false
Consumables.consumable[24].localizeTag = 'DAILY_GUN_HEATSINK'
Consumables.consumable[24].maxLevel = 10
Consumables.consumable[24].minLevel = 1
Consumables.consumable[24].mods = []
Consumables.consumable[24].mods.insert(0, None)
Consumables.consumable[24].mods[0] = Dummy()
Consumables.consumable[24].mods[0].activationRequired = 1
Consumables.consumable[24].mods[0].activationValue = 30.0
Consumables.consumable[24].mods[0].type = ModsTypeEnum.CLEAR_GUNS_OVERHEAT
Consumables.consumable[24].mods[0].value_ = 1.0
Consumables.consumable[24].mods.insert(1, None)
Consumables.consumable[24].mods[1] = Dummy()
Consumables.consumable[24].mods[1].activationRequired = 0
Consumables.consumable[24].mods[1].type = ModsTypeEnum.FREE_GUNS_FIRING
Consumables.consumable[24].mods[1].value_ = 10.0
Consumables.consumable[24].nations = []
Consumables.consumable[24].nations.insert(0, None)
Consumables.consumable[24].nations[0] = 'USSR'.lower()
Consumables.consumable[24].nations.insert(1, None)
Consumables.consumable[24].nations[1] = 'USA'.lower()
Consumables.consumable[24].nations.insert(2, None)
Consumables.consumable[24].nations[2] = 'Germany'.lower()
Consumables.consumable[24].nations.insert(3, None)
Consumables.consumable[24].nations[3] = 'GB'.lower()
Consumables.consumable[24].nations.insert(4, None)
Consumables.consumable[24].nations[4] = 'Japan'.lower()
Consumables.consumable[24].nations.insert(5, None)
Consumables.consumable[24].nations[5] = 'France'.lower()
Consumables.consumable[24].nations.insert(6, None)
Consumables.consumable[24].nations[6] = 'China'.lower()
Consumables.consumable[24].planeType = []
Consumables.consumable[24].planeType.insert(0, None)
Consumables.consumable[24].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[24].soundEffects = Dummy()
Consumables.consumable[24].soundEffects.finishSound = 'HUDGainRuddersTimerLast'
Consumables.consumable[24].soundEffects.initSound = 'HUDWeaponCooling'
Consumables.consumable[24].soundEffects.tickInterval = 1.0
Consumables.consumable[24].soundEffects.tickSound = 'HUDGainRuddersTimer'
Consumables.consumable[24].tickets = 0
Consumables.consumable[24].uiIndex = 21
Consumables.consumable.insert(25, None)
Consumables.consumable[25] = Dummy()
Consumables.consumable[25].behaviour = 0
Consumables.consumable[25].buyAvailable = false
Consumables.consumable[25].chargesCount = 2
Consumables.consumable[25].coolDownTime = 45
Consumables.consumable[25].credits = 5000
Consumables.consumable[25].effectTime = 10
Consumables.consumable[25].excludeList = []
Consumables.consumable[25].excludeList.insert(0, None)
Consumables.consumable[25].excludeList[0] = 1304
Consumables.consumable[25].excludeList.insert(1, None)
Consumables.consumable[25].excludeList[1] = 1399
Consumables.consumable[25].gold = 0
Consumables.consumable[25].group = 6
Consumables.consumable[25].icoPath = 'icons/modules/supDailyElevatorBoost.png'
Consumables.consumable[25].icoPathBig = 'icons/quests/supDailyElevatorBoost.png'
Consumables.consumable[25].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[25].icoPathSmall = 'icons/quests/supDailyElevatorBoost.png'
Consumables.consumable[25].id = 26
Consumables.consumable[25].includeList = []
Consumables.consumable[25].isDiscount = false
Consumables.consumable[25].isNew = false
Consumables.consumable[25].localizeTag = 'DAILY_ADRENALIN'
Consumables.consumable[25].maxLevel = 10
Consumables.consumable[25].minLevel = 1
Consumables.consumable[25].mods = []
Consumables.consumable[25].mods.insert(0, None)
Consumables.consumable[25].mods[0] = Dummy()
Consumables.consumable[25].mods[0].activationRequired = 0
Consumables.consumable[25].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Consumables.consumable[25].mods[0].value_ = 1.09
Consumables.consumable[25].mods.insert(1, None)
Consumables.consumable[25].mods[1] = Dummy()
Consumables.consumable[25].mods[1].activationRequired = 0
Consumables.consumable[25].mods[1].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Consumables.consumable[25].mods[1].value_ = 1.08
Consumables.consumable[25].mods.insert(2, None)
Consumables.consumable[25].mods[2] = Dummy()
Consumables.consumable[25].mods[2].activationRequired = 0
Consumables.consumable[25].mods[2].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Consumables.consumable[25].mods[2].value_ = 1.08
Consumables.consumable[25].nations = []
Consumables.consumable[25].nations.insert(0, None)
Consumables.consumable[25].nations[0] = 'USSR'.lower()
Consumables.consumable[25].nations.insert(1, None)
Consumables.consumable[25].nations[1] = 'USA'.lower()
Consumables.consumable[25].nations.insert(2, None)
Consumables.consumable[25].nations[2] = 'Germany'.lower()
Consumables.consumable[25].nations.insert(3, None)
Consumables.consumable[25].nations[3] = 'GB'.lower()
Consumables.consumable[25].nations.insert(4, None)
Consumables.consumable[25].nations[4] = 'Japan'.lower()
Consumables.consumable[25].nations.insert(5, None)
Consumables.consumable[25].nations[5] = 'France'.lower()
Consumables.consumable[25].nations.insert(6, None)
Consumables.consumable[25].nations[6] = 'China'.lower()
Consumables.consumable[25].planeType = []
Consumables.consumable[25].planeType.insert(0, None)
Consumables.consumable[25].planeType[0] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[25].planeType.insert(1, None)
Consumables.consumable[25].planeType[1] = consts.PLANE_TYPE.NAVY
Consumables.consumable[25].soundEffects = Dummy()
Consumables.consumable[25].soundEffects.finishSound = 'HUDGainRuddersTimerLast'
Consumables.consumable[25].soundEffects.initSound = 'HUDGainRudders'
Consumables.consumable[25].soundEffects.tickInterval = 1.0
Consumables.consumable[25].soundEffects.tickSound = 'HUDGainRuddersTimer'
Consumables.consumable[25].tickets = 0
Consumables.consumable[25].uiIndex = 18
Consumables.consumable.insert(26, None)
Consumables.consumable[26] = Dummy()
Consumables.consumable[26].affectedModules = Dummy()
Consumables.consumable[26].affectedModules.isAnimationEquipment = true
Consumables.consumable[26].affectedModules.module = []
Consumables.consumable[26].affectedModules.module.insert(0, None)
Consumables.consumable[26].affectedModules.module[0] = 'LeftWing'
Consumables.consumable[26].affectedModules.module.insert(1, None)
Consumables.consumable[26].affectedModules.module[1] = 'RightWing'
Consumables.consumable[26].affectedModules.module.insert(2, None)
Consumables.consumable[26].affectedModules.module[2] = 'Tail'
Consumables.consumable[26].behaviour = 0
Consumables.consumable[26].buyAvailable = false
Consumables.consumable[26].chargesCount = 2
Consumables.consumable[26].coolDownTime = 10
Consumables.consumable[26].credits = 5000
Consumables.consumable[26].effectTime = 0
Consumables.consumable[26].excludeList = []
Consumables.consumable[26].excludeList.insert(0, None)
Consumables.consumable[26].excludeList[0] = 1304
Consumables.consumable[26].excludeList.insert(1, None)
Consumables.consumable[26].excludeList[1] = 1399
Consumables.consumable[26].gold = 0
Consumables.consumable[26].group = 7
Consumables.consumable[26].icoPath = 'icons/modules/supDailyTrimming.png'
Consumables.consumable[26].icoPathBig = 'icons/modules/hud/supDailyTrimming.png'
Consumables.consumable[26].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[26].icoPathSmall = 'icons/quests/supDailyTrimming.png'
Consumables.consumable[26].id = 27
Consumables.consumable[26].includeList = []
Consumables.consumable[26].isDiscount = false
Consumables.consumable[26].isNew = false
Consumables.consumable[26].localizeTag = 'DAILY_FIX_TAIL_AND_WINGS'
Consumables.consumable[26].maxLevel = 10
Consumables.consumable[26].minLevel = 1
Consumables.consumable[26].mods = []
Consumables.consumable[26].mods.insert(0, None)
Consumables.consumable[26].mods[0] = Dummy()
Consumables.consumable[26].mods[0].activationRequired = 1
Consumables.consumable[26].mods[0].type = ModsTypeEnum.FIX_TAIL_AND_WINGS
Consumables.consumable[26].mods[0].value_ = 1.0
Consumables.consumable[26].nations = []
Consumables.consumable[26].nations.insert(0, None)
Consumables.consumable[26].nations[0] = 'USSR'.lower()
Consumables.consumable[26].nations.insert(1, None)
Consumables.consumable[26].nations[1] = 'USA'.lower()
Consumables.consumable[26].nations.insert(2, None)
Consumables.consumable[26].nations[2] = 'Germany'.lower()
Consumables.consumable[26].nations.insert(3, None)
Consumables.consumable[26].nations[3] = 'GB'.lower()
Consumables.consumable[26].nations.insert(4, None)
Consumables.consumable[26].nations[4] = 'Japan'.lower()
Consumables.consumable[26].nations.insert(5, None)
Consumables.consumable[26].nations[5] = 'China'.lower()
Consumables.consumable[26].nations.insert(6, None)
Consumables.consumable[26].nations[6] = 'France'.lower()
Consumables.consumable[26].planeType = []
Consumables.consumable[26].planeType.insert(0, None)
Consumables.consumable[26].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[26].planeType.insert(1, None)
Consumables.consumable[26].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[26].planeType.insert(2, None)
Consumables.consumable[26].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[26].planeType.insert(3, None)
Consumables.consumable[26].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[26].soundEffects = Dummy()
Consumables.consumable[26].soundEffects.finishSound = ''
Consumables.consumable[26].soundEffects.initSound = 'HUDFireExtinguishing'
Consumables.consumable[26].soundEffects.tickInterval = 0.0
Consumables.consumable[26].soundEffects.tickSound = ''
Consumables.consumable[26].tickets = 0
Consumables.consumable[26].uiIndex = 12
Consumables.consumable.insert(27, None)
Consumables.consumable[27] = Dummy()
Consumables.consumable[27].affectedModules = Dummy()
Consumables.consumable[27].affectedModules.isAnimationEquipment = true
Consumables.consumable[27].affectedModules.module = []
Consumables.consumable[27].affectedModules.module.insert(0, None)
Consumables.consumable[27].affectedModules.module[0] = 'Engine'
Consumables.consumable[27].behaviour = 0
Consumables.consumable[27].buyAvailable = false
Consumables.consumable[27].chargesCount = 2
Consumables.consumable[27].coolDownTime = 10
Consumables.consumable[27].credits = 5000
Consumables.consumable[27].effectTime = 0
Consumables.consumable[27].excludeList = []
Consumables.consumable[27].excludeList.insert(0, None)
Consumables.consumable[27].excludeList[0] = 1304
Consumables.consumable[27].excludeList.insert(1, None)
Consumables.consumable[27].excludeList[1] = 1399
Consumables.consumable[27].gold = 0
Consumables.consumable[27].group = 3
Consumables.consumable[27].icoPath = 'icons/modules/supDailyAirRestarter.png'
Consumables.consumable[27].icoPathBig = 'icons/modules/hud/supDailyAirRestarter.png'
Consumables.consumable[27].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[27].icoPathSmall = 'icons/quests/supDailyAirRestarter.png'
Consumables.consumable[27].id = 28
Consumables.consumable[27].includeList = []
Consumables.consumable[27].isDiscount = false
Consumables.consumable[27].isNew = false
Consumables.consumable[27].localizeTag = 'DAILY_AIR_RESTARTER'
Consumables.consumable[27].maxLevel = 10
Consumables.consumable[27].minLevel = 1
Consumables.consumable[27].mods = []
Consumables.consumable[27].mods.insert(0, None)
Consumables.consumable[27].mods[0] = Dummy()
Consumables.consumable[27].mods[0].activationRequired = 1
Consumables.consumable[27].mods[0].type = ModsTypeEnum.ENGINE_RESTORE
Consumables.consumable[27].mods[0].value_ = 1.0
Consumables.consumable[27].nations = []
Consumables.consumable[27].nations.insert(0, None)
Consumables.consumable[27].nations[0] = 'USSR'.lower()
Consumables.consumable[27].nations.insert(1, None)
Consumables.consumable[27].nations[1] = 'USA'.lower()
Consumables.consumable[27].nations.insert(2, None)
Consumables.consumable[27].nations[2] = 'Germany'.lower()
Consumables.consumable[27].nations.insert(3, None)
Consumables.consumable[27].nations[3] = 'GB'.lower()
Consumables.consumable[27].nations.insert(4, None)
Consumables.consumable[27].nations[4] = 'Japan'.lower()
Consumables.consumable[27].nations.insert(5, None)
Consumables.consumable[27].nations[5] = 'China'.lower()
Consumables.consumable[27].nations.insert(6, None)
Consumables.consumable[27].nations[6] = 'France'.lower()
Consumables.consumable[27].planeType = []
Consumables.consumable[27].planeType.insert(0, None)
Consumables.consumable[27].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[27].planeType.insert(1, None)
Consumables.consumable[27].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[27].planeType.insert(2, None)
Consumables.consumable[27].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[27].planeType.insert(3, None)
Consumables.consumable[27].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[27].soundEffects = Dummy()
Consumables.consumable[27].soundEffects.finishSound = ''
Consumables.consumable[27].soundEffects.initSound = 'HUDRestartTheEngine'
Consumables.consumable[27].soundEffects.tickInterval = 0.0
Consumables.consumable[27].soundEffects.tickSound = ''
Consumables.consumable[27].tickets = 0
Consumables.consumable[27].uiIndex = 9
Consumables.consumable.insert(28, None)
Consumables.consumable[28] = Dummy()
Consumables.consumable[28].behaviour = 1
Consumables.consumable[28].buyAvailable = true
Consumables.consumable[28].chargesCount = 1
Consumables.consumable[28].coolDownTime = 0
Consumables.consumable[28].credits = 0
Consumables.consumable[28].effectTime = 0
Consumables.consumable[28].excludeList = []
Consumables.consumable[28].excludeList.insert(0, None)
Consumables.consumable[28].excludeList[0] = 1304
Consumables.consumable[28].excludeList.insert(1, None)
Consumables.consumable[28].excludeList[1] = 1399
Consumables.consumable[28].gold = 0
Consumables.consumable[28].group = 8
Consumables.consumable[28].icoPath = 'icons/modules/econOutpost.png'
Consumables.consumable[28].icoPathBig = 'icons/modules/hud/econOutpost.png'
Consumables.consumable[28].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[28].icoPathSmall = 'icons/quests/econOutpost.png'
Consumables.consumable[28].id = 29
Consumables.consumable[28].includeList = []
Consumables.consumable[28].isDiscount = false
Consumables.consumable[28].isNew = false
Consumables.consumable[28].localizeTag = 'ECON_OUTPOST'
Consumables.consumable[28].maxLevel = 10
Consumables.consumable[28].minLevel = 1
Consumables.consumable[28].mods = []
Consumables.consumable[28].mods.insert(0, None)
Consumables.consumable[28].mods[0] = Dummy()
Consumables.consumable[28].mods[0].activationRequired = 1
Consumables.consumable[28].mods[0].type = ModsTypeEnum.ECONOMIC_BONUS_CREDITS
Consumables.consumable[28].mods[0].value_ = 1.5
Consumables.consumable[28].nations = []
Consumables.consumable[28].nations.insert(0, None)
Consumables.consumable[28].nations[0] = 'USSR'.lower()
Consumables.consumable[28].nations.insert(1, None)
Consumables.consumable[28].nations[1] = 'USA'.lower()
Consumables.consumable[28].nations.insert(2, None)
Consumables.consumable[28].nations[2] = 'Germany'.lower()
Consumables.consumable[28].nations.insert(3, None)
Consumables.consumable[28].nations[3] = 'GB'.lower()
Consumables.consumable[28].nations.insert(4, None)
Consumables.consumable[28].nations[4] = 'Japan'.lower()
Consumables.consumable[28].nations.insert(5, None)
Consumables.consumable[28].nations[5] = 'China'.lower()
Consumables.consumable[28].nations.insert(6, None)
Consumables.consumable[28].nations[6] = 'France'.lower()
Consumables.consumable[28].planeType = []
Consumables.consumable[28].planeType.insert(0, None)
Consumables.consumable[28].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[28].planeType.insert(1, None)
Consumables.consumable[28].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[28].planeType.insert(2, None)
Consumables.consumable[28].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[28].planeType.insert(3, None)
Consumables.consumable[28].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[28].soundEffects = Dummy()
Consumables.consumable[28].soundEffects.finishSound = ''
Consumables.consumable[28].soundEffects.initSound = 'HUDRestartTheEngine'
Consumables.consumable[28].soundEffects.tickInterval = 0.0
Consumables.consumable[28].soundEffects.tickSound = ''
Consumables.consumable[28].tickets = 1
Consumables.consumable[28].uiIndex = 27
Consumables.consumable.insert(29, None)
Consumables.consumable[29] = Dummy()
Consumables.consumable[29].behaviour = 1
Consumables.consumable[29].buyAvailable = true
Consumables.consumable[29].chargesCount = 1
Consumables.consumable[29].coolDownTime = 0
Consumables.consumable[29].credits = 0
Consumables.consumable[29].effectTime = 0
Consumables.consumable[29].excludeList = []
Consumables.consumable[29].excludeList.insert(0, None)
Consumables.consumable[29].excludeList[0] = 1304
Consumables.consumable[29].excludeList.insert(1, None)
Consumables.consumable[29].excludeList[1] = 1399
Consumables.consumable[29].gold = 0
Consumables.consumable[29].group = 9
Consumables.consumable[29].icoPath = 'icons/modules/econRecon.png'
Consumables.consumable[29].icoPathBig = 'icons/modules/hud/econRecon.png'
Consumables.consumable[29].icoPathEmpty = 'icons/modules/modulesIconEmpty.png'
Consumables.consumable[29].icoPathSmall = 'icons/quests/econRecon.png'
Consumables.consumable[29].id = 30
Consumables.consumable[29].includeList = []
Consumables.consumable[29].isDiscount = false
Consumables.consumable[29].isNew = false
Consumables.consumable[29].localizeTag = 'ECON_RECON'
Consumables.consumable[29].maxLevel = 10
Consumables.consumable[29].minLevel = 1
Consumables.consumable[29].mods = []
Consumables.consumable[29].mods.insert(0, None)
Consumables.consumable[29].mods[0] = Dummy()
Consumables.consumable[29].mods[0].activationRequired = 1
Consumables.consumable[29].mods[0].type = ModsTypeEnum.ECONOMIC_BONUS_XP
Consumables.consumable[29].mods[0].value_ = 1.25
Consumables.consumable[29].nations = []
Consumables.consumable[29].nations.insert(0, None)
Consumables.consumable[29].nations[0] = 'USSR'.lower()
Consumables.consumable[29].nations.insert(1, None)
Consumables.consumable[29].nations[1] = 'USA'.lower()
Consumables.consumable[29].nations.insert(2, None)
Consumables.consumable[29].nations[2] = 'Germany'.lower()
Consumables.consumable[29].nations.insert(3, None)
Consumables.consumable[29].nations[3] = 'GB'.lower()
Consumables.consumable[29].nations.insert(4, None)
Consumables.consumable[29].nations[4] = 'Japan'.lower()
Consumables.consumable[29].nations.insert(5, None)
Consumables.consumable[29].nations[5] = 'China'.lower()
Consumables.consumable[29].nations.insert(6, None)
Consumables.consumable[29].nations[6] = 'France'.lower()
Consumables.consumable[29].planeType = []
Consumables.consumable[29].planeType.insert(0, None)
Consumables.consumable[29].planeType[0] = consts.PLANE_TYPE.ASSAULT
Consumables.consumable[29].planeType.insert(1, None)
Consumables.consumable[29].planeType[1] = consts.PLANE_TYPE.FIGHTER
Consumables.consumable[29].planeType.insert(2, None)
Consumables.consumable[29].planeType[2] = consts.PLANE_TYPE.HFIGHTER
Consumables.consumable[29].planeType.insert(3, None)
Consumables.consumable[29].planeType[3] = consts.PLANE_TYPE.NAVY
Consumables.consumable[29].soundEffects = Dummy()
Consumables.consumable[29].soundEffects.finishSound = ''
Consumables.consumable[29].soundEffects.initSound = 'HUDRestartTheEngine'
Consumables.consumable[29].soundEffects.tickInterval = 0.0
Consumables.consumable[29].soundEffects.tickSound = ''
Consumables.consumable[29].tickets = 1
Consumables.consumable[29].uiIndex = 28
ConsumableDB = None
Filter = None

def initDB():
    global Filter
    global ConsumableDB
    if ConsumableDB is None:
        ConsumableDB = {}
        Filter = {'nation': {},
         'include': {},
         'exclude': {},
         'level': {},
         'planeType': {}}
        for consumable in Consumables.consumable:
            ConsumableDB[consumable.id] = consumable
            consumable.name = 'LOBBY_CONSUMABLES_NAME_' + consumable.localizeTag
            consumable.description = 'LOBBY_CONSUMABLES_DESCRIPTION_SHORT_' + consumable.localizeTag
            consumable.fullDescription = 'LOBBY_CONSUMABLES_EFFECT_ON_USE_' + consumable.localizeTag
            consumable.effectContinuous = 'LOBBY_CONSUMABLES_EFFECT_CONTINUOUS_' + consumable.localizeTag
            consumable.effectOnUse = 'LOBBY_CONSUMABLES_EFFECT_ON_USE_' + consumable.localizeTag
            for nationID in consumable.nations:
                Filter['nation'].setdefault(nationID, set()).add(consumable.id)

            for level in xrange(consumable.minLevel, consumable.maxLevel + 1):
                Filter['level'].setdefault(level, set()).add(consumable.id)

            for planeID in consumable.excludeList:
                Filter['exclude'].setdefault(planeID, set()).add(consumable.id)

            for planeID in consumable.includeList:
                Filter['include'].setdefault(planeID, set()).add(consumable.id)

            if not consumable.planeType:
                consumable.planeType = filter(lambda x: isinstance(x, int), consts.PLANE_TYPE.__dict__.values())
            for planeType in consumable.planeType:
                Filter['planeType'].setdefault(planeType, set()).add(consumable.id)

    return


initDB()