# Embedded file name: scripts/client/input/ProfileLoader/DummyDeviceLoader.py
from db.DBHelpers import readValue

class MouseDummy:

    def __init__(self, section):
        self.__readMappingData(section)
        readValue(self, section, 'SLIP_COMPENSATION', True)
        readValue(self, section, 'INVERT_VERT', False)
        readValue(self, section, 'INERTIA_CAMERA', 1.0)

    def flash(self, rootSection):
        rootSection.writeBool('SLIP_COMPENSATION', self.SLIP_COMPENSATION)
        rootSection.writeBool('INVERT_VERT', self.INVERT_VERT)
        rootSection.writeFloat('INERTIA_CAMERA', self.INERTIA_CAMERA)

    def __readMappingData(self, section):
        readValue(self, section, 'ROLL_AXIS', 0)
        readValue(self, section, 'INVERT_ROLL', 0)
        readValue(self, section, 'ROLL_SENSITIVITY', 0.0)
        readValue(self, section, 'ROLL_DEAD_ZONE', 0.05)
        readValue(self, section, 'VERTICAL_AXIS', 2)
        readValue(self, section, 'INVERT_VERTICAL', 0)
        readValue(self, section, 'VERTICAL_SENSITIVITY', 0.0)
        readValue(self, section, 'VERTICAL_DEAD_ZONE', 0.05)
        readValue(self, section, 'FORCE_AXIS', 1)
        readValue(self, section, 'INVERT_FORCE', 0)
        readValue(self, section, 'FORCE_SENSITIVITY', 0.0)
        readValue(self, section, 'FORCE_DEAD_ZONE', 0.05)
        readValue(self, section, 'HORIZONTAL_AXIS', 3)
        readValue(self, section, 'INVERT_HORIZONTAL', 0)
        readValue(self, section, 'HORIZONTAL_SENSITIVITY', 0.0)
        readValue(self, section, 'HORIZONTAL_DEAD_ZONE', 0.05)