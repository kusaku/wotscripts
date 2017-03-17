# Embedded file name: scripts/client/adapters/IQuestDescriptionAdapter.py
from Helpers.i18n import localizeLobby, localizeAchievements
from adapters.DefaultAdapter import DefaultAdapter
from exchangeapi.Connectors import getObject

class IQuestDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(IQuestDescriptionAdapter, self).__call__(account, ob, **kw)
        for n in ('name',):
            adaptedOB[n], _dynVar = adaptedOB[n]
            if adaptedOB[n].isupper():
                adaptedOB[n] = localizeLobby(adaptedOB[n], **_dynVar)
                if adaptedOB[n].isupper():
                    adaptedOB[n] = localizeAchievements(adaptedOB[n])
            else:
                adaptedOB[n] = adaptedOB[n].format(**_dynVar)

        if 'names' in adaptedOB['maps']:
            import db.DBLogic
            from Helpers.i18n import localizeMap
            locationMap = {}
            for locationData in db.DBLogic.g_instance.getArenaList():
                locationMap[locationData.typeID] = locationData.typeName

            locationMap[-1] = 'map_undefined'
            names = (localizeMap(locationMap[mapID].upper()) for mapID in adaptedOB['maps']['names'])
            adaptedOB['maps']['names'] = list(names)
        return adaptedOB