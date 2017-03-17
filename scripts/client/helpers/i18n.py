# Embedded file name: scripts/client/Helpers/i18n.py
from encodings import utf_8
import gettext, consts
import BigWorld
from debug_utils import LOG_DEBUG, LOG_WARNING, LOG_CURRENT_EXCEPTION, LOG_INFO, LOG_ERROR
from config_consts import IS_DEVELOPMENT
from time import localtime, strftime
from locale import getlocale, LC_TIME
import os
import glob
g_translators = {}

def convert(utf8String):
    try:
        return utf_8.decode(utf8String)[0]
    except Exception:
        LOG_CURRENT_EXCEPTION()
        LOG_WARNING('Wrong UTF8 string', utf8String)
        return utf_8.decode('----')[0]


g_localizationPath = convert(BigWorld.wg_resolveFileName('localization')) + '\\'

def makeString(key, *args, **kargs):
    try:
        if not key or key[0] != '#':
            return key
        moName, subkey = key[1:].split(':', 1)
        if not moName or not subkey:
            return key
        if subkey.endswith('\r'):
            subkey = subkey[:len(subkey) - 1]
        text = BigWorld.gettext(moName, subkey)
        if text == '?empty?':
            text = ''
        if args:
            try:
                text = text % args
            except TypeError:
                LOG_WARNING("Arguments do not match string read by key '%s': %s", (key, args))
                return key

        elif kargs:
            try:
                text = text % kargs
            except TypeError:
                LOG_WARNING("Arguments do not match string read by key '%s': %s", (key, kargs))
                return key

        return text
    except Exception:
        LOG_CURRENT_EXCEPTION()
        LOG_WARNING('Key string incompatible with args', key, args, kargs)
        return key


def localizeMap(label):
    return convert(makeString('#maps:' + label.upper()))


def localizeAchievements(label, *args, **kargs):
    return convert(makeString('#achievements:' + label.upper())).format(*args, **kargs)


def localizeSkill(label, *args, **kargs):
    return convert(makeString('#skills:' + label.upper())).format(*args, **kargs)


def localizeMenu(label, message = None):
    if message is not None:
        return convert(makeString('#menu:' + label.upper())) % message
    else:
        return convert(makeString('#menu:' + label.upper()))


def localizeBattleResults(label):
    return convert(makeString('#battle_results:' + label.upper()))


def localizeMessages(label):
    return convert(makeString('#messages:' + label.upper()))


def localizeLobby(label, *args, **kargs):
    return convert(makeString('#lobby:' + label.upper())).format(*args, **kargs)


def localizeLobbyUnformatted(label):
    return convert(makeString('#lobby:' + label.upper()))


def localizeHUD(label):
    return convert(makeString('#hud:' + label.upper()))


def localizeOptions(label):
    return convert(makeString('#options:' + label.upper()))


def localizeAirplaneAny(label):
    return convert(makeString('#airplanes:' + label.upper()))


def localizeAirplane(label):
    return convert(makeString('#airplanes:PLANE_NAME_' + label.upper()))


def localizeAirplaneLong(label):
    return convert(makeString('#airplanes:PLANE_LONGNAME_' + label.upper()))


def localizeAirplaneMid(label):
    return convert(makeString('#airplanes:PLANE_MIDNAME_' + label.upper()))


def localizeObject(label):
    return convert(makeString('#maps:OBJECT_NAME_' + label.upper()))


def localizeComponents(label):
    return convert(makeString('#components:' + label.upper()))


def localizePresets(label):
    return convert(makeString('#presets:' + label.upper()))


def localizeTrainingRooms(label):
    return convert(makeString('#trainingRooms:' + label.upper()))


def localizePilot(key, label):
    if label is None:
        return
    else:
        return convert(makeString('#%s:' % key + label.upper()))


def localizeAchievements(label):
    if label is None:
        return
    else:
        return convert(makeString('#achievements:' + label.upper()))


def localizeAchievementsInQuest(label):
    if label is None:
        return
    else:
        list = label.split('|achievements:')
        listSize = len(list)
        if listSize > 1:
            import _awards_data
            i = 1
            while i < listSize:
                pos = list[i].find('|')
                if pos > 0:
                    try:
                        achievId = list[i][0:pos]
                        awardData = _awards_data.AwardsDB[int(achievId)]
                        awardStr = localizeAchievements(awardData.ui.name)
                        label = label.replace('|achievements:{0}|'.format(achievId), awardStr)
                    except:
                        LOG_CURRENT_EXCEPTION()

                i = i + 1

        return label


