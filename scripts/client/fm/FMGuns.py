# Embedded file name: scripts/client/fm/FMGuns.py
from WeaponsHelpers import isGunGroupShooting

def fmGuns(objClass):

    class Guns(objClass):

        def calcArmaments(self, fireFlags):
            armaments = 0
            for bit, group in enumerate(self.__weaponGroups):
                if isGunGroupShooting(fireFlags, bit):
                    armaments |= 1 << bit

            return armaments

        def cellUpdate(self, dt, fireFlags):
            armaments = self.calcArmaments(fireFlags)
            self.commonUpdate(dt, armaments)
            self.eTotalRecoilGunsThrust(self.__totalRecoilThrust)
            return armaments

    Guns.__name__ = objClass.__name__
    return Guns