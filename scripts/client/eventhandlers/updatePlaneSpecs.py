# Embedded file name: scripts/client/eventhandlers/updatePlaneSpecs.py
from Account import PlayerAccount
import BigWorld

def updatePlaneSpecs(event):
    planeID = next((iD for iD, typ in event.idTypeList if typ == 'plane'), None)
    if planeID is not None and event.ob != event.prevob:
        player = BigWorld.player()
        if player is not None and player._lobbyInstance is not None and player.__class__ == PlayerAccount:
            player._lobbyInstance.lobbyModulesTreeHelper.sendSpecsToAS(event.ob.get('globalID'))
    return