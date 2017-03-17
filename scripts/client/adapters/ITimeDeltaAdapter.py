# Embedded file name: scripts/client/adapters/ITimeDeltaAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class ITimeDeltaAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        import time
        adaptedOB = super(ITimeDeltaAdapter, self).__call__(account, ob, **kw)
        adaptedOB['delta'] = time.time() - adaptedOB['delta']
        return adaptedOB