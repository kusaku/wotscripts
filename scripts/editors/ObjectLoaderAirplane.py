# Embedded file name: scripts/editors/ObjectLoaderAirplane.py
from db.DBPostInit import posInitDB
from consts import WORLD_SCALING, IS_EDITOR
from ObjectLoader import ObjectLoader
import Math

class ObjectLoaderAirplane(ObjectLoader):

    def __init__(self, loadingData, dataHolder):
        ObjectLoader.__init__(self, loadingData, dataHolder)

    def load(self):
        gunsData = []
        shelsData = {}
        weapons = self.loadingData.aircraft.components.weapons2
        if len(self.dataHolder.weaponSlots) == 0:
            for slotId in weapons.slots.keys():
                self.dataHolder.weaponSlots.append((slotId, 0))

        try:
            manipulatorParams = (False,
             0,
             self.loadingData.aircraft.airplane,
             self.dataHolder.partsUpgrades,
             self.dataHolder.partsStates,
             gunsData,
             shelsData,
             weapons,
             self.dataHolder.weaponSlots,
             True,
             self.onLoaded,
             self.dataHolder.bodyType)
            self.dataHolder.manipulator = self.createManipulator(manipulatorParams)
        except Exception as e:
            print e

        self.dataHolder.updatePartsUpgradesStates()
        for slotId, slot in weapons.slots.items():
            for typeId, type in slot.types.items():
                for weapon in type.linkedModels:
                    self.dataHolder.weaponsData.append({'slot': slotId,
                     'type': typeId,
                     'weapon': weapon})

        matrix = Math.Matrix()
        matrix.setIdentity()
        self.__setEntityMatrix(matrix)

    def __getCameraOffset(self):
        settings = self.__getVisualSettings()
        if settings:
            return settings.cameraOffset
        vec = Math.Vector3(0, 0, 0)
        return vec

    def __getVisualSettings(self):
        if self.loadingData.aircraft and hasattr(self.loadingData.aircraft, 'airplane'):
            return self.loadingData.aircraft.airplane.visualSettings
        else:
            return None

    def __setEntityMatrix(self, matrix):
        matr = Math.Matrix()
        matr.setIdentity()
        scale = self.loadingData.aircraft.modelScaling if hasattr(self.loadingData.aircraft, 'modelScaling') else WORLD_SCALING
        matr.setScale(Math.Vector3(scale, scale, scale))
        if IS_EDITOR:
            pass
        else:
            cameraOffset = self.__getCameraOffset()
            matr.translation = -cameraOffset
        matr.postMultiply(matrix)
        self.dataHolder.setManipulatorMatrix(matr)