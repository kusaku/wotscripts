# Embedded file name: scripts/client/adapters/IAvailableEquipmentAdapter.py
from DefaultAdapter import DefaultAdapter

class IAvailableEquipmentAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IAvailableEquipmentAdapter, self).__call__(account, ob, **kw)
        from db.DBLogic import g_instance as DB
        obid = kw['idTypeList'][0][0]
        ob['equipmentIDs'] = DB.getAvailableEquipmentByPlaneID(obid)
        return ob