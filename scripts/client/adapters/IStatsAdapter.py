# Embedded file name: scripts/client/adapters/IStatsAdapter.py
from copy import deepcopy
from functools import partial
from locale import getpreferredencoding
from time import localtime, strftime
from Helpers.i18n import localizeAchievements, getFormattedTime, localizeAirplaneLong
from _awards_data import AwardsDB
import _awards_data
import db.DBLogic
from adapters.DefaultAdapter import DefaultAdapter
from consts import AWARD_DATA_KEYS
from debug_utils import LOG_DEBUG, LOG_ERROR
from HelperFunctions import wowpRound
import Settings
NATION_FLAG_TEMPLATE = 'icons/shop/flagAchiev{0}.dds'

def _createStatRecord(stats, name = None, valueKey = None, percentValueKey = None, title = None):
    value = None
    percentValue = None
    if valueKey is not None:
        value = stats.get(valueKey, 0)
    if percentValueKey is not None:
        percentValue = stats.get(percentValueKey, 0)
    planeStat = {'name': localizeAchievements(name),
     'value': value,
     'percentValue': percentValue,
     'title': localizeAchievements(title)}
    return planeStat


def _convertStats(planeID, stats, lastGameTime):
    stats['draws'] = stats.get('gamesPlayed', 0) - stats.get('losses', 0) - stats.get('wins', 0)
    stats['totalGroundObjectsDestroyed'] = stats.get('totalGroundObjectsDestroyed', 0) + stats.get('totalTurretsDestroyed', 0) + stats.get('totalTeamObjectsDestroyed', 0)

    def __sum(*args):
        if args[0] is None:
            LOG_ERROR('Not all stats receive from server. See None or absent params in stats={0}'.format(stats))
            return 0
        else:
            return sum(*args)
            return

    def __producePercent(totalKey, partialKey, precision = 0):
        return lambda ignoreArg: (wowpRound(stats[partialKey] * 100.0 / stats[totalKey], precision) if stats[totalKey] > 0 else 0)

    stats['totalShots'] = stats['totalShots'][0]
    stats['totalHits'] = stats['totalHits'][0]
    conversions = [('totalKilled', __sum),
     ('totalDamageDealt', __sum),
     ('totalStructureDamage', __sum),
     ('totalTeamObjectsDestroyed', __sum),
     ('totalGroundObjectsDestroyed', __sum),
     ('totalTurretsDestroyed', __sum),
     ('winsPercent', __producePercent('gamesPlayed', 'wins', 2)),
     ('lossesPercent', __producePercent('gamesPlayed', 'losses', 2)),
     ('survivedPercent', __producePercent('gamesPlayed', 'survived', 2)),
     ('hitsPercent', __producePercent('totalShots', 'totalHits')),
     ('squadWinsPercent', __producePercent('gamesPlayed', 'squadWins'))]
    for item in conversions:
        stats[item[0]] = item[1](stats.get(item[0], None))

    stats['planeID'] = planeID
    if stats['gamesPlayed'] > 0:
        stats['avgExperience'] = stats['baseGainExperience'] / stats['gamesPlayed']
        if stats['wins'] + stats['losses'] == stats['gamesPlayed']:
            stats['winsPercent'] = 100 - stats['lossesPercent']
        stats['drawsPercent'] = wowpRound(100.0 - stats['lossesPercent'] - stats['winsPercent'], 2)
    else:
        stats['avgExperience'] = 0
        stats['drawsPercent'] = 0
    if lastGameTime > 0:
        stats['lastGameTime'] = getFormattedTime(lastGameTime, Settings.g_instance.scriptConfig.timeFormated['dbYHMS'])
    else:
        stats['lastGameTime'] = ''
    return [_createStatRecord(stats, 'ACHIEVEMENTS_TOTAL_BATTLES', 'gamesPlayed'),
     _createStatRecord(stats, 'ACHIEVEMENTS_WINS', 'wins', 'winsPercent'),
     _createStatRecord(stats, 'ACHIEVEMENTS_DEFEATS', 'losses', 'lossesPercent'),
     _createStatRecord(stats, 'ACHIEVEMENTS_DRAWS', 'draws', 'drawsPercent'),
     _createStatRecord(stats, 'ACHIEVEMENTS_SURVIVED_BATTLES', 'survived', 'survivedPercent'),
     _createStatRecord(stats, None, None, None, 'ACHIEVEMENTS_BETTLE_EFFICIENCY'),
     _createStatRecord(stats, 'ACHIEVEMENTS_AIRCRAFTS_DESTROYED', 'totalKilled'),
     _createStatRecord(stats, 'ACHIEVEMENTS_MAX_DESTROYED_PER_BATTLE', 'maxKilled'),
     _createStatRecord(stats, 'ACHIEVEMENTS_WINS_IN_GROUP', 'totalAssists'),
     _createStatRecord(stats, 'ACHIEVEMENTS_GROUND_TARGETS_DESTROYED', 'totalGroundObjectsDestroyed'),
     _createStatRecord(stats, 'ACHIEVEMENTS_', 'hitsPercent'),
     _createStatRecord(stats, 'ACHIEVEMENTS_DAMAGE_TO_AIRCRAFTS', 'totalDamageDealt'),
     _createStatRecord(stats, 'ACHIEVEMENTS_DAMAGE_TO_GROUND_TARGETS', 'totalStructureDamage'),
     _createStatRecord(stats, None, None, None, 'ACHIEVEMENTS_XP'),
     _createStatRecord(stats, 'ACHIEVEMENTS_SUMMARY_XP', 'gainExperience'),
     _createStatRecord(stats, 'ACHIEVEMENTS_AVG_XP_PER_BATTLE', 'avgExperience'),
     _createStatRecord(stats, 'ACHIEVEMENTS_MAX_XP_FOR_BATTLE', 'maxGainExperience')]


class IPlaneStatsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        lastGameTime = ob['stats'].pop('lastGameTime', None)
        ob['row'] = ob['stats']
        ob['stats'] = _convertStats(kw['idTypeList'][0][0], ob['stats'], lastGameTime)
        return ob


class ISummaryStatsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        lastGameTime = ob['lastGameTime']
        ob['lastGameTime'] = getFormattedTime(lastGameTime, Settings.g_instance.scriptConfig.timeFormated['dmYHM']) if lastGameTime > 0 else ''
        ob['gamesPlayed'] = ob['stats']['gamesPlayed']
        ob['createdAt'] = strftime(Settings.g_instance.scriptConfig.timeFormated['dmYHM'], localtime(float(ob['createdAt']))).decode(getpreferredencoding())
        ob['stats'] = _convertStats(kw['idTypeList'][0][0], ob['stats'], lastGameTime)
        return ob


class IShortPlaneDescription(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IShortPlaneDescription, self).__call__(account, ob, **kw)
        planeData = db.DBLogic.g_instance.getAircraftData(kw['idTypeList'][0][0]).airplane
        ob['planeName'] = localizeAirplaneLong(planeData.name)
        ob['level'] = planeData.level
        ob['icoPath'] = planeData.iconPath
        ob['flagPath'] = NATION_FLAG_TEMPLATE.format(planeData.country)
        ob['nationID'] = db.DBLogic.g_instance.getNationIDbyAircraftID(kw['idTypeList'][0][0])
        ob['planeID'] = kw['idTypeList'][0][0]
        return ob


def processAwars(ob):

    def awardList(items, stat):
        for k, v in items:
            if v.options.enable:
                if v.options.ribbon:
                    count = stat.get(k, {}).get(AWARD_DATA_KEYS.MAX_PROGRESS, 0) if stat.get(k, {}).get(AWARD_DATA_KEYS.COUNT, 0) > 0 else 0
                else:
                    count = stat.get(k, {}).get(AWARD_DATA_KEYS.COUNT, 0)
                if (count > 0 or not v.ui.hidden) and _awards_data.AwardsDB[k].options.quest == _awards_data.QUEST_TYPE.NONE:
                    yield {'id': k,
                     'count': count}

    ob['medals'] = []
    ob['achievements'] = list(awardList(AwardsDB.iteritems(), ob['stats']['awards']))
    ob['ribbons'] = []
    a_ids = set([ a['id'] for a in ob['achievements'] if a['count'] > 0 ])
    list_del = set()
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


class IPlayerSummaryStatsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        lastGameTime = ob.get('lastGameTime', 0)
        ob['lastGameTime'] = getFormattedTime(lastGameTime, Settings.g_instance.scriptConfig.timeFormated['dmYHM']) if lastGameTime > 0 else ''
        ob['gamesPlayed'] = ob['stats']['gamesPlayed']
        ob['createdAt'] = strftime(Settings.g_instance.scriptConfig.timeFormated['dmYHM'], localtime(float(ob['stats']['createdAt']))).decode(getpreferredencoding()) if ob['stats']['createdAt'] > 0 else ''
        processAwars(ob)
        ob['stats'] = _convertStats(kw['idTypeList'][0][0], ob['stats'], lastGameTime)
        return ob


class IPlayerShortPlaneDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IPlayerShortPlaneDescriptionAdapter, self).__call__(account, ob, **kw)
        import db.DBLogic
        planeData = db.DBLogic.g_instance.getAircraftData(kw['idTypeList'][1][0]).airplane
        ob['planeName'] = localizeAirplaneLong(planeData.name)
        ob['level'] = planeData.level
        ob['icoPath'] = planeData.iconPath
        ob['flagPath'] = NATION_FLAG_TEMPLATE.format(planeData.country)
        ob['nationID'] = db.DBLogic.g_instance.getNationIDbyAircraftID(kw['idTypeList'][1][0])
        ob['planeID'] = kw['idTypeList'][1][0]
        return ob


class IPlayerPlaneStatsAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        processAwars(ob)
        ob['stats'] = _convertStats(kw['idTypeList'][1][0], ob['stats'], ob['stats'].get('lastGameTime', 0))
        return ob