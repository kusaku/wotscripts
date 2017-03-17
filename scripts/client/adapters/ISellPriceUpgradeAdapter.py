# Embedded file name: scripts/client/adapters/ISellPriceUpgradeAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from exchangeapi.Connectors import getObject

class ISellPriceUpgradeAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(ISellPriceUpgradeAdapter, self).__call__(account, ob, **kw)
        from db.DBLogic import g_instance
        adaptedOB['credits'] = g_instance.getUpgradeSellPrice(ob)
        return adaptedOB