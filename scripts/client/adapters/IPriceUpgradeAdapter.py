# Embedded file name: scripts/client/adapters/IPriceUpgradeAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from exchangeapi.Connectors import getObject
from consts import ALLOW_CREDIT_BUYS
import _economics

class IPriceUpgradeAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(IPriceUpgradeAdapter, self).__call__(account, ob, **kw)
        from db.DBLogic import g_instance as dbInst
        price = list(dbInst.getUpgradePrice(ob))
        if kw['idTypeList'][0][1] in ALLOW_CREDIT_BUYS and price[1] > 0:
            price[0] = price[1] * _economics.Economics.goldRateForCreditBuys
        adaptedOB['price'] = price
        return adaptedOB