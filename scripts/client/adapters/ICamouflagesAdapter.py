# Embedded file name: scripts/client/adapters/ICamouflagesAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
import _camouflages_data

class ICamouflagesAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(ICamouflagesAdapter, self).__call__(account, ob, **kw)
        planeID = kw['idTypeList'][0][0]
        adaptedOB['camouflages'] = list(_camouflages_data.getCamouflages(planeID=planeID))
        return adaptedOB