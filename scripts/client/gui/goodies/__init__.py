# Embedded file name: scripts/client/gui/goodies/__init__.py
from gui.goodies.goodies_cache import GoodiesCache
from skeletons.gui.goodies import IGoodiesCache
__all__ = ('getGoodiesCacheConfig',)

def getGoodiesCacheConfig(manager):
    """ Configures services for package goodies.
    :param manager: instance of dependency manager.
    """
    cache = GoodiesCache()
    cache.init()
    manager.addInstance(IGoodiesCache, cache, finalizer='fini')