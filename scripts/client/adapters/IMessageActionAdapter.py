# Embedded file name: scripts/client/adapters/IMessageActionAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from debug_utils import LOG_DEBUG

class IMessageActionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IMessageActionAdapter, self).__call__(account, ob, **kw)
        LOG_DEBUG('IMessageActionAdapter')
        import IMessageActionHandler
        IMessageActionHandler.handle(ob)
        return ob