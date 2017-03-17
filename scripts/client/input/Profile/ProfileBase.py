# Embedded file name: scripts/client/input/Profile/ProfileBase.py
from abc import ABCMeta, abstractmethod

class IProfileBase(object):
    """
    ProfileBase base interface for profiles of input system
    Profile performs mixing input signals from various devices and
     provides emulation for signal visualization rudders and other aircraft systems
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, notControlledByUser):
        pass

    @abstractmethod
    def getCurrentForce(self):
        return 0.0

    @abstractmethod
    def dispose(self):
        """resources are released before deleting"""
        pass

    @abstractmethod
    def restart(self):
        """before re-use"""
        pass

    @abstractmethod
    def processMouseEvent(self, event):
        pass

    @abstractmethod
    def processJoystickEvent(self, event):
        pass

    @abstractmethod
    def sendAxis(self, axis, value):
        """keyboard  calls to send the axes. """
        pass

    @abstractmethod
    def addCommandListeners(self, processor):
        pass

    @abstractmethod
    def removeCommandListeners(self, processor):
        pass

    @abstractmethod
    def _onSaveControls(self):
        pass

    @abstractmethod
    def notControlledByUser(self, value):
        """It is caused an external manager when the user has no control over the plane """
        pass

    def slipCompensationVisualisation(self):
        pass

    def mute(self, value):
        pass