# Embedded file name: scripts/editors/ObjectLoaderBase.py
from ObjectLoader import ObjectLoader
import Math

class ObjectLoaderBase(ObjectLoader):

    def __init__(self, loadingData, dataHolder):
        ObjectLoader.__init__(self, loadingData, dataHolder)

    def load(self):
        partTypes = []
        partStates = []
        manipulatorParams = (False,
         0,
         self.loadingData.aircraft,
         partTypes,
         partStates,
         [],
         {},
         None,
         [],
         True,
         self.onLoaded)
        self.dataHolder.manipulator = self.createManipulator(manipulatorParams)
        self.dataHolder.updatePartsUpgradesStates()
        matrix = Math.Matrix()
        scale = self.loadingData.aircraft.modelScaling
        matrix.setScale(Math.Vector3(scale, scale, scale))
        self.dataHolder.manipulator.setMatrixProvider(matrix)
        return