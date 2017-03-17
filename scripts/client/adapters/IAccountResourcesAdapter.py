# Embedded file name: scripts/client/adapters/IAccountResourcesAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class IAccountResourcesAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IAccountResourcesAdapter, self).__call__(account, ob, **kw)
        account.updateAccountResources(adaptedOB['credits'], adaptedOB['gold'], adaptedOB['exp'], adaptedOB['tickets'], adaptedOB['questChips'])
        return adaptedOB