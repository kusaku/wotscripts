# Embedded file name: scripts/client/adapters/ISkillDescriptionAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizeSkill, localizeLobby

class ISkillDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        isSpecialization = hasattr(ob, 'mainForSpecialization')
        aob = super(ISkillDescriptionAdapter, self).__call__(account, ob, **kw)
        for k, v in aob.iteritems():
            if k.find('Path') == -1 and k != 'uiIndex' and k != 'fullDescription':
                aob[k] = (isSpecialization and localizeLobby or localizeSkill)(v, skill_modifier=int(abs(100 - ob.mods[0].states[0] * 100)))

        return aob