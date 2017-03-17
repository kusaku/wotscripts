# Embedded file name: scripts/common/DictKeys.py
NEW_AVATARS_INFO_KEYS_DICT = {'classID': 1,
 'squadID': 2,
 'unitNumber': 3,
 'isChatBan': 4,
 'rateID': 5,
 'stats': 6,
 'playerName': 7,
 'teamIndex': 8,
 'planeType': 9,
 'avatarID': 10,
 'airplaneInfo': 11,
 'fragsTeamObjects': 12,
 'flags': 13,
 'frags': 14,
 'lifes': 15,
 'decals': 16,
 'weaponsSlot': 17,
 'plane': 18,
 'giveAmmo': 19,
 'globalID': 20,
 'shells': 21,
 'logicalParts': 22,
 'parts': 23,
 'camouflage': 24,
 'crew': 25,
 'planeLevel': 26,
 'key': 27,
 'value': 28,
 'clanAbbrev': 29,
 'clanDBID': 30,
 'assists': 31,
 'assistsGround': 32,
 'disguise': 33,
 'databaseID': 34,
 'maxHealth': 35,
 'score': 36,
 'attrs': 37,
 'equipment': 38,
 'crewBodyType': 39}
NEW_AVATARS_INFO_KEYS_INVERT_DICT = dict(((v, k) for k, v in NEW_AVATARS_INFO_KEYS_DICT.items()))
REPORT_BATTLE_RESULT_KEYS_DICT = {'spottedList': 1,
 'shots': 3,
 'hitted': 4,
 'received': 5,
 'winState': 6,
 'gameResult': 8,
 'playersData': 9,
 'credits': 11,
 'xp': 12,
 'xpCoeff': 13,
 'creditsPenalty': 14,
 'xpPenalty': 15,
 'creditsFromTK': 16,
 'hitsStructure': 17,
 'shotsReceivedStructure': 18,
 'killerID': 19,
 'damagedTurrets': 20,
 'damagedGroundObjects': 21,
 'damagedBaseObjects': 22,
 'damagedPlanes': 23,
 'killedTurrets': 24,
 'killedGroundObjects': 25,
 'killedBaseObjects': 26,
 'killedPlanes': 27,
 'avatarID': 28,
 'fragsTeamObjects': 29,
 'frags': 30,
 'dead': 31,
 'assists': 32,
 'assistsGround': 33,
 'xpFactor': 34,
 'crFactor': 35,
 'crCoeff': 36}
REPORT_BATTLE_RESULT_KEYS_INVERT_DICT = dict(((v, k) for k, v in REPORT_BATTLE_RESULT_KEYS_DICT.items()))

class STATS_KEYS:
    killerID = 1
    killerType = 2
    deadPosition = 3
    deadTime = 4
    presenceTime = 5
    survived = 6
    spottedBy = 7
    shotsArray = 8
    shotsReceivedMap = 9
    piercingHitsReceivedMap = 10
    hitsCausedFireMap = 11
    criticalHitsMap = 12
    shotsReceivedStructure = 13
    damageReceivedMap = 14
    damageReceivedStructure = 15
    damageReceivedRamming = 16
    damageReceivedByFire = 17
    controllerProfileName = 18
    graphicsDetails = 19
    minFPS = 20
    medFPS = 21
    fpsRanges = 22
    partStates = 23
    globalID = 24
    minPing = 25
    medPing = 26
    lostRatio = 27
    keyboardUsagePercent = 28
    mouseUsagePercent = 29
    joystickUsagePercent = 30
    autopilotsCount = 31
    borderReachedCount = 32
    battleActivityPoints = 34
    squadActivityPoints = 35
    equipment = 36
    consumablesCount = 37
    bombsCount = 38
    rocketsCount = 39
    beltsCount = 40
    spentBelts = 41
    spentShells = 42
    pilotDamaged = 46
    averageSpeed = 47
    killerPosition = 48
    usedConsumablesSlots = 49
    eachTimeSpottedCount = 50
    planeDamagePercent = 51
    crewSkills = 52
    myDamagedParts = 53
    damageReceivedFromGunnerFire = 54
    firesFromGunnerMap = 55
    hitsArray = 56
    shotsReachedGoalArray = 57
    hitsStructure = 58
    TKhitsPlane = 59
    damageReceivedFromHighAltitudeTurrets = 60
    damageReceivedFromCommonTurrets = 61
    hitsReceivedFromHighAltitudeTurrets = 62
    hitsReceivedFromCommonTurrets = 63
    distinctFiresCount = 64
    effectActions = 65
    mainArmamentHitPlanes = 66
    mainArmamentHitStructures = 67
    stallCount = 68
    engineOverheatsCount = 69
    criticalCritReasons = 70
    skillsActivationCount = 71
    skillsActiveTime = 72
    damageReceivedFirstTime = 73
    skipIntro = 74


STATS_KEYS_INVERT_DICT = dict(((v, k) for k, v in STATS_KEYS.__dict__.items()))