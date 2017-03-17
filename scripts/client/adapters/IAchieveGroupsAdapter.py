# Embedded file name: scripts/client/adapters/IAchieveGroupsAdapter.py
from DefaultAdapter import DefaultAdapter
from _awards_data import ACHIEVE_GROUP_TYPE

class IAchieveGroupsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IAchieveGroupsAdapter, self).__call__(account, ob, **kw)
        ob['groups'] = dict((('ACHIEVEMENTS_TAB_AWARDS_%s' % k, v) for k, v in ACHIEVE_GROUP_TYPE.__dict__.iteritems() if isinstance(v, int) and not k.startswith('_') and not callable(getattr(ACHIEVE_GROUP_TYPE, k, None))))
        return ob