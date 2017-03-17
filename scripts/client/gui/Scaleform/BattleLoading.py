# Embedded file name: scripts/client/gui/Scaleform/BattleLoading.py
import BigWorld
import db.DBLogic
from Helpers.i18n import localizeAirplane, localizeTutorial, localizeOptions, localizeMap
from debug_utils import LOG_DEBUG, LOG_INFO, CRITICAL_ERROR, LOG_ERROR
from gui.HelpHint import HelpHint
from _tutorial_data import TutorialData
import InputMapping
from clientConsts import INPUT_SYSTEM_PROFILES, PERFORMANCE_SPECS_PARAMETERS, getHudPlaneIcon
import GameEnvironment
from EntityHelpers import EntityStates, AvatarFlags
from gui.Scaleform.windows import CustomObject
from consts import SUPERIORITY2_BASE_HEALTH, ACCOUNT_ATTR
import gui.HUDconsts
from Event import Event
from gui.Scaleform.UIHelper import BattleInfo, SQUAD_TYPES
import BattleReplay
from EntityHelpers import EntitySupportedClasses

class _BattleLoadingInfo:

    def __init__(self):
        self.battleType = -1
        self.battleName = ''
        self.battleLoadingTitle = ''
        self.battleLoadingDescription = ''


class _BattleLoadingTeamsVO:

    def __init__(self):
        self.teamA = []
        self.teamB = []


class _BattleLoadingPlayerObj:

    def __init__(self):
        self.playerName = ''
        self.isLoaded = False
        self.planeName = ''
        self.clanAbbrev = ''
        self.planeLevel = ''
        self.planeIcoPath = ''
        self.planeType = -1
        self.isOwner = False
        self.squadNumber = 0
        self.squadType = 0
        self.planeNumber = 0
        self.typeIconPath = ''


