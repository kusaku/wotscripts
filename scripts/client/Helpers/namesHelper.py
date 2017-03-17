# Embedded file name: scripts/client/Helpers/namesHelper.py
from consts import BOT_NAME_PREFFIX, BOT_NAME_SUFFIX
from i18n import localizePilot
from exchangeapi.Connectors import getObject
from clientConsts import CREW_BODY_TYPE_LOCALIZE_PO_INDEX
from CrewHelpers import DEFAULT_CREW_BODY_TYPE
COUNTRIES = map(str.lower, ('GB', 'Germany', 'Japan', 'USA', 'USSR', 'China', 'France'))
CONTRY_MSG_ID_WRAPPER = dict(((x, x[:3].upper()) for x in COUNTRIES))
CONTRY_MSG_ID_WRAPPER['USSR'.lower()] = 'RUS'
CONTRY_MSG_ID_WRAPPER['China'.lower()] = 'CN'
CONTRY_MSG_ID_WRAPPER['France'.lower()] = 'FR'
CONTRY_PO_FILE_WRAPPER = dict(((x, '%s_pilots' % x) for x in COUNTRIES))
CONTRY_PO_FILE_WRAPPER['Japan'.lower()] = 'japanese_pilots'
CONTRY_PO_FILE_WRAPPER['China'.lower()] = 'chinese_pilots'
CONTRY_PO_FILE_WRAPPER['France'.lower()] = 'france_pilots'
FIRST_NAME_MSG_ID = 'NAMES/%s%sN%d'
LAST_NAME_MSG_ID = 'NAMES/%s%s%d'
RANKS_MSG_ID = 'RANKS%s/%d'
SPECIALIZATION_MSG_ID = 'LOBBY_CREW_HEADER_%s'
INFO_ICO_PATH = 'icons/pilots/info/%s/%s/pilot_%02d.png'
CREW_ICO_PATH = 'icons/pilots/crew/%s/%s/pilot_%02d.png'
MINI_ICO_PATH = 'icons/pilots/mini/%s/%s/pilot_%02d.png'
COUNTRY_ICO_PATH = 'icons/shop/flag%s_.dds'
RANKS_ICO_PATH = 'icons/ranks/%s/crew/rank_%02d.dds'
RANKS_MINI_ICO_PATH = 'icons/ranks/%s/crewMini/rank_%02d.dds'
RANKS_INFO_ICO_PATH = 'icons/ranks/%s/info/rank_%02d.dds'

def getBotName(playerName, planeID, country = None):
    if playerName.find(BOT_NAME_PREFFIX) == 0 and playerName.find(BOT_NAME_SUFFIX) != 0:
        nameIndex = int(playerName[playerName.find(BOT_NAME_PREFFIX) + 1:playerName.find(BOT_NAME_SUFFIX)])
        poBodyTypeIndex = CREW_BODY_TYPE_LOCALIZE_PO_INDEX[DEFAULT_CREW_BODY_TYPE]
        if country is None:
            country = getObject([[planeID, 'plane']]).country
        return localizePilot(CONTRY_PO_FILE_WRAPPER[country], FIRST_NAME_MSG_ID % (CONTRY_MSG_ID_WRAPPER[country], poBodyTypeIndex, nameIndex))
    else:
        return playerName
        return


def replaceTagChars(name):
    return name.replace('<', '&lt;').replace('>', '&gt;')