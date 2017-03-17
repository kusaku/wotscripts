# Embedded file name: scripts/common/exchangeapi/EventUtils.py
from exchangeapi.IfaceUtils import getIface, IfaceNotFound
from exchangeapi.CommonUtils import import_string
from debug_utils import LOG_ERROR, LOG_MX_DEV
from consts import IS_CLIENT, SERVER_TICK_LENGTH
import operator
import BigWorld
from functools import partial
import collections
DEFAULT_IFACE_NAME = 'IInterface'
EventDB = None
QUANTUM_EVENT_HANDLER_LIMIT = 85
LOG_EVENT = False

class Handler(object):

    def __init__(self, target, priority = 0):
        self.target = target
        self.priority = priority

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

    def __eq__(self, other):
        return operator.eq(self.target, other.target)

    def run(self, event):
        self.target(event)


class HandlerList(list):

    def __contains__(self, item):
        for _item in self.__iter__():
            if item == _item:
                return True

        return False


class Event(object):

    def __init__(self, name, iface, idTypeList, account, ob, prevob):
        self.name = name
        self.iface = iface
        self.ob = ob
        self.prevob = prevob
        self.account = account
        self.idTypeList = idTypeList


def initDB():
    global EventDB
    if EventDB is None:
        from exchangeapi._handlers import Handlers
        EventDB = {}
        defaultHandlers = {}
        for item in Handlers.handler:
            if item.scope in ['all', IS_CLIENT and 'client' or 'server']:
                handler = Handler(import_string(item), item.priority)
                for eventName in item.eventName:
                    handlers = EventDB.setdefault('%s:%s' % (eventName, item.ifaceName), HandlerList())
                    defaultHandlers[eventName] = None
                    if handler not in handlers:
                        handlers.append(handler)

        for eventName in set(defaultHandlers):
            defaultHandlers[eventName] = EventDB.pop('%s:%s' % (eventName, DEFAULT_IFACE_NAME), HandlerList())

        for dbID, handlers in EventDB.iteritems():
            eventName = dbID.split(':')[0]
            default = defaultHandlers.get(eventName, HandlerList())
            for handler in default:
                if handler not in handlers:
                    handlers.append(handler)

            handlers.sort(reverse=True)

        from _ifaces import Ifaces
        for eventName, handlers in defaultHandlers.iteritems():
            for iface in Ifaces.iface:
                iD = '%s:%s' % (eventName, iface.ifacename)
                if iD not in EventDB:
                    EventDB[iD] = handlers

    return


initDB()

def getEventHandlers(event):
    return EventDB.get('%s:%s' % (event.name, event.iface.ifacename), HandlerList())


def serverProcessEventHandlers(event, handlers, start = True):
    _processHandlers(0, 0, event, handlers, start)


def clientProcessEventHandlers(event, handlers):
    if handlers:
        handlers.popleft().run(event)
        BigWorld.callback(0, partial(clientProcessEventHandlers, event, handlers))


processEventHandlers = IS_CLIENT and clientProcessEventHandlers or serverProcessEventHandlers

def eventManager(event):
    handlers = collections.deque(getEventHandlers(event))
    if handlers:
        processEventHandlers(event, handlers)


def generateEvent(method, eventName, ifaceName, idTypeList, account, ob, prevob = None):
    ifaceNameList = ifaceName.split(':')
    if method == 'view' and len(ifaceNameList) > 1 and len(set(ifaceNameList)) > 1:
        return
    try:
        eventManager(Event(eventName, getIface(ifaceName), idTypeList, account, ob, prevob))
        if LOG_EVENT:
            LOG_MX_DEV('Event {0} for iface {1} generated'.format(eventName, ifaceName))
    except IfaceNotFound as msg:
        LOG_ERROR('Event {0} for iface {1} generation error: {2}'.format(eventName, ifaceName, msg))


def _processHandlers(iD, userArg, event, handlers, start):
    if iD:
        BigWorld.delTimer(iD)
        event.account.exchangeapiHelper.handlerTimerIDs.remove(iD)
    if not start:
        while handlers and BigWorld.quantumPassedPercent() < QUANTUM_EVENT_HANDLER_LIMIT:
            handlers.popleft().run(event)

    if handlers:
        timerID = BigWorld.addTimer(partial(_processHandlers, event=event, handlers=handlers, start=False), SERVER_TICK_LENGTH * (BigWorld.quantumPassedPercent() + 5) / 100)
        event.account.exchangeapiHelper.handlerTimerIDs.append(timerID)