# Embedded file name: scripts/client/VOIP/Fsm.py
import re
import inspect

class _NameHelper:
    """ Helper for automatic extraction of event IDs from handler method names.
        Naming conventions are the following:
        - event IDs must be uppercase, words separated by underscores (e.g. ENABLED_FLAG_CHANGED);
        - event handler method name must be the same as event ID converted to CamelCase,
          with 'on' added at the beginning (e.g. onEnabledFlagChanged).
    """
    __regex = re.compile('(.)([A-Z])')

    @staticmethod
    def eventNameFromHandlerName(methodName):
        return _NameHelper.__regex.sub('\\1_\\2', methodName[2:]).upper()


class Fsm(object):
    """ Simple finite state machine. Should be used as a base class. """

    def __init__(self, states, events, initialState):
        """ FSM constructor.
        @param states:       dict, mapping state IDs to classes
        @param events:       enum-class containing supported event IDs
        @param initialState: state ID in which the FSM starts (from statesTable keys)
        """
        self.__unstable = True
        self.__factory = states
        self._events = events
        self.__handlingEvent = False
        self.__deferredEvents = []
        self.__stateID = initialState
        self.__state = self.__factory[initialState](self)
        self.__unstable = False

    def shutdown(self):
        self.__state.leave(self)
        self.__state._shutdown()
        self.__state = None
        return

    @property
    def stateID(self):
        return self.__stateID

    @property
    def __unstable(self):
        return self.__unstableFlag

    @__unstable.setter
    def __unstable(self, value):
        self.__unstableFlag = value
        if not value:
            while self.__deferredEvents:
                deferredEvents = self.__deferredEvents
                self.__deferredEvents = []
                for event, kwargs in deferredEvents:
                    self.processEvent(event, **kwargs)

    def processEvent(self, event, **kwargs):
        """ Call to inject an event into the FSM.
            Event will be handled by the current state, possibly causing transition to another state.
            If the FSM is unstable (i.e. during a transition), event will be deferred until it is stable again.
        
        @param event:  event ID
        @param kwargs: event-specific keyword arguments
        """
        if self.__unstable:
            self.__deferredEvents.append((event, kwargs))
        else:
            wasHandlingEvent = self.__handlingEvent
            self.__handlingEvent = True
            self.__state.processEvent(self, event, **kwargs)
            self.__handlingEvent = wasHandlingEvent

    def _transit(self, stateID, **kwargs):
        """ Transit FSM from current state to another one.
            Must only be called by event classes and only during processEvent.
        
        @param stateID: target state ID
        @param kwargs:  keyword parameters for target state (state-specific)
        """
        if not self.__handlingEvent or self.__unstable:
            raise RuntimeError('FSM transition denied')
        self.__unstable = True
        oldStateID = self.__stateID
        self.__state.leave(self)
        self.__state._shutdown()
        self.__stateID = stateID
        self.__state = self.__factory[stateID](self, **kwargs)
        self.onStateChange(oldStateID, stateID)
        self.__unstable = False

    def onStateChange(self, oldStateID, newStateID):
        """ Called after each FSM state change. Intended for override by derived class.
            Not called for initial state.
        
        @param oldStateID: previous state ID
        @param newStateID: new state ID
        """
        pass


class StateBase(object):
    """ Base class for all FSM states. """

    def __init__(self, fsm):
        """ State constructor. Must be called by all derived classes,
            regardless of their own initialization logic.
        """
        self._handlers = {}
        for methodName, method in inspect.getmembers(self, inspect.ismethod):
            if methodName.startswith('on'):
                eventName = _NameHelper.eventNameFromHandlerName(methodName)
                event = fsm._events.__dict__[eventName]
                self._handlers[event] = method

    def _shutdown(self):
        self._handlers.clear()

    def leave(self, fsm):
        """ State 'destructor'. Called before transition to another state.
            Empty by default; should be overridden by derived classes as needed.
        """
        pass

    def processEvent(self, fsm, event, **kwargs):
        """ Generic event handler. Automatically invokes event-specific handler from derived class.
            Must not be overridden.
        
        @param fsm:    Fsm object owning this state
        @param event:  event ID
        @param kwargs: event-specific keyword arguments
        """
        handler = self._handlers.get(event, None)
        if handler is not None:
            handler(fsm, **kwargs)
        return