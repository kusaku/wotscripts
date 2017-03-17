# Embedded file name: scripts/client/adapters/IListUpgradesAdapter.py
from DefaultAdapter import DefaultAdapter

class IListUpgradesAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IListUpgradesAdapter, self).__call__(account, ob, **kw)
        import db.DBLogic
        adaptedOB['ids'] = [ x.id for x in db.DBLogic.g_instance.upgrades.itervalues() ]
        return adaptedOB