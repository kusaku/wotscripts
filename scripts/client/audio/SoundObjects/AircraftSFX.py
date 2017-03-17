# Embedded file name: scripts/client/audio/SoundObjects/AircraftSFX.py
from WwiseGameObject import WwiseGameObject, GS, WwiseGameObjectFactory
import BigWorld
from audio.AKTunes import CritParts
from audio.AKConsts import PartState
import db.DBLogic
from audio.SoundObjectSettings import SoundObjectSettings

class AircraftSFX(WwiseGameObject):

    def __init__(self, cid, node, set):
        self.__eventSet = set
        self.__stall = False
        self.__state = PartState.Normal
        self.__flaps = False
        BigWorld.player().ePartCrit += self.__onPartCrit
        BigWorld.player().eReportDestruction += self.__onReportDestruction
        BigWorld.player().eLeaveWorldEvent += self.__onLeaveWorld
        GS().eOnStallDanger += self.__onStall
        GS().eOnBattleEnd += self.__onBattleEnd
        WwiseGameObject.__init__(self, 'AircraftSFX', cid, node)

    def play(self, what, cat = 'Misc', cb = None):
        tag = '{0}{1}'.format(cat, what)
        e = self.__eventSet[tag]
        self.postEvent(e, cb)

    def stop(self, what, cat = 'Misc', cb = None):
        tag = '{0}{1}'.format(cat, what)
        e = str(self.__eventSet[tag]).replace('Play_', 'Stop_')
        self.postEvent(e, cb)

    def playFlaps(self, value):
        if value == 0:
            self.stop('Flaps')
        elif not self.__flaps:
            self.play('Flaps', 'Misc', self.__stoppedFlapsCB)
            self.__flaps = True

    def __stoppedFlapsCB(self):
        self.__flaps = False

    def __onStall(self, stall):
        if self.__stall == stall:
            return
        if stall:
            self.play('Vibration', 'State')
            if BigWorld.player().altitudeAboveObstacle > 10:
                GS().voice.play('voice_stalling_danger')
        else:
            self.stop('Vibration', 'State')
        self.__stall = stall

    def __onReportDestruction(self, ki):
        if ki['victimID'] == BigWorld.player().id:
            WwiseGameObject.stopAll(self, 100)

    def __onLeaveWorld(self):
        WwiseGameObject.stopAll(self, 500, True)

    def __onPartCrit(self, part):
        stateID = part.logicalState
        name = part.partTypeData.componentType
        if stateID == PartState.Damaged and name in CritParts:
            self.play('Crit', 'State')
        else:
            self.stop('Crit', 'State')
        self.__setPartState(name, stateID, part.damageReason)

    def __setEngineState(self, stateID, damageReason):
        if stateID < self.__state:
            if stateID == PartState.Normal:
                GS().voice.playPartStateSpeech('Engine', PartState.Repaired, damageReason)
            elif stateID == PartState.Damaged:
                GS().voice.playPartStateSpeech('Engine', PartState.RepairedPartly, damageReason)
        GS().voice.playPartStateSpeech('Engine', stateID, damageReason)
        self.__state = stateID

    def __setPartState(self, partName, stateID, damageReason):
        if partName == 'Engine':
            self.__setEngineState(stateID, damageReason)
            return
        GS().voice.playPartStateSpeech(partName, stateID, damageReason)

    def __onBattleEnd(self):
        self.stop('Flaps', 'Misc', self.__stoppedFlapsCB)


g_factory = None

class AircraftSFXFactory(WwiseGameObjectFactory):

    def createPlayer(self, so):
        so.wwiseGameObject = AircraftSFX(so.context.cidProxy.handle, so.node.id, so.soundSet)

    @staticmethod
    def instance():
        global g_factory
        if not g_factory:
            g_factory = AircraftSFXFactory()
        return g_factory

    @staticmethod
    def getSoundObjectSettings(data):
        if not data['isPlayer']:
            return
        modelManipulator = data['modelManipulator']
        info = data['info']
        partByNames = data['partByNames']
        objectBuilder = data['objectBuilder']
        soundObjects = data['soundObjects']
        context = data['context']
        so = SoundObjectSettings()
        hp = 'plane/HP_mass'
        pathList = modelManipulator.ModelManipulator3.ObjectDataReader._resolvePath(hp, '', partByNames)
        misc = db.DBLogic.g_instance.getAircraftSFX(info.misc)
        states = db.DBLogic.g_instance.getAircraftStates(info.states)
        so.node = objectBuilder.rootNode.resolvePath(modelManipulator.CompoundBuilder.convertPath(pathList))
        so.soundSet = misc.copy()
        so.soundSet.update(states)
        so.factory = AircraftSFXFactory.instance()
        so.context = context
        soundObjects.append(so)