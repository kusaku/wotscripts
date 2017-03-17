# Embedded file name: scripts/client/adapters/IBonusSchemesAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
import _bonusSchemes_data

class IBonusSchemesAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IBonusSchemesAdapter, self).__call__(account, ob, **kw)
        adaptedOB['bonusSchemes'] = [ {'schemaName': name,
         'bonuses': [ {'type': o.type,
                     'value': int((o.value_ - 1) * 100),
                     'isActiveForAllMapTypes': o.isActiveForAllMapTypes} for o in schema ]} for name, schema in _bonusSchemes_data.BonusSchemesDB.iteritems() ]
        return adaptedOB