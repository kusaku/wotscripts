# Embedded file name: scripts/client/gui/prb_control/items/__init__.py
from collections import namedtuple
from UnitBase import ROSTER_TYPE
from constants import PREBATTLE_TYPE, QUEUE_TYPE
from gui.prb_control.items.prb_items import PlayerPrbInfo
from gui.prb_control.items.unit_items import PlayerUnitInfo
from gui.prb_control.settings import CTRL_ENTITY_TYPE, FUNCTIONAL_FLAG
from gui.shared.utils.decorators import ReprInjector

@ReprInjector.simple('ctrlTypeID', 'entityTypeID', 'hasModalEntity', 'hasLockedState', 'isIntroMode')

class FunctionalState(object):
    __slots__ = ('ctrlTypeID', 'entityTypeID', 'hasModalEntity', 'hasLockedState', 'isIntroMode', 'funcState', 'funcFlags', 'rosterType')

    def __init__(self, ctrlTypeID = 0, entityTypeID = 0, hasModalEntity = False, hasLockedState = False, isIntroMode = False, funcState = None, funcFlags = FUNCTIONAL_FLAG.UNDEFINED, rosterType = 0):
        super(FunctionalState, self).__init__()
        self.ctrlTypeID = ctrlTypeID
        self.entityTypeID = entityTypeID
        self.hasModalEntity = hasModalEntity
        self.hasLockedState = hasLockedState
        self.isIntroMode = isIntroMode
        self.funcState = funcState
        self.funcFlags = funcFlags
        self.rosterType = rosterType

    def isInPrebattle(self, prbType = 0):
        result = False
        if self.ctrlTypeID == CTRL_ENTITY_TYPE.PREBATTLE:
            if prbType:
                result = prbType == self.entityTypeID
            else:
                result = self.entityTypeID != 0
        return result

    def isInClubsPreArena(self):
        if self.isInUnit(PREBATTLE_TYPE.CLUBS) and self.funcState is not None:
            return self.funcState.isInPreArena()
        else:
            return False

    def isInSpecialPrebattle(self):
        return self.ctrlTypeID == CTRL_ENTITY_TYPE.PREBATTLE and self.entityTypeID in (PREBATTLE_TYPE.CLAN, PREBATTLE_TYPE.TOURNAMENT)

    def isInUnit(self, prbType = 0):
        result = False
        if self.ctrlTypeID == CTRL_ENTITY_TYPE.UNIT:
            if prbType:
                result = prbType == self.entityTypeID
            else:
                result = self.entityTypeID != 0
        return result

    def isInPreQueue(self, queueType = 0):
        result = False
        if self.ctrlTypeID == CTRL_ENTITY_TYPE.PREQUEUE:
            if queueType:
                result = queueType == self.entityTypeID
            else:
                result = self.entityTypeID != 0
        return result

    def isInFallout(self):
        return self.isInUnit(PREBATTLE_TYPE.FALLOUT) or self.funcFlags & FUNCTIONAL_FLAG.FALLOUT_BATTLES > 0

    def isQueueSelected(self, queueType):
        if self.isInPreQueue(queueType):
            return True
        if self.isInUnit(PREBATTLE_TYPE.SQUAD) and queueType == QUEUE_TYPE.RANDOMS:
            return True
        if self.isInUnit(PREBATTLE_TYPE.EVENT) and queueType == QUEUE_TYPE.EVENT_BATTLES:
            return True
        if self.isInUnit(PREBATTLE_TYPE.FALLOUT) and (queueType == QUEUE_TYPE.FALLOUT_CLASSIC and self.rosterType == ROSTER_TYPE.FALLOUT_CLASSIC_ROSTER or queueType == QUEUE_TYPE.FALLOUT_MULTITEAM and self.rosterType == ROSTER_TYPE.FALLOUT_MULTITEAM_ROSTER):
            return True
        return False

    def doLeaveToAcceptInvite(self, prbType = 0):
        result = False
        if self.hasModalEntity:
            if prbType and self.isIntroMode:
                result = prbType != self.entityTypeID
            else:
                result = True
        return result

    def isReadyActionSupported(self):
        return self.hasModalEntity and not self.isIntroMode and (self.isInPrebattle() or self.isInUnit())

    def isNavigationDisabled(self):
        return self.hasLockedState and (self.isInPreQueue() or self.isInPrebattle(PREBATTLE_TYPE.COMPANY) or self.isInUnit(PREBATTLE_TYPE.SQUAD) or self.isInUnit(PREBATTLE_TYPE.EVENT) or self.isInClubsPreArena())


@ReprInjector.simple('isCreator', 'isReady')

class PlayerDecorator(object):
    __slots__ = ('isCreator', 'isReady')

    def __init__(self, isCreator = False, isReady = False):
        self.isCreator = isCreator
        self.isReady = isReady


SelectResult = namedtuple('SelectResult', ('isProcessed', 'newEntry'))
SelectResult.__new__.__defaults__ = (False, None)
CreationResult = namedtuple('SelectResult', ('creationFlags', 'initFlags'))