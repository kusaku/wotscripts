# Embedded file name: scripts/client/helpers/tips.py
import random
import re
import sys
from collections import defaultdict, namedtuple
from constants import ARENA_GUI_TYPE
import constants
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.battle_control import arena_info, g_sessionProvider
from gui.shared.utils.functions import rnd_choice_loop
from helpers import i18n
from debug_utils import LOG_CURRENT_EXCEPTION
from items.vehicles import VEHICLE_CLASS_TAGS
import nations
ALL = 'all'
ANY = 'any'
EXCEPT = 'except'
INFINITY_STR_VALUE = 'infinity'
TIPS_IMAGE_SOURCE = '../maps/icons/battleLoading/tips/%s.png'
TIPS_GROUPS_SOURCE = '../maps/icons/battleLoading/groups/%s.png'
TIPS_PATTERN_PARTS_COUNT = 8
BATTLE_CONDITIONS_PARTS_COUNT = 2
_FoundTip = namedtuple('_FoundTip', 'status, body, icon')

class _TipsCriteria(object):
    __slots__ = ('_count', '_classTag', '_nation', '_level')

    def __init__(self):
        super(_TipsCriteria, self).__init__()
        self._count = 0
        self._classTag = ALL
        self._nation = ALL
        self._level = 1

    def getBattleCount(self):
        return self._count

    def setBattleCount(self, count):
        self._count = count
        return self

    def getClassTag(self):
        return self._classTag

    def setClassTag(self, tag):
        raise tag in VEHICLE_CLASS_TAGS or AssertionError
        self._classTag = tag
        return self

    def getNation(self):
        return self._nation

    def setNation(self, nation):
        raise nation in nations.NAMES or AssertionError
        self._nation = nation
        return self

    def getLevel(self):
        return self._level

    def setLevel(self, level):
        raise 0 < level < 11 or AssertionError
        self._level = level
        return self

    def find(self):
        raise NotImplementedError


class RandomTipsCriteria(_TipsCriteria):

    def find(self):
        iterator = getTipsIterator(constants.ARENA_GUI_TYPE.RANDOM, self._count, self._classTag, self._nation, self._level)
        if iterator is not None:
            tip = _FoundTip(*next(iterator))
        else:
            tip = _FoundTip('', '', '')
        return tip


class SandboxTipsCriteria(_TipsCriteria):

    def find(self):
        playerBaseYPos = enemyBaseYPos = 0
        arenaDP = g_sessionProvider.getCtx().getArenaDP()
        playerTeam = 1
        if arenaDP:
            playerTeam = arenaDP.getNumberOfTeam()
        positions = arena_info.getTeamBasePositions()
        for team, position, number in positions:
            if team == playerTeam:
                playerBaseYPos = position[2]
            else:
                enemyBaseYPos = position[2]

        geometryNames = ('100_thepit', '10_hills')
        geometryIndex = 0
        positionIndex = 0
        type = arena_info.getArenaType()
        if type is not None:
            geometryIndex = geometryNames.index(type.geometryName)
            positionIndex = 0 if playerBaseYPos < enemyBaseYPos else 1
        return _FoundTip(i18n.makeString('#tips:howToPlay'), i18n.makeString('#tips:sandbox%s' % geometryIndex), TIPS_IMAGE_SOURCE % ('sandbox' + str(geometryIndex) + str(positionIndex)))


class EventTipsCriteria(_TipsCriteria):

    def find(self):
        tips = [{'header': 'header01',
          'body': 'body01',
          'image': 'football01'},
         {'header': 'header02',
          'body': 'body02',
          'image': 'football02'},
         {'header': 'header03',
          'body': 'body03',
          'image': 'football03'},
         {'header': 'header04',
          'body': 'body04',
          'image': 'football04'}]
        tip = random.choice(tips)
        return _FoundTip(i18n.makeString('#tips:football/%s' % tip['header']), i18n.makeString('#tips:football/%s' % tip['body']), TIPS_IMAGE_SOURCE % tip['image'])


