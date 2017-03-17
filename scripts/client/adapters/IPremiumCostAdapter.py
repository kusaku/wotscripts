# Embedded file name: scripts/client/adapters/IPremiumCostAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class IPremiumCostAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        import BWPersonality
        adaptedOb = super(IPremiumCostAdapter, self).__call__(account, ob, **kw)
        adaptedOb['optionList'] = BWPersonality.g_premiumData
        return adaptedOb