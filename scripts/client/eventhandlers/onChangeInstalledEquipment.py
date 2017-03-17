# Embedded file name: scripts/client/eventhandlers/onChangeInstalledEquipment.py
import Settings
from gui.WindowsManager import g_windowsManager

def onChangeInstalledEquipment(event):
    import BWPersonality
    planeID = next((iD for iD, typ in event.idTypeList if typ == 'plane'), None)
    if planeID:
        if event.ob != event.prevob:
            helper = BWPersonality.g_lobbyCarouselHelper
            helper.inventory.setPlaneEquipment(planeID, event.ob['equipmentIDs'])
            helper.refreshAircraftData(planeID, True)
            if planeID in helper.inventory.getBoughtAircraftsList():
                globalID = helper.inventory.getInstalledUpgradesGlobalID(planeID)
                accountUI = g_windowsManager.getAccountUI()
                shortCofigSpec = [[globalID, 'planePreset']]
                measurementSystem = Settings.g_instance.gameUI['measurementSystem']
                configSpec = shortCofigSpec + [[measurementSystem, 'measurementSystem']]
                accountUI.editIFace([[{'IConfigSpecs': {}}, configSpec]])
                accountUI.editIFace([[{'IShortConfigSpecs': {}}, shortCofigSpec]])
    return