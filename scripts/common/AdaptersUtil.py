# Embedded file name: scripts/common/AdaptersUtil.py
import Interfaces
import BigWorld
import db.DBLogic
from consts import PLANE_KEYS

def getAircraftOb(account, params):
    inv = account.pdata['inventory']
    boughtAircraftsDict = dict(((aircraftInfo[PLANE_KEYS.PLANE], aircraftInfo) for aircraftInfo in inv['planes']))

    def create_ob(planeID):
        aircraftData = boughtAircraftsDict.get(planeID, None)

        def updateCamouflagesDict(camouflagesDict):
            if camouflagesDict is None:
                return
            else:
                camouflagesLeftTime = {}
                for groupID, groupList in camouflagesDict.items():
                    camouflagesLeftTime[groupID] = [ {'id': camouflage['id'],
                     'expiring': camouflage['expiring'],
                     'timeLeft': getLeftTimeByExpiring(camouflage['expiring'])} for camouflage in groupList ]

                return camouflagesLeftTime

        def getLeftTimeByExpiring(expiring):
            if expiring == -1:
                return -1
            return max(expiring - BigWorld.time(), 0) / 3600

        import _economics
        dailyWinBonusRemains = account.dailyWinBonusRemains(planeID)
        return Interfaces.create_ob(Interfaces.ISYNC_AIRCRAFT, planeID, inv['planes'].index(aircraftData) if aircraftData is not None else None, aircraftData if aircraftData is not None else None, None, account.pdata['stats']['planeExp'].get(planeID, 0), _economics.Economics.dailyBonus.firstWinBonus.xpCoeff if dailyWinBonusRemains > 0 else 1, dailyWinBonusRemains)

    return [ create_ob(aircraftID) for aircraftID in params ]


def getInventoryOb(account, params):
    inv = account.pdata['inventory']
    boughtAircraftsList = [ aircraftInfo[PLANE_KEYS.PLANE] for aircraftInfo in inv['planes'] ]
    return Interfaces.create_ob(Interfaces.ISYNC_INVENTORY, inv['upgrades'], inv['equipment'], inv['consumables'], inv['openedAircrafts'], boughtAircraftsList, inv['customPresets'], inv['inBattlePlaneList'], inv['unlockPlaneMap'])


def getStatsOb(account, params):
    stats = account.pdata['stats']
    return Interfaces.create_ob(Interfaces.ISYNC_STATS, stats['credits'], stats['gold'], stats['slots'], stats['current_slot'], stats['experience'], account.pdata['createdAt'])


def getPlaneList(account, params):
    return Interfaces.create_ob(Interfaces.ISYNC_PLANE_LIST, account.pdata['inventory']['elitePlanes'])


adapters = {'ISYNC_AIRCRAFT': getAircraftOb,
 'ISYNC_INVENTORY': getInventoryOb,
 'ISYNC_STATS': getStatsOb,
 'ISYNC_PLANE_LIST': getPlaneList}