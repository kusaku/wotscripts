# Embedded file name: scripts/client/fm/FMPlayerAvatar.py
import functools
import BattleReplay
import BigWorld
from EntityHelpers import canFireControllEntity, EntityStates
import Settings
from fm.FMAvatarMethods import fmAvatarMethods

def fmPlayerAvatar(objClass):
    FM_FILTER = EntityStates.CREATED | EntityStates.WAIT_START | EntityStates.GAME_CONTROLLED | EntityStates.DESTROYED_FALL | EntityStates.PRE_START_INTRO

    def fm(func):

        @functools.wraps(func)
        def decorated(*args, **kwargs):
            if args[0].filter.__class__ == BigWorld.FMFilter:
                getattr(args[0].filter, func.func_name)(*args[1:], **kwargs)

        return decorated

    @fmAvatarMethods(fm)

    class PlayerAvatar(objClass):

        def onBecomePlayer(self):
            objClass.onBecomePlayer(self)
            self.__firing = False

        def calcCorrectFireFlags(self, flag):
            flag = objClass.calcCorrectFireFlags(self, flag)
            if canFireControllEntity(self):
                armaments = self.controllers['weapons'].calcArmaments(flag)
                self.__firing = armaments != 0
                self.armamentStates = armaments
            return flag

        def __useFMFilter(self):
            return EntityStates.inState(self, FM_FILTER) and Settings.g_instance.getFastFMEnabled()

        def createFilter(self):
            if self.__useFMFilter():
                return BigWorld.FMFilter()
            else:
                return objClass.createFilter(self)

        def movementFilter(self):
            if self.__useFMFilter():
                return self.filter.__class__ == BigWorld.FMFilter
            else:
                return objClass.movementFilter(self)

        def onRespawn(self):
            objClass.onRespawn(self)
            if self.filter.__class__ == BigWorld.FMFilter:
                self.filter.fmReset()

        def set_armamentStates(self, oldValue):
            objClass.set_armamentStates(self, oldValue)
            if self.__useFMFilter():
                if self.__firing:
                    if self.armamentStates != 0:
                        self.lastArmamentStates = self.armamentStates
                else:
                    self.armamentStates = 0

        def set_fmTimeOffset(self, oldValue):
            if self.filter.__class__ == BigWorld.PredictionFilter:
                self.filter.fmTimeOffset = self.fmTimeOffset

    PlayerAvatar.__name__ = objClass.__name__
    return PlayerAvatar