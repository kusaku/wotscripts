# Embedded file name: scripts/editors/ModelManipulatorEditor.py
from modelManipulator.ModelManipulator3 import ModelManipulator3, PLANE_PART_NAME
from modelManipulator.ModelManipulator3 import ObjectDataReader
from ObjectsBuilderEditor import ObjectsBuilderEditor
import ResMgr
from modelManipulator.CompoundBuilder import syncHpMap
import debug_utils
import Math
import math
import CompoundSystem

class FileIsReadonly(Exception):

    def __init__(self):
        self.files = []


class ModelManipulatorEditor(ModelManipulator3):

    def __init__(self, isPlayer, entityId, objDBData, partTypes, partsStates, gunsData = [], shelsData = {}, weaponsSlotsDBData = None, weaponSlots = None, fullLoading = True, callback = None, bodyType = None):
        try:
            bType = 0 if bodyType == None or bodyType == 'man' else 1
            ModelManipulator3.__init__(self, isPlayer, entityId, objDBData, partTypes, partsStates, gunsData, shelsData, weaponsSlotsDBData, weaponSlots, fullLoading, None, 0, None, None, None, None, bType, ObjectsBuilderEditor)
        except Exception as e:
            print e

        self.context.rootModel.enterWorld()
        self.__nodesDirty = {}
        self.__partsDirty = []
        self.__callback = callback
        return

    @property
    def partsHierarchy(self):
        return self.context.partsHierarchy

    @property
    def groundDecalMap(self):
        return self.context.groundDecalMap

    def toggleFireEffect(self, upgradeId, bVisible):
        partByNames = dict()
        modelParts = self.context.objDBData.partsSettings.getPartsOnlyList()
        for partDb in modelParts:
            partByNames[partDb.name] = partDb

        for partDb in modelParts:
            partType = partDb.getPartType(self.context.partTypes[partDb.partId])
            if partType.fireMountPoint != '' and self.context.fullLoading:
                for effect in self.context.fireEffectsPerUpgrade:
                    if partType.id == effect[0]:
                        effect[1].onVisibleChange(bVisible)

    def trackTurretTrackersTarget(self, pos):
        matrix = Math.Matrix()
        matrix.translation = pos
        turretTrackers = self.getTurretController().trackers
        headTrackers = self.getHeadController().trackers
        for tracker in turretTrackers:
            tracker.setTargetMatrix(matrix)

        for tracker in headTrackers:
            tracker.setTargetMatrix(matrix)

    def trackerEnableIdleAnimation(self, enableIdle, enableShoot):
        try:
            turretTrackers = self.getTurretController().trackers
            headTrackers = self.getHeadController().trackers
            for tracker in turretTrackers:
                nodeInfo = tracker.tracker.nodeInfo
                nodeInfo.enableIdleAnimation = enableIdle
                if enableShoot == True:
                    nodeInfo.playShootAnimation()

            for tracker in headTrackers:
                tracker.tracker.nodeInfo.enableIdleAnimation = enableIdle

        except Exception as e:
            print e

    def trackerUpdateAngles(self, mountPoint, minPitch, maxPitch, minYaw, maxYaw):
        turretTrackers = self.getTurretController().trackers
        for tracker in turretTrackers:
            if tracker.mountPoint == mountPoint:
                trackerInfo = tracker.tracker.nodeInfo
                trackerInfo.minYaw = math.radians(minYaw)
                trackerInfo.maxYaw = math.radians(maxYaw)
                trackerInfo.minPitch = math.radians(minPitch)
                trackerInfo.maxPitch = math.radians(maxPitch)

    def landTurretTrackers(self):
        turretTrackers = self.getTurretController().trackers
        headTrackers = self.getHeadController().trackers
        for tracker in turretTrackers:
            tracker.setDefaultDirection()

        for tracker in headTrackers:
            tracker.setDefaultDirection()

    def onLoaded_internal(self, objectBuilder):
        self.context.particleNames = objectBuilder.getParticleNames()
        self.context.loftNames = objectBuilder.getLoftNames()
        ModelManipulator3.onLoaded_internal(self, objectBuilder)
        if self.__callback:
            self.__callback()
            self.__callback = None
        return

    def addNodeDirty(self, nodeName, localMatrix):
        self.__nodesDirty[nodeName] = localMatrix

    def addPartDirty(self, partId, upgradeId, mountPoint = ''):
        if (partId, upgradeId, mountPoint) not in self.__partsDirty:
            self.__partsDirty.append((partId, upgradeId, mountPoint))
            partName = self.context.partsNames[partId]
            attachedIK = self.context.ikSystemByPart.get(partName, None)
            if attachedIK is not None:
                attachedIK.refresh()
        return

    def setPoleVector(self, partId, handleName, poleVector):
        partName = self.context.partsNames[partId]
        ikSystem = self.context.ikSystemByPart[partName]
        handle = ikSystem.getIKHandle(handleName)
        handle.poleVector = poleVector

    def _saveVisual(self, dataSection, allnodes):
        changed = False
        try:
            identifier = dataSection.readString('identifier', '')
            if allnodes or identifier.startswith('HP_'):
                for nodeName, matrix in self.__nodesDirty.iteritems():
                    if nodeName == identifier:
                        dataSection.writeMatrix('transform', matrix)
                        changed = True

            for item in dataSection.values():
                if item.name == 'node':
                    changed = self._saveVisual(item, allnodes) or changed

        except Exception as e:
            print '_saveVisual: ', e

        return changed

    def saveVisualsList(self, visuals, allnodes, errorMsg = []):
        saved = True
        readonlyfiles = []
        if len(self.__nodesDirty) > 0:
            import os
            import stat
            for res in visuals:
                path = ResMgr.resolveToAbsolutePath(res)
                fileAtt = os.stat(path)[0]
                writable = fileAtt & stat.S_IWRITE
                root = ResMgr.openSection(res, False)
                if root != None:
                    changed = self._saveVisual(root, allnodes)
                    if changed:
                        if writable:
                            root.save()
                            ResMgr.purge(res, True)
                        else:
                            readonlyfiles.append(res)
                            saved = False

            if saved:
                self.__nodesDirty = {}
                self.__partsDirty = []
            elif len(readonlyfiles) > 0:
                errorMsg.append(' Files ' + ', '.join(readonlyfiles) + ' are read only!!!')
        return saved

    def __buildVisuals(self):
        visuals = []
        for partId, upgradeId, mountPoint in self.__partsDirty:
            if partId in self.partsHierarchy and upgradeId in self.partsHierarchy[partId]:
                states = self.partsHierarchy[partId][upgradeId]
                models = []
                for stateId, stateData in states.iteritems():
                    if isinstance(stateId, int):
                        modelPath = stateData['model']
                        if modelPath == '':
                            for subitemId, subitemData in stateData.iteritems():
                                if isinstance(subitemId, int) and subitemData['mountPoint'] == mountPoint:
                                    modelPath = subitemData['model']

                        if modelPath not in models:
                            models.append(modelPath)
                            while modelPath != '':
                                visPath = modelPath[:-5] + 'visual'
                                if visPath not in visuals:
                                    visuals.append(visPath)
                                    modelRes = ResMgr.openSection(modelPath, False)
                                    modelPath = ''
                                    if modelRes is not None:
                                        modelPath = modelRes.readString('parent', '')
                                        if modelPath != '':
                                            modelPath = modelPath + '.model'

        return visuals

    def saveVisuals(self, errorMsg = []):
        visuals = []
        allnodes = False
        if len(self.__partsDirty):
            visuals = self.__buildVisuals()
            allnodes = True
        else:
            visuals = self.context.visuals.keys()
        return self.saveVisualsList(visuals, allnodes, errorMsg)

    def __getTextureQuality(self):
        return 1

    def addShadowEntity(self):
        pass

    def __createGroundDecal(self, partId, partState, refresh = False):
        return ModelManipulator3.__createGroundDecal(self, partId, partState, True)

    @staticmethod
    def buildPivots(context):
        if context.weaponsSlotsDBData:
            partByNames = dict()
            for partDb in context.objDBData.partsSettings.getPartsOnlyList():
                partByNames[partDb.name] = partDb

            flameData = list()
            for slotId, slotData in context.weaponsSlotsDBData.slots.iteritems():
                for typeId, weaponsData in slotData.types.iteritems():
                    for linkedModelDescription in weaponsData.linkedModels:
                        hpMap = syncHpMap(linkedModelDescription.model)
                        partName, mountPoint = ObjectDataReader._partAndHp(linkedModelDescription.mountPath)
                        partType = partByNames[partName].getPartType(linkedModelDescription.parentUpgrade)
                        if partType:
                            parentModelName = partType.states[1].model
                            parentHpMap = syncHpMap(parentModelName)
                            parentHp = Math.Matrix(parentHpMap[mountPoint])
                            partId = partByNames[partName].partId
                            while partName != ObjectDataReader.HULL_PART_NAME:
                                partName, mountPoint = ObjectDataReader._partAndHp(partByNames[partName].mountPoint)
                                parentModelName = partByNames[partName].getPartType(1).states[1].model
                                parentHpMap = syncHpMap(parentModelName)
                                parentHp.postMultiply(parentHpMap[mountPoint])

                            for hpKey, hpValue in hpMap.iteritems():
                                flameName = '{0}/{1}/{2}/{3}/{4}/{5}'.format(partId, linkedModelDescription.parentUpgrade, slotId, typeId, linkedModelDescription.mountPath, hpKey)
                                matrix = Math.Matrix(hpValue)
                                matrix.postMultiply(parentHp)
                                flameData.append((flameName, matrix.translation, (matrix.yaw, matrix.pitch, matrix.roll)))

            return flameData

    @staticmethod
    def buildCenterOfMass(context):
        massData = list()
        CONST_HPNAME = 'HP_mass'
        CONST_MODEL_NAME = 'model'
        if context.partsHierarchy:
            for partDB in context.objDBData.partsSettings.getPartsOnlyList():
                if partDB.name == PLANE_PART_NAME:
                    for partId in context.partsHierarchy.iterkeys():
                        if partId == partDB.partId:
                            modelName = context.partsHierarchy[partDB.partId][1][1][CONST_MODEL_NAME]
                            parentHpMap = syncHpMap(modelName)
                            if CONST_HPNAME in parentHpMap:
                                matrix = Math.Matrix(parentHpMap[CONST_HPNAME])
                                massData = (matrix.translation, (matrix.yaw, matrix.pitch, matrix.roll))
                            else:
                                debug_utils.LOG_TRACE('No HP_Mass node found')
                            break

        return massData