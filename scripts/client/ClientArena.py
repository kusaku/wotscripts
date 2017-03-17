# Embedded file name: scripts/client/ClientArena.py
import BigWorld
from GameServiceBase import GameServiceBase
import Math
import ResMgr
import wgPickle
import Event
from debug_utils import *
from consts import *
import consts
import ClientLog
from EntityHelpers import EntitySupportedClasses, buildAndGetWeaponsInfo, translateDictThroughAnother, AvatarFlags
import db.DBLogic
from DestructibleObjectFactory import DestructibleObjectFactory
from DictKeys import NEW_AVATARS_INFO_KEYS_INVERT_DICT, REPORT_BATTLE_RESULT_KEYS_INVERT_DICT
from Descriptors import getTeamObjectDescriptorFromCompactDescriptor
from _airplanesConfigurations_db import getAirplaneConfiguration, airplanesConfigurations
from ObjectsStrategies import selectTeamObjectStrategy
import VOIP
from Helpers.namesHelper import getBotName
import StaticModels
from Helpers.i18n import localizePilot, localizeAirplane, localizeBotChat
from adapters.ICrewMemberAdapter import CONTRY_PO_FILE_WRAPPER, FIRST_NAME_MSG_ID, CONTRY_MSG_ID_WRAPPER
import random
from config_consts import IS_DEVELOPMENT
import Helpers.BotChatHelper as BotChatHelper
from db.DBParts import buildPartsMapByPartName

