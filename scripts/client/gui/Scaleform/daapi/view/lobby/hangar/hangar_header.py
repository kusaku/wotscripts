# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/hangar/hangar_header.py
import constants
from CurrentVehicle import g_currentVehicle
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.Scaleform.daapi.view.lobby.server_events import events_helpers
from gui.Scaleform.daapi.view.meta.HangarHeaderMeta import HangarHeaderMeta
from gui.Scaleform.genConsts.TOOLTIPS_CONSTANTS import TOOLTIPS_CONSTANTS
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.server_events.events_dispatcher import showEventsWindow
from gui.shared.ItemsCache import g_itemsCache
from gui.shared.formatters import text_styles, icons
from gui.shared.utils.functions import makeTooltip
from helpers import dependency
from helpers.i18n import makeString as _ms
from shared_utils import first
from skeletons.gui.server_events import IEventsCache
from skeletons.gui.game_control import IQuestsController

class WIDGET_PQ_STATE(object):
    """ State of the personal quests overall relatively to current vehicle.
    """
    DISABLED = 'disabled'
    UNAVAILABLE = 'unavailable'
    COMPLETED = 'completed'
    AVAILABLE = 'available'
    IN_PROGRESS = 'inprogress'
    AWARD = 'award'
    UNSUITABLE = (DISABLED, UNAVAILABLE, COMPLETED)
    NOT_SELECTED = (DISABLED,
     UNAVAILABLE,
     AVAILABLE,
     COMPLETED)


class WIDGET_BQ_STATE(object):
    """ State of the battle quests overall relatively to current vehicle.
    """
    AVAILABLE = 'available'
    DISABLED = 'disabled'
    ALL_DONE = 'all_done'


class LABEL_STATE(object):
    """ State of the counter label on the flag.
    """
    ACTIVE = 'active'
    EMPTY = 'empty'
    INACTIVE = 'inactive'
    ALL_DONE = 'all_done'


def _getPersonalQuestsTooltipData(state, **ctx):
    if state != WIDGET_PQ_STATE.IN_PROGRESS:
        return {'personalQuestsTooltip': makeTooltip(_ms(TOOLTIPS.personalQuestsTooltipHeader(state), **ctx), _ms(TOOLTIPS.personalQuestsTooltipBody(state), **ctx)),
         'personalQuestsTooltipIsSpecial': False}
    else:
        return {'personalQuestsTooltip': TOOLTIPS_CONSTANTS.PERSONAL_QUESTS_PREVIEW,
         'personalQuestsTooltipIsSpecial': True}


def _findPersonalQuestsState(eventsCache, vehicle):
    """ Find state of PQs with relation to current vehicle.
    
    Here we iterate over all personal quests looking for the most
    suitable state.
    
    In three states (DISABLED, UNAVAILABLE, AVAILABLE) we continue to
    search for a better option, once we encounter quest in state of
    progress or in state of having an available award, we stop immediately.
    
    :param eventsCache: instance of gui.server_events._EventsCache
    :param vehicle: instance of gui_items.Vehicle
    
    :return: tuple (WIDGET_PQ_STATE, quest, quest's chain, quest's tile)
    """
    state = WIDGET_PQ_STATE.DISABLED
    vehicleLvl = vehicle.level
    vehicleType = vehicle.type
    for tile in eventsCache.potapov.getTiles().itervalues():
        for chainID, chain in tile.getQuests().iteritems():
            if tile.getChainVehicleClass(chainID) != vehicleType:
                continue
            for quest in chain.itervalues():
                if vehicleLvl < quest.getVehMinLevel():
                    continue
                if quest.isFullCompleted(isRewardReceived=True):
                    if state == WIDGET_PQ_STATE.DISABLED:
                        state = WIDGET_PQ_STATE.COMPLETED
                    continue
                if state in WIDGET_PQ_STATE.UNSUITABLE:
                    state = WIDGET_PQ_STATE.UNAVAILABLE
                if quest.canBeSelected() and state in WIDGET_PQ_STATE.UNSUITABLE:
                    state = WIDGET_PQ_STATE.AVAILABLE
                if quest.isInProgress():
                    return (WIDGET_PQ_STATE.IN_PROGRESS,
                     quest,
                     chain,
                     tile)
                if quest.needToGetReward():
                    return (WIDGET_PQ_STATE.AWARD,
                     quest,
                     chain,
                     tile)

    return (state,
     None,
     None,
     None)


