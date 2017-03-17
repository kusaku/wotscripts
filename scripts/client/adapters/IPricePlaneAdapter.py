# Embedded file name: scripts/client/adapters/IPricePlaneAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from exchangeapi.Connectors import getObject

class IPricePlaneAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(IPricePlaneAdapter, self).__call__(account, ob, **kw)
        adaptedOB['price'] = [getattr(ob.options, 'price', 0), getattr(ob.options, 'gold', 0)] if ob is not None else None
        return adaptedOB