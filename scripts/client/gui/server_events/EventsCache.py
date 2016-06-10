# Embedded file name: scripts/client/gui/server_events/EventsCache.py
import math
import sys
import zlib
import cPickle as pickle
from collections import defaultdict
import BigWorld
from PlayerEvents import g_playerEvents
import clubs_quests
import motivation_quests
from Event import Event, EventManager
from adisp import async, process
from constants import EVENT_TYPE, EVENT_CLIENT_DATA, QUEUE_TYPE, ARENA_BONUS_TYPE
from potapov_quests import _POTAPOV_QUEST_XML_PATH
from gui.shared.utils.requesters.QuestsProgressRequester import QuestsProgressRequester
from helpers import isPlayerAccount
from items import getTypeOfCompactDescr
from dossiers2.ui.achievements import ACHIEVEMENT_BLOCK
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG
from gui.LobbyContext import g_lobbyContext
from gui.shared import events
from gui.server_events import caches as quests_caches
from gui.server_events.modifiers import ACTION_SECTION_TYPE, ACTION_MODIFIER_TYPE
from gui.server_events.PQController import RandomPQController, FalloutPQController
from gui.server_events.CompanyBattleController import CompanyBattleController
from gui.server_events.event_items import EventBattles, createQuest, createAction, FalloutConfig, MotiveQuest
from gui.server_events.event_items import CompanyBattles, ClubsQuest
from gui.shared.utils.RareAchievementsCache import g_rareAchievesCache
from gui.shared.gui_items import GUI_ITEM_TYPE
from quest_cache_helpers import readQuestsFromFile
from shared_utils import makeTupleByDict
QUEUE_TYPE_TO_ARENA_BONUS_TYPE = {QUEUE_TYPE.FALLOUT_CLASSIC: ARENA_BONUS_TYPE.FALLOUT_CLASSIC,
 QUEUE_TYPE.FALLOUT_MULTITEAM: ARENA_BONUS_TYPE.FALLOUT_MULTITEAM}

def _defaultQuestMaker(qID, qData, progress):
    return createQuest(qData.get('type', 0), qID, qData, progress.getQuestProgress(qID), progress.getTokenExpiryTime(qData.get('requiredToken')))


def _clubsQuestMaker(qID, qData, progress, seasonID, questDescr):
    return ClubsQuest(seasonID, questDescr, progress.getQuestProgress(qID))


def _motiveQuestMaker(qID, qData, progress):
    return MotiveQuest(qID, qData, progress.getQuestProgress(qID))


class _PotapovComposer(object):

    def __init__(self, random, fallout):
        super(_PotapovComposer, self).__init__()
        self.__composedObjects = [random, fallout]

    def getQuests(self):
        return self.__composeDict('getQuests')

    def getTiles(self):
        return self.__composeDict('getTiles')

    def getSelectedQuests(self):
        return self.__composeDict('getSelectedQuests')

    def hasQuestsForReward(self):
        return any((obj.hasQuestsForReward() for obj in self.__composedObjects))

    def hasQuestsForSelect(self):
        return any((obj.hasQuestsForSelect() for obj in self.__composedObjects))

    def getNextTankwomanIDs(self, *args):
        return self.__composedObjects[0].getNextTankwomanIDs(*args)

    def __composeDict(self, getter):
        result = {}
        for obj in self.__composedObjects:
            result.update(getattr(obj, getter)())

        return result


