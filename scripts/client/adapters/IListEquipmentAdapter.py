# Embedded file name: scripts/client/adapters/IListEquipmentAdapter.py
from DefaultAdapter import DefaultAdapter
from _equipment_data import EquipmentDB

class IListEquipmentAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IListEquipmentAdapter, self).__call__(account, ob, **kw)
        adaptedOB['ids'] = [ x.id for x in EquipmentDB.itervalues() ]
        return adaptedOB