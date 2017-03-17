# Embedded file name: scripts/client/adapters/IAwardDescriptionAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizeAchievements
from _awards_data import ACHIEVE_GROUP_TYPE

class IAwardDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IAwardDescriptionAdapter, self).__call__(account, ob, **kw)
        for k, v in ob.iteritems():
            if isinstance(v, basestring) and k.find('Path') == -1:
                ob[k] = localizeAchievements(v)
                if ob[k].isupper() and k == 'history':
                    ob[k] = ''

        ob['page'] = 1 if ob['group'] == ACHIEVE_GROUP_TYPE.NEW_YEAR else 0
        return ob