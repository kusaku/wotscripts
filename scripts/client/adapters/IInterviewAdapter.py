# Embedded file name: scripts/client/adapters/IInterviewAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizeLobby

class IInterviewAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IInterviewAdapter, self).__call__(account, ob, **kw)
        adaptedOB['title'] = localizeLobby(adaptedOB['title'])
        adaptedOB['description'] = localizeLobby(adaptedOB['description'])
        return adaptedOB