# Embedded file name: scripts/common/db/DBEffects.py
import db.DBLogic

class Effects:

    @staticmethod
    def getEffectId(effectName):
        return db.DBLogic.g_instance.getEffectId(effectName)

    @staticmethod
    def exists(effectNameToCheck):
        return db.DBLogic.g_instance.getEffectExists(effectNameToCheck)