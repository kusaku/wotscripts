# Embedded file name: scripts/client/adapters/IRentSchemeAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from exchangeapi.Connectors import getObject
from config_consts import IS_CHINA

class IRentSchemeAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(IRentSchemeAdapter, self).__call__(account, ob.options, **kw)
        adaptedOB['rentScheme'] = [ el.__dict__ for el in adaptedOB['rentScheme'].price ] if adaptedOB['rentScheme'] and IS_CHINA else []
        return adaptedOB