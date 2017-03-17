# Embedded file name: scripts/client/adapters/IWeaponInfoAdapter.py
import db
from adapters.DefaultAdapter import DefaultAdapter
from consts import UPGRADE_TYPE_TO_COMPONENT_TYPE

class IWeaponInfoAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(IWeaponInfoAdapter, self).__call__(account, ob, **kw)
        if ob is None:
            return adaptedOb
        else:
            dbInstance = db.DBLogic.g_instance
            wInfo = dbInstance.getWeaponInfo(kw['idTypeList'][0][0], kw['idTypeList'][1][0], kw['idTypeList'][2][0])
            if wInfo is None:
                adaptedOb['weaponCount'] = 0
                adaptedOb['weaponType'] = ''
                adaptedOb['weaponId'] = 0
                return adaptedOb
            adaptedOb['weaponCount'] = wInfo[2]
            adaptedOb['weaponType'] = wInfo[0]
            upgrade = dbInstance.getComponentByName(UPGRADE_TYPE_TO_COMPONENT_TYPE[wInfo[0]], wInfo[1])
            if upgrade:
                adaptedOb['weaponId'] = upgrade.id
            else:
                adaptedOb['weaponId'] = 0
            return adaptedOb