# Embedded file name: scripts/client/modelManipulator/CompoundBuilder.py
import BigWorld
import CompoundSystem
import Math
import consts
import HierarchyWorker
import db.DBLogic
import math
import debug_utils
import PartAnimator2
from db.DBEffects import Effects
from audio import EffectSound
INVALID_ID = 4294967295L

class DrawObjectBase(object):
    """Base class for part of compound object"""

    def __init__(self, context, objId, partName = None):
        self.__visible = False
        self._context = context
        self.id = objId
        self.partName = partName

    def _onVisibleChange(self, visible):
        pass

    @property
    def isVisible(self):
        return self.__visible

    def onVisibleChange(self, visible):
        self.__visible = visible
        if self._context.isLoaded:
            self._onVisibleChange(visible)


class ModelObject(DrawObjectBase):

    def _onVisibleChange(self, visible):
        CompoundSystem.changeModelVisibility(self._context.cidProxy.handle, self.id, 1 if visible else 0)
        attachedIK = self._context.ikSystemByPart.get(self.partName, None)
        if attachedIK is not None:
            attachedIK.refresh()
        return


class ModelAnimation(DrawObjectBase):

    def _onVisibleChange(self, visible):
        if visible:
            if self._context.curTimeAction:
                parentQueue = CompoundSystem.getModelAction(self._context.cidProxy.handle, self.id, self.animtionNames[0])()
                for animName in self.animtionNames[1:]:
                    try:
                        parentQueue = parentQueue.action(animName)()
                    except ValueError:
                        debug_utils.LOG_ERROR('Animation %s not found for model %s' % (animName, self.mainModel.modelName))

            elif CompoundSystem.getModelAction(self._context.cidProxy.handle, self.id, self.animtionNames[-1])() is None:
                debug_utils.LOG_ERROR('Animation %s not found for model %s' % self.animtionNames[-1])
        return


class SoundObject(DrawObjectBase):

    def __init__(self, context, idObj, sound):
        DrawObjectBase.__init__(self, context, idObj)
        self.__sound = sound

    def _onVisibleChange(self, visible):
        if self.__sound:
            if visible:
                self.__sound[2] = EffectSound(self.__sound[1], self._context.cidProxy.handle, self.__sound[0])
            elif self.__sound[2]:
                self.__sound[2].stop()


class EffectObject(SoundObject):

    def _onVisibleChange(self, visible):
        SoundObject._onVisibleChange(self, visible)
        if visible or consts.IS_EDITOR or self.instantHide:
            CompoundSystem.changeParticleVisible(self._context.cidProxy.handle, self.id, visible)
        CompoundSystem.changeParticleActive(self._context.cidProxy.handle, self.id, visible)


class LoftEffectObject(SoundObject):

    def _onVisibleChange(self, visible):
        SoundObject._onVisibleChange(self, visible)
        CompoundSystem.changeLoftActive(self._context.cidProxy.handle, self.id, visible)


class TimeEffectObject(SoundObject):

    @property
    def isVisible(self):
        return super(TimeEffectObject, self).isVisible and self._context.curTimeAction

    def _onVisibleChange(self, visible):
        SoundObject._onVisibleChange(self, visible)
        if visible or consts.IS_EDITOR:
            CompoundSystem.changeParticleVisible(self._context.cidProxy.handle, self.id, visible)
            CompoundSystem.forceParticle(self._context.cidProxy.handle, self.id, 1)


class PropellerObject(DrawObjectBase):

    def __init__(self, context, idObj, modelsCount):
        DrawObjectBase.__init__(self, context, idObj)
        self.__modelsCount = modelsCount

    def _onVisibleChange(self, visible):
        for modeId in range(self.id, self.id + self.__modelsCount):
            CompoundSystem.changeModelVisibility(self._context.cidProxy.handle, modeId, 1 if visible else 0)

    def onItemVisibleChange(self, itemId, visible):
        CompoundSystem.changeModelVisibility(self._context.cidProxy.handle, self.id + itemId, 1 if visible and self.isVisible else 0)


