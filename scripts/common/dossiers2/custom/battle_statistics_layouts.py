# Embedded file name: scripts/common/dossiers2/custom/battle_statistics_layouts.py
from dossiers2.common.DossierBlockBuilders import *
from dossiers2.custom.dependencies import VEH_TYPE_FRAGS_DEPENDENCIES
from dossiers2.custom.dependencies import A15X15_STATS_DEPENDENCIES
from dossiers2.custom.dependencies import CLAN_STATS_DEPENDENCIES
from dossiers2.custom.dependencies import A7X7_STATS_DEPENDENCIES
from dossiers2.custom.dependencies import HISTORICAL_STATS_DEPENDENCIES
from dossiers2.custom.dependencies import FORT_BATTLES_STATS_DEPENDENCIES
from dossiers2.custom.dependencies import FORT_SORTIES_STATS_DEPENDENCIES
A15X15_BLOCK_LAYOUT = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'xpBefore8_8',
 'battlesCountBefore8_8',
 'winAndSurvived',
 'frags8p',
 'battlesCountBefore9_0']
A15X15_2_BLOCK_LAYOUT = ['originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
CLAN_BLOCK_LAYOUT = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'xpBefore8_9',
 'battlesCountBefore8_9',
 'battlesCountBefore9_0']
CLAN2_BLOCK_LAYOUT = ['originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
COMPANY_BLOCK_LAYOUT = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'xpBefore8_9',
 'battlesCountBefore8_9',
 'battlesCountBefore9_0']
COMPANY2_BLOCK_LAYOUT = ['originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
A7X7_BLOCK_LAYOUT = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'winAndSurvived',
 'frags8p',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'battlesCountBefore9_0',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
RATED_7X7_BLOCK_LAYOUT = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'winAndSurvived',
 'frags8p',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
HISTORICAL_BLOCK_LAYOUT = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'winAndSurvived',
 'frags8p',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
FORT_BLOCK_LAYOUT_BASE = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'winAndSurvived',
 'frags8p',
 'potentialDamageReceived',
 'damageBlockedByArmor']
FORT_BLOCK_LAYOUT = FORT_BLOCK_LAYOUT_BASE + ['battlesOnStunningVehicles', 'stunNum', 'damageAssistedStun']
GLOBAL_MAP_BLOCK_LAYOUT = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'winAndSurvived',
 'frags8p',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'xpBefore8_9',
 'battlesCountBefore8_9',
 'battlesCountBefore9_0',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
RANKED_BLOCK_LAYOUT = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'winAndSurvived',
 'frags8p',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
FALLOUT_VEHICLE_BLOCK_LAYOUT_BASE = ['xp',
 'battlesCount',
 'wins',
 'losses',
 'survivedBattles',
 'frags',
 'shots',
 'directHits',
 'spotted',
 'damageDealt',
 'damageReceived',
 'capturePoints',
 'droppedCapturePoints',
 'originalXP',
 'damageAssistedTrack',
 'damageAssistedRadio',
 'directHitsReceived',
 'noDamageDirectHitsReceived',
 'piercingsReceived',
 'explosionHitsReceived',
 'explosionHits',
 'piercings',
 'winAndSurvived',
 'frags8p',
 'potentialDamageReceived',
 'damageBlockedByArmor',
 'winPoints',
 'flagCapture',
 'soloFlagCapture',
 'coins',
 'resourceAbsorbed',
 'deathCount']
FALLOUT_VEHICLE_BLOCK_LAYOUT = FALLOUT_VEHICLE_BLOCK_LAYOUT_BASE + ['battlesOnStunningVehicles', 'stunNum', 'damageAssistedStun']
FALLOUT_BLOCK_LAYOUT = FALLOUT_VEHICLE_BLOCK_LAYOUT_BASE + ['avatarDamageDealt',
 'avatarKills',
 'battlesOnStunningVehicles',
 'stunNum',
 'damageAssistedStun']
MAX_BLOCK_LAYOUT = ['maxXP', 'maxFrags', 'maxDamage']
MAX_AND_BEST_VEHICLE_BLOCK_LAYOUT = MAX_BLOCK_LAYOUT + ['maxXPVehicle', 'maxFragsVehicle', 'maxDamageVehicle']
MAX_FALLOUT_BLOCK_LAYOUT = MAX_BLOCK_LAYOUT + ['maxWinPoints', 'maxCoins']
MAX_FALLOUT_BLOCK_LAYOUT_WITH_AVATAR = MAX_FALLOUT_BLOCK_LAYOUT + ['maxFragsWithAvatar', 'maxDamageWithAvatar']