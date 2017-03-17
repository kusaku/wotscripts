# Embedded file name: scripts/client/audio/SoundObjectSettings.py


class SoundObjectSettings:

    def __init__(self):
        self.__wwiseGameObject = None
        self.__context = None
        self.__node = None
        self.__factory = None
        self.__soundSet = None
        self.__weaponID = None
        self.__soundModeHandlerCreated = False
        return

    @property
    def soundModeHandlerCreated(self):
        return self.__soundModeHandlerCreated

    @soundModeHandlerCreated.setter
    def soundModeHandlerCreated(self, soundModeHandlerCreated):
        self.__soundModeHandlerCreated = soundModeHandlerCreated

    @property
    def wwiseGameObject(self):
        return self.__wwiseGameObject

    @wwiseGameObject.setter
    def wwiseGameObject(self, wwiseGameObject):
        self.__wwiseGameObject = wwiseGameObject

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, context):
        self.__context = context

    @property
    def node(self):
        return self.__node

    @node.setter
    def node(self, node):
        self.__node = node

    @property
    def factory(self):
        return self.__factory

    @factory.setter
    def factory(self, factory):
        self.__factory = factory

    @property
    def soundSet(self):
        return self.__soundSet

    @soundSet.setter
    def soundSet(self, soundSet):
        self.__soundSet = soundSet

    @property
    def weaponID(self):
        return self.__weaponID

    @weaponID.setter
    def weaponID(self, weaponID):
        self.__weaponID = weaponID