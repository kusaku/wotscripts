# Embedded file name: scripts/client/gui/HUD3DObject.py
import GUI
import Math
from debug_utils import LOG_ERROR

class Hud3DObjectBase(object):

    def __init__(self):
        self._sfProxy = None
        return

    def __setActive(self, val):
        if self._sfProxy is None:
            LOG_ERROR('Hud3DObjectBase.__setActive() : trying to address an uninitialized proxy')
        else:
            self._sfProxy.active = val
        return

    def __getActive(self):
        return self._sfProxy is not None and self._sfProxy.isActive()

    active = property(__getActive, __setActive)

    def update(self):
        pass

    def activate(self, **kargs):
        pass

    def setUpdatableData(self, **kargs):
        pass


class Hud3DObjectEntity(Hud3DObjectBase):

    def __init__(self, **kargs):
        Hud3DObjectBase.__init__(self)
        self._sfProxy = GUI.SF_EntityPositionStrategy(kargs['movie'])
        self._sfProxy.setModelData('addCallback', kargs['addCallback'])
        self._sfProxy.setModelData('removeCallback', kargs['removeCallback'])
        self._sfProxy.setModelData('updateCallback', kargs['updateCallback'])
        self._sfProxy.setModelData('dimensionsCallback', kargs['dimensionsCallback'])
        self._sfProxy.setModelData('updateTime', kargs['updateTime'])
        self._sfProxy.setModelData('py_callback', kargs['onAddedToScaleform'])

    def activate(self, **kargs):
        Hud3DObjectBase.activate(self, **kargs)
        self._sfProxy.setModelData('id', kargs['param'].entityId)

    def setUpdatableData(self, **kargs):
        Hud3DObjectEntity.update(self)
        self._sfProxy.setModelData('updatableData', kargs['param'])
        addData = self._sfProxy.getModelData('addData')
        if addData is not None:
            if addData.health != kargs['param'].health:
                addData.health = kargs['param'].health
            if hasattr(kargs['param'], 'sideType') and addData.sideType != kargs['param'].sideType:
                addData.sideType = kargs['param'].sideType
        return


class Hud3DObjectMarker(Hud3DObjectEntity):

    def __init__(self, **kargs):
        Hud3DObjectEntity.__init__(self, **kargs)
        self._sfProxy.align = Math.Vector2(0, 0.5)

    def activate(self, **kargs):
        Hud3DObjectEntity.activate(self, **kargs)
        param = kargs['param']
        self._sfProxy.setModelData('addData', param)
        self._sfProxy.setModelData('removeData', param.entityId)
        self._sfProxy.setModelData('updatableData', param)
        self._sfProxy.setModelData('objectName', '_root.mcInfoEntities.entity{0}'.format(param.entityId))


class Hud3DObjectTarget(Hud3DObjectEntity):

    def __init__(self, **kargs):
        Hud3DObjectEntity.__init__(self, **kargs)
        self._sfProxy.setModelData('objectName', '_root.mcInfoEntities.marker')
        self._sfProxy.align = Math.Vector2(0, 0.0)

    def activate(self, **kargs):
        Hud3DObjectEntity.activate(self, **kargs)
        self._sfProxy.setModelData('addData', kargs['param'])
        self._sfProxy.setModelData('objectType', kargs['param'].objectType)


def createTargetObj(**kargs):
    return Hud3DObjectTarget(**kargs)


def createMarkerObj(**kargs):
    return Hud3DObjectMarker(**kargs)


class Hud3DObjectManager:
    __hud3DObjectCreators = {'hud_target': createTargetObj,
     'hud_marker': createMarkerObj}

    def __init__(self):
        self.__cache = {}
        self.__elements = {}

    def __getElement(self, name, id):
        if self.__elements.has_key(name):
            return self.__elements[name].get(id, None)
        else:
            return None

    def clear(self):
        self.__cache = None
        self.__elements = None
        return

    def reserveElements(self, name, numElem, **kargs):
        for i in range(0, numElem):
            self.createElement(name, **kargs)

    def createElement(self, name, **kargs):
        if self.__hud3DObjectCreators.has_key(name):
            creatorFunc = self.__hud3DObjectCreators[name]
            elem = creatorFunc(**kargs)
            if not self.__cache.has_key(name):
                self.__cache[name] = []
            self.__cache[name].append(elem)
            return elem
        else:
            LOG_ERROR('Hud3DObjectManager.CreateElement : unknown element name %s' % name)
            return None
            return None

    def activateElement(self, name, id, **kargs):
        elem = self.__getElement(name, id)
        if elem is None and self.__cache.has_key(name) and len(self.__cache[name]) > 0:
            elem = self.__cache[name].pop()
            if not self.__elements.has_key(name):
                self.__elements[name] = {}
            elem = self.__elements[name][id] = elem
        if elem is None:
            LOG_ERROR('Hud3DObjectManager.activateElement : not enough objects of type %s in cache' % name)
        else:
            getattr(elem, 'activate')(**kargs)
            elem._sfProxy.setModelData('active', True)
        return

    def deactivateElement(self, name, id):
        elem = self.__getElement(name, id)
        if elem is not None:
            elem._sfProxy.setModelData('active', False)
        else:
            LOG_ERROR('Hud3DObjectManager.deactivateElement : cannot find element to deactivate; name %s id %d' % (name, id))
        return

    def removeElement(self, name, id):
        elem = self.__getElement(name, id)
        if elem is not None:
            elem._sfProxy.setModelData('active', False)
            self.__elements[name].pop(id)
            self.__cache[name].append(elem)
        return

    def removeAll(self, name):
        if self.__elements.has_key(name):
            ids = []
            for k in self.__elements[name].iterkeys():
                ids.append(k)

            for k in ids:
                self.removeElement(name, k)

    def updateElement(self, name, id, **kargs):
        elem = self.__getElement(name, id)
        if elem is not None:
            getattr(elem, 'setUpdatableData')(**kargs)
        else:
            LOG_ERROR('Hud3DObjectManager.updateElement : cannot find element to update; name %s id %d' % (name, id))
        return

    def isElementActive(self, name, id):
        elem = self.__getElement(name, id)
        if elem is not None:
            return elem.active
        else:
            return False