# Embedded file name: scripts/client/adapters/IMessageAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from consts import MESSAGE_TYPE
from debug_utils import LOG_TRACE
from exchangeapi.CommonUtils import splitIDTypeList, idFromList
from Helpers.cache import setToCache, getFromCache
from HelperFunctions import generateID
cache = {}

class IMessageAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IMessageAdapter, self).__call__(account, ob, **kw)
        idTypeList = kw['idTypeList']
        idList, typeList = splitIDTypeList(idTypeList)
        ids = idFromList(idList)
        types = idFromList(typeList)
        cache.setdefault(ids, {}).setdefault(types, 1)
        import IMessageHandler
        if ob['msgType'] == MESSAGE_TYPE.MESSAGE_GROUP:
            modifiedob = IMessageHandler.handleMessageGroup(ob)
        else:
            modifiedob = IMessageHandler.handle(ob)
        LOG_TRACE('IMessageAdapter. modifiedob %s' % str(modifiedob))
        return modifiedob


class IMessageUIAdapter(DefaultAdapter):

    def add(self, account, requestID, data, **kw):
        kw['idTypeList'][0][0] = generateID()
        setToCache(kw['idTypeList'], self._iface.ifacename, data)
        return data

    def view(self, account, requestID, idTypeList, ob = None, **kw):
        return getFromCache(idTypeList, self._iface.ifacename)