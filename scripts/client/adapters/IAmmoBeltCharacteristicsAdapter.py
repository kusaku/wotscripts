# Embedded file name: scripts/client/adapters/IAmmoBeltCharacteristicsAdapter.py
from Helpers.i18n import localizeLobbyUnformatted
from adapters.DefaultAdapter import DefaultAdapter
import db.DBLogic
from consts import AMMOBELT_SPECS

class IAmmoBeltCharacteristicsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        dbInst = db.DBLogic.g_instance
        if isinstance(ob, list):
            beltData, gunData = ob
            isDefault = gunData.defaultBelt == beltData.id
        else:
            guns = dbInst.getBeltSuitableGuns(ob.id)
            gunData = guns[0]
            isDefault = False
            beltData = ob
        adaptedOB = super(IAmmoBeltCharacteristicsAdapter, self).__call__(account, beltData, **kw)
        if beltData is None or gunData is None:
            return adaptedOB
        else:
            minDamage, maxDamage = dbInst.calculateBeltMinMaxDamage(gunData, beltData)
            adaptedOB['minDamage'] = minDamage
            adaptedOB['maxDamage'] = maxDamage
            adaptedOB['isDefault'] = isDefault
            adaptedOB['specsList'] = []
            for spec in AMMOBELT_SPECS.SPEC_LIST:
                value, flag = dbInst.calculateBeltSpec(gunData, beltData, spec)
                adaptedOB['specsList'].append([localizeLobbyUnformatted(spec.locTag), round(value), round(flag)])

            return adaptedOB