def localizeTutorial(label):
    """
    Returns localized string
    @param label: localized string id
    @return: string
    """
    return convert(makeString('#tutorial:' + label.upper()))


def localizeChat(label):
    return convert(makeString('#chat:' + label.upper()))


def localizeTooltips(label):
    return convert(makeString('#tooltips:' + label.upper()))


def localizeCAPTCHA(label):
    return convert(makeString('#captcha:' + label.upper()))


def localizeAOGAS(label):
    return convert(makeString('#AOGAS:' + label.upper()))


def printAllTranslationFiles():
    allFiles = []
    path = os.path.join(g_localizationPath, 'text', 'LC_MESSAGES', '*.mo')
    names = glob.glob(path)
    for name in names:
        fileName = os.path.split(name)
        if fileName:
            allFiles.append(fileName[len(fileName) - 1].encode('utf8'))

    LOG_INFO('localizationPath: %s' % g_localizationPath)
    LOG_INFO('localization files exists: %s' % allFiles)


def getTranslationTable(moName, language):
    return BigWorld.translations(moName)
    path = g_localizationPath
    translator = gettext.translation(moName, path, languages=['text'])
    d = {}
    for key, value in translator._catalog.items():
        sKey = str(key)
        if sKey != '':
            d[sKey] = value

    return d


def getFormattedTime(utc, format = None):
    if format is None:
        import Settings
        format = Settings.g_instance.scriptConfig.timeFormated['default']
    result = ''
    if utc:
        result = strftime(format, localtime(float(utc))).decode(getlocale(LC_TIME)[1])
    return result


def localizeTimeInterval(period):
    result = ''
    days, rest = divmod(period + 30, 86400)
    hours, rest = divmod(rest, 3600)
    minutes = int(rest / 60)
    if days == 0 and hours == 0 and minutes < 1.0:
        minutes = 1.0
    if days > 0:
        result += '%d ' % days + localizeLobby('COUNTER_DAYS')
    if hours > 0:
        result += ' %d ' % hours + localizeLobby('COUNTER_HOURS')
    if minutes > 0:
        result += ' %d ' % minutes + localizeLobby('COUNTER_MINUTES')
    return result


def localizeUpgrade(upgrade, addPremiumSuffix = False):
    import db.DBLogic
    dbInstance = db.DBLogic.g_instance
    PERMIUM_SUFIX_FOR_UPGRADE_TYPE = [consts.UPGRADE_TYPE.BOMB, consts.UPGRADE_TYPE.ROCKET]
    if addPremiumSuffix and upgrade.type in PERMIUM_SUFIX_FOR_UPGRADE_TYPE:
        planes = dbInstance.getSuitablePlanesForUpgrade(upgrade)
        if planes and dbInstance.isPlanePremium(planes[0]):
            return '{0} {1}'.format(localizeComponents('WEAPON_NAME_{0}'.format(upgrade.name)), localizeComponents('WEAPON_NAME_GOLDBELT'))
    if upgrade.type in consts.UPGRADE_TYPE.WEAPON:
        return localizeComponents('WEAPON_NAME_{0}'.format(upgrade.name))
    if upgrade.type == consts.UPGRADE_TYPE.TURRET:
        turret = dbInstance.getTurretData(upgrade.name)
        if turret:
            weaponName = localizeComponents('WEAPON_NAME_{0}'.format(turret.hangarName))
            weaponCount = turret.weaponCount
        else:
            weaponName = ''
            weaponCount = 1
        weaponName = '{0}x {1}'.format(weaponCount, weaponName) if weaponCount > 1 else weaponName
        return weaponName
    if upgrade.type in consts.UPGRADE_TYPE.MODULES:
        return localizeComponents('NAME_MODULE_{0}'.format(upgrade.name))
    if upgrade.type == consts.UPGRADE_TYPE.AIRCRAFT:
        return localizeAirplane(upgrade.name)


def localizeBotChat(label):
    key = '#bot_chat:' + label.upper()
    result = convert(makeString(key))
    if not IS_DEVELOPMENT:
        resultCheck = result.lower()
        if resultCheck == key.lower() or resultCheck == label.lower() or result == '----':
            return ''
    return result


def localizeBattleMessageReaction(label):
    return localizeBotChat(label)


global g_translators ## Warning: Unused global