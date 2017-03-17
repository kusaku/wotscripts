# Embedded file name: scripts/editors/ObjectLoader.py
import ObjectLoaderData
from ModelManipulatorEditor import ModelManipulatorEditor

class ObjectLoader:

    def __init__(self, loadingData, dataHolder):
        self.loadingData = loadingData
        if dataHolder == None:
            self.dataHolder = self.createDataHolder()
        else:
            self.dataHolder = dataHolder
        return

    def createDataHolder(self):
        return ObjectLoaderData.ObjectLoaderData()

    def createManipulator(self, paramTuple):
        return ModelManipulatorEditor(*paramTuple)

    def onLoaded(self):
        self.loadingData.onLoaded(self.dataHolder)
        self.loadingData = None
        self.dataHolder = None
        return


class LoadingData:

    def __init__(self, aircraft, endCallback):
        self.aircraft = aircraft
        self.endCallback = endCallback

    def onLoaded(self, dataHolder):
        self.endCallback(dataHolder)