# Embedded file name: scripts/client/adapters/ILocalizationLanguageAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class ILocalizationLanguageAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        from Helpers.i18n import localizeLobby
        adaptedOB = super(ILocalizationLanguageAdapter, self).__call__(account, ob, **kw)
        adaptedOB['lang'] = localizeLobby('LOCALIZATION_LANGUAGE')
        return adaptedOB