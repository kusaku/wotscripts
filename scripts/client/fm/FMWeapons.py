# Embedded file name: scripts/client/fm/FMWeapons.py


def fmWeapons(objClass):

    class Weapons(objClass):

        def calcArmaments(self, fireFlags):
            return self.__guns.calcArmaments(fireFlags)

    Weapons.__name__ = objClass.__name__
    return Weapons