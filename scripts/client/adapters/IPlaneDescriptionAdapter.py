# Embedded file name: scripts/client/adapters/IPlaneDescriptionAdapter.py
from Helpers.i18n import localizeAirplaneAny, localizeAirplane, localizeAirplaneMid, localizeAirplaneLong, localizeTooltips
import db
from adapters.DefaultAdapter import DefaultAdapter
from _airplanesConfigurations_db import airplanesConfigurationsList, airplanesDefaultConfigurations

class IPlaneDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(IPlaneDescriptionAdapter, self).__call__(account, ob, **kw)
        if ob is None:
            return adaptedOb
        else:
            if ob.description:
                adaptedOb['description'] = localizeAirplaneAny(ob.description.textDescription)
            dbInstance = db.DBLogic.g_instance
            adaptedOb['presetsList'] = airplanesConfigurationsList[ob.id]
            adaptedOb['defaultPreset'] = airplanesDefaultConfigurations[ob.id]
            adaptedOb['level'] = ob.level
            adaptedOb['icoPath'] = ob.iconPath
            adaptedOb['bigIcoPath'] = ob.previewIconPath
            adaptedOb['hudIcoPath'] = ob.hudIcoPath
            adaptedOb['treeIcoPath'] = ob.treeIconPath
            adaptedOb['battleLoadingIcoPath'] = ob.battleLoadingIconPath if hasattr(ob, 'battleLoadingIconPath') else ob.previewIconPath
            adaptedOb['middleName'] = localizeAirplaneMid(ob.name)
            adaptedOb['name'] = localizeAirplane(ob.name)
            adaptedOb['longName'] = localizeAirplaneLong(ob.name)
            adaptedOb['isExclusive'] = dbInstance.isPlaneExclusive(ob.id)
            adaptedOb['isTest'] = getattr(ob.options, 'isTest', False)
            if hasattr(ob, 'tags'):
                adaptedOb['tagsList'] = [ [localizeTooltips(x.name), x.type] for x in ob.tags.tag ]
            else:
                adaptedOb['tagsList'] = []
            return adaptedOb