# Embedded file name: scripts/client/adapters/IListConsumablesAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from _consumables_data import ConsumableDB

class IListConsumablesAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IListConsumablesAdapter, self).__call__(account, ob, **kw)
        adaptedOB['ids'] = ConsumableDB.keys()
        return adaptedOB