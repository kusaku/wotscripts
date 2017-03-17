# Embedded file name: scripts/client/Helpers/AccountOperationsMgr.py
from OperationCodes import OPERATION_CODE
from Operations.OperationSender import OperationSender
from config_consts import IS_DEVELOPMENT
from wgPickle import FromClientToServer, FromServerToClient
from functools import partial
from Helpers.reliableDelivery import ifaceDataCallback
from consts import TRAINING_ROOM_CREATE_DESCRIPTION_LIMIT
from exchangeapi.CompactDescriptor import requestToCompactDescriptor

class AccountOperationsMgr(OperationSender):

    def __init__(self, receiver, invocationIdCounter = None):
        OperationSender.__init__(self, receiver, FromServerToClient, FromClientToServer, invocationIdCounter)

    def _sendOp(self, opCode, callback, *args):
        op = self.sendOperation(opCode, None, False, *args)
        if callback is not None:
            op.onResponse += callback
        return op

    def verifyCaptcha(self, challenge, response, callback):
        """
        @param challenge: challenge string
        @param response: client CAPTCHA response
        @param callback: delegate(operation, returnCode, errorCode)
        """
        self.sendOperation(OPERATION_CODE.CAPTCHA_CHALLENGE, None, False, challenge, response).onResponse += callback
        return

    def getCaptchaData(self, callback):
        """
        @param callback: delegate(operation, returnCode, publicKey)
        """
        self.sendOperation(OPERATION_CODE.CAPTCHA_GET_DATA, None, False).onResponse += callback
        return

    def getAOGASInfo(self, callback):
        """
        @param callback: delegate(operation, returnCode, accOnline, sessionStartedAt)
        """
        self.sendOperation(OPERATION_CODE.AOGAS_GET_INFO, None, False).onResponse += callback
        return

    def installPresetOnAircraft(self, globalID, callback):
        """
        Install preset by preset name
        @param globalID:
        @param callback:
        """
        self.sendOperation(OPERATION_CODE.CMD_INSTALL_PRESSET, None, False, globalID).onResponse += callback
        return

    def clearInventory(self, callback):
        """
        Request to clear user inventory
        """
        self._sendOp(OPERATION_CODE.CMD_CLEAR_INVENTORY, callback)

    def saveCustomPreset(self, globalID, callback):
        self.sendOperation(OPERATION_CODE.CMD_SAVE_CUSTOM_PRESET, None, False, globalID).onResponse += callback
        return

    def getTrainingRoomFilters(self, callback = None):
        self._sendOp(OPERATION_CODE.CMD_GET_TRAINING_ROOM_FILTERS, callback)

    def refreshRoomList(self, mapID, gameModeID, fireModeID, levelTypeID, callback = None):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_REFRESH_ROOM_LIST, callback, mapID, gameModeID, fireModeID, levelTypeID)

    def subscribeRoomList(self, roomType, callback = None):
        self._sendOp(OPERATION_CODE.CMD_SUBSCRIBE_ROOM_LIST, callback, roomType)

    def unSubscribeRoomList(self, roomType, callback = None):
        self._sendOp(OPERATION_CODE.CMD_UNSUBSCRIBE_ROOM_LIST, callback, roomType)

    def getTrainingCreateRoomFilters(self, callback = None):
        self._sendOp(OPERATION_CODE.CMD_GET_TRAINING_CREATE_ROOM_FILTERS, callback)

    def getTrainingCreateRoomCreated(self, roomData, callback = None):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_ROOM_CREATED, callback, roomData)

    def getInitDataOnEnterToTrainingRoom(self, callback = None):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_ENTER_ROOM_GET_INIT_DATA, callback)

    def enterTrainingRoom(self, roomID, callback = None):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_ON_ENTER_ROOM, callback, roomID)

    def updateAccountTeamID(self, accountID, teamID):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_UPDATE_ACCOUNT_TEAM_ID, None, accountID, teamID).destroy()
        return

    def trainingSwapTeams(self):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_SWAP_TEAMS, None).destroy()
        return

    def trainingMoveTeam(self, origTeamID, destTeamID):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_MOVE_TEAM, None, origTeamID, destTeamID).destroy()
        return

    def addBots(self, botsCount, botsPlaneID, teamID, difficulty, level, fillType, planeType, planeNation):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_ADD_BOTS, None, botsCount, botsPlaneID, teamID, difficulty, level, fillType, planeType, planeNation).destroy()
        return

    def trainingEditBot(self, botID, planeID, difficulty, level, planeType, planeNation):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_EDIT_BOT, None, botID, planeID, difficulty, level, planeType, planeNation).destroy()
        return

    def botsAutoFill(self):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_BOTS_AUTO_FILL, None).destroy()
        return

    def botsRemove(self):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_BOTS_REMOVE, None).destroy()
        return

    def deleteBot(self, botID):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_DELETE_BOT, None, botID).destroy()
        return

    def changeMap(self, mapID):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_CHANGE_MAP, None, mapID).destroy()
        return

    def changeDescription(self, txtDescription):
        txtDescription = str(txtDescription[:TRAINING_ROOM_CREATE_DESCRIPTION_LIMIT])
        self._sendOp(OPERATION_CODE.CMD_TRAINING_CHANGE_DESC, None, txtDescription).destroy()
        return

    def leaveTrainingRoom(self):
        self._sendOp(OPERATION_CODE.CMD_TRAINING_ROOM_LEAVE, None).destroy()
        return

    def showTrainingRoomResponse(self):
        self._sendOp(OPERATION_CODE.CMD_SHOW_TRAINING_ROOM_RESPONSE, None).destroy()
        return

    def aircraftResearch(self, aircraftID, parentPlaneID = None, callback = None):
        self._sendOp(OPERATION_CODE.CMD_TREE_AIRCRAFT_RESEARCH, callback, aircraftID, parentPlaneID)

    def researchUpgrade(self, aircraftID, upgradeName, callback):
        """
        @param aircraftID:
        @param upgradeName: upgrade name that should be researched
        @param callback:
        """
        self._sendOp(OPERATION_CODE.CMD_RESEARCH_UPGRADE, callback, aircraftID, upgradeName)

    def buyUpgrade(self, aircraftID, moduleName, count, callback):
        """
        @param aircraftID:
        @param moduleName: module upgrade name that should be bought
        @param count:
        @param callback:
        """
        self._sendOp(OPERATION_CODE.CMD_BUY_UPGRADE, callback, aircraftID, moduleName, count)

    def setSlotPrimary(self, slotID, isPrimary, callback = None):
        self._sendOp(OPERATION_CODE.CMD_HANGAR_SET_SLOT_PRIMARY, callback, slotID, isPrimary)

    def updatePlayerResources(self, callback = None):
        self._sendOp(OPERATION_CODE.CMD_HANGAR_UPDATE_PLAYER_RESOURCES, callback)

    def setAirplaneAutoRepairFlag(self, planeID, value):
        self._sendOp(OPERATION_CODE.CMD_HANGAR_SET_AIRPLANE_AUTO_REPAIR_FLAG, None, planeID, value).destroy()
        return

    def getAircraftsExp(self, callback):
        self._sendOp(OPERATION_CODE.CMD_GET_AIRCRAFT_EXP, callback)

    def setTutorialInvite(self, lessonIndex):
        self._sendOp(OPERATION_CODE.CMD_HANGAR_SET_TUTORIAL_INVITES, None, lessonIndex)
        return

    def dbgBreakAllPlanes(self, callback = None):
        self._sendOp(OPERATION_CODE.CMD_DEBUG_BREAK_ALL_PLANES, callback)

    def dbgQuestProgress(self, operation, questID, callback = None):
        if IS_DEVELOPMENT and operation in [OPERATION_CODE.CMD_DEBUG_QUEST_CHANGE_PROGRESS,
         OPERATION_CODE.CMD_DEBUG_QUEST_SEND_MESSAGE,
         OPERATION_CODE.CMD_DEBUG_QUEST_SET_COMPLETE,
         OPERATION_CODE.CMD_DEBUG_QUEST_DROP_PROGRESS,
         OPERATION_CODE.CMD_DEBUG_QUEST_RESET_DAILY]:
            self._sendOp(operation, callback, questID)

    def dbgRepairAllPlanes(self, callback = None):
        self._sendOp(OPERATION_CODE.CMD_DEBUG_REPAIR_ALL_PLANES, callback)

    def buyPremium(self, timeIndex, callback = None):
        self._sendOp(OPERATION_CODE.CMD_HANGAR_BUY_PREMIUM, callback, timeIndex)

    def buyCredits(self, credits, gold, callback = None):
        self._sendOp(OPERATION_CODE.CMD_HANGAR_BUY_CREDITS, callback, credits, gold)

    def buyFreeExp(self, freeExp, planeIDs, gold, callback = None):
        self._sendOp(OPERATION_CODE.CMD_HANGAR_BUY_FREE_EXP, callback, freeExp, planeIDs, gold)

    def setShellsAutoRefillingFlag(self, aircraftID, flag):
        self._sendOp(OPERATION_CODE.CMD_MAINTENANCE_SET_SHELLS_AUTO_REFILLING_FLAG, None, aircraftID, flag).destroy()
        return

    def getIfaceData(self, requestobserv, callback = None):
        self._sendOp(OPERATION_CODE.CMD_GET_IFACE_DATA, partial(ifaceDataCallback, callback), requestToCompactDescriptor(requestobserv))

    def getInterfaceData(self, callback, ifaceName):
        self._sendOp(OPERATION_CODE.CMD_GET_INTERFACE_DATA, callback, ifaceName)

    def getNewSessionKey(self, callback):
        self._sendOp(OPERATION_CODE.CMD_GET_NEW_SESSION_KEY, callback)

    def saveSessionKey(self, sessionKey, callback = None):
        self._sendOp(OPERATION_CODE.CMD_SAVE_SESSION_KEY, callback, sessionKey)

    def sessionKeySynced(self):
        self._sendOp(OPERATION_CODE.CMD_SESSION_KEY_SYNCED, None)
        return

    def interviewAnswer(self, data, callback = None):
        self._sendOp(OPERATION_CODE.CMD_SEND_INTERVIEW_ANSWER, callback, data)