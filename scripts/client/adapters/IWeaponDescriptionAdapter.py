# Embedded file name: scripts/client/adapters/IWeaponDescriptionAdapter.py
from Helpers.i18n import localizeComponents, localizeLobby
from adapters.DefaultAdapter import DefaultAdapter
from consts import UPGRADE_TYPE
import db.DBLogic
from gui.Scaleform.LobbyAirplaneHelper import getShellDescription
from exchangeapi.CommonUtils import splitIDTypeList
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem
from debug_utils import LOG_ERROR
import consts

class IWeaponDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        _, typeList = splitIDTypeList(kw['idTypeList'])
        weapon = None
        measurementSystem = None
        if isinstance(ob, list):
            for idx in xrange(0, len(typeList)):
                if typeList[idx] == 'measurementSystem':
                    measurementSystem = MeasurementSystem(ob[idx])
                else:
                    weapon = ob[idx]

        else:
            weapon = ob
        adaptedOB = super(IWeaponDescriptionAdapter, self).__call__(account, weapon, **kw)
        if weapon is None:
            LOG_ERROR('IWeaponDescriptionAdapter: weapon not found', ob, kw)
            return adaptedOB
        else:
            adaptedOB['name'] = localizeComponents('WEAPON_NAME_%s' % weapon.name)
            if kw['weaponType'] in UPGRADE_TYPE.SHELL:
                adaptedOB['iconPathSmall'] = weapon.iconPathSmall
            else:
                adaptedOB['iconPathSmall'] = ''
            dbInstance = db.DBLogic.g_instance
            adaptedOB['caliber'] = weapon.caliber
            upgrade = dbInstance.upgrades.get(weapon.name, None)
            if upgrade is not None:
                adaptedOB['iconPath'] = upgrade.typeIconPath
                adaptedOB['upgradeID'] = upgrade.id
                adaptedOB['suitablePlaneIDs'] = dbInstance.getSuitablePlanesForUpgrade(upgrade)
                if adaptedOB['suitablePlaneIDs']:
                    if dbInstance.isPlanePremium(adaptedOB['suitablePlaneIDs'][0]):
                        adaptedOB['name'] = '{0} {1}'.format(adaptedOB['name'], localizeComponents('WEAPON_NAME_GOLDBELT'))
                if upgrade.type == UPGRADE_TYPE.ROCKET or upgrade.type == UPGRADE_TYPE.BOMB:
                    adaptedOB['description'] = '\n'.join([ '{0} {1}{2} '.format(x.name, x.value, x.unit) for x in getShellDescription(weapon, measurementSystem) ])
                    adaptedOB['shortDescription'] = '{0} {1}'.format(localizeLobby('LOBBY_MAINTENANCE_MODULE_PARAMETER_DAMAGE'), weapon.explosionDamage)
                else:
                    adaptedOB['description'] = ''
                    adaptedOB['shortDescription'] = ''
                adaptedOB['buyAvailable'] = getattr(upgrade, 'buyAvailable', True)
                if upgrade.type == UPGRADE_TYPE.GUN:
                    gunData = dbInstance.getGunData(upgrade.name)
                    adaptedOB['maxDistance'] = round(measurementSystem.getMeters(gunData.bulletFlyDist / consts.WORLD_SCALING))
                else:
                    adaptedOB['maxDistance'] = 0
            return adaptedOB


class IGunDescriptionAdapter(IWeaponDescriptionAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IGunDescriptionAdapter, self).__call__(account, ob, weaponType=UPGRADE_TYPE.GUN, **kw)
        return adaptedOB


class IBombDescriptionAdapter(IWeaponDescriptionAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IBombDescriptionAdapter, self).__call__(account, ob, weaponType=UPGRADE_TYPE.BOMB, **kw)
        adaptedOB['caliber'] = localizeComponents('WEAPON_NAME_' + adaptedOB['caliber'])
        return adaptedOB


class IRocketDescriptionAdapter(IWeaponDescriptionAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IRocketDescriptionAdapter, self).__call__(account, ob, weaponType=UPGRADE_TYPE.ROCKET, **kw)
        adaptedOB['caliber'] = localizeComponents('WEAPON_NAME_' + adaptedOB['caliber'])
        return adaptedOB