class HangarHeader(HangarHeaderMeta):
    """ This class is responsible for displaying current vehicle information
    and battle/personal quests widgets (those two flags on top of hangar).
    """
    _eventsCache = dependency.descriptor(IEventsCache)
    _questController = dependency.descriptor(IQuestsController)

    def __init__(self):
        super(HangarHeader, self).__init__()
        self._currentVehicle = None
        self._personalQuestID = None
        self._battleQuestId = None
        return

    def showPersonalQuests(self):
        showEventsWindow(eventID=self._personalQuestID, eventType=constants.EVENT_TYPE.POTAPOV_QUEST, doResetNavInfo=self._personalQuestID is None)
        return

    def showCommonQuests(self):
        showEventsWindow(eventID=self._battleQuestId, eventType=constants.EVENT_TYPE.BATTLE_QUEST)

    def showBeginnerQuests(self):
        showEventsWindow(eventID=self._battleQuestId, eventType=constants.EVENT_TYPE.TUTORIAL)

    def update(self, *args):
        self._personalQuestID = None
        if self._currentVehicle.isPresent():
            vehicle = self._currentVehicle.item
            isBeginner = self._questController.isNewbiePlayer()
            headerVO = {'tankType': '{}_elite'.format(vehicle.type) if vehicle.isElite else vehicle.type,
             'tankInfo': text_styles.concatStylesToMultiLine(text_styles.promoSubTitle(vehicle.shortUserName), text_styles.stats(MENU.levels_roman(vehicle.level))),
             'isPremIGR': vehicle.isPremiumIGR,
             'isVisible': True,
             'isBeginner': isBeginner}
            if isBeginner:
                headerVO.update(self.__getBeginnerQuestsVO())
            else:
                headerVO.update(self.__getBattleQuestsVO(vehicle))
                headerVO.update(self.__getPersonalQuestsVO(vehicle))
        else:
            headerVO = {'isVisible': False}
        self.as_setDataS(headerVO)
        return

    def _populate(self):
        super(HangarHeader, self)._populate()
        self._currentVehicle = g_currentVehicle
        self._eventsCache.onSyncCompleted += self.update
        self._eventsCache.onProgressUpdated += self.update
        g_clientUpdateManager.addCallbacks({'inventory.1': self.update,
         'stats.tutorialsCompleted': self.update})

    def _dispose(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self._eventsCache.onSyncCompleted -= self.update
        self._eventsCache.onProgressUpdated -= self.update
        self._currentVehicle = None
        self._personalQuestID = None
        super(HangarHeader, self)._dispose()
        return

    def __getBeginnerQuestsVO(self):
        completed = g_itemsCache.items.stats.tutorialsCompleted
        questsDescriptor = events_helpers.getTutorialEventsDescriptor()
        chapters = []
        for chapter in questsDescriptor:
            chapterStatus = chapter.getChapterStatus(questsDescriptor, completed)
            if chapterStatus != events_helpers.EVENT_STATUS.NOT_AVAILABLE and chapterStatus != events_helpers.EVENT_STATUS.COMPLETED:
                chapters.append(chapter)

        chapter = first(chapters)
        self._battleQuestId = chapter.getID() if chapter else None
        return {'beginnerQuestsLabel': str(len(chapters)),
         'beginnerQuestsIcon': RES_ICONS.MAPS_ICONS_LIBRARY_OUTLINE_BEGINNER,
         'beginnerQuestsTooltip': makeTooltip(chapter.getTitle(), chapter.getDescription()),
         'beginnerQuestsEnable': True}

    def __getBattleQuestsVO(self, vehicle):
        """ Get part of VO responsible for battle quests flag.
        """
        quests = self._questController.getQuestForVehicle(vehicle)
        totalCount = len(quests)
        completedQuests = len([ q for q in quests if q.isCompleted() ])
        if totalCount > 0:
            if completedQuests != totalCount:
                bqState = WIDGET_BQ_STATE.AVAILABLE
                commonQuestsIcon = RES_ICONS.questsStateIconOutline(WIDGET_BQ_STATE.AVAILABLE)
                label = _ms(MENU.hangarHeaderBattleQuestsLabel(LABEL_STATE.ACTIVE), total=totalCount - completedQuests)
                self._battleQuestId = first(quests).getID()
            else:
                bqState = WIDGET_BQ_STATE.ALL_DONE
                commonQuestsIcon = RES_ICONS.questsStateIconOutline(WIDGET_BQ_STATE.AVAILABLE)
                label = icons.makeImageTag(RES_ICONS.MAPS_ICONS_LIBRARY_OUTLINE_QUESTS_ALL_DONE)
                self._battleQuestId = first(quests).getID() if quests else None
        else:
            bqState = WIDGET_BQ_STATE.DISABLED
            commonQuestsIcon = RES_ICONS.questsStateIconOutline(WIDGET_BQ_STATE.DISABLED)
            label = ''
        return {'commonQuestsLabel': label,
         'commonQuestsIcon': commonQuestsIcon,
         'commonQuestsTooltip': TOOLTIPS_CONSTANTS.QUESTS_PREVIEW,
         'commonQuestsEnable': bqState != WIDGET_BQ_STATE.DISABLED}

    def __getPersonalQuestsVO(self, vehicle):
        """ Get part of VO responsible for personal quests flag.
        """
        pqState, quest, chain, tile = _findPersonalQuestsState(self._eventsCache, vehicle)
        isReward = False
        if pqState == WIDGET_PQ_STATE.AVAILABLE:
            icon = RES_ICONS.MAPS_ICONS_LIBRARY_OUTLINE_PLUS
        elif pqState == WIDGET_PQ_STATE.AWARD:
            icon = RES_ICONS.MAPS_ICONS_LIBRARY_OUTLINE_REWARD
            isReward = True
        elif pqState == WIDGET_PQ_STATE.DISABLED:
            icon = RES_ICONS.vehicleTypeInactiveOutline(vehicle.type)
        else:
            icon = RES_ICONS.vehicleTypeOutline(vehicle.type)
        if pqState == WIDGET_PQ_STATE.DISABLED:
            labelState = LABEL_STATE.INACTIVE
        elif pqState == WIDGET_PQ_STATE.AVAILABLE:
            labelState = LABEL_STATE.EMPTY
        elif pqState in WIDGET_PQ_STATE.UNSUITABLE:
            labelState = LABEL_STATE.ALL_DONE
        else:
            labelState = LABEL_STATE.ACTIVE
        ctx = {}
        if all((quest, chain, tile)):
            self._personalQuestID = quest.getID()
            chainType = tile.getChainMajorTag(quest.getChainID())
            ctx.update({'current': len(filter(lambda q: q.isCompleted(), chain.itervalues())),
             'total': len(chain),
             'tileName': tile.getUserName(),
             'chainName': _ms(MENU.classesShort(chainType))})
        else:
            self._personalQuestID = None
            ctx.update({'icon': icons.makeImageTag(RES_ICONS.MAPS_ICONS_LIBRARY_OUTLINE_QUESTS_ALL_DONE)})
        res = {'personalQuestsLabel': _ms(MENU.hangarHeaderPersonalQuestsLabel(labelState), **ctx),
         'personalQuestsIcon': icon,
         'personalQuestsEnable': pqState != WIDGET_PQ_STATE.DISABLED,
         'isPersonalReward': isReward}
        res.update(_getPersonalQuestsTooltipData(pqState, **ctx))
        return res