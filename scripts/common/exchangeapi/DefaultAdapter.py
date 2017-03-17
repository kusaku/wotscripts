# Embedded file name: scripts/common/exchangeapi/DefaultAdapter.py
from exchangeapi.Connectors import getObject
from debug_utils import LOG_ERROR_FORMAT
from consts import EMPTY_IDTYPELIST
from config_consts import IS_DEVELOPMENT
from exchangeapi.IfaceUtils import getIface

class DefaultAdapter(object):

    def __init__(self, ifacename):
        self._ifacename = ifacename
        self._iface = getIface(ifacename)

    def __call__(self, account, ob, **kw):
        ob = ob if ob is None or isinstance(ob, dict) else getattr(ob, '__dict__', {})
        if not ob:
            return {}
        else:
            return dict(((attr, ob.get(attr, None)) for attr in self._iface.attr))

    def view(self, account, requestID, idTypeList, ob = None, **kw):
        if ob is not None:
            return ob
        else:
            return getObject(idTypeList, account) or idTypeList == EMPTY_IDTYPELIST and account or None

    def add(self, account, requestID, data, **kw):
        LOG_ERROR_FORMAT(account, 'Method add for adapter {0} must be implemented', self.__class__.__name__)
        raise not IS_DEVELOPMENT or AssertionError('Must be implemented')

    def delete(self, account, requestID, idTypeList, **kw):
        LOG_ERROR_FORMAT(account, 'Method delete for adapter {0} must be implemented', self.__class__.__name__)
        raise not IS_DEVELOPMENT or AssertionError('Must be implemented')

    def edit(self, account, requestID, idTypeList, data, ob = None, **kw):
        LOG_ERROR_FORMAT(account, 'Method edit for adapter {0} must be implemented', self.__class__.__name__)
        raise not IS_DEVELOPMENT or AssertionError('Must be implemented')

    def logStr(self, obtype, msg):
        return '[IFace: {0}; obType: {1}; Adapter: {2}] {3}'.format(self._iface.ifacename, obtype, self.__class__.__name__, msg)