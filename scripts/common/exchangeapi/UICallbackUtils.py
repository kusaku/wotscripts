# Embedded file name: scripts/common/exchangeapi/UICallbackUtils.py
from _functools import partial
import consts
import debug_utils
from exchangeapi.CommonUtils import convertIfaceDataForUI, METHODTOINDEX, convertIDTypeListForUI, splitIDTypeList, idFromList, COMMAND_TYPES, listFromId, joinIDTypeList
from exchangeapi.IfaceUtils import isCallbackSubscriable, getIface
from consts import IS_CLIENT
from debug_utils import LOG_DEBUG
from exchangeapi import ErrorCodes
UI_CALLBACKS = {}
UI_CALLBACKS_SUBSCRIABLE = {}
PARENT_INTERFACES = {}

def sendSavedUICallbacks(ifacehandler):
    for ids, typesDict in UI_CALLBACKS.iteritems():
        idList = listFromId(ids)
        for types, ifaces in typesDict.iteritems():
            typeList = listFromId(types)
            for iface, callbacks in ifaces.iteritems():
                idTypeList = joinIDTypeList(idList, typeList)
                for callback in callbacks:
                    ifacehandler.viewIFace([[{iface: {}}, idTypeList]], callback)


def clearUICallbacks(clearSubscriavble = True):
    UI_CALLBACKS.clear()
    PARENT_INTERFACES.clear()
    if clearSubscriavble:
        UI_CALLBACKS_SUBSCRIABLE.clear()


def removeFromCache(ids, types, iface, callbacks, subscriable = False):
    if subscriable and not isCallbackSubscriable(iface):
        return
    data = UI_CALLBACKS if not subscriable else UI_CALLBACKS_SUBSCRIABLE
    if isinstance(callbacks, basestring):
        callbacks = set([callbacks])
    cached = data.get(ids, {}).get(types, {}).get(iface, set())
    cached.difference_update(callbacks)
    if not cached:
        try:
            del UI_CALLBACKS[ids][types][iface]
            if not UI_CALLBACKS[ids][types]:
                del UI_CALLBACKS[ids][types]
                if not UI_CALLBACKS[ids]:
                    del UI_CALLBACKS[ids]
        except KeyError:
            pass

    if not subscriable:
        removeFromCache(ids, types, iface, callbacks, True)
        debug_utils.IfaceDebugOutput(COMMAND_TYPES.UNSUBSCRIBE, ifacename=iface, obtype=types, obid=ids, callbacks=callbacks)


def addToCache(ids, types, iface, callbacks, subscriable = False):
    if subscriable and not isCallbackSubscriable(iface):
        return
    if isinstance(callbacks, basestring):
        callbacks = set([callbacks])
    data = UI_CALLBACKS if not subscriable else UI_CALLBACKS_SUBSCRIABLE
    data.setdefault(ids, {}).setdefault(types, {}).setdefault(iface, set()).update(callbacks)
    if not subscriable:
        addToCache(ids, types, iface, callbacks, True)
        debug_utils.IfaceDebugOutput(COMMAND_TYPES.SUBSCRIBE, ifacename=iface, obtype=types, obid=ids, callbacks=callbacks)


def getDefaultCallbacks(ifaceName, lobby, data):
    from exchangeapi.IfaceUtils import IfaceNotFound
    try:
        return filter(None, [getIface(ifaceName).defaultCallback])
    except IfaceNotFound as msg:
        debug_utils.LOG_ERROR(msg)

    return []


def addUICallback(respdata, callback, ifacehandler, data = UI_CALLBACKS, force = False):
    for ifaces, idTypeList in respdata:
        ids, types = map(idFromList, splitIDTypeList(idTypeList))
        for iface in ifaces:
            callbacks = set(data.get(ids, {}).get(types, {}).get(iface, []))
            if force or ifaces[iface]:
                if callback and callback not in callbacks:
                    addToCache(ids, types, iface, callback)
            elif callbacks:
                removeFromCache(ids, types, iface, callbacks)


def removeAllUICallbacks():
    LOG_DEBUG('Removed all UI callbacks')
    clearUICallbacks(False)
    UI_CALLBACKS.update(UI_CALLBACKS_SUBSCRIABLE)


def removeUICallback(requestdata, callback, ifacehandler, data = UI_CALLBACKS):
    for ifaces, idTypeList in requestdata:
        ids, types = map(idFromList, splitIDTypeList(idTypeList))
        for iface in ifaces:
            callbacks = set(data.get(ids, {}).get(types, {}).get(iface, []))
            if callback and callback in callbacks:
                removeFromCache(ids, types, iface, callback)
            elif callback is None and callbacks:
                removeFromCache(ids, types, iface, callbacks)

    return


