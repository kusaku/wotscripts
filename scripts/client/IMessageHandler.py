# Embedded file name: scripts/client/IMessageHandler.py
from functools import partial
from operator import itemgetter
import datetime
import BigWorld
from HelperFunctions import select, wowpRound, filter2
from _awards_data import AwardsDB
import _consumables_data
from _skills_data import SkillDB, SpecializationSkillDB
from _specializations_data import SpecializationEnum
import _weapons
import db.DBLogic
import _airplanesConfigurations_db
from consts import MESSAGE_TYPE, CUSTOM_PRESET_NAME, GET_CLIENT_MOTD, UPGRADE_TYPE, COMPONENT_TYPE, MESSAGE_GROUP_TYPE
from Helpers.i18n import localizeMessages, getFormattedTime, localizeTutorial, localizeChat, localizeUpgrade, localizeAchievements
from Helpers.i18n import localizeMap, localizeBattleResults, localizeAirplane, localizeComponents
from Helpers.i18n import localizePresets, localizeLobby, localizeTimeInterval, localizeSkill
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_WARNING
from gui.Scaleform.BattleResult import getStrValueWithFactor
from gui.HtmlMessagerTypes import HtmlMessagerTypes
from consts import STATS_DAILY_KILL
from exchangeapi.Connectors import getObject
import consts
import time
from exchangeapi.EventUtils import generateEvent
import Settings
from Helpers.namesHelper import getBotName
from clientConsts import CREW_BODY_TYPE_LOCALIZE_PO_INDEX
from Helpers.cache import getFromCache
import BWPersonality
from config_consts import IS_CHINA
import _economics
SEC_IN_DAY = 86400

def defaultHandler(imsg):
    """
    Default message handler. Return imsg without any transforms
    :param imsg: IMessage
    """
    imsg['msgHeader'] = ''
    imsg['msgData'] = dict(msgBody=imsg['msgData'])
    return imsg


def switchSpaceHandler(imsg):
    """
    :param imsg: IMessage
    """
    if 'msgBody' not in imsg['msgData']:
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_HEADER_HANGAR_HOLIDAY')
        imsg['msgData'] = dict(msgBody=imsg['msgData'])
    return imsg


def motd(imsg):
    """
    Motd message handler
    :param imsg: IMessage
    """
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_HELLO')
    imsg['msgData'] = dict(msgBody=localizeMessages(imsg['msgData']) if imsg['msgData'] != GET_CLIENT_MOTD else localizeMessages('LOBBY_MSG_HELLO'), senderName=imsg['senderName'])
    return imsg


def reboot(imsg):
    """
    Reboot message handler
    :param imsg: IMessage
    """
    utc, message = (imsg['msgData'].split('#') + [None])[:2]
    rebootTime = getFormattedTime(utc)
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_REBOOT')
    imsg['msgData'] = dict(msgBody=message.decode('utf-8') + ' ' + rebootTime)
    return imsg


def goldReceived(imsg):
    """
    Gold received message handler
    :param imsg: IMessage
    """
    gold = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_DAILY_WIN')
    imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_MSG_DAILY_WIN'), gold=__localizeGoldPositive(gold))
    return imsg


def tutorialReward(imsg):
    """
    :param imsg: IMessage
    """
    lessonID, lessonCredits, lessonExp = imsg['msgData'].split(',')
    iexp = int(lessonExp)
    icredits = int(lessonCredits)
    localizedLessonExp = __localizeExpPositive(lessonExp)
    if iexp > 0 < icredits:
        action = HtmlMessagerTypes.MESSAGE_SUBSTITUTE_EQUIPMENT
    elif iexp > 0 >= icredits:
        action = HtmlMessagerTypes.MESSAGE_RESEARCH
    else:
        action = HtmlMessagerTypes.MESSAGE_BUY
        localizedLessonExp = None
    imsg['msgHeader'] = localizeTutorial('LESSON_PASSED')
    imsg['msgData'] = dict(msgBody='', action=action, credits=__localizeCreditsPositive(lessonCredits) if icredits != 0 else '', exp=localizedLessonExp)
    return imsg


def tutorialRewardGold(imsg):
    lessonID, lessonGold = imsg['msgData'].split(',')
    imsg['msgHeader'] = localizeTutorial('LESSON_PASSED')
    imsg['msgData'] = dict(msgBody='', gold=__localizeGoldPositive(lessonGold))
    return imsg


def __ban(banExpireTime, reason, isChatBan):
    reasonUtf8 = unicode(reason, encoding='utf-8')
    if isChatBan:
        txtDescription = localizeChat('CHAT_SYSTEM_MESSAGE_BAN_REASON').format(reason=reasonUtf8)
        txtHeader = localizeChat('CHAT_SYSTEM_MESSAGE_CHAT_BLOCKED')
        if banExpireTime > 0:
            txtTime = localizeChat('CHAT_SYSTEM_MESSAGE_BAN_TIMER_SHORT').format(bandate=getFormattedTime(banExpireTime, Settings.g_instance.scriptConfig.timeFormated['dmY']))
            return (txtHeader, dict(msgBody=txtDescription + '\n' + txtTime, action=HtmlMessagerTypes.MESSAGE_CHAT_LOBBY_DISABLED))
        else:
            return (txtHeader, dict(msgBody=txtDescription, action=HtmlMessagerTypes.MESSAGE_CHAT_LOBBY_DISABLED))
    else:
        txtDescription = localizeChat('CHAT_SYSTEM_MESSAGE_CHAT_USABILITY_RESTORED') + '\n' + getFormattedTime(banExpireTime, Settings.g_instance.scriptConfig.timeFormated['dmY'])
        return (localizeChat('CHAT_SYSTEM_MESSAGE_CHAT_UNLOCKED'), dict(msgBody=txtDescription, action=HtmlMessagerTypes.MESSAGE_CHAT_LOBBY_ENABLED))


def ban(imsg):
    imsg['msgHeader'], imsg['msgData'] = __ban(imsg['utcTime'], imsg['msgData'], True)
    return imsg


def unban(imsg):
    imsg['msgHeader'], imsg['msgData'] = __ban(imsg['utcTime'], imsg['msgData'], False)
    return imsg


def premBought(imsg):
    gold = imsg['msgData'].get('gold', 0)
    tickets = imsg['msgData'].get('tickets', 0)
    expiryTimeDelta = int(round(imsg['msgData']['expiryTimeDelta'] / SEC_IN_DAY))
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_PREMIUM')
    imsg['msgData'] = dict(msgBody=localizeLobby('PREMIUM_AVAILABLE_FOR_DAYS', number=expiryTimeDelta))
    if gold:
        imsg['msgData']['gold'] = __localizeGoldNegative(gold)
    if tickets:
        imsg['msgData']['tickets'] = __localizeTicketsNegative(tickets)
    return imsg


def premExtended(imsg):
    gold = imsg['msgData'].get('gold', 0)
    tickets = imsg['msgData'].get('tickets', 0)
    premiumExpiryTimeDelta = imsg['msgData']['expiryTimeDelta']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_PREMIUM')
    expiryTime = imsg['msgData']['expiryTime'] + BigWorld.player().deltaTimeClientServer
    if premiumExpiryTimeDelta > 0:
        imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_MSG_PREMIUM_EXTENDED').format(time=getFormattedTime(expiryTime, Settings.g_instance.scriptConfig.timeFormated['dBYAHMS'])))
    else:
        imsg['msgData'] = dict(msgBody=localizeMessages('COMPONENT_NAME_TEXT_PREMIUM_DEDUCTED') + localizeTimeInterval(abs(premiumExpiryTimeDelta)))
    if gold:
        imsg['msgData']['gold'] = __localizeGoldNegative(gold)
    if tickets:
        imsg['msgData']['tickets'] = __localizeTicketsNegative(tickets)
    return imsg


