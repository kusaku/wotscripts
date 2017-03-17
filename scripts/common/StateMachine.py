# Embedded file name: scripts/common/StateMachine.py
from os import name
from debug_utils import *

class StateBase(object):
    """
    Base class for states
    """

    def exit(self):
        """
        On exit
        """
        pass

    def enter(self):
        """
        On enter
        """
        pass

    def reEnter(self):
        """
        On reenter
        """
        pass


class StateMachine(object):
    """
    State machine
    """

    def __init__(self):
        self.__states = {}
        self.__curState = None
        self.__curStateId = None
        return

    @property
    def currentState(self):
        """
        Current state
        @return: State; see StateMachine.StateBase class
        """
        return self.__curState

    @property
    def currentStateId(self):
        """
        Current state id
        @return: state id
        """
        return self.__curStateId

    @property
    def statesCount(self):
        """
        States count
        @return: count
        """
        return len(self.__states)

    def addState(self, name, state):
        """
        Add state
        @param name: state name
        @param state: state
        """
        self.__states[name] = state

    def setState(self, id, params = None):
        """
        Sets new state
        @param id: state id
        """
        if self.__curState:
            self.__curState.exit()
        self.__curState = self.__states[id]
        self.__curStateId = id
        self.__curState.enter(params)

    def getState(self):
        """
        Get current state id
        @return: state id
        """
        return self.__curStateId

    def getStateObject(self, id):
        return self.__states[id]

    def getCurStateObject(self):
        return self.getStateObject(self.__curStateId)

    def reset(self):
        self.__curStateId = None
        return

    def _reEnterState(self, params = None):
        if self.__curState:
            self.__curState.reEnter(params)

    def updateStateAttr(self, id, attrName, value):
        """
        Update state attribute
        @param id: state id
        @param attrName: attribute name
        @param value: attribute value
        """
        if id in self.__states:
            state = self.__states[id]
            if hasattr(state, attrName):
                attr = getattr(state, attrName)
                if attr is not None:
                    attr(value)
                    return True
                LOG_WARNING("StateMachine: Can't set value for a state attribute (attribute is None): ", name)
        else:
            LOG_ERROR("StateMachine: Can't find state: ", id)
        return False


class State:

    def __init__(self):
        self.onEnterFun = None
        self.onLeaveFun = None
        return


class ExternalBitStateMachine:

    def __init__(self, setStateFun, getStateFun, onTransitionFun):
        self.__setStateFun = setStateFun
        self.__getStateFun = getStateFun
        self.__onTransitionFun = onTransitionFun
        self.__states = {}
        self.__transition = []

    def destroy(self):
        self.__setStateFun = None
        self.__getStateFun = None
        self.__onTransitionFun = None
        return

    def addState(self, stateID, enterFun, leaveFun):
        if stateID not in self.__states:
            self.__states[stateID] = State()
        self.__states[stateID].onEnterFun = enterFun
        self.__states[stateID].onLeaveFun = leaveFun

    def addTransition(self, fromStateID, toStateID, signalID, callback = None):
        self.__transition.append((fromStateID,
         toStateID,
         signalID,
         callback))

    def signal(self, signalID, data = None):
        if self.__getStateFun:
            curState = self.__getStateFun()
            for fromStateIDData, toStateIDData, signalIDData, callback in self.__transition:
                if curState & fromStateIDData != 0 and signalID & signalIDData != 0:
                    if curState != toStateIDData:
                        self.__onTransition(curState, toStateIDData, signalID, data)
                        if callback:
                            callback(data)
                    return

    def __onTransition(self, fromStateID, toStateID, signalID, data):
        if self.__onTransitionFun:
            self.__onTransitionFun(fromStateID, toStateID, signalID, data)
        self.setState(toStateID, data)

    def setState(self, stateID, data = None):
        curState = self.__getStateFun()
        if curState in self.__states and self.__states[curState].onLeaveFun:
            self.__states[curState].onLeaveFun(stateID)
        self.__setStateFun(stateID, data)
        if stateID in self.__states and self.__states[stateID].onEnterFun:
            self.__states[stateID].onEnterFun()

    def clearTransitions(self):
        self.__transition = []