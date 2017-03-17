# Embedded file name: scripts/client/adapters/IMessageSessionAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from Helpers import cache

class IMessageSessionAdapter(DefaultAdapter):

    def view(self, account, requestID, idTypeList, ob = None, **kw):
        return self.getCacheData(idTypeList, account)

    def edit(self, account, requestID, idTypeList, data, ob = None, **kw):
        ob = self.getCacheData(idTypeList, account)
        newIDs = data.get('messageIDs', [])
        if not ob.get('messageIDs', []):
            ob['messageIDs'] = []
        for ID in newIDs:
            if ID not in ob['messageIDs']:
                ob['messageIDs'].append(ID)

        newMessages = data.get('storedMessages', [])
        if not ob.get('storedMessages', []):
            ob['storedMessages'] = []
        for item in newMessages:
            if item not in ob['storedMessages']:
                ob['storedMessages'].append(item)

        return ob

    def getCacheData(self, idTypeList, account):
        return cache.getFromCache(idTypeList, self._ifacename) or self.__call__(account, {})