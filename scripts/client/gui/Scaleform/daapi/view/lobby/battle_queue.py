# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/battle_queue.py
import BigWorld
import weakref
from UnitBase import FALLOUT_QUEUE_TYPE_TO_ROSTER
import constants
import MusicControllerWWISE
from debug_utils import LOG_DEBUG
from gui import makeHtmlString
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ViewTypes
from gui.Scaleform.framework.managers.containers import POP_UP_CRITERIA
from gui.prb_control import prb_getters
from gui.prb_control.prb_helpers import preQueueFunctionalProperty, prbDispatcherProperty
from gui.server_events import g_eventsCache
from gui.shared import events
from gui.shared.event_bus import EVENT_BUS_SCOPE
from gui.sounds.ambients import LobbySubViewEnv
from helpers.i18n import makeString
from PlayerEvents import g_playerEvents
from gui.Scaleform.daapi import LobbySubView
from gui.Scaleform.daapi.view.meta.BattleQueueMeta import BattleQueueMeta
from shared_utils import findFirst
TYPES_ORDERED = (('heavyTank', '#item_types:vehicle/tags/heavy_tank/name'),
 ('mediumTank', '#item_types:vehicle/tags/medium_tank/name'),
 ('lightTank', '#item_types:vehicle/tags/light_tank/name'),
 ('AT-SPG', '#item_types:vehicle/tags/at-spg/name'),
 ('SPG', '#item_types:vehicle/tags/spg/name'))
DIVISIONS_ORDERED = (constants.PREBATTLE_COMPANY_DIVISION.JUNIOR,
 constants.PREBATTLE_COMPANY_DIVISION.MIDDLE,
 constants.PREBATTLE_COMPANY_DIVISION.CHAMPION,
 constants.PREBATTLE_COMPANY_DIVISION.ABSOLUTE)

class _QueueProvider(object):

    def __init__(self, proxy, qType = constants.QUEUE_TYPE.UNKNOWN):
        super(_QueueProvider, self).__init__()
        self._proxy = weakref.proxy(proxy)
        self._queueType = qType
        self._queueCallback = None
        return

    def start(self):
        g_playerEvents.onQueueInfoReceived += self.processQueueInfo
        self.requestQueueInfo()

    def stop(self):
        g_playerEvents.onQueueInfoReceived -= self.processQueueInfo
        if self._queueCallback is not None:
            BigWorld.cancelCallback(self._queueCallback)
            self._queueCallback = None
        self._queueType = constants.QUEUE_TYPE.UNKNOWN
        self._proxy = None
        return

    def getQueueType(self):
        return self._queueType

    def requestQueueInfo(self):
        self._queueCallback = None
        currPlayer = BigWorld.player()
        if currPlayer is not None and hasattr(currPlayer, 'requestQueueInfo'):
            LOG_DEBUG('Requestion queue info: ', self._queueType)
            currPlayer.requestQueueInfo(self._queueType)
            self._queueCallback = BigWorld.callback(5, self.requestQueueInfo)
        return

    def processQueueInfo(self, qInfo):
        pass


class _RandomQueueProvider(_QueueProvider):

    def processQueueInfo(self, qInfo):
        info = dict(qInfo)
        if 'classes' in info:
            vClasses = info['classes']
            vClassesLen = len(vClasses)
        else:
            vClasses = []
            vClassesLen = 0
        self._proxy.flashObject.as_setPlayers(makeHtmlString('html_templates:lobby/queue/playersLabel', 'players', {'count': sum(vClasses)}))
        if vClassesLen:
            data = {'title': '#menu:prebattle/typesTitle',
             'data': []}
            vClassesData = data['data']
            for vClass, message in TYPES_ORDERED:
                idx = constants.VEHICLE_CLASS_INDICES[vClass]
                vClassesData.append((message, vClasses[idx] if idx < vClassesLen else 0))

            self._proxy.as_setListByTypeS(data)
        self._proxy.as_showStartS(constants.IS_DEVELOPMENT and sum(vClasses) > 1)