def sendDataToUICallbacks(headers, respdata, callback, ifacehandler = None, data = UI_CALLBACKS, fromserver = False, broadcast = True, proccesedIfaces = None):
    data = dict(data)
    from Helpers.ExchangeObBuilder import ExchangeObBuilder, cacheIFaceData, responseEventGenerate
    from Helpers.cache import getFromCache
    proccesedIfaces = proccesedIfaces or dict()
    if callback:
        ifacehandler.addResponseCallbackToQueue(partial(ifacehandler.call_1, callback, convertIfaceDataForUI(respdata), 0))
    for ifaces, idTypeList in respdata:
        ids, types = map(idFromList, splitIDTypeList(idTypeList))
        for ifacename in ifaces:
            if ifacename in proccesedIfaces.get(ids, {}).get(types, set([])):
                continue
            ifacedata = {ifacename: ifaces[ifacename]}
            idata = [[ifacedata, idTypeList]]
            iface = getIface(ifacename)
            if fromserver:
                from Helpers.ExchangeObBuilder import processIFaceData
                processIFaceData([int(not IS_CLIENT), METHODTOINDEX['view']], idata)
                responseEventGenerate(headers, idata)
                cacheIFaceData(idata)
                if ifacedata[ifacename]:
                    for c in getDefaultCallbacks(ifacename, ifacehandler, data):
                        addUICallback([[{ifacename: True}, idTypeList]], c, ifacehandler, data)

                    data.update(UI_CALLBACKS)
                if iface.parent:

                    def constructed(ifacehandler, fromserver, broadcast, proccesedIfaces, responseob):
                        if responseob[-1] == ErrorCodes.SUCCESS:
                            responseEventGenerate([int(not consts.IS_CLIENT), METHODTOINDEX['edit']], responseob[1])
                            sendDataToUICallbacks(responseob[0], responseob[1], None, ifacehandler, data, fromserver, broadcast, proccesedIfaces)
                        return

                    requestob = [[int(consts.IS_CLIENT)], [[{ifacename: {}}, idTypeList]], METHODTOINDEX['view']]
                    builder = ExchangeObBuilder(requestob, False)
                    builder.setFinishCallback(partial(constructed, ifacehandler, False, broadcast, proccesedIfaces))
                    builder.build()
                    continue
            elif ifacedata[ifacename]:
                for c in getDefaultCallbacks(ifacename, ifacehandler, data):
                    addUICallback([[{ifacename: True}, idTypeList]], c, ifacehandler, data)

                data.update(UI_CALLBACKS)
            proccesedIfaces.setdefault(ids, {}).setdefault(types, set([])).update([ifacename])
            callbacks = set(data.get(ids, {}).get(types, {}).get(ifacename, []))
            if callbacks:
                for parentname in iface.parent:
                    PARENT_INTERFACES.setdefault(ids, {}).setdefault(types, set([])).update([ifacename])

            for item in callbacks:
                if item != callback:
                    if broadcast and ifacehandler:
                        debug_utils.LOG_DEBUG('UICallbackUtils:Iface:response', idata, item)
                        convertedIDTypeList = convertIDTypeListForUI(idTypeList)
                        if not convertedIDTypeList:
                            obid = None
                            obtype = None
                        else:
                            obid = convertedIDTypeList[0][0]
                            obtype = convertedIDTypeList[0][1]
                        ifacehandler.addResponseCallbackToQueue(partial(ifacehandler.call_1, item, [[ifacedata, obid, obtype]] if idTypeList is not None and len(idTypeList) < 2 else [[ifacedata, convertedIDTypeList]], 0))
                    if not fromserver and ifacedata[ifacename]:
                        addUICallback(idata, item, ifacehandler, data)
                    elif not ifacedata[ifacename]:
                        removeUICallback(idata, item, ifacehandler, data)

            if broadcast and ifacehandler:
                for parentname in iface.parent:
                    if parentname in proccesedIfaces.get(ids, {}).get(types, set([])):
                        continue
                    piface = getIface(parentname)
                    cacheddata = getFromCache(idTypeList, parentname) or {}
                    parentdata = dict(((attr, ifaces[ifacename].get(attr, cacheddata.get(attr, None))) for attr in piface.attr))
                    if parentdata:
                        iparentdata = [[{parentname: parentdata}, idTypeList]]
                        responseEventGenerate([int(consts.IS_CLIENT), METHODTOINDEX['edit']], iparentdata)
                        sendDataToUICallbacks(headers, iparentdata, None, ifacehandler, data, fromserver, broadcast, proccesedIfaces)

                pnames = list(PARENT_INTERFACES.get(ids, {}).get(types, set([])))
                for pname in pnames:
                    if pname in proccesedIfaces.get(ids, {}).get(types, set([])):
                        continue

                    def constructed(ifacehandler, broadcast, proccesedIfaces, responseob):
                        if responseob[-1] == ErrorCodes.SUCCESS:
                            responseEventGenerate([int(consts.IS_CLIENT), METHODTOINDEX['edit']], responseob[1])
                            sendDataToUICallbacks(responseob[0], responseob[1], None, ifacehandler, data, False, broadcast, proccesedIfaces)
                        return

                    requestob = [[int(consts.IS_CLIENT)], [[{pname: {}}, idTypeList]], METHODTOINDEX['view']]
                    builder = ExchangeObBuilder(requestob, False)
                    builder.setFinishCallback(partial(constructed, ifacehandler, broadcast, proccesedIfaces))
                    builder.build()

    return