# Embedded file name: scripts/client/eventhandlers/onChangeExperience.py
from Account import PlayerAccount
import BigWorld

def onSynced():
    player = BigWorld.player()
    if player != None and player.__class__ == PlayerAccount and player._lobbyInstance is not None:
        if player._lobbyInstance.lobbyModulesTreeHelper is not None and player._lobbyInstance.lobbyModulesTreeHelper.initialized:
            player._lobbyInstance.lobbyModulesTreeHelper.updatePlanesExperience()
            player._lobbyInstance.lobbyModulesTreeHelper.updateAircraftInfo()
            player._lobbyInstance.lobbyModulesTreeHelper.sendSpecsToAS()
        if player._lobbyInstance.researchTreeHelper is not None:
            player._lobbyInstance.researchTreeHelper.reloadCurrentBranch()
    return


def onChangeExperience(event):
    planeID = next((iD for iD, typ in event.idTypeList if typ == 'plane'), None)
    if planeID is not None and event.ob != event.prevob:
        from BWPersonality import g_lobbyCarouselHelper as lch
        lch.inventory.syncAircraftsData([planeID], onSynced)
    return