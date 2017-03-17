# Embedded file name: scripts/client/eventhandlers/responsedataCache.py


def updateResponsedataCache(event):
    from Helpers import cache
    if event.ob != event.prevob:
        cache.updateRespDataInCache(event.idTypeList, event.iface.ifacename, event.ob)


def deleteResponsedataCache(event):
    from Helpers import cache
    cache.deleteRespDataFromCache(idTypeList=event.idTypeList, ifaceName=event.iface.ifacename)