class _EventsCache(object):
    USER_QUESTS = (EVENT_TYPE.BATTLE_QUEST,
     EVENT_TYPE.TOKEN_QUEST,
     EVENT_TYPE.FORT_QUEST,
     EVENT_TYPE.PERSONAL_QUEST,
     EVENT_TYPE.POTAPOV_QUEST)
    SYSTEM_QUESTS = (EVENT_TYPE.REF_SYSTEM_QUEST,)

    def __init__(self):
        self.__waitForSync = False
        self.__invalidateCbID = None
        self.__cache = defaultdict(dict)
        self.__potapovHidden = {}
        self.__actionsCache = defaultdict(lambda : defaultdict(dict))
        self.__questsDossierBonuses = defaultdict(set)
        self.__random = RandomPQController()
        self.__fallout = FalloutPQController()
        self.__potapovComposer = _PotapovComposer(self.__random, self.__fallout)
        self.__questsProgress = QuestsProgressRequester()
        self.__companies = CompanyBattleController(self)
        self.__em = EventManager()
        self.onSyncStarted = Event(self.__em)
        self.onSyncCompleted = Event(self.__em)
        self.onSelectedQuestsChanged = Event(self.__em)
        self.onSlotsCountChanged = Event(self.__em)
        self.onProgressUpdated = Event(self.__em)
        self.__lockedQuestIds = {}
        return

    def init(self):
        self.__random.init()
        self.__fallout.init()

    def fini(self):
        self.__fallout.fini()
        self.__random.fini()
        self.__em.clear()
        self.__clearInvalidateCallback()

    def start(self):
        self.__companies.start()
        self.__lockedQuestIds = BigWorld.player().potapovQuestsLock
        g_playerEvents.onPQLocksChanged += self.__onLockedQuestsChanged

    def stop(self):
        g_playerEvents.onPQLocksChanged -= self.__onLockedQuestsChanged
        self.__companies.stop()

    def clear(self):
        self.stop()
        quests_caches.clearNavInfo()

    @property
    def waitForSync(self):
        return self.__waitForSync

    @property
    def falloutQuestsProgress(self):
        return self.__fallout.questsProgress

    @property
    def randomQuestsProgress(self):
        return self.__random.questsProgress

    @property
    def random(self):
        return self.__random

    @property
    def fallout(self):
        return self.__fallout

    @property
    def questsProgress(self):
        return self.__questsProgress

    @property
    def potapov(self):
        return self.__potapovComposer

    @property
    def companies(self):
        return self.__companies

    def getLockedQuestTypes(self):
        questIDs = set()
        result = set()
        allQuests = self.potapov.getQuests()
        for lockedList in self.__lockedQuestIds.values():
            if lockedList is not None:
                questIDs.update(lockedList)

        for questID in questIDs:
            if questID in allQuests:
                result.add(allQuests[questID].getMajorTag())

        return result

    @async
    @process
    def update(self, diff = None, callback = None):
        if diff is not None:
            if diff.get('eventsData', {}).get(EVENT_CLIENT_DATA.INGAME_EVENTS):
                self.__companies.setNotificators()
        yield self.falloutQuestsProgress.request()
        yield self.randomQuestsProgress.request()
        yield self.__questsProgress.request()
        isNeedToInvalidate = True
        isNeedToClearItemsCaches = False

        def _cbWrapper(*args):
            self.__random.update(self, diff)
            self.__fallout.update(self, diff)
            callback(*args)

        if diff is not None:
            isQPUpdated = 'quests' in diff
            isEventsDataUpdated = ('eventsData', '_r') in diff or diff.get('eventsData', {})
            isNeedToInvalidate = isQPUpdated or isEventsDataUpdated
            hasVehicleUnlocks = False
            for intCD in diff.get('stats', {}).get('unlocks', set()):
                if getTypeOfCompactDescr(intCD) == GUI_ITEM_TYPE.VEHICLE:
                    hasVehicleUnlocks = True
                    break

            isNeedToClearItemsCaches = 'inventory' in diff and GUI_ITEM_TYPE.VEHICLE in diff['inventory'] or hasVehicleUnlocks
        if isNeedToInvalidate:
            self.__invalidateData(_cbWrapper)
            return
        else:
            if isNeedToClearItemsCaches:
                self.__clearQuestsItemsCache()
            _cbWrapper(True)
            return

    def getQuests(self, filterFunc = None):
        filterFunc = filterFunc or (lambda a: True)

        def userFilterFunc(q):
            return not q.isHidden() and filterFunc(q)

        return self._getQuests(userFilterFunc)

    def getMotiveQuests(self, filterFunc = None):
        filterFunc = filterFunc or (lambda a: True)

        def userFilterFunc(q):
            return q.getType() == EVENT_TYPE.MOTIVE_QUEST and filterFunc(q)

        return self.getQuests(userFilterFunc)

    def getGroups(self, filterFunc = None):
        svrGroups = self._getQuestsGroups(filterFunc)
        svrGroups.update(self._getActionsGroups(filterFunc))
        return svrGroups

    def getHiddenQuests(self, filterFunc = None):
        filterFunc = filterFunc or (lambda a: True)

        def hiddenFilterFunc(q):
            return q.isHidden() and filterFunc(q)

        return self._getQuests(hiddenFilterFunc)

    def getAllQuests(self, filterFunc = None, includePotapovQuests = False):
        return self._getQuests(filterFunc, includePotapovQuests)

    def getActions(self, filterFunc = None):
        filterFunc = filterFunc or (lambda a: True)

        def userFilterFunc(q):
            return filterFunc(q) and q.getType() != EVENT_TYPE.GROUP

        return self._getActions(userFilterFunc)

    def getEventBattles(self):
        battles = self.__getEventBattles()
        if len(battles):
            return EventBattles(battles.get('vehicleTags', set()), battles.get('vehicles', []), bool(battles.get('enabled', 0)), battles.get('arenaTypeID'), battles.get('dueDate'))
        else:
            return EventBattles(set(), [], False, None, None)
            return None

    def isEventEnabled(self):
        battles = self.__getEventBattles()
        return bool(battles.get('enabled', 0)) and len(self.getEventVehicles()) > 0

    def getEventDueDate(self):
        return self.getEventBattles().dueDate

    def isGasAttackEnabled(self):
        return len(self.__getGasAttack()) > 0

    def getEventVehicles(self):
        from gui.shared import g_itemsCache
        result = []
        for v in self.getEventBattles().vehicles:
            item = g_itemsCache.items.getItemByCD(v)
            if item.isInInventory:
                result.append(item)

        return sorted(result)

    def getEvents(self, filterFunc = None):
        svrEvents = self.getQuests(filterFunc)
        svrEvents.update(self.getActions(filterFunc))
        return svrEvents

    def getCurrentEvents(self):
        return self.getEvents(lambda q: q.getStartTimeLeft() <= 0 < q.getFinishTimeLeft())

    def getFutureEvents(self):
        return self.getEvents(lambda q: q.getStartTimeLeft() > 0)

    def getCompanyBattles(self):
        battle = self.__getCompanyBattlesData()
        startTime = battle.get('startTime', 0.0)
        finishTime = battle.get('finishTime', 0.0)
        return CompanyBattles(startTime=None if startTime is None else float(startTime), finishTime=None if finishTime is None else float(finishTime), peripheryIDs=battle.get('peripheryIDs', set()))

    def isFalloutEnabled(self):
        return bool(self.__getFallout().get('enabled', False))

    def getFalloutConfig(self, queueType):
        arenaBonusType = QUEUE_TYPE_TO_ARENA_BONUS_TYPE.get(queueType, ARENA_BONUS_TYPE.UNKNOWN)
        return makeTupleByDict(FalloutConfig, self.__getFallout().get(arenaBonusType, {}))

    def getItemAction(self, item, isBuying = True, forCredits = False):
        result = []
        type = ACTION_MODIFIER_TYPE.DISCOUNT if isBuying else ACTION_MODIFIER_TYPE.SELLING
        itemTypeID = item.itemTypeID
        nationID = item.nationID
        intCD = item.intCD
        values = self.__actionsCache[ACTION_SECTION_TYPE.ALL][type].get(itemTypeID, {}).get(nationID, [])
        values += self.__actionsCache[ACTION_SECTION_TYPE.ALL][type].get(itemTypeID, {}).get(15, [])
        for (key, value), actionID in values:
            if item.isPremium and key in ('creditsPrice', 'creditsPriceMultiplier') and not forCredits:
                continue
            result.append((value, actionID))

        result.extend(self.__actionsCache[ACTION_SECTION_TYPE.ITEM][type].get(itemTypeID, {}).get(intCD, tuple()))
        return result

    def getRentAction(self, item, rentPackage):
        result = []
        type = ACTION_MODIFIER_TYPE.RENT
        itemTypeID = item.itemTypeID
        nationID = item.nationID
        intCD = item.intCD
        values = self.__actionsCache[ACTION_SECTION_TYPE.ALL][type].get(itemTypeID, {}).get(nationID, [])
        values += self.__actionsCache[ACTION_SECTION_TYPE.ALL][type].get(itemTypeID, {}).get(15, [])
        for (key, value), actionID in values:
            result.append((value, actionID))

        result.extend(self.__actionsCache[ACTION_SECTION_TYPE.ITEM][type].get(itemTypeID, {}).get((intCD, rentPackage), tuple()))
        return result

    def getEconomicsAction(self, name):
        result = self.__actionsCache[ACTION_SECTION_TYPE.ECONOMICS][ACTION_MODIFIER_TYPE.DISCOUNT].get(name, [])
        resultMult = self.__actionsCache[ACTION_SECTION_TYPE.ECONOMICS][ACTION_MODIFIER_TYPE.DISCOUNT].get('%sMultiplier' % name, [])
        return tuple(result + resultMult)

    def getCamouflageAction(self, vehicleIntCD):
        return tuple(self.__actionsCache[ACTION_SECTION_TYPE.CUSTOMIZATION][ACTION_MODIFIER_TYPE.DISCOUNT].get(vehicleIntCD, tuple()))

    def getEmblemsAction(self, group):
        return tuple(self.__actionsCache[ACTION_SECTION_TYPE.CUSTOMIZATION][ACTION_MODIFIER_TYPE.DISCOUNT].get(group, tuple()))

    def isBalancedSquadEnabled(self):
        return bool(self.__getUnitRestrictions().get('enabled', False))

    def getBalancedSquadBounds(self):
        return (self.__getUnitRestrictions().get('lowerBound', 0), self.__getUnitRestrictions().get('upperBound', 0))

    def isSquadXpFactorsEnabled(self):
        return bool(self.__getUnitXpFactors().get('enabled', False))

    def getSquadBonusLevelDistance(self):
        return set(self.__getUnitXpFactors().get('levelDistanceWithBonuses', ()))

    def getSquadPenaltyLevelDistance(self):
        return set(self.__getUnitXpFactors().get('levelDistanceWithPenalties', ()))

    def getSquadZeroBonuses(self):
        return set(self.__getUnitXpFactors().get('zeroBonusesFor', ()))

    def getQuestsDossierBonuses(self):
        return self.__questsDossierBonuses

    def getQuestsByTokenRequirement(self, token):
        result = []
        for q in self._getQuests(includePotapovQuests=True).itervalues():
            if token in map(lambda t: t.getID(), q.accountReqs.getTokens()):
                result.append(q)

        return result

    def getQuestsByTokenBonus(self, token):
        result = []
        for q in self._getQuests(includePotapovQuests=True).itervalues():
            for t in q.getBonuses('tokens'):
                if token in t.getTokens().keys():
                    result.append(q)
                    break

        return result

    def _getQuests(self, filterFunc = None, includePotapovQuests = False):
        result = {}
        groups = {}
        filterFunc = filterFunc or (lambda a: True)
        for qID, q in self.__getCommonQuestsIterator():
            if q.getType() == EVENT_TYPE.GROUP:
                groups[qID] = q
                continue
            if q.getDestroyingTimeLeft() <= 0:
                continue
            if not filterFunc(q):
                continue
            result[qID] = q

        if includePotapovQuests:
            for qID, q in self.potapov.getQuests().iteritems():
                if filterFunc(q):
                    result[qID] = q

        for gID, group in groups.iteritems():
            for qID in group.getGroupEvents():
                if qID in result:
                    result[qID].setGroupID(gID)

        children, parents = self._makeQuestsRelations(result)
        for qID, q in result.iteritems():
            if qID in children:
                q.setChildren(children[qID])
            if qID in parents:
                q.setParents(parents[qID])

        return result

    def _getQuestsGroups(self, filterFunc = None):
        filterFunc = filterFunc or (lambda a: True)
        result = {}
        for qID, q in self.__getCommonQuestsIterator():
            if q.getType() != EVENT_TYPE.GROUP:
                continue
            if not filterFunc(q):
                continue
            result[qID] = q

        return result

    def _getActions(self, filterFunc = None):
        filterFunc = filterFunc or (lambda a: True)
        actions = self.__getActionsData()
        result = {}
        groups = {}
        for aData in actions:
            if 'id' in aData:
                a = self._makeAction(aData['id'], aData)
                actionID = a.getID()
                if a.getType() == EVENT_TYPE.GROUP:
                    groups[actionID] = a
                    continue
                if not filterFunc(a):
                    continue
                result[actionID] = a

        for gID, group in groups.iteritems():
            for aID in group.getGroupEvents():
                if aID in result:
                    result[aID].setGroupID(gID)

        return result

    def _getActionsGroups(self, filterFunc = None):
        actions = self.__getActionsData()
        filterFunc = filterFunc or (lambda a: True)
        result = {}
        for aData in actions:
            if 'id' in aData:
                a = self._makeAction(aData['id'], aData)
                if a.getType() != EVENT_TYPE.GROUP:
                    continue
                if not filterFunc(a):
                    continue
                result[a.getID()] = a

        return result

    def _onResync(self, *args):
        self.__invalidateData()

    def _makeQuest(self, qID, qData, maker = _defaultQuestMaker, **kwargs):
        storage = self.__cache['quests']
        if qID in storage:
            return storage[qID]
        q = storage[qID] = maker(qID, qData, self.__questsProgress, **kwargs)
        return q

    def _makeAction(self, aID, aData):
        storage = self.__cache['actions']
        if aID in storage:
            return storage[aID]
        a = storage[aID] = createAction(aData.get('type', 0), aID, aData)
        return a

    @classmethod
    def _makeQuestsRelations(cls, quests):
        makeTokens = defaultdict(list)
        needTokens = defaultdict(list)
        for qID, q in quests.iteritems():
            if q.getType() != EVENT_TYPE.GROUP:
                tokens = q.getBonuses('tokens')
                if len(tokens):
                    for t in tokens[0].getTokens():
                        makeTokens[t].append(qID)

                for t in q.accountReqs.getTokens():
                    needTokens[qID].append(t.getID())

        children = defaultdict(dict)
        for parentID, tokensIDs in needTokens.iteritems():
            for tokenID in tokensIDs:
                children[parentID][tokenID] = makeTokens.get(tokenID, [])

        parents = defaultdict(dict)
        for parentID, tokens in children.iteritems():
            for tokenID, chn in tokens.iteritems():
                for childID in chn:
                    parents[childID][tokenID] = [parentID]

        return (children, parents)

    def __invalidateData(self, callback = lambda *args: None):
        self.__clearCache()
        self.__clearInvalidateCallback()
        self.__waitForSync = True
        self.onSyncStarted()

        def mergeValues(a, b):
            result = list(a)
            result.extend(b)
            return result

        for action in self.getActions().itervalues():
            for modifier in action.getModifiers():
                section = modifier.getSection()
                type = modifier.getType()
                itemType = modifier.getItemType()
                values = modifier.getValues(action)
                currentSection = self.__actionsCache[section][type]
                if itemType is not None:
                    currentSection = currentSection.setdefault(itemType, {})
                for k in values:
                    if k in currentSection:
                        currentSection[k] = mergeValues(currentSection[k], values[k])
                    else:
                        currentSection[k] = values[k]

        rareAchieves = set()
        invalidateTimeLeft = sys.maxint
        for q in self.getCurrentEvents().itervalues():
            dossierBonuses = q.getBonuses('dossier')
            if len(dossierBonuses):
                storage = self.__questsDossierBonuses[q.getID()]
                for bonus in dossierBonuses:
                    records = bonus.getRecords()
                    storage.update(records)
                    rareAchieves |= set((r for r in records if r[0] == ACHIEVEMENT_BLOCK.RARE))

            timeLeftInfo = q.getNearestActivityTimeLeft()
            if timeLeftInfo is not None:
                isAvailable, errorMsg = q.isAvailable()
                if not isAvailable:
                    if errorMsg in ('invalid_weekday', 'invalid_time_interval'):
                        invalidateTimeLeft = min(invalidateTimeLeft, timeLeftInfo[0])
                else:
                    intervalBeginTimeLeft, (intervalStart, intervalEnd) = timeLeftInfo
                    invalidateTimeLeft = min(invalidateTimeLeft, intervalBeginTimeLeft + intervalEnd - intervalStart)
            else:
                invalidateTimeLeft = min(invalidateTimeLeft, q.getFinishTimeLeft())

        g_rareAchievesCache.request(rareAchieves)
        for q in self.getFutureEvents().itervalues():
            timeLeftInfo = q.getNearestActivityTimeLeft()
            if timeLeftInfo is None:
                startTime = q.getStartTimeLeft()
            else:
                startTime = timeLeftInfo[0]
            invalidateTimeLeft = min(invalidateTimeLeft, startTime)

        if invalidateTimeLeft != sys.maxint:
            self.__loadInvalidateCallback(invalidateTimeLeft)
        self.__waitForSync = False
        self.onSyncCompleted()
        callback(True)
        from gui.shared import g_eventBus
        g_eventBus.handleEvent(events.LobbySimpleEvent(events.LobbySimpleEvent.EVENTS_UPDATED))
        return

    def __clearQuestsItemsCache(self):
        for qID, q in self._getQuests().iteritems():
            q.accountReqs.clearItemsCache()
            q.vehicleReqs.clearItemsCache()

    @classmethod
    def __getEventsData(cls, eventsTypeName):
        try:
            if isPlayerAccount():
                if eventsTypeName in BigWorld.player().eventsData:
                    return pickle.loads(zlib.decompress(BigWorld.player().eventsData[eventsTypeName]))
                return {}
            LOG_DEBUG('Trying to get quests data from not account player', eventsTypeName, BigWorld.player())
        except Exception:
            LOG_CURRENT_EXCEPTION()

        return {}

    def __getQuestsData(self):
        return self.__getEventsData(EVENT_CLIENT_DATA.QUEST)

    def __getFortQuestsData(self):
        return self.__getEventsData(EVENT_CLIENT_DATA.FORT_QUEST)

    def __getPersonalQuestsData(self):
        return self.__getEventsData(EVENT_CLIENT_DATA.PERSONAL_QUEST)

    def __getActionsData(self):
        return self.__getEventsData(EVENT_CLIENT_DATA.ACTION)

    def __getIngameEventsData(self):
        return self.__getEventsData(EVENT_CLIENT_DATA.INGAME_EVENTS)

    def __getEventBattles(self):
        return self.__getIngameEventsData().get('eventBattles', {})

    def __getCompanyBattlesData(self):
        return self.__getIngameEventsData().get('eventCompanies', {})

    def __getUnitRestrictions(self):
        return self.__getUnitData().get('restrictions', {})

    def __getUnitXpFactors(self):
        return self.__getUnitData().get('xpFactors', {})

    def __getFallout(self):
        return self.__getEventsData(EVENT_CLIENT_DATA.FALLOUT)

    def __getGasAttack(self):
        return self.__getEventsData(EVENT_CLIENT_DATA.INGAME_EVENTS).get('gasAttack', {})

    def __getUnitData(self):
        return self.__getEventsData(EVENT_CLIENT_DATA.SQUAD_BONUSES)

    def __getCommonQuestsIterator(self):
        questsData = self.__getQuestsData()
        questsData.update(self.__getFortQuestsData())
        questsData.update(self.__getPersonalQuestsData())
        questsData.update(self.__getPotapovHiddenQuests())
        for qID, qData in questsData.iteritems():
            yield (qID, self._makeQuest(qID, qData))

        currentESportSeasonID = g_lobbyContext.getServerSettings().eSportCurrentSeason.getID()
        eSportQuests = clubs_quests.g_cache.getLadderQuestsBySeasonID(currentESportSeasonID) or []
        for questDescr in eSportQuests:
            yield (questDescr.questID, self._makeQuest(questDescr.questID, questDescr.questData, maker=_clubsQuestMaker, seasonID=currentESportSeasonID, questDescr=questDescr))

        motiveQuests = motivation_quests.g_cache.getAllQuests() or []
        for questDescr in motiveQuests:
            yield (questDescr.questID, self._makeQuest(questDescr.questID, questDescr.questData, maker=_motiveQuestMaker))

    def __loadInvalidateCallback(self, duration):
        LOG_DEBUG('load quest window invalidation callback (secs)', duration)
        self.__clearInvalidateCallback()
        self.__invalidateCbID = BigWorld.callback(math.ceil(duration), self.__invalidateData)

    def __clearInvalidateCallback(self):
        if self.__invalidateCbID is not None:
            BigWorld.cancelCallback(self.__invalidateCbID)
            self.__invalidateCbID = None
        return

    def __clearCache(self):
        self.__questsDossierBonuses.clear()
        self.__actionsCache.clear()
        for storage in self.__cache.itervalues():
            storage.clear()

    def __getPotapovHiddenQuests(self):
        if not self.__potapovHidden:
            xmlPath = _POTAPOV_QUEST_XML_PATH + '/tiles.xml'
            for quest in readQuestsFromFile(xmlPath, EVENT_TYPE.TOKEN_QUEST):
                self.__potapovHidden[quest[0]] = quest[3]

        return self.__potapovHidden.copy()

    def __onLockedQuestsChanged(self):
        self.__lockedQuestIds = BigWorld.player().potapovQuestsLock


g_eventsCache = _EventsCache()