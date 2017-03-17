# Embedded file name: scripts/client/StaticModels.py
import BigWorld
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_ERROR
g_staticModelsList = {}

def destroyAll():
    global g_staticModelsList
    LOG_DEBUG('StaticModels: destroyAll', g_staticModelsList)
    for model in g_staticModelsList.values():
        LOG_DEBUG('StaticModels: destroyAll', model)
        try:
            BigWorld.delModel(model)
        except:
            LOG_CURRENT_EXCEPTION()

    g_staticModelsList = {}


def delModel(id):
    if id in g_staticModelsList:
        LOG_DEBUG('StaticModels: delModel', id)
        try:
            BigWorld.delModel(g_staticModelsList.pop(id))
        except:
            LOG_CURRENT_EXCEPTION()


def addModel(id, model):
    LOG_DEBUG('StaticModels: addModel', id, model)
    try:
        BigWorld.addModel(model)
        g_staticModelsList[id] = model
    except TypeError:
        LOG_ERROR('StaticModels: Model cannot be attached elsewhere:', id, model)
    except:
        LOG_CURRENT_EXCEPTION()


def popModel(id):
    if id in g_staticModelsList:
        model = g_staticModelsList.pop(id)
        LOG_DEBUG('StaticModels: popModel', id, model)
        try:
            BigWorld.delModel(model)
        except:
            LOG_CURRENT_EXCEPTION()

        return model


def isInStaticModelsList(id):
    return id in g_staticModelsList