class ClientArena(GameServiceBase):
    __onUpdate = {ARENA_UPDATE.RECEIVE_TEXT_MESSAGE: '_ClientArena__onReceiveTextMessage',
     ARENA_UPDATE.RECEIVE_MARKER_MESSAGE: '_ClientArena__onReceiveMarkerMessage',
     ARENA_UPDATE.VEHICLE_KILLED: '_ClientArena__onVehicleKilled',
     ARENA_UPDATE.TEAM_OBJECT_DESTROYED: '_ClientArena__onTeamObjectDestruction',
     ARENA_UPDATE.TEAM_DOMINATION_PRC: '_ClientArena__onUpdateDominationPrc',
     ARENA_UPDATE.BASE_IS_UNDER_ATTACK: '_ClientArena__onBaseIsUnderAttack',
     ARENA_UPDATE.PLAYER_STATS: '_ClientArena__onUpdatePlayerStats',
     ARENA_UPDATE.RECEIVE_ALL_TEAM_OBJECTS_DATA: '_ClientArena__onReceiveAllTeamObjectsData',
     ARENA_UPDATE.RECEIVE_NEW_AVATARS_INFO: '_ClientArena__onNewAvatarsInfo',
     ARENA_UPDATE.TEAM_SUPERIORITY_POINTS: '_ClientArena__onUpdateTeamSuperiorityPoints',
     ARENA_UPDATE.REPORT_BATTLE_RESULT: '_ClientArena__onReportBattleResult',
     ARENA_UPDATE.RECEIVE_VOIP_CHANNEL_CREDENTIALS: '_ClientArena__onReceiveVOIPChannelCredentials',
     ARENA_UPDATE.TURRET_BOOSTER_DESTROYED: '_ClientArena__onReceiveTurretBoosterInfo',
     ARENA_UPDATE.GAME_RESULT_CHANGED: '_ClientArena__onGameResultChanged',
     ARENA_UPDATE.RECEIVE_LAUNCH: '_ClientArena__onReceiveLaunch',
     ARENA_UPDATE.GAIN_AWARD: '_ClientArena__onGainAward',
     ARENA_UPDATE.TEAM_OBJECT_PARTGROUP_DESTROYED: '_ClientArena__onTeamObjectPartGroupDestroyed',
     ARENA_UPDATE.SCENARIO_ICON: '_ClientArena__onScenarioSetIcon',
     ARENA_UPDATE.SCENARIO_TEXT: '_ClientArena__onScenarioSetText',
     ARENA_UPDATE.UPDATE_OBJECTS_DATA: '_ClientArena__onUpdateObjectsData',
     ARENA_UPDATE.UPDATE_DEBUG_INFO: '_ClientArena__onDebugInfoReceived',
     ARENA_UPDATE.RECEIVE_BATTLE_MESSAGE_REACTION_RESULT: '_ClientArena__onReceiveBattleMessageReactionResult'}

    def __init__(self):
        super(ClientArena, self).__init__()
        self.__sortedAvatarsIDs = dict()
        self.__avatarsDataReceived = False
        from gui.AlwaysVisibleObjects import AlwaysVisibleObjects
        self.__alwaysVisibleObjects = AlwaysVisibleObjects()
        self.__allObjectsData = {}
        self.__scenarioObjectMap = {}
        self.dominationPrc = [0, 0]
        self.superiorityPoints = [0, 0]
        self.avatarInfos = {}
        self.__eventManager = Event.EventManager()
        self.__ownerID = BigWorld.player().id
        self.avatarModelLoaded = 0
        self.__lastUpdateFunctionIndex = 0
        self.__waitingUpdateFunctionsPool = {}
        self.arenaData = None
        self.battleType = None
        self.__isBattleUILoaded = False
        em = self.__eventManager
        self.onReceiveTextMessage = Event.Event(em)
        self.onReceiveMarkerMessage = Event.Event(em)
        self.onVehicleKilled = Event.Event(em)
        self.onGainAward = Event.Event(em)
        self.onUpdateDominationPrc = Event.Event(em)
        self.onBaseIsUnderAttack = Event.Event(em)
        self.onNewAvatarsInfo = Event.Event(em)
        self.onUpdatePlayerStats = Event.Event(em)
        self.onApplyArenaData = Event.Event(em)
        self.onReceiveAllTeamObjectsData = Event.Event(em)
        self.onUpdateTeamSuperiorityPoints = Event.Event(em)
        self.onReportBattleResult = Event.Event(em)
        self.onReceiveVOIPChannelCredentials = Event.Event(em)
        self.onTeamObjectDestruction = Event.Event(em)
        self.onRecreateAvatar = Event.Event(em)
        self.onGameResultChanged = Event.Event(em)
        self.onUpdateTurretBoosterInfo = Event.Event(em)
        self.onAllServerDataReceived = Event.Event(em)
        self.onLaunch = Event.Event(em)
        self.onTeamObjectPartGroupChanged = Event.Event(em)
        self.onScenarioSetIcon = Event.Event(em)
        self.onScenarioSetText = Event.Event(em)
        self.onBattleMessageReactionResult = Event.Event(em)
        return

    def __callUpdateFunction(self, updateFunctionID, argStr):
        delegateName = self.__onUpdate.get(updateFunctionID, None)
        if delegateName is not None:
            getattr(self, delegateName)(argStr)
            return True
        else:
            return False

    def update(self, updateFunctionID, argStr):
        self.__callUpdateFunction(updateFunctionID, argStr)

    def doLeaveWorld(self):
        self.__isBattleUILoaded = False
        self.__eventManager.clear()
        for avatarInfo in self.avatarInfos.values():
            self.__destroyObjectControllers(avatarInfo)

        for objData in self.__allObjectsData.itervalues():
            self.__destroyObjectControllers(objData)

        VOIP.api().unsubscribeMemberStateObserversByType(consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.ARENA_HUD)

    def findIDsByPlayerName(self, name):
        return [ id for id, avatarInfo in self.avatarInfos.items() if avatarInfo.has_key('playerName') and name == avatarInfo['playerName'] ]

    def getAvatarIdByDBId(self, dbId):
        """for Vivox id maping"""
        return next((info.get('avatarID') for info in self.avatarInfos.itervalues() if info.get('databaseID') == dbId), None)

    def getDBId(self, avatarID):
        return next((info.get('databaseID') for info in self.avatarInfos.values() if info.get('avatarID') == avatarID), None)

    def getObjectName(self, id):
        avatarInfo = self.avatarInfos.get(id, None)
        if avatarInfo:
            return avatarInfo['playerName']
        else:
            objName = self.__alwaysVisibleObjects.getObjectName(id)
            if objName:
                return objName
            return str(id)
            return

    def getTeamObjectType(self, id):
        if id in self.__allObjectsData:
            return self.__allObjectsData[id]['settings'].type
        else:
            return None

    def getScenarioObjectByDSName(self, name):
        return self.__scenarioObjectMap.get(name)

    def isTeamObjectContainsTurret(self, id):
        if id in self.__allObjectsData:
            return bool(self.__allObjectsData[id]['settings'].turretName)
        return False

    @property
    def allObjectsData(self):
        return self.__allObjectsData

    @property
    def alwaysVisibleObjects(self):
        return self.__alwaysVisibleObjects

    def __onReceiveTextMessage(self, argStr):
        senderID, messageType, messageStringID, targetID, message = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        avatarsInfo = self.avatarInfos
        senderInfo = avatarsInfo.get(senderID, None)
        if senderInfo:
            if BotChatHelper.isBotChatMessage(messageType):
                message = BotChatHelper.convertMessage(message, self.avatarInfos, senderInfo, targetID).encode('utf-8')
                messageType = BotChatHelper.convertMessageType(messageType)
                targetID = 0
            if messageType == MESSAGE_TYPE.BATTLE_ALL and senderInfo['teamIndex'] != BigWorld.player().teamIndex:
                messageType = MESSAGE_TYPE.BATTLE_ALL_FROM_OPPONENT
            try:
                msg = 'Player %s(%s) say: %s' % (self.getObjectName(senderID), senderID, unicode(message, encoding='utf-8'))
                ClientLog.g_instance.gameplay(msg.encode('utf-8'))
            except:
                LOG_ERROR('__onReceiveTextMessage', senderID, message)
                return

            self.onReceiveTextMessage(senderID, messageType, messageStringID, targetID, message, False)
        return

    def __onReceiveMarkerMessage(self, argStr):
        senderID, posX, posZ, messageStringID = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onReceiveMarkerMessage(senderID, posX, posZ, messageStringID, False)

    def __onReceiveBattleMessageReactionResult(self, argStr):
        battleMessageType, isPositive, senderID, callerID, targetID = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onBattleMessageReactionResult(battleMessageType, isPositive, senderID, callerID, targetID)

    def __onVehicleKilled(self, argStr):
        killingInfo = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onVehicleKilled(killingInfo)

    def __onGainAward(self, argStr):
        awardInfo = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onGainAward(awardInfo)

    def __onTeamObjectDestruction(self, argStr):
        killingInfo = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        victimData = self.__allObjectsData[killingInfo['victimID']]
        superiorityPoints, superiorityPointsMax = self.getSuperiorityPoints4TeamObject(killingInfo['victimID'])
        points = killingInfo.get('points', superiorityPoints)
        self.onTeamObjectDestruction(killingInfo['killerID'], killingInfo['victimID'], victimData['settings'].type, victimData['teamIndex'], points, superiorityPointsMax)

    def __onBaseIsUnderAttack(self, argStr):
        objID = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        objectType = self.getTeamObjectType(objID)
        if objectType:
            obj = BigWorld.entities.get(objID)
            if not obj:
                obj = self.getMapEntry(objID)
            if obj and getattr(obj, 'isAlive', True):
                self.onBaseIsUnderAttack(obj.position, obj.teamIndex, objectType)
        else:
            LOG_ERROR('__onBaseIsUnderAttack - objectType undefined (%s)' % objID)

    def __onUpdatePlayerStats(self, argStr):
        stats = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        avatarInfo = self.avatarInfos.get(stats['avatarID'], None)
        if avatarInfo:
            avatarInfo['stats'] = stats
            self.onUpdatePlayerStats(avatarInfo)
        return

    def __onReceiveAllTeamObjectsData(self, argStr):
        objectsList, serverTeamObjectsCheckSum = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        LOG_INFO('__onReceiveAllTeamObjectsData')
        player = BigWorld.player()
        arenaType = player.arenaType
        arenaSettings = db.DBLogic.g_instance.getArenaData(arenaType)
        arenaObjects = arenaSettings.arenaObjects
        if arenaObjects.teamObjectsCheckSum != serverTeamObjectsCheckSum:
            CRITICAL_ERROR('Invalid teamObjectsCheckSum - sync your server with client please!')
        for r in objectsList:
            record = getTeamObjectDescriptorFromCompactDescriptor(r)
            objID = record['id']
            arenaObjID = record['arenaObjID']
            maxHealth = record['maxHealth']
            objArenaData = arenaSettings.getTeamObjectData(arenaObjID)
            modelStrID = objArenaData['modelID']
            settings = db.DBLogic.g_instance.getEntityDataByName(db.DBLogic.DBEntities.BASES, modelStrID)
            classID = EntitySupportedClasses.TeamTurret if settings.type == TYPE_TEAM_OBJECT.TURRET else EntitySupportedClasses.TeamObject
            modelID = settings.typeID
            teamIndex = objArenaData['teamID']
            groupName = objArenaData['groupName']
            self.createTeamObjectControllers(objID, settings)
            self.__allObjectsData[objID].update({'groupName': groupName,
             'classID': classID,
             'teamIndex': teamIndex,
             'settings': settings,
             'modelID': modelID,
             'maxHealth': maxHealth,
             'valid': True})
            self.__alwaysVisibleObjects.addAllTimeVisibleObject(objID, classID, teamIndex, record['pos'], record['isAlive'], modelID)
            name = objArenaData['DsName']
            if name and name not in self.__scenarioObjectMap:
                self.__scenarioObjectMap[name] = (self.__allObjectsData[objID], objArenaData, objID)

        self.onReceiveAllTeamObjectsData()

    def createTeamObjectControllers(self, objID, settings, owner = None, partTypes = None, partStates = None, bodyType = None):
        partTypes = partTypes or []
        partStates = partStates or []
        objData = self.__allObjectsData.get(objID, {})
        if 'modelManipulator' not in objData:
            gunnersPartsMap = buildPartsMapByPartName('Gunner', settings.partsSettings, partTypes)
            if gunnersPartsMap:
                turretName = gunnersPartsMap[gunnersPartsMap.keys()[0]].componentXml
            else:
                turretName = ''
            controllersData = DestructibleObjectFactory.createControllers(objID, settings, settings, partTypes, partStates, turretName=turretName, bodyType=bodyType)
            objData.update(controllersData)
            self.__allObjectsData[objID] = objData
        if owner:
            selectTeamObjectStrategy(owner, owner.arenaObjID, BigWorld.player().arenaType)
            objData['movementStrategy'] = owner.controllers.get('movementStrategy', None)
        return objData

    def getMapEntry(self, objID):
        if self.__alwaysVisibleObjects:
            return self.__alwaysVisibleObjects.getMapEntry(objID)
        else:
            return None

    def initArenaData(self):
        player = BigWorld.player()
        arenaType = player.arenaType
        arenaSettings = db.DBLogic.g_instance.getArenaData(arenaType)
        arenaObjects = arenaSettings.arenaObjects
        self.battleType = player.battleType
        self.arenaData = {'waterLevel': arenaObjects.waterLevel,
         'bounds': arenaObjects.bounds,
         'battleType': player.battleType}
        self.onApplyArenaData(self.arenaData)

    def __onUpdateObjectsData(self, argStr):
        data = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        for updatableData in data:
            objID = updatableData['id']
            objData = self.avatarInfos.get(objID, None)
            if not objData:
                objData = self.__allObjectsData.get(objID, None)
            if objData:
                if objData.has_key('classID'):
                    self.__alwaysVisibleObjects.updateTemporaryVisibleObjectData(updatableData, objData['classID'], objData['teamIndex'], objData.get('modelID', None))

        return

    def __onNewAvatarsInfo(self, argStr):
        newAvatarsList = translateDictThroughAnother(wgPickle.loads(wgPickle.FromServerToClient, argStr), NEW_AVATARS_INFO_KEYS_INVERT_DICT)
        LOG_INFO('__onNewAvatarsInfo', self.__ownerID, [ avatarData['avatarID'] for avatarData in newAvatarsList ])
        LOG_INFO('INFO crewBodyType', [ (avatarData['avatarID'], avatarData['crewBodyType']) for avatarData in newAvatarsList ])
        for avatarData in newAvatarsList:
            avatarID = avatarData['avatarID']
            airplaneInfo = avatarData['airplaneInfo']
            currentOwner = None
            avatarPrevInfo = self.avatarInfos.get(avatarID, None)
            if not avatarPrevInfo:
                self.avatarInfos[avatarID] = avatarData
            else:
                if 'airplaneInfo' in avatarPrevInfo and avatarPrevInfo['airplaneInfo']['globalID'] != airplaneInfo['globalID']:
                    currentOwner = self.__destroyControllers(avatarPrevInfo)
                self.avatarInfos[avatarID].update(avatarData)
            from CrewHelpers import getPilotBodyType
            controllersData = self.createControllers(avatarID, airplaneInfo['globalID'], camouflage=airplaneInfo['camouflage'], decals=airplaneInfo['decals'], bodyType=getPilotBodyType(avatarData['crewBodyType']))
            if currentOwner:
                currentOwner.registerControllers(controllersData)
                if currentOwner == BigWorld.player():
                    self.onRecreateAvatar()
            avatarInfo = self.avatarInfos[avatarID]
            avatarInfo['playerName'] = getBotName(avatarData['playerName'], getAirplaneConfiguration(airplaneInfo['globalID']).planeID)
            avatarInfo['maxHealth'] = avatarData['maxHealth']
            avatarInfo['equipment'] = avatarData['equipment']
            if avatarID == BigWorld.player().id:
                LOG_TRACE('ClientArena: VOIP.initialize()')
                wasInit = bool(VOIP.api())
                VOIP.initialize(avatarInfo['databaseID'])
                if not wasInit:
                    VOIP.api().onEnterArenaScreen()

        self.__sortAvatars()
        for ids in self.__sortedAvatarsIDs.values():
            for i, avatarID in enumerate(ids):
                self.avatarInfos[avatarID]['airplaneInfo']['decals'][4] = i + 1
                self.avatarInfos[avatarID]['modelManipulator'].surface.setDecalsByIds(self.avatarInfos[avatarID]['airplaneInfo']['camouflage'], self.avatarInfos[avatarID]['airplaneInfo']['decals'])

        teamMembers = dict()
        for avatarID, info in self.avatarInfos.iteritems():
            if info['teamIndex'] == BigWorld.player().teamIndex:
                teamMembers[info['databaseID']] = avatarID

        VOIP.api().unsubscribeMemberStateObserversByType(consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.ARENA_HUD)
        VOIP.api().subscribeMemberStateObserver(consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.ARENA_HUD, teamMembers)
        self.__avatarsDataReceived = True
        self.onNewAvatarsInfo(newAvatarsList)
        return

    def __sortAvatars(self):
        teams = dict()
        for avatarInfo in self.avatarInfos.values():
            level = avatarInfo['settings'].airplane.level
            teamIndex = avatarInfo['teamIndex']
            name = localizeAirplane(avatarInfo['settings'].airplane.name)
            if teamIndex not in teams:
                teams[teamIndex] = dict()
            if level not in teams[teamIndex]:
                teams[teamIndex][level] = dict()
            if name not in teams[teamIndex][level]:
                teams[teamIndex][level][name] = list()
            teams[teamIndex][level][name].append(avatarInfo)

        sortedList = list()
        for team in teams.values():
            for level in team.values():
                for name in level.values():
                    name.sort(key=lambda avatarInfo: avatarInfo['playerName'])

            sortedLevelsList = sorted(team.keys(), None, None, True)
            for levelID in sortedLevelsList:
                sortedPlaneNameList = sorted(team[levelID].keys())
                for planeName in sortedPlaneNameList:
                    sortedList.extend(team[levelID][planeName])

        for avatarInfo in sortedList:
            if avatarInfo['teamIndex'] not in self.__sortedAvatarsIDs:
                self.__sortedAvatarsIDs[avatarInfo['teamIndex']] = list()
            self.__sortedAvatarsIDs[avatarInfo['teamIndex']].append(avatarInfo['avatarID'])

        return

    def isAllServerDataReceived(self):
        return self.__avatarsDataReceived

    def __onReceiveLaunch(self, argStr):
        avatarID, shellsCount = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.avatarInfos[avatarID]['shellsCount'] = shellsCount
        self.onLaunch(avatarID)

    def __destroyControllers(self, avatarInfo):
        weapons = avatarInfo.get('weapons', None)
        if weapons:
            owner = weapons.getOwner()
            self.__destroyObjectControllers(avatarInfo)
            return owner
        else:
            return

    def __destroyObjectControllers(self, objData):
        if 'modelManipulator' in objData:
            objData['modelManipulator'].destroy()
            del objData['modelManipulator']
        if 'weapons' in objData:
            objData['weapons'].destroy()
            del objData['weapons']
        if 'turretsLogic' in objData:
            objData['turretsLogic'].destroy()
            del objData['turretsLogic']
        if 'shellController' in objData:
            objData['shellController'].destroy()
            del objData['shellController']

    def createControllers(self, avatarID, globalID, partStates = None, camouflage = None, decals = None, bodyType = None):
        """
        create Weapons, ShellController and ModelManipulator controllers if they are not present yet
        @param avatarID:
        @param globalID:
        @param partStates:
        @return full AvatarInfo if present of created controllers data if not.
        Any way controllers data are part of AvatarInfo
        """
        ATTRS_FOR_COPY = ('teamIndex', 'stats', 'classID')
        partStates = partStates or []
        avatarInfo = self.avatarInfos.get(avatarID, {})
        if 'modelManipulator' not in avatarInfo:
            controllersData = self.__createControllers(avatarID, globalID, partStates, camouflage, decals, bodyType)
            avatarInfo.update(controllersData)
            self.avatarInfos[avatarID] = avatarInfo
        return avatarInfo

    def __createControllers(self, avatarID, globalID, partStates, camouflage = None, decals = None, bodyType = None):
        aircraftConfiguration = getAirplaneConfiguration(globalID)
        settings = db.DBLogic.g_instance.getAircraftData(aircraftConfiguration.planeID)
        player = BigWorld.player()
        if player.id == avatarID:
            player.weaponsInfo = buildAndGetWeaponsInfo(settings.components.weapons2, aircraftConfiguration.weaponSlots)
        logicalParts = airplanesConfigurations[globalID].logicalParts
        turretName = settings.airplane.flightModel.turret[logicalParts[LOGICAL_PART.TURRET]].name
        return DestructibleObjectFactory.createControllers(avatarID, settings, settings.airplane, aircraftConfiguration.partTypes, partStates, aircraftConfiguration.weaponSlots, callback=self.__onAvatarModelLoaded, camouflage=camouflage, decals=decals, bodyType=bodyType, turretName=turretName)

    def __convertServerTeamDataToOwnClientTeamData(self, data):
        ownerTeamIndex = BigWorld.player().teamIndex
        return (data[ownerTeamIndex], data[1 - ownerTeamIndex])

    def __onUpdateTeamSuperiorityPoints(self, argStr):
        score = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        ownScore, enemyScore = self.__convertServerTeamDataToOwnClientTeamData(score)
        self.onUpdateTeamSuperiorityPoints(self.superiorityPoints, ownScore, enemyScore)
        self.superiorityPoints[0], self.superiorityPoints[1] = ownScore, enemyScore

    def __onReceiveTurretBoosterInfo(self, argStr):
        teamIndex = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onUpdateTurretBoosterInfo(teamIndex == BigWorld.player().teamIndex)

    def __onUpdateDominationPrc(self, argStr):
        basesPrc = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.dominationPrc[0], self.dominationPrc[1] = self.__convertServerTeamDataToOwnClientTeamData(basesPrc)
        self.onUpdateDominationPrc(self.dominationPrc)

    def __onReportBattleResult(self, argStr):
        clientBattleResult = translateDictThroughAnother(wgPickle.loads(wgPickle.FromServerToClient, argStr), REPORT_BATTLE_RESULT_KEYS_INVERT_DICT)
        self.onReportBattleResult(clientBattleResult)

    def __onReceiveVOIPChannelCredentials(self, argStr):
        name, teamMembers = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onReceiveVOIPChannelCredentials(name, teamMembers)

    def vehiclesLoadStatus(self):
        return [self.avatarModelLoaded, len(self.avatarInfos)]

    def __onAvatarModelLoaded(self):
        self.avatarModelLoaded += 1

    def doUpdateArena(self, functionIndex, updateFunctionID, argStr):
        if functionIndex == self.__lastUpdateFunctionIndex + 1:
            self.__lastUpdateFunctionIndex += 1
            self.update(updateFunctionID, argStr)
            if self.__waitingUpdateFunctionsPool:

                def filterPool():
                    indices = self.__waitingUpdateFunctionsPool.keys()
                    indices.sort()
                    for i in indices:
                        if i == self.__lastUpdateFunctionIndex + 1:
                            self.__lastUpdateFunctionIndex += 1
                            try:
                                fID, fArgs = self.__waitingUpdateFunctionsPool[i]
                                self.update(fID, fArgs)
                            except Exception as msg:
                                print msg

                        else:
                            yield (i, self.__waitingUpdateFunctionsPool[i])

                self.__waitingUpdateFunctionsPool = dict(filterPool())
        else:
            self.__waitingUpdateFunctionsPool[functionIndex] = (updateFunctionID, argStr)

    def getAvatarInfoByName(self, name):
        for avatarInfo in self.avatarInfos.values():
            if avatarInfo['playerName'] == name:
                return avatarInfo

        return None

    def getAvatarInfo(self, avatarID):
        return self.avatarInfos.get(avatarID, None)

    def getSortedAvatarInfosList(self):
        if self.isAllServerDataReceived():
            sortedList = list()
            for ids in self.__sortedAvatarsIDs.values():
                sortedList.extend(ids)

            return [ self.avatarInfos[id] for id in sortedList ]
        return [ avatarInfo for avatarInfo in self.avatarInfos.values() ]

    def getWaterLevel(self):
        if self.arenaData is None:
            LOG_WARNING('getWaterLevel - water level set as default value = 0.0')
            return 0.0
        else:
            return self.arenaData['waterLevel']

    def __onGameResultChanged(self, argStr):
        gameResult, winState = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onGameResultChanged(gameResult, winState)

    def onBattleUILoaded(self):
        self.__isBattleUILoaded = True

    def isLoaded(self):
        return self.__isBattleUILoaded

    def getSuperiorityPoints4TeamObject(self, teamObjectID):
        mapEntry = self.getMapEntry(teamObjectID)
        if mapEntry is not None:
            return (mapEntry.superiorityPoints, mapEntry.superiorityPointsMax)
        else:
            LOG_WARNING('getSuperiorityPoints4TeamObject - team object not in MapEntry table', teamObjectID)
            return (None, None)

    def __decSuperiorityPoints4TeamObject(self, teamObjectID, points):
        if not points:
            LOG_DEBUG('__decSuperiorityPoints4TeamObject - points = 0', teamObjectID, points)
            return
        else:
            mapEntry = self.getMapEntry(teamObjectID)
            if mapEntry is not None:
                mapEntry.superiorityPoints -= points
            else:
                LOG_WARNING('__decSuperiorityPoints4TeamObject - team object not in MapEntry table', teamObjectID, points)
            return

    def __onTeamObjectPartGroupDestroyed(self, argStr):
        for teamObjectID, points, killerID in wgPickle.loads(wgPickle.FromServerToClient, argStr):
            self.__decSuperiorityPoints4TeamObject(teamObjectID, points)
            self.onTeamObjectPartGroupChanged(killerID, teamObjectID, points)

    def __onScenarioSetIcon(self, argStr):
        groupName, iconIndex, textID, temaIndex = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onScenarioSetIcon(groupName, iconIndex, textID, temaIndex)

    def __onScenarioSetText(self, argStr):
        textID, colorID = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        self.onScenarioSetText(textID, colorID)

    def __onDebugInfoReceived(self, argStr):
        from Math import Matrix, Vector3
        positions = wgPickle.loads(wgPickle.FromServerToClient, argStr)
        for planeID, pos in positions:
            m = Matrix()
            m.setTranslate(pos)
            BigWorld.addPoint('spawnPoint%d' % planeID, m, 4278190335L, False)