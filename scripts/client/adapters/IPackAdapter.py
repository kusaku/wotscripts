# Embedded file name: scripts/client/adapters/IPackAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from packsCommon import giftGenerator

class IPackAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        """ Add in adaptedOB['packItemsList'] list [[giftID, giftType, giftCount], ...].
            See WPCOR-41468.a
        """
        if ob is None:
            return {}
        else:
            return super(IPackAdapter, self).__call__(account, {'packItemsList': list(giftGenerator(ob['items']))}, **kw)