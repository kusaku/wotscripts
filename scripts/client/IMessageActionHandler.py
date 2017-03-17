# Embedded file name: scripts/client/IMessageActionHandler.py
import BigWorld
import db.DBLogic
from consts import MESSAGE_TYPE, BLOCK_TYPE
from Helpers.i18n import localizeMessages, getFormattedTime, localizeTutorial, localizeChat
from Helpers.i18n import localizeMap, localizeBattleResults, localizeAirplane
from gui.Scaleform.BattleResult import getStrValueWithFactor
from gui.HtmlMessagerTypes import HtmlMessagerTypes
from debug_utils import LOG_ERROR, LOG_TRACE

def defaultHandler(imsg):
    """
    Default message handler. Return imsg without any transforms
    :param imsg: IMessage
    """
    imsg['msgData'] = dict(msgBody=imsg['msgData'])
    return imsg


def chat(imsg):
    """
    Chat message handler
    :param imsg: IMessage
    """
    import messenger
    if messenger.g_xmppChatHandler:
        messenger.g_xmppChatHandler.onReceiveSystemMessage(imsg['senderName'], imsg['msgData'])


def premBought(imsg):
    msgData = imsg['msgData']
    BigWorld.player().premBought(msgData['expiryTime'], msgData['waitForUserAction'])


def premExtended(imsg):
    msgData = imsg['msgData']
    BigWorld.player().premExtended(msgData['expiryTime'], msgData['expiryTimeDelta'])


def premExpired(imsg):
    BigWorld.player().premExpired()


def resbattle(imsg):
    import BWPersonality
    msgData = imsg['msgData']
    BWPersonality.g_lobbyCarouselHelper.updatePlaneAfterBattle(msgData['aircraftID'])


def updateInBattle(imsg):
    msgData = imsg['msgData']
    planeID = msgData['planeID']
    import BWPersonality
    if not BWPersonality.g_lobbyCarouselHelper.inventory.getAircraftPData(planeID):
        LOG_ERROR('Attempt to update plane (id={0}) that is not present in carousel'.format(planeID))
        return
    blockType = msgData['blockType']
    LOG_TRACE('updateInBattle() setting block type {0} for {1}'.format(blockType, planeID))
    from Account import PLANE_BLOCK_TYPE
    PLANE_BLOCK_TYPE[planeID] = blockType or BLOCK_TYPE.UNLOCKED
    BWPersonality.g_lobbyCarouselHelper.setPlaneBlockType(planeID, blockType)
    BWPersonality.g_lobbyCarouselHelper.updateInBattleButton(True)
    BWPersonality.g_lobbyCarouselHelper.refreshAircraftData(planeID, True)
    selectedPlane = BWPersonality.g_lobbyCarouselHelper.getCarouselAirplaneSelected()
    if selectedPlane and selectedPlane.planeID == planeID:
        BWPersonality.g_lobbyCarouselHelper.queryRefresh3DModel(selectedPlane)


def freeXPActivated(imsg):
    pass


def giftPlane(imsg):
    BigWorld.player()._lobbyInstance.giftPlaneWindowShow()


def synAllInventory(imsg):
    import BWPersonality
    BWPersonality.g_lobbyCarouselHelper.inventory.syncInventoryData()


def pvpFirstRun(imsg):
    msgData = imsg['msgData']
    BigWorld.player()._lobbyInstance.pveWindowShow(MESSAGE_TYPE.PVP_FIRST_RUN)


def pveOldUserWelcome(imsg):
    BigWorld.player()._lobbyInstance.pveWindowShow(MESSAGE_TYPE.PVE_OLDUSER_WELCOME)


def pveCompleteMainQuest(imsg):
    msgData = imsg['msgData']
    gold = msgData['gold']
    credits = msgData['credits']
    freeXP = msgData['freeXP']
    BigWorld.player()._lobbyInstance.pveWindowShow(MESSAGE_TYPE.PVE_COMPLETE_MAIN_QUEST, freeXP, credits, gold)


def pveVsPvpInfo(imsg):
    BigWorld.player()._lobbyInstance.pveWindowShow(MESSAGE_TYPE.PVE_VS_PVP_INFO)


def pveInviteWelcome(imsg):
    BigWorld.player()._lobbyInstance.pveWindowShow(MESSAGE_TYPE.PVE_INVITE_WELCOME)


def callmethod(imsg):
    import BWPersonality
    instDict = dict(lobby=BWPersonality.g_lobbyCarouselHelper.getHandler(), carouselHelper=BWPersonality.g_lobbyCarouselHelper, trainingRoomHelper=BWPersonality.g_lobbyCarouselHelper.getHandler().trainingRoomHelper, researchTreeHelper=BWPersonality.g_lobbyCarouselHelper.getHandler().researchTreeHelper, lobbyShopHelper=BWPersonality.g_lobbyCarouselHelper.getHandler().lobbyShopHelper)
    data = imsg['msgData']
    try:
        ob = instDict[data['obname']]
        try:
            func = data['func']
            func = getattr(ob, func)(*data['args'])
        except AttributeError:
            LOG_ERROR('Method {0} in object {1} not found'.format(func, ob))
        except TypeError as e:
            LOG_ERROR('Object {0}. Error {1}'.format(ob, e))

    except KeyError:
        LOG_ERROR('Object {0} not found'.format(ob))


_MESSAGE_HANDLERS = {MESSAGE_TYPE.ADMIN: chat,
 MESSAGE_TYPE.PRIVATE: chat,
 MESSAGE_TYPE.PREMIUM_BOUGHT: premBought,
 MESSAGE_TYPE.PREMIUM_EXTENDED: premExtended,
 MESSAGE_TYPE.PREMIUM_EXPIRED: premExpired,
 MESSAGE_TYPE.RESULT_BATTLE: resbattle,
 MESSAGE_TYPE.GIFT_PLANE: giftPlane,
 MESSAGE_TYPE.UPDATE_IN_BATTLE_BUTTON: updateInBattle,
 MESSAGE_TYPE.CALL_CLIENT_METHOD: callmethod,
 MESSAGE_TYPE.FREE_XP_ACTIVATED: freeXPActivated,
 MESSAGE_TYPE.PVP_FIRST_RUN: pvpFirstRun,
 MESSAGE_TYPE.PVE_OLDUSER_WELCOME: pveOldUserWelcome,
 MESSAGE_TYPE.PVE_COMPLETE_MAIN_QUEST: pveCompleteMainQuest,
 MESSAGE_TYPE.PVE_VS_PVP_INFO: pveVsPvpInfo,
 MESSAGE_TYPE.PVE_INVITE_WELCOME: pveInviteWelcome,
 MESSAGE_TYPE.SYSTEM_SYNC_ALL_INVENTORY: synAllInventory}

def handle(imsg):
    return _MESSAGE_HANDLERS.get(imsg['msgType'], defaultHandler)(imsg)