# Embedded file name: scripts/client/adapters/ICrewMemberAdapter.py
from DefaultAdapter import DefaultAdapter
from Helpers.i18n import localizePilot
from _skills_data import SpecializationSkillDB
from Helpers.namesHelper import *
from SkillsHelper import MAX_SKILL_SP
from CrewHelpers import getNextRank
from consts import CREW_BODY_TYPE_PATH
from clientConsts import CREW_BODY_TYPE_LOCALIZE_PO_INDEX

class ICrewMemberAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(ICrewMemberAdapter, self).__call__(account, ob, **kw)
        from exchangeapi.Connectors import getObject
        country = getObject([[ob['planeSpecializedOn'], 'plane']]).country
        bodyTypeStr = CREW_BODY_TYPE_PATH[ob['bodyType']]
        bodyTypePO = CREW_BODY_TYPE_LOCALIZE_PO_INDEX[ob['bodyType']]
        icoIndex = ob['icoIndex']
        ob['firstName'] = localizePilot(CONTRY_PO_FILE_WRAPPER[country], FIRST_NAME_MSG_ID % (CONTRY_MSG_ID_WRAPPER[country], bodyTypePO, ob['firstName'] or 1))
        ob['lastName'] = localizePilot(CONTRY_PO_FILE_WRAPPER[country], LAST_NAME_MSG_ID % (CONTRY_MSG_ID_WRAPPER[country], bodyTypePO, ob['lastName'] or 1))
        rankID = ob['ranks']
        ob['ranks'] = localizePilot(CONTRY_PO_FILE_WRAPPER[country], RANKS_MSG_ID % (CONTRY_MSG_ID_WRAPPER[country], rankID))
        ob['rankIcoPath'] = RANKS_ICO_PATH % (country, rankID)
        ob['rankSmallIcoPath'] = RANKS_MINI_ICO_PATH % (country, rankID)
        ob['specialization'] = SpecializationSkillDB[ob['specialization']].id
        ob['crewIcoPath'] = CREW_ICO_PATH % (country, bodyTypeStr, icoIndex)
        ob['miniIcoPath'] = MINI_ICO_PATH % (country, bodyTypeStr, icoIndex)
        ob['infoIcoPath'] = INFO_ICO_PATH % (country, bodyTypeStr, icoIndex)
        ob['nationIcoPath'] = COUNTRY_ICO_PATH % country
        from db.DBLogic import g_instance as db_instance
        ob['nationID'] = db_instance.getNationIDbyName(country)
        ob['maxSP'] = MAX_SKILL_SP
        nextRankID = getNextRank(rankID, ob['specialization'])
        ob['nextRankIcoPath'] = RANKS_ICO_PATH % (country, nextRankID) if nextRankID != rankID else ''
        ob['nextRank'] = localizePilot(CONTRY_PO_FILE_WRAPPER[country], RANKS_MSG_ID % (CONTRY_MSG_ID_WRAPPER[country], nextRankID))
        return ob