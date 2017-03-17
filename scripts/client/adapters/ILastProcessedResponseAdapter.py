# Embedded file name: scripts/client/adapters/ILastProcessedResponseAdapter.py
from DefaultAdapter import DefaultAdapter
from consts import EMPTY_IDTYPELIST
from Helpers.cache import getFromCache

class ILastProcessedResponseAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        return super(ILastProcessedResponseAdapter, self).__call__(account, (getFromCache(EMPTY_IDTYPELIST, self._iface.ifacename) or self.add(None, None, {'rid': 0})), **kw)

    def add(self, account, requestID, data, **kw):
        return self.edit(account, requestID, EMPTY_IDTYPELIST, data, **kw)

    def edit(self, account, requestID, idTypeList, data, ob = None, **kw):
        from Helpers.cache import setToCache
        setToCache(idTypeList, self._iface.ifacename, data)
        return data