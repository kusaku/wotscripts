# Embedded file name: scripts/client/eventhandlers/onBattleResult.py
import BigWorld
from exchangeapi.AdapterUtils import getAdapter
from exchangeapi.ErrorCodes import SUCCESS
from consts import EMPTY_IDTYPELIST

def expirePlaneExperience(planeID):
    player = BigWorld.player()
    player.responseSender([[planeID, 'plane']], 'IExperience', {}, SUCCESS)


def onBattleResultShort(event):
    expirePlaneExperience(event.ob['myData']['planeID'])
    getAdapter('IBattleResultShort', [event.idTypeList[0][1]]).add(None, None, event.ob, reportID=event.idTypeList[0][0])
    return


def onSessionBattleResults(event):
    getAdapter('ISessionBattleResults', ['account']).edit(None, None, EMPTY_IDTYPELIST, event.idTypeList[0][0], reportID=None)
    return