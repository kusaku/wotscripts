# Embedded file name: scripts/client/adapters/ITypePlaneAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from clientConsts import PLANE_TYPE_BATTLE_RESULT_ICO_PATH, PREBATTLE_PLANE_TYPE_NAME, PLANE_TYPE_ICO_PATH
from Helpers.i18n import localizeLobby
from consts import PLANE_CLASS

class ITypePlaneAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(ITypePlaneAdapter, self).__call__(account, ob, **kw)
        if ob is not None:
            adaptedOB['type'] = ob.planeType
            adaptedOB['typeString'] = localizeLobby(PREBATTLE_PLANE_TYPE_NAME[ob.planeType])
            adaptedOB['typeIcoPath'] = PLANE_TYPE_ICO_PATH.icon(ob.planeType, PLANE_CLASS.REGULAR)
        return adaptedOB