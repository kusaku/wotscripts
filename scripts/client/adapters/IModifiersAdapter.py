# Embedded file name: scripts/client/adapters/IModifiersAdapter.py
from adapters.DefaultAdapter import DefaultAdapter

class IModifiersUpgradeAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(IModifiersUpgradeAdapter, self).__call__(account, ob, **kw)
        adaptedOb['modsList'] = [ dict(activation=bool(getattr(x, 'activationRequired', False)), type=x.type, value=x.value_) for x in ob.mods ]
        return adaptedOb