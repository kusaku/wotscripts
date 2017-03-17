# Embedded file name: scripts/client/adapters/IAvailableConsumablesAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class IAvailableConsumablesAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedob = super(IAvailableConsumablesAdapter, self).__call__(account, ob, **kw)
        from db.DBLogic import g_instance as DB
        obid = kw['idTypeList'][0][0]
        adaptedob['consumableIDs'] = DB.getAvailableConsumablesByPlaneID(obid)
        return adaptedob