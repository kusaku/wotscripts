# Embedded file name: scripts/client/adapters/IPlanesAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class IPlanesAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IPlanesAdapter, self).__call__(account, ob, **kw)
        import db.DBLogic
        dbInst = db.DBLogic.g_instance
        ob['planeIDs'] = dbInst.getShopPlaneList()
        return ob