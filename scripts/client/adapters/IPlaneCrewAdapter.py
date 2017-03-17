# Embedded file name: scripts/client/adapters/IPlaneCrewAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizeLobby
from adapters.ICrewMemberAdapter import SPECIALIZATION_MSG_ID
from CrewHelpers import getSpecializationName
from _skills_data import SpecializationSkillDB

class IPlaneCrewAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IPlaneCrewAdapter, self).__call__(account, ob, **kw)
        for entry in ob['crewMembers']:
            SpecializationSkill = SpecializationSkillDB[entry['specialization']]
            entry['specialization'] = SpecializationSkill.id
            entry['specializationIcoPath'], entry['specializationSmallIcoPath'] = SpecializationSkill.icoPath, SpecializationSkill.smallIcoPath

        return ob