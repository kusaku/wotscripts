# Embedded file name: scripts/client/adapters/IAwardsListAdapter.py
from DefaultAdapter import DefaultAdapter
import _awards_data

class IAwardsListAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = {'medals': [],
         'ribbons': [],
         'achievements': [ k for k, v in _awards_data.AwardsDB.iteritems() if v.options.quest == _awards_data.QUEST_TYPE.NONE ]}
        return super(IAwardsListAdapter, self).__call__(account, ob, **kw)