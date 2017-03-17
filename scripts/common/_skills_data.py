# Embedded file name: scripts/common/_skills_data.py
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


class SKILL_GROUP:
    MAIN = 0
    COMMON = 1
    IMPROVED = 2
    UNIQUE = 3
    ALL_TYPES = (MAIN,
     COMMON,
     IMPROVED,
     UNIQUE)


class ModsTypeEnum:
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


class SpecializationEnum:
    PILOT = 0
    GUNNER = 1
    NAVIGATOR = 2
    ALL_TYPES = (PILOT, GUNNER, NAVIGATOR)


Skills = Dummy()
Skills.skill = []
Skills.skill.insert(0, None)
Skills.skill[0] = Dummy()
Skills.skill[0].cost = 0
Skills.skill[0].crewMemberSubTypes = []
Skills.skill[0].crewMemberTypes = []
Skills.skill[0].crewMemberTypes.insert(0, None)
Skills.skill[0].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[0].group = SKILL_GROUP.MAIN
Skills.skill[0].icoPath = 'icons/specialization/tab/hangarTabSquarePilot.png'
Skills.skill[0].id = 1
Skills.skill[0].localizeTag = 'PILOT'
Skills.skill[0].mainForSpecialization = SpecializationEnum.PILOT
Skills.skill[0].mods = []
Skills.skill[0].mods.insert(0, None)
Skills.skill[0].mods[0] = Dummy()
Skills.skill[0].mods[0].states = Dummy()
Skills.skill[0].mods[0].states.crit = 0.8
Skills.skill[0].mods[0].states.damaged = 0.8
Skills.skill[0].mods[0].states.good = 0.9
Skills.skill[0].mods[0].type = ModsTypeEnum.AIR_AGILITY
Skills.skill[0].mods.insert(1, None)
Skills.skill[0].mods[1] = Dummy()
Skills.skill[0].mods[1].states = Dummy()
Skills.skill[0].mods[1].states.crit = 0.8
Skills.skill[0].mods[1].states.damaged = 0.8
Skills.skill[0].mods[1].states.good = 0.9
Skills.skill[0].mods[1].type = ModsTypeEnum.ENGINE_POWER
Skills.skill[0].mods.insert(2, None)
Skills.skill[0].mods[2] = Dummy()
Skills.skill[0].mods[2].states = Dummy()
Skills.skill[0].mods[2].states.crit = 0.5
Skills.skill[0].mods[2].states.damaged = 0.7
Skills.skill[0].mods[2].states.good = 0.8
Skills.skill[0].mods[2].type = ModsTypeEnum.WEAPONS_FOCUS
Skills.skill[0].mods.insert(3, None)
Skills.skill[0].mods[3] = Dummy()
Skills.skill[0].mods[3].states = Dummy()
Skills.skill[0].mods[3].states.crit = 0.5
Skills.skill[0].mods[3].states.damaged = 0.7
Skills.skill[0].mods[3].states.good = 0.8
Skills.skill[0].mods[3].type = ModsTypeEnum.BOMB_MISSILE_FOCUS
Skills.skill[0].mods.insert(4, None)
Skills.skill[0].mods[4] = Dummy()
Skills.skill[0].mods[4].states = Dummy()
Skills.skill[0].mods[4].states.crit = 0.0
Skills.skill[0].mods[4].states.damaged = 1.0
Skills.skill[0].mods[4].states.good = 1.0
Skills.skill[0].mods[4].type = ModsTypeEnum.AUTO_AIM
Skills.skill[0].order = 0
Skills.skill[0].smallIcoPath = 'icons/specialization/crew/hangPilotsIconPilot.png'
Skills.skill[0].uiIndex = 1
Skills.skill.insert(1, None)
Skills.skill[1] = Dummy()
Skills.skill[1].cost = 0
Skills.skill[1].crewMemberSubTypes = []
Skills.skill[1].crewMemberTypes = []
Skills.skill[1].crewMemberTypes.insert(0, None)
Skills.skill[1].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[1].group = SKILL_GROUP.MAIN
Skills.skill[1].icoPath = 'icons/specialization/tab/hangarTabSquareGunner.png'
Skills.skill[1].id = 2
Skills.skill[1].localizeTag = 'GUNNER'
Skills.skill[1].mainForSpecialization = SpecializationEnum.GUNNER
Skills.skill[1].mods = []
Skills.skill[1].mods.insert(0, None)
Skills.skill[1].mods[0] = Dummy()
Skills.skill[1].mods[0].states = Dummy()
Skills.skill[1].mods[0].states.crit = 0.5
Skills.skill[1].mods[0].states.damaged = 0.5
Skills.skill[1].mods[0].states.good = 0.75
Skills.skill[1].mods[0].type = ModsTypeEnum.TURRET_DELAY
Skills.skill[1].mods.insert(1, None)
Skills.skill[1].mods[1] = Dummy()
Skills.skill[1].mods[1].states = Dummy()
Skills.skill[1].mods[1].states.crit = 0.0
Skills.skill[1].mods[1].states.damaged = 1.0
Skills.skill[1].mods[1].states.good = 1.0
Skills.skill[1].mods[1].type = ModsTypeEnum.GUNNER_ALIVE
Skills.skill[1].order = 0
Skills.skill[1].smallIcoPath = 'icons/specialization/crew/hangPilotsIconGunner.png'
Skills.skill[1].uiIndex = 2
Skills.skill.insert(2, None)
Skills.skill[2] = Dummy()
Skills.skill[2].cost = 1
Skills.skill[2].crewMemberSubTypes = []
Skills.skill[2].crewMemberSubTypes.insert(0, None)
Skills.skill[2].crewMemberSubTypes[0] = 0
Skills.skill[2].crewMemberSubTypes.insert(1, None)
Skills.skill[2].crewMemberSubTypes[1] = 1
Skills.skill[2].crewMemberSubTypes.insert(2, None)
Skills.skill[2].crewMemberSubTypes[2] = 2
Skills.skill[2].crewMemberSubTypes.insert(3, None)
Skills.skill[2].crewMemberSubTypes[3] = 3
Skills.skill[2].crewMemberTypes = []
Skills.skill[2].crewMemberTypes.insert(0, None)
Skills.skill[2].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[2].group = SKILL_GROUP.COMMON
Skills.skill[2].icoPath = 'icons/skills/lobby/pilotFireDuration.png'
Skills.skill[2].id = 201
Skills.skill[2].infotipsIcoPath = 'icons/skills/infotips/pilotFireDuration.png'
Skills.skill[2].localizeTag = 'PILOT_FIREDURATION'
Skills.skill[2].mods = []
Skills.skill[2].mods.insert(0, None)
Skills.skill[2].mods[0] = Dummy()
Skills.skill[2].mods[0].states = Dummy()
Skills.skill[2].mods[0].states.crit = 0.8
Skills.skill[2].mods[0].states.damaged = 0.8
Skills.skill[2].mods[0].states.good = 0.8
Skills.skill[2].mods[0].type = ModsTypeEnum.FIRE_DAMAGE_K
Skills.skill[2].mods.insert(1, None)
Skills.skill[2].mods[1] = Dummy()
Skills.skill[2].mods[1].states = Dummy()
Skills.skill[2].mods[1].states.crit = 1.2
Skills.skill[2].mods[1].states.damaged = 1.2
Skills.skill[2].mods[1].states.good = 1.2
Skills.skill[2].mods[1].type = ModsTypeEnum.FIRE_DURATION
Skills.skill[2].order = 0
Skills.skill[2].smallIcoPath = 'icons/skills/lobby/pilotFireDuration_Mini.png'
Skills.skill[2].uiIndex = 201
Skills.skill.insert(3, None)
Skills.skill[3] = Dummy()
Skills.skill[3].cost = 2
Skills.skill[3].crewMemberSubTypes = []
Skills.skill[3].crewMemberSubTypes.insert(0, None)
Skills.skill[3].crewMemberSubTypes[0] = 0
Skills.skill[3].crewMemberSubTypes.insert(1, None)
Skills.skill[3].crewMemberSubTypes[1] = 1
Skills.skill[3].crewMemberSubTypes.insert(2, None)
Skills.skill[3].crewMemberSubTypes[2] = 2
Skills.skill[3].crewMemberSubTypes.insert(3, None)
Skills.skill[3].crewMemberSubTypes[3] = 3
Skills.skill[3].crewMemberTypes = []
Skills.skill[3].crewMemberTypes.insert(0, None)
Skills.skill[3].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[3].group = SKILL_GROUP.COMMON
Skills.skill[3].icoPath = 'icons/skills/lobby/pilotBattleTried.png'
Skills.skill[3].id = 202
Skills.skill[3].infotipsIcoPath = 'icons/skills/infotips/pilotBattleTried.png'
Skills.skill[3].localizeTag = 'PILOT_BATTLETRIED'
Skills.skill[3].mods = []
Skills.skill[3].mods.insert(0, None)
Skills.skill[3].mods[0] = Dummy()
Skills.skill[3].mods[0].states = Dummy()
Skills.skill[3].mods[0].states.crit = 0.8
Skills.skill[3].mods[0].states.damaged = 0.8
Skills.skill[3].mods[0].states.good = 0.8
Skills.skill[3].mods[0].type = ModsTypeEnum.CRIT_WEAKNESS_PILOT
Skills.skill[3].mods.insert(1, None)
Skills.skill[3].mods[1] = Dummy()
Skills.skill[3].mods[1].states = Dummy()
Skills.skill[3].mods[1].states.crit = 1.25
Skills.skill[3].mods[1].states.damaged = 1.25
Skills.skill[3].mods[1].states.good = 1.25
Skills.skill[3].mods[1].type = ModsTypeEnum.DAMAGE_AGILITY
Skills.skill[3].order = 2
Skills.skill[3].smallIcoPath = 'icons/skills/lobby/pilotBattleTried_Mini.png'
Skills.skill[3].uiIndex = 203
Skills.skill.insert(4, None)
Skills.skill[4] = Dummy()
Skills.skill[4].cost = 2
Skills.skill[4].crewMemberSubTypes = []
Skills.skill[4].crewMemberSubTypes.insert(0, None)
Skills.skill[4].crewMemberSubTypes[0] = 0
Skills.skill[4].crewMemberSubTypes.insert(1, None)
Skills.skill[4].crewMemberSubTypes[1] = 1
Skills.skill[4].crewMemberSubTypes.insert(2, None)
Skills.skill[4].crewMemberSubTypes[2] = 2
Skills.skill[4].crewMemberTypes = []
Skills.skill[4].crewMemberTypes.insert(0, None)
Skills.skill[4].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[4].group = SKILL_GROUP.COMMON
Skills.skill[4].icoPath = 'icons/skills/lobby/pilotKnowEngine_1.png'
Skills.skill[4].id = 203
Skills.skill[4].infotipsIcoPath = 'icons/skills/infotips/pilotKnowEngine_1.png'
Skills.skill[4].localizeTag = 'PILOT_KNOWENGINE_I'
Skills.skill[4].mods = []
Skills.skill[4].mods.insert(0, None)
Skills.skill[4].mods[0] = Dummy()
Skills.skill[4].mods[0].states = Dummy()
Skills.skill[4].mods[0].states.crit = 1.03
Skills.skill[4].mods[0].states.damaged = 1.03
Skills.skill[4].mods[0].states.good = 1.03
Skills.skill[4].mods[0].type = ModsTypeEnum.ENGINE_POWER
Skills.skill[4].order = 3
Skills.skill[4].smallIcoPath = 'icons/skills/lobby/pilotKnowEngine_1_Mini.png'
Skills.skill[4].uiIndex = 207
Skills.skill.insert(5, None)
Skills.skill[5] = Dummy()
Skills.skill[5].cost = 2
Skills.skill[5].crewMemberSubTypes = []
Skills.skill[5].crewMemberSubTypes.insert(0, None)
Skills.skill[5].crewMemberSubTypes[0] = 0
Skills.skill[5].crewMemberSubTypes.insert(1, None)
Skills.skill[5].crewMemberSubTypes[1] = 1
Skills.skill[5].crewMemberSubTypes.insert(2, None)
Skills.skill[5].crewMemberSubTypes[2] = 2
Skills.skill[5].crewMemberSubTypes.insert(3, None)
Skills.skill[5].crewMemberSubTypes[3] = 3
Skills.skill[5].crewMemberTypes = []
Skills.skill[5].crewMemberTypes.insert(0, None)
Skills.skill[5].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[5].group = SKILL_GROUP.COMMON
Skills.skill[5].icoPath = 'icons/skills/lobby/pilotMarksman_1.png'
Skills.skill[5].id = 204
Skills.skill[5].infotipsIcoPath = 'icons/skills/infotips/pilotMarksman_1.png'
Skills.skill[5].localizeTag = 'PILOT_MARKSMAN_I'
Skills.skill[5].mods = []
Skills.skill[5].mods.insert(0, None)
Skills.skill[5].mods[0] = Dummy()
Skills.skill[5].mods[0].states = Dummy()
Skills.skill[5].mods[0].states.crit = 1.05
Skills.skill[5].mods[0].states.damaged = 1.05
Skills.skill[5].mods[0].states.good = 1.05
Skills.skill[5].mods[0].type = ModsTypeEnum.WEAPONS_FOCUS
Skills.skill[5].order = 4
Skills.skill[5].smallIcoPath = 'icons/skills/lobby/pilotMarksman_1_Mini.png'
Skills.skill[5].uiIndex = 209
Skills.skill.insert(6, None)
Skills.skill[6] = Dummy()
Skills.skill[6].cost = 1
Skills.skill[6].crewMemberSubTypes = []
Skills.skill[6].crewMemberSubTypes.insert(0, None)
Skills.skill[6].crewMemberSubTypes[0] = 0
Skills.skill[6].crewMemberSubTypes.insert(1, None)
Skills.skill[6].crewMemberSubTypes[1] = 2
Skills.skill[6].crewMemberSubTypes.insert(2, None)
Skills.skill[6].crewMemberSubTypes[2] = 3
Skills.skill[6].crewMemberTypes = []
Skills.skill[6].crewMemberTypes.insert(0, None)
Skills.skill[6].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[6].group = SKILL_GROUP.COMMON
Skills.skill[6].icoPath = 'icons/skills/lobby/pilotSightRange.png'
Skills.skill[6].id = 205
Skills.skill[6].infotipsIcoPath = 'icons/skills/infotips/pilotSightRange.png'
Skills.skill[6].localizeTag = 'PILOT_SIGHTRANGE'
Skills.skill[6].mods = []
Skills.skill[6].mods.insert(0, None)
Skills.skill[6].mods[0] = Dummy()
Skills.skill[6].mods[0].states = Dummy()
Skills.skill[6].mods[0].states.crit = 1.2
Skills.skill[6].mods[0].states.damaged = 1.2
Skills.skill[6].mods[0].states.good = 1.2
Skills.skill[6].mods[0].type = ModsTypeEnum.SIGHT_RANGE_PILOT
Skills.skill[6].order = 1
Skills.skill[6].smallIcoPath = 'icons/skills/lobby/pilotSightRange_Mini.png'
Skills.skill[6].uiIndex = 202
Skills.skill.insert(7, None)
Skills.skill[7] = Dummy()
Skills.skill[7].cost = 2
Skills.skill[7].crewMemberSubTypes = []
Skills.skill[7].crewMemberSubTypes.insert(0, None)
Skills.skill[7].crewMemberSubTypes[0] = 0
Skills.skill[7].crewMemberSubTypes.insert(1, None)
Skills.skill[7].crewMemberSubTypes[1] = 1
Skills.skill[7].crewMemberSubTypes.insert(2, None)
Skills.skill[7].crewMemberSubTypes[2] = 3
Skills.skill[7].crewMemberTypes = []
Skills.skill[7].crewMemberTypes.insert(0, None)
Skills.skill[7].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[7].group = SKILL_GROUP.COMMON
Skills.skill[7].icoPath = 'icons/skills/lobby/pilotShellMaster.png'
Skills.skill[7].id = 206
Skills.skill[7].infotipsIcoPath = 'icons/skills/infotips/pilotShellMaster.png'
Skills.skill[7].localizeTag = 'PILOT_SHELLMASTER'
Skills.skill[7].mods = []
Skills.skill[7].mods.insert(0, None)
Skills.skill[7].mods[0] = Dummy()
Skills.skill[7].mods[0].states = Dummy()
Skills.skill[7].mods[0].states.crit = 1.15
Skills.skill[7].mods[0].states.damaged = 1.15
Skills.skill[7].mods[0].states.good = 1.15
Skills.skill[7].mods[0].type = ModsTypeEnum.ROCKET_DAMAGE
Skills.skill[7].mods.insert(1, None)
Skills.skill[7].mods[1] = Dummy()
Skills.skill[7].mods[1].states = Dummy()
Skills.skill[7].mods[1].states.crit = 1.15
Skills.skill[7].mods[1].states.damaged = 1.15
Skills.skill[7].mods[1].states.good = 1.15
Skills.skill[7].mods[1].type = ModsTypeEnum.ROCKET_SPLASH
Skills.skill[7].mods.insert(2, None)
Skills.skill[7].mods[2] = Dummy()
Skills.skill[7].mods[2].states = Dummy()
Skills.skill[7].mods[2].states.crit = 1.15
Skills.skill[7].mods[2].states.damaged = 1.15
Skills.skill[7].mods[2].states.good = 1.15
Skills.skill[7].mods[2].type = ModsTypeEnum.BOMB_DAMAGE
Skills.skill[7].mods.insert(3, None)
Skills.skill[7].mods[3] = Dummy()
Skills.skill[7].mods[3].states = Dummy()
Skills.skill[7].mods[3].states.crit = 1.15
Skills.skill[7].mods[3].states.damaged = 1.15
Skills.skill[7].mods[3].states.good = 1.15
Skills.skill[7].mods[3].type = ModsTypeEnum.BOMB_SPLASH
Skills.skill[7].order = 5
Skills.skill[7].smallIcoPath = 'icons/skills/lobby/pilotShellMaster_Mini.png'
Skills.skill[7].uiIndex = 211
Skills.skill.insert(8, None)
Skills.skill[8] = Dummy()
Skills.skill[8].cost = 3
Skills.skill[8].crewMemberSubTypes = []
Skills.skill[8].crewMemberSubTypes.insert(0, None)
Skills.skill[8].crewMemberSubTypes[0] = 0
Skills.skill[8].crewMemberSubTypes.insert(1, None)
Skills.skill[8].crewMemberSubTypes[1] = 1
Skills.skill[8].crewMemberSubTypes.insert(2, None)
Skills.skill[8].crewMemberSubTypes[2] = 2
Skills.skill[8].crewMemberTypes = []
Skills.skill[8].crewMemberTypes.insert(0, None)
Skills.skill[8].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[8].dependedFrom = 203
Skills.skill[8].group = SKILL_GROUP.IMPROVED
Skills.skill[8].icoPath = 'icons/skills/lobby/pilotKnowEngine_2.png'
Skills.skill[8].id = 207
Skills.skill[8].infotipsIcoPath = 'icons/skills/infotips/pilotKnowEngine_2.png'
Skills.skill[8].localizeTag = 'PILOT_KNOWENGINE_II'
Skills.skill[8].mods = []
Skills.skill[8].mods.insert(0, None)
Skills.skill[8].mods[0] = Dummy()
Skills.skill[8].mods[0].states = Dummy()
Skills.skill[8].mods[0].states.crit = 1.02
Skills.skill[8].mods[0].states.damaged = 1.02
Skills.skill[8].mods[0].states.good = 1.02
Skills.skill[8].mods[0].type = ModsTypeEnum.ENGINE_POWER
Skills.skill[8].mods.insert(1, None)
Skills.skill[8].mods[1] = Dummy()
Skills.skill[8].mods[1].states = Dummy()
Skills.skill[8].mods[1].states.crit = 1.02
Skills.skill[8].mods[1].states.damaged = 1.02
Skills.skill[8].mods[1].states.good = 1.02
Skills.skill[8].mods[1].type = ModsTypeEnum.MAX_SPEED
Skills.skill[8].order = 3
Skills.skill[8].smallIcoPath = 'icons/skills/lobby/pilotKnowEngine_2_Mini.png'
Skills.skill[8].uiIndex = 208
Skills.skill.insert(9, None)
Skills.skill[9] = Dummy()
Skills.skill[9].cost = 2
Skills.skill[9].crewMemberSubTypes = []
Skills.skill[9].crewMemberSubTypes.insert(0, None)
Skills.skill[9].crewMemberSubTypes[0] = 0
Skills.skill[9].crewMemberSubTypes.insert(1, None)
Skills.skill[9].crewMemberSubTypes[1] = 1
Skills.skill[9].crewMemberSubTypes.insert(2, None)
Skills.skill[9].crewMemberSubTypes[2] = 2
Skills.skill[9].crewMemberSubTypes.insert(3, None)
Skills.skill[9].crewMemberSubTypes[3] = 3
Skills.skill[9].crewMemberTypes = []
Skills.skill[9].crewMemberTypes.insert(0, None)
Skills.skill[9].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[9].group = SKILL_GROUP.IMPROVED
Skills.skill[9].icoPath = 'icons/skills/lobby/pilotPilotage.png'
Skills.skill[9].id = 208
Skills.skill[9].infotipsIcoPath = 'icons/skills/infotips/pilotPilotage.png'
Skills.skill[9].localizeTag = 'PILOT_PILOTAGE'
Skills.skill[9].mods = []
Skills.skill[9].mods.insert(0, None)
Skills.skill[9].mods[0] = Dummy()
Skills.skill[9].mods[0].states = Dummy()
Skills.skill[9].mods[0].states.crit = 1.005
Skills.skill[9].mods[0].states.damaged = 1.005
Skills.skill[9].mods[0].states.good = 1.005
Skills.skill[9].mods[0].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Skills.skill[9].mods.insert(1, None)
Skills.skill[9].mods[1] = Dummy()
Skills.skill[9].mods[1].states = Dummy()
Skills.skill[9].mods[1].states.crit = 1.02
Skills.skill[9].mods[1].states.damaged = 1.02
Skills.skill[9].mods[1].states.good = 1.02
Skills.skill[9].mods[1].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Skills.skill[9].mods.insert(2, None)
Skills.skill[9].mods[2] = Dummy()
Skills.skill[9].mods[2].states = Dummy()
Skills.skill[9].mods[2].states.crit = 1.02
Skills.skill[9].mods[2].states.damaged = 1.02
Skills.skill[9].mods[2].states.good = 1.02
Skills.skill[9].mods[2].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Skills.skill[9].order = 0
Skills.skill[9].smallIcoPath = 'icons/skills/lobby/pilotPilotage_Mini.png'
Skills.skill[9].uiIndex = 204
Skills.skill.insert(10, None)
Skills.skill[10] = Dummy()
Skills.skill[10].cost = 3
Skills.skill[10].crewMemberSubTypes = []
Skills.skill[10].crewMemberSubTypes.insert(0, None)
Skills.skill[10].crewMemberSubTypes[0] = 0
Skills.skill[10].crewMemberSubTypes.insert(1, None)
Skills.skill[10].crewMemberSubTypes[1] = 1
Skills.skill[10].crewMemberSubTypes.insert(2, None)
Skills.skill[10].crewMemberSubTypes[2] = 2
Skills.skill[10].crewMemberSubTypes.insert(3, None)
Skills.skill[10].crewMemberSubTypes[3] = 3
Skills.skill[10].crewMemberTypes = []
Skills.skill[10].crewMemberTypes.insert(0, None)
Skills.skill[10].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[10].dependedFrom = 204
Skills.skill[10].group = SKILL_GROUP.IMPROVED
Skills.skill[10].icoPath = 'icons/skills/lobby/pilotMarksman_2.png'
Skills.skill[10].id = 209
Skills.skill[10].infotipsIcoPath = 'icons/skills/infotips/pilotMarksman_2.png'
Skills.skill[10].localizeTag = 'PILOT_MARKSMAN_II'
Skills.skill[10].mods = []
Skills.skill[10].mods.insert(0, None)
Skills.skill[10].mods[0] = Dummy()
Skills.skill[10].mods[0].states = Dummy()
Skills.skill[10].mods[0].states.crit = 1.05
Skills.skill[10].mods[0].states.damaged = 1.05
Skills.skill[10].mods[0].states.good = 1.05
Skills.skill[10].mods[0].type = ModsTypeEnum.WEAPONS_FOCUS
Skills.skill[10].mods.insert(1, None)
Skills.skill[10].mods[1] = Dummy()
Skills.skill[10].mods[1].states = Dummy()
Skills.skill[10].mods[1].states.crit = 1.1
Skills.skill[10].mods[1].states.damaged = 1.1
Skills.skill[10].mods[1].states.good = 1.1
Skills.skill[10].mods[1].type = ModsTypeEnum.AUTOAIM_ANGLE
Skills.skill[10].order = 4
Skills.skill[10].smallIcoPath = 'icons/skills/lobby/pilotMarksman_2_Mini.png'
Skills.skill[10].uiIndex = 210
Skills.skill.insert(11, None)
Skills.skill[11] = Dummy()
Skills.skill[11].cost = 2
Skills.skill[11].crewMemberSubTypes = []
Skills.skill[11].crewMemberSubTypes.insert(0, None)
Skills.skill[11].crewMemberSubTypes[0] = 0
Skills.skill[11].crewMemberSubTypes.insert(1, None)
Skills.skill[11].crewMemberSubTypes[1] = 1
Skills.skill[11].crewMemberSubTypes.insert(2, None)
Skills.skill[11].crewMemberSubTypes[2] = 2
Skills.skill[11].crewMemberSubTypes.insert(3, None)
Skills.skill[11].crewMemberSubTypes[3] = 3
Skills.skill[11].crewMemberTypes = []
Skills.skill[11].crewMemberTypes.insert(0, None)
Skills.skill[11].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[11].group = SKILL_GROUP.IMPROVED
Skills.skill[11].icoPath = 'icons/skills/lobby/pilotRocketKiller.png'
Skills.skill[11].id = 210
Skills.skill[11].infotipsIcoPath = 'icons/skills/infotips/pilotRocketKiller.png'
Skills.skill[11].localizeTag = 'PILOT_ROCKETKILLER'
Skills.skill[11].mods = []
Skills.skill[11].mods.insert(0, None)
Skills.skill[11].mods[0] = Dummy()
Skills.skill[11].mods[0].states = Dummy()
Skills.skill[11].mods[0].states.crit = 2.5
Skills.skill[11].mods[0].states.damaged = 2.5
Skills.skill[11].mods[0].states.good = 2.5
Skills.skill[11].mods[0].type = ModsTypeEnum.ACTIVATE_ROCKET_DETONATOR
Skills.skill[11].order = 5
Skills.skill[11].smallIcoPath = 'icons/skills/lobby/pilotRocketKiller_Mini.png'
Skills.skill[11].uiIndex = 212
Skills.skill.insert(12, None)
Skills.skill[12] = Dummy()
Skills.skill[12].cost = 2
Skills.skill[12].crewMemberSubTypes = []
Skills.skill[12].crewMemberSubTypes.insert(0, None)
Skills.skill[12].crewMemberSubTypes[0] = 0
Skills.skill[12].crewMemberSubTypes.insert(1, None)
Skills.skill[12].crewMemberSubTypes[1] = 1
Skills.skill[12].crewMemberSubTypes.insert(2, None)
Skills.skill[12].crewMemberSubTypes[2] = 2
Skills.skill[12].crewMemberSubTypes.insert(3, None)
Skills.skill[12].crewMemberSubTypes[3] = 3
Skills.skill[12].crewMemberTypes = []
Skills.skill[12].crewMemberTypes.insert(0, None)
Skills.skill[12].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[12].group = SKILL_GROUP.IMPROVED
Skills.skill[12].icoPath = 'icons/skills/lobby/pilotEquipFlight.png'
Skills.skill[12].id = 211
Skills.skill[12].infotipsIcoPath = 'icons/skills/infotips/pilotEquipFlight.png'
Skills.skill[12].localizeTag = 'PILOT_EQUIP_FLIGHT'
Skills.skill[12].mods = []
Skills.skill[12].mods.insert(0, None)
Skills.skill[12].mods[0] = Dummy()
Skills.skill[12].mods[0].relation = Dummy()
Skills.skill[12].mods[0].relation.type = []
Skills.skill[12].mods[0].relation.type.insert(0, None)
Skills.skill[12].mods[0].relation.type[0] = ModsTypeEnum.ENGINE_POWER
Skills.skill[12].mods[0].relation.type.insert(1, None)
Skills.skill[12].mods[0].relation.type[1] = ModsTypeEnum.MAX_SPEED
Skills.skill[12].mods[0].relation.type.insert(2, None)
Skills.skill[12].mods[0].relation.type[2] = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Skills.skill[12].mods[0].relation.type.insert(3, None)
Skills.skill[12].mods[0].relation.type[3] = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Skills.skill[12].mods[0].relation.type.insert(4, None)
Skills.skill[12].mods[0].relation.type[4] = ModsTypeEnum.YAW_MAX_SPEED_CFG
Skills.skill[12].mods[0].states = Dummy()
Skills.skill[12].mods[0].states.crit = 1.4
Skills.skill[12].mods[0].states.damaged = 1.4
Skills.skill[12].mods[0].states.good = 1.4
Skills.skill[12].mods[0].type = ModsTypeEnum.EQUIPMENT_EFFECT
Skills.skill[12].order = 1
Skills.skill[12].smallIcoPath = 'icons/skills/lobby/pilotEquipFlight_Mini.png'
Skills.skill[12].uiIndex = 205
Skills.skill.insert(13, None)
Skills.skill[13] = Dummy()
Skills.skill[13].cost = 2
Skills.skill[13].crewMemberSubTypes = []
Skills.skill[13].crewMemberSubTypes.insert(0, None)
Skills.skill[13].crewMemberSubTypes[0] = 0
Skills.skill[13].crewMemberSubTypes.insert(1, None)
Skills.skill[13].crewMemberSubTypes[1] = 1
Skills.skill[13].crewMemberSubTypes.insert(2, None)
Skills.skill[13].crewMemberSubTypes[2] = 2
Skills.skill[13].crewMemberSubTypes.insert(3, None)
Skills.skill[13].crewMemberSubTypes[3] = 3
Skills.skill[13].crewMemberTypes = []
Skills.skill[13].crewMemberTypes.insert(0, None)
Skills.skill[13].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[13].group = SKILL_GROUP.IMPROVED
Skills.skill[13].icoPath = 'icons/skills/lobby/pilotEquipArmor.png'
Skills.skill[13].id = 212
Skills.skill[13].infotipsIcoPath = 'icons/skills/infotips/pilotEquipArmor.png'
Skills.skill[13].localizeTag = 'PILOT_EQUIP_ARMOR'
Skills.skill[13].mods = []
Skills.skill[13].mods.insert(0, None)
Skills.skill[13].mods[0] = Dummy()
Skills.skill[13].mods[0].relation = Dummy()
Skills.skill[13].mods[0].relation.type = []
Skills.skill[13].mods[0].relation.type.insert(0, None)
Skills.skill[13].mods[0].relation.type[0] = ModsTypeEnum.MAIN_HP
Skills.skill[13].mods[0].relation.type.insert(1, None)
Skills.skill[13].mods[0].relation.type[1] = ModsTypeEnum.SYSTEM_HP
Skills.skill[13].mods[0].relation.type.insert(2, None)
Skills.skill[13].mods[0].relation.type[2] = ModsTypeEnum.VITALS_ARMOR
Skills.skill[13].mods[0].relation.type.insert(3, None)
Skills.skill[13].mods[0].relation.type[3] = ModsTypeEnum.AA_PLANE_DAMAGE_K
Skills.skill[13].mods[0].states = Dummy()
Skills.skill[13].mods[0].states.crit = 1.4
Skills.skill[13].mods[0].states.damaged = 1.4
Skills.skill[13].mods[0].states.good = 1.4
Skills.skill[13].mods[0].type = ModsTypeEnum.EQUIPMENT_EFFECT
Skills.skill[13].order = 2
Skills.skill[13].smallIcoPath = 'icons/skills/lobby/pilotEquipArmor_Mini.png'
Skills.skill[13].uiIndex = 206
Skills.skill.insert(14, None)
Skills.skill[14] = Dummy()
Skills.skill[14].activation = Dummy()
Skills.skill[14].activation.disableEvent = Dummy()
Skills.skill[14].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_S_FIREMANUVER_END
Skills.skill[14].activation.enableEvent = Dummy()
Skills.skill[14].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_S_FIREMANUVER_START
Skills.skill[14].cost = 1
Skills.skill[14].crewMemberSubTypes = []
Skills.skill[14].crewMemberSubTypes.insert(0, None)
Skills.skill[14].crewMemberSubTypes[0] = 0
Skills.skill[14].crewMemberSubTypes.insert(1, None)
Skills.skill[14].crewMemberSubTypes[1] = 1
Skills.skill[14].crewMemberSubTypes.insert(2, None)
Skills.skill[14].crewMemberSubTypes[2] = 2
Skills.skill[14].crewMemberSubTypes.insert(3, None)
Skills.skill[14].crewMemberSubTypes[3] = 3
Skills.skill[14].crewMemberTypes = []
Skills.skill[14].crewMemberTypes.insert(0, None)
Skills.skill[14].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[14].group = SKILL_GROUP.UNIQUE
Skills.skill[14].icoHudActivePath = 'icons/skills/hud/pilotSFireManuver_Active.png'
Skills.skill[14].icoHudPath = 'icons/skills/hud/pilotSFireManuver.png'
Skills.skill[14].icoPath = 'icons/skills/lobby/pilotSFireManuver.png'
Skills.skill[14].id = 213
Skills.skill[14].infotipsIcoPath = 'icons/skills/infotips/pilotSFireManuver.png'
Skills.skill[14].localizeTag = 'PILOT_S_FIREMANUVER'
Skills.skill[14].mods = []
Skills.skill[14].mods.insert(0, None)
Skills.skill[14].mods[0] = Dummy()
Skills.skill[14].mods[0].states = Dummy()
Skills.skill[14].mods[0].states.crit = 1.75
Skills.skill[14].mods[0].states.damaged = 1.75
Skills.skill[14].mods[0].states.good = 1.75
Skills.skill[14].mods[0].type = ModsTypeEnum.FIRE_DURATION
Skills.skill[14].order = 0
Skills.skill[14].smallIcoPath = 'icons/skills/lobby/pilotSFireManuver_Mini.png'
Skills.skill[14].uiIndex = 213
Skills.skill.insert(15, None)
Skills.skill[15] = Dummy()
Skills.skill[15].activation = Dummy()
Skills.skill[15].activation.disableEvent = Dummy()
Skills.skill[15].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_S_CRUISEFLIGHT_END
Skills.skill[15].activation.enableEvent = Dummy()
Skills.skill[15].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_S_CRUISEFLIGHT_START
Skills.skill[15].cost = 2
Skills.skill[15].crewMemberSubTypes = []
Skills.skill[15].crewMemberSubTypes.insert(0, None)
Skills.skill[15].crewMemberSubTypes[0] = 0
Skills.skill[15].crewMemberSubTypes.insert(1, None)
Skills.skill[15].crewMemberSubTypes[1] = 1
Skills.skill[15].crewMemberSubTypes.insert(2, None)
Skills.skill[15].crewMemberSubTypes[2] = 2
Skills.skill[15].crewMemberSubTypes.insert(3, None)
Skills.skill[15].crewMemberSubTypes[3] = 3
Skills.skill[15].crewMemberTypes = []
Skills.skill[15].crewMemberTypes.insert(0, None)
Skills.skill[15].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[15].group = SKILL_GROUP.UNIQUE
Skills.skill[15].icoHudActivePath = 'icons/skills/hud/pilotSCruiseFlight_Active.png'
Skills.skill[15].icoHudPath = 'icons/skills/hud/pilotSCruiseFlight.png'
Skills.skill[15].icoPath = 'icons/skills/lobby/pilotSCruiseFlight.png'
Skills.skill[15].id = 214
Skills.skill[15].infotipsIcoPath = 'icons/skills/infotips/pilotSCruiseFlight.png'
Skills.skill[15].localizeTag = 'PILOT_S_CRUISEFLIGHT'
Skills.skill[15].mods = []
Skills.skill[15].mods.insert(0, None)
Skills.skill[15].mods[0] = Dummy()
Skills.skill[15].mods[0].states = Dummy()
Skills.skill[15].mods[0].states.crit = 1.2
Skills.skill[15].mods[0].states.damaged = 1.2
Skills.skill[15].mods[0].states.good = 1.2
Skills.skill[15].mods[0].type = ModsTypeEnum.SIGHT_RANGE_PILOT
Skills.skill[15].mods.insert(1, None)
Skills.skill[15].mods[1] = Dummy()
Skills.skill[15].mods[1].states = Dummy()
Skills.skill[15].mods[1].states.crit = 1.03
Skills.skill[15].mods[1].states.damaged = 1.03
Skills.skill[15].mods[1].states.good = 1.03
Skills.skill[15].mods[1].type = ModsTypeEnum.ENGINE_POWER
Skills.skill[15].mods.insert(2, None)
Skills.skill[15].mods[2] = Dummy()
Skills.skill[15].mods[2].states = Dummy()
Skills.skill[15].mods[2].states.crit = 1.03
Skills.skill[15].mods[2].states.damaged = 1.03
Skills.skill[15].mods[2].states.good = 1.03
Skills.skill[15].mods[2].type = ModsTypeEnum.MAX_SPEED
Skills.skill[15].order = 1
Skills.skill[15].smallIcoPath = 'icons/skills/lobby/pilotSCruiseFlight_Mini.png'
Skills.skill[15].uiIndex = 214
Skills.skill.insert(16, None)
Skills.skill[16] = Dummy()
Skills.skill[16].activation = Dummy()
Skills.skill[16].activation.disableEvent = Dummy()
Skills.skill[16].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_S_DIEHARD_END
Skills.skill[16].activation.enableEvent = Dummy()
Skills.skill[16].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_S_DIEHARD_START
Skills.skill[16].cost = 3
Skills.skill[16].crewMemberSubTypes = []
Skills.skill[16].crewMemberSubTypes.insert(0, None)
Skills.skill[16].crewMemberSubTypes[0] = 0
Skills.skill[16].crewMemberSubTypes.insert(1, None)
Skills.skill[16].crewMemberSubTypes[1] = 1
Skills.skill[16].crewMemberSubTypes.insert(2, None)
Skills.skill[16].crewMemberSubTypes[2] = 2
Skills.skill[16].crewMemberSubTypes.insert(3, None)
Skills.skill[16].crewMemberSubTypes[3] = 3
Skills.skill[16].crewMemberTypes = []
Skills.skill[16].crewMemberTypes.insert(0, None)
Skills.skill[16].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[16].group = SKILL_GROUP.UNIQUE
Skills.skill[16].icoHudActivePath = 'icons/skills/hud/pilotSDiehard_Active.png'
Skills.skill[16].icoHudPath = 'icons/skills/hud/pilotSDiehard.png'
Skills.skill[16].icoPath = 'icons/skills/lobby/pilotSDiehard.png'
Skills.skill[16].id = 215
Skills.skill[16].infotipsIcoPath = 'icons/skills/infotips/pilotSDiehard.png'
Skills.skill[16].localizeTag = 'PILOT_S_DIEHARD'
Skills.skill[16].mods = []
Skills.skill[16].mods.insert(0, None)
Skills.skill[16].mods[0] = Dummy()
Skills.skill[16].mods[0].states = Dummy()
Skills.skill[16].mods[0].states.crit = 1.0
Skills.skill[16].mods[0].states.damaged = 1.0
Skills.skill[16].mods[0].states.good = 1.0
Skills.skill[16].mods[0].type = ModsTypeEnum.HP_RESTORE
Skills.skill[16].mods.insert(1, None)
Skills.skill[16].mods[1] = Dummy()
Skills.skill[16].mods[1].states = Dummy()
Skills.skill[16].mods[1].states.crit = 1.0
Skills.skill[16].mods[1].states.damaged = 1.0
Skills.skill[16].mods[1].states.good = 1.0
Skills.skill[16].mods[1].type = ModsTypeEnum.FIRE_EXTINGUISH_MANUAL
Skills.skill[16].mods.insert(2, None)
Skills.skill[16].mods[2] = Dummy()
Skills.skill[16].mods[2].states = Dummy()
Skills.skill[16].mods[2].states.crit = 1.0
Skills.skill[16].mods[2].states.damaged = 1.0
Skills.skill[16].mods[2].states.good = 1.0
Skills.skill[16].mods[2].type = ModsTypeEnum.FIX_TAIL_AND_WINGS
Skills.skill[16].mods.insert(3, None)
Skills.skill[16].mods[3] = Dummy()
Skills.skill[16].mods[3].states = Dummy()
Skills.skill[16].mods[3].states.crit = 1.0
Skills.skill[16].mods[3].states.damaged = 1.0
Skills.skill[16].mods[3].states.good = 1.0
Skills.skill[16].mods[3].type = ModsTypeEnum.ENGINE_RESTORE
Skills.skill[16].mods.insert(4, None)
Skills.skill[16].mods[4] = Dummy()
Skills.skill[16].mods[4].states = Dummy()
Skills.skill[16].mods[4].states.crit = 0.5
Skills.skill[16].mods[4].states.damaged = 0.5
Skills.skill[16].mods[4].states.good = 0.5
Skills.skill[16].mods[4].type = ModsTypeEnum.CLEAR_GUNS_OVERHEAT
Skills.skill[16].mods.insert(5, None)
Skills.skill[16].mods[5] = Dummy()
Skills.skill[16].mods[5].states = Dummy()
Skills.skill[16].mods[5].states.crit = 0.33
Skills.skill[16].mods[5].states.damaged = 0.33
Skills.skill[16].mods[5].states.good = 0.33
Skills.skill[16].mods[5].type = ModsTypeEnum.CLEAR_ENGINE_OVERHEAT
Skills.skill[16].mods.insert(6, None)
Skills.skill[16].mods[6] = Dummy()
Skills.skill[16].mods[6].states = Dummy()
Skills.skill[16].mods[6].states.crit = 1.05
Skills.skill[16].mods[6].states.damaged = 1.05
Skills.skill[16].mods[6].states.good = 1.05
Skills.skill[16].mods[6].type = ModsTypeEnum.ENGINE_POWER
Skills.skill[16].mods.insert(7, None)
Skills.skill[16].mods[7] = Dummy()
Skills.skill[16].mods[7].states = Dummy()
Skills.skill[16].mods[7].states.crit = 1.02
Skills.skill[16].mods[7].states.damaged = 1.02
Skills.skill[16].mods[7].states.good = 1.02
Skills.skill[16].mods[7].type = ModsTypeEnum.PITCH_MAX_SPEED_CFG
Skills.skill[16].mods.insert(8, None)
Skills.skill[16].mods[8] = Dummy()
Skills.skill[16].mods[8].states = Dummy()
Skills.skill[16].mods[8].states.crit = 1.1
Skills.skill[16].mods[8].states.damaged = 1.1
Skills.skill[16].mods[8].states.good = 1.1
Skills.skill[16].mods[8].type = ModsTypeEnum.ROLL_MAX_SPEED_CFG
Skills.skill[16].mods.insert(9, None)
Skills.skill[16].mods[9] = Dummy()
Skills.skill[16].mods[9].states = Dummy()
Skills.skill[16].mods[9].states.crit = 1.02
Skills.skill[16].mods[9].states.damaged = 1.02
Skills.skill[16].mods[9].states.good = 1.02
Skills.skill[16].mods[9].type = ModsTypeEnum.YAW_MAX_SPEED_CFG
Skills.skill[16].order = 2
Skills.skill[16].smallIcoPath = 'icons/skills/lobby/pilotSDiehard_Mini.png'
Skills.skill[16].uiIndex = 215
Skills.skill.insert(17, None)
Skills.skill[17] = Dummy()
Skills.skill[17].activation = Dummy()
Skills.skill[17].activation.disableEvent = Dummy()
Skills.skill[17].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_S_BLOODLUST_END
Skills.skill[17].activation.enableEvent = Dummy()
Skills.skill[17].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_S_BLOODLUST_START
Skills.skill[17].cost = 3
Skills.skill[17].crewMemberSubTypes = []
Skills.skill[17].crewMemberSubTypes.insert(0, None)
Skills.skill[17].crewMemberSubTypes[0] = 0
Skills.skill[17].crewMemberSubTypes.insert(1, None)
Skills.skill[17].crewMemberSubTypes[1] = 2
Skills.skill[17].crewMemberSubTypes.insert(2, None)
Skills.skill[17].crewMemberSubTypes[2] = 3
Skills.skill[17].crewMemberTypes = []
Skills.skill[17].crewMemberTypes.insert(0, None)
Skills.skill[17].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[17].group = SKILL_GROUP.UNIQUE
Skills.skill[17].icoHudActivePath = 'icons/skills/hud/pilotSBloodlust_Active.png'
Skills.skill[17].icoHudPath = 'icons/skills/hud/pilotSBloodlust.png'
Skills.skill[17].icoPath = 'icons/skills/lobby/pilotSBloodlust.png'
Skills.skill[17].id = 216
Skills.skill[17].infotipsIcoPath = 'icons/skills/infotips/pilotSBloodlust.png'
Skills.skill[17].localizeTag = 'PILOT_S_BLOODLUST'
Skills.skill[17].mods = []
Skills.skill[17].mods.insert(0, None)
Skills.skill[17].mods[0] = Dummy()
Skills.skill[17].mods[0].states = Dummy()
Skills.skill[17].mods[0].states.crit = 0.25
Skills.skill[17].mods[0].states.damaged = 0.25
Skills.skill[17].mods[0].states.good = 0.25
Skills.skill[17].mods[0].type = ModsTypeEnum.CLEAR_GUNS_OVERHEAT
Skills.skill[17].mods.insert(1, None)
Skills.skill[17].mods[1] = Dummy()
Skills.skill[17].mods[1].states = Dummy()
Skills.skill[17].mods[1].states.crit = 1.1
Skills.skill[17].mods[1].states.damaged = 1.1
Skills.skill[17].mods[1].states.good = 1.1
Skills.skill[17].mods[1].type = ModsTypeEnum.AUTOAIM_ANGLE
Skills.skill[17].mods.insert(2, None)
Skills.skill[17].mods[2] = Dummy()
Skills.skill[17].mods[2].states = Dummy()
Skills.skill[17].mods[2].states.crit = 1.1
Skills.skill[17].mods[2].states.damaged = 1.1
Skills.skill[17].mods[2].states.good = 1.1
Skills.skill[17].mods[2].type = ModsTypeEnum.WEAPONS_FOCUS
Skills.skill[17].order = 5
Skills.skill[17].smallIcoPath = 'icons/skills/lobby/pilotSBloodlust_Mini.png'
Skills.skill[17].uiIndex = 218
Skills.skill.insert(18, None)
Skills.skill[18] = Dummy()
Skills.skill[18].activation = Dummy()
Skills.skill[18].activation.disableEvent = Dummy()
Skills.skill[18].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_S_EVASIONMANUVER_END
Skills.skill[18].activation.enableEvent = Dummy()
Skills.skill[18].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_S_EVASIONMANUVER_START
Skills.skill[18].cost = 3
Skills.skill[18].crewMemberSubTypes = []
Skills.skill[18].crewMemberSubTypes.insert(0, None)
Skills.skill[18].crewMemberSubTypes[0] = 0
Skills.skill[18].crewMemberSubTypes.insert(1, None)
Skills.skill[18].crewMemberSubTypes[1] = 1
Skills.skill[18].crewMemberSubTypes.insert(2, None)
Skills.skill[18].crewMemberSubTypes[2] = 3
Skills.skill[18].crewMemberTypes = []
Skills.skill[18].crewMemberTypes.insert(0, None)
Skills.skill[18].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[18].group = SKILL_GROUP.UNIQUE
Skills.skill[18].icoHudActivePath = 'icons/skills/hud/pilotSEvasionManuver_Active.png'
Skills.skill[18].icoHudPath = 'icons/skills/hud/pilotSEvasionManuver.png'
Skills.skill[18].icoPath = 'icons/skills/lobby/pilotSEvasionManuver.png'
Skills.skill[18].id = 217
Skills.skill[18].infotipsIcoPath = 'icons/skills/infotips/pilotSEvasionManuver.png'
Skills.skill[18].localizeTag = 'PILOT_S_EVASIONMANUVER'
Skills.skill[18].mods = []
Skills.skill[18].mods.insert(0, None)
Skills.skill[18].mods[0] = Dummy()
Skills.skill[18].mods[0].states = Dummy()
Skills.skill[18].mods[0].states.crit = 0.75
Skills.skill[18].mods[0].states.damaged = 0.75
Skills.skill[18].mods[0].states.good = 0.75
Skills.skill[18].mods[0].type = ModsTypeEnum.DAMAGE_K
Skills.skill[18].mods.insert(1, None)
Skills.skill[18].mods[1] = Dummy()
Skills.skill[18].mods[1].states = Dummy()
Skills.skill[18].mods[1].states.crit = 0.75
Skills.skill[18].mods[1].states.damaged = 0.75
Skills.skill[18].mods[1].states.good = 0.75
Skills.skill[18].mods[1].type = ModsTypeEnum.VITALS_ARMOR
Skills.skill[18].mods.insert(2, None)
Skills.skill[18].mods[2] = Dummy()
Skills.skill[18].mods[2].states = Dummy()
Skills.skill[18].mods[2].states.crit = 0.75
Skills.skill[18].mods[2].states.damaged = 0.75
Skills.skill[18].mods[2].states.good = 0.75
Skills.skill[18].mods[2].type = ModsTypeEnum.SYSTEM_HP
Skills.skill[18].order = 3
Skills.skill[18].smallIcoPath = 'icons/skills/lobby/pilotSEvasionManuver_Mini.png'
Skills.skill[18].uiIndex = 216
Skills.skill.insert(19, None)
Skills.skill[19] = Dummy()
Skills.skill[19].activation = Dummy()
Skills.skill[19].activation.disableEvent = Dummy()
Skills.skill[19].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_S_BOOMZOOM_END
Skills.skill[19].activation.enableEvent = Dummy()
Skills.skill[19].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_S_BOOMZOOM_START
Skills.skill[19].cost = 3
Skills.skill[19].crewMemberSubTypes = []
Skills.skill[19].crewMemberSubTypes.insert(0, None)
Skills.skill[19].crewMemberSubTypes[0] = 0
Skills.skill[19].crewMemberSubTypes.insert(1, None)
Skills.skill[19].crewMemberSubTypes[1] = 1
Skills.skill[19].crewMemberSubTypes.insert(2, None)
Skills.skill[19].crewMemberSubTypes[2] = 2
Skills.skill[19].crewMemberTypes = []
Skills.skill[19].crewMemberTypes.insert(0, None)
Skills.skill[19].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[19].group = SKILL_GROUP.UNIQUE
Skills.skill[19].icoHudActivePath = 'icons/skills/hud/pilotSBoomzoom_Active.png'
Skills.skill[19].icoHudPath = 'icons/skills/hud/pilotSBoomzoom.png'
Skills.skill[19].icoPath = 'icons/skills/lobby/pilotSBoomzoom.png'
Skills.skill[19].id = 218
Skills.skill[19].infotipsIcoPath = 'icons/skills/infotips/pilotSBoomzoom.png'
Skills.skill[19].localizeTag = 'PILOT_S_BOOMZOOM'
Skills.skill[19].mods = []
Skills.skill[19].mods.insert(0, None)
Skills.skill[19].mods[0] = Dummy()
Skills.skill[19].mods[0].states = Dummy()
Skills.skill[19].mods[0].states.crit = 1.5
Skills.skill[19].mods[0].states.damaged = 1.5
Skills.skill[19].mods[0].states.good = 1.5
Skills.skill[19].mods[0].type = ModsTypeEnum.GUNS_INFLICT_CRIT
Skills.skill[19].mods.insert(1, None)
Skills.skill[19].mods[1] = Dummy()
Skills.skill[19].mods[1].states = Dummy()
Skills.skill[19].mods[1].states.crit = 1.5
Skills.skill[19].mods[1].states.damaged = 1.5
Skills.skill[19].mods[1].states.good = 1.5
Skills.skill[19].mods[1].type = ModsTypeEnum.GUNS_INFLICT_FIRE
Skills.skill[19].order = 4
Skills.skill[19].smallIcoPath = 'icons/skills/lobby/pilotSBoomzoom_Mini.png'
Skills.skill[19].uiIndex = 217
Skills.skill.insert(20, None)
Skills.skill[20] = Dummy()
Skills.skill[20].activation = Dummy()
Skills.skill[20].activation.disableEvent = Dummy()
Skills.skill[20].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_S_BOOMZOOM_END
Skills.skill[20].activation.enableEvent = Dummy()
Skills.skill[20].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_S_BOOMZOOM_START
Skills.skill[20].cost = 3
Skills.skill[20].crewMemberSubTypes = []
Skills.skill[20].crewMemberSubTypes.insert(0, None)
Skills.skill[20].crewMemberSubTypes[0] = 3
Skills.skill[20].crewMemberTypes = []
Skills.skill[20].crewMemberTypes.insert(0, None)
Skills.skill[20].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[20].group = SKILL_GROUP.UNIQUE
Skills.skill[20].icoHudActivePath = 'icons/skills/hud/pilotSValkyrie_Active.png'
Skills.skill[20].icoHudPath = 'icons/skills/hud/pilotSValkyrie.png'
Skills.skill[20].icoPath = 'icons/skills/lobby/pilotSValkyrie.png'
Skills.skill[20].id = 219
Skills.skill[20].infotipsIcoPath = 'icons/skills/infotips/pilotSValkyrie.png'
Skills.skill[20].localizeTag = 'PILOT_VALKYRIE'
Skills.skill[20].locked = true
Skills.skill[20].mods = []
Skills.skill[20].mods.insert(0, None)
Skills.skill[20].mods[0] = Dummy()
Skills.skill[20].mods[0].states = Dummy()
Skills.skill[20].mods[0].states.crit = 2.0
Skills.skill[20].mods[0].states.damaged = 2.0
Skills.skill[20].mods[0].states.good = 2.0
Skills.skill[20].mods[0].type = ModsTypeEnum.ROCKET_DAMAGE
Skills.skill[20].mods.insert(1, None)
Skills.skill[20].mods[1] = Dummy()
Skills.skill[20].mods[1].states = Dummy()
Skills.skill[20].mods[1].states.crit = 2.0
Skills.skill[20].mods[1].states.damaged = 2.0
Skills.skill[20].mods[1].states.good = 2.0
Skills.skill[20].mods[1].type = ModsTypeEnum.BOMB_DAMAGE
Skills.skill[20].order = 4
Skills.skill[20].smallIcoPath = 'icons/skills/lobby/pilotSValkyrie_Mini.png'
Skills.skill[20].uiIndex = 217
Skills.skill.insert(21, None)
Skills.skill[21] = Dummy()
Skills.skill[21].cost = 1
Skills.skill[21].crewMemberSubTypes = []
Skills.skill[21].crewMemberSubTypes.insert(0, None)
Skills.skill[21].crewMemberSubTypes[0] = 1
Skills.skill[21].crewMemberTypes = []
Skills.skill[21].crewMemberTypes.insert(0, None)
Skills.skill[21].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[21].group = SKILL_GROUP.COMMON
Skills.skill[21].icoPath = 'icons/skills/lobby/pilotBrightStar.png'
Skills.skill[21].id = 220
Skills.skill[21].infotipsIcoPath = 'icons/skills/infotips/pilotBrightStar.png'
Skills.skill[21].localizeTag = 'PILOT_BRIGHT_STAR'
Skills.skill[21].locked = true
Skills.skill[21].mods = []
Skills.skill[21].mods.insert(0, None)
Skills.skill[21].mods[0] = Dummy()
Skills.skill[21].mods[0].states = Dummy()
Skills.skill[21].mods[0].states.crit = 1.4
Skills.skill[21].mods[0].states.damaged = 1.4
Skills.skill[21].mods[0].states.good = 1.4
Skills.skill[21].mods[0].type = ModsTypeEnum.SIGHT_RANGE_PILOT
Skills.skill[21].mods.insert(1, None)
Skills.skill[21].mods[1] = Dummy()
Skills.skill[21].mods[1].states = Dummy()
Skills.skill[21].mods[1].states.crit = 1.1
Skills.skill[21].mods[1].states.damaged = 1.1
Skills.skill[21].mods[1].states.good = 1.1
Skills.skill[21].mods[1].type = ModsTypeEnum.VISIBILITY_FACTOR_TO_ENEMY
Skills.skill[21].order = 1
Skills.skill[21].smallIcoPath = 'icons/skills/lobby/pilotBrightStar_Mini.png'
Skills.skill[21].uiIndex = 202
Skills.skill.insert(22, None)
Skills.skill[22] = Dummy()
Skills.skill[22].activation = Dummy()
Skills.skill[22].activation.disableEvent = Dummy()
Skills.skill[22].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_S_CELESTIAL_FURY_END
Skills.skill[22].activation.enableEvent = Dummy()
Skills.skill[22].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_S_CELESTIAL_FURY_START
Skills.skill[22].cost = 3
Skills.skill[22].crewMemberSubTypes = []
Skills.skill[22].crewMemberSubTypes.insert(0, None)
Skills.skill[22].crewMemberSubTypes[0] = 1
Skills.skill[22].crewMemberTypes = []
Skills.skill[22].crewMemberTypes.insert(0, None)
Skills.skill[22].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[22].group = SKILL_GROUP.UNIQUE
Skills.skill[22].icoHudActivePath = 'icons/skills/hud/pilotSSkyFury_Active.png'
Skills.skill[22].icoHudPath = 'icons/skills/hud/pilotSSkyFury.png'
Skills.skill[22].icoPath = 'icons/skills/lobby/pilotSSkyFury.png'
Skills.skill[22].id = 221
Skills.skill[22].infotipsIcoPath = 'icons/skills/infotips/pilotSSkyFury.png'
Skills.skill[22].localizeTag = 'PILOT_SKY_FURY'
Skills.skill[22].locked = true
Skills.skill[22].mods = []
Skills.skill[22].mods.insert(0, None)
Skills.skill[22].mods[0] = Dummy()
Skills.skill[22].mods[0].states = Dummy()
Skills.skill[22].mods[0].states.crit = 1.2
Skills.skill[22].mods[0].states.damaged = 1.2
Skills.skill[22].mods[0].states.good = 1.2
Skills.skill[22].mods[0].type = ModsTypeEnum.GUNS_INCFLICT_DAMAGE
Skills.skill[22].mods.insert(1, None)
Skills.skill[22].mods[1] = Dummy()
Skills.skill[22].mods[1].states = Dummy()
Skills.skill[22].mods[1].states.crit = 1.2
Skills.skill[22].mods[1].states.damaged = 1.2
Skills.skill[22].mods[1].states.good = 1.2
Skills.skill[22].mods[1].type = ModsTypeEnum.GUNS_INFLICT_CRIT
Skills.skill[22].mods.insert(2, None)
Skills.skill[22].mods[2] = Dummy()
Skills.skill[22].mods[2].states = Dummy()
Skills.skill[22].mods[2].states.crit = 1.2
Skills.skill[22].mods[2].states.damaged = 1.2
Skills.skill[22].mods[2].states.good = 1.2
Skills.skill[22].mods[2].type = ModsTypeEnum.GUNS_INFLICT_FIRE
Skills.skill[22].order = 5
Skills.skill[22].smallIcoPath = 'icons/skills/lobby/pilotSSkyFury_Mini.png'
Skills.skill[22].uiIndex = 218
Skills.skill.insert(23, None)
Skills.skill[23] = Dummy()
Skills.skill[23].cost = 2
Skills.skill[23].crewMemberSubTypes = []
Skills.skill[23].crewMemberSubTypes.insert(0, None)
Skills.skill[23].crewMemberSubTypes[0] = 3
Skills.skill[23].crewMemberTypes = []
Skills.skill[23].crewMemberTypes.insert(0, None)
Skills.skill[23].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[23].group = SKILL_GROUP.COMMON
Skills.skill[23].icoPath = 'icons/skills/lobby/pilotFasterThanWind.png'
Skills.skill[23].id = 222
Skills.skill[23].infotipsIcoPath = 'icons/skills/infotips/pilotFasterThanWind.png'
Skills.skill[23].localizeTag = 'PILOT_FASTER_THAN_WIND'
Skills.skill[23].locked = true
Skills.skill[23].mods = []
Skills.skill[23].mods.insert(0, None)
Skills.skill[23].mods[0] = Dummy()
Skills.skill[23].mods[0].states = Dummy()
Skills.skill[23].mods[0].states.crit = 1.02
Skills.skill[23].mods[0].states.damaged = 1.02
Skills.skill[23].mods[0].states.good = 1.02
Skills.skill[23].mods[0].type = ModsTypeEnum.ENGINE_POWER
Skills.skill[23].mods.insert(1, None)
Skills.skill[23].mods[1] = Dummy()
Skills.skill[23].mods[1].states = Dummy()
Skills.skill[23].mods[1].states.crit = 1.1
Skills.skill[23].mods[1].states.damaged = 1.1
Skills.skill[23].mods[1].states.good = 1.1
Skills.skill[23].mods[1].type = ModsTypeEnum.WEP_WORK_TIME
Skills.skill[23].order = 3
Skills.skill[23].smallIcoPath = 'icons/skills/lobby/pilotFasterThanWind_Mini.png'
Skills.skill[23].uiIndex = 207
Skills.skill.insert(24, None)
Skills.skill[24] = Dummy()
Skills.skill[24].cost = 2
Skills.skill[24].crewMemberSubTypes = []
Skills.skill[24].crewMemberSubTypes.insert(0, None)
Skills.skill[24].crewMemberSubTypes[0] = 2
Skills.skill[24].crewMemberTypes = []
Skills.skill[24].crewMemberTypes.insert(0, None)
Skills.skill[24].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[24].group = SKILL_GROUP.COMMON
Skills.skill[24].icoPath = 'icons/skills/lobby/pilotExplosiveCharacter.png'
Skills.skill[24].id = 223
Skills.skill[24].infotipsIcoPath = 'icons/skills/infotips/pilotExplosiveCharacter.png'
Skills.skill[24].localizeTag = 'PILOT_EXPLOSIVE_CHARACTER'
Skills.skill[24].locked = true
Skills.skill[24].mods = []
Skills.skill[24].mods.insert(0, None)
Skills.skill[24].mods[0] = Dummy()
Skills.skill[24].mods[0].states = Dummy()
Skills.skill[24].mods[0].states.crit = 1.15
Skills.skill[24].mods[0].states.damaged = 1.15
Skills.skill[24].mods[0].states.good = 1.15
Skills.skill[24].mods[0].type = ModsTypeEnum.ROCKET_DAMAGE
Skills.skill[24].mods.insert(1, None)
Skills.skill[24].mods[1] = Dummy()
Skills.skill[24].mods[1].states = Dummy()
Skills.skill[24].mods[1].states.crit = 1.15
Skills.skill[24].mods[1].states.damaged = 1.15
Skills.skill[24].mods[1].states.good = 1.15
Skills.skill[24].mods[1].type = ModsTypeEnum.ROCKET_SPLASH
Skills.skill[24].mods.insert(2, None)
Skills.skill[24].mods[2] = Dummy()
Skills.skill[24].mods[2].states = Dummy()
Skills.skill[24].mods[2].states.crit = 1.15
Skills.skill[24].mods[2].states.damaged = 1.15
Skills.skill[24].mods[2].states.good = 1.15
Skills.skill[24].mods[2].type = ModsTypeEnum.BOMB_DAMAGE
Skills.skill[24].mods.insert(3, None)
Skills.skill[24].mods[3] = Dummy()
Skills.skill[24].mods[3].states = Dummy()
Skills.skill[24].mods[3].states.crit = 1.15
Skills.skill[24].mods[3].states.damaged = 1.15
Skills.skill[24].mods[3].states.good = 1.15
Skills.skill[24].mods[3].type = ModsTypeEnum.BOMB_SPLASH
Skills.skill[24].mods.insert(4, None)
Skills.skill[24].mods[4] = Dummy()
Skills.skill[24].mods[4].states = Dummy()
Skills.skill[24].mods[4].states.crit = 1.1
Skills.skill[24].mods[4].states.damaged = 1.1
Skills.skill[24].mods[4].states.good = 1.1
Skills.skill[24].mods[4].type = ModsTypeEnum.EXPLOSIVE_CHARACTER
Skills.skill[24].order = 5
Skills.skill[24].smallIcoPath = 'icons/skills/lobby/pilotExplosiveCharacter_Mini.png'
Skills.skill[24].uiIndex = 211
Skills.skill.insert(25, None)
Skills.skill[25] = Dummy()
Skills.skill[25].activation = Dummy()
Skills.skill[25].activation.disableEvent = Dummy()
Skills.skill[25].activation.disableEvent.eventID = consts.SKILL_EVENT.PILOT_HOT_CHICK_END
Skills.skill[25].activation.enableEvent = Dummy()
Skills.skill[25].activation.enableEvent.eventID = consts.SKILL_EVENT.PILOT_HOT_CHICK_START
Skills.skill[25].cost = 3
Skills.skill[25].crewMemberSubTypes = []
Skills.skill[25].crewMemberSubTypes.insert(0, None)
Skills.skill[25].crewMemberSubTypes[0] = 2
Skills.skill[25].crewMemberTypes = []
Skills.skill[25].crewMemberTypes.insert(0, None)
Skills.skill[25].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[25].group = SKILL_GROUP.UNIQUE
Skills.skill[25].icoHudActivePath = 'icons/skills/hud/pilotSSomeLikeItHot_Active.png'
Skills.skill[25].icoHudPath = 'icons/skills/hud/pilotSSomeLikeItHot.png'
Skills.skill[25].icoPath = 'icons/skills/lobby/pilotSSomeLikeItHot.png'
Skills.skill[25].id = 224
Skills.skill[25].infotipsIcoPath = 'icons/skills/infotips/pilotSSomeLikeItHot.png'
Skills.skill[25].localizeTag = 'PILOT_SOME_LIKE_IT_HOT'
Skills.skill[25].locked = true
Skills.skill[25].mods = []
Skills.skill[25].mods.insert(0, None)
Skills.skill[25].mods[0] = Dummy()
Skills.skill[25].mods[0].states = Dummy()
Skills.skill[25].mods[0].states.crit = 100.0
Skills.skill[25].mods[0].states.damaged = 100.0
Skills.skill[25].mods[0].states.good = 100.0
Skills.skill[25].mods[0].type = ModsTypeEnum.TEAM_OBJ_GUNS_INFLICT_FIRE
Skills.skill[25].order = 3
Skills.skill[25].smallIcoPath = 'icons/skills/lobby/pilotSSomeLikeItHot_Mini.png'
Skills.skill[25].uiIndex = 216
Skills.skill.insert(26, None)
Skills.skill[26] = Dummy()
Skills.skill[26].cost = 3
Skills.skill[26].crewMemberSubTypes = []
Skills.skill[26].crewMemberSubTypes.insert(0, None)
Skills.skill[26].crewMemberSubTypes[0] = 3
Skills.skill[26].crewMemberTypes = []
Skills.skill[26].crewMemberTypes.insert(0, None)
Skills.skill[26].crewMemberTypes[0] = SpecializationEnum.PILOT
Skills.skill[26].dependedFrom = 219
Skills.skill[26].group = SKILL_GROUP.IMPROVED
Skills.skill[26].icoPath = 'icons/skills/lobby/pilotKnowEngine_2.png'
Skills.skill[26].id = 225
Skills.skill[26].infotipsIcoPath = 'icons/skills/infotips/pilotKnowEngine_2.png'
Skills.skill[26].localizeTag = 'PILOT_FTW_KNOWENGINE_II'
Skills.skill[26].mods = []
Skills.skill[26].mods.insert(0, None)
Skills.skill[26].mods[0] = Dummy()
Skills.skill[26].mods[0].states = Dummy()
Skills.skill[26].mods[0].states.crit = 1.02
Skills.skill[26].mods[0].states.damaged = 1.02
Skills.skill[26].mods[0].states.good = 1.02
Skills.skill[26].mods[0].type = ModsTypeEnum.ENGINE_POWER
Skills.skill[26].mods.insert(1, None)
Skills.skill[26].mods[1] = Dummy()
Skills.skill[26].mods[1].states = Dummy()
Skills.skill[26].mods[1].states.crit = 1.02
Skills.skill[26].mods[1].states.damaged = 1.02
Skills.skill[26].mods[1].states.good = 1.02
Skills.skill[26].mods[1].type = ModsTypeEnum.MAX_SPEED
Skills.skill[26].order = 3
Skills.skill[26].smallIcoPath = 'icons/skills/lobby/pilotKnowEngine_2_Mini.png'
Skills.skill[26].uiIndex = 208
Skills.skill.insert(27, None)
Skills.skill[27] = Dummy()
Skills.skill[27].cost = 1
Skills.skill[27].crewMemberSubTypes = []
Skills.skill[27].crewMemberSubTypes.insert(0, None)
Skills.skill[27].crewMemberSubTypes[0] = 0
Skills.skill[27].crewMemberTypes = []
Skills.skill[27].crewMemberTypes.insert(0, None)
Skills.skill[27].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[27].group = SKILL_GROUP.COMMON
Skills.skill[27].icoPath = 'icons/skills/lobby/gunnerTough.png'
Skills.skill[27].id = 241
Skills.skill[27].infotipsIcoPath = 'icons/skills/infotips/gunnerTough.png'
Skills.skill[27].localizeTag = 'GUNNER_TOUGH'
Skills.skill[27].mods = []
Skills.skill[27].mods.insert(0, None)
Skills.skill[27].mods[0] = Dummy()
Skills.skill[27].mods[0].states = Dummy()
Skills.skill[27].mods[0].states.crit = 0.8
Skills.skill[27].mods[0].states.damaged = 0.8
Skills.skill[27].mods[0].states.good = 0.8
Skills.skill[27].mods[0].type = ModsTypeEnum.CRIT_WEAKNESS_GUNNER
Skills.skill[27].order = 0
Skills.skill[27].smallIcoPath = 'icons/skills/lobby/gunnerTough_Mini.png'
Skills.skill[27].uiIndex = 241
Skills.skill.insert(28, None)
Skills.skill[28] = Dummy()
Skills.skill[28].cost = 1
Skills.skill[28].crewMemberSubTypes = []
Skills.skill[28].crewMemberSubTypes.insert(0, None)
Skills.skill[28].crewMemberSubTypes[0] = 0
Skills.skill[28].crewMemberTypes = []
Skills.skill[28].crewMemberTypes.insert(0, None)
Skills.skill[28].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[28].group = SKILL_GROUP.COMMON
Skills.skill[28].icoPath = 'icons/skills/lobby/gunnerSightRange.png'
Skills.skill[28].id = 242
Skills.skill[28].infotipsIcoPath = 'icons/skills/infotips/gunnerSightRange.png'
Skills.skill[28].localizeTag = 'GUNNER_SIGHTRANGE'
Skills.skill[28].mods = []
Skills.skill[28].mods.insert(0, None)
Skills.skill[28].mods[0] = Dummy()
Skills.skill[28].mods[0].states = Dummy()
Skills.skill[28].mods[0].states.crit = 1.2
Skills.skill[28].mods[0].states.damaged = 1.2
Skills.skill[28].mods[0].states.good = 1.2
Skills.skill[28].mods[0].type = ModsTypeEnum.SIGHT_RANGE_GUNNER
Skills.skill[28].order = 1
Skills.skill[28].smallIcoPath = 'icons/skills/lobby/gunnerSightRange_Mini.png'
Skills.skill[28].uiIndex = 242
Skills.skill.insert(29, None)
Skills.skill[29] = Dummy()
Skills.skill[29].cost = 2
Skills.skill[29].crewMemberSubTypes = []
Skills.skill[29].crewMemberSubTypes.insert(0, None)
Skills.skill[29].crewMemberSubTypes[0] = 0
Skills.skill[29].crewMemberTypes = []
Skills.skill[29].crewMemberTypes.insert(0, None)
Skills.skill[29].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[29].group = SKILL_GROUP.COMMON
Skills.skill[29].icoPath = 'icons/skills/lobby/gunnerVolley.png'
Skills.skill[29].id = 243
Skills.skill[29].infotipsIcoPath = 'icons/skills/infotips/gunnerVolley.png'
Skills.skill[29].localizeTag = 'GUNNER_VOLLEY'
Skills.skill[29].mods = []
Skills.skill[29].mods.insert(0, None)
Skills.skill[29].mods[0] = Dummy()
Skills.skill[29].mods[0].states = Dummy()
Skills.skill[29].mods[0].states.crit = 1.2
Skills.skill[29].mods[0].states.damaged = 1.2
Skills.skill[29].mods[0].states.good = 1.2
Skills.skill[29].mods[0].type = ModsTypeEnum.GUNNER_BURST_TIME_MODIFIER
Skills.skill[29].order = 2
Skills.skill[29].smallIcoPath = 'icons/skills/lobby/gunnerVolley_Mini.png'
Skills.skill[29].uiIndex = 243
Skills.skill.insert(30, None)
Skills.skill[30] = Dummy()
Skills.skill[30].cost = 3
Skills.skill[30].crewMemberSubTypes = []
Skills.skill[30].crewMemberSubTypes.insert(0, None)
Skills.skill[30].crewMemberSubTypes[0] = 0
Skills.skill[30].crewMemberTypes = []
Skills.skill[30].crewMemberTypes.insert(0, None)
Skills.skill[30].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[30].dependedFrom = 243
Skills.skill[30].group = SKILL_GROUP.IMPROVED
Skills.skill[30].icoPath = 'icons/skills/lobby/gunnerLongRange.png'
Skills.skill[30].id = 244
Skills.skill[30].infotipsIcoPath = 'icons/skills/infotips/gunnerLongRange.png'
Skills.skill[30].localizeTag = 'GUNNER_LONGRANGE'
Skills.skill[30].mods = []
Skills.skill[30].mods.insert(0, None)
Skills.skill[30].mods[0] = Dummy()
Skills.skill[30].mods[0].states = Dummy()
Skills.skill[30].mods[0].states.crit = 1.15
Skills.skill[30].mods[0].states.damaged = 1.15
Skills.skill[30].mods[0].states.good = 1.15
Skills.skill[30].mods[0].type = ModsTypeEnum.TURRET_RANGE
Skills.skill[30].mods.insert(1, None)
Skills.skill[30].mods[1] = Dummy()
Skills.skill[30].mods[1].relation = Dummy()
Skills.skill[30].mods[1].relation.type = []
Skills.skill[30].mods[1].relation.type.insert(0, None)
Skills.skill[30].mods[1].relation.type[0] = ModsTypeEnum.TURRET_RANGE
Skills.skill[30].mods[1].states = Dummy()
Skills.skill[30].mods[1].states.crit = 1.2
Skills.skill[30].mods[1].states.damaged = 1.2
Skills.skill[30].mods[1].states.good = 1.2
Skills.skill[30].mods[1].type = ModsTypeEnum.EQUIPMENT_EFFECT
Skills.skill[30].order = 2
Skills.skill[30].smallIcoPath = 'icons/skills/lobby/gunnerLongRange_Mini.png'
Skills.skill[30].uiIndex = 244
Skills.skill.insert(31, None)
Skills.skill[31] = Dummy()
Skills.skill[31].cost = 2
Skills.skill[31].crewMemberSubTypes = []
Skills.skill[31].crewMemberSubTypes.insert(0, None)
Skills.skill[31].crewMemberSubTypes[0] = 0
Skills.skill[31].crewMemberTypes = []
Skills.skill[31].crewMemberTypes.insert(0, None)
Skills.skill[31].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[31].group = SKILL_GROUP.COMMON
Skills.skill[31].icoPath = 'icons/skills/lobby/gunnerNimble.png'
Skills.skill[31].id = 245
Skills.skill[31].infotipsIcoPath = 'icons/skills/infotips/gunnerNimble.png'
Skills.skill[31].localizeTag = 'GUNNER_NIMBLE'
Skills.skill[31].mods = []
Skills.skill[31].mods.insert(0, None)
Skills.skill[31].mods[0] = Dummy()
Skills.skill[31].mods[0].states = Dummy()
Skills.skill[31].mods[0].states.crit = 0.5
Skills.skill[31].mods[0].states.damaged = 0.5
Skills.skill[31].mods[0].states.good = 0.5
Skills.skill[31].mods[0].type = ModsTypeEnum.GUNNER_REDUCTION_TIME
Skills.skill[31].order = 3
Skills.skill[31].smallIcoPath = 'icons/skills/lobby/gunnerNimble_Mini.png'
Skills.skill[31].uiIndex = 245
Skills.skill.insert(32, None)
Skills.skill[32] = Dummy()
Skills.skill[32].cost = 3
Skills.skill[32].crewMemberSubTypes = []
Skills.skill[32].crewMemberSubTypes.insert(0, None)
Skills.skill[32].crewMemberSubTypes[0] = 0
Skills.skill[32].crewMemberTypes = []
Skills.skill[32].crewMemberTypes.insert(0, None)
Skills.skill[32].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[32].group = SKILL_GROUP.IMPROVED
Skills.skill[32].icoPath = 'icons/skills/lobby/gunnerPunisher.png'
Skills.skill[32].id = 246
Skills.skill[32].infotipsIcoPath = 'icons/skills/infotips/gunnerPunisher.png'
Skills.skill[32].localizeTag = 'GUNNER_PUNISHER'
Skills.skill[32].mods = []
Skills.skill[32].mods.insert(0, None)
Skills.skill[32].mods[0] = Dummy()
Skills.skill[32].mods[0].states = Dummy()
Skills.skill[32].mods[0].states.crit = 500.0
Skills.skill[32].mods[0].states.damaged = 500.0
Skills.skill[32].mods[0].states.good = 500.0
Skills.skill[32].mods[0].type = ModsTypeEnum.TURRET_INFLICT_CRIT
Skills.skill[32].order = 4
Skills.skill[32].smallIcoPath = 'icons/skills/lobby/gunnerPunisher_Mini.png'
Skills.skill[32].uiIndex = 247
Skills.skill.insert(33, None)
Skills.skill[33] = Dummy()
Skills.skill[33].cost = 4
Skills.skill[33].crewMemberSubTypes = []
Skills.skill[33].crewMemberSubTypes.insert(0, None)
Skills.skill[33].crewMemberSubTypes[0] = 0
Skills.skill[33].crewMemberTypes = []
Skills.skill[33].crewMemberTypes.insert(0, None)
Skills.skill[33].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[33].group = SKILL_GROUP.IMPROVED
Skills.skill[33].icoPath = 'icons/skills/lobby/gunnerKiller.png'
Skills.skill[33].id = 247
Skills.skill[33].infotipsIcoPath = 'icons/skills/infotips/gunnerKiller.png'
Skills.skill[33].localizeTag = 'GUNNER_KILLER'
Skills.skill[33].mods = []
Skills.skill[33].mods.insert(0, None)
Skills.skill[33].mods[0] = Dummy()
Skills.skill[33].mods[0].states = Dummy()
Skills.skill[33].mods[0].states.crit = 1.1
Skills.skill[33].mods[0].states.damaged = 1.1
Skills.skill[33].mods[0].states.good = 1.1
Skills.skill[33].mods[0].type = ModsTypeEnum.GUNNER_ENEMYHP_WATCHER
Skills.skill[33].order = 5
Skills.skill[33].smallIcoPath = 'icons/skills/lobby/gunnerKiller_Mini.png'
Skills.skill[33].uiIndex = 248
Skills.skill.insert(34, None)
Skills.skill[34] = Dummy()
Skills.skill[34].activation = Dummy()
Skills.skill[34].activation.disableEvent = Dummy()
Skills.skill[34].activation.disableEvent.eventID = consts.SKILL_EVENT.GUNNER_PROTECTOR_END
Skills.skill[34].activation.enableEvent = Dummy()
Skills.skill[34].activation.enableEvent.eventID = consts.SKILL_EVENT.GUNNER_PROTECTOR_START
Skills.skill[34].cost = 3
Skills.skill[34].crewMemberSubTypes = []
Skills.skill[34].crewMemberSubTypes.insert(0, None)
Skills.skill[34].crewMemberSubTypes[0] = 0
Skills.skill[34].crewMemberTypes = []
Skills.skill[34].crewMemberTypes.insert(0, None)
Skills.skill[34].crewMemberTypes[0] = SpecializationEnum.GUNNER
Skills.skill[34].group = SKILL_GROUP.IMPROVED
Skills.skill[34].icoPath = 'icons/skills/lobby/gunnerProtector.png'
Skills.skill[34].id = 248
Skills.skill[34].infotipsIcoPath = 'icons/skills/infotips/gunnerProtector.png'
Skills.skill[34].localizeTag = 'GUNNER_PROTECTOR'
Skills.skill[34].mods = []
Skills.skill[34].mods.insert(0, None)
Skills.skill[34].mods[0] = Dummy()
Skills.skill[34].mods[0].states = Dummy()
Skills.skill[34].mods[0].states.crit = 0.7
Skills.skill[34].mods[0].states.damaged = 0.7
Skills.skill[34].mods[0].states.good = 0.7
Skills.skill[34].mods[0].type = ModsTypeEnum.GUNNER_BARRAGE_FIRE
Skills.skill[34].order = 3
Skills.skill[34].smallIcoPath = 'icons/skills/lobby/gunnerProtector_Mini.png'
Skills.skill[34].uiIndex = 246