class _CompanyQueueProvider(_QueueProvider):

    def processQueueInfo(self, qInfo):
        info = dict(qInfo)
        vDivisions = info['divisions']
        data = {'title': '#menu:prebattle/typesCompaniesTitle',
         'data': list()}
        self._proxy.flashObject.as_setPlayers(makeHtmlString('html_templates:lobby/queue/playersLabel', 'teams', {'count': sum(vDivisions)}))
        vDivisions = info['divisions']
        if vDivisions is not None:
            vClassesLen = len(vDivisions)
            for vDivision in DIVISIONS_ORDERED:
                data['data'].append(('#menu:prebattle/CompaniesTitle/%s' % constants.PREBATTLE_COMPANY_DIVISION_NAMES[vDivision], vDivisions[vDivision] if vDivision < vClassesLen else 0))

            self._proxy.as_setListByTypeS(data)
        self._proxy.as_showStartS(constants.IS_DEVELOPMENT)
        return


class _FalloutQueueProvider(_QueueProvider):

    def processQueueInfo(self, qInfo):
        info = dict(qInfo)
        vClasses = info.get('classes', [])
        vClassesLen = len(vClasses)
        totalPlayers = info.get('players', 0)
        self._proxy.flashObject.as_setPlayers(makeHtmlString('html_templates:lobby/queue/playersLabel', 'players', {'count': totalPlayers}))
        if vClassesLen:
            data = {'title': '#menu:prebattle/typesTitle',
             'data': []}
            vClassesData = data['data']
            for vClass, message in TYPES_ORDERED:
                idx = constants.VEHICLE_CLASS_INDICES[vClass]
                vClassesData.append((message, vClasses[idx] if idx < vClassesLen else 0))

            self._proxy.as_setListByTypeS(data)
        self._proxy.as_showStartS(constants.IS_DEVELOPMENT and sum(vClasses) > 1)


class _EventQueueProvider(_QueueProvider):

    def processQueueInfo(self, qInfo):
        info = dict(qInfo)
        totalPlayers = info.get('players', 0)
        self._proxy.flashObject.as_setPlayers(makeHtmlString('html_templates:lobby/queue/playersLabel', 'players', {'count': totalPlayers}))
        if g_eventsCache.isEventEnabled():
            data = {'title': '#menu:prebattle/typesTitle',
             'data': []}
            vClassesData = data['data']
            for vClass, message in TYPES_ORDERED:
                vClassesData.append((message, totalPlayers if g_eventsCache.getEventVehicles()[0].type == vClass else 0))

            self._proxy.as_setListByTypeS(data)
        self._proxy.as_showStartS(constants.IS_DEVELOPMENT and totalPlayers > 1)


_PROVIDER_BY_QUEUE_TYPE = {constants.QUEUE_TYPE.RANDOMS: _RandomQueueProvider,
 constants.QUEUE_TYPE.COMPANIES: _CompanyQueueProvider,
 constants.QUEUE_TYPE.FALLOUT_MULTITEAM: _FalloutQueueProvider,
 constants.QUEUE_TYPE.FALLOUT_CLASSIC: _FalloutQueueProvider,
 constants.QUEUE_TYPE.EVENT_BATTLES: _EventQueueProvider}

def _providerFactory(proxy, qType):
    return _PROVIDER_BY_QUEUE_TYPE.get(qType, _QueueProvider)(proxy, qType)


