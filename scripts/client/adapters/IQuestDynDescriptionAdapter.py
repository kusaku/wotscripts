# Embedded file name: scripts/client/adapters/IQuestDynDescriptionAdapter.py
from Helpers.i18n import localizeLobby
from adapters.DefaultAdapter import DefaultAdapter
from exchangeapi.Connectors import getObject

class IQuestDynDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(IQuestDynDescriptionAdapter, self).__call__(account, ob, **kw)
        for n in ('description',):
            adaptedOB[n], _dynVar = adaptedOB[n]
            if adaptedOB[n].isupper():
                adaptedOB[n] = localizeLobby(adaptedOB[n], **_dynVar)
            else:
                adaptedOB[n] = adaptedOB[n].format(**_dynVar)

        return adaptedOB