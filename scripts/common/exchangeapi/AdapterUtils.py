# Embedded file name: scripts/common/exchangeapi/AdapterUtils.py
from _adapters import Adapters
from debug_utils import LOG_ERROR
from adapters.DefaultAdapter import DefaultAdapter
from IfaceUtils import IfaceNotFound
from consts import IS_CLIENT, OB_LOCATION
from exchangeapi._oblocations import Objects
OblocationDB = None
OblocationObjectsDB = None
AdaptersDB = None

def adapter_id(ifacename, typeList):
    from exchangeapi.CommonUtils import iface_name
    return '%s:%s' % (iface_name(ifacename), ':'.join(typeList))


def getOblocation(ifacename, typeList):
    global OblocationDB
    adapterid = adapter_id(ifacename, ((i if i is not None else 'account') for i in typeList or ['account']))
    try:
        return OblocationDB[adapterid]
    except KeyError:
        LOG_ERROR("Adapter '%s' can't be found" % adapterid)


def getOblocationDBObject(ifacename, typeList):
    global OblocationObjectsDB
    adapterid = adapter_id(ifacename, ((i if i is not None else 'account') for i in typeList or ['account']))
    try:
        return OblocationObjectsDB[adapterid]
    except KeyError:
        LOG_ERROR("Adapter '%s' can't be found" % adapterid)


def import_adapter(adapter):
    oblocation = getOblocation(adapter.ifacename, adapter.obtype)
    if IS_CLIENT and oblocation == OB_LOCATION.CLIENT or oblocation == OB_LOCATION.MIXED or not IS_CLIENT and oblocation != OB_LOCATION.CLIENT:
        from exchangeapi.CommonUtils import import_string
        return import_string(adapter, oblocation != OB_LOCATION.CLIENT)
    else:
        return None


def initDB():
    global AdaptersDB
    global OblocationDB
    global OblocationObjectsDB
    if OblocationDB is None:
        OblocationDB = dict(((adapter_id(ob.ifacename, ob.obtype), ob.oblocation) for ob in Objects.object))
    if OblocationObjectsDB is None:
        OblocationObjectsDB = dict(((adapter_id(ob.ifacename, ob.obtype), ob) for ob in Objects.object))
    if AdaptersDB is None:

        def formDB():
            for adapter in Adapters.adpater:
                item = import_adapter(adapter)
                if item is not None:
                    item = item(adapter.ifacename)
                yield (adapter_id(adapter.ifacename, adapter.obtype), item)

            return

        AdaptersDB = dict(formDB())
    return


initDB()

class AdapterNotFound(Exception):
    pass


def getAdapter(ifacename, typeList, default = DefaultAdapter, silent = False):
    adapterid = adapter_id(ifacename, ((i if i is not None else 'account') for i in typeList or ['account']))
    try:
        return AdaptersDB[adapterid] or default(ifacename)
    except KeyError:
        if default or silent:
            return default(ifacename)
        LOG_ERROR("Adapter '%s' can't be found" % adapterid)
    except IfaceNotFound as msg:
        LOG_ERROR(msg)


def getAdaptedOb(ob, iface, *args):
    return getAdapter(*args)(ob, iface)()