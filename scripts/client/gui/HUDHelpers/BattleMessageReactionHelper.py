# Embedded file name: scripts/client/gui/HUDHelpers/BattleMessageReactionHelper.py
from random import choice
from consts import BATTLE_MESSAGE_TYPE
from Helpers.i18n import localizeBattleMessageReaction
USE_STANDARD_MESSAGE_TEXT = True
USE_COLORS = True
USE_MULTIPLE_STRINGS = False
POSITIVE_REACTION_COLOR = '#ffc364'
NEGATIVE_REACTION_COLOR = '#c9c9b6'
POSITIVE_REACTION_COLOR_ALT = '#ffff00'
NEGATIVE_REACTION_COLOR_ALT = '#c9c9b6'
BATTLE_MESSAGE_TYPE_RESULT_MAP_POSITIVE = {BATTLE_MESSAGE_TYPE.NEED_SHELTER: BATTLE_MESSAGE_TYPE.JOIN_ME,
 BATTLE_MESSAGE_TYPE.SOS: BATTLE_MESSAGE_TYPE.JOIN_ME,
 BATTLE_MESSAGE_TYPE.JOIN_ME: BATTLE_MESSAGE_TYPE.GOT_IT,
 BATTLE_MESSAGE_TYPE.ENEMY_MY_AIM: BATTLE_MESSAGE_TYPE.GOT_IT}
SINGLE_STRING_MAP = {(BATTLE_MESSAGE_TYPE.NEED_SHELTER, True): 3,
 (BATTLE_MESSAGE_TYPE.NEED_SHELTER, False): 6,
 (BATTLE_MESSAGE_TYPE.SOS, True): 3,
 (BATTLE_MESSAGE_TYPE.SOS, False): 6,
 (BATTLE_MESSAGE_TYPE.JOIN_ME, True): 3,
 (BATTLE_MESSAGE_TYPE.JOIN_ME, False): 1,
 (BATTLE_MESSAGE_TYPE.ENEMY_MY_AIM, True): 2,
 (BATTLE_MESSAGE_TYPE.ENEMY_MY_AIM, False): 1}
BATTLE_MESSAGE_LOCALE_MAP = {(BATTLE_MESSAGE_TYPE.NEED_SHELTER, True): ['SOS_PLAYER_ACCEPTED_01',
                                            'SOS_PLAYER_ACCEPTED_02',
                                            'SOS_PLAYER_ACCEPTED_03',
                                            'SOS_PLAYER_ACCEPTED_04',
                                            'SOS_PLAYER_ACCEPTED_05',
                                            'SOS_PLAYER_ACCEPTED_06',
                                            'SOS_PLAYER_ACCEPTED_07',
                                            'SOS_PLAYER_ACCEPTED_08',
                                            'SOS_PLAYER_ACCEPTED_09',
                                            'SOS_PLAYER_ACCEPTED_10'],
 (BATTLE_MESSAGE_TYPE.NEED_SHELTER, False): ['SOS_PLAYER_DENIED_01',
                                             'SOS_PLAYER_DENIED_02',
                                             'SOS_PLAYER_DENIED_03',
                                             'SOS_PLAYER_DENIED_04',
                                             'SOS_PLAYER_DENIED_05',
                                             'SOS_PLAYER_DENIED_06',
                                             'SOS_PLAYER_DENIED_07',
                                             'SOS_PLAYER_DENIED_08',
                                             'SOS_PLAYER_DENIED_09',
                                             'SOS_PLAYER_DENIED_10',
                                             'SOS_PLAYER_DENIED_11'],
 (BATTLE_MESSAGE_TYPE.SOS, True): ['SOS_PLAYER_ACCEPTED_01',
                                   'SOS_PLAYER_ACCEPTED_02',
                                   'SOS_PLAYER_ACCEPTED_03',
                                   'SOS_PLAYER_ACCEPTED_04',
                                   'SOS_PLAYER_ACCEPTED_05',
                                   'SOS_PLAYER_ACCEPTED_06',
                                   'SOS_PLAYER_ACCEPTED_07',
                                   'SOS_PLAYER_ACCEPTED_08',
                                   'SOS_PLAYER_ACCEPTED_09',
                                   'SOS_PLAYER_ACCEPTED_10'],
 (BATTLE_MESSAGE_TYPE.SOS, False): ['SOS_PLAYER_DENIED_01',
                                    'SOS_PLAYER_DENIED_02',
                                    'SOS_PLAYER_DENIED_03',
                                    'SOS_PLAYER_DENIED_04',
                                    'SOS_PLAYER_DENIED_05',
                                    'SOS_PLAYER_DENIED_06',
                                    'SOS_PLAYER_DENIED_07',
                                    'SOS_PLAYER_DENIED_08',
                                    'SOS_PLAYER_DENIED_09',
                                    'SOS_PLAYER_DENIED_10',
                                    'SOS_PLAYER_DENIED_11'],
 (BATTLE_MESSAGE_TYPE.JOIN_ME, True): ['ATTACK_TARGET_ACCEPTED_01',
                                       'ATTACK_TARGET_ACCEPTED_02',
                                       'ATTACK_TARGET_ACCEPTED_03',
                                       'ATTACK_TARGET_ACCEPTED_04',
                                       'ATTACK_TARGET_ACCEPTED_05',
                                       'ATTACK_TARGET_ACCEPTED_06',
                                       'ATTACK_TARGET_ACCEPTED_07',
                                       'ATTACK_TARGET_ACCEPTED_08',
                                       'ATTACK_TARGET_ACCEPTED_09',
                                       'ATTACK_TARGET_ACCEPTED_10'],
 (BATTLE_MESSAGE_TYPE.JOIN_ME, False): ['ATTACK_TARGET_DENIED_01',
                                        'ATTACK_TARGET_DENIED_02',
                                        'ATTACK_TARGET_DENIED_03',
                                        'ATTACK_TARGET_DENIED_04',
                                        'ATTACK_TARGET_DENIED_05',
                                        'ATTACK_TARGET_DENIED_06',
                                        'ATTACK_TARGET_DENIED_07',
                                        'ATTACK_TARGET_DENIED_08',
                                        'ATTACK_TARGET_DENIED_09',
                                        'ATTACK_TARGET_DENIED_10'],
 (BATTLE_MESSAGE_TYPE.ENEMY_MY_AIM, True): ['TARGET_IS_MY_ACCEPTED_01',
                                            'TARGET_IS_MY_ACCEPTED_02',
                                            'TARGET_IS_MY_ACCEPTED_03',
                                            'TARGET_IS_MY_ACCEPTED_04',
                                            'TARGET_IS_MY_ACCEPTED_05',
                                            'TARGET_IS_MY_ACCEPTED_06',
                                            'TARGET_IS_MY_ACCEPTED_07',
                                            'TARGET_IS_MY_ACCEPTED_08'],
 (BATTLE_MESSAGE_TYPE.ENEMY_MY_AIM, False): ['TARGET_IS_MY_DENIED_01',
                                             'TARGET_IS_MY_DENIED_02',
                                             'TARGET_IS_MY_DENIED_03',
                                             'TARGET_IS_MY_DENIED_04',
                                             'TARGET_IS_MY_DENIED_05',
                                             'TARGET_IS_MY_DENIED_06',
                                             'TARGET_IS_MY_DENIED_07']}

def LocalizeBattleMessageReaction(battleMessageType, isPositive, senderName, callerName, targetName):
    strings = BATTLE_MESSAGE_LOCALE_MAP.get((battleMessageType, isPositive))
    if strings is None or len(strings) == 0:
        return ''
    else:
        stringId = choice(strings) if USE_MULTIPLE_STRINGS else strings[SINGLE_STRING_MAP.get((battleMessageType, isPositive), 1) - 1]
        message = localizeBattleMessageReaction(stringId)
        fmtMessage = message.format(sender_name=senderName, caller_name=callerName, target_name=targetName)
        return fmtMessage