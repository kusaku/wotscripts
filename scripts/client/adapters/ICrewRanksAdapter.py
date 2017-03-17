# Embedded file name: scripts/client/adapters/ICrewRanksAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizePilot
from Helpers.namesHelper import *
from CrewHelpers import getNextRank, getRankFromSP, getRank
from SkillsHelper import MAX_SKILL_SP, getCrewSP
from Helpers.cache import getFromCache
from _skills_data import SkillDB

def getRankInfo(sp, specialization, country):
    rankID = getRankFromSP(sp, specialization)
    return {'rank': rankID,
     'rankName': localizePilot(CONTRY_PO_FILE_WRAPPER[country], RANKS_MSG_ID % (CONTRY_MSG_ID_WRAPPER[country], rankID)),
     'rankIco': RANKS_ICO_PATH % (country, rankID)}


class ICrewRanksAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        aob = super(ICrewRanksAdapter, self).__call__(account, ob, **kw)
        member = getFromCache([kw['idTypeList'][0]], 'ICrewMember')
        country = getObject([[member['planeSpecializedOn'], 'plane']]).country
        specialization = SkillDB[member['specialization']].mainForSpecialization
        aob['ranks'] = {sp:getRankInfo(sp, specialization, country) for sp in range(1, MAX_SKILL_SP + 1)}
        return aob