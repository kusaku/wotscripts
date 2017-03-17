# Embedded file name: scripts/client/eventhandlers/onChangedDepotCount.py
from consts import COMPONENT_TYPE
_COMPONENT_BY_TYPE = {'bomb': COMPONENT_TYPE.BOMBS,
 'rocket': COMPONENT_TYPE.ROCKETS}

def onChangedDepotCount(event):
    upgradeID = next((iD for iD, typ in event.idTypeList if typ == 'upgrade'), None)
    from db.DBLogic import g_instance as dbInstance
    if upgradeID is None and event.idTypeList[0][1] in ('bomb', 'rocket'):
        upgradeID = event.idTypeList[0][0]
        component = dbInstance.getComponentByID(_COMPONENT_BY_TYPE[event.idTypeList[0][1]], upgradeID)
        upgradeName = component.name
    elif upgradeID is not None:
        upgrade = dbInstance.upgrades.get(dbInstance.getUpgradeNameByID(upgradeID), None)
        upgradeName = upgrade.name
    if upgradeID is not None and event.ob != event.prevob:
        from BWPersonality import g_lobbyCarouselHelper
        if not g_lobbyCarouselHelper.inventory.inventoryDataInitialized:
            return
        currentValue = g_lobbyCarouselHelper.inventory.getUpgradeCountInDepot(upgradeName)
        g_lobbyCarouselHelper.inventory.addUpgradeToDepot(upgradeName, event.ob['value'] - currentValue)
    return