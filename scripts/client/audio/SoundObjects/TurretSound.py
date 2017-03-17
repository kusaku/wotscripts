# Embedded file name: scripts/client/audio/SoundObjects/TurretSound.py
from WwiseGameObject import WwiseGameObject, WwiseGameObjectFactory, GS
import db.DBLogic
import BigWorld
from WeaponSound import WeaponSound
import GameEnvironment
from audio.SoundObjectSettings import SoundObjectSettings
from audio.SoundBanksManager import SoundBanksManager
from audio.AKConsts import SOUND_CASES

class TurretSound(WeaponSound):

    def __init__(self, eid, cid, node, weaponSoundID, shootEvent, isAA = False, isTL = False):
        WeaponSound.__init__(self, eid, cid, node, weaponSoundID, shootEvent, isAA, isTL)


g_factory = None

class TurretSoundFactory(WwiseGameObjectFactory):

    def createPlayer(self, so):
        player = BigWorld.player()
        turrets = player.controllers.get('turretsLogic', None)
        shootEvent = TurretSound.getShootEventName(False, False, True, so.soundSet)
        if turrets and shootEvent:
            so.wwiseGameObject = TurretSound(player.id, so.context.cidProxy.handle, so.node.id, so.weaponID, shootEvent, False, True)
            turrets.linkSound(so.wwiseGameObject)
        return

    def createAvatar(self, avatar, so):
        if so.wwiseGameObject:
            return
        shootEvent = TurretSound.getShootEventName(False, False, False, so.soundSet)
        arena = GameEnvironment.getClientArena()
        avatarInfo = arena.avatarInfos.get(avatar.id, {})
        turrets = avatarInfo.get('turretsLogic')
        if turrets and shootEvent:
            so.wwiseGameObject = TurretSound(avatar.id, so.context.cidProxy.handle, so.node.id, so.weaponID, shootEvent, False, True)
            turrets.linkSound(so.wwiseGameObject)

    def createTurret(self, object, so, val):
        shootEvent = TurretSound.getShootEventName(False, True, False, so.soundSet)
        if shootEvent:
            so.wwiseGameObject = TurretSound(object, so.context.cidProxy.handle, so.node.id, so.weaponID, shootEvent, True, False)
            val['turretsLogic'].linkSound(so.wwiseGameObject)

    @staticmethod
    def instance():
        global g_factory
        if not g_factory:
            g_factory = TurretSoundFactory()
        return g_factory

    @staticmethod
    def getSoundObjectSettings(data):
        modelManipulator = data['modelManipulator']
        partByNames = data['partByNames']
        objectBuilder = data['objectBuilder']
        isPlayer = data['isPlayer']
        turretSoundID = data['turretSoundID']
        soundObjects = data['soundObjects']
        context = data['context']
        if turretSoundID is not None:
            for snd in turretSoundID:
                isAA = str(snd).find('AA') != -1
                isTL = isPlayer and str(snd).find('TL') != -1
                hp = 'HP_mass'
                for p in partByNames:
                    if str(p).find('gun') != -1 and hasattr(partByNames[p], 'mountPoint'):
                        hp = partByNames[p].mountPoint
                        break

                so = SoundObjectSettings()
                so.context = context
                pathList = modelManipulator.ModelManipulator3.ObjectDataReader._resolvePath(hp, '', partByNames)
                so.node = objectBuilder.rootNode.resolvePath(modelManipulator.CompoundBuilder.convertPath(pathList))
                so.weaponID = snd
                so.soundSet = GS().findLoadSet(db.DBLogic.g_instance.getWeaponSoundSet(so.weaponID), isPlayer, isAA, isTL)
                so.factory = TurretSoundFactory.instance()
                soundObjects.append(so)

        return