def __xreload_old_new__(namespace, name, oldObj, newObj):
    from config_consts import IS_DEVELOPMENT
    if IS_DEVELOPMENT:
        namespace[name] = newObj
        import BigWorld
        BigWorld.globalData['modifiersUpdateRequired'] = True


SkillDB = None
SpecializationSkillDB = None
SkillWithRelationsDB = None

def initDB():
    global SkillWithRelationsDB
    global SpecializationSkillDB
    global SkillDB
    if SkillDB is None:
        SkillDB = {}
        SpecializationSkillDB = {}
        SkillWithRelationsDB = {}
        for skill in Skills.skill:
            SkillDB[skill.id] = skill
            if hasattr(skill, 'mainForSpecialization'):
                SpecializationSkillDB[skill.mainForSpecialization] = skill
                skill.name = 'LOBBY_CREW_HEADER_' + skill.localizeTag
                skill.description = 'LOBBY_CREW_LABEL_' + skill.localizeTag
                skill.fullDescription = 'LOBBY_CREW_LABEL_' + skill.localizeTag
                skill.middleDescription = 'LOBBY_CREW_LABEL_PLACE_FOR_' + skill.localizeTag
            else:
                skill.name = 'SKILL_NAME_' + skill.localizeTag
                skill.description = 'SKILL_DESCRIPTION_SHORT_' + skill.localizeTag
                skill.fullDescription = 'SKILL_DESCRIPTION_' + skill.localizeTag
                skill.middleDescription = 'SKILL_DESCRIPTION_MIDDLE_' + skill.localizeTag
            skill.activation = getattr(skill, 'activation', None)
            if skill.activation:
                skill.activation.isOneTimeAction = bool(getattr(skill.activation, 'isOneTimeAction', False))
            for mod in skill.mods:
                mod.states = [mod.states.good, mod.states.damaged, mod.states.crit]
                if hasattr(mod, 'relation'):
                    SkillWithRelationsDB[skill.id] = [mod.type, mod.relation.type]

    return


initDB()