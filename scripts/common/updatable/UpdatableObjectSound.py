# Embedded file name: scripts/common/updatable/UpdatableObjectSound.py
import BigWorld
from consts import IS_CLIENT
from UpdatableObjectBase import UPDATABLE_STATE
if IS_CLIENT:
    from audio.SoundObjects import ShellSound

def isClient(func):

    def wrapper(*args):
        if IS_CLIENT:
            func(*args)

    return wrapper


class UpdatableObjectSound:

    @isClient
    def __init__(self, soundName, creatorOwnerID):
        self.__soundName = soundName
        self.__isPlayer = BigWorld.player().id == creatorOwnerID
        self.__dp = None
        self.__soundObject = None
        return

    @isClient
    def updatePosition(self):
        if not self.__isPlayer or not self.__soundObject or self.__soundObject.destroyed:
            return
        player = BigWorld.player()
        self.__dp = player.position - self.__dp
        self.__soundObject.setPosition(self.__soundObject.pos + self.__dp)
        self.__dp = player.position

    @isClient
    def startSound(self, shellDesc, position, state):
        if not hasattr(shellDesc, 'weaponSoundID') or UPDATABLE_STATE.DESTROY == state:
            return
        player = BigWorld.player()
        self.__dp = player.position
        self.__soundObject = ShellSound('{0}-{1}'.format(self.__soundName, shellDesc.weaponSoundID), 0, 0, position, shellDesc.weaponSoundID, self.__isPlayer)
        self.__soundObject.play()

    @isClient
    def stopSound(self):
        if self.__soundObject:
            self.__soundObject.stop()