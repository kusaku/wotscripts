# Embedded file name: scripts/client/adapters/IRequiredExperienceAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class IRequiredExperienceAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IRequiredExperienceAdapter, self).__call__(account, ob, **kw)
        import BWPersonality
        inventory = BWPersonality.g_lobbyCarouselHelper.inventory
        dataMap = inventory.getAircraftClientDataMap(kw['idTypeList'][0][0])
        adaptedOB['requiredExperience'] = dataMap['reqiuredExperience']
        return adaptedOB