# Embedded file name: scripts/common/exchangeapi/IfaceUtils.py
from _ifaces import Ifaces
from debug_utils import LOG_ERROR
from _oblocations import Objects
IfacesByParentDB = {}

def initDB():
    for index, iface in enumerate(Ifaces.iface):
        iface.index = index
        iface.attr = sorted(iface.attr)
        yield (iface.ifacename, iface)


IfacesDB = dict(initDB())
ObTypes = sorted(set((obtype for item in Objects.object for obtype in item.obtype)))
ObTypesDB = {obtype:i for i, obtype in enumerate(ObTypes)}

class IfaceNotFound(Exception):
    pass


def getIface(ifacename):
    from CommonUtils import iface_name
    iname = iface_name(ifacename)
    try:
        return IfacesDB[iname]
    except KeyError:
        raise IfaceNotFound("Iface '%s' can't be found" % iname)


def initParentDB(iface, ifacename):
    for parent in iface.parent:
        IfacesByParentDB.setdefault(parent, set()).add(iface.ifacename)
        if parent != ifacename:
            IfacesByParentDB.setdefault(parent, set()).add(ifacename)
        initParentDB(getIface(parent), ifacename)


for iface in Ifaces.iface:
    initParentDB(iface, iface.ifacename)

def isCallbackSubscriable(ifacename):
    try:
        return getIface(ifacename).callbackSubscriable
    except IfaceNotFound as msg:
        LOG_ERROR(msg)

    return False


def getChildIfaceNames(parentIfaceName):
    from CommonUtils import iface_name
    return IfacesByParentDB.get(iface_name(parentIfaceName), set())