class DropModelObject(DrawObjectBase):
    SIDE_DROP_SPEED = 0.5
    DROP_PART_ROTATION_SPEED = math.radians(50.0)

    def _onVisibleChange(self, visible):
        active = self._context.curTimeAction and visible and self._context.cidProxy.handle != INVALID_ID
        CompoundSystem.changeCompoundActive(self.cid, 1 if active else 0)
        if active:
            CompoundSystem.modelCopyParms(self.cid, self._context.cidProxy.handle)
            selfMatrix = CompoundSystem.getNodeMatrix(self._context.cidProxy.handle, self.id)
            mainMatrix = Math.Matrix(self._context.rootMP)
            self.matrix.setMatrix(selfMatrix)
            sideVelocity = Math.Vector3(0, 0, 0)
            sideVelocity = selfMatrix.translation - mainMatrix.translation
            if sideVelocity.length > 0.0:
                sideVelocity.normalise()
                sideVelocity *= DropModelObject.SIDE_DROP_SPEED
            self.matrix.velocity = self._context.velocity + sideVelocity
            self.matrix.acceleration = Math.Vector3(0, -9.8, 0) * consts.WORLD_SCALING
            rotationSpeed = Math.Quaternion()
            rotationSpeed.fromAngleAxis(DropModelObject.DROP_PART_ROTATION_SPEED, Math.Vector3(1.0, 1.0, 0.0))
            self.matrix.rotationSpeed = rotationSpeed


MODEL_NAME_SUFIX = '.model'
VISUAL_NAME_SUFIX = '.visual'

def _loadVisual(dataSection, hpMap, parentTransform = None, allnodes = False):
    identifier = dataSection.readString('identifier', '')
    transform = None
    if allnodes or identifier.startswith('HP_'):
        transform = dataSection.readMatrix('transform')
        if parentTransform:
            transform.preMultiply(parentTransform)
        hpMap[identifier] = transform
    for item in dataSection.values():
        if item.name == 'node':
            if transform is None and dataSection.name == 'node':
                transform = dataSection.readMatrix('transform')
                if parentTransform:
                    transform.preMultiply(parentTransform)
            _loadVisual(item, hpMap, transform, allnodes)

    return


def convertPath(path):
    return path.strip('/').split('/')


def _getVisualName(modelName):
    return modelName[:-len(MODEL_NAME_SUFIX)] + VISUAL_NAME_SUFIX


def syncHpMap(modelName, allnodes = False):
    import ResMgr
    visualName = _getVisualName(modelName)
    xml = ResMgr.openSection(visualName, False)
    hpMap = dict()
    if xml is not None:
        _loadVisual(xml, hpMap, None, allnodes)
    else:
        debug_utils.LOG_ERROR("Can't load visual file{0}".format(visualName))
    ResMgr.purge(visualName)
    return hpMap


