# Embedded file name: scripts/client/input/ProfileLoader/MouseLoader.py
__author__ = 'm_kobets'
from db.DBHelpers import readValue, writeValue, readValueOnCondition
from consts import MOUSE_INTENSITY_SPLINE_POINT_NUMBER, MOUSE_INTENSITY_SPLINE_POINT_COUNT
from Curve import Curve
from Math import Vector2

class MouseLoader:

    def __init__(self, section):
        readValue(self, section, 'ROLL_AXIS', 0)
        readValue(self, section, 'ALLOW_LEAD', 0)
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
        readValueOnCondition(self, section, 'CAMERA_TYPE', cameraTypeCondition, default=0)
        readValue(self, section, 'MOUSE_SENSITIVITY', 1.0)
        readValue(self, section, 'MOUSE_INVERT_VERT', False)
        readValue(self, section, 'AUTOMATIC_FLAPS', True)
        readValue(self, section, 'RADIUS_OF_CONDUCTING', 1.0)
        readValue(self, section, 'CAMERA_FLEXIBILITY', 1.0)
        readValue(self, section, 'EQUALIZER_ZONE_SIZE', 0.75)
        readValue(self, section, 'ROLL_SPEED_CFC', 1.0)
        readValue(self, section, 'EQUALIZER_FORCE', 1.0)
        readValue(self, section, 'SHIFT_TURN', True)
        readValue(self, section, 'SAFE_ROLL_ON_LOW_ALTITUDE', True)
        readValueOnCondition(self, section, 'MOUSE_INTENSITY_SPLINE', curveCondition, default=Curve([Vector2(0.0, 1.0), Vector2(1.0, 1.0)], MOUSE_INTENSITY_SPLINE_POINT_COUNT))
        readValue(self, section, 'CAMERA_ROLL_SPEED', 0.5)
        readValue(self, section, 'CAMERA_ANGLE', 1.0)
        readValue(self, section, 'CAMERA_ACCELERATION', 0.0)
        readValue(self, section, 'METHOD_OF_MIXING', 2)

    def flash(self, rootSection):
        rootSection.writeFloat('CAMERA_ACCELERATION', self.CAMERA_ACCELERATION)
        rootSection.writeInt('CAMERA_TYPE', self.CAMERA_TYPE)
        rootSection.writeInt('ALLOW_LEAD', self.ALLOW_LEAD)
        rootSection.writeFloat('MOUSE_SENSITIVITY', self.MOUSE_SENSITIVITY)
        rootSection.writeBool('MOUSE_INVERT_VERT', self.MOUSE_INVERT_VERT)
        rootSection.writeBool('AUTOMATIC_FLAPS', self.AUTOMATIC_FLAPS)
        rootSection.writeFloat('RADIUS_OF_CONDUCTING', self.RADIUS_OF_CONDUCTING)
        rootSection.writeFloat('CAMERA_FLEXIBILITY', self.CAMERA_FLEXIBILITY)
        rootSection.writeFloat('EQUALIZER_ZONE_SIZE', self.EQUALIZER_ZONE_SIZE)
        rootSection.writeFloat('ROLL_SPEED_CFC', self.ROLL_SPEED_CFC)
        rootSection.writeFloat('EQUALIZER_FORCE', self.EQUALIZER_FORCE)
        rootSection.writeBool('SHIFT_TURN', self.SHIFT_TURN)
        rootSection.writeBool('SAFE_ROLL_ON_LOW_ALTITUDE', self.SAFE_ROLL_ON_LOW_ALTITUDE)
        writeValue(self, rootSection, 'MOUSE_INTENSITY_SPLINE', Curve)
        rootSection.writeFloat('CAMERA_ROLL_SPEED', self.CAMERA_ROLL_SPEED)
        rootSection.writeFloat('CAMERA_ANGLE', self.CAMERA_ANGLE)
        rootSection.writeInt('METHOD_OF_MIXING', self.METHOD_OF_MIXING)


def curveCondition(curve):
    if curve is not None:
        pointNumber = len(curve.readVector2s('p'))
        pointCount = curve.readInt('pointCount', MOUSE_INTENSITY_SPLINE_POINT_COUNT)
        if pointNumber == MOUSE_INTENSITY_SPLINE_POINT_NUMBER and pointCount == MOUSE_INTENSITY_SPLINE_POINT_COUNT:
            return True
    raise Exception, "MouseLoader: can't correctly read MOUSE_INTENSITY_SPLINE from xml"
    return


def cameraTypeCondition(value):
    if value in (0, 1, 2):
        return True
    raise Exception, "MouseLoader: can't correctly read CAMERA_TYPE from xml"