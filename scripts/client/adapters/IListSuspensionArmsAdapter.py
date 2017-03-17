# Embedded file name: scripts/client/adapters/IListSuspensionArmsAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from consts import COMPONENT_TYPE

class IListBombsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IListBombsAdapter, self).__call__(account, ob, **kw)
        import db.DBLogic
        dbInst = db.DBLogic.g_instance
        upgrades = dbInst.upgrades
        idList = [ x.id for x in dbInst.getComponents(COMPONENT_TYPE.BOMBS) if x.name in upgrades ]
        ob['ids'] = idList
        return ob


class IListRocketsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IListRocketsAdapter, self).__call__(account, ob, **kw)
        import db.DBLogic
        dbInst = db.DBLogic.g_instance
        upgrades = dbInst.upgrades
        idList = [ x.id for x in dbInst.getComponents(COMPONENT_TYPE.ROCKETS) if x.name in upgrades ]
        ob['ids'] = idList
        return ob