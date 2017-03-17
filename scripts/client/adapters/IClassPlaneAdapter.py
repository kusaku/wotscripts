# Embedded file name: scripts/client/adapters/IClassPlaneAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from clientConsts import PLANE_TYPE_ICO_PATH
from exchangeapi.Connectors import getObject

class IClassPlaneAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(IClassPlaneAdapter, self).__call__(account, ob, **kw)
        plane = getObject(kw['idTypeList'])
        if plane is not None and adaptedOb['classValue'] is not None:
            adaptedOb['classIcoPath'] = PLANE_TYPE_ICO_PATH.icon(plane.planeType, adaptedOb['classValue'])
        else:
            adaptedOb['classIcoPath'] = ''
        return adaptedOb