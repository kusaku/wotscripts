# Embedded file name: scripts/client/adapters/IAvailableSkillsAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizeLobby

class IAvailableSkillsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IAvailableSkillsAdapter, self).__call__(account, ob, **kw)
        from _skills_data import SkillDB
        for skill in ob['skills']:
            skillData = SkillDB[skill['id']]
            skill['cost'] = skillData.cost
            skill['group'] = skillData.group
            skill['order'] = skillData.order
            skill['dependedFrom'] = getattr(skillData, 'dependedFrom', 0)
            skill['dependedTo'] = next((s.id for s in SkillDB.itervalues() if hasattr(s, 'dependedFrom') and s.dependedFrom == skill['id']), 0)

        return ob