# Embedded file name: scripts/common/db/DBNavigationWindows.py
__author__ = 's_karchavets'
from consts import NAVIGATION_WINDOWS_TYPES
ALL_NAVIGATION_WINDOWS_TYPES = [NAVIGATION_WINDOWS_TYPES.BIG_MAP, NAVIGATION_WINDOWS_TYPES.MINIMAP, NAVIGATION_WINDOWS_TYPES.RADAR]

class _NavigationWindowContainer:

    def __init__(self):
        self.ENTITY_COMPONENTS = dict()


class _NavigationWindow:

    def __init__(self):
        self.container = _NavigationWindowContainer()

    def readData(self, rootSection, navWindowsType):
        root = rootSection.child(navWindowsType)
        self.container.stateCount = len(root.values())
        for state in range(self.container.stateCount):
            self.container.ENTITY_COMPONENTS[state] = dict()
            states = root.child(state)
            for entity in range(len(states.values())):
                self.container.ENTITY_COMPONENTS[state][entity] = {}
                entitys = states.child(entity)
                for entitySubtype in range(len(entitys.values())):
                    entitySubtypes = entitys.child(entitySubtype)
                    self.container.ENTITY_COMPONENTS[state][entity][entitySubtype] = {}
                    if entitySubtypes.has_key('texture'):
                        self.container.ENTITY_COMPONENTS[state][entity][entitySubtype]['texture'] = entitySubtypes.readString('texture')
                    if entitySubtypes.has_key('lock'):
                        self.container.ENTITY_COMPONENTS[state][entity][entitySubtype]['lock'] = entitySubtypes.readBool('lock')
                    if entitySubtypes.has_key('size'):
                        self.container.ENTITY_COMPONENTS[state][entity][entitySubtype]['size'] = entitySubtypes.readVector2('size')
                    if entitySubtypes.has_key('color'):
                        self.container.ENTITY_COMPONENTS[state][entity][entitySubtype]['color'] = entitySubtypes.readVector4('color')
                    if entitySubtypes.has_key('up_texture'):
                        self.container.ENTITY_COMPONENTS[state][entity][entitySubtype]['up_texture'] = entitySubtypes.readString('up_texture')


class NavigationWindows:

    def __init__(self, data = None):
        self.__container = dict()
        if data is not None:
            self.readData(data)
        return

    def readData(self, rootSection):
        for navWindowsType in ALL_NAVIGATION_WINDOWS_TYPES:
            self.__container[navWindowsType] = _NavigationWindow()
            self.__container[navWindowsType].readData(rootSection, navWindowsType)

    def getNavigationWindowData(self, navWindowsType):
        return self.__container.get(navWindowsType, None)