class BattleQueue(BattleQueueMeta, LobbySubView):
    __sound_env__ = LobbySubViewEnv

    def __init__(self, ctx = None):
        super(BattleQueue, self).__init__()
        self.__createTime = 0
        self.__timerCallback = None
        self.__provider = None
        return

    @preQueueFunctionalProperty
    def preQueueFunctional(self):
        return None

    @prbDispatcherProperty
    def prbDispatcher(self):
        return None

    def onEscape(self):
        dialogsContainer = self.app.containerManager.getContainer(ViewTypes.TOP_WINDOW)
        if not dialogsContainer.getView(criteria={POP_UP_CRITERIA.VIEW_ALIAS: VIEW_ALIAS.LOBBY_MENU}):
            self.fireEvent(events.LoadViewEvent(VIEW_ALIAS.LOBBY_MENU), scope=EVENT_BUS_SCOPE.LOBBY)

    def startClick(self):
        currPlayer = BigWorld.player()
        if currPlayer is not None and hasattr(currPlayer, 'createArenaFromQueue'):
            currPlayer.createArenaFromQueue()
        return

    def exitClick(self):
        if self.prbDispatcher is not None:
            self.prbDispatcher.exitFromQueue()
        return

    def onStartBattle(self):
        self.__stopUpdateScreen()

    def _populate(self):
        super(BattleQueue, self)._populate()
        g_playerEvents.onArenaCreated += self.onStartBattle
        self.__updateQueueInfo()
        self.__updateTimer()
        self.__updateClientState()
        MusicControllerWWISE.play(MusicControllerWWISE.MUSIC_EVENT_LOBBY)
        MusicControllerWWISE.play(MusicControllerWWISE.AMBIENT_EVENT_LOBBY)

    def _dispose(self):
        self.__stopUpdateScreen()
        g_playerEvents.onArenaCreated -= self.onStartBattle
        super(BattleQueue, self)._dispose()

    def __updateClientState(self):
        if self.prbDispatcher is not None:
            permissions = self.prbDispatcher.getUnitFunctional().getPermissions()
            if permissions and not permissions.canExitFromQueue():
                self.as_showExitS(False)
        guiType = prb_getters.getArenaGUIType(queueType=self.__provider.getQueueType())
        title = '#menu:loading/battleTypes/%d' % guiType
        description = '#menu:loading/battleTypes/desc/%d' % guiType
        if guiType != constants.ARENA_GUI_TYPE.UNKNOWN and guiType in constants.ARENA_GUI_TYPE_LABEL.LABELS:
            iconlabel = constants.ARENA_GUI_TYPE_LABEL.LABELS[guiType]
        else:
            iconlabel = 'neutral'
        self.as_setTypeInfoS(iconlabel, title, description)
        return

    def __stopUpdateScreen(self):
        if self.__timerCallback is not None:
            BigWorld.cancelCallback(self.__timerCallback)
            self.__timerCallback = None
        if self.__provider is not None:
            self.__provider.stop()
            self.__provider = None
        return

    def __updateQueueInfo(self):
        if prb_getters.isCompany():
            qType = constants.QUEUE_TYPE.COMPANIES
        elif self.prbDispatcher is not None and self.prbDispatcher.getFunctionalState().isInUnit():
            funcState = self.prbDispatcher.getFunctionalState()
            if funcState.entityTypeID == constants.PREBATTLE_TYPE.FALLOUT:
                rosterType = funcState.rosterType
                qType, _ = findFirst(lambda (k, v): v == rosterType, FALLOUT_QUEUE_TYPE_TO_ROSTER.iteritems(), (constants.QUEUE_TYPE.RANDOMS, None))
            elif funcState.entityTypeID == constants.PREBATTLE_TYPE.EVENT:
                qType = constants.QUEUE_TYPE.EVENT_BATTLES
            else:
                qType = constants.QUEUE_TYPE.RANDOMS
        else:
            qType = prb_getters.getQueueType()
        self.__provider = _providerFactory(self, qType)
        self.__provider.start()
        return

    def __updateTimer(self):
        self.__timerCallback = None
        self.__timerCallback = BigWorld.callback(1, self.__updateTimer)
        textLabel = makeString('#menu:prebattle/timerLabel')
        timeLabel = '%d:%02d' % divmod(self.__createTime, 60)
        self.flashObject.as_setTimer(textLabel, timeLabel)
        self.__createTime += 1
        return