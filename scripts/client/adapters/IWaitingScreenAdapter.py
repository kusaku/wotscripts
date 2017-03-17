# Embedded file name: scripts/client/adapters/IWaitingScreenAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from gui.Scaleform.Waiting import Waiting

class IWaitingScreenAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IWaitingScreenAdapter, self).__call__(account, ob, **kw)
        adaptedOB['isVisible'] = Waiting.isVisible()
        return adaptedOB