def getTipsCriteria(arena):
    if arena_info.isEventBattle():
        return EventTipsCriteria()
    elif arena_info.isInSandboxBattle(arena):
        return SandboxTipsCriteria()
    else:
        return RandomTipsCriteria()


def getTipsIterator(arenaGuiType, battlesCount, vehicleType, vehicleNation, vehicleLvl):
    tipsItems = _getConditionedTips(arenaGuiType, battlesCount, vehicleType, vehicleNation, vehicleLvl)
    if len(tipsItems) > 0:
        return rnd_choice_loop(*tipsItems)
    else:
        return None


class _ArenaGuiTypeCondition(namedtuple('_SquadExtra', ('mainPart', 'additionalPart'))):

    def validate(self, arenaGuiType):
        if self.mainPart == ALL:
            return True
        elif self.mainPart == ANY:
            arenaGuiTypes = map(_getIntValue, self.additionalPart)
            return arenaGuiType in arenaGuiTypes
        elif self.mainPart == EXCEPT:
            arenaGuiTypes = map(_getIntValue, self.additionalPart)
            return arenaGuiType not in arenaGuiTypes
        else:
            return False


_ArenaGuiTypeCondition.__new__.__defaults__ = (ALL, None)

def _readTips():
    result = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(list)))))
    tipsPattern = re.compile('^tip(\\d+)')
    try:
        translator = i18n.g_translators['tips']
    except IOError:
        LOG_CURRENT_EXCEPTION()
        return result

    for key in translator._catalog.iterkeys():
        if len(key) > 0:
            sreMatch = tipsPattern.match(key)
            if sreMatch is not None and len(sreMatch.groups()) > 0:
                strTipsConditions = key.split('/')
                if len(strTipsConditions) == TIPS_PATTERN_PARTS_COUNT:
                    tipID, status, group, battlesCountConditions, arenaGuiType, vehicleTypeCondition, nation, vehLevel = strTipsConditions
                    battlesCountConditions = battlesCountConditions.split('_')
                    if len(battlesCountConditions) == BATTLE_CONDITIONS_PARTS_COUNT:
                        minBattlesCount = _getIntValue(battlesCountConditions[0])
                        maxBattlesCount = _getIntValue(battlesCountConditions[1])
                        if minBattlesCount is not None and maxBattlesCount is not None:
                            battleCondition = (minBattlesCount, maxBattlesCount)
                            arenaGuiTypeParts = arenaGuiType.split('_')
                            arenaGuiTypeCondition = _ArenaGuiTypeCondition(arenaGuiTypeParts[0], arenaGuiTypeParts[1:])
                            for arenaGuiType in ARENA_GUI_TYPE.RANGE:
                                if arenaGuiTypeCondition.validate(arenaGuiType):
                                    result[battleCondition][arenaGuiType][vehicleTypeCondition][nation][vehLevel].append((i18n.makeString('#tips:%s' % status), i18n.makeString('#tips:%s' % key), _getTipIcon(tipID, group)))

    return result


def _getTipIcon(tipID, group):
    currentTipImage = TIPS_IMAGE_SOURCE % tipID
    if currentTipImage in RES_ICONS.MAPS_ICONS_BATTLELOADING_TIPS_ENUM:
        return currentTipImage
    return TIPS_GROUPS_SOURCE % group


def _getIntValue(strCondition):
    if strCondition == INFINITY_STR_VALUE:
        return sys.maxint
    else:
        intValue = None
        try:
            intValue = int(strCondition)
        except ValueError:
            LOG_CURRENT_EXCEPTION()

        return intValue
        return


_predefinedTips = _readTips()

def _getConditionedTips(arenaGuiType, battlesCount, vehicleType, vehicleNation, vehicleLvl):
    result = []
    battlesCountConditions = filter(lambda ((minBattlesCount, maxBattlesCount), item): minBattlesCount <= battlesCount <= maxBattlesCount, _predefinedTips.iteritems())
    for _, vehicleTypeConditions in battlesCountConditions:
        for vehType in (vehicleType, ALL):
            for nation in (vehicleNation, ALL):
                for level in (str(vehicleLvl), ALL):
                    result.extend(vehicleTypeConditions[arenaGuiType][vehType][nation][level])

    return result