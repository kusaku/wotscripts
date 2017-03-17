# Embedded file name: scripts/client/adapters/IPlaneNameAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class IPlaneNameAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        from Helpers.i18n import localizeAirplane
        ob = super(IPlaneNameAdapter, self).__call__(account, ob, **kw)
        if 'name' in ob and ob['name']:
            ob['name'] = localizeAirplane(ob['name'])
        return ob