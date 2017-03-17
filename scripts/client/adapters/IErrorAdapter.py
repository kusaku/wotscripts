# Embedded file name: scripts/client/adapters/IErrorAdapter.py
from DefaultAdapter import DefaultAdapter
from OperationCodes import getCodeDescription

class IErrorAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IErrorAdapter, self).__call__(account, ob, **kw)
        if not ob['description']:
            errorCode = ob['code']
            errorKwargs = ob['kwargs']
            ob['description'] = getCodeDescription(errorCode, False, **errorKwargs)
        return ob