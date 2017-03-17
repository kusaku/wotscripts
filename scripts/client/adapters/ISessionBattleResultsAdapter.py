# Embedded file name: scripts/client/adapters/ISessionBattleResultsAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from Helpers.cache import getFromCache, setToCache

class ISessionBattleResultsAdapter(DefaultAdapter):

    def edit(self, account, requestID, idTypeList, data, ob = None, **kw):
        adapteddata = getFromCache(idTypeList, self._iface.ifacename) or dict(ids=[])
        if isinstance(data, long):
            adapteddata['ids'].append(str(data))
            setToCache(idTypeList, self._iface.ifacename, adapteddata)
        return adapteddata