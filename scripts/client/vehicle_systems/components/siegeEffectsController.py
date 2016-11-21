# Embedded file name: scripts/client/vehicle_systems/components/siegeEffectsController.py
import svarog_script.py_component
import Math
from constants import VEHICLE_SIEGE_STATE

class SiegeEffectsController(svarog_script.py_component.Component):
    SIEGE_TIMEOUT = 2.0
    SIEGE_IMPULSE = 0.25

    def __init__(self, appearance):
        self.__appearance = appearance
        self.__effectManager = appearance.customEffectManager
        self.__siegeTimeOut = 0.0
        self.__siegeInProgress = 0
        self.__state = VEHICLE_SIEGE_STATE.DISABLED

    def __del__(self):
        self.__effectManager = None
        self.__appearance = None
        return

    def onSiegeStateChanged(self, newState):
        if self.__state != newState:
            if newState == VEHICLE_SIEGE_STATE.SWITCHING_ON:
                self.__siegeInProgress = 1
                self.__siegeTimeOut = self.SIEGE_TIMEOUT
                matrix = Math.Matrix(self.__appearance.compoundModel.matrix)
                self.__appearance.receiveShotImpulse(-matrix.applyToAxis(2), self.SIEGE_IMPULSE)
            elif newState == VEHICLE_SIEGE_STATE.ENABLED:
                self.__siegeInProgress = 0
            elif newState == VEHICLE_SIEGE_STATE.SWITCHING_OFF:
                self.__siegeInProgress = 1
                self.__siegeTimeOut = self.SIEGE_TIMEOUT
                matrix = Math.Matrix(self.__appearance.compoundModel.matrix)
                self.__appearance.receiveShotImpulse(-matrix.applyToAxis(2), self.SIEGE_IMPULSE)
            elif newState == VEHICLE_SIEGE_STATE.DISABLED:
                self.__siegeInProgress = 0
            self.__state = newState

    def tick(self, dt):
        if self.__siegeTimeOut > 0.0:
            self.__siegeTimeOut -= dt
        self.__effectManager.variables['siegeStart'] = 1 if self.__siegeTimeOut > 0.0 else 0
        self.__effectManager.variables['siegeProgress'] = self.__siegeInProgress