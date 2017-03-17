# Embedded file name: scripts/client/adapters/IResponseAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.cache import getFromCache, setToCache, deleteFromCache
from Helpers.reliableDelivery import popMappedCallback
from debug_utils import LOG_TRACE

class IResponseAdapter(DefaultAdapter):

    def add(self, account, requestID, data, **kw):
        from exchangeapi.EventUtils import generateEvent
        setToCache(kw['idTypeList'], self._iface.ifacename, data)
        generateEvent('add', 'add', self._iface.ifacename, kw['idTypeList'], account, data)
        return data

    def delete(self, account, requestID, idTypeList, **kw):
        from exchangeapi.EventUtils import generateEvent
        ob = getFromCache(idTypeList, self._iface.ifacename)
        if ob:
            LOG_TRACE('Executing callback for package id: {0}'.format(idTypeList[0][0]))
            import BigWorld
            from Account import PlayerAccount
            player = BigWorld.player()
            if player and player.__class__ == PlayerAccount:
                popMappedCallback(idTypeList[0][0], player.processIfaceData)(None, None, ob['data'])
                deleteFromCache(idTypeList, self._iface.ifacename)
                generateEvent('delete', 'delete', self._iface.ifacename, idTypeList, account, {}, ob)
        return {}