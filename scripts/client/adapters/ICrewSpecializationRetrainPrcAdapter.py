# Embedded file name: scripts/client/adapters/ICrewSpecializationRetrainPrcAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.cache import getFromCache
import db.DBLogic

class ICrewSpecializationRetrainPrcAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        member = getFromCache([kw['idTypeList'][0]], 'ICrewMember')
        newPlaneID = kw['idTypeList'][1][0]
        percentList = []
        isPremium = db.DBLogic.g_instance.isPlanePremium(newPlaneID)
        if not isPremium:
            curPlaneSettings = db.DBLogic.g_instance.getAircraftData(member['planeSpecializedOn'])
            newPlaneSettings = db.DBLogic.g_instance.getAircraftData(newPlaneID)
            if curPlaneSettings.airplane.planeType != newPlaneSettings.airplane.planeType:
                percentList.append(50)
            else:
                percentList.append(70)
        return {'percents': percentList if member['planeSpecializedOn'] != newPlaneID else []}