class BattleLoading(object):
    profiler = BigWorld.ProfilerEvent('BattleLoading')

    def __init__(self):
        self.__uiOwner = None
        self.__initialized = False
        self.__timerCallback = None
        self.__loadLevel = int(0)
        self.__teamsIdsLoaded = [[], []]
        self.__tooltipsHelp = HelpHint()
        self.__tutorialHelpIndexes = None
        self.__isLoaded = False
        self.__dispossessed = False
        self.onDispossed = Event()
        self.__disposeConditionFunc = None
        BattleLoading.profiler.start()
        return

    def initialized(self, uiOwner, performanceSpecsDescriptions = None):
        if not self.__initialized:
            self.__uiOwner = uiOwner
            self.__initialized = True
            self.__dispossessed = False
            self.__tooltipsHelp.receive += self.__onShowHelpText
            owner = BigWorld.player()
            arenaData = db.DBLogic.g_instance.getArenaData(owner.arenaType)
            self.__uiOwner.call_1('setBattleMap', localizeMap(arenaData.typeName), arenaData.hudIcoPath)
            self.__timerCallback = BigWorld.callback(0.5, self.__checkLoadLevel)
            self.__setBattleType(owner.battleType, owner.tutorialIndex)
            LOG_INFO('Battle in loading process')
            self.__onNewAvatarsInfo()
            self.__linkEvents()
            if performanceSpecsDescriptions is not None:
                self.sendHintsData(performanceSpecsDescriptions)
        else:
            CRITICAL_ERROR('Loading flow corrupted: BattleLoading already initialized')
        return

    def sendHintsData(self, performanceSpecsDescriptions):
        playerData = CustomObject()
        playerData.description = ''
        playerData.characteristics = list()
        for performanceSpecs in PERFORMANCE_SPECS_PARAMETERS:
            characteristicsVO = CustomObject()
            characteristicsVO.stars = performanceSpecsDescriptions[performanceSpecs].stars
            characteristicsVO.text = performanceSpecsDescriptions[performanceSpecs].name
            characteristicsVO.value = performanceSpecsDescriptions[performanceSpecs].value
            playerData.characteristics.append(characteristicsVO)

        if self.__uiOwner is not None:
            self.__uiOwner.call_1('responsePlayerInfo', playerData)
        return

    def __linkEvents(self):
        clientArena = GameEnvironment.getClientArena()
        clientArena.onNewAvatarsInfo += self.__onNewAvatarsInfo
        clientArena.onUpdatePlayerStats += self.onUpdatePlayerStats

    def __unlinkEvents(self):
        clientArena = GameEnvironment.getClientArena()
        if clientArena is not None:
            clientArena.onNewAvatarsInfo -= self.__onNewAvatarsInfo
            clientArena.onUpdatePlayerStats -= self.onUpdatePlayerStats
        return

    def __onNewAvatarsInfo(self, newAvatarsList = None):
        LOG_DEBUG('BattleLoading::__onNewAvatarsInfo(), stateName=%s' % EntityStates.getStateName(BigWorld.player().state))
        self.__updateBattleLoading(GameEnvironment.getClientArena().getSortedAvatarInfosList())

    def dispossess(self):
        if self.__initialized:
            LOG_INFO('BattleLoading.dispossess')
            GameEnvironment.getCamera().stopPreIntro()
            self.__uiOwner.call_1('hud.hideLoadingScreen')
            self.__unlinkEvents()
            self.__tooltipsHelp.stop()
            self.__cancelCallback()
            self.__uiOwner = None
            self.__initialized = False
            self.__dispossessed = True
            self.__disposeConditionFunc = None
            self.onDispossed()
        else:
            LOG_ERROR('Loading flow corrupted: BattleLoading already dispossessed')
        return

    def isDispossessed(self):
        return self.__dispossessed

    def __cancelCallback(self):
        if self.__timerCallback is not None:
            BigWorld.cancelCallback(self.__timerCallback)
            self.__timerCallback = None
        return

    def __setBattleType(self, battleType, tutorialIndex):
        if not self.__initialized:
            CRITICAL_ERROR('Loading flow corrupted')
        vo = _BattleLoadingInfo()
        vo.battleType, vo.battleName, mapName, vo.battleLoadingTitle, vo.battleLoadingDescription = BattleInfo().getBattleInfo(battleType, tutorialIndex)
        vo.pvpUnlocked = BigWorld.player().isPvPUnlocked
        if tutorialIndex != -1:
            self.__tutorialHelpIndexes = TutorialData.lesson[tutorialIndex].battleLoadingHelpHints.split(',')
            self.__tooltipsHelp.setCountMessages(len(self.__tutorialHelpIndexes) - 1)
        vo.titleProfile = localizeOptions('CONTROL_PRESET') + ': ' + InputMapping.g_instance.getLocalizedProfileName()
        vo.curProfileName = INPUT_SYSTEM_PROFILES[InputMapping.g_instance.currentProfileType]
        vo.tutorialIndex = tutorialIndex
        self.__tooltipsHelp.start()
        self.__uiOwner.call_1('setBattleType', vo)

    def onUpdatePlayerStats(self, avatarInfo):
        self.__updateBattleLoading(GameEnvironment.getClientArena().getSortedAvatarInfosList())

    def __updateBattleLoading(self, data):
        if not self.__initialized:
            CRITICAL_ERROR('Loading flow corrupted')
        LOG_DEBUG('BattleLoading::__updateBattleLoading', data)
        self.__teamsData = _BattleLoadingTeamsVO()
        teamsObjData = [self.__teamsData.teamA, self.__teamsData.teamB]
        teamsLoaded = [[], []]
        needReinitTeams = False
        owner = BigWorld.player()
        ownerTeamIndex = owner.teamIndex
        ownerID = owner.id
        for avatarInfo in data:
            avatarTeamIndex = avatarInfo.get('teamIndex', -1)
            if avatarTeamIndex >= 0:
                if SUPERIORITY2_BASE_HEALTH and avatarInfo['classID'] == EntitySupportedClasses.AvatarBot:
                    continue
                side = 0 if ownerTeamIndex == avatarTeamIndex else 1
                settings = avatarInfo['settings']
                id = avatarInfo['avatarID']
                playerObj = _BattleLoadingPlayerObj()
                playerObj.isLoaded = avatarInfo['stats']['flags'] & AvatarFlags.LOADED != 0
                playerObj.isOwner = id == ownerID
                playerObj.planeIcoPath = settings.airplane.hudIcoPath
                playerObj.typeIconPath = getHudPlaneIcon(settings.airplane.planeType)
                playerObj.battleLoadingIconPath = settings.airplane.battleLoadingIconPath if hasattr(settings.airplane, 'battleLoadingIconPath') else settings.airplane.previewIconPath
                playerObj.planeLevel = settings.airplane.level
                playerObj.planeName = localizeAirplane(settings.airplane.name)
                playerObj.playerName = avatarInfo['playerName']
                playerObj.clanAbbrev = avatarInfo['clanAbbrev']
                playerObj.planeType = settings.airplane.planeType
                playerObj.planeNumber = avatarInfo['airplaneInfo']['decals'][4]
                playerObj.squadNumber = avatarInfo['squadID']
                playerObj.isIgr = bool(avatarInfo['attrs'] & (ACCOUNT_ATTR.IGR_BASE | ACCOUNT_ATTR.IGR_PREMIUM))
                playerObj.squadType = SQUAD_TYPES.getSquadType(playerObj.squadNumber, id)
                playerObj.id = id
                isNewId = True
                for data in self.__teamsIdsLoaded[side]:
                    if id in data:
                        data[id] = playerObj.isLoaded
                        isNewId = False
                        break

                if isNewId:
                    self.__teamsIdsLoaded[side].append({id: playerObj.isLoaded})
                    needReinitTeams = True
                teamsObjData[side].append(playerObj)

        if needReinitTeams:
            self.__uiOwner.call_1('initTeams', self.__teamsData)
        else:
            teamIndex = 0
            for team in self.__teamsIdsLoaded:
                for data in team:
                    teamsLoaded[teamIndex].append(data.values())

                teamIndex += 1

            self.__uiOwner.call_1('updateTeamA', teamsLoaded[0])
            self.__uiOwner.call_1('updateTeamB', teamsLoaded[1])

    def __isTimeForHide(self):
        curTime = int(round(BigWorld.player().arenaStartTime - BigWorld.serverTime()))
        return BigWorld.player().arenaStartTime >= 0 and curTime <= gui.HUDconsts.TIME_AFTER_ARENA_STARTED_FOR_HIDE_LOADING_SCREEN

    def __chekForHide(self):
        if self.__isLoaded and self.__isTimeForHide() and (self.__disposeConditionFunc is None or self.__disposeConditionFunc()):
            if BattleReplay.isPlaying():
                BigWorld.callback(0, self.dispossess)
            else:
                self.dispossess()
        return

    def __checkLoadLevel(self):
        self.__timerCallback = BigWorld.callbackRealTime(0.5, self.__checkLoadLevel)
        if not self.__isLoaded:
            vehiclesLoadStatusInfo = GameEnvironment.getClientArena().vehiclesLoadStatus()
            vehiclesLoadStatus = 1.0
            if vehiclesLoadStatusInfo[1] > 0:
                vehiclesLoadStatus = float(vehiclesLoadStatusInfo[0]) / vehiclesLoadStatusInfo[1]
            spaceLoadStatus = BigWorld.spaceLoadStatus()
            self.__loadLevel = max(int(50 * (spaceLoadStatus + vehiclesLoadStatus)), self.__loadLevel)
            self.__uiOwner.call_1('updateProgressBar', [self.__loadLevel])
            if self.__loadLevel >= 100.0:
                self.__isLoaded = True
                LOG_INFO('Battle was loaded')
                BigWorld.player().onArenaLoaded()
                self.__uiOwner.call_1('arenaLoaded')
                BattleLoading.profiler.end()
                BigWorld.memoryMark('arenaLoaded')
        self.__chekForHide()

    def __onShowHelpText(self, messageIndex):
        LOG_DEBUG('updateHelpText', messageIndex)
        if self.__tutorialHelpIndexes is not None:
            id = self.__tutorialHelpIndexes[messageIndex]
        else:
            id = 'HINT_' + str(messageIndex)
        self.__uiOwner.call_1('updateHelpText', localizeTutorial(id))
        return

    def setDisposeCondition(self, func):
        self.__disposeConditionFunc = func