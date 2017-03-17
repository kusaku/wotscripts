# Embedded file name: scripts/editors/ObjectsBuilderEditor.py
from modelManipulator.CompoundBuilder import ObjectsBuilder
from modelManipulator.CompoundBuilder import syncHpMap
from modelManipulator.CompoundBuilder import convertPath
from modelManipulator.ModelManipulator3 import ObjectDataReader

class ObjectsBuilderEditor(ObjectsBuilder):

    def __init__(self, animationController, boolCombiner, eventSystem, context, onLoadedCallback):
        ObjectsBuilder.__init__(self, animationController, boolCombiner, eventSystem, context, onLoadedCallback)
        self.context = context
        self.context.fireEffectsPerUpgrade = []
        self.context.turretTrackers = []
        self.context.headTrackers = []
        self.__particleNames = []
        self.__loftNames = []

    def addNode(self, path):
        node = self.rootNode.resolvePath(convertPath(path))

    def addParticleToList(self, nodeId, vis, particleFile, name):
        ObjectsBuilder.addParticleToList(self, nodeId, vis, particleFile, name)
        self.__particleNames.append((name, particleFile))

    def addLoftToList(self, nodeId, isVisible, effectDB, name):
        ObjectsBuilder.addLoftToList(self, nodeId, isVisible, effectDB, name)
        self.__loftNames.append(name)

    def getParticleNames(self):
        return self.__particleNames

    def getLoftNames(self):
        return self.__loftNames

    def postRead(self):
        self.context.partsHierarchy = {}
        self.context.partsNames = {}
        self.context.nodes = {}
        hardpoints = dict()
        partByNames = dict()
        modelParts = self.context.objDBData.partsSettings.getPartsOnlyList()
        for partDb in modelParts:
            partByNames[partDb.name] = partDb

        modelParts = self.context.objDBData.partsSettings.getPartsOnlyList()
        for partDb in modelParts:
            self.context.partsNames[partDb.partId] = partDb.name
            self.context.partsHierarchy[partDb.partId] = {'mountPoint': partDb.mountPoint}
            allNodes = True if partDb.name == 'turret' else False
            for upgradeDb in partDb.upgrades.values():
                bodyTypes = upgradeDb.bodyTypes.types.keys()
                self.context.partsHierarchy[partDb.partId][upgradeDb.id] = {'bboxes': upgradeDb.bboxes,
                 'componentXml': upgradeDb.componentXml,
                 'bodyTypes': bodyTypes}
                for stateDb in upgradeDb.states.values():
                    if stateDb.model != '':
                        hps = syncHpMap(stateDb.model, allNodes)
                        for hp in hps.keys():
                            hardpoints[hp] = ObjectDataReader._resolvePath(partDb.mountPoint, '', partByNames)

                    self.context.partsHierarchy[partDb.partId][upgradeDb.id][stateDb.id] = {'model': stateDb.model,
                     'fallingOutModel': stateDb.fallingOutModel}
                    subitemId = 0
                    for subItem in stateDb.subItems:
                        if subItem.model != '':
                            hps = syncHpMap(subItem.model, allNodes)
                            for hp in hps.keys():
                                hardpoints[hp] = subItem.mountPoint

                        self.context.partsHierarchy[partDb.partId][upgradeDb.id][stateDb.id][subitemId] = {'model': subItem.model,
                         'mountPoint': subItem.mountPoint,
                         'animatorName': subItem.animatorName,
                         'name': subItem.name}
                        subitemId += 1

        for hp, mpParent in hardpoints.iteritems():
            hppath = ObjectDataReader._resolvePath(hp, mpParent, partByNames)
            self.addNode(hppath)

        for parentId, node in self.rootNode.linearHierarchy:
            self.context.nodes[node.id] = node.name

        animationController = self._animationController
        self.context.headTrackers = animationController.getController('GunnerHeadController').trackers
        self.context.turretTrackers = animationController.getController('TurretController').trackers

    def addEffectForUpgrade(self, upgradeId, effect):
        self.context.fireEffectsPerUpgrade.append((upgradeId, effect))

    def loadResources(self):
        ObjectsBuilder.loadResources(self)
        self.context.visuals = self._visuals