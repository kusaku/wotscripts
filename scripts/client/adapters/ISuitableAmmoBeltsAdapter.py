# Embedded file name: scripts/client/adapters/ISuitableAmmoBeltsAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from _weapons import AVAILABLE_BELTS_BY_PLANE_TYPE, COMPONENT_TYPE

class ISuitableAmmoBeltsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(ISuitableAmmoBeltsAdapter, self).__call__(account, ob, **kw)
        planeData, gunData = ob
        availableAmmoTypes = AVAILABLE_BELTS_BY_PLANE_TYPE[planeData.planeType]
        adaptedOB['compatibleBeltIDs'] = []
        from db.DBLogic import g_instance as db
        for beltID in gunData.compatibleBeltIDs:
            if db.getComponentByID(COMPONENT_TYPE.AMMOBELT, beltID).ammo[0] in availableAmmoTypes:
                adaptedOB['compatibleBeltIDs'].append(beltID)

        return adaptedOB