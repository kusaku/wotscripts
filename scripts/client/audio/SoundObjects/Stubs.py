# Embedded file name: scripts/client/audio/SoundObjects/Stubs.py


class WwiseGameObject:
    pass


class AircraftEngineSound(WwiseGameObject):

    def __init__(self, eid, cid, node, soundSet):
        pass

    def play(self, state = 'Main', npc = False):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def spectate(self, spectated):
        pass


class AircraftSFX(WwiseGameObject):

    def __init__(self, cid, node, set):
        pass

    def play(self, what, cat = 'Misc'):
        pass

    def stop(self, what, cat = 'Misc'):
        pass

    def playFlaps(self, value):
        pass

    def update(self, speedMPS):
        pass


class AirshowSound(WwiseGameObject):

    def __init__(self, player):
        pass


class EffectSound(WwiseGameObject):

    def __init__(self, id, cid, node, position = None, sfxSwitch = None):
        pass

    def play(self):
        pass

    def stop(self):
        pass


class ExplosionSound(WwiseGameObject):

    def __init__(self):
        pass


class HitSound(WwiseGameObject):

    def __init__(self):
        pass


class Music(WwiseGameObject):

    def __init__(self):
        pass

    def event(self, name, eventEndCB = None):
        pass

    def playHangar(self, isPremium, space):
        pass

    def unloadHangar(self):
        pass

    def unloadArena(self):
        pass

    def playArena(self):
        pass

    def stopArena(self):
        pass

    def playBattle(self, ownScore, enemyScore):
        pass

    def startBattle(self, eid):
        pass

    def endBattle(self, eid):
        pass

    def playVictimDestroyed(self, killingInfo):
        pass

    def playTeamObjectDestroyed(self, killerID, objectTeamIndex):
        pass


class ShellSound(WwiseGameObject):

    def __init__(self, name, cid, node, position):
        pass


class TurretSound:

    def __init__(self):
        pass


class UI(WwiseGameObject):

    def __init__(self):
        pass

    def play(self, tag):
        pass


class Voiceover(WwiseGameObject):
    PRIORITY_DISCARD = 0
    PRIORITY_ENQUEUE = 1
    PRIORITY_EXCLUSIVE = 2

    def __init__(self):
        pass

    def init(self):
        pass

    def load(self):
        pass

    def enableGameMsgs(self, enable):
        pass

    def play(self, name):
        pass

    def stop(self):
        pass

    def playTutorial(self, name):
        pass

    def stopTutorial(self):
        pass

    def playPartStateSpeech(self, partName, stateID):
        pass

    def onBattleStart(self):
        pass


class WeaponSound(WwiseGameObject):

    def __init__(self, eid, cid, node, weaponSoundID, soundSet, isAA = False, isTL = False):
        pass

    def play(self):
        pass

    def stop(self):
        pass


class WindSound(WwiseGameObject):

    def __init__(self, id, cid, node):
        pass


class WwiseGameObjectFactory:
    pass


class AircraftEngineSoundFactory(WwiseGameObjectFactory):
    pass


class AircraftSFXFactory(WwiseGameObjectFactory):
    pass


class AirshowSoundFactory(WwiseGameObjectFactory):
    pass


class TurretSoundFactory(WwiseGameObjectFactory):
    pass


class WeaponSoundFactory(WwiseGameObjectFactory):
    pass


class WindSoundFactory(WwiseGameObjectFactory):
    pass