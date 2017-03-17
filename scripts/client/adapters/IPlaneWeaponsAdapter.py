# Embedded file name: scripts/client/adapters/IPlaneWeaponsAdapter.py
import db
from adapters.DefaultAdapter import DefaultAdapter
from _airplanesConfigurations_db import getAirplaneConfiguration

class IPlaneWeaponsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(IPlaneWeaponsAdapter, self).__call__(account, ob, **kw)
        if ob is None:
            return adaptedOb
        else:
            slots = [ (x[0], x[1]) for x in db.DBLogic.g_instance.getAllWeapons(kw['idTypeList'][0][0]) ]
            adaptedOb['weaponSlots'] = {}
            for slot in slots:
                adaptedOb['weaponSlots'].setdefault(slot[0], []).append(slot[1])

            return adaptedOb


class IPlaneWeaponsForConfigAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(IPlaneWeaponsForConfigAdapter, self).__call__(account, ob, **kw)
        if ob is None:
            return adaptedOb
        else:
            planeConfig = getAirplaneConfiguration(kw['idTypeList'][0][0])
            if not planeConfig:
                return adaptedOb
            adaptedOb['weaponSlots'] = dict(((x[0], [x[1]]) for x in planeConfig.weaponSlots))
            return adaptedOb