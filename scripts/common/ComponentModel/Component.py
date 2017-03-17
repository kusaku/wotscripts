# Embedded file name: scripts/common/ComponentModel/Component.py


class Slot(object):
    """description of an input or output slot"""

    def __init__(self, isInput, name, dataType, func):
        self.isInput = isInput
        self.name = name
        self.dataType = dataType
        self.func = func


class InputSlot(Slot):

    def __init__(self, name, dataType, func):
        Slot.__init__(self, True, name, dataType, func)


class OutputSlot(Slot):

    def __init__(self, name, dataType, func):
        Slot.__init__(self, False, name, dataType, func)


class Component(object):
    """base class for all component"""
    ASPECT_SERVER = 'SERVER'
    ASPECT_CLIENT = 'CLIENT'
    SLOT_BOOL = 1
    SLOT_STR = 2
    SLOT_INT = 3
    SLOT_FLOAT = 4
    SLOT_EVENT = 5
    SLOT_VECTOR2 = 6
    SLOT_VECTOR3 = 7
    SLOT_VECTOR4 = 8
    SLOT_MATRIX = 9
    SLOT_ANGLE = 10

    @classmethod
    def componentName(cls):
        return cls.__name__

    @classmethod
    def componentAspects(cls):
        return [Component.ASPECT_SERVER, Component.ASPECT_CLIENT]

    @classmethod
    def componentIcon(cls):
        return ':vse/components/python'

    @classmethod
    def componentColor(cls):
        return 7189746

    @classmethod
    def componentCategory(cls):
        return 'General'

    def slotDefinitions(self):
        return []

    def captionText(self):
        return ''