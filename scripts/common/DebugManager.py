# Embedded file name: scripts/common/DebugManager.py
__author__ = 'm_kobets'
import BigWorld
import wgPickle
import zlib
import config_consts
from Math import *
from MultiUpdate import MultiUpdate
from consts import IS_CLIENT, IS_CELLAPP, IS_BASEAPP
from Singleton import singleton
from debug_utils import LOG_ERROR
from collections import defaultdict
_GLOBAL_ACTIVITY = config_consts.IS_DEVELOPMENT
FILTER_KEY = 'ArbiterFilterSettings'

class COLORS:
    GREEN = 1996554018
    DARK_GREEN = 2147516501L
    DARK_BLUE = 4278190335L
    WHITE = 4294967295L
    BLUE = 3137404927L
    RED = 4289864226L
    DEFAULT = 3137404927L


class SETTINGS_SPECIFICATION:
    DEGREES = 1
    WORLD_SCALING = 2


class LINE_STILE:
    SOLID = 0
    DASH = 1
    DOT = 2
    DEFAULT = SOLID


class DV_OBJ_TYPES:
    MESSAGE = 'massage'
    TEXT_3D_LOCAL = 'text_3d_local'
    POINT_2D = 'point2d'
    LINE_2D = 'line2d'
    CIRCLE_2D = 'circle2d'
    RECTANGLE_2D = 'rectangle2d'
    LINE_3D = 'line3d'
    LINE_3D_LOCAL = 'line3d_local'
    POINT_3D = 'point3d'
    POINT_3D_LOCAL = 'point3d_local'
    BOX_3D = 'box3d'
    BOX_3D_LOCAL = 'box3d_local'
    CIRCLE_3D_LOCAL = 'circle3d_local'


def DEFAULT_GROUP_NAME():
    if IS_CLIENT:
        return 'CLIENT'
    if IS_CELLAPP:
        return 'CELL'
    if IS_BASEAPP:
        return 'BASE'
    raise


class StorageData(object):
    __slots__ = ['is_change', '_data']

    def __init__(self, change_state = False, data = None):
        self.is_change = change_state
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if value != self._data:
            self.is_change = True
            self._data = value


class KeyDescription(object):

    def __init__(self, name, type = DV_OBJ_TYPES.MESSAGE, group = DEFAULT_GROUP_NAME(), **kwargs):
        self.name = name
        self.type = type
        self.group = group
        for key, data in kwargs.iteritems():
            setattr(self, key, data)


@singleton

class __DebugManager(MultiUpdate):

    def __init__(self):
        self.__newViewers = set()
        self.__storage = defaultdict(StorageData)
        self.__addSettingsStorage = {}
        self.__dvKeyArray = {}
        self.__filter = {}
        if IS_CLIENT:
            self.setFilter(-1, wgPickle.dumps(wgPickle.FromClientToServer, {}))
        else:
            globalData = BigWorld.globalData
            arbiterAllListener = globalData.get('ArbiterAllListener', [])
            for viewerId in arbiterAllListener:
                key = FILTER_KEY + str(viewerId)
                try:
                    self.setFilter(viewerId, globalData.get(key, None))
                except KeyError:
                    pass

        self.__lazyInitialization = False
        MultiUpdate.__init__(self, (0.1, self.__updateData))
        return

    def __del__(self):
        MultiUpdate.dispose(self)
        if not IS_CLIENT:
            arbiter = BigWorld.globalData.get('Arbiter', False)
            if arbiter:
                for dvKey in self.__dvKeyArray.iterkeys():
                    arbiter.removeKey(dvKey)

    def createKey(self, keyDescription):
        if isinstance(keyDescription, KeyDescription):
            dvKey = zlib.crc32(str(keyDescription.__dict__))
            if dvKey not in self.__dvKeyArray.keys():
                self.__dvKeyArray[dvKey] = keyDescription
                self.__pushToClientNewKey(dvKey, keyDescription)
            return dvKey
        raise

    def addSettingToView(self, keyDescription, data):
        dvKey = zlib.crc32(str(keyDescription.__dict__))
        if not self.__addSettingsStorage.has_key(dvKey):
            self.__addSettingsStorage[dvKey] = data
        send_data = self.__addSettingsStorage[dvKey]
        keyDescription.data = send_data
        self.__pushToClientNewKey(dvKey, keyDescription)
        return send_data

    def __pushToClientNewKey(self, dvKey, keyDescription):
        if IS_CLIENT:
            BigWorld.player().debugViewer_addNewKey(dvKey, wgPickle.dumps(wgPickle.FromServerToServer, keyDescription))
        else:
            arbiter = BigWorld.globalData.get('Arbiter', False)
            if arbiter:
                arbiter.addNewKey(dvKey, wgPickle.dumps(wgPickle.FromServerToServer, keyDescription))
            else:
                self.__lazyInitialization = True

    def __setSettingToViewData(self, mask):
        for obj in mask:
            if isinstance(obj, dict):
                for key, data in obj.iteritems():
                    if self.__addSettingsStorage.has_key(key):
                        for k, v in data.iteritems():
                            self.__addSettingsStorage[key][k] = v

                mask.remove(obj)

    def removeKey(self, dvKey):
        del self.__dvKeyArray[dvKey]
        if IS_CLIENT:
            BigWorld.player().debugViewer_removeKey(dvKey)
        else:
            arbiter = BigWorld.globalData.get('Arbiter', False)
            if arbiter:
                arbiter.removeKey(dvKey)

    def removeDataByGroup(self, group):
        temp_dvKey_list = []
        temp_disc = self.__dvKeyArray.copy()
        for key, value in temp_disc.iteritems():
            if value.group == group:
                self.removeKey(key)
                temp_dvKey_list.append(key)

        temp_filter = self.__filter.copy()
        for viewerId, mask in temp_filter.iteritems():
            for dvKey in temp_dvKey_list:
                if dvKey in mask:
                    self.__filter[viewerId].remove(dvKey)

        temp_storage = self.__storage.copy()
        for dvKey in temp_storage.iterkeys():
            if dvKey in temp_dvKey_list:
                del self.__storage[dvKey]

    def setFilter(self, viewerId, data):
        try:
            mask = wgPickle.loads(wgPickle.FromClientToServer, data)
        except Exception as e:
            LOG_ERROR('DebugManager::setFilter. Cant load: ', data)
            return

        self.__setSettingToViewData(mask)
        self.__filter[viewerId] = mask
        if len(mask):
            self.__newViewers.add(viewerId)

    def pushToView(self, dvKey, *args):
        self.__storage[dvKey].data = wgPickle.dumps(wgPickle.FromServerToClient, *args)

    def __updateData(self):
        if self.__lazyInitialization:
            arbiter = BigWorld.globalData.get('Arbiter', False)
            if arbiter:
                self.__lazyInitialization = False
                for dvKey, keyDescription in self.__dvKeyArray.iteritems():
                    arbiter.addNewKey(dvKey, wgPickle.dumps(wgPickle.FromServerToServer, keyDescription))

            else:
                return
        else:
            _buffer = {}
            for dvKey, dataObj in self.__storage.iteritems():
                for viewerId, mask in self.__filter.iteritems():
                    is_new_viewer = viewerId in self.__newViewers
                    in_mask = dvKey in mask
                    is_change = self.__storage[dvKey].is_change
                    if in_mask and (is_change or is_new_viewer):
                        _buffer.setdefault(viewerId, {})[dvKey] = dataObj.data

                self.__storage[dvKey].is_change = False

            _puck_buffer = dict(((ID, wgPickle.dumps(wgPickle.FromServerToClient, single_buffer)) for ID, single_buffer in _buffer.iteritems()))
            if len(_puck_buffer):
                if IS_CLIENT:
                    fromClient = _puck_buffer.get(-1, None)
                    if fromClient:
                        fromClient = wgPickle.loads(wgPickle.FromServerToClient, fromClient)
                        BigWorld.player().debugViewer_pushToView(wgPickle.dumps(wgPickle.FromServerToServer, fromClient))
                else:
                    BigWorld.globalData['Arbiter'].pushToView(wgPickle.dumps(wgPickle.FromServerToServer, _puck_buffer))
            self.__newViewers.clear()
        return


def debug_observer(observe_attr_list = None):
    __AVAILABLE_TYPES = (int,
     float,
     tuple,
     list,
     dict,
     Vector2,
     Vector3,
     Vector4,
     str)

    def wrapper(cls):
        if _GLOBAL_ACTIVITY:
            class_name = cls.__name__

            class Cache_:

                def __init__(self):
                    self.group_name = DEFAULT_GROUP_NAME()
                    self.dvKey_dict = {}
                    self.kwargs = {}

            def _observer(self, name, value):
                if isinstance(value, __AVAILABLE_TYPES):
                    cls_name = '_' + class_name
                    if cls_name in name:
                        name = name[len(cls_name):]
                    if observe_attr_list is None or name in observe_attr_list:
                        cache = self.debug_viewer_observer_cache
                        keyDescription = KeyDescription(name, group=cache.group_name, **cache.kwargs)
                        dvKey = cache.dvKey_dict.setdefault(name, CREATE_KEY(keyDescription))
                        SHOW_OBJ(dvKey, value)
                return

            class wrapper_class(cls):

                def __init__(self, *args, **kwargs):
                    self.debug_viewer_observer_cache = Cache_()
                    self.debug_viewer_observer_cache.kwargs = kwargs.copy()
                    self.debug_viewer_observer_cache.group_name = GET_UNIQUE_GROUP(self)
                    cls.__init__(self, *args, **kwargs)

                def __setattr__(self, key, value):
                    cls.__setattr__(self, key, value)
                    _observer(self, key, value)

            wrapper_class.__name__ = class_name
            return wrapper_class
        else:
            return cls

    return wrapper


def SET_MASK_FROM_VIEWER(viewerId, mask):
    """
        pass
    """
    if _GLOBAL_ACTIVITY:
        __DebugManager().setFilter(viewerId, mask)


def SHOW_OBJ(dvKey, *args):
    """
    pass
    """
    if _GLOBAL_ACTIVITY:
        __DebugManager().pushToView(dvKey, *args)
    else:
        LOG_ERROR('Attempt to use Debug System not in development mode.')


def SHOW_DEBUG_OBJ(name, data, **kwargs):
    keyDescription = KeyDescription(name, **kwargs)
    dvKey = __DebugManager().createKey(keyDescription)
    if _GLOBAL_ACTIVITY:
        __DebugManager().pushToView(dvKey, data)
    else:
        LOG_ERROR('Attempt to use Debug System not in development mode.')


def GET_UNIQUE_GROUP(inst, local_group = ''):
    class_name = inst.__class__.__name__
    ID = id(inst)
    if len(local_group):
        add_group_name = local_group
    else:
        add_group_name = 'observer'
    return class_name + ' (id: ' + str(ID) + ') -> ' + add_group_name


def REMOVE_VIEW_GROUP(group):
    if _GLOBAL_ACTIVITY:
        __DebugManager().removeDataByGroup(group)
    else:
        LOG_ERROR('Attempt to use Debug System not in development mode.')


def CREATE_KEY(keyDescription):
    """
    create dvKey
    """
    if _GLOBAL_ACTIVITY:
        return __DebugManager().createKey(keyDescription)
    LOG_ERROR('Attempt to use Debug System not in development mode.')


def ADD_DEBUG_SETTINGS(name, dict_data, specification = {}):
    """
    :param name: settings name
    :param dict_data:
    :param specification:
    :return:
    """
    if _GLOBAL_ACTIVITY:
        if isinstance(dict_data, dict):
            keyDescription = KeyDescription(name, type='setting', data=dict_data, spec=specification)
            return __DebugManager().addSettingToView(keyDescription, dict_data.copy())
        raise AttributeError, 'ADD_DEBUG_SETTINGS: need dict data'
    else:
        LOG_ERROR('ADD_DEBUG_SETTINGS : attempt to use Debug System not in development mode.')