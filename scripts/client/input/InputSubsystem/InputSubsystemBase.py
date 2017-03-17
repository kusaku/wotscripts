# Embedded file name: scripts/client/input/InputSubsystem/InputSubsystemBase.py
INPUT_AXIS_TIMER_DT = 0.09
from abc import ABCMeta, abstractmethod

class InputSubsystemBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def dispose(self):
        pass

    @abstractmethod
    def restart(self):
        pass

    def notControlledByUser(self, value):
        pass