class ObjectsBuilder:
    """
    Build compound object 
    """

    def __init__(self, animationController, boolCombiner, eventSystem, context, onLoadedCallback):
        self.__compoundsForLoad = 0
        self.__context = context
        self.__context.isLoaded = False
        self.__boolCombiner = boolCombiner
        self.__eventSystem = eventSystem
        self.__animationController = animationController
        self.__onLoadedCallback = onLoadedCallback
        self.__visualForLoading = dict()
        self.__drawObjects = []
        self.__rootNode = HierarchyWorker.MainHierarchyNode()
        self.__modelsList = []
        self.__particleList = []
        self.__matrixProviderList = []
        self.__animationsList = []
        self.__loftList = []
        self.__fashions = []
        self.__iks = {}
        self.__dropModels = []
        self.__flamePaths = []

    @property
    def _animationController(self):
        return self.__animationController

    def __registerDrawObj(self, drawObj):
        self.__drawObjects.append((drawObj, drawObj.isVisible))

    def addController(self, path, controllerName):
        node = self.__rootNode.resolvePath(convertPath(path))
        controller = self.__animationController.getController(controllerName)
        if controller:
            matrixProvider = controller.matrixProvider
            self.__matrixProviderList.append((node.id, matrixProvider))
        else:
            debug_utils.LOG_ERROR("Unregistered animation controller '%s' for %s" % (controllerName, self.__context.objDBData.name))

    def addModel(self, path, visibleCondition, resourceName, animationName = None, partName = None):
        if not resourceName:
            return
        node = self.__rootNode.resolvePath(convertPath(path))
        visualName = _getVisualName(resourceName)
        self.__visualForLoading.setdefault(visualName, []).append(node.hardpoints)
        modelObject = ModelObject(self.__context, len(self.__modelsList), partName)
        self.__boolCombiner.addObject(visibleCondition, modelObject.onVisibleChange)
        self.__modelsList.append((node.id, modelObject.isVisible, resourceName))
        self.__registerDrawObj(modelObject)
        if animationName:
            animation = ModelAnimation(self.__context, modelObject.id)
            animation.animtionNames = animationName.split(',')
            self.__boolCombiner.addObject(visibleCondition, animation.onVisibleChange)
            self.__animationsList.append(animation)
            self.__registerDrawObj(animation)
            animation.onVisibleChange(False)

    def addHangarPropeller(self, path, visibleCondition, rotorModel, meshModel, leftDirection):
        nodeId = self.__rootNode.resolvePath(convertPath(path)).id
        animator = self.__animationController.getController('PropellorControllerL' if leftDirection else 'PropellorControllerR')
        self.__matrixProviderList.append((nodeId, animator.matrixProvider))
        propeller = PropellerObject(self.__context, len(self.__modelsList), 2)
        self.__boolCombiner.addObject(visibleCondition, propeller.onVisibleChange)
        self.__modelsList.append((nodeId, propeller.isVisible, rotorModel))
        self.__modelsList.append((nodeId, propeller.isVisible, meshModel))
        self.__registerDrawObj(propeller)

    def addPropeller(self, path, visibleCondition, brokenCondition, rotorModel, meshModel, normalTextureModel, forsageModel, leftDirection):
        nodeId = self.__rootNode.resolvePath(convertPath(path)).id
        animator = self.__animationController.getController('PropellorControllerL' if leftDirection else 'PropellorControllerR')
        self.__matrixProviderList.append((nodeId, animator.matrixProvider))
        propeller = PropellerObject(self.__context, len(self.__modelsList), 4)
        animator.callback += propeller.onItemVisibleChange
        self.__boolCombiner.addObject(visibleCondition, propeller.onVisibleChange)
        self.__boolCombiner.addObject(brokenCondition, animator.setBroken)
        self.__modelsList.append((nodeId, propeller.isVisible, rotorModel))
        self.__modelsList.append((nodeId, propeller.isVisible, meshModel))
        self.__modelsList.append((nodeId, propeller.isVisible, normalTextureModel))
        self.__modelsList.append((nodeId, propeller.isVisible, forsageModel))
        self.__fashions.extend([ (propeller.id + modelId + 1, animator.fashions[modelId], []) for modelId in range(3) ])
        self.__registerDrawObj(propeller)

    def addIK(self, ikData, partName):
        self.__iks[partName] = ikData

    def loadIKs(self, cid):
        nodeIdsMapping = [ i[0] for i in self.__modelsList ]
        for partName, ikData in self.__iks.iteritems():
            for data in ikData:
                if data:
                    ikSys = BigWorld.IKConstraintSystem()
                    actuators = self.__findModel(partName)
                    linkedModels = ikSys.buildIKSystem(data, cid, actuators, nodeIdsMapping)
                    self.__context.ikSystemByPart[partName] = ikSys
                    if linkedModels and len(linkedModels) > 0:
                        for modelId in linkedModels:
                            hierarchyUpdates = []
                            linearHierarchy = self.__rootNode.linearHierarchy
                            for parentId, node in linearHierarchy:
                                if parentId == self.__modelsList[modelId][0]:
                                    try:
                                        hierarchyUpdates.append((node.id, node.name))
                                    except HierarchyWorker.HardpointNotFound:
                                        debug_utils.LOG_WARNING_DEBUG('Hardpoint not found "{0}" in object "{1}, {2}"'.format(node.path, self.__context.objDBData.name, getattr(self.__context.objDBData, 'fileName', '')))

                            if modelId not in actuators:
                                CompoundSystem.setModelFashion(cid, modelId, ikSys)
                            CompoundSystem.setModelNodeSyncList(cid, modelId, hierarchyUpdates)

                        self.__context.ikSystems.append(ikSys)
                    else:
                        debug_utils.LOG_WARNING('loadIKs - cant build complete IK model')

    def addGunnerHeadModel(self, path, visibleCondition, model, partName, settings, entityId):
        if not model:
            return
        parentNode = self.__rootNode.resolvePath(convertPath(path))
        nodeId = parentNode.id
        modelObject = ModelObject(self.__context, len(self.__modelsList), partName)
        self.__boolCombiner.addObject(visibleCondition, modelObject.onVisibleChange)
        visualName = _getVisualName(model)
        self.__visualForLoading.setdefault(visualName, []).append(parentNode.hardpoints)
        self.__modelsList.append((nodeId, modelObject.isVisible, model))
        self.__registerDrawObj(modelObject)
        animator = self.__animationController.getController('GunnerHeadController')
        tracker = animator.createTracker(nodeId, modelObject.id, settings, entityId)
        if tracker:
            self.__fashions.append((modelObject.id, tracker.tracker, []))
            out_tracker = tracker
        return out_tracker

    def addFirePoint(self, path, uniqueId):
        node = self.__rootNode.resolvePath(convertPath(path))
        self.__flamePaths.append((node.id, uniqueId, path))

    def addTurret(self, path, visibleCondition, gunnerId, model, turretSettings, partName):
        if not model:
            return
        else:
            out_tracker = None
            parentNode = self.__rootNode.resolvePath(convertPath(path))
            nodeId = parentNode.id
            gunIds = []
            flameNodes = []
            for firePoint in self.__flamePaths:
                fireNodePath = convertPath(firePoint[2])
                fireNode = self.__rootNode.resolvePath(fireNodePath)
                if fireNode in parentNode.childs.values():
                    flameNodes.append(fireNode.path)
                    gunIds.append(firePoint[1])

            modelObject = ModelObject(self.__context, len(self.__modelsList), partName)
            self.__boolCombiner.addObject(visibleCondition, modelObject.onVisibleChange)
            visualName = _getVisualName(model)
            self.__visualForLoading.setdefault(visualName, []).append(parentNode.hardpoints)
            self.__modelsList.append((nodeId, modelObject.isVisible, model))
            self.__registerDrawObj(modelObject)
            animator = self.__animationController.getController('TurretController')
            tracker = animator.createTracker(nodeId, gunnerId, turretSettings, gunIds, path)
            if tracker and tracker.tracker is not None:
                self.__fashions.append((modelObject.id, tracker.tracker, flameNodes))
                out_tracker = tracker
            return out_tracker

    def addDropModel(self, path, visibleCondition, resourceName):
        node = self.__rootNode.resolvePath(convertPath(path))
        modelObject = DropModelObject(self.__context, node.id)
        self.__boolCombiner.addObject(visibleCondition, modelObject.onVisibleChange)
        visualName = resourceName[:-len(MODEL_NAME_SUFIX)] + VISUAL_NAME_SUFIX
        hardpoints = dict()
        self.__visualForLoading.setdefault(visualName, []).append(hardpoints)
        self.__dropModels.append((modelObject, hardpoints, resourceName))
        self.__registerDrawObj(modelObject)

    def addParticle(self, path, playId, particleFileOrFiles):
        particlesList = particleFileOrFiles if isinstance(particleFileOrFiles, list) else [particleFileOrFiles]
        node = self.__rootNode.resolvePath(convertPath(path))
        firstObjID = len(self.__particleList)
        from functools import partial
        listener = partial(self.__selectAndPlayParticle, particlesList, firstObjID)
        self.__eventSystem.addListener(playId, listener)
        for particleFile in particlesList:
            self.addParticleToList(node.id, True, particleFile, particleFile)

    def addParticleToList(self, nodeId, isVisible, particleFile, name):
        self.__particleList.append((nodeId, isVisible, particleFile))

    def addLoftToList(self, nodeId, isVisible, effectDB, name):
        self.__loftList.append((nodeId, isVisible, effectDB))

    def __selectAndPlayParticle(self, particlesList, firstObjID, delay):
        from random import randint
        idObj = firstObjID + randint(0, len(particlesList) - 1)
        CompoundSystem.forceParticleDelayed(self.__context.cidProxy.handle, idObj, 1, delay)

    def addEffect(self, path, visibleCondition, name, timed, delayRange = None):
        outObject = None
        variant = 'OWN' if self.__context.isPlayer else 'OTHER'
        effectDB = db.DBLogic.g_instance.getEffectDataVariant(Effects.getEffectId(name), variant)
        if effectDB:
            effectType = effectDB['type']
            nodeId = self.__rootNode.resolvePath(convertPath(path)).id
            sound = None
            if 'SoundEffectID' in effectDB:
                sound = [nodeId, effectDB['SoundEffectID'], None]
            if effectType == 'Loft' or effectType == 'Jet':
                effectObject = LoftEffectObject(self.__context, len(self.__loftList), sound)
                self.__boolCombiner.addObject(visibleCondition, effectObject.onVisibleChange)
                self.addLoftToList(nodeId, effectObject.isVisible, effectDB, name)
                self.__registerDrawObj(effectObject)
                outObject = effectObject
            elif effectType == 'TimedParticle' or effectType == 'LoopParticle':
                resourceName = effectDB.get('particleFile', None)
                if resourceName:
                    objId = len(self.__particleList)
                    if timed or effectType == 'TimedParticle':
                        effectObject = TimeEffectObject(self.__context, objId, sound)
                    else:
                        effectObject = EffectObject(self.__context, objId, sound)
                    effectObject.instantHide = effectDB.get('instantHide', False)
                    self.__boolCombiner.addObject(visibleCondition, effectObject.onVisibleChange)
                    self.addParticleToList(nodeId, effectObject.isVisible, resourceName, name)
                    self.__registerDrawObj(effectObject)
                    outObject = effectObject
            else:
                debug_utils.LOG_ERROR("Can't create effect {0}. Unsupported type {1} for compound model".format(Effects.getEffectId(name), effectType))
        else:
            debug_utils.LOG_WARNING_DEBUG("Can't create effect {0}".format(Effects.getEffectId(name)))
        return outObject

    def addEffectForUpgrade(self, upgradeId, effect):
        pass

    def __createDropModel(self, dropModelObject, hardpoints, resourceName):
        variant = 'OWN' if self.__context.isPlayer else 'OTHER'
        effectDB = db.DBLogic.g_instance.getEffectDataVariant(Effects.getEffectId('FALLING_OUT_PART'), variant)
        hierarchy = [(-1, Math.Matrix())]
        if 'HP_hit' in hardpoints:
            hierarchy.append((0, hardpoints['HP_hit']))
            particleList = [(1, True, effectDB['particleFile'])]
        else:
            particleList = []
        matrix = BigWorld.DropMatrixProvider()
        matrixProviders = [(0, matrix)]
        modelList = [(0, True, resourceName)]
        self.__compoundsForLoad += 1
        cid = CompoundSystem.addDynamicModel(hierarchy, matrixProviders, modelList, particleList, [], self.__onCompoundLoaded)
        dropModelObject.cid = cid
        dropModelObject.matrix = matrix

    def loadResources(self):
        resources = [ path + '_' for path in self.__visualForLoading.iterkeys() ]
        BigWorld.loadResourceListBG(resources, self.__onResourcesLoaded)

    def __onResourcesLoaded(self, resources):
        for resName, resource in resources.items():
            if resName in self.__visualForLoading:
                hardpointsLists = self.__visualForLoading[resName]
                _loadVisual(resource, hardpointsLists[0])
                for hardpoints in hardpointsLists[1:]:
                    hardpoints.update(hardpointsLists[0])

        self.__buid()

    @property
    def _visuals(self):
        return self.__visualForLoading

    @property
    def rootNode(self):
        return self.__rootNode

    @property
    def flamePaths(self):
        return self.__flamePaths

    def __findModel(self, partName):
        result = []
        for obj, isVisible in self.__drawObjects:
            if obj.partName == partName:
                result.append(obj.id)

        return result

    def __buid(self):
        hierarchy = []
        linearHierarchy = self.__rootNode.linearHierarchy
        for parentId, node in linearHierarchy:
            try:
                hierarchy.append((parentId, node.localMatrix or Math.Matrix()))
            except HierarchyWorker.HardpointNotFound:
                debug_utils.LOG_WARNING_DEBUG('Hardpoint not found "{0}" in object "{1}, {2}"'.format(node.path, self.__context.objDBData.name, getattr(self.__context.objDBData, 'fileName', '')))
                hierarchy.append((parentId, Math.Matrix()))

        matrixProviders = []
        matrixProviders.append((0, self.__context.rootMP))
        for nodeId, mp in self.__matrixProviderList:
            matrix = Math.MatrixProduct()
            matrix.b = linearHierarchy[nodeId][1].localMatrix
            matrix.a = mp
            matrixProviders.append((nodeId, matrix))

        self.__compoundsForLoad += 1
        self.__context.cidProxy.handle = cid = CompoundSystem.addDynamicModel(hierarchy, matrixProviders, self.__modelsList, self.__particleList, self.__loftList, self.__onCompoundLoaded)
        self.__fashionSyncLists = {}
        for modelId, fashion, nodeSyncList in self.__fashions:
            CompoundSystem.setModelFashion(cid, modelId, fashion)
            hierarchyUpdates = []
            for syncNodePath in nodeSyncList:
                for parentId, node in linearHierarchy:
                    if node.path == syncNodePath:
                        hierarchyUpdates.append((node.id, node.name))

            self.__fashionSyncLists.setdefault(modelId, []).extend(hierarchyUpdates)

        active = 1 if self.__context.rootMP.a is not None and self.__context.isActive else 0
        CompoundSystem.changeCompoundActive(cid, active)
        for dropModelObject, hardpoints, resourceName in self.__dropModels:
            self.__createDropModel(dropModelObject, hardpoints, resourceName)

        return

    def getStatistic(self):
        return {'particles': len(self.__particleList),
         'models': len(self.__modelsList)}

    def __onLoaded(self):
        self.__context.isLoaded = True
        for drawObject, isVisible in self.__drawObjects:
            if drawObject.isVisible != isVisible:
                drawObject.onVisibleChange(drawObject.isVisible)

        for modelId, syncList in self.__fashionSyncLists.iteritems():
            CompoundSystem.setModelNodeSyncList(self.__context.cidProxy.handle, modelId, syncList)

        self.__onLoadedCallback(self)
        self.__rootNode.clear()

    def __onCompoundLoaded(self):
        if not CompoundSystem.isHandleValid(self.__context.cidProxy.handle):
            return
        self.__compoundsForLoad -= 1
        if self.__compoundsForLoad == 0:
            self.__onLoaded()

    def postRead(self):
        pass