def premExpired(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_PREMIUM')
    imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_MSG_PREMIUM_EXPIRED'))
    return imsg


def __battle(msgData):
    arenaData = db.DBLogic.g_instance.getArenaData(msgData['arenaTypeID'])
    arenaName = localizeMap(arenaData.typeName)
    quests = msgData['fullStat']['quests']
    tickets = 0
    for questData in quests.itervalues():
        if questData['isExecuted']:
            for bonus in questData['bonus']:
                if bonus['type'] == 'tickets':
                    tickets += int(round(bonus['value']))

    utc = msgData['arenaCreateTime']
    arenaStartTime = getFormattedTime(utc, Settings.g_instance.scriptConfig.timeFormated['dBAHMS'])
    battleData = {'BATTLE': arenaName + ' (' + arenaStartTime + ')',
     'AIRCRAFT': __getAircraftName(msgData['planeType']),
     'CREDITS_RECEIVED': msgData['fullStat']['myData']['sumCreditPremium'] if msgData['fullStat']['myData']['isPremium'] else msgData['fullStat']['myData']['sumCreditBase'],
     'DESTROYED_AIRCRAFT': msgData['killed'],
     'DETECTED_TEAM_OBJECTS': msgData['spotted'],
     'DAMAGED_AIRCRAFT': msgData['damaged'],
     'DESTROYED_TEAM_OBJECTS': msgData['objectsDestroyed'],
     'DESTROYED_TURRENTS': msgData['turretsDestroyed'],
     'EXPERIENCE': msgData['fullStat']['myData']['sumXPPremium'] if msgData['fullStat']['myData']['isPremium'] else msgData['fullStat']['myData']['sumXPBase'],
     'FREE_EXPERIENCE': msgData['fullStat']['myData']['sumFreeXP'],
     'PENALTY_EXPERIENCE': msgData['xpPenalty'] if 'xpPenalty' in msgData else 0,
     'PENALTY_CREDITS': msgData['creditsPenalty'] if 'creditsPenalty' in msgData else 0,
     'COMPENSATION_CREDITS': msgData['creditsFromTK'] if 'creditsFromTK' in msgData else 0,
     'XP_FACTOR': msgData['xpFactor'] if 'xpFactor' in msgData else 0,
     'XP_FREE_FACTOR': msgData['xpFreeFactor'] if 'xpFreeFactor' in msgData else 0,
     'CR_COEFF': msgData['crFactor'] if 'crFactor' in msgData else 0}
    if msgData['winState'] == 0:
        action = HtmlMessagerTypes.MESSAGE_LOSE
        msgHeader = localizeMessages('LOBBY_HEADER_LOSE').format(aircraft=battleData['AIRCRAFT'])
    elif msgData['winState'] == 1:
        action = HtmlMessagerTypes.MESSAGE_WIN
        msgHeader = localizeMessages('LOBBY_HEADER_WIN').format(aircraft=battleData['AIRCRAFT'])
    else:
        action = HtmlMessagerTypes.MESSAGE_DRAW
        msgHeader = localizeMessages('LOBBY_HEADER_DRAW').format(aircraft=battleData['AIRCRAFT'])
    txtRewards = ', '.join((localizeAchievements(AwardsDB[id].ui.name) for id in msgData['achievements']))
    msgData = dict(msgBody=battleData['BATTLE'], action=action, txtDestroyedCount=battleData['DESTROYED_AIRCRAFT'], txtDestroyedLabel=localizeMessages('LOBBY_MSG_DESTROYED_AIRCRAFT'), txtDamagedCount=battleData['DAMAGED_AIRCRAFT'], txtDamagedLabel=localizeMessages('LOBBY_MSG_DAMAGED_AIRCRAFT'), txtDiscoveredCount=battleData['DETECTED_TEAM_OBJECTS'], txtDiscoveredLabel=localizeMessages('LOBBY_MSG_DISCOVERED_TEAM_OBJECTS'), txtObjDestroyedCount=battleData['DESTROYED_TEAM_OBJECTS'], txtObjDestroyedLabel=localizeMessages('LOBBY_MSG_DESTROYED_TEAM_OBJECTS'), txtTurrentsDestroyedCount=battleData['DESTROYED_TURRENTS'], txtTurrentsDestroyedLabel=localizeMessages('LOBBY_MSG_DESTROYED_TURRENTS'), txtExperience=getStrValueWithFactor(int(battleData['EXPERIENCE']), int(battleData['XP_FACTOR'])), txtCredits=getStrValueWithFactor(int(battleData['CREDITS_RECEIVED']), int(battleData['CR_COEFF'])), txtFreeExperience=getStrValueWithFactor(int(battleData['FREE_EXPERIENCE']), int(battleData['XP_FREE_FACTOR'])), txtTitleReward=localizeMessages('LOBBY_MSG_TITLE_REWARD'), txtTitleStatistics=localizeMessages('LOBBY_MSG_TITLE_STATS'), txtTickets=str(tickets) if tickets > 0 else '', arenaModType=msgData['arenaModType'], quests=msgData['fullStat']['quests'])
    if txtRewards:
        msgData['txtTitleRewads'] = localizeMessages('COMPONENT_NAME_LABEL_ACHIEVEMENTS_UNLOCKED')
        msgData['txtRewards'] = txtRewards
    penaltyExperience = battleData['PENALTY_EXPERIENCE']
    penaltyCredits = battleData['PENALTY_CREDITS']
    if penaltyExperience or penaltyCredits:
        msgData['txtTitlePenalty'] = localizeMessages('LOBBY_MSG_TITLE_PENALTY')
        msgData['txtPenaltyCredits'] = __localizeCreditsNegative(penaltyCredits)
        msgData['txtPenaltyExperience'] = __localizeExpNegative(penaltyExperience)
    compensationCredits = battleData['COMPENSATION_CREDITS']
    if compensationCredits:
        msgData['txtTitleCompensation'] = localizeBattleResults('HUD_BATTLE_RESULT_TITLE_COMPENSATION')
        msgData['txtCompensationCredits'] = __localizeCreditsPositive(compensationCredits)
    return (msgHeader, msgData)


def resbattle(imsg):
    stat = imsg['msgData']['fullStat']
    imsg['reportID'] = str(stat['reportID'])
    imsg['autoShow'] = stat['autoShow']
    msgheader, msgdata = __battle(imsg['msgData'])
    arenaData = db.DBLogic.g_instance.getArenaData(stat['myData']['arenaType'])
    stat['myData']['arenaName'] = localizeMap(arenaData.typeName)
    for team in stat['teamsData']:
        for p in team:
            p['playerName'] = getBotName(p['playerName'], p['planeID'])

    battleResultData = {'teams': stat['teamsData'],
     'healthsTO': stat['healthsTO'],
     'myData': stat['myData'],
     'myID': stat['myID'],
     'quests': stat['quests'],
     'warAction': stat.get('warAction', {}),
     'events': stat['events'],
     'wasPlayerPractices': stat.get('wasPlayerPractices', True)}
    battleResultData['myData'].update(imsg['msgData'])
    battleResultData['myData']['planeID'] = battleResultData['myData']['planeType']
    del battleResultData['myData']['planeType']
    del battleResultData['myData']['fullStat']
    battleResultData['myData']['loadTime'] = imsg['msgData']['arenaCreateTime']
    battleResultData['myData']['arenaCreateTime'] = getFormattedTime(battleResultData['myData']['arenaCreateTime'], Settings.g_instance.scriptConfig.timeFormated['dBAHMS'])
    for questData in battleResultData['quests'].itervalues():
        if 'setAwardBits' in questData['progress']:
            del questData['progress']['setAwardBits']
        if 'setAwardBits' in questData['progress_before']:
            del questData['progress_before']['setAwardBits']
        if 'inrowByHour' in questData['progress']:
            if any((v < questData['progress_before'].get(k, 0) for k, v in questData['progress'].iteritems() if k != 'inrowByHour')):
                for k in questData['progress_before'].iterkeys():
                    if k != 'inrowByHour':
                        questData['progress_before'][k] = 0

    aogasCoeff = battleResultData['myData']['aogasCoeff']
    if aogasCoeff != 1.0:
        isPremium = battleResultData['myData']['isPremium']
        lstFields = ['actionsCreditsCoef',
         'questsCreditsCoef',
         'actionsXpCoef',
         'questsXpCoef',
         'actionsFreeXpCoef',
         'questsFreeXpCoef',
         'xpCoeffFirstWin',
         'actionsCrewXpCoef',
         'questsCrewXpCoef',
         'crewPumpingXp']
        for k in ('baseCredits', 'baseXP', 'baseFreeXP'):
            battleResultData['myData'][k] = int(round(battleResultData['myData'][k] * aogasCoeff))

        for k in lstFields:
            if k in battleResultData['myData']:
                data = battleResultData['myData'][k]
                if isinstance(data, list):
                    for d in data:
                        for kk in ('exp', 'freeExp', 'credits'):
                            if kk in d:
                                d[kk] = int(round(d[kk] * aogasCoeff))

                else:
                    d = data
                    for kk in ('exp', 'freeExp', 'credits'):
                        if kk in d:
                            d[kk] = int(round(d[kk] * aogasCoeff))

        for v in battleResultData['quests'].itervalues():
            for bonus in v['bonus']:
                if bonus['type'] in ('credits', 'freeXP', 'planeXP', 'tankmenXP'):
                    bonus['value'] = int(round(bonus['value'] * aogasCoeff))

    from BattleReplay import BattleReplay, g_replay
    if g_replay is not None:
        g_replay.onBattleResultsReceived(battleResultData)
    from exchangeapi.AdapterUtils import getAdapter
    getAdapter('IBattleResult', ['battleResult']).add(None, None, battleResultData, reportID=stat['reportID'])
    generateEvent('add', 'add', 'IBattleResult', [[stat['reportID'], 'battleResult']], None, battleResultData, None)
    imsg['msgHeader'], imsg['msgData'] = msgheader, msgdata
    return imsg


def repair(imsg):
    txtCredits = -abs(imsg['msgData']['credits'])
    isFreeAction = imsg['msgData']['isFreeAction']
    if imsg['msgData']['credits'] != 0:
        isFreeAction = False
    imsg['msgData'] = dict(msgBody=localizeMessages('COMPONENT_NAME_LABEL_REPAIR'), itemName=__getAircraftName(imsg['msgData']['aircraftID']), credits=txtCredits, resultID=imsg['msgData']['resultID'], isFreeAction=isFreeAction)
    if isFreeAction or txtCredits == 0:
        imsg['msgData']['description'] = localizeMessages('LOBBY_MSG_AIRCRAFT_REPAIR_FREE_PVE')
    return imsg


def buy(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_MSG_AIRCRAFT_BOUGHT'), aircraftName=__getAircraftName(msgData['aircraftID']), isPremium=db.DBLogic.g_instance.isPlanePremium(msgData['aircraftID']), resultID=msgData['resultID'])
    credits, gold, tickets = msgData['price']
    if credits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(credits)
    elif gold:
        imsg['msgData']['gold'] = __localizeGoldNegative(gold)
    elif tickets:
        imsg['msgData']['tickets'] = __localizeTicketsNegative(tickets)
    return imsg


def sell(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_MSG_AIRCRAFT_SELL'), aircraftName=__getAircraftName(msgData['aircraftID']), isPremium=db.DBLogic.g_instance.isPlanePremium(msgData['aircraftID']), credits=__localizeCreditsPositive(msgData['price']), resultID=msgData['resultID'])
    return imsg


def research(imsg):
    msgData = imsg['msgData']
    allExp = msgData['planeExp'] + msgData['freeExp']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_INVESTIGATED')
    imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_MSG_AIRCRAFT_INVESTIGATED'), aircraftName=__getAircraftName(msgData['aircraftID']), credits=__localizeExpNegative(allExp), expPlane=__localizePlaneExpNegative(msgData['planeExp']), expFree=__localizeFreeExpNegative(msgData['freeExp']))
    return imsg


def goldSpent(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgType'] = MESSAGE_TYPE.BUY_AIRCRAFT
    imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_BUBBLE_GOLD_EXCHANGE_SUCCESFULL_CH') if IS_CHINA else localizeMessages('LOBBY_BUBBLE_GOLD_EXCHANGE_SUCCESFULL'), gold=__localizeGoldNegative(imsg['msgData']))
    return imsg


def ticketsReceived(imsg):
    imsg['msgHeader'] = localizeLobby('LOBBY_EVENT_HEADER_DAILY_REWARD')
    imsg['msgType'] = MESSAGE_TYPE.BUY_AIRCRAFT
    tickets = imsg['msgData']['tickets']
    imsg['msgData']['tickets'] = __localizeTicketsPositive(tickets)
    imsg['msgData']['msgBody'] = localizeLobby('LOBBY_EVENT_MESSAGE_DAILY_REWARD')
    return imsg


def buyQuestChips(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgType'] = MESSAGE_TYPE.BUY_AIRCRAFT
    questChips = imsg['msgData']['questChips']
    imsg['msgData']['questChips'] = '{0}'.format(abs(int(questChips)))
    imsg['msgData']['msgBody'] = localizeLobby('LOBBY_MESSAGE_SERTIFICATE_SUCCESFULL_PURCHASE')
    return imsg


def buyQuestAndSpendCurrency(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgType'] = MESSAGE_TYPE.BUY_AIRCRAFT
    questChips = imsg['msgData']['questChips']
    credits = imsg['msgData']['credits']
    tickets = imsg['msgData']['tickets']
    gold = imsg['msgData']['gold']
    buy = imsg['msgData']['buy']
    questName = imsg['msgData']['name']
    if questName.isupper():
        questName = localizeLobby(questName)
    groupID = imsg['msgData']['groupID']
    del imsg['msgData']['buy']
    del imsg['msgData']['name']
    del imsg['msgData']['groupID']
    imsg['msgData']['questChips'] = '-{0}'.format(abs(int(questChips))) if questChips != 0 else ''
    imsg['msgData']['credits'] = '-{0}'.format(abs(int(credits))) if credits != 0 else ''
    imsg['msgData']['tickets'] = '-{0}'.format(abs(int(tickets))) if tickets != 0 else ''
    imsg['msgData']['gold'] = '-{0}'.format(abs(int(gold))) if gold != 0 else ''
    body = localizeLobby('LOBBY_JA_TR_SPECIAL_QUEST_{0}'.format(groupID), color='FFFFFF') if groupID is not None else localizeLobby('LOBBY_QUESTS_MESSAGE_NAME_COMPLETED_PERFECTLY', name=questName)
    if not buy:
        DAYS_SECONDS = 86400
        dt = imsg['msgData']['deltaTime']
        deltaTime = '{0} {1} {2}'.format(str(int(dt / DAYS_SECONDS)), localizeLobby('COUNTER_DAYS'), str(datetime.timedelta(seconds=int(dt) % DAYS_SECONDS)))
        del imsg['msgData']['deltaTime']
        body = '{0}\n{1}{2}'.format(body, localizeLobby('LOBBY_QUESTS_CONTEXT_TILL_COMPLETION'), deltaTime)
    imsg['msgData']['msgBody'] = body
    for k in ('questChips', 'credits', 'tickets', 'gold'):
        if not imsg['msgData'][k]:
            del imsg['msgData'][k]

    return imsg


def warActionChangeFraction(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgType'] = MESSAGE_TYPE.BUY_AIRCRAFT
    credits = imsg['msgData']['credits']
    tickets = imsg['msgData']['tickets']
    gold = imsg['msgData']['gold']
    imsg['msgData']['credits'] = '-{0}'.format(abs(int(credits))) if credits != 0 else ''
    imsg['msgData']['tickets'] = '-{0}'.format(abs(int(tickets))) if tickets != 0 else ''
    imsg['msgData']['gold'] = '-{0}'.format(abs(int(gold))) if gold != 0 else ''
    imsg['msgData']['msgBody'] = localizeLobby('LOBBY_JA_TR_SWITCH_FACTION_2')
    for k in ('credits', 'tickets', 'gold'):
        if not imsg['msgData'][k]:
            del imsg['msgData'][k]

    return imsg


def warCashPayTicket(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgType'] = MESSAGE_TYPE.BUY_AIRCRAFT
    tickets = imsg['msgData']['tickets']
    imsg['msgData']['tickets'] = '-{0}'.format(abs(int(tickets)))
    imsg['msgData']['msgBody'] = localizeLobby('LOBBY_JA_TR_TROPHY_RECEIVED')
    return imsg


def creditsReceived(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_MSG_CREDITS_RECEIVED')
    imsg['msgData'] = dict(msgBody='', action=HtmlMessagerTypes.MESSAGE_BUY, credits=__localizeCreditsPositive(imsg['msgData']))
    return imsg


def exchangeExp(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgType'] = MESSAGE_TYPE.BUY_AIRCRAFT
    imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_BUBBLE_FREE_XP_CONVERTED').format(number=imsg['msgData']['exp']), gold=__localizeGoldNegative(imsg['msgData']['gold']))
    return imsg


def installPreset(imsg):
    msgData = imsg['msgData']
    aircraftID = _airplanesConfigurations_db.getAirplaneConfiguration(msgData['globalID']).planeID
    aircraftName = __getAircraftName(aircraftID)
    presetName = db.DBLogic.g_instance.getPresetNameByGlobalID(msgData['globalID'])
    resources = msgData['resources']
    module_name = localizeComponents('PRESET_NAME_%s' % presetName) if presetName == CUSTOM_PRESET_NAME else localizePresets('PRESET_NAME_%s' % presetName)
    if resources['credits'] > 0:
        creditsMessage = __localizeCreditsNegative(resources['credits'])
    else:
        creditsMessage = ''
    if resources['exp'] > 0:
        expMessage = __localizeExpNegative(resources['exp'])
    else:
        expMessage = ''
    if not creditsMessage and not expMessage:
        imsg['msgHeader'] = aircraftName
        bodyMessage = localizeLobby('MODULES_CHARACTERISTICS_INSTALLED') + ' ' + module_name
    else:
        imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_SET_MODULES').format(plane_name=aircraftName)
        bodyMessage = localizeMessages('LOBBY_MSG_SET_CONFIGURATION').format(module_name=module_name)
    imsg['msgData'] = dict(msgBody=bodyMessage, action=HtmlMessagerTypes.MESSAGE_SUBSTITUTE_EQUIPMENT if resources['exp'] > 0 else HtmlMessagerTypes.MESSAGE_BUY, credits=creditsMessage, exp=expMessage)
    return imsg


def __getNameWithClan(name, clanAbbrev):
    return clanAbbrev and '%s[%s]' % (name, clanAbbrev) or name


def __playerName(name):
    return '<font color="#{playerColor}">%s</font>' % name


def squadInviteAccepted(imsg):
    body = '%s %s\n%s' % (__playerName(__getNameWithClan(imsg['msgData']['name'], imsg['msgData']['clanAbbrev'])), localizeMessages('COMPONENT_NAME_PLAYER_JOINED_WING'), getFormattedTime(imsg['msgData']['time']))
    imsg['msgHeader'] = localizeLobby('WING_HEADER_WING')
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def squadInviteRejected(imsg):
    body = '%s\n%s' % (localizeLobby('WING_PLAYER_DECLINED_INVITATION', name=__playerName(__getNameWithClan(imsg['msgData']['name'], imsg['msgData']['clanAbbrev']))), getFormattedTime(imsg['msgData']['time']))
    imsg['msgHeader'] = localizeLobby('WING_HEADER_WING')
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def squadMemberLeaving(imsg):
    body = '%s %s\n%s' % (__playerName(__getNameWithClan(imsg['msgData']['name'], imsg['msgData']['clanAbbrev'])), localizeMessages('COMPONENT_NAME_PLAYER_LEFT_WING'), getFormattedTime(imsg['msgData']['time']))
    imsg['msgHeader'] = localizeLobby('WING_HEADER_WING')
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def squadInvite(imsg):
    body = '%s\n%s' % (localizeMessages('SYSTEM_MESSAGE_WING_PLAYER_INVITES_YOU_TO_WING').format(name=__playerName(__getNameWithClan(imsg['msgData']['name'], imsg['msgData']['clanAbbrev']))), getFormattedTime(imsg['msgData']['time']))
    imsg['msgHeader'] = localizeLobby('WING_HEADER_WING')
    imsg['msgData'] = dict(msgBody=body, memberID=str(imsg['msgData']['memberID']), peripheryID=str(imsg['msgData']['peripheryID']))
    return imsg


def squadLeaving(imsg):
    body = localizeMessages('SYSTEM_MESSAGE_WING_PLAYER_LEAVE')
    imsg['msgHeader'] = localizeLobby('WING_HEADER_WING')
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def squadExcluding(imsg):
    body = localizeMessages('SYSTEM_MESSAGE_WING_PLAYER_EXCLUDED')
    imsg['msgHeader'] = localizeLobby('WING_HEADER_WING')
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def squadDestroying(imsg):
    body = localizeMessages('SYSTEM_MESSAGE_WING_DESTROYED')
    imsg['msgHeader'] = localizeLobby('WING_HEADER_WING')
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def squadErrorMemberOffline(imsg):
    body = '%s ' % (__playerName(__getNameWithClan(imsg['msgData']['name'], imsg['msgData']['clanAbbrev'])),)
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def squadErrorMemberBattle(imsg):
    body = '%s ' % (__playerName(__getNameWithClan(imsg['msgData']['name'], imsg['msgData']['clanAbbrev'])),)
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def squadErrorMemberNotInSquadFinder(imsg):
    body = '%s ' % (__playerName(__getNameWithClan(imsg['msgData']['name'], imsg['msgData']['clanAbbrev'])),)
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def researchUpgrade(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    msgBodyTag = 'MESSAGE_MODULE_EXPLORED_SUCCESSFULLY' if len(msgData['upgrades']) == 1 else 'MESSAGE_MODULES_EXPLORED_SUCCESSFULLY'
    imsg['msgData'] = dict(msgBody=localizeMessages(msgBodyTag).format(name=', '.join((localizeUpgrade(db.DBLogic.g_instance.upgrades[u]) for u in msgData['upgrades']))), credits=__localizeExpNegative(msgData['exp']), expPlane=__localizePlaneExpNegative(msgData['exp_plane']), expFree=__localizeFreeExpNegative(msgData['exp_free']))
    return imsg


def buyUpgrade(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('MESSAGE_MODULE_PURCHASED_SUCCESSFULLY').format(name=', '.join((localizeUpgrade(db.DBLogic.g_instance.upgrades[u], True) for u in msgData['upgrades']))))
    creds, gold = msgData['price']
    if creds:
        imsg['msgData']['credits'] = __localizeCreditsNegative(creds)
    elif gold:
        imsg['msgData']['gold'] = __localizeGoldNegative(gold)
    return imsg


def sellUpgrade(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('COMPONENT_NAME_LABEL_SELL') + ' ' + ', '.join((localizeUpgrade(db.DBLogic.g_instance.upgrades[u], True) for u in msgData['upgrades'])))
    if len(msgData['price']) < 3:
        creds, gold = msgData['price']
        tickets = 0
    else:
        creds, gold, tickets = msgData['price']
    if creds:
        imsg['msgData']['credits'] = __localizeCreditsPositive(creds)
    elif gold:
        imsg['msgData']['gold'] = __localizeGoldPositive(gold)
    return imsg


def _localizeAmmo(ammoName, ammoType):
    ammo = db.DBLogic.g_instance.getComponentByName(ammoType, ammoName)
    ret = localizeComponents('WEAPON_NAME_' + (ammo.ui_name if ammoType == COMPONENT_TYPE.AMMOBELT else ammo.name))
    if ammoType == COMPONENT_TYPE.AMMOBELT:
        guns = filter(lambda x: ammo.id in x.compatibleBeltIDs, db.DBLogic.g_instance.getComponents(consts.COMPONENT_TYPE.GUNS))
        if guns:
            ret = '{0} {1}'.format(ret, wowpRound(guns[0].caliber, 2))
    return ret


def buyAmmo(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('COMPONENT_NAME_LABEL_PURCHASE') + ' ' + ', '.join((_localizeAmmo(u, t) for u, t in msgData['upgrades'])))
    creds, gold = msgData['price']
    if creds:
        imsg['msgData']['credits'] = __localizeCreditsNegative(creds)
    elif gold:
        imsg['msgData']['gold'] = __localizeGoldNegative(gold)
    return imsg


def sellAmmo(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('COMPONENT_NAME_LABEL_SELL') + ' ' + ', '.join((_localizeAmmo(u, t) for u, t in msgData['upgrades'])))
    creds = msgData['price'][0]
    if creds:
        imsg['msgData']['credits'] = __localizeCreditsPositive(creds)
    return imsg


def sellConsumables(imsg):
    spendCredits = imsg['msgData']['credits']
    consumable = db.DBLogic.g_instance.getConsumableByID(imsg['msgData']['consumableID'])
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('COMPONENT_NAME_LABEL_SELL') + ' ' + localizeLobby(consumable.name))
    if spendCredits:
        imsg['msgData']['credits'] = __localizeCreditsPositive(spendCredits)
    return imsg


def sellEquipment(imsg):
    equipmentIDs = imsg['msgData']['equipmentIDs']
    spendCredits = imsg['msgData']['credits']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('COMPONENT_NAME_LABEL_SELL') + ' ' + ', '.join((localizeLobby(db.DBLogic.g_instance.getEquipmentByID(eq).name) for eq in equipmentIDs)))
    if spendCredits:
        imsg['msgData']['credits'] = __localizeCreditsPositive(spendCredits)
    return imsg


def __updateUpgrade(imsg, isInstall):
    msgData = imsg['msgData']
    planeID = imsg['msgData']['planeID']
    imsg['msgHeader'] = localizeAirplane(db.DBLogic.g_instance.getAircraftName(planeID))
    if isInstall:
        msgBody = localizeMessages('MESSAGE_MODULE_INSTALLED_SUCCESSFULLY').format(module_name=', '.join((localizeUpgrade(db.DBLogic.g_instance.upgrades[u]) for u in msgData['upgrades'])))
    else:
        msgBody = localizeMessages('MESSAGE_MODULE_UNINSTALLED_SUCCESSFULLY').format(module=', '.join((localizeUpgrade(db.DBLogic.g_instance.upgrades[u]) for u in msgData['upgrades'])))
    imsg['msgData'] = dict(msgBody=msgBody)
    return imsg


def uninstallUpgrade(imsg):
    return __updateUpgrade(imsg, False)


def installUpgrade(imsg):
    return __updateUpgrade(imsg, True)


def refillAircraftShells(imsg):
    msgData = imsg['msgData']
    credits, gold = msgData['price']
    imsg['msgHeader'] = localizeAirplane(db.DBLogic.g_instance.getAircraftName(imsg['msgData']['planeID']))
    if gold:
        imsg['msgData']['gold'] = __localizeGoldNegative(gold)
    if credits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(credits)
    if msgData['shellType'] == UPGRADE_TYPE.BOMB:
        if credits < 0 or gold < 0:
            imsg['msgData']['msgBody'] = localizeMessages('LOBBY_HEADER_BOMBS_REFILL_FAILED')
        else:
            imsg['msgData']['msgBody'] = localizeMessages('LOBBY_HEADER_BOMBS_REFILL')
    elif credits < 0 or gold < 0:
        imsg['msgData']['msgBody'] = localizeMessages('LOBBY_HEADER_ROCKETS_REFILL_FAILED')
    else:
        imsg['msgData']['msgBody'] = localizeMessages('LOBBY_HEADER_ROCKETS_REFILL')
    return imsg


def refillAircraftBelts(imsg):
    msgData = imsg['msgData']
    credits, gold = msgData['price']
    imsg['msgHeader'] = localizeAirplane(db.DBLogic.g_instance.getAircraftName(imsg['msgData']['planeID']))
    LOG_DEBUG('@ refillAircraftBelts ', credits, gold)
    if credits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(credits)
    if gold:
        imsg['msgData']['gold'] = __localizeGoldNegative(gold)
    if imsg['msgData']['isFreeAction']:
        imsg['msgData']['msgBody'] = localizeMessages('LOBBY_MSG_AMMO_REFILL_FREE_PVE')
    elif credits < 0 or gold < 0:
        imsg['msgData']['msgBody'] = localizeMessages('LOBBY_MSG_AMMO_REFILL_FAILED')
    else:
        imsg['msgData']['msgBody'] = localizeMessages('LOBBY_MSG_AMMO_REFILL')
    return imsg


def refillAircraftConsumables(imsg):
    msgData = imsg['msgData']
    credits, gold, tickets = msgData['price']
    imsg['msgHeader'] = localizeAirplane(db.DBLogic.g_instance.getAircraftName(imsg['msgData']['planeID']))
    if imsg['msgData']['isFreeAction']:
        imsg['msgData']['msgBody'] = localizeMessages('LOBBY_MSG_CONSUMABLES_REFILL_FREE_PVE')
    else:
        if credits:
            imsg['msgData']['credits'] = __localizeCreditsNegative(credits)
        if gold:
            imsg['msgData']['gold'] = __localizeGoldNegative(gold)
        if tickets:
            imsg['msgData']['tickets'] = __localizeTicketsNegative(tickets)
        consumable = db.DBLogic.g_instance.getConsumableByID(msgData['consumableID'])
        if consumable:
            consumableLoc = consumable.name
        else:
            consumableLoc = 'INVALID_CONSUMABLE_ID_' + consumable.name
        if credits < 0 or gold < 0:
            imsg['msgData']['msgBody'] = localizeMessages('LOBBY_HEADER_CONSUMABLES_REFILL_FAILED').format(name=localizeLobby(consumableLoc))
        else:
            imsg['msgData']['msgBody'] = localizeMessages('LOBBY_HEADER_CONSUMABLES_REFILL').format(name=localizeLobby(consumableLoc))
    return imsg


def trainingSkill(imsg):
    creds, gold = imsg['msgData']['price']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData']['msgBody'] = localizeMessages('MESSAGES_FAST_TRAINING_PILOT')
    if creds:
        imsg['msgData']['credits'] = -abs(creds)
    if gold:
        imsg['msgData']['gold'] = -abs(gold)
    return imsg


def reTrainingSkill(imsg):
    creds, gold = imsg['msgData']['price']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData']['msgBody'] = localizeMessages('MESSAGES_RETRAINING_PILOT')
    if creds:
        imsg['msgData']['credits'] = -abs(creds)
    if gold:
        imsg['msgData']['gold'] = -abs(gold)
    return imsg


def dropSkills(imsg):
    creds, gold = imsg['msgData']['price']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData']['msgBody'] = localizeMessages('MESSAGES_RESET_SKILLS_PILOT')
    if creds:
        imsg['msgData']['credits'] = -abs(creds)
    if gold:
        imsg['msgData']['gold'] = -abs(gold)
    return imsg


def gotFirstSP(imsg):
    planeID = imsg['msgData']['planeID']
    localizedPlane = localizeAirplane(db.DBLogic.g_instance.getAircraftName(planeID))
    localizedSpecialization = localizeLobby('LOBBY_CREW_HEADER_' + SpecializationSkillDB[imsg['msgData']['specializationID']].localizeTag)
    notification = {'crew_member': localizedSpecialization,
     'plane_name': localizedPlane}
    imsg['msgHeader'] = ''
    imsg['notification'] = notification
    imsg['msgData']['msgBody'] = localizeBattleResults('BATTLE_RESULT_AVAILABLE_FIRST_SKILL_POINT')
    return imsg


def gotNewSP(imsg):
    planeID = imsg['msgData']['planeID']
    localizedPlane = localizeAirplane(db.DBLogic.g_instance.getAircraftName(planeID))
    localizedSpecialization = localizeLobby('LOBBY_CREW_HEADER_' + SpecializationSkillDB[imsg['msgData']['specializationID']].localizeTag)
    notification = {'crew_member': localizedSpecialization,
     'plane_name': localizedPlane}
    imsg['msgHeader'] = ''
    imsg['notification'] = notification
    imsg['msgData']['msgBody'] = localizeBattleResults('BATTLE_RESULT_AVAILABLE_NEW_SKILL_POINT')
    return imsg


def changeXpToSp(imsg):
    localizedSpecialization = localizeLobby('LOBBY_CREW_HEADER_' + SpecializationSkillDB[imsg['msgData']['specializationID']].localizeTag)
    notification = {'crew_member': localizedSpecialization}
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['notification'] = notification
    imsg['msgData']['msgBody'] = localizeLobby('LOBBY_CREW_HEADER_TRAINING')
    imsg['msgData']['exp'] = imsg['msgData']['expFree'] * _economics.Economics.freeXPToCrewXPRate
    return imsg


def crewDemobilize(imsg):
    from Helpers.namesHelper import CONTRY_PO_FILE_WRAPPER, localizePilot, FIRST_NAME_MSG_ID, LAST_NAME_MSG_ID, CONTRY_MSG_ID_WRAPPER
    nation = imsg['msgData']['nation']
    countryDict = {nationID:cc for cc, nationID in db.DBLogic.g_instance.getNationList().iteritems()}
    contry = countryDict[nation]
    bodyTypePO = CREW_BODY_TYPE_LOCALIZE_PO_INDEX[imsg['msgData']['bodyType']]
    specialization = imsg['msgData']['specializationID']
    if specialization == SpecializationEnum.PILOT:
        msgString = 'SYSTEM_MESSAGE_PILOT_DISMISS'
    elif specialization == SpecializationEnum.GUNNER:
        msgString = 'SYSTEM_MESSAGE_GUNNER_DISMISS'
    else:
        msgString = 'SYSTEM_MESSAGE_UNKNOWN_DISMISS'
    notification = {'firstName': localizePilot(CONTRY_PO_FILE_WRAPPER[contry], FIRST_NAME_MSG_ID % (CONTRY_MSG_ID_WRAPPER[contry], bodyTypePO, imsg['msgData']['firstName'] or 1)),
     'lastName': localizePilot(CONTRY_PO_FILE_WRAPPER[contry], LAST_NAME_MSG_ID % (CONTRY_MSG_ID_WRAPPER[contry], bodyTypePO, imsg['msgData']['lastName'] or 1))}
    imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_DISMISS_CREW')
    imsg['msgData']['msgBody'] = localizeMessages(msgString)
    imsg['notification'] = notification
    return imsg


def crewExpPumping(imsg):
    isPumping = imsg['msgData']['isPumping']
    if isPumping:
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_FAST_TRAINING_ON')
        imsg['msgData']['msgBody'] = localizeMessages('SYSTEM_MESSAGE_NOW_CREW_TRAINING_FASTER')
    else:
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_FAST_TRAINING_OFF')
        imsg['msgData']['msgBody'] = localizeMessages('SYSTEM_MESSAGE_NOW_EXP_COLLECT_ON_PLANE')
    return imsg


def buyEquipment(imsg):
    equipmentIDs = imsg['msgData']['equipmentIDs']
    spendCredits = imsg['msgData']['credits']
    spendTickets = imsg['msgData'].get('tickets', 0)
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('SYSTEM_MESSAGE_MODULE_PURCHASED_MSGTEXT').format(module_name=', '.join((localizeLobby(db.DBLogic.g_instance.getEquipmentByID(eq).name) for eq in equipmentIDs))))
    if spendCredits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(spendCredits)
    if spendTickets:
        imsg['msgData']['tickets'] = __localizeTicketsNegative(spendTickets)
    return imsg


def installEquipment(imsg):
    equipmentIDs = imsg['msgData']['equipmentIDs']
    planeID = imsg['msgData']['planeID']
    imsg['msgHeader'] = localizeAirplane(db.DBLogic.g_instance.getAircraftName(planeID))
    imsg['msgData'] = dict(msgBody=localizeMessages('SYSTEM_MESSAGE_MODULE_INSTALLED_MSGTEXT').format(module_name=', '.join((localizeLobby(db.DBLogic.g_instance.getEquipmentByID(eq).name) for eq in equipmentIDs))))
    return imsg


def detachEquipment(imsg):
    equipmentIDs = imsg['msgData']['equipmentIDs']
    spendGold = imsg['msgData']['gold']
    planeID = imsg['msgData']['planeID']
    imsg['msgHeader'] = localizeAirplane(db.DBLogic.g_instance.getAircraftName(planeID))
    imsg['msgData'] = dict(msgBody=localizeMessages('SYSTEM_MESSAGE_MODULE_UNINSTALLED_MSGTEXT').format(module_name=', '.join((localizeLobby(db.DBLogic.g_instance.getEquipmentByID(eq).name) for eq in equipmentIDs))))
    if spendGold:
        imsg['msgData']['gold'] = __localizeGoldNegative(spendGold)
    return imsg


def destroyedEquipment(imsg):
    equipmentID = imsg['msgData']['equipmentID']
    planeID = imsg['msgData']['planeID']
    imsg['msgHeader'] = localizeAirplane(db.DBLogic.g_instance.getAircraftName(planeID))
    imsg['msgData'] = dict(msgBody=localizeMessages('SYSTEM_MESSAGE_MODULE_DESTROYED_MSGTEXT').format(module_name=localizeLobby(db.DBLogic.g_instance.getEquipmentByID(equipmentID).name)))
    return imsg


def buyConsumables(imsg):
    spendCredits = imsg['msgData']['credits']
    spendGold = imsg['msgData']['gold']
    spendTickets = imsg['msgData']['tickets']
    consumable = db.DBLogic.g_instance.getConsumableByID(imsg['msgData']['consumableID'])
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_SHOP_HEADER_PURCHASE') + ' ' + localizeLobby(consumable.name))
    if spendCredits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(spendCredits)
    if spendGold:
        imsg['msgData']['gold'] = __localizeGoldNegative(spendGold)
    if spendTickets:
        imsg['msgData']['tickets'] = __localizeTicketsNegative(spendTickets)
    return imsg


def screenshotPopup(imsg):
    imsg['msgHeader'] = ''
    if 'msgBody' not in imsg['msgData']:
        imsg['msgData'] = dict(msgBody=imsg['msgData'])
    return imsg


def crewMemberGetNewRank(imsg):
    membersList, notificationsList = imsg['msgData']['crewmembers'], []
    membersList.sort(key=lambda x: x['specializationID'])
    imsg['msgData'] = {'msgHeader': '',
     'msgBody': '',
     'notifications': notificationsList,
     'memberID': membersList[0]['memberID'],
     'crewMembers': [ memberData['memberID'] for memberData in membersList ]}
    imsg['msgData']['msgBody'] = repr(imsg['msgData'])
    return imsg


def voipServiceDown(imsg):
    body = localizeMessages('VOIP_SERVICE_DOWN')
    imsg['msgHeader'] = localizeMessages('VOIP_MESSAGE_HEADER')
    imsg['msgData'] = dict(msgBody=body)
    return imsg


def giftPlaneI15dm2(imsg):
    GIFT_PLANE = 'I-15bis-dm2'
    imsg['msgHeader'] = localizeLobby('SYSTEM_MESSAGE_I-15BIS-DM2_RECEIVED')
    imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_I-15BIS-DM2_GIFT_MESSAGE_TEXT', name=localizeAirplane(GIFT_PLANE)))
    return imsg


def giftPlane(imsg):
    imsg['msgHeader'] = localizeLobby('SYSTEM_MESSAGE_I-15BIS-DM2_RECEIVED')
    planeName = db.DBLogic.g_instance.getAircraftName(imsg['msgData']['planeID'])
    imsg['msgData'] = dict(msgBody='{0} {1}'.format(localizeLobby('LOBBY_CREW_HEADER_PLANE'), localizeAirplane(planeName)), planeID=imsg['msgData']['planeID'])
    return imsg


def giftPlaneSleipnir(imsg):
    imsg['msgHeader'] = localizeLobby('LOBBY_APRIL_2014_GIFT_MESSAGE_HEADER')
    planeName = db.DBLogic.g_instance.getAircraftName(imsg['msgData']['planeID'])
    imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_APRIL_2014_GIFT_MESSAGE_TEXT'))
    return imsg


def deductPlane(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_DEDUCT')
    if int(msgData['aircraftID']) == 1304:
        imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_APRIL_2014_REMOVAL_MESSAGE_TEXT').format(aircraft=__getAircraftName(msgData['aircraftID'])), credits=__localizeCreditsPositive(msgData['price']), resultID=msgData['resultID'])
    else:
        imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_MSG_AIRCRAFT_DEDUCT').format(aircraft=__getAircraftName(msgData['aircraftID'])), credits=__localizeCreditsPositive(msgData['price']), resultID=msgData['resultID'])
    return imsg


def shopPurchase(imsg):
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    idTypeList = imsg['msgData']['idTypeList']
    spendCredits, spendGold = imsg['msgData']['price']
    try:
        ob = getObject(idTypeList)
        localizedName = localizeAirplane(ob.name)
        imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_SHOP_HEADER_PURCHASE') + ' ' + localizedName)
    except AttributeError as e:
        LOG_ERROR('object {0} has no attribute {1}'.format(ob, 'name'))
        LOG_ERROR(e)

    if spendCredits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(spendCredits)
    if spendGold:
        imsg['msgData']['gold'] = __localizeGoldNegative(spendGold)
    return imsg


def buySlot(imsg):
    spendCredits, spendGold, spendTickets = imsg['msgData']['price']
    slotCount = imsg['msgData'].get('count', 1)
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    if slotCount == 1:
        imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_SHOP_HEADER_SLOT_IN_HANGAR'))
    else:
        imsg['msgData'] = dict(msgBody=localizeLobby('SYSTEM_MESSAGE_PACK_SLOT_SUCCESSFUL_PURCHASE').format(number=slotCount))
    if spendCredits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(spendCredits)
    if spendGold:
        imsg['msgData']['gold'] = __localizeGoldNegative(spendGold)
    if spendTickets:
        imsg['msgData']['tickets'] = __localizeTicketsNegative(spendTickets)
    imsg['msgData']['count'] = slotCount
    return imsg


def buyBarrackSlot(imsg):
    spendCredits, spendGold = imsg['msgData']['price']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_CREW_HEADER_ENLARGE_BARRACKS'))
    if spendCredits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(spendCredits)
    if spendGold:
        imsg['msgData']['gold'] = __localizeGoldNegative(spendGold)
    return imsg


def tokenExchanged(imsg):
    gold = imsg['msgData']['gold']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    imsg['msgData'] = dict(msgBody=localizeMessages('LOBBY_BUBBLE_TOKENS_EXCHANGE_SUCCESFULL'))
    if gold > 0:
        imsg['msgData']['gold'] = __localizeTokensNegative(gold)
    return imsg


def buyCamouflage(imsg):
    spendCredits, spendGold = imsg['msgData']['price']
    imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_CAMO_HEADER_CAMO_DECOR'))
    if spendCredits:
        imsg['msgData']['credits'] = -abs(spendCredits)
    if spendGold:
        imsg['msgData']['gold'] = -abs(spendGold)
    return imsg


def walletConnected(imsg):
    imsg['msgData'] = dict(msgBody=localizeMessages('SYSTEM_MESSAGE_GOLD_ACCESS_GRANTED'))
    return imsg


def refillFailed(imsg):
    imsg['msgHeader'] = localizeAirplane(db.DBLogic.g_instance.getAircraftName(imsg['msgData']['planeID']))
    failedOn = imsg['msgData']['failedOn']
    if len(failedOn) == 1:
        item = failedOn[0]
        errorLocalizationTags = {'ammobelt': 'LOBBY_HEADER_AMMO_REFILL_FAILED',
         'bomb': 'LOBBY_HEADER_BOMBS_REFILL_FAILED',
         'rocket': 'LOBBY_HEADER_ROCKETS_REFILL_FAILED',
         'consumable': 'LOBBY_HEADER_CONSUMABLES_REFILL_FAILED'}
        messageLocalizationTags = {'ammobelt': 'LOBBY_MSG_AMMO_REFILL_FAILED',
         'bomb': 'LOBBY_MSG_BOMBS_REFILL_FAILED',
         'rocket': 'LOBBY_MSG_ROCKETS_REFILL_FAILED',
         'consumable': 'LOBBY_MSG_CONSUMABLES_REFILL_FAILED'}
        msgErrorLocalizeTag = errorLocalizationTags.get(item, 'LOBBY_HEADER_AMMO_REFILL_FAILED')
        msgMessageLocalizeTag = messageLocalizationTags.get(item, 'LOBBY_MSG_AMMO_REFILL_FAILED')
    else:
        msgErrorLocalizeTag = 'LOBBY_HEADER_AMMO_REFILL_FAILED'
        msgMessageLocalizeTag = 'LOBBY_MSG_AMMO_REFILL_FAILED'
    imsg['msgData']['msgBody'] = '{0} {1}'.format(localizeMessages(msgErrorLocalizeTag), localizeMessages(msgMessageLocalizeTag))
    return imsg


def premiumBeltsGiven(imsg):
    planeID = imsg['msgData']['planeID']
    imsg['msgHeader'] = localizeLobby('LOBBY_CREW_MESSAGE_CONGRATULATIONS')
    imsg['msgData'] = dict(msgBody=localizeLobby('LOBBY_CREW_MESSAGE_DOUBLE_AMMO_BELTS_PLANE', plane_name=__getAircraftName(planeID)), msgTitle=localizeLobby('LOBBY_CREW_MESSAGE_GIFT'), planeID=planeID)
    return imsg


def questGetBonus(imsg):
    questID, questName, count, bonus, isConsist, questChips, isDelayedAward = imsg['msgData']
    if isinstance(questName, dict):
        locale = localizeLobby('LOCALIZATION_LANGUAGE').encode('ascii').lower()
        questName = questName.get(locale, questName.values()[0])
    if questName.isupper():
        questName = localizeLobby(questName)
    if isDelayedAward:
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_HEADER_PRIZES')
    elif isConsist:
        imsg['msgHeader'] = localizeLobby('LOBBY_QUESTS_MESSAGE_NAME_COMPLETED_PERFECTLY', name=questName)
    elif count > 1:
        imsg['msgHeader'] = '{0} x{1}'.format(localizeMessages('SYSTEM_MESSAGE_QUESTS_QUEST_COMPLETED').format(quest=questName), count)
    else:
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_QUESTS_QUEST_COMPLETED').format(quest=questName)
    imsg['msgData'] = dict(msgBody='', questID=questID, bonus=bonus, isDelayedAward=isDelayedAward)
    if questChips != 0:
        normalized = abs(int(questChips))
        imsg['msgData']['questChips'] = '{0}'.format(-normalized if normalized > 0 else normalized)
    return imsg


def questNewMessage(imsg):
    quests_count = imsg['msgData']
    imsg['msgHeader'] = '{0} {1}'.format(localizeMessages('SYSTEM_MESSAGE_QUESTS_NEW_QUESTS_AVAILABLE'), quests_count)
    imsg['msgData'] = dict(msgBody='', count=int(quests_count))
    return imsg


def serverDowntimeCompensation(imsg):
    prem, camouflages = imsg['msgData']['prem'], imsg['msgData']['camouflages']
    imsg['msgHeader'] = localizeLobby('COMPENSATION_HEADER')
    if prem and camouflages:
        imsg['msgData']['msgBody'] = localizeLobby('LOBBY_MSG_COMPENSATION_PREMIUM_CAMOUFLAGES')
    elif prem and not camouflages:
        imsg['msgData']['msgBody'] = localizeLobby('LOBBY_MSG_COMPENSATION_PREMIUM')
    elif not prem and camouflages:
        imsg['msgData']['msgBody'] = localizeLobby('LOBBY_MSG_COMPENSATION_CAMOUFLAGES')
    return imsg


def aircraftRentExtended(imsg):
    planeName = __getAircraftName(imsg['msgData']['planeID'])
    imsg['msgHeader'] = localizeMessages('CHINA_MESSAGE_RENT_AIRCRAFT_TOP_PART')
    imsg['msgData'] = {'msgBody': localizeMessages('CHINA_MESSAGE_RENT_AIRCRAFT_FOR_DAYS').format(days=imsg['msgData']['days']),
     'name': planeName}
    return imsg


def rentComplencation(imsg):
    planeName = __getAircraftName(imsg['msgData']['planeID'])
    imsg['msgHeader'] = localizeLobby('CHINA_LOBBY_RENT_CONTEXT_RENT_REFUND')
    imsg['msgData'] = {'msgBody': localizeMessages('CHINA_MESSAGE_QUEST_REFUND_FOR_RENT_PERIOD').format(aircraft_name=planeName, days=imsg['msgData']['days']),
     'name': planeName,
     'days': imsg['msgData']['days'],
     'credit': imsg['msgData']['credit'],
     'gold': imsg['msgData']['gold']}
    return imsg


def aircraftPurchasedRentRefund(imsg):
    planeName = __getAircraftName(imsg['msgData']['planeID'])
    imsg['msgHeader'] = localizeLobby('CHINA_LOBBY_RENT_CONTEXT_RENT_REFUND')
    imsg['msgData'] = {'msgBody': localizeMessages('CHINA_MESSAGE_RENT_AIRCRAFT_PURCHASED_REFUND').format(name=planeName, days=imsg['msgData']['refundPeriod']),
     'gold': imsg['msgData']['compensationGold']}
    return imsg


def serverOverloaded(imsg):
    imsg['msgHeader'] = ''
    imsg['msgData'] = dict(msgBody=localizeLobby('TRAINING_ROOMS_MSG_ERROR_NOT_READY'))
    return imsg


def broadcast(imsg):
    imsg['msgHeader'] = ''
    lang = localizeLobby('LOCALIZATION_LANGUAGE').lower()
    if isinstance(imsg['msgData'], dict):
        imsg['msgData'] = dict(msgBody=imsg['msgData'].get(lang, imsg['msgData']))
    else:
        imsg['msgData'] = dict(msgBody=imsg['msgData'])
    return imsg


def upgradesChanged(imsg):
    imsg['msgHeader'] = ''
    imsg['msgData'] = dict(credits=imsg['msgData']['credits'], exp=imsg['msgData']['exp'])
    return imsg


def award_complete(imsg):
    imsg['msgHeader'] = ''
    return imsg


birthdayConvertDict = {1: 'SYSTEM_MESSAGE_BIRTHDAY_1_MONTH',
 2: 'SYSTEM_MESSAGE_BIRTHDAY_3_MONTHS',
 3: 'SYSTEM_MESSAGE_BIRTHDAY_6_MONTHS',
 4: 'SYSTEM_MESSAGE_BIRTHDAY_9_MONTHS',
 5: 'SYSTEM_MESSAGE_BIRTHDAY_1_YEAR',
 6: 'SYSTEM_MESSAGE_BIRTHDAY_2_YEARS',
 7: 'SYSTEM_MESSAGE_BIRTHDAY_3_YEARS',
 8: 'SYSTEM_MESSAGE_BIRTHDAY_4_YEARS',
 9: 'SYSTEM_MESSAGE_BIRTHDAY_5_YEARS'}

def planeBirthday(imsg):

    def __processBirthday(birthdayData):
        planeName = __getAircraftName(int(birthdayData['planeID']))
        bd = birthdayData['birthday']
        msgBody = localizeMessages(birthdayConvertDict[bd]) if bd in birthdayConvertDict else bd
        d = dict(msgBody=msgBody.format(plane_name=planeName), planeName=planeName)
        for k in ('freeXP', 'premium', 'xpFactor', 'battles', 'creditsFactor', 'camouflage', 'birthday', 'planeID'):
            if k in birthdayData:
                d[k] = birthdayData[k]

        return d

    if 'birthdaysList' in imsg['msgData']:
        birthdaysList = imsg['msgData']['birthdaysList']
    else:
        birthdaysList = [imsg['msgData']]
    if len(birthdaysList) == 1:
        birthdayData = birthdaysList[0]
        planeName = __getAircraftName(int(birthdayData['planeID']))
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_BIRTHDAY_HEADER_ONE').format(plane_name=planeName)
    else:
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_BIRTHDAY_HEADER_FEW')
    for i, birthdayData in enumerate(birthdaysList):
        birthdaysList[i] = __processBirthday(birthdayData)

    imsg['msgData']['msgBody'] = ''
    return imsg


def planeBirthdayEmblem(imsg):
    msgData = imsg['msgData']
    if len(msgData['planes']) == 1:
        planeName = __getAircraftName(msgData['planes'][0])
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_BIRTHDAY_HEADER_ONE').format(plane_name=planeName)
    else:
        imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_BIRTHDAY_HEADER_FEW')
    msgData['msgBody'] = localizeLobby('LOBBY_BIRTHDAY_SEVERAL_YEARS')
    planesList = msgData['planes']
    msgData['planeIDs'] = planesList
    msgData['planes'] = [ __getAircraftName(planeID) for planeID in planesList ]
    return imsg


def planeBirthdayInfoBefore(imsg):
    msgData = imsg['msgData']
    planeName = __getAircraftName(int(msgData['planeID']))
    imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_BIRTHDAY_HEADER_ONE').format(plane_name=planeName)
    msgData['msgBody'] = localizeMessages(birthdayConvertDict.get(int(msgData['birthday']), '')).format(plane_name=planeName)
    msgData['description'] = localizeMessages('SYSTEM_MESSAGE_BIRTHDAY_EVENT_DATE')
    msgData['date'] = getFormattedTime(float(msgData['date']), Settings.g_instance.scriptConfig.timeFormated['dmY'])
    return imsg


def skinnerBoxAwards(imsg):
    imsg['msgHeader'] = localizeMessages('SYSTEM_MESSAGE_HEADER_PRIZES')
    imsg['msgData'] = dict(msgBody='', items=imsg['msgData']['items'], compensation=imsg['msgData']['compensation'], secretSanta=imsg['msgData'].get('secretSanta'))
    for item in imsg['msgData']['items']:
        item['icon'] = 'icons/quests/{0}'.format(item['icon'].split('/')[-1])

    return imsg


def __getAircraftName(aircraftID):
    airplaneData = db.DBLogic.g_instance.getAircraftData(aircraftID)
    if airplaneData.airplane is None:
        return ''
    else:
        return localizeAirplane(airplaneData.airplane.name)


def __localizeGoldPositive(amount):
    gold = abs(int(amount))
    return gold


def __localizeGoldNegative(amount):
    gold = -abs(int(amount))
    return gold


def __localizeTicketsNegative(amount):
    tickets = -abs(int(amount))
    return localizeMessages('LOBBY_MSG_PENALTY_TICKETS').format(tickets=tickets)


def __localizeTokensNegative(amount):
    tokens = -abs(int(amount))
    return localizeMessages('LOBBY_MSG_PENALTY_TOKENS').format(gold=tokens)


def __localizeCreditsPositive(amount):
    credits_ = abs(int(amount))
    return credits_


def __localizeCreditsNegative(amount):
    credits_ = -abs(int(amount))
    return credits_


def __localizeExpPositive(amount):
    exp = abs(int(amount))
    return localizeMessages('LOBBY_MSG_EXP').format(exp=exp)


def __localizeExpNegative(amount):
    exp = -abs(int(amount))
    return localizeMessages('LOBBY_MSG_PENALTY_EXP').format(exp=exp)


def __localizePlaneExpNegative(amount):
    exp = -abs(int(amount))
    return localizeMessages('LOBBY_MSG_PENALTY_EXP_PLANE').format(exp=exp)


def __localizeFreeExpNegative(amount):
    exp = -abs(int(amount))
    return localizeMessages('LOBBY_MSG_PENALTY_EXP_FREE').format(exp=exp)


def __localizeTicketsPositive(amount):
    tickets_ = abs(int(amount))
    return localizeMessages('LOBBY_MSG_PENALTY_TICKETS').format(tickets=tickets_)


def interview(imsg):
    msgData = imsg['msgData']
    imsg['msgHeader'] = ''
    imsg['isHidden'] = True
    imsg['msgData'] = dict(msgBody=localizeLobby(msgData['question']), title=localizeLobby(msgData['title']))
    if not BWPersonality.g_lobbyInterview[1]:
        BWPersonality.g_lobbyInterview = [localizeLobby(msgData['title']), localizeLobby(msgData['question'])]
        LOG_DEBUG('Added lobbyInterview,', BWPersonality.g_lobbyInterview)
    return imsg


def goldToTicketExchange(imsg):
    msgData = imsg['msgData']
    spentGold = int(msgData['gold']) if 'gold' in msgData else 0
    spentCredits = int(msgData['credits']) if 'credits' in msgData else 0
    tickets = int(msgData['tickets'])
    imsg['msgData']['msgBody'] = localizeLobby('LOBBY_EVENT_EXCHANGE_TICKETS_SUCCESFULL')
    if spentGold > 0:
        imsg['msgData']['gold'] = '-{0}'.format(abs(int(spentGold)))
    else:
        msgData.pop('gold', None)
    if spentCredits > 0:
        imsg['msgData']['credits'] = '-{0}'.format(abs(int(spentCredits)))
    elif spentCredits < 0:
        imsg['msgData']['credits'] = '{0}'.format(abs(int(spentCredits)))
    else:
        msgData.pop('credits', None)
    imsg['msgData']['tickets'] = '{0}{1}'.format('-' if tickets < 0 else '+', __localizeTicketsPositive(tickets))
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    return imsg


def skinnerCompensationTickets(imsg):
    msgData = imsg['msgData']
    credits = msgData['credits']
    tickets = msgData['tickets']
    if IS_CHINA:
        imsg['msgData']['msgBody'] = localizeLobby('LOBBY_EVENT_MESSAGE_TICKETS_EXCHANGE_CH')
    else:
        imsg['msgData']['msgBody'] = localizeLobby('LOBBY_EVENT_MESSAGE_TICKETS_EXCHANGE')
    if credits:
        imsg['msgData']['credits'] = '+{0}'.format(abs(int(credits)))
    else:
        imsg['msgData']['credits'] = ''
        imsg['msgData']['tickets'] = ''
    if tickets != 0:
        imsg['msgData']['tickets'] = '-{0}'.format(abs(int(tickets)))
    else:
        del imsg['msgData']['tickets']
    imsg['msgHeader'] = ''
    return imsg


def compensationQuestChips(imsg):
    msgData = imsg['msgData']
    gold = msgData['gold']
    questChips = msgData['questChips']
    imsg['msgData']['msgBody'] = localizeLobby('LOBBY_EVENT_MESSAGE_CERTIFICATE_EXCHANGE')
    if gold:
        imsg['msgData']['gold'] = '+{0}'.format(abs(int(gold)))
    else:
        imsg['msgData']['gold'] = ''
        imsg['msgData']['questChips'] = ''
    if questChips != 0:
        imsg['msgData']['questChips'] = '-{0}'.format(abs(int(questChips)))
    else:
        del imsg['msgData']['questChips']
    imsg['msgHeader'] = ''
    return imsg


def endActionSummer(imsg):
    imsg['msgData']['msgBody'] = localizeLobby('LOBBY_EVENT_MESSAGE_END_IS_NEAR1')
    imsg['msgHeader'] = ''
    return imsg


def skinnerBeforeEndAction(imsg):
    if IS_CHINA:
        imsg['msgData']['msgBody'] = localizeLobby('LOBBY_EVENT_MESSAGE_END_IS_NEAR_CH')
    else:
        imsg['msgData']['msgBody'] = localizeLobby('LOBBY_EVENT_MESSAGE_END_IS_NEAR')
    imsg['msgHeader'] = ''
    return imsg


def endOfSellGoldItems(imsg):
    imsg['msgData']['msgBody'] = ' '.join([localizeLobby('LOBBY_LABEL_STOP_SELL_EQUIPMENT'), localizeLobby('LOBBY_COMPENSATION_MESSAGE')])
    imsg['msgData']['msgTitle'] = localizeLobby('LOBBY_LABEL_STOP_SELL_GOLD_BELT')
    imsg['msgHeader'] = localizeLobby('LOBBY_POPUP_MESSAGE1_URGENT')
    return imsg


def beltsRecharged(imsg):
    rechargedWeapons = imsg['msgData']['weapons']
    rechargedCount = len(rechargedWeapons)
    if rechargedCount is 1:
        wName = localizeUpgrade(db.DBLogic.g_instance.upgrades[rechargedWeapons[0]])
        imsg['msgData'] = dict(msgBody=localizeLobby('MESSAGE_INSTALLED_STANDARTBELT_1', armour_name=wName))
    elif rechargedCount is 2:
        wNames = [ localizeUpgrade(db.DBLogic.g_instance.upgrades[weapon]) for weapon in rechargedWeapons ]
        imsg['msgData'] = dict(msgBody=localizeLobby('MESSAGE_INSTALLED_STANDARTBELT_2', armour_name1=wNames[0], armour_name2=wNames[1]))
    else:
        LOG_ERROR('Unexpected weapons count got. Expected 1 or 2, got {0}'.format(rechargedCount))
    return imsg


def warActionWarBegin(imsg):
    LOG_DEBUG('warActionWarBegin', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('LOBBY_BANNER_JA_TR_TEXT_1'))
    return imsg


def warActionWarEnd(imsg):
    LOG_DEBUG('warActionWarBegin', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('LOBBY_BANNER-2_JA_TR_TEXT_1'))
    return imsg


def warActionFirstLoose(imsg):
    LOG_DEBUG('warActionFirstLoose', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_FIRST_LOOSE'))
    return imsg


def warActionScoreLead(imsg):
    LOG_DEBUG('warActionScoreLead', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_SCORE_LEAD'))
    return imsg


def warActionScoreEquals(imsg):
    imsg['msgData'] = dict(msgBody=localizeLobby('MESSAGE_WARACTION_SCORE_EQUALS'))
    LOG_DEBUG('warActionScoreEquals', imsg)
    return imsg


def warActionScoreHalf(imsg):
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_SCORE_HALF'))
    LOG_DEBUG('warActionScoreHalf', imsg)
    return imsg


def warActionVictoryIsNear(imsg):
    LOG_DEBUG('warActionVictoryIsNear', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_VICTORY_IS_NEAR'))
    return imsg


def warActionUnbreakableSeries(imsg):
    LOG_DEBUG('warActionUnbreakableSeries', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_UNBREAKABLE_SERIES'))
    return imsg


def warActionEpicAwardGain(imsg):
    LOG_DEBUG('warActionUnbreakableSeries', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_EPIC_AWARD_GAIN'))
    return imsg


def warActionHeroAwardGain(imsg):
    LOG_DEBUG('warActionUnbreakableSeries', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_HERO_AWARD_GAIN'))
    return imsg


def warActionWinWithoutLoose(imsg):
    LOG_DEBUG('warActionUnbreakableSeries', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_WIN_WITHOUT_LOOSE'))
    return imsg


def warActionALotPlanesLoose(imsg):
    LOG_DEBUG('warActionUnbreakableSeries', imsg)
    imsg['msgData'] = dict(fraction=imsg['msgData'], msgBody=localizeLobby('MESSAGE_WARACTION_A_LOT_PLANE_LOOSE'))
    return imsg


def buyPack(imsg):
    spendCredits, spendGold, sendTickets = imsg['msgData']['price']
    imsg['msgHeader'] = localizeMessages('LOBBY_HEADER_BOUGHT')
    if spendCredits:
        imsg['msgData']['credits'] = __localizeCreditsNegative(spendCredits)
    if spendGold:
        imsg['msgData']['gold'] = __localizeGoldNegative(spendGold)
    if sendTickets:
        imsg['msgData']['tickets'] = __localizeTicketsNegative(sendTickets)
    msgParams = imsg['msgData']['msgParam']
    imsg['msgData']['planes'] = []
    for planeID in msgParams.get('planes', []):
        imsg['msgData']['planes'].append(__getAircraftName(planeID))

    return imsg


def buyPackInfo(imsg):
    msgParams = imsg['msgData']['msgParam']
    imsg['msgData']['planes'] = []
    for planeID in msgParams.get('planes', []):
        imsg['msgData']['planes'].append(__getAircraftName(planeID))

    return imsg


def secretsanta(imsg):
    return imsg


_MESSAGE_HANDLERS = {MESSAGE_TYPE.MOTD: motd,
 MESSAGE_TYPE.REBOOT: reboot,
 MESSAGE_TYPE.GOLD_RECEIVED: goldReceived,
 MESSAGE_TYPE.TUTORIAL_REWARD: tutorialReward,
 MESSAGE_TYPE.TUTORIAL_REWARD_GOLD: tutorialRewardGold,
 MESSAGE_TYPE.USER_BANNED: ban,
 MESSAGE_TYPE.USER_UNBANNED: unban,
 MESSAGE_TYPE.PREMIUM_BOUGHT: premBought,
 MESSAGE_TYPE.PREMIUM_EXTENDED: premExtended,
 MESSAGE_TYPE.PREMIUM_EXPIRED: premExpired,
 MESSAGE_TYPE.RESULT_BATTLE: resbattle,
 MESSAGE_TYPE.REPAIR_AIRCRAFT: repair,
 MESSAGE_TYPE.REFILL_AIRCRAFT_SHELLS: refillAircraftShells,
 MESSAGE_TYPE.REFILL_AIRCRAFT_BELTS: refillAircraftBelts,
 MESSAGE_TYPE.REFILL_AIRCRAFT_CONSUMABLES: refillAircraftConsumables,
 MESSAGE_TYPE.BUY_AIRCRAFT: buy,
 MESSAGE_TYPE.SELL_AIRCRAFT: sell,
 MESSAGE_TYPE.RESEARCH_AIRCRAFT: research,
 MESSAGE_TYPE.GOLD_SPENT: goldSpent,
 MESSAGE_TYPE.CREDITS_RECEIVED: creditsReceived,
 MESSAGE_TYPE.EXCHANGE_EXP: exchangeExp,
 MESSAGE_TYPE.INSTALL_PRESET: installPreset,
 MESSAGE_TYPE.SQUAD_INVITE_ACCEPTED: squadInviteAccepted,
 MESSAGE_TYPE.SQUAD_INVITE_REJECTED: squadInviteRejected,
 MESSAGE_TYPE.SQUAD_MEMBER_LEAVING: squadMemberLeaving,
 MESSAGE_TYPE.SQUAD_INVITATION: squadInvite,
 MESSAGE_TYPE.SQUAD_LEAVING: squadLeaving,
 MESSAGE_TYPE.SQUAD_EXCLUDED: squadExcluding,
 MESSAGE_TYPE.SQUAD_DESTROYED: squadDestroying,
 MESSAGE_TYPE.SQUAD_ERROR_MEMBER_OFFLINE: squadErrorMemberOffline,
 MESSAGE_TYPE.SQUAD_ERROR_MEMBER_BATTLE: squadErrorMemberBattle,
 MESSAGE_TYPE.SQUAD_ERROR_MEMBER_NOT_IN_SQUADFINDER: squadErrorMemberNotInSquadFinder,
 MESSAGE_TYPE.RESEARCH_UPGRADE: researchUpgrade,
 MESSAGE_TYPE.BUY_UPGRADE: buyUpgrade,
 MESSAGE_TYPE.INSTALL_UPGRADE: installUpgrade,
 MESSAGE_TYPE.UNINSTALL_UPGRADE: uninstallUpgrade,
 MESSAGE_TYPE.BUY_EQUIPMENT: buyEquipment,
 MESSAGE_TYPE.INSTALL_EQUIPMENT: installEquipment,
 MESSAGE_TYPE.DETACH_EQUIPMENT: detachEquipment,
 MESSAGE_TYPE.DESTROY_EQUIPMENT: destroyedEquipment,
 MESSAGE_TYPE.BUY_CONSUMABLES: buyConsumables,
 MESSAGE_TYPE.SCREENSHOT: screenshotPopup,
 MESSAGE_TYPE.VOIP_SERVICE_DOWN: voipServiceDown,
 MESSAGE_TYPE.TRAINING_SKILL: trainingSkill,
 MESSAGE_TYPE.RETRAINING_SKILL: reTrainingSkill,
 MESSAGE_TYPE.DROP_SKILLS: dropSkills,
 MESSAGE_TYPE.GOT_FIRST_SP: gotFirstSP,
 MESSAGE_TYPE.GOT_NEW_SP: gotNewSP,
 MESSAGE_TYPE.CREW_DEMOBILIZE: crewDemobilize,
 MESSAGE_TYPE.CREW_EXP_PUMPING: crewExpPumping,
 MESSAGE_TYPE.CHANGE_XP_TO_SP: changeXpToSp,
 MESSAGE_TYPE.GIFT_PLANE_I15DM2: giftPlaneI15dm2,
 MESSAGE_TYPE.GIFT_PLANE: giftPlane,
 MESSAGE_TYPE.GIFT_PLANE_SLEIPNIR: giftPlaneSleipnir,
 MESSAGE_TYPE.DEDUCT_PLANE: deductPlane,
 MESSAGE_TYPE.SHOP_PURCHASE: shopPurchase,
 MESSAGE_TYPE.BUY_SLOT: buySlot,
 MESSAGE_TYPE.CREW_MEMBER_GET_NEW_RANK: crewMemberGetNewRank,
 MESSAGE_TYPE.BUY_AMMO: buyAmmo,
 MESSAGE_TYPE.SELL_AMMO: sellAmmo,
 MESSAGE_TYPE.SELL_UPGRADE: sellUpgrade,
 MESSAGE_TYPE.SELL_EQUIPMENT: sellEquipment,
 MESSAGE_TYPE.SELL_CONSUMABLES: sellConsumables,
 MESSAGE_TYPE.TOKEN_EXCHANGED: tokenExchanged,
 MESSAGE_TYPE.BUY_BARRACK_SLOTS: buyBarrackSlot,
 MESSAGE_TYPE.BUY_CAMOUFLAGE: buyCamouflage,
 MESSAGE_TYPE.WALLET_CONNECTED: walletConnected,
 MESSAGE_TYPE.REFILL_FAILED: refillFailed,
 MESSAGE_TYPE.PREMIUM_BELTS_GIVEN: premiumBeltsGiven,
 MESSAGE_TYPE.QUEST_GET_BONUS: questGetBonus,
 MESSAGE_TYPE.QUEST_NEW_MESSAGES: questNewMessage,
 MESSAGE_TYPE.SERVER_DOWNTIME_COMPENSATION: serverDowntimeCompensation,
 MESSAGE_TYPE.PLANE_RENT_EXTENDED: aircraftRentExtended,
 MESSAGE_TYPE.PLANE_PURCHASED_RENT_REFUND: aircraftPurchasedRentRefund,
 MESSAGE_TYPE.SERVER_OVERLOADED: serverOverloaded,
 MESSAGE_TYPE.BROADCAST: broadcast,
 MESSAGE_TYPE.PLANE_RENT_COMPENSATION: rentComplencation,
 MESSAGE_TYPE.UPGRADES_CHANGED: upgradesChanged,
 MESSAGE_TYPE.AWARD_COMPLETE: award_complete,
 MESSAGE_TYPE.PLANE_BIRTHDAY: planeBirthday,
 MESSAGE_TYPE.PLANE_BIRTHDAY_EMBLEM: planeBirthdayEmblem,
 MESSAGE_TYPE.PLANE_BIRTHDAY_INFO_BEFORE: planeBirthdayInfoBefore,
 MESSAGE_TYPE.GOLD_TO_TICKET_EXCHANGE: goldToTicketExchange,
 MESSAGE_TYPE.INTERVIEW_WINDOW: interview,
 MESSAGE_TYPE.SKINNER_BOX_AWARDS: skinnerBoxAwards,
 MESSAGE_TYPE.TICKETS_RECEIVED: ticketsReceived,
 MESSAGE_TYPE.SKINNER_END_ACTION_WINDOW: skinnerCompensationTickets,
 MESSAGE_TYPE.SKINNER_BEFORE_END_ACTION_WINDOW: skinnerBeforeEndAction,
 MESSAGE_TYPE.END_OF_SELL_GOLD_ITEMS: endOfSellGoldItems,
 MESSAGE_TYPE.COMPENSATION_QUEST_CHIPS: compensationQuestChips,
 MESSAGE_TYPE.BUY_QUEST_CHIPS: buyQuestChips,
 MESSAGE_TYPE.SPEND_BUYING_QUEST: buyQuestAndSpendCurrency,
 MESSAGE_TYPE.WAR_CASH_PAY_TICKET: warCashPayTicket,
 MESSAGE_TYPE.WARNING_END_OF_ACTION_SUMMER: endActionSummer,
 MESSAGE_TYPE.WINDOW_BELTS_RECHARGED: beltsRecharged,
 MESSAGE_TYPE.TOOLTIP_HOLIDAY_HANGAR: switchSpaceHandler,
 MESSAGE_TYPE.WAR_ACTION_WAR_BEGIN: warActionWarBegin,
 MESSAGE_TYPE.WAR_ACTION_FIRST_LOOSE: warActionFirstLoose,
 MESSAGE_TYPE.WAR_ACTION_SCORE_LEAD: warActionScoreLead,
 MESSAGE_TYPE.WAR_ACTION_SCORE_EQUALS: warActionScoreEquals,
 MESSAGE_TYPE.WAR_ACTION_SCORE_HALF: warActionScoreHalf,
 MESSAGE_TYPE.WAR_ACTION_VICTORY_IS_NEAR: warActionVictoryIsNear,
 MESSAGE_TYPE.WAR_ACTION_WAR_END: warActionWarEnd,
 MESSAGE_TYPE.WAR_ACTION_UNBREAKABLE_SERIES: warActionUnbreakableSeries,
 MESSAGE_TYPE.WAR_ACTION_EPIC_AWARD_GAIN: warActionEpicAwardGain,
 MESSAGE_TYPE.WAR_ACTION_HERO_AWARD_GAIN: warActionHeroAwardGain,
 MESSAGE_TYPE.WAR_ACTION_WIN_WITHOUT_LOOSE: warActionWinWithoutLoose,
 MESSAGE_TYPE.WAR_ACTION_A_LOT_PLANES_LOOSE: warActionALotPlanesLoose,
 MESSAGE_TYPE.WAR_ACTION_CHANGE_FRACTION: warActionChangeFraction,
 MESSAGE_TYPE.BUY_PACK_INFO: buyPackInfo,
 MESSAGE_TYPE.SECRET_SANTA_ACHIEVEMENT: secretsanta}

def handle(imsg):
    try:
        return _MESSAGE_HANDLERS.get(imsg['msgType'], defaultHandler)(imsg)
    except Exception as e:
        LOG_ERROR('Error occured in message handler: {0}'.format(e))
        LOG_ERROR('Wrong message {0}'.format(imsg))
        return defaultHandler(imsg)


_GROUP_HANDLERS = {}

class GroupHandler(object):

    def __init__(self, grpType):
        super(GroupHandler, self).__init__()
        self.grpType = grpType

    def __call__(self, handler):
        if self.grpType in _GROUP_HANDLERS:
            LOG_WARNING('Redefinition of handler for group type {0}'.format(self.grpType))
        _GROUP_HANDLERS[self.grpType] = handler
        return handler


@GroupHandler(MESSAGE_GROUP_TYPE.COMMON)
def defaultGroupHandler(msgList):

    def processMessage(msgListEntry):
        index, message = msgListEntry
        return (index, handle(message))

    return list(map(processMessage, msgList))


@GroupHandler(MESSAGE_GROUP_TYPE.SERVICE)
def serviceGroupHandler(msgList):
    _, fMessage = msgList[0]
    planeID = fMessage['msgData'].get('planeID', 0)
    serviceMessage = {'msgType': MESSAGE_GROUP_TYPE.SERVICE,
     'msgData': {'msgBody': localizeMessages('COMPONENT_NAME_LABEL_MAINTENANSE_EXPENSES'),
                 'itemName': __getAircraftName(planeID) if planeID else '',
                 'credits': 0,
                 'gold': 0,
                 'tickets': 0,
                 'isFreeAction': True}}
    for _, message in msgList:
        creds, gold, tickets = (0, 0, 0)
        if 'price' in message['msgData']:
            creds, gold, tickets = message['msgData']['price'] + (0,) * (3 - len(message['msgData']['price']))
        else:
            if 'credits' in message['msgData']:
                creds = message['msgData']['credits']
            if 'gold' in message['msgData']:
                gold = message['msgData']['gold']
            if 'tickets' in message['msgData']:
                tickets = message['msgData']['tickets']
        serviceMessage['msgData']['credits'] += creds
        serviceMessage['msgData']['gold'] += gold
        serviceMessage['msgData']['tickets'] += tickets
        serviceMessage['msgData']['isFreeAction'] = serviceMessage['msgData']['isFreeAction'] and message['msgData'].get('isFreeAction', False)

    serviceMessage['msgData']['credits'] = -abs(serviceMessage['msgData']['credits'])
    serviceMessage['msgData']['gold'] = -abs(serviceMessage['msgData']['gold'])
    serviceMessage['msgData']['tickets'] = -abs(serviceMessage['msgData']['tickets'])
    if serviceMessage['msgData']['credits'] != 0 or serviceMessage['msgData']['gold'] != 0:
        serviceMessage['msgData']['isFreeAction'] = False
    if serviceMessage['msgData']['isFreeAction']:
        serviceMessage['msgData']['description'] = localizeMessages('LOBBY_MSG_AMMO_REFILL_FREE_PVE')
    messageIndex = min(map(itemgetter(0), msgList))
    return [(messageIndex, serviceMessage)]


def handleGroup(msgGroup, msgList):
    try:
        return _GROUP_HANDLERS.get(msgGroup, defaultGroupHandler)(msgList)
    except Exception as e:
        LOG_ERROR('Error occured in message handler: {0}'.format(e))
        return defaultGroupHandler(msgList)


def birthdayCleaner(grpList):
    bithPlaneIDs, emblemPlaneIDs = [], []
    cacheEmblemGrp = None
    for grp in grpList:
        if grp['msgType'] == MESSAGE_TYPE.PLANE_BIRTHDAY:
            bithPlaneIDs = [ int(l['planeID']) for l in grp['msgData'].get('birthdaysList', []) ]
        if grp['msgType'] == MESSAGE_TYPE.PLANE_BIRTHDAY_EMBLEM:
            emblemPlaneIDs = grp['msgData'].get('planes', [])
            cacheEmblemGrp = grp

    for planeID in bithPlaneIDs:
        if planeID in emblemPlaneIDs:
            emblemPlaneIDs.remove(planeID)

    if cacheEmblemGrp and emblemPlaneIDs:
        cacheEmblemGrp['planes'] = emblemPlaneIDs
        return grpList
    else:
        return [ grp for grp in grpList if grp['msgType'] != MESSAGE_TYPE.PLANE_BIRTHDAY_EMBLEM ]
        return [ grp for grp in grpList if grp['msgType'] != MESSAGE_TYPE.PLANE_BIRTHDAY_EMBLEM ]


def handleMessageGroup(imsg):
    grpList = imsg['msgData']['grpList']
    grpMap = {}
    grpList = birthdayCleaner(grpList)
    for i, entry in enumerate(grpList):
        msgGroup = entry['msgGroup']
        grpMap.setdefault(msgGroup, []).append((i, entry))

    handledList = []
    for msgGroup, msgList in grpMap.iteritems():
        handledGroup = handleGroup(msgGroup, msgList)
        handledList.extend(handledGroup)

    handledList.sort(key=itemgetter(0))
    resultList = list(map(itemgetter(1), handledList))
    imsg['msgData'] = dict(msgList=resultList)
    return imsg