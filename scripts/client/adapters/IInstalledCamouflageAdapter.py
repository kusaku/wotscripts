# Embedded file name: scripts/client/adapters/IInstalledCamouflageAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from Helpers.cache import getFromCache

class IInstalledCamouflageAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IInstalledCamouflageAdapter, self).__call__(account, ob, **kw)
        return adaptedOB

    def edit(self, account, requestID, idTypeList, data, ob = None, **kw):
        cachedata = getFromCache(idTypeList, self._ifacename)
        if cachedata:
            ids = dict(((int(k), int(v)) for k, v in data['ids'].iteritems()))
            for k, v in cachedata['ids'].iteritems():
                newval = ids.setdefault(k, v)
                if newval != v:
                    ids[k] = newval

            return dict(ids=ids)
        return data