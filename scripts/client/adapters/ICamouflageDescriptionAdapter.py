# Embedded file name: scripts/client/adapters/ICamouflageDescriptionAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from debug_utils import LOG_ERROR

class ICamouflageDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        import db.DBLogic
        from consts import CAMOUFLAGE_GROUP_ID_TO_NAME_MAP
        adaptedOB = super(ICamouflageDescriptionAdapter, self).__call__(account, ob, **kw)
        if ob is None:
            raise Exception, 'ICamouflageDescriptionAdapter kw={0}'.format(kw)
        try:
            adaptedOB['isUnique'] = str(ob.awardTag).startswith('reward') or str(ob.awardTag).startswith('warcache')
            adaptedOB['planeID'] = ob.planeID
            adaptedOB['icoPath'] = db.DBLogic.g_instance.getAircraftData(ob.planeID).airplane.visualSettings.surfaceSettings.decalsSettings.decalGroups[CAMOUFLAGE_GROUP_ID_TO_NAME_MAP[ob.camouflageType]].decals[ob.camouflageID].icoPath
        except Exception as e:
            adaptedOB['icoPath'] = ''
            adaptedOB['planeID'] = 0
            LOG_ERROR('camouflage not found. Error {0}'.format(e))

        return adaptedOB