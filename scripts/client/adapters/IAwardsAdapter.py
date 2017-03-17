# Embedded file name: scripts/client/adapters/IAwardsAdapter.py
from DefaultAdapter import DefaultAdapter
import _awards_data
from consts import NEW_ACHIEVEMENT_DATA, NEW_MEDAL_DATA, NEW_RIBBON_DATA, NEW_AWARD_DATA, AWARD_DATA_KEYS

def processHideAchievements(ob):

    def createStruct(iD):
        return dict(id=iD, progress=0, maxProgress=0, firstTime=0, lastTime=0, count=0, planes=[])

    a_ids = set((a['id'] for a in ob['achievements']))
    ob['achievements'].extend((createStruct(a.id) for a in _awards_data.Awards.award if a.id not in a_ids and a.options.enable and not a.ui.hidden and a.options.quest == _awards_data.QUEST_TYPE.NONE))
    list_del = set()
    a_ids = set((a['id'] for a in ob['achievements'] if a['count'] > 0))
    for a in ob['achievements']:
        id = a['id']
        count = a['count']
        parentId = getattr(_awards_data.AwardsDB[id].ui, 'parentId', -1)
        if parentId >= 0:
            if count > 0:
                if parentId in a_ids:
                    list_del.add(id)
            else:
                list_del.add(parentId)

    ob['achievements'] = [ a for a in ob['achievements'] if a['id'] not in list_del ]


class IAwardsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        processHideAchievements(ob)
        return super(IAwardsAdapter, self).__call__(account, ob, **kw)


class IAwardsPlaneAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        processHideAchievements(ob)
        return super(IAwardsPlaneAdapter, self).__call__(account, ob, **kw)