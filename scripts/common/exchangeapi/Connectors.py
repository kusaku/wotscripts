# Embedded file name: scripts/common/exchangeapi/Connectors.py
from _airplanesConfigurations_db import airplanesConfigurations
from consts import COMPONENT_TYPE
from debug_utils import LOG_ERROR
from db.DBLogic import initDB, UpgradeNotFoundException, AircraftNotFoundException
from exchangeapi.CommonUtils import splitIDTypeList, idFromList
from functools import partial

class PlaneObject:

    def __init__(self, iD):
        self.id = iD


def getCamouflage(obid, account = None):
    from _camouflages_data import getCamouflage
    return getCamouflage(obid)


def getPlane(obid, account = None):
    try:
        from db.DBLogic import g_instance as db_instance
        return db_instance.getAircraftData(obid).airplane
    except AircraftNotFoundException:
        return None

    return None


def getPlanePreset(obid, account = None):
    plane = airplanesConfigurations.get(obid, None)
    if plane is None:
        LOG_ERROR('Plane was not found by globalId', obid)
        return
    else:
        planeId = plane.planeID
        ob = {}
        ob['preset'] = airplanesConfigurations.get(obid, None)
        ob['plane'] = plane
        ob['globalID'] = obid
        return ob


def getUpgrade(obid, account = None):
    if obid < 0:
        return None
    else:
        try:
            from db.DBLogic import g_instance as db_instance
            return db_instance.upgrades[db_instance.getUpgradeNameByID(obid)]
        except UpgradeNotFoundException:
            return None

        return None


def getAmmoBelt(obid, account = None):
    from db.DBLogic import g_instance as db_instance
    return db_instance.getComponentByID(COMPONENT_TYPE.AMMOBELT, obid)


def getGun(obid, account = None):
    from db.DBLogic import g_instance as db_instance
    return db_instance.getComponentByID(COMPONENT_TYPE.GUNS, obid)


def getConsumable(obid, account = None):
    from db.DBLogic import g_instance as db_instance
    return db_instance.getConsumableByID(obid)


def getPlaneObject(obid, account = None):
    return PlaneObject(obid)


def getEquipment(obid, account = None):
    from db.DBLogic import g_instance as db_instance
    return db_instance.getEquipmentByID(obid)


def getBomb(obid, account = None):
    from db.DBLogic import g_instance as db_instance
    return db_instance.getComponentByID(COMPONENT_TYPE.BOMBS, obid)


def getRocket(obid, account = None):
    from db.DBLogic import g_instance as db_instance
    return db_instance.getComponentByID(COMPONENT_TYPE.ROCKETS, obid)


def getSkill(obid, account = None):
    from db.DBLogic import g_instance as db_instance
    return db_instance.getSkillByID(obid)


def getAward(obid, account = None):
    import _awards_data
    return getattr(_awards_data.AwardsDB.get(obid, None), 'ui', None)


def getPeriphery(obid, account = None):
    return {'name': 'periphery_' + str(obid)}


def getBattleResult(obid, account = None):
    from Helpers.cache import getFromCache
    return getFromCache([[obid, 'battleResult']], 'IBattleResult')


def getActionUI(obid, account):
    return account.quests.getActionUIDescription(obid)


def getPack(obid, account = None):
    from _packs_db import Packs
    return Packs.packs.get(obid)


connectors = {'plane': getPlane,
 'planePreset': getPlanePreset,
 'upgrade': getUpgrade,
 'ammobelt': getAmmoBelt,
 'gun': getGun,
 'consumable': getConsumable,
 'weaponslot': getPlaneObject,
 'slotConfig': getPlaneObject,
 'equipment': getEquipment,
 'bomb': getBomb,
 'rocket': getRocket,
 'skill': getSkill,
 'achievement': getAward,
 'ribbon': getAward,
 'medal': getAward,
 'camouflage': getCamouflage,
 'periphery': getPeriphery,
 'battleResult': getBattleResult,
 'actionui': getActionUI,
 'pack': getPack}

def getObject(idTypeList, account = None):
    initDB()
    idList, typeList = splitIDTypeList(idTypeList)
    if idList and typeList:
        if len(idList) > 1:
            obList = map(lambda x: (x[0] if x[0] is None else getObject([x], account)), idTypeList)
            return connectors.get(idFromList(typeList), lambda x, _: x)(obList, account)
        elif idList[0] is None:
            return
        else:
            return connectors.get(typeList[0], lambda x, _: x)(idList[0], account)
    return