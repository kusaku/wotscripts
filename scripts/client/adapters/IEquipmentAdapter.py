# Embedded file name: scripts/client/adapters/IEquipmentAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizeLobby
from exchangeapi.Connectors import getObject

class IEquipmentAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        if ob is None:
            return ob
        else:
            adaptedOB = super(IEquipmentAdapter, self).__call__(account, getObject(kw['idTypeList']), **kw)
            adaptedOB['buyAvailable'] = ob.buyAvailable
            adaptedOB['minLevel'] = ob.minLevel
            adaptedOB['maxLevel'] = ob.maxLevel
            from db.DBLogic import g_instance as dbInst
            adaptedOB['nations'] = [ dbInst.getNationIDbyName(x) for x in ob.nations ]
            adaptedOB['name'] = localizeLobby(adaptedOB['name'])
            adaptedOB['description'] = localizeLobby(adaptedOB['description'])
            adaptedOB['suitablePlaneIDs'] = dbInst.getAvailablePlanesByEquipmentID(kw['idTypeList'][0][0])
            return adaptedOB