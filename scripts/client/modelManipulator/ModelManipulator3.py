# Embedded file name: scripts/client/modelManipulator/ModelManipulator3.py
import BigWorld
import Math
import PartAnimator2
import consts
import db.DBLogic
import Helpers.BoolCombiner
import CompoundBuilder
from CompoundBuilder import ObjectsBuilder
from CompoundBuilder import convertPath
from CompoundBuilder import syncHpMap
import clientConsts
import debug_utils
from EntityHelpers import EntityStates, isAvatar
import CompoundSystem
import EntityHelpers
import SurfaceManipulator
from debug_utils import *
from audio import GameSound
PLANE_PART_NAME = 'plane'
AIRCRAFT_FAKE_MODEL_NAME = 'objects/fake_model.model'
CREATE_STATISTIC = consts.IS_EDITOR or consts.IS_DEBUG_IMPORTED
INVALID_COMPOUND_ID = 4294967295L

class ObjectDataReader():
    """Build compound object from context, using CompoundBuilder"""
    HULL_PART_NAME = 'hull'

    @staticmethod
    def _resolvePath(path, defaultRootPath, partByNames):
        if path == '':
            return path
        pathList = CompoundBuilder.convertPath(path)
        if len(pathList) == 1:
            if defaultRootPath != '':
                return '{0}/{1}'.format(defaultRootPath, path)
            else:
                return path
        if pathList[0] in partByNames:
            root = ObjectDataReader._resolvePath(partByNames[pathList[0]].mountPoint, '', partByNames)
            if root:
                return '/'.join([root] + pathList[1:])
            else:
                return '/'.join(pathList[1:])
        else:
            debug_utils.LOG_WARNING_DEBUG("Can't resolve path{0}".format(path))
            return ''

    @staticmethod
    def _partAndHp(path):
        parts = path.split('/')
        if len(parts) == 2:
            return (parts[0], parts[1])
        else:
            return (ObjectDataReader.HULL_PART_NAME, parts[0])

    @staticmethod
    def partStateId(partId, stateId):
        return 'Part{0}_State{1}'.format(partId, stateId)

    @staticmethod
    def effectId(effectTrigger):
        return 'Effect{0}'.format(effectTrigger)

    @staticmethod
    def partFireId(partId):
        return 'Fire{0}'.format(partId)

    @staticmethod
    def shelId(shelType, sheldId):
        return 'shell{0}_{1}'.format(shelType, sheldId)

    @staticmethod
    def fire():
        return 'Fire'

    @staticmethod
    def stateEffect():
        return 'StateEffect'

    @staticmethod
    def fallingParts():
        return 'fallingParts'

    @staticmethod
    def prepareUpgrade(upgrade, bodyTypeName):
        if upgrade is None:
            return
        elif bodyTypeName is None:
            return upgrade
        else:
            bodyType = upgrade.bodyTypes.getBodyType(bodyTypeName)
            if bodyType is None:
                return upgrade
            import copy
            copyupg = copy.deepcopy(upgrade)
            for state in copyupg.states.values():
                bodyTypeState = bodyType.states.get(state.id)
                LOG_INFO('Applying body type: ', bodyTypeName)
                if bodyTypeState is not None:
                    state.model = bodyTypeState.model
                    state.subItems = bodyTypeState.subItems
                    state.animationController = bodyTypeState.animationController
                else:
                    LOG_ERROR('Body type: ', type, ': state: ', state.id, ' not found. Using default.')

            return copyupg

    @staticmethod
    def prepareParts(context, partTypesDb, partByNames, linkedModels, bodyTypeName):
        modelParts = context.objDBData.partsSettings.getPartsOnlyList()
        for partDb in modelParts:
            partByNames[partDb.name] = partDb
            linkedModels[partDb.partId] = []
            if partDb.partId in context.partTypes:
                partTypesDb[partDb.partId] = ObjectDataReader.prepareUpgrade(partDb.getPartType(context.partTypes[partDb.partId]), bodyTypeName)
            else:
                partTypesDb[partDb.partId] = ObjectDataReader.prepareUpgrade(partDb.getFirstPartType(), bodyTypeName)
                context.partTypes[partDb.partId] = partTypesDb[partDb.partId].id
            for _, stateDb in partTypesDb[partDb.partId].states.iteritems():
                if hasattr(stateDb, 'groundDecal'):
                    context.groundDecalMap[partDb.partId, stateDb.id] = stateDb.groundDecal

    @staticmethod
    def partsRead(builder, context):
        """Build compound with data from context"""
        propellerAnimators = ['PropellorControllerR',
         'PropellorMeshControllerR',
         'PropellorTextureControllerR',
         'PropellorTextureForsageControllerR']
        propellerAnimators += ['PropellorControllerL',
         'PropellorMeshControllerL',
         'PropellorTextureControllerL',
         'PropellorTextureForsageControllerL']
        propellerAnimators += ['PropellorController',
         'PropellorMeshController',
         'PropellorTextureController',
         'PropellorTextureForsageController']
        modelParts = context.objDBData.partsSettings.getPartsOnlyList()
        partTypesDb = dict()
        partByNames = dict()
        linkedModels = dict()
        shellModels = dict()
        bodyTypeTag = 'man' if context.bodyType is not None and context.bodyType == 0 else 'woman'
        ObjectDataReader.prepareParts(context, partTypesDb, partByNames, linkedModels, bodyTypeTag)
        for shellIndex, shells in context.shelsData.iteritems():
            for id_, (modelName, flamePath) in enumerate(shells):
                path = ObjectDataReader._resolvePath(flamePath, '', partByNames)
                linkedModelPath, _ = path.rsplit('/', 1)
                condition = [[(1, ObjectDataReader.shelId(shellIndex, id_))]]
                shellModels.setdefault(linkedModelPath, list()).append((modelName, path, condition))

        if context.weaponsSlotsDBData and context.weaponSlots:
            for wSlotId, slotData in context.weaponsSlotsDBData.slots.iteritems():
                slotState = next((v for k, v in context.weaponSlots if k == wSlotId), -1)
                if slotState in slotData.types:
                    weaponsData = slotData.types[slotState]
                    for linkedModelDescription in weaponsData.linkedModels:
                        partName, mountPoint = ObjectDataReader._partAndHp(linkedModelDescription.mountPath)
                        partDb = partByNames[partName]
                        if context.partTypes[partDb.partId] == linkedModelDescription.parentUpgrade:
                            if linkedModelDescription.model:
                                linkedModels[partDb.partId].append((linkedModelDescription.model, mountPoint, [[]]))

        if context.fullLoading:
            for flamePath, flameParticle, uniqueId, shellPath, shellParticle in context.gunsData:
                path = ObjectDataReader._resolvePath(flamePath, '', partByNames)
                builder.addParticle(path, uniqueId, flameParticle)
                builder.addFirePoint(path, uniqueId)
                if shellPath != '' and shellParticle != '':
                    path = ObjectDataReader._resolvePath(shellPath, '', partByNames)
                    builder.addParticle(path, long(uniqueId) + ModelManipulator3.SHELL_EVENT_OFFS, shellParticle)

        damageEffects = context.objDBData.damageEffects if context.isBaseObject else context.objDBData.visualSettings.damageEffects
        stateEffectPred = [[(1, ObjectDataReader.stateEffect())]]
        fallingPartsPred = [[(1, ObjectDataReader.fallingParts())]]
        for partDb in modelParts:
            partType = partTypesDb[partDb.partId]
            path = ObjectDataReader._resolvePath(partDb.mountPoint, '', partByNames)
            context.partNodeIds[partDb.partId] = builder.rootNode.resolvePath(CompoundBuilder.convertPath(path)).id
            if partType.fireMountPoint != '' and context.fullLoading:
                isFire = partType.fire and partType.fire.effectFire
                effectName = partType.fire.effectFire if isFire else damageEffects.effectFire
                effectObj = builder.addEffect(ObjectDataReader._resolvePath(partType.fireMountPoint, path, partByNames), [[(1, ObjectDataReader.partFireId(partDb.partId))]], effectName, False)
                builder.addEffectForUpgrade(partType.id, effectObj)
            states = partType.states.itervalues() if context.fullLoading else [partType.states[context.partsStates[partDb.partId]]]
            models = dict()
            timedEffects = dict()
            stateEffects = dict()
            triggerEffects = dict()
            propellers = dict()
            partTriggers = list()
            for state in states:
                visualGroup = (1, ObjectDataReader.partStateId(partDb.partId, state.id))
                if state.model:
                    if linkedModels[partDb.partId]:
                        modelHps = CompoundBuilder.syncHpMap(state.model)
                        for _, mountPoint, condition in linkedModels[partDb.partId]:
                            if mountPoint in modelHps:
                                condition[0].append((1, ObjectDataReader.partStateId(partDb.partId, state.id)))

                    animatorData = state.animationController or None
                    models.setdefault((path, state.model, state.stateAnimation), list()).append((visualGroup, animatorData, state.customSettings))
                for subItem in state.subItems:
                    modelPath = ObjectDataReader._resolvePath(subItem.mountPoint, path, partByNames)
                    if subItem.animatorName in propellerAnimators:
                        propellers.setdefault(modelPath, dict())[subItem.animatorName] = subItem.model
                    else:
                        animatorData = subItem.animatorName or None
                        models.setdefault((modelPath, subItem.model, None), list()).append((visualGroup, animatorData, subItem.customSettings))

                if state.fallingOutModel:
                    builder.addDropModel(path, fallingPartsPred + [[visualGroup]], state.fallingOutModel)
                for effect in state.effectSettings.onStart:
                    effetPath = ObjectDataReader._resolvePath(effect.mountPoint, path, partByNames)
                    timedEffects.setdefault((effetPath, effect.name), list()).append(visualGroup)

                for effect in state.effectSettings.state:
                    effetPath = ObjectDataReader._resolvePath(effect.mountPoint, path, partByNames)
                    stateEffects.setdefault((effetPath, effect.name), list()).append(visualGroup)

                for effect in state.effectSettings.triggered:
                    effetPath = ObjectDataReader._resolvePath(effect.mountPoint, path, partByNames)
                    triggerEffects.setdefault((effetPath, effect.name), list()).append((visualGroup, (1, ObjectDataReader.effectId(effect.trigger))))
                    context.effectNodeIds[effect.trigger] = builder.rootNode.resolvePath(CompoundBuilder.convertPath(effetPath)).id
                    partTriggers.append(effect.trigger)
                    if context.isAircraft and clientConsts.SNOWBALLS_MOD.ENABLED:
                        if effect.trigger in clientConsts.SNOWBALLS_MOD.TRIGGERS:
                            triggerEffects.setdefault((effetPath, clientConsts.SNOWBALLS_MOD.modName(effect.name)), list()).append((visualGroup, (1, ObjectDataReader.effectId(clientConsts.SNOWBALLS_MOD.modName(effect.trigger)))))
                            context.effectNodeIds[clientConsts.SNOWBALLS_MOD.modName(effect.trigger)] = builder.rootNode.resolvePath(CompoundBuilder.convertPath(effetPath)).id
                        if effect.trigger == 'LOFT':
                            triggerEffects.setdefault((effetPath, clientConsts.SNOWBALLS_MOD.BengalFireEffect), list()).append((visualGroup, (1, ObjectDataReader.effectId(clientConsts.SNOWBALLS_MOD.BengalFireTrigger))))
                            context.effectNodeIds[clientConsts.SNOWBALLS_MOD.BengalFireTrigger] = builder.rootNode.resolvePath(CompoundBuilder.convertPath(effetPath)).id

            for (itemPath, modelName, animName), dataList in models.iteritems():
                condition = [ cond for cond, animatorData, customSettings in dataList ]
                controllerName = dataList[0][1]
                customSettings = dataList[0][2]
                turretSettings = db.DBLogic.g_instance.getTurretData(partType.componentXml)
                if controllerName == 'TurretController' and turretSettings and turretSettings.visualSettings:
                    if hasattr(turretSettings, 'ik') and turretSettings.ik is not None:
                        builder.addIK(turretSettings.ik, partDb.name)
                    gunnerId = 0
                    for part in modelParts:
                        upgrade = partTypesDb[part.partId]
                        if hasattr(upgrade, 'gunPartName') and upgrade.gunPartName == partDb.name:
                            gunnerId = part.partId
                            break

                    if not turretSettings.isScenarioAnimator:
                        builder.addTurret(itemPath, [condition], gunnerId, modelName, turretSettings, partDb.name)
                    else:
                        for triggerName in partTriggers:
                            builder.addTurret(itemPath, [condition], triggerName, modelName, turretSettings, partDb.name)

                elif controllerName == 'GunnerHeadController' and hasattr(context.objDBData, 'visualSettings'):
                    planeVisualSettings = context.objDBData.visualSettings
                    settings = planeVisualSettings.gunnerAnimatorSettings.get(partDb.partId)
                    if settings is not None:
                        builder.addGunnerHeadModel(itemPath, [condition], modelName, partDb.name, settings, context.entityId)
                else:
                    builder.addModel(itemPath, [condition], modelName, animName, partDb.name)
                    if controllerName:
                        builder.addController(itemPath, controllerName)

            if context.fullLoading:
                for (itemPath, effectName), condition in timedEffects.iteritems():
                    builder.addEffect(itemPath, stateEffectPred + [condition], effectName, True)

                for (itemPath, effectName), condition in stateEffects.iteritems():
                    builder.addEffect(itemPath, stateEffectPred + [condition], effectName, False)

                for (itemPath, effectName), conditions in triggerEffects.iteritems():
                    visualCondition = [ condition for condition, trigger in conditions ]
                    triggers = [ trigger for condition, trigger in conditions ]
                    builder.addEffect(itemPath, [visualCondition] + [triggers], effectName, False)

            for itemPath, models in propellers.iteritems():
                if 'PropellorControllerR' in models:
                    rotorModel, meshModel, normalTextureModel, forsageModel, direction = (models['PropellorControllerR'],
                     models['PropellorMeshControllerR'],
                     models['PropellorTextureControllerR'],
                     models['PropellorTextureForsageControllerR'],
                     False)
                if 'PropellorControllerL' in models:
                    rotorModel, meshModel, normalTextureModel, forsageModel, direction = (models['PropellorControllerL'],
                     models['PropellorMeshControllerL'],
                     models['PropellorTextureControllerL'],
                     models['PropellorTextureForsageControllerL'],
                     True)
                if 'PropellorController' in models:
                    rotorModel, meshModel, normalTextureModel, forsageModel, direction = (models['PropellorController'],
                     models['PropellorMeshController'],
                     models['PropellorTextureController'],
                     models['PropellorTextureForsageController'],
                     True)
                if context.fullLoading:
                    builder.addPropeller(itemPath, [], [[(1, ObjectDataReader.partStateId(partDb.partId, 3))]], rotorModel, meshModel, normalTextureModel, forsageModel, direction)
                else:
                    builder.addHangarPropeller(itemPath, [], rotorModel, meshModel, direction)

            for model, mountPoint, condition in linkedModels[partDb.partId]:
                mountPath = ObjectDataReader._resolvePath(mountPoint, path, partByNames)
                builder.addModel(mountPath, condition, model)
                if mountPath in shellModels:
                    for shellModel, shellPath, shellCondition in shellModels[mountPath]:
                        builder.addModel(shellPath, condition + shellCondition, shellModel)

        builder.postRead()
        return


class ObjectContext():
    """Container for setup data of compound object"""
    pass


class EventSystem():
    """Simple event system for particles"""

    def __init__(self):
        self.__events = dict()
        self.__enable = False

    def clear(self):
        self.__events = None
        return

    def addListener(self, eventId, listener):
        self.__events.setdefault(eventId, []).append(listener)

    def setEnable(self, enable):
        self.__enable = enable

    def onEvent(self, eventId, *args):
        if self.__enable and eventId in self.__events:
            for f in self.__events[eventId]:
                f(*args)


class ModelManipulator3(object):
    SHELL_EVENT_OFFS = 4294967295L

    def __init__(self, isPlayer, entityId, objDBData, partTypes, partsStates, gunsData = [], shelsData = {}, weaponsSlotsDBData = None, weaponSlots = None, fullLoading = True, callback = None, copyFromCompoundID = 0, weaponSoundID = None, turretSoundID = None, camouflage = None, decals = None, bodyType = None, builder = ObjectsBuilder):
        """
        :param isPlayer: is main current player model
        :param entityId: id of parent entity
        :param objDBData: settings from DBLogic
        :param partTypes: part types setup ( [{'key':partId, 'value':typeId},...])
        :param partsStates: part states setup ( [(partId, stateId),...])
        :param gunsData: data of main guns [ (gun.flamePath, group.gunDescription.bulletShot, gun.uniqueId),... ]
        :param shelsData: data of bombs and rockets [ shellTypeId: [(model, hpName),...] ]
        :param weaponsSlotsDBData: settingsRoot.components.weapons2 from object DB
        :param weaponSlots: configuration of weapon slots [(slotId, typeId),...]
        :param fullLoading: load all states or only current
        :param callback: loading complete callback
        """
        context = ObjectContext()
        context.isPlayer = isPlayer
        context.entityId = entityId
        context.objDBData = objDBData
        context.partTypes = dict(((it['key'], it['value']) for it in partTypes))
        context.partsStates = dict()
        context.groundDecalMap = dict()
        context.weaponsSlotsDBData = weaponsSlotsDBData
        context.weaponSlots = weaponSlots
        context.gunsData = gunsData
        context.shelsData = shelsData
        context.fullLoading = fullLoading
        context.isAircraft = hasattr(objDBData, 'flightModel')
        context.curTimeAction = False
        context.rootModel = BigWorld.Model(AIRCRAFT_FAKE_MODEL_NAME)
        context.rootMP = Math.MatrixProduct()
        context.velocity = Math.Vector3(0, 0, 0)
        context.cidProxy = BigWorld.PyHandleProxy()
        context.isLoaded = False
        context.isDestroyed = False
        context.partNodeIds = dict()
        context.effectNodeIds = dict()
        context.isActive = True
        context.ikSystems = []
        context.ikSystemByPart = {}
        context.bodyType = bodyType
        from db.DBBaseObject import DBBaseObject
        context.isBaseObject = issubclass(objDBData.__class__, DBBaseObject)
        self.__context = context
        self.__loadingCallback = callback
        self.__externalNodeNames = []
        self.__animatorsController = PartAnimator2.PartAnimatorController(objDBData, entityId)
        self.__boolCombiner = Helpers.BoolCombiner.BoolCombiner()
        self.__eventSystem = EventSystem()
        if hasattr(self.__context.objDBData, 'visualSettings'):
            self.__surfaceManipulator = SurfaceManipulator.SurfaceManipulator(self.__context.objDBData.visualSettings, self.__getTextureQuality(), self.compoundIDProxy, self.__context)
            if camouflage is not None and decals is not None:
                self.__surfaceManipulator.setDecalsByIds(camouflage, decals)
        else:
            self.__surfaceManipulator = None
        self.__externalNodes = {}
        self.__shelsCount = dict()
        self.__isJetforsageOn = False
        self.__lastSpeedwiseEngineEffectID = -1
        for partId, stateId in partsStates:
            self.__updatePartState(partId, stateId)

        modelParts = context.objDBData.partsSettings.getPartsOnlyList()
        for partDb in modelParts:
            if partDb.partId not in self.__context.partsStates:
                self.__updatePartState(partDb.partId, 1)

        self.setCondition(ObjectDataReader.stateEffect(), self.__context.fullLoading)
        self.setCondition(ObjectDataReader.fallingParts(), self.__context.fullLoading)
        objectBuilder = builder(self.__animatorsController, self.__boolCombiner, self.__eventSystem, self.__context, self.onLoaded_internal)
        ObjectDataReader.partsRead(objectBuilder, context)
        self.__copyFromCompoundID = copyFromCompoundID
        objectBuilder.loadResources()
        self.__soundObjects = []
        if fullLoading:
            GameSound().cache(context.objDBData, objectBuilder, self.__context, isPlayer, self.__soundObjects, weaponSoundID, turretSoundID)
        self.statistic = None
        self.consumablesEffects = list()
        self.__turretGunFlamesMP = {}
        return

    def refreshContextForAvatarCopy(self, avatarCopyID):
        self.__context.entityId = avatarCopyID
        self.__context.isPlayer = False

    def getIKSystems(self):
        return self.context.ikSystems

    @property
    def surface(self):
        return self.__surfaceManipulator

    @property
    def entityId(self):
        return self.__context.entityId

    @property
    def compoundID(self):
        """compound id in low level API"""
        return self.__context.cidProxy.handle

    @property
    def compoundIDProxy(self):
        return self.__context.cidProxy

    @property
    def velocity(self):
        """return velocity of compound"""
        return self.__context.velocity

    @property
    def context(self):
        return self.__context

    @velocity.setter
    def velocity(self, value):
        """setup velocity of compound. Used for drop parts"""
        self.__context.velocity = value

    @property
    def soundObjects(self):
        return self.__soundObjects

    def addShadowEntity(self):
        if self.__hasShadow:
            BigWorld.addShadowEntity(self.compoundID)

    def onLoaded_internal(self, objectBuilder):
        if not self.__context.isDestroyed:
            if self.__copyFromCompoundID:
                CompoundSystem.modelCopyParms(self.compoundID, self.__copyFromCompoundID)
                self.__copyFromCompoundID = 0
            if CREATE_STATISTIC:
                self.statistic = objectBuilder.getStatistic()
            if self.__context.isPlayer:
                CompoundSystem.reflectionDrawCompound(self.compoundID)
                BigWorld.setPlayersCompoundID(self.compoundID)
            try:
                objectBuilder.loadIKs(self.compoundID)
            except Exception as e:
                debug_utils.LOG_TRACE('Error loading IK: %s' % e.message)

            self.__animatorsController.onLoaded(self.__context)
            self.__fillExternalNodes(objectBuilder.rootNode)
            self.addShadowEntity()
            if self.__surfaceManipulator:
                self.__surfaceManipulator.applySurfaces()
            self.__eventSystem.setEnable(True)
            if self.__loadingCallback is not None:
                self.__loadingCallback()
            self.__updateGroundDecals()
            CompoundSystem.compoundPrepareDraw(self.compoundID)
            if self.__context.isPlayer and hasattr(BigWorld.player(), 'controllers'):
                GameSound().initPlayer()
            debug_utils.LOG_TRACE('onLoaded_internal', self.__context.isPlayer)
            observ = False
            if self.__context.isPlayer and hasattr(BigWorld.player(), 'state'):
                observ = EntityHelpers.EntityStates.inState(BigWorld.player(), EntityHelpers.EntityStates.OBSERVER)
                observ = observ or EntityHelpers.EntityStates.inState(BigWorld.player(), EntityHelpers.EntityStates.DESTROYED)
                observ = observ or EntityHelpers.EntityStates.inState(BigWorld.player(), EntityHelpers.EntityStates.DESTROYED_FALL)
                debug_utils.LOG_TRACE('onLoaded_internal observ:', observ, BigWorld.player().state)
            if not self.__context.isPlayer and not observ:
                CompoundSystem.setCompoundAlpha(self.compoundID, 0)
                CompoundSystem.setCompoundTargetAlpha(self.compoundID, 1)
                debug_utils.LOG_TRACE('onLoaded_internal', self.__context.entityId, self.compoundID)
            for nodeId, gunId, path in objectBuilder.flamePaths:
                nodeMatrixProvider = BigWorld.CompoundNodeMP()
                nodeMatrixProvider.handle = self.compoundID
                nodeMatrixProvider.nodeIdx = nodeId
                self.__turretGunFlamesMP[gunId] = nodeMatrixProvider

        return

    def checkTurretCanShoot(self, gunId):
        return self.getTurretController().canShoot(gunId)

    def getTurretGunPos(self, gunId):
        m = self.__turretGunFlamesMP.get(gunId, None)
        if m:
            return Math.Matrix(m).translation
        else:
            return

    def setExternalNodeNames(self, nodeNames):
        """specifies the list of nodes for which it is possible to obtain a matrix(by getNodeMatrix)"""
        self.__externalNodeNames = nodeNames

    def __fillExternalNodes(self, rootNode):
        for nodePath in self.__externalNodeNames:
            node = rootNode.resolvePath([nodePath])
            self.__externalNodes[nodePath] = node.localMatrix

    def getCondition(self, symbol):
        """return state of predicate in conditions. Only for debug"""
        return self.__boolCombiner.getCondition(symbol)

    def setCondition(self, symbol, visible):
        """setup state of predicate in conditions"""
        return self.__boolCombiner.setCondition(symbol, visible)

    @property
    def symbols(self):
        """return all predicates names in conditions. Only for debug"""
        return self.__boolCombiner.symbols

    def __isEffectAlias(self, effectName):
        return self.__boolCombiner.hasSymbol(ObjectDataReader.effectId(effectName))

    def setMatrixProvider(self, mp):
        """setup main matrix provider of compound"""
        self.__context.rootMP.a = mp
        active = 1 if self.__context.rootMP.a is not None and self.__context.isActive else 0
        CompoundSystem.changeCompoundActive(self.compoundID, active)
        if mp is not None:
            self.__updateGroundDecals(True)
        return

    def getMatrixProvider(self):
        """return main matrix provider of compound"""
        return self.__context.rootMP.a

    def getNodeMatrix(self, path):
        """return node matrix. For using: after creating of modelManipulator necessary to call setExternalNodeNames with node names"""
        return self.__externalNodes[path]

    @property
    def __hasShadow(self):
        return self.__context.fullLoading and self.__context.isAircraft

    def __getTextureQuality(self):
        if not self.__context.fullLoading:
            return 4
        elif self.__context.isPlayer:
            return 1
        else:
            return 0

    def setShelsCount(self, shellsCount):
        """Set bombs an rockets count(in start and after launch)"""
        for shellIndex, newCount in enumerate(shellsCount):
            if shellIndex in self.__context.shelsData:
                maxCount = len(self.__context.shelsData[shellIndex]) - 1
                currentCount = self.__shelsCount.get(shellIndex, 0)
                self.__shelsCount[shellIndex] = newCount
                if newCount > currentCount:
                    for sheldId in range(currentCount, newCount):
                        self.setCondition(ObjectDataReader.shelId(shellIndex, maxCount - sheldId), True)

                elif newCount < currentCount:
                    for sheldId in range(currentCount - 1, newCount - 1, -1):
                        self.setCondition(ObjectDataReader.shelId(shellIndex, maxCount - sheldId), False)

    def updateStatesNet(self, partsStates, curTimeAction):
        """On change parts states from server"""
        self.__context.curTimeAction = curTimeAction
        for partId, stateId in partsStates:
            self.__updatePartState(partId, stateId)

    def __updatePartState(self, partId, partState):
        oldValue = self.__context.partsStates.get(partId, -1)
        if oldValue != partState:
            if oldValue != -1:
                self.setCondition(ObjectDataReader.partStateId(partId, oldValue), False)
            self.__context.partsStates[partId] = partState
            self.setCondition(ObjectDataReader.partStateId(partId, partState), True)
            if self.__context.groundDecalMap.get((partId, partState)):
                self.__createGroundDecal(partId, partState, True)

    def setEffectVisible(self, effectName, value):
        """Show or hide some triggered effect"""
        if clientConsts.SNOWBALLS_MOD.ENABLED:
            name = clientConsts.SNOWBALLS_MOD.getName(self.consumablesEffects, effectName)
            if name == clientConsts.SNOWBALLS_MOD.LoftTrigger and self.getCondition(ObjectDataReader.effectId(clientConsts.SNOWBALLS_MOD.BengalFireTrigger)):
                value = False
            self.setCondition(ObjectDataReader.effectId(name), value)
        else:
            self.setCondition(ObjectDataReader.effectId(effectName), value)

    def updatePartsFlags(self, partsFlags):
        """
        update part flags (for example firing particles) and return map with flags which were really switched
        @param partsFlags:
        @return:
        """
        partsBitFlags = 0
        partChanges = []
        for partID, partFlags in partsFlags:
            partsBitFlags |= partFlags
            if self.setCondition(ObjectDataReader.partFireId(partID), bool(partFlags & consts.PART_FLAGS.FIRE)):
                partChanges.append((partID, consts.PART_FLAGS.FIRE, bool(partFlags & consts.PART_FLAGS.FIRE)))

        if self.setCondition(ObjectDataReader.fire(), bool(partsBitFlags & consts.PART_FLAGS.FIRE)):
            GameSound().onBurning(self.__context.entityId, self.__context.isPlayer, bool(partsBitFlags & consts.PART_FLAGS.FIRE))
            if not self.__context.isBaseObject:
                self.setCondition(ObjectDataReader.stateEffect(), not bool(partsBitFlags & consts.PART_FLAGS.FIRE))
        return partChanges

    def criticalDamage(self):
        """on critical part destroyed"""
        if self.__isEffectAlias('FIRECRITICAL'):
            self.setEffectVisible('FIRE', False)
            self.setEffectVisible('FIRECRITICAL', True)

    def mediumDamage(self):
        """on < 30% HP"""
        self.setEffectVisible('SMOKE', True)

    def clearMediumDamage(self):
        self.setEffectVisible('SMOKE', False)

    def setState(self, avatarState, transitionActions):
        """on change parent entity state"""
        if not self.__context.isBaseObject:
            if avatarState & (EntityHelpers.EntityStates.GAME_CONTROLLED | EntityHelpers.EntityStates.WAIT_START | EntityHelpers.EntityStates.PRE_START_INTRO):
                self.setEffectVisible('FIRE', False)
                self.setEffectVisible('FIRECRITICAL', False)
                self.setEffectVisible('LOFT', False)
                self.setEffectVisible('SMOKE', False)
                self.setEffectVisible('ATTACKANGLE', False)
                self.setCondition(ObjectDataReader.fallingParts(), True)
                self.setCondition(ObjectDataReader.stateEffect(), True)
                self.__resetControlAxises()
            if avatarState & EntityHelpers.EntityStates.DESTROYED:
                self.setCondition(ObjectDataReader.fallingParts(), False)
                self.setEffectVisible('FIRE', False)
                self.setEffectVisible('FIRECRITICAL', False)
                self.setAxisValue(consts.FORCE_AXIS, clientConsts.FORCE_AXIS_DEATH_VALUE)
                self.setAxisValue(consts.FLAPS_AXIS, 0)
            if avatarState & EntityHelpers.EntityStates.DESTROYED_FALL:
                self.setAxisValue(consts.FORCE_AXIS, clientConsts.FORCE_AXIS_FALL_VALUE)
                self.setEffectVisible('FIRE', True)
            if avatarState & EntityHelpers.EntityStates.DEAD:
                self.setEffectVisible('LOFT', False)
                self.setEffectVisible('SMOKE', False)
                self.setEffectVisible('ATTACKANGLE', False)
                self.updateForsageEffects(False)
                self.setCondition(ObjectDataReader.stateEffect(), False)
            self.setEffectVisible('JETENGINESTART', bool(avatarState & EntityHelpers.EntityStates.GAME_CONTROLLED))

    def getPartMatrix(self, partId):
        """return matrix of some part"""
        compoundId = self.compoundID
        if compoundId != INVALID_COMPOUND_ID:
            if partId in self.__context.partNodeIds:
                matrix = CompoundSystem.getNodeMatrix(compoundId, self.__context.partNodeIds[partId])
                return matrix

    def getEffectCoordinate(self, effectName):
        """return world position of some effect"""
        if effectName in self.__context.effectNodeIds:
            matrix = CompoundSystem.getNodeMatrix(self.compoundID, self.__context.effectNodeIds[effectName])
            if matrix:
                return matrix.translation
            return None
        else:
            return None

    def getRootModel(self):
        """return main model of compound system"""
        return self.__context.rootModel

    def setAxisValue(self, axis, value):
        """on control axis value change - for animation"""
        if self.__animatorsController:
            self.__animatorsController.setAxisValue(axis, value)
            self.__checkAxisEffects(axis, value)

    def triggerAnimation(self, trigger, value):
        if self.__animatorsController:
            self.__animatorsController.setTriggerValue(trigger, value)

    def __checkAxisEffects(self, axis, value):
        if axis == consts.FORCE_AXIS:
            self.setEffectVisible('ENGINE', value > -1)
            self.setEffectVisible('JETENGINE', value >= -1)
            self.setEffectVisible('BRAKE', value < 0 and value >= -1)

    def updateForsageEffects(self, value):
        """on forsage event"""
        self.setEffectVisible('FORSAGE', value)
        self.setEffectVisible('JETFORSAGE', value)
        if clientConsts.SNOWBALLS_MOD.canPlayBengalFire(self.consumablesEffects):
            self.setEffectVisible('FORSAGE_SNOWBALLS', value)
        self.__isJetforsageOn = value

    def setPropellorAngle(self, left, right):
        """set up propeller angle in hangar"""
        if self.__animatorsController:
            self.__animatorsController.setPropellorAngle(left, right)

    def __resetControlAxises(self):
        self.setAxisValue(consts.HORIZONTAL_AXIS, 0)
        self.setAxisValue(consts.VERTICAL_AXIS, 0)
        self.setAxisValue(consts.ROLL_AXIS, 0)
        self.setAxisValue(consts.FORCE_AXIS, 0)

    def onAddBullet(self, gunId, delay = 0, shellEffect = False):
        """on shot event"""
        if self.__context.isActive:
            self.__eventSystem.onEvent(gunId, delay)
            if shellEffect:
                self.__eventSystem.onEvent(long(gunId) + ModelManipulator3.SHELL_EVENT_OFFS, delay)
            turretController = self.getTurretController()
            if turretController is not None:
                turretController.onTurretShoot(gunId, delay)
        return

    def setVisible(self, value):
        """change visibility of compound"""
        self.__context.isActive = value
        active = 1 if self.__context.rootMP.a is not None and self.__context.isActive else 0
        CompoundSystem.changeCompoundActive(self.compoundID, active)
        return

    @property
    def isLoaded(self):
        return self.__context.isLoaded

    def destroy(self):
        """destroy compound on end of game and clear all references and resources"""
        self.__turretGunFlamesMP = None
        self.__context.ikSystemByPart = None
        self.__context.ikSystems = None
        self.__context.isDestroyed = True
        self.__animatorsController.destroy()
        self.__animatorsController = None
        self.__boolCombiner = None
        self.__eventSystem.clear()
        self.__eventSystem = None
        self.__destroyGroundDecals()
        return

    def __updateGroundDecals(self, refresh = False):
        if len(self.__context.groundDecalMap) > 0:
            for partId, partState in self.__context.partsStates.items():
                if (partId, partState) in self.__context.groundDecalMap:
                    self.__createGroundDecal(partId, partState, refresh)

    def __createGroundDecal(self, partId, partState, refresh = False):
        decalInst = self.__context.groundDecalMap.get(partId)
        if decalInst is None or refresh:
            decal = self.__context.groundDecalMap[partId, partState]
            mp = self.getPartMatrix(partId)
            if mp and self.__context.rootMP.a != None:
                scaleMatrix = Math.Matrix()
                scaleMatrix.setScale(decal.scale)
                matrix = Math.Matrix(mp)
                tr = matrix.translation
                if tr.dot(tr) == 0 and self.getMatrixProvider():
                    matrix.postMultiply(self.getMatrixProvider())
                matrix.preMultiply(scaleMatrix)
                if decalInst is None:
                    self.__context.groundDecalMap[partId] = BigWorld.GroundDecalWrapper(matrix, decal.texture, partId + 100)
                elif decal.texture != '':
                    decalInst.update(matrix, decal.texture)
                    debug_utils.LOG_DEBUG('ModelManipulator:__updateGroundDecal', self.__context.objDBData.name, self.__context.groundDecalMap[partId])
                else:
                    debug_utils.LOG_DEBUG('ModelManipulator:__removeGroundDecal', self.__context.objDBData.name, self.__context.groundDecalMap[partId])
                    self.__context.groundDecalMap[partId] = None
        return

    def __destroyGroundDecals(self):
        if len(self.__context.groundDecalMap) > 0:
            self.__context.groundDecalMap = dict()

    def setGroundDecals(self, decals):
        if consts.IS_AIRPLANE_EDITOR:
            for iter in decals:
                if (iter[0], iter[1]) in self.__context.groundDecalMap:
                    self.__context.groundDecalMap[iter[0], iter[1]].texture = iter[2]
                    self.__context.groundDecalMap[iter[0], iter[1]].scale[0] = iter[3]
                    self.__context.groundDecalMap[iter[0], iter[1]].scale[1] = iter[4]
                    self.__context.groundDecalMap[iter[0], iter[1]].scale[2] = iter[5]
                    self.__context.groundDecalMap[iter[0], iter[1]].ed_data.writeString('texture', iter[2])
                    mp = self.getPartMatrix(iter[0])
                    scaleMatrix = Math.Matrix()
                    scaleMatrix.setScale(Math.Vector3(iter[3], iter[4], iter[5]))
                    matrix = Math.Matrix(mp)
                    matrix.preMultiply(scaleMatrix)
                    decalHolder = self.__context.groundDecalMap.get(iter[0])
                    if decalHolder != None:
                        decalHolder.update(matrix, iter[2])

        return

    def updateConsumablesEffects(self, consumables):
        self.consumablesEffects = list()
        for consumableData in consumables:
            key = consumableData['key']
            if key != -1 and consumableData['chargesCount'] >= 0 and (key in clientConsts.SNOWBALLS_MOD.TRIGGERS.values() or key == clientConsts.SNOWBALLS_MOD.BengalFireConsumableID):
                self.consumablesEffects.append(key)

    def getLeftAileronAngle(self):
        leftAileronController = self.__animatorsController.getController('LeftAileronController')
        if leftAileronController is not None:
            return leftAileronController.matrixProvider.pitch
        else:
            return 0

    def getRightAileronAngle(self):
        rightAileronController = self.__animatorsController.getController('RightAileronController')
        if rightAileronController is not None:
            return rightAileronController.matrixProvider.pitch
        else:
            return 0

    def getTurretController(self):
        return self.__animatorsController.getController('TurretController')

    def getHeadController(self):
        return self.__animatorsController.getController('GunnerHeadController')

    def updateSpeedwiseEngineEffects(self, currentSpeed, maxSpeed, effectStartSpeedCoef):
        curSpeedCoef = currentSpeed / maxSpeed
        curSpeedEffectID = -1
        if curSpeedCoef >= effectStartSpeedCoef:
            if self.__isJetforsageOn:
                curSpeedEffectID = 3
            else:
                curSpeedEffectID = 2
        else:
            curSpeedEffectID = 1
        if self.__lastSpeedwiseEngineEffectID != curSpeedEffectID:
            if self.__lastSpeedwiseEngineEffectID != -1:
                self.setEffectVisible('SPEEDWISE_ENGINE_EFFECT_' + str(self.__lastSpeedwiseEngineEffectID), False)
            self.setEffectVisible('SPEEDWISE_ENGINE_EFFECT_' + str(curSpeedEffectID), True)
            self.__lastSpeedwiseEngineEffectID = curSpeedEffectID

    def onOwnerChanged(self, owner):
        if self.__animatorsController is not None:
            self.__animatorsController.onOwnerChanged(owner)
        return