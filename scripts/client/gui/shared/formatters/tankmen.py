# Embedded file name: scripts/client/gui/shared/formatters/tankmen.py
from helpers import dependency
from skeletons.gui.shared import IItemsCache

@dependency.replace_none_kwargs(itemsCache=IItemsCache)
def formatDeletedTankmanStr(tankman, itemsCache = None):
    vehicle = itemsCache.items.getItemByCD(tankman.vehicleNativeDescr.type.compactDescr)
    return tankman.fullUserName + ' (%s, %s)' % (tankman.roleUserName, vehicle.userName)