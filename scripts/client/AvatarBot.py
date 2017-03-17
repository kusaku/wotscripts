# Embedded file name: scripts/client/AvatarBot.py
from debug_utils import LOG_DEBUG_DEV
import Avatar
import BigWorld
from config_consts import IS_DEVELOPMENT
if __debug__ and IS_DEVELOPMENT:
    import sys
    from os.path import dirname, join
    cd = dirname(__file__)
    sys.path.append(join(cd, '..', 'server_common', 'Bot', 'Agent', 'DecisionSystem'))
    try:
        from AIStateMachineData import AIState
    except:

        class AIState:

            def __getattr__(self, key):
                return 0

            def getStateName(self, *kargs, **kwargs):
                pass


class AvatarBot(Avatar.Avatar):
    _DEBUG = False
    _ENTITIES = []

    @staticmethod
    def setDebug(value):
        LOG_DEBUG_DEV('AvatarBot.setDebug', value)
        AvatarBot._DEBUG = value
        if not AvatarBot._DEBUG:
            for e in AvatarBot._ENTITIES:
                AvatarBot.clearDebugInfo(e)

    def onEnterWorld(self, prereqs):
        Avatar.Avatar.onEnterWorld(self, prereqs)
        AvatarBot._ENTITIES.append(self)
        self.__updateCallBack = None
        self.__update()
        return

    def onLeaveWorld(self):
        Avatar.Avatar.onLeaveWorld(self)
        AvatarBot._ENTITIES.remove(self)
        if self.__updateCallBack != None:
            BigWorld.cancelCallback(self.__updateCallBack)
            self.__updateCallBack = None
            AvatarBot.clearDebugInfo(self)
        return

    @staticmethod
    def clearDebugInfo(self):
        BigWorld.clearGroup('targetLine_' + str(self.id))
        BigWorld.clearGroup('movementLine_' + str(self.id))

    def __update(self):
        self.__updateCallBack = BigWorld.callback(0.001, self.__update)
        if IS_DEVELOPMENT and __debug__:
            AvatarBot.clearDebugInfo(self)
            if not self._DEBUG:
                return
            AvatarBot.renderDebugLines(self)

    @staticmethod
    def renderDebugLines(self):
        BigWorld.clearGroup('targetLine_' + str(self.id))
        BigWorld.clearGroup('movementLine_' + str(self.id))
        if hasattr(self, 'targetPoint') and self.targetPoint and self.targetPoint.length > 0:
            colors = {AIState.inState(self.AIState, AIState.ATTACK): 4294901760L,
             AIState.inState(self.AIState, AIState.IDLE): 4278190335L,
             AIState.inState(self.AIState, AIState.SURVIVE): 4278255360L}
            BigWorld.addDrawLine('targetLine_' + str(self.id), self.position, self.targetPoint, colors.get(True, 4294967295L), 2)
        if hasattr(self, 'movementDirection') and self.movementDirection and self.movementDirection.length > 0:
            BigWorld.addDrawLine('movementLine_' + str(self.id), self.position, self.position + self.movementDirection * 50, 4294967040L, 2)
        if hasattr(self, 'movePoint') and self.movePoint and self.movePoint.length > 0:
            BigWorld.addDrawLine('movementLine_' + str(self.id), self.position, self.movePoint, 4278255360L, 2)
        if hasattr(self, 'navigationPathData') and self.navigationPathData:
            AvatarBot.debugDrawSpline(self, self.navigationPathData)
        if hasattr(self, 'subTargetPoint') and self.subTargetPoint:
            AvatarBot.debugDrawDottedLine(self, self.position, self.subTargetPoint)

    @staticmethod
    def debugDrawSpline(self, data):
        for A, B in zip(data[:-1], data[1:]):
            BigWorld.addDrawLine('movementLine_{}'.format(self.id), A, B, 1996554018, True)

    @staticmethod
    def debugDrawDottedLine(self, start, end, size = 1, space = 0.3):
        """
        :type start: Vector3
        :type end: Vector3
        """
        length = (end - start).length
        direction = (end - start).getNormalized()
        for i in xrange(int(length / (size + space)) - 1):
            A = start + direction * i * (size + space)
            B = A + direction * size
            BigWorld.addDrawLine('movementLine_{}'.format(self.id), A, B, 124780544, False)

    @staticmethod
    def _getDebugInfo(self):
        data = [('id', self.id)]
        if hasattr(self, 'AIState'):
            data.append(('AIState', AIState.getStateName(self.AIState)))

        def safeAppend(attrName):
            if hasattr(self, attrName):
                data.append((attrName, getattr(self, attrName)))

        safeAppend('MovementSystemState')
        safeAppend('profile')
        safeAppend('targetDistance')
        safeAppend('turnAttackDistanceEnter')
        safeAppend('turnAttackDistanceExit')
        safeAppend('breakDistance')
        safeAppend('shootDistance')
        if hasattr(self, 'shootDistance'):
            data.append(('shootDistance', '{0} ({1},{2})'.format(self.shootDistance, self.startAttackDistance, self.stopAttackDistance)))
        if hasattr(self, 'flightStrategyName'):
            data.append(('Strategy', self.flightStrategyName))
        safeAppend('groupID')
        return data

    def getDebugInfo(self):
        return AvatarBot._getDebugInfo(self)