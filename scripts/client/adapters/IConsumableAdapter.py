# Embedded file name: scripts/client/adapters/IConsumableAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizeLobby
from exchangeapi.Connectors import getObject

class IConsumableAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        if ob is None:
            return ob
        else:

            def localizeIfNotEmpty(tag):
                ret = localizeLobby(tag)
                if ret == tag:
                    return ''
                return ret

            adaptedOB = super(IConsumableAdapter, self).__call__(account, getObject(kw['idTypeList']), **kw)
            adaptedOB['buyAvailable'] = ob.buyAvailable
            adaptedOB['name'] = localizeLobby(adaptedOB['name'])
            adaptedOB['description'] = localizeLobby(adaptedOB['description'])
            adaptedOB['fullDescription'] = localizeLobby(adaptedOB['fullDescription'])
            adaptedOB['effectContinuous'] = localizeIfNotEmpty(adaptedOB['effectContinuous'])
            adaptedOB['effectOnUse'] = localizeIfNotEmpty(adaptedOB['effectOnUse'])
            from db.DBLogic import g_instance as dbInst
            adaptedOB['minLevel'] = ob.minLevel
            adaptedOB['maxLevel'] = ob.maxLevel
            adaptedOB['nations'] = [ dbInst.getNationIDbyName(x) for x in ob.nations ]
            adaptedOB['planeTypes'] = ob.planeType
            adaptedOB['coolDownTime'] = ob.coolDownTime
            adaptedOB['effectTime'] = ob.effectTime
            adaptedOB['chargesCount'] = ob.chargesCount
            adaptedOB['suitablePlaneIDs'] = dbInst.getAvailablePlanesByConsumableID(kw['idTypeList'][0][0])
            adaptedOB['behaviour'] = ob.behaviour
            return adaptedOB

    def view(self, account, requestID, idTypeList, ob = None, **kw):
        return DefaultAdapter.view(self, account, requestID, idTypeList, ob=ob, **kw)