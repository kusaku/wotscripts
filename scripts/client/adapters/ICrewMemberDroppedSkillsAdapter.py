# Embedded file name: scripts/client/adapters/ICrewMemberDroppedSkillsAdapter.py
from DefaultAdapter import DefaultAdapter
import _economics
from Helpers.cache import getFromCache

class ICrewMemberDroppedSkillsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        member = getFromCache([kw['idTypeList'][0]], 'ICrewMember')
        dropLevel = [ [0, item.level] for item in _economics.Economics.crewSkillsDropCost.items ]
        return {'dropResults': dropLevel if member and len(member['skills']) > 0 else []}