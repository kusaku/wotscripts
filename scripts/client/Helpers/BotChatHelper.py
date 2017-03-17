# Embedded file name: scripts/client/Helpers/BotChatHelper.py
import random
from EntityHelpers import EntitySupportedClasses, AvatarFlags
from Helpers.i18n import localizeAirplane, localizeBotChat
from consts import MESSAGE_TYPE
_botChatMessageTypeMap = {MESSAGE_TYPE.BOT_CHAT_ALL: MESSAGE_TYPE.BATTLE_ALL,
 MESSAGE_TYPE.BOT_CHAT_TEAM: MESSAGE_TYPE.BATTLE_ALLY}

def isBotChatMessage(messageType):
    return messageType in _botChatMessageTypeMap


def convertMessageType(messageType):
    return _botChatMessageTypeMap[messageType]


def convertMessage(message, players, senderInfo, targetID):
    if not message or message[0] == '!':
        return message
    else:
        message = localizeBotChat(message)
        if not message:
            return ''
        lastPlayerName = ''
        botName = ''
        planeName = ''
        team = senderInfo['teamIndex']
        isAlive = lambda e: e['stats']['flags'] & AvatarFlags.DEAD == 0
        targetInfo = players.get(targetID, None)
        if targetInfo:
            localPlaneName = localizeAirplane(targetInfo['settings'].airplane.name)
            botName = targetInfo['playerName']
            planeName = localPlaneName
        allPlayers = []
        aliveAllyPlayers = []
        for id_, player in players.iteritems():
            if player['classID'] == EntitySupportedClasses.AvatarBot:
                continue
            allPlayers.append(player)
            if player['teamIndex'] == team and isAlive(player):
                aliveAllyPlayers.append(player)

        randomPlayerName = random.choice(allPlayers)['playerName']
        if len(aliveAllyPlayers) > 0:
            lastPlayerName = random.choice(aliveAllyPlayers)['playerName']
        result = message.format(bot_name=botName, plane_name=planeName, random_player_name=randomPlayerName, last_player_name=lastPlayerName)
        return result