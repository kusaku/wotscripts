# Embedded file name: scripts/client/adapters/IBattleResultAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from Helpers.cache import setToCache

class IBattleResultAdapter(DefaultAdapter):

    def add(self, account, requestID, data, **kw):
        setToCache([[kw['reportID'], 'battleResult']], self._iface.ifacename, data)
        return data


class IBattleResultShortAdapter(DefaultAdapter):

    def add(self, account, requestID, data, **kw):
        setToCache([[kw['reportID'], 'battleResult']], self._iface.ifacename, super(IBattleResultShortAdapter, self).__call__(account, data['myData'], **kw))
        return data