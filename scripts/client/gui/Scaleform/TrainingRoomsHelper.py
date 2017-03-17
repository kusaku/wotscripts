# Embedded file name: scripts/client/gui/Scaleform/TrainingRoomsHelper.py
import BigWorld
import db.DBLogic
from consts import GAME_MODE, TRAINING_ROOM_REASON, UNDEFINED_PLANE, PREBATLE_ACCOUNT_STATUS, BOT_DIFFICULTY
import consts
import messenger
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_WARNING, LOG_TRACE
from Helpers.i18n import localizeHUD, localizeLobby, localizeMap, localizeAirplane, convert as convertToLocal
from Helpers.namesHelper import getBotName
from gui.Scaleform.Waiting import Waiting
from clientConsts import getHudPlaneIcon, PREBATTLE_BOT_DIFFICULTY
from functools import partial
from encodings import utf_8
import time

class TrainingRoomVO:

    def __init__(self):
        """
        http://10.135.0.21:8090/display/Hammer/Rooms+List
        """
        self.roomID = -1
        self.nameArea = ''
        self.currentCountPlayers = -1
        self.currentCountUserPlayers = -1
        self.maxCountPlayers = -1
        self.descriptionArea = ''
        self.nameCommander = ''
        self.clanAbbrevCommander = ''
        self.time = ''
        self.gameMode = ''
        self.planeLevelFrom = 1
        self.planeLevelTo = 10
        self.fireMode = ''
        self.previewIcoPath = ''
        self.planeHidden = False
        self.buttonEnabled = True
        self.planeLevel = ''
        self.botDifficulties = [ BotDifficultyVO(d) for d in BOT_DIFFICULTY.ALL ]


class AccountVO:

    def __init__(self):
        self.id = -1
        self.name = ''
        self.clanAbbrev = ''
        self.blockType = -1
        self.status = -1
        self.teamID = -1
        self.planeID = -1
        self.planeLevel = ''
        self.planeName = ''
        self.planeIcoPath = ''
        self.isBot = False
        self.isMe = False
        self.difficulty = None
        self.difficultyIconPath = ''
        return


class BotDifficultyVO:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.iconPath = PREBATTLE_BOT_DIFFICULTY.ICON_PATH_MAP[difficulty]
        self.title = localizeLobby(PREBATTLE_BOT_DIFFICULTY.TITLE_MAP[difficulty])


class ItemVO:

    def __init__(self, mapID = -1, mapName = ''):
        self.id = mapID
        self.name = mapName


class RoomMapsVO:

    def __init__(self):
        self.mapID = 1
        self.mapName = 'Item'
        self.selectedIcoPath = 'icons/trainingListMaps/trainingIconMapElHalluf.png'
        self.unselectedIcoPath = 'icons/trainingListMaps/trainingIconMapElHallufDisabled.png'
        self.mapIcoPath = 'trainingsMapPreview/trainingsMapNovorossiysk.tga'
        self.mapDescription = 'Item description'


class RoomVO:

    def __init__(self):
        self.mapID = -1
        self.roomDescription = ''
        self.durationBattle = 15
        self.planeLevelFrom = 1
        self.planeLevelTo = 10
        self.gameModeID = 0
        self.fireTypeID = 0
        self.voiceChatID = 0
        self.invitationOnly = False
        self.playSingle = False


from itertools import ifilter

class BotVO:

    def __init__(self):
        self.planeID = -1
        self.planeLevel = 0
        self.planeName = ''
        self.planeIcoPath = ''
        self.planeType = 0
        self.isBot = True

    def __cmp__(self, other):
        return next(ifilter(None, (cmp(getattr(self, name), getattr(other, name)) for name in ('planeLevel', 'planeType', 'planeName'))), 0)


class TrainingRoomHelper:
    TIME_WAIT_ENTERING_TO_TRAINING_ROOM = 10

    class TrainingRoomUI:
        OUTSIDE = 0
        IN_LIST_ROOM = 1
        IN_CREATE_ROOM = 2
        IN_TRAINING_ROOM = 3

    def __init__(self, account):
        self.__account = account
        self.__roomSettings = {}
        self.__locationMap = {}
        for locationData in db.DBLogic.g_instance.getArenaList():
            self.__locationMap[locationData.typeID] = locationData.typeName

        self.__locationMap[-1] = 'map_undefined'
        self.__isCreator = False
        self.__playerASList = []
        self.__roomCreateActive = False
        self.__roomsListActive = False
        self.__lastRoomSearchFilters = {'mapID': consts.PREBATTLE_MAPID_UNDEFINED_FILTER,
         'gameModeID': GAME_MODE.UNDEFINED,
         'fireModeID': consts.PREBATTLE_FIRE_MODE_FILTER.UNDEFINED,
         'levelTypeID': consts.PREBATTLE_LEVELS_FILTER.ALL}
        from BWPersonality import g_lobbyCarouselHelper
        self.__lobbyCarouselHelper = g_lobbyCarouselHelper
        self.__roomTeamsActive = False
        self.__waitingID = None
        self.__roomList = []
        self.__waitCallBackEnterRoom = None
        self.positionInUI = self.TrainingRoomUI.OUTSIDE
        self.__roomSettings = {}
        self.__mapPreviewOpen = False
        self.planeLevel = None
        self.__forceCloseTime = 0
        self._WasResponseToEnterRoom = False
        self.__initFilterChain()
        player = BigWorld.player()
        from Account import PlayerAccount
        if player != None and player.__class__ == PlayerAccount:
            self.__entityID = player.id
        else:
            self.__entityID = None
        return

    def destroy(self):
        self.__account = None
        self.__lobbyCarouselHelper = None
        self.__cancel_waitCallBack()
        return

    def __initFilterChain(self):
        self._filterChain = messenger.filters.FilterChain()
        self._filterChain.addFilter('olFilter', messenger.filters.ObsceneLanguageFilter())
        self._filterChain.addFilter('domainFilter', messenger.filters.DomainNameFilter())
        self._filterChain.addFilter('spamFilter', messenger.filters.SpamFilter())

    def __cancel_waitCallBack(self):
        if self.__waitCallBackEnterRoom:
            BigWorld.cancelCallback(self.__waitCallBackEnterRoom)
        self.__waitCallBackEnterRoom = None
        return

    def __returnToHangar(self, additionalCheck = True, needCheckButton = True):
        self.__account.call_1('hangar.isCarouselEnabled', True)
        if needCheckButton:
            self.__lobbyCarouselHelper.updateInBattleButton(additionalCheck)

    def onInitialized(self):
        LOG_DEBUG('TrainingRoomHelper::onInitialized')
        self.__roomList = []
        self.__roomsListActive = True
        LOG_TRACE('onInitialized() disabling battle button')
        self.__account.call_1('hangar.isInBattleEnabled', False)
        self.__account.call_1('hangar.isCarouselEnabled', False)
        if self.__forceCloseTime and time.time() - self.__forceCloseTime < 0.1:
            self.forceLeaveRoom()
        self.setFilterRequest()
        self.onRefreshRoomList(consts.PREBATTLE_MAPID_UNDEFINED_FILTER, GAME_MODE.UNDEFINED, consts.PREBATTLE_FIRE_MODE_FILTER.UNDEFINED, consts.PREBATTLE_LEVELS_FILTER.ALL)
        self.__getAccountCmd().subscribeRoomList(consts.ARENA_TYPE.TRAINING)
        self.__cancel_waitCallBack()
        self.positionInUI = self.TrainingRoomUI.IN_LIST_ROOM

    def onCloseTrainingRoomList(self):
        LOG_DEBUG('onTrainingRoomListClose')
        self.__getAccountCmd().unSubscribeRoomList(consts.ARENA_TYPE.TRAINING)
        self.__returnToHangar(False, False)
        self.__roomsListActive = False
        self.positionInUI = self.TrainingRoomUI.OUTSIDE

    def onEnterTrainingRoom(self, roomID):
        LOG_DEBUG('onEnterTrainingRoom', roomID)
        if self.__forceCloseTime and time.time() - self.__forceCloseTime < 0.1:
            return
        else:
            self.__getAccountCmd().enterTrainingRoom(roomID)
            player = BigWorld.player()
            if not self.__waitCallBackEnterRoom:
                self._WasResponseToEnterRoom = False
                self.__waitCallBackEnterRoom = BigWorld.callback(self.TIME_WAIT_ENTERING_TO_TRAINING_ROOM, self.__WaitEnteringToTrainingRoom)
            if self.__waitingID is not None:
                Waiting.hide(self.__waitingID)
                self.__waitingID = None
            self.__waitingID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE')
            self.positionInUI = self.TrainingRoomUI.IN_TRAINING_ROOM
            return

    def __WaitEnteringToTrainingRoom(self):
        self.__waitCallBackEnterRoom = None
        if not self._WasResponseToEnterRoom:
            if self.__waitingID is not None:
                Waiting.hide(self.__waitingID)
                self.__waitingID = None
            self.__getAccountCmd().leaveTrainingRoom()
            self.forceLeaveRoom()
            self.__ShowErrorMessageBox(TRAINING_ROOM_REASON.ERROR_MESSAGE[TRAINING_ROOM_REASON.ROOM_DELETED])
        return

    def onRefreshRoomList(self, mapID, gameModeID, fireModeID, levelTypeID):
        LOG_DEBUG('onTrainingRoomListRequest', mapID, gameModeID, fireModeID, levelTypeID)
        self.__lastRoomSearchFilters = {'mapID': mapID,
         'gameModeID': gameModeID,
         'fireModeID': fireModeID,
         'levelTypeID': levelTypeID}
        self.__getAccountCmd().refreshRoomList(mapID, gameModeID, fireModeID, levelTypeID)
        self.positionInUI = self.TrainingRoomUI.IN_LIST_ROOM

    def refreshRoomListForChangePlane(self, planeID, planeLevel):
        """
        Refresh training list room, button enable for change plane on client before server send new list options
        This is client fix for pause from change plane and button enable for training room
        :type planeLevel: int
        :param planeLevel: plane level
        :return: :rtype:
        """
        self.planeLevel = planeLevel
        self.planeID = planeID
        if not self.__roomList:
            return
        if self.__roomsListActive and not self.__roomCreateActive and self.positionInUI == TrainingRoomHelper.TrainingRoomUI.IN_LIST_ROOM:
            updateRooms = [ self.__convertRoomMapToVO(room) for room in self.__roomList ]
            try:
                self.__account.call_1('trainingRoomsList.UpdateRooms', updateRooms)
            except:
                LOG_WARNING('TrainingRoomHelper:refreshRoomListForChangePlane trainingRoomsList.UpdateRooms not found!')

    def refreshRoomListResponse(self, roomList):
        LOG_DEBUG('TrainingRoomHelper::refreshRoomListResponse', roomList)
        oldRoomDict = dict(((room['roomID'], room) for room in self.__roomList))
        newRoomDict = dict(((room['roomID'], room) for room in roomList))
        toAddRoomIDs = set(newRoomDict).difference(oldRoomDict)
        toRemoveRoomIDs = set(oldRoomDict).difference(newRoomDict)
        toUpdateRoomIDs = set()
        for roomID, room in newRoomDict.iteritems():
            if roomID in oldRoomDict:
                for k, v in room.items():
                    if oldRoomDict[roomID][k] != v:
                        toUpdateRoomIDs.add(roomID)
                        break

        if self.__roomsListActive and not self.__roomCreateActive:
            if toRemoveRoomIDs:
                self.__account.call_1('trainingRoomsList.RemoveRoomIDs', list(toRemoveRoomIDs))
            if toAddRoomIDs:
                addRooms = [ self.__convertRoomMapToVO(newRoomDict[roomID]) for roomID in toAddRoomIDs ]
                self.__account.call_1('trainingRoomsList.AddRooms', addRooms)
            if toUpdateRoomIDs:
                updateRooms = [ self.__convertRoomMapToVO(newRoomDict[roomID]) for roomID in toUpdateRoomIDs ]
                self.__account.call_1('trainingRoomsList.UpdateRooms', updateRooms)
        self.__roomList = roomList

    def setFilterRequest(self):
        LOG_DEBUG('setFilterRequest')
        self.__getAccountCmd().getTrainingRoomFilters(self.__setFiltersResponse)

    def __setFiltersResponse(self, operation, resultID, *args):
        """
        @type operation: ReceivedOperation
        @param resultID:
        @param args:
        @return:
        """
        LOG_DEBUG('__setFiltersResponse: ', 'invocationId ', operation.invocationId, ' resultID ', resultID, ' data ', args)
        self.__filtersMap = args[0]
        self.__setLocalizedFilters(self.__filtersMap)

    def __getAccountCmd(self):
        player = BigWorld.player()
        from Account import PlayerAccount
        if player != None and player.__class__ == PlayerAccount:
            return player.accountCmd
        else:
            LOG_ERROR('TrainingRoomHelper::__getAccountCmd. Player =', player)
            return
            return

    def __convertRoomMapToVO(self, roomMap):
        """
        convert to flash struct
        :param roomMap: struct information about room
        :param planeLevel: None - response from server, planeLevel - from client for set button enable
        :return: result for flash :rtype: TrainingRoomVO
        """
        planeLevel = self.planeLevel
        roomVO = TrainingRoomVO()
        roomVO.roomID = roomMap['roomID']
        roomVO.currentCountPlayers = roomMap['currentCountPlayers']
        roomVO.maxCountPlayers = roomMap['maxCountPlayers']
        roomVO.nameCommander = roomMap['nameCommander']
        roomVO.clanAbbrevCommander = roomMap['clanAbbrevCommander']
        roomVO.time = roomMap['time'] / 60
        roomVO.gameMode = localizeHUD(consts.PREBATTLE_GAMEMODES_FILTER_MAP.get(roomMap['gameMode']))
        if planeLevel is None:
            roomVO.buttonEnabled = roomMap['enterButtonEnabled']
        else:
            roomVO.buttonEnabled = roomMap['planeLevelFrom'] <= planeLevel <= roomMap['planeLevelTo']
        planeLevelFrom = localizeHUD(consts.PREBATTLE_PLANES_LEVELS.PREBATTLE_PLANES_LEVELS_MAP.get(roomMap['planeLevelFrom']))
        planeLevelTo = localizeHUD(consts.PREBATTLE_PLANES_LEVELS.PREBATTLE_PLANES_LEVELS_MAP.get(roomMap['planeLevelTo']))
        roomVO.planeLevel = planeLevelFrom + ' - ' + planeLevelTo
        RoomVO.planeLevelFrom = roomMap['planeLevelFrom']
        RoomVO.planeLevelTo = roomMap['planeLevelTo']
        RoomVO.planeHidden = roomMap['planeHidden']
        roomVO.fireMode = localizeLobby(consts.PREBATTLE_FIRE_MODE_FILTER.PREBATTLE_FIRE_MODE_FILTER_MAP.get(roomMap['fireMode']))
        arenaData = db.DBLogic.g_instance.getArenaData(roomMap['mapID'])
        roomVO.nameArea = localizeMap(self.__locationMap[roomMap['mapID']].upper())
        roomVO.descriptionArea = roomMap['roomDescription']
        roomVO.previewIcoPath = arenaData.trainingRoomIcoPathSelected
        return roomVO

    def onRoomCreateInitialized(self):
        LOG_DEBUG('onRoomCreateInitialized')
        self.__getAccountCmd().getTrainingCreateRoomFilters(self.__setCreateRoomFiltersResponse)
        LOG_TRACE('onRoomCreateInitialized() disabling battle button')
        self.__account.call_1('hangar.isInBattleEnabled', False)
        self.__roomCreateActive = True

    def updatePrebattleCreateRoomAvailableFilters(self):
        if self.__roomCreateActive == True:
            self.onRoomCreateInitialized()
        elif self.__roomsListActive == True:
            self.onRefreshRoomList(self.__lastRoomSearchFilters['mapID'], self.__lastRoomSearchFilters['gameModeID'], self.__lastRoomSearchFilters['fireModeID'], self.__lastRoomSearchFilters['levelTypeID'])

    def __setCreateRoomFiltersResponse(self, operation, resultID, *args):
        LOG_DEBUG('__setCreateRoomFiltersResponse', resultID, *args)
        if self.__roomCreateActive:
            self.__createRoomAvailableParams = args[0]
            self.__setLocalizedCreateRoomSettings(self.__createRoomAvailableParams)

    def onRoomCreateContinue(self, roomVO):
        if messenger.g_xmppChatHandler:
            from messenger.XmppChat import ChannelType
            chatJid, chatPass = messenger.g_xmppChatHandler.createChannel(ChannelType.TRAINING)
        roomDescription = self._filterChain.chainIn(convertToLocal(roomVO.roomDescription), 0, BigWorld.time())
        roomDescription = utf_8.encode(roomDescription)[0]
        roomData = {'mapID': roomVO.mapID,
         'roomDescription': roomDescription[:consts.TRAINING_ROOM_CREATE_DESCRIPTION_LIMIT],
         'durationBattle': roomVO.durationBattle,
         'planeLevelFrom': roomVO.planeLevelFrom,
         'planeLevelTo': roomVO.planeLevelTo,
         'chatJid': chatJid,
         'chatPass': chatPass,
         'planeHidden': roomVO.planeHidden}
        LOG_DEBUG('onRoomCreateContinue', roomData)
        self.__getAccountCmd().getTrainingCreateRoomCreated(roomData)
        self.positionInUI = self.TrainingRoomUI.IN_CREATE_ROOM
        self.__roomSettings['chatJid'] = chatJid
        self.__roomSettings['chatPass'] = chatPass

    def onRoomTeamsInitialized(self):
        LOG_DEBUG('onRoomTeamsInitialized')
        self.__roomTeamsActive = True
        self.__account.call_1('hangar.isCarouselEnabled', False)
        player = BigWorld.player()
        self.__getAccountCmd().getInitDataOnEnterToTrainingRoom()
        self.__getAccountCmd().getTrainingRoomFilters(self.__setFiltersResponseTeamRoom)
        self.positionInUI = self.TrainingRoomUI.IN_TRAINING_ROOM
        if not self.__waitCallBackEnterRoom:
            self._WasResponseToEnterRoom = False
            self.__waitCallBackEnterRoom = BigWorld.callback(self.TIME_WAIT_ENTERING_TO_TRAINING_ROOM, self.__WaitEnteringToTrainingRoom)

    def __setFiltersResponseTeamRoom(self, operation, resultID, *args):
        """
        @type operation: ReceivedOperation
        @param resultID:
        @param args:
        @return:
        """
        LOG_DEBUG('__setFiltersResponseTeamRoom: ', 'invocationId ', operation.invocationId, ' resultID ', resultID, ' data ', args)
        self.__filtersMap = args[0]
        if self.__roomTeamsActive:
            self.__setLocalizedFilters(self.__filtersMap, inRoom=True)

    def updateTrainingRoom(self, initDataMap):
        LOG_DEBUG('updateTrainingRoom')
        if self.__roomTeamsActive:
            self.__isCreator = initDataMap['isCreator']
            self.__account.call_1('trainingsRoomTeams.isCreator', initDataMap['ownAccountID'], initDataMap['isCreator'], self.__isCreator)
            botsList = map(self.__convertAirplaneIdToVO, filter(lambda planeID: db.DBLogic.g_instance.isPlaneBotAcceptable(planeID) and db.DBLogic.g_instance.getPlaneLevelByID(planeID) >= initDataMap['roomSettings']['planeLevelFrom'] and db.DBLogic.g_instance.getPlaneLevelByID(planeID) <= initDataMap['roomSettings']['planeLevelTo'], db.DBLogic.g_instance._db__aircrafts))
            botsList.sort()
            self.__account.call_1('trainingsRoomTeams.setInfoBots', botsList)
            self.__roomSettings = initDataMap['roomSettings']
            mapChanged = hasattr(self, '_TrainingRoomHelper__roomMapID') and self.__roomMapID != self.__roomSettings.get('mapID', None)
            self.__roomMapID = self.__roomSettings['mapID']
            if self.__isCreator:
                self.__account.call_1('trainingsRoomTeams.setBotAmount', self.__roomSettings['maxBotsInTeam'])
            self.__setLocalizedRoomSettings(self.__roomSettings)
            self.__setLocalizedRoomPlayersList(initDataMap['playersList'], initDataMap['time'])
            LOG_DEBUG('self.__lobbyCarouselHelper.updateInBattleButton', self.__isCreator, self.__checkIsPlayerInTwoTeams())
            self.__lobbyCarouselHelper.updateInBattleButton(self.__isCreator and self.__checkIsPlayerInTwoTeams())
            self._WasResponseToEnterRoom = True
            if mapChanged and self.__mapPreviewOpen:
                self.onRoomPreviewInitialized()
            chatJid = self.__roomSettings.get('chatJid')
            chatPass = self.__roomSettings.get('chatPass')
            if chatJid and messenger.g_xmppChatHandler:
                messenger.g_xmppChatHandler.joinChannel(chatJid, chatPass)
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        self.__cancel_waitCallBack()
        self.positionInUI = self.TrainingRoomUI.IN_TRAINING_ROOM
        return

    def __setLocalizedCreateRoomSettings(self, createRoomAvailableParams):
        mapASList = []
        for mapID in createRoomAvailableParams['mapFilters']:
            map = self.__locationMap.get(mapID, None)
            if map:
                roomMapVO = RoomMapsVO()
                roomMapVO.mapID = mapID
                arenaData = db.DBLogic.g_instance.getArenaData(mapID)
                roomMapVO.mapName = localizeMap(self.__locationMap[mapID])
                roomMapVO.mapDescription = localizeMap(arenaData.trainingRoomDescription)
                roomMapVO.mapIcoPath = arenaData.trainingRoomIcoPathPreviewBig
                roomMapVO.selectedIcoPath = arenaData.trainingRoomIcoPathSelected
                roomMapVO.unselectedIcoPath = arenaData.trainingRoomIcoPathUnselected
                mapASList.append(roomMapVO)

        LOG_DEBUG('trainingsRoomCreating.setRoomMaps', mapASList)
        self.__account.call_1('trainingsRoomCreating.setRoomMaps', mapASList)
        planesLevelsFrom = []
        for planeLevelFrom in createRoomAvailableParams['planesLevelsFrom']:
            levelFromVO = ItemVO()
            levelFromVO.name = consts.PREBATTLE_PLANES_LEVELS.PREBATTLE_PLANES_LEVELS_MAP.get(planeLevelFrom)
            levelFromVO.id = planeLevelFrom
            planesLevelsFrom.append(levelFromVO)

        LOG_DEBUG('trainingsRoomCreating.setPlaneLevelsFrom', planesLevelsFrom)
        self.__account.call_1('trainingsRoomCreating.setPlaneLevelsFrom', planesLevelsFrom)
        planesLevelsTo = []
        for planesLevelTo in createRoomAvailableParams['planesLevelsTo']:
            levelToVO = ItemVO()
            levelToVO.name = consts.PREBATTLE_PLANES_LEVELS.PREBATTLE_PLANES_LEVELS_MAP.get(planesLevelTo)
            levelToVO.id = planesLevelTo
            planesLevelsTo.append(levelToVO)

        LOG_DEBUG('trainingsRoomCreating.setPlaneLevelsTo', planesLevelsTo)
        self.__account.call_1('trainingsRoomCreating.setPlaneLevelsTo', planesLevelsTo)
        battleDurations = []
        for battleDuration in createRoomAvailableParams['durationBattle']:
            durationVO = ItemVO()
            durationVO.name = localizeLobby(consts.BATTLE_DURATIONS.BATTLE_DURATIONS_MAP.get(battleDuration))
            durationVO.id = battleDuration
            battleDurations.append(durationVO)

        LOG_DEBUG('trainingsRoomCreating.setDurationBattle', battleDurations)
        self.__account.call_1('trainingsRoomCreating.setDurationBattle', battleDurations)
        return

    def __setLocalizedRoomSettings(self, roomSettings):
        if self.__roomTeamsActive:
            curMap = self.__locationMap.get(self.__roomMapID, None)
            if curMap:
                arenaData = db.DBLogic.g_instance.getArenaData(self.__roomMapID)
                roomVO = TrainingRoomVO()
                roomVO.roomID = roomSettings['roomID']
                roomVO.roomDescription = roomSettings['roomDescription']
                roomVO.mapName = localizeMap(curMap)
                roomVO.mapPreviewIcoPath = arenaData.trainingRoomIcoPathSelected
                roomVO.nameCommander = roomSettings['nameCommander']
                roomVO.clanAbbrevCommander = roomSettings['clanAbbrevCommander']
                roomVO.time = roomSettings['durationTime'] / 60
                roomVO.gameMode = localizeHUD(consts.PREBATTLE_GAMEMODES_FILTER_MAP.get(roomSettings['gameMode']))
                planeLevelFrom = localizeHUD(consts.PREBATTLE_PLANES_LEVELS.PREBATTLE_PLANES_LEVELS_MAP.get(roomSettings['planeLevelFrom']))
                planeLevelTo = localizeHUD(consts.PREBATTLE_PLANES_LEVELS.PREBATTLE_PLANES_LEVELS_MAP.get(roomSettings['planeLevelTo']))
                roomVO.planeLevel = planeLevelFrom + ' - ' + planeLevelTo
                roomVO.planeLevelFrom = roomSettings['planeLevelFrom']
                roomVO.planeLevelTo = roomSettings['planeLevelTo']
                roomVO.fireMode = localizeLobby(consts.PREBATTLE_FIRE_MODE_FILTER.PREBATTLE_FIRE_MODE_FILTER_MAP.get(roomSettings['fireMode']))
                self.__account.call_1('trainingsRoomTeams.updateRoomData', roomVO)
        return

    def __setLocalizedRoomPlayersList(self, playerList, responseTime):
        if self.__roomTeamsActive:
            self.__playerASList = []
            for playerMap in playerList:
                accountVO = self.__convertAccountMapToVO(playerMap, responseTime)
                self.__playerASList.append(accountVO)

            LOG_DEBUG('trainingsRoomTeams.updateAccounts', self.__playerASList)
            self.__account.call_1('trainingsRoomTeams.updateAccounts', self.__playerASList)

    def __setLocalizedFilters(self, filtersMap, inRoom = False):
        if self.__roomsListActive or inRoom:
            mapASList = []
            for mapID in filtersMap['mapFilters']:
                map = self.__locationMap.get(mapID, None)
                if map:
                    mapVO = ItemVO(mapID, localizeMap(map))
                    mapASList.append(mapVO)
                else:
                    LOG_ERROR('You are trying to add map which is not present in client list.xml. Looks like you need to sync it with server')

            if inRoom:
                self.__account.call_1('trainingsRoomTeams.setAreaNames', mapASList)
            else:
                self.__account.call_1('trainingRoomsList.setAreaNames', mapASList)
            if not inRoom:
                fireModeASList = []
                for fireMode in filtersMap['fireModeFilters']:
                    localizedText = localizeLobby(consts.PREBATTLE_FIRE_MODE_FILTER.PREBATTLE_FIRE_MODE_FILTER_MAP.get(fireMode))
                    fireModeVO = ItemVO(fireMode, localizedText)
                    fireModeASList.append(fireModeVO)

                self.__account.call_1('trainingRoomsList.setFireModes', fireModeASList)
                gameModeASList = []
                for gameMode in filtersMap['gameModeFilters']:
                    localizedText = localizeLobby(consts.PREBATTLE_GAMEMODES_FILTER_MAP.get(gameMode))
                    gameModeVO = ItemVO(gameMode, localizedText)
                    gameModeASList.append(gameModeVO)

                self.__account.call_1('trainingRoomsList.setGameModes', gameModeASList)
            levelASList = []
            for levelType in filtersMap['planeLevelFilters']:
                localizedText = localizeLobby(consts.PREBATTLE_LEVELS_FILTER.PREBATTLE_LEVELS_FILTER_MAP.get(levelType))
                levelTypeVO = ItemVO(levelType, localizedText)
                levelASList.append(levelTypeVO)

            if inRoom:
                self.__account.call_1('trainingsRoomTeams.setPlaneLevels', levelASList)
            else:
                self.__account.call_1('trainingRoomsList.setPlaneLevels', levelASList)
        return

    def __setLocalizedRoomList(self, roomList):
        if self.__roomsListActive:
            roomASList = [ self.__convertRoomMapToVO(roomMap) for roomMap in roomList ]
            LOG_DEBUG('trainingRoomsList.RefreshRoomListResponse', roomASList)
            self.__account.call_1('trainingRoomsList.RefreshRoomListResponse', roomASList)

    def onRoomTeamUpdateAccountTeamID(self, accountID, teamID):
        LOG_DEBUG('onRoomTeamUpdateAccountTeamID', accountID, teamID)
        self.__getAccountCmd().updateAccountTeamID(accountID, teamID)

    def onRoomTeamAddBots(self, botsCount, teamID, botsPlaneID, difficulty, level, fillType, planeType, planeNation):
        """
        Adds bots
        :param botsCount:
        :param teamID:
        :param botsPlaneID:
        :param difficulty: const from consts.BOT_DIFFICULTY
        :param level:
        :param fillType: const from consts.BOTS_AUTOFILL
        """
        if botsCount > 0:
            if self.__waitingID is not None:
                Waiting.hide(self.__waitingID)
                self.__waitingID = None
            self.__waitingID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE')
            self.__getAccountCmd().addBots(botsCount, int(botsPlaneID), teamID, difficulty, level, fillType, planeType, planeNation)
        else:
            LOG_ERROR('onRoomTeamAddBots, botsCount = {0}'.format(botsCount))
        return

    def editBot(self, botID, planeID, difficulty, level, planeType, planeNation):
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        self.__waitingID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE')
        self.__getAccountCmd().trainingEditBot(botID, planeID, difficulty, level, planeType, planeNation)
        return

    def swapTeams(self):
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        self.__waitingID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE')
        self.__getAccountCmd().trainingSwapTeams()
        return

    def moveTeam(self, origTeamID, destTeamID):
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        self.__waitingID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE')
        self.__getAccountCmd().trainingMoveTeam(origTeamID, destTeamID)
        return

    def onRoomTeamBotsAutoFill(self):
        self.__cancel_waitCallBack()
        self.__waitCallBackEnterRoom = BigWorld.callback(5, self.__waitingBotsAutoFill)
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        self.__waitingID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE')
        self.__getAccountCmd().botsAutoFill()
        return

    def onRoomTeamBotsRemove(self):
        self.__cancel_waitCallBack()
        self.__waitCallBackEnterRoom = BigWorld.callback(1, self.__waitingBotsAutoFill)
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        self.__waitingID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE')
        self.__getAccountCmd().botsRemove()
        return

    def onRoomTeamDeleteBot(self, botID):
        self.__getAccountCmd().deleteBot(botID)

    def updateRoomTeamAccount(self, accountMap):
        self._WasResponseToEnterRoom = True
        if self.__roomTeamsActive:
            accountVO = self.__convertAccountMapToVO(accountMap, accountMap['time'])
            isPlaneFound = False
            for player in self.__playerASList:
                if accountVO.id == player.id:
                    player.teamID = accountVO.teamID
                    player.blockType = accountVO.blockType
                    player.status = accountVO.status
                    isPlaneFound = True
                    break

            if not isPlaneFound:
                self.__playerASList.append(accountVO)
            self.__lobbyCarouselHelper.updateInBattleButton(self.__isCreator and self.__checkIsPlayerInTwoTeams())
            LOG_DEBUG('trainingsRoomTeams.updateAccount', accountVO.planeID, accountVO.teamID, accountVO)
            self.__account.call_1('trainingsRoomTeams.updateAccount', accountVO)
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        self.__cancel_waitCallBack()
        return

    def __waitingBotsAutoFill(self):
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        self.__cancel_waitCallBack()
        return

    def onChangeMap(self, mapID):
        self.__getAccountCmd().changeMap(mapID)

    def onChangeDescription(self, txtDescription):
        roomDescription = self._filterChain.chainIn(convertToLocal(txtDescription), 0, BigWorld.time())
        roomDescription = utf_8.encode(roomDescription)[0]
        self.__getAccountCmd().changeDescription(roomDescription[:consts.TRAINING_ROOM_CREATE_DESCRIPTION_LIMIT])

    def __convertAccountMapToVO(self, accountMap, responseTime):
        accountVO = AccountVO()
        accountVO.id = accountMap['id']
        accountVO.name = accountMap['name']
        accountVO.clanAbbrev = accountMap['clanAbbrev']
        accountVO.blockType = accountMap['blockType']
        accountVO.status = accountMap['status']
        accountVO.teamID = accountMap['teamID']
        accountVO.isBot = accountMap['isBot']
        accountVO.isMe = False if self.__entityID is None else accountMap['id'] == self.__entityID
        accountVO.difficulty = accountMap['difficulty']
        accountVO.difficultyIconPath = PREBATTLE_BOT_DIFFICULTY.ICON_PATH_MAP.get(accountVO.difficulty, '')
        if accountVO.isBot:
            if accountMap['planeID'] != -1:
                accountVO.name = getBotName(accountVO.name, accountMap['planeID'], None)
            else:
                accountVO.name = getBotName(accountVO.name, None, accountMap['planeCountry'])
        selectedAirplane = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
        currentPlaneID = selectedAirplane.planeID if selectedAirplane else -1
        if accountVO.isMe and accountVO.teamID and accountMap['planeID'] != -1:
            if accountMap['planeID'] != currentPlaneID:
                BigWorld.callback(1, partial(self.__lobbyCarouselHelper.onSelectedPlaneID, accountMap['planeID']))
                self.__account.call_1('hangar.setSelectedAircraftID', accountMap['planeID'])
        accountVO.planeID = currentPlaneID if accountMap['planeID'] == -1 and accountVO.isMe else accountMap['planeID']
        if accountVO.planeID != UNDEFINED_PLANE:
            planeSettings = db.DBLogic.g_instance.getAircraftData(accountVO.planeID).airplane
            accountVO.planeLevel = planeSettings.level
            accountVO.planeName = localizeAirplane(planeSettings.name)
            accountVO.planeIcoPath = planeSettings.hudIcoPath
            accountVO.planeTypeIcoPath = getHudPlaneIcon(planeSettings.planeType)
            accountVO.planeType = planeSettings.planeType
        return accountVO

    def __convertAirplaneIdToVO(self, planeID):
        botVO = BotVO()
        botVO.planeID = planeID
        planeSettings = db.DBLogic.g_instance.getAircraftData(planeID).airplane
        botVO.planeLevel = planeSettings.level
        botVO.planeType = planeSettings.planeType
        botVO.planeName = localizeAirplane(planeSettings.name)
        botVO.planeIcoPath = planeSettings.hudIcoPath
        botVO.planeTypeIcoPath = getHudPlaneIcon(planeSettings.planeType)
        return botVO

    def onCloseTrainingTeams(self):
        self.__roomTeamsActive = False
        if self.positionInUI == self.TrainingRoomUI.IN_TRAINING_ROOM:
            self.__getAccountCmd().leaveTrainingRoom()
        self.__closeChatChannel()
        self.__returnToHangar(False, False)
        self.__cancel_waitCallBack()
        self.positionInUI = self.TrainingRoomUI.IN_LIST_ROOM

    def removeRoomTeamAccount(self, accountID):
        if self.__roomTeamsActive:
            LOG_DEBUG('trainingsRoomTeams.removeAccount', accountID)
            for player in self.__playerASList:
                if accountID == player.id:
                    self.__playerASList.remove(player)

            self.__lobbyCarouselHelper.updateInBattleButton(self.__isCreator and self.__checkIsPlayerInTwoTeams())
            self.__account.call_1('trainingsRoomTeams.removeAccount', accountID)

    def forceLeaveRoom(self):
        self._WasResponseToEnterRoom = True
        self.positionInUI = self.TrainingRoomUI.IN_LIST_ROOM
        if self.__roomTeamsActive:
            LOG_DEBUG('trainingsRoomTeams.forceClose')
            self.__forceCloseTime = 0
            self.__account.call_1('trainingsRoomTeams.forceClose')
        else:
            self.__forceCloseTime = time.time()
        self.__closeChatChannel()
        self.__cancel_waitCallBack()

    def leaveRoomWithReason(self, reasonID):
        LOG_DEBUG('trainingsRoomTeams.leaveRoomWithReason with errorID={0} msg={1}'.format(reasonID, TRAINING_ROOM_REASON.ERROR_MESSAGE[reasonID]))
        self.positionInUI = self.TrainingRoomUI.IN_LIST_ROOM
        self.__account.call_1('trainingsRoomTeams.forceClose')
        self.__ShowErrorMessageBox(TRAINING_ROOM_REASON.ERROR_MESSAGE[reasonID])
        self._WasResponseToEnterRoom = True
        self.__closeChatChannel()
        self.__cancel_waitCallBack()

    def __ShowErrorMessageBox(self, error_msg):
        if self.__waitingID is not None:
            Waiting.hide(self.__waitingID)
            self.__waitingID = None
        _error_local = localizeLobby(error_msg)
        self.__account.call_1('hangar.showErrorMessage', _error_local)
        LOG_DEBUG('__ShowErrorMessageBox: {0} / {1}'.format(error_msg, _error_local))
        return

    def onRoomPreviewInitialized(self):
        self.__mapPreviewOpen = True
        if hasattr(self, '_TrainingRoomHelper__roomMapID'):
            self.__setLocalizedMapPreview(self.__roomMapID)

    def onRoomPreviewClosed(self):
        self.__mapPreviewOpen = False

    def __setLocalizedMapPreview(self, roomMapID):
        arenaData = db.DBLogic.g_instance.getArenaData(roomMapID)
        self.__account.call_1('trainingsRoomPreview.updateMapData', arenaData.trainingRoomIcoPathPreview, localizeMap(arenaData.trainingRoomDescription))

    def onTrainingRoomLeave(self):
        self.__returnToHangar(True)
        self.positionInUI = self.TrainingRoomUI.OUTSIDE

    def onRoomCreateClose(self):
        self.__returnToHangar(False)
        self.__roomCreateActive = False

    def __checkIsPlayerInTwoTeams(self):
        teamsFlag = set()
        for player in self.__playerASList:
            if player.id == BigWorld.player().id and player.teamID == consts.TEAM_ID.UNDEFINED:
                return False
            if player.teamID != consts.TEAM_ID.UNDEFINED:
                if player.status != PREBATLE_ACCOUNT_STATUS.READY:
                    return False
                teamsFlag.add(player.teamID)

        return len(teamsFlag) == 2

    def isReadyToButtleForCreator(self):
        return self.__isCreator and self.__checkIsPlayerInTwoTeams()

    def __closeChatChannel(self):
        chatJid = self.__roomSettings.get('chatJid')
        if chatJid and messenger.g_xmppChatHandler:
            if self.__isCreator:
                messenger.g_xmppChatHandler.deleteChannel(chatJid)
            else:
                messenger.g_xmppChatHandler.leaveChannel(chatJid)