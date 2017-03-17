# Embedded file name: scripts/common/db/DBDecals.py
g_decalCount = 0

class Decals:

    @staticmethod
    def getDecalId(decalName):
        return Decals.__dict__[decalName]

    @staticmethod
    def getDecalNameId(decalID):
        for i, v in Decals.__dict__.items():
            if type(v) == int and v == decalID:
                return i

        return None

    @staticmethod
    def exists(decalNameToCheck):
        """True if decal with the given name exists; False if not."""
        for decalName, decalId in Decals.__dict__.items():
            if type(decalId) == int and decalName == decalNameToCheck:
                return True
        else:
            return False

    @staticmethod
    def addNewDecalID(decalName):
        global g_decalCount
        Decals.__dict__[decalName] = g_decalCount
        g_decalCount += 1