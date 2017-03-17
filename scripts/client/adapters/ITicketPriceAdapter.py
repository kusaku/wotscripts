# Embedded file name: scripts/client/adapters/ITicketPriceAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class ITicketPriceUpgradeAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(ITicketPriceUpgradeAdapter, self).__call__(account, ob, **kw)
        adaptedOb['ticketPrice'] = ob.tickets
        return adaptedOb