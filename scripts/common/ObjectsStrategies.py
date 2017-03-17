# Embedded file name: scripts/common/ObjectsStrategies.py
import BigWorld
from AvatarControllerBase import AvatarControllerBase
import db.DBLogic
from EntityHelpers import EntityStates
import Math
from consts import *
from debug_utils import LOG_WARNING, LOG_ERROR
teamObjectStrategies = {'spline': lambda owner, objData: SplineMovementStrategy(owner, objData['movementStrategyDataPath'], objData['movementStrategyStartPosPrc']),
 'fall': lambda owner, objData: FallMovementStrategy(owner, objData['matrix'].applyToOrigin()),
 'static': lambda owner, objData: StaticStrategy(owner, objData['matrix']),
 'script': lambda owner, objData: VScriptMovementStrategy(owner, objData['matrix'])}

def selectTeamObjectStrategy(owner, arenaObjID, arenaID):
    arenaSettings = db.DBLogic.g_instance.getArenaData(arenaID)
    objData = arenaSettings.getTeamObjectData(arenaObjID)
    strategyName = objData['movementStrategyName']
    if strategyName not in teamObjectStrategies:
        if strategyName:
            LOG_WARNING('Unknown strategyName <{n}> for {id}. Use static as default'.format(n=strategyName, id=owner.id))
        strategyName = 'static'
    strategyInstance = teamObjectStrategies[strategyName](owner, objData)
    owner._registerController('movementStrategy', strategyInstance)


class MovementStrategyBaseClass(AvatarControllerBase):

    def __init__(self, owner):
        AvatarControllerBase.__init__(self, owner)
        self._matrixProvider = None
        return

    def restart(self):
        if IS_CELLAPP:
            self.setStartTime(self.isActive() and BigWorld.time() or 0)
            self.setPauseTime(0)

    def onDestruction(self):
        pass

    def isActive(self):
        return True

    def setPause(self, flag):
        if flag and IS_CELLAPP and self._owner.curStrategyPausedAt != 0:
            return
        if flag:
            self.setPauseTime(BigWorld.time())
        else:
            self.setStartTime(BigWorld.time() - (self._owner.curStrategyPausedAt - self._owner.curStrategyStartTime))
            self.setPauseTime(0)

    def setStartTime(self, t):
        if IS_CELLAPP:
            self._owner.curStrategyStartTime = t
        if self._matrixProvider:
            self._matrixProvider.startTime = t

    def setPauseTime(self, t):
        if IS_CELLAPP:
            self._owner.curStrategyPausedAt = t
        if self._matrixProvider:
            self._matrixProvider.pausedAt = t

    def createFilter(self):
        """Creates a position filter suitable for this Moving Strategy"""
        return BigWorld.MatrixProviderFilter(self._matrixProvider)

    @property
    def matrixProvider(self):
        return self._matrixProvider


class StaticStrategy(MovementStrategyBaseClass):

    def __init__(self, owner, matrix):
        MovementStrategyBaseClass.__init__(self, owner)
        if IS_CLIENT:
            m = Math.Matrix(matrix)
            self._owner.setupMP(m)
            self._matrixProvider = m
        else:
            self._owner.setRotationFromMatrix(matrix)
            self._owner.position = matrix.applyToOrigin()

    def setStartTime(self, t):
        pass

    def setPauseTime(self, t):
        pass


class SplineMovementStrategy(MovementStrategyBaseClass):

    def __init__(self, owner, splineName, startPosPrc):
        MovementStrategyBaseClass.__init__(self, owner)
        spline = db.DBLogic.g_instance.getSpline(splineName)
        self._matrixProvider = spline and BigWorld.SplineMatrixProvider(self._owner.curStrategyStartTime, self._owner.curStrategyPausedAt, spline.bwSpline, startPosPrc * spline.totalTime) or None
        if IS_CLIENT and self._matrixProvider:
            self._owner.setupMP(self._matrixProvider)
        return

    def isActive(self):
        return EntityStates.inState(self._owner, EntityStates.GAME)

    def update(self, dt):
        if self.isActive():
            if self._owner.curStrategyStartTime == 0:
                self.setStartTime(BigWorld.time())
            if self._matrixProvider:
                transformationMatrix = Math.Matrix(self._matrixProvider)
                self._owner.setRotationFromMatrix(transformationMatrix)
                try:
                    self._owner.position = transformationMatrix.translation
                except:
                    arenaSettings = db.DBLogic.g_instance.getArenaData(self._owner.arenaType)
                    objData = arenaSettings.getTeamObjectData(self._owner.arenaObjID)
                    LOG_ERROR(self._owner.id, 'Invalid spline position={pos}, splineName={splineName}, startPrc={startPrc}, splineTime={splineTime}, isPaused={isPaused}'.format(pos=transformationMatrix.translation, splineName=objData['movementStrategyDataPath'], startPrc=objData['movementStrategyStartPosPrc'], splineTime=BigWorld.time() - self._owner.curStrategyStartTime, isPaused=bool(self._owner.curStrategyPausedAt)))

    def onDestruction(self):
        self.setPause(True)


class FallMovementStrategy(MovementStrategyBaseClass):

    def __init__(self, owner, startPos):
        MovementStrategyBaseClass.__init__(self, owner)
        self._matrixProvider = BigWorld.FallMatrixProvider(self._owner.curStrategyStartTime, self._owner.curStrategyPausedAt, startPos, GRAVITY * WORLD_SCALING)
        if IS_CLIENT:
            self._owner.setupMP(self._matrixProvider)

    def restart(self):
        if IS_CELLAPP:
            MovementStrategyBaseClass.restart(self)
            self.__updatePosition()

    def isActive(self):
        return EntityStates.inState(self._owner, EntityStates.DESTROYED)

    def update(self, dt):
        if self.isActive():
            self.__updatePosition()

    def __updatePosition(self):
        transformationMatrix = Math.Matrix(self._matrixProvider)
        self._owner.position = transformationMatrix.translation

    def onDestruction(self):
        boundCollide = BigWorld.hm_collideSimple(self._owner.spaceID, self._owner.position, self._owner.position - Math.Vector3(0, 3000 * WORLD_SCALING, 0))
        if boundCollide:
            self._matrixProvider.lowY = boundCollide[0].y
            self.setStartTime(BigWorld.time())
        else:
            LOG_ERROR("Can't find collision under falling object", self._owner.arenaObjID, self._owner.position, self._owner.spaceID)


class VScriptMovementStrategy(MovementStrategyBaseClass):

    def __init__(self, owner, matrix):
        MovementStrategyBaseClass.__init__(self, owner)
        if IS_CLIENT:
            m = owner.matrix
            m.notModel = True
            self._owner.setupMP(m)
            self._matrixProvider = m
        else:
            self._owner.setRotationFromMatrix(matrix)
            self._owner.position = matrix.applyToOrigin()

    def setStartTime(self, t):
        pass

    def setPauseTime(self, t):
        pass

    def createFilter(self):
        """Creates a position filter suitable for this Moving Strategy"""
        return BigWorld.PredictionFilter()