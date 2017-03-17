# Embedded file name: scripts/client/gui/Scaleform/GameOptions/GameOptionsManager.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.vo.RootSettingsVO import RootSettingsVO
from gui.Scaleform.GameOptions.loaders.RootSettingsLoader import RootSettingsLoader
from gui.Scaleform.GameOptions.preservers.RootSettingsPreserver import RootSettingsPreserver
from gui.Scaleform.GameOptions.utils import BasePreserver, parseBracket, getListsIndexes
from debug_utils import LOG_DEBUG, LOG_ERROR
from copy import deepcopy
LAZY_ENABLED = True

class GameOptionsManager:
    PRIMITIVE_TYPES = [int,
     float,
     bool,
     str,
     long,
     unicode]

    def __init__(self, isNeedSaveSrc):
        self.__isNeedSaveSrc = isNeedSaveSrc
        self.root = RootSettingsVO()
        self.__rootSettingsLoader = RootSettingsLoader('root')
        self.__rootSettingsPreserver = RootSettingsPreserver()

    def delete(self, path, obj):
        """
        @param path: <str>
        @param obj: <list>
        """
        rootObj = self.load(path, False)
        if rootObj is not None:
            if isinstance(rootObj, list):
                if not len(obj):
                    rootObj = list()
                else:
                    for key in obj:
                        del rootObj[key]

            elif isinstance(rootObj, dict):
                if not len(obj):
                    rootObj.clear()
                else:
                    for key in obj:
                        del rootObj[key]

            elif hasattr(rootObj, '__dict__'):
                for key in obj:
                    delattr(rootObj, key)

            else:
                LOG_ERROR('delete - unknown rootObj', path)
        return

    def loadSrc(self, p):
        pList = p.split('.')
        if not pList:
            LOG_ERROR('loadSrc - empty path')
            return
        else:
            self.__rootSettingsLoader.load(self.root, pList[:], None, True)
            return

    def load(self, p, isConsiderLazzy = True):
        """
        load data
        @param p: <str>
        @return: <object>
        """
        pList = p.split('.')
        if not pList:
            LOG_ERROR('load - empty path')
            return
        if isConsiderLazzy:
            if self.__isNeedSaveSrc and pList[0] == 'settings':
                pListSrc = pList[:]
                pListSrc[0] = 'settingsSource'
                self.__rootSettingsLoader.load(self.root, pListSrc)
            self.__rootSettingsLoader.load(self.root, pList[:])
        if len(pList) == 1:
            o = self.__getBracketObject(self.root, pList[0])
        else:
            o = self.root
            for attr in pList:
                o = self.__getBracketObject(o, attr)

        if isConsiderLazzy and LAZY_ENABLED and o is not None:
            copyObject = deepcopy(o)
            self.__applyLazy(copyObject)
            return copyObject
        else:
            return o

    def save(self, p, v):
        """
        save data
        @param p: <str>
        @param v: <object>
        """
        self.__set(self.root, p, v)
        self.__dispatchEvent(p, v)
        print '----DISPATCH EVENT---'

    def destroy(self):
        self.__rootSettingsLoader.destroy()
        self.__rootSettingsPreserver.destroy()

    def __dispatchEvent(self, p, v):
        pList = p.split('.')
        l = self.__rootSettingsPreserver.listeners
        for i, path in enumerate(pList):
            listAttrName, listIndex = parseBracket(path)
            if listAttrName is not None:
                if listAttrName not in l:
                    LOG_DEBUG('__dispatchEvent array without listeners', p)
                    return
                l = l[listAttrName]
                if isinstance(l, BasePreserver):
                    l.save(self.load('.'.join(pList[:i]) + '.' + str(listAttrName), False))
                else:
                    LOG_DEBUG('__dispatchEvent array without listeners', p)
                return
            if isinstance(l, BasePreserver):
                l.save(self.load('.'.join(pList[:i]), False))
                return
            if path not in l:
                LOG_DEBUG('__dispatchEvent without listeners', p)
                return
            l = l[path]

        if type(v) in GameOptionsManager.PRIMITIVE_TYPES:
            if isinstance(l, BasePreserver):
                l.save(v)
            else:
                LOG_DEBUG('__dispatchEvent primitive without listeners', p)
            return
        else:
            container = dict()
            self.__fillPathsInDict(v, container)
            self.__parsePathInDict(container, l, self.load(p, False))
            return

    def __fillPathsInDict(self, obj, container):
        """
        @param obj: object
        @param container: <dict>
        """
        if hasattr(obj, '__dict__'):
            keys = obj.__dict__.keys()
            for attribute in keys:
                container[attribute] = dict()
                if isinstance(obj.__dict__[attribute], list):
                    for listObj in obj.__dict__[attribute]:
                        self.__fillPathsInDict(listObj, container[attribute])

                elif isinstance(obj.__dict__[attribute], dict):
                    for dictObj in obj.__dict__[attribute].itervalues():
                        self.__fillPathsInDict(dictObj, container[attribute])

                elif hasattr(obj, '__dict__'):
                    self.__fillPathsInDict(obj.__dict__[attribute], container[attribute])

    def __parsePathInDict(self, pathDict, listeners, data):
        """
        @param pathDict: <dict> with pathes
        @param listeners: <dict> with BasePreservers classes
        @param data: <BasePreserver>
        """
        if isinstance(listeners, BasePreserver):
            listeners.save(data)
            return
        for key, value in pathDict.iteritems():
            if key in listeners:
                listener = listeners[key]
                if isinstance(listener, BasePreserver):
                    listener.save(getattr(data, key))
                elif isinstance(listener, dict):
                    self.__parsePathInDict(pathDict[key], listener, getattr(data, key))

    def __set(self, root, p, v):
        if type(v) in GameOptionsManager.PRIMITIVE_TYPES:
            self.__setValue(p, root, v)
        elif isinstance(v, list):
            allPrimitives = True
            for val in v:
                if type(val) not in GameOptionsManager.PRIMITIVE_TYPES:
                    allPrimitives = False
                    break

            if allPrimitives:
                self.__setValue(p, root, v)
            else:
                for i, val in enumerate(v):
                    self.__set(root, ''.join([p,
                     '[',
                     str(i),
                     ']']), val)

        elif isinstance(v, dict):
            allPrimitives = True
            for val in v.itervalues():
                if type(val) not in GameOptionsManager.PRIMITIVE_TYPES:
                    allPrimitives = False
                    break

            if allPrimitives:
                self.__setValue(p, root, v)
            else:
                for k, val in v.iteritems():
                    self.__set(root, ''.join([p,
                     '.',
                     '[',
                     str(k),
                     ']']), val)

        elif hasattr(v, '__dict__'):
            for k, val in v.__dict__.iteritems():
                self.__set(root, ''.join([p, '.', k]), val)

        else:
            LOG_DEBUG('__set - unknown v', p, v)

    def __setValue(self, path, obj, value):
        pathList = path.split('.')
        if len(pathList) == 1:
            suffixPath = pathList[0]
            listAttrName, listIndex = parseBracket(suffixPath)
            if listAttrName is not None:
                childObj = getattr(obj, listAttrName, None)
                if childObj is not None:
                    if isinstance(childObj, list):
                        attr, listIndexes = getListsIndexes(path)
                        if len(listIndexes) > 1:
                            for i, ii in enumerate(listIndexes):
                                if ii < len(childObj):
                                    if i == len(listIndexes) - 1:
                                        childObj[ii] = value
                                    else:
                                        childObj = childObj[ii]
                                else:
                                    LOG_ERROR('__setValue - ii not found in childObj<list>', path, value, i, ii)

                            return
                        listIndex = int(listIndex)
                        if listIndex >= len(childObj):
                            childObj.append(value)
                        elif isinstance(value, list):
                            for i, v in enumerate(value):
                                if v is not None:
                                    childObj[listIndex][i] = v

                        else:
                            childObj[listIndex] = value
                    elif isinstance(childObj, dict):
                        childObj[listIndex] = value
                    else:
                        LOG_ERROR('__setValue - unknown childObj', path, obj, value)
            else:
                setattr(obj, suffixPath, value)
        else:
            suffixPath = pathList[len(pathList) - 1]
            prefixPath = '.'.join(pathList[:len(pathList) - 1])
            parentObj = eval(''.join(['obj', '.', prefixPath]))
            self.__setValue(suffixPath, parentObj, value)
        return

    def __getBracketObject(self, o, attr):
        listAttrName, listIndex = parseBracket(attr)
        if listAttrName is not None:
            o = getattr(o, listAttrName)
            if isinstance(o, list):
                listIndex = int(listIndex)
            o = o[listIndex]
        else:
            o = getattr(o, attr)
        return o

    def __applyLazy(self, obj):
        if hasattr(obj, '__dict__'):
            keys = obj.__dict__.keys()
            for attribute in keys:
                if isinstance(obj.__dict__[attribute], list):
                    for listObj in obj.__dict__[attribute]:
                        self.__applyLazy(listObj)

                elif isinstance(obj.__dict__[attribute], dict):
                    for dictObj in obj.__dict__[attribute].itervalues():
                        self.__applyLazy(dictObj)

                elif hasattr(obj, '__dict__'):
                    isLazy = obj.__dict__[attribute].isLazy if hasattr(obj.__dict__[attribute], 'isLazy') else False
                    if isLazy:
                        delattr(obj, attribute)
                    else:
                        self.__applyLazy(obj.__dict__[attribute])

    @property
    def preservers(self):
        return self.__rootSettingsPreserver