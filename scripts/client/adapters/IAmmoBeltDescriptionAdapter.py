# Embedded file name: scripts/client/adapters/IAmmoBeltDescriptionAdapter.py
from Helpers.i18n import localizeComponents, localizeLobby, localizeTooltips
from adapters.DefaultAdapter import DefaultAdapter
from exchangeapi.Connectors import getObject
from _weapons import AVAILABLE_BELTS_BY_PLANE_TYPE
from HelperFunctions import wowpRound
import _economics
from consts import AMMOBELT_SPECS
_BELT_TYPE_DESCRIPTION = {'standartbelt': '',
 'armourpiercingbelt': 'TOOLTIP_ARMOURPIERCINGBELT_EFF_ALL_WEP',
 'ap_incinerating': 'TOOLTIP_AP-INCINERATINGBELT_EFF_RAPID-FIRE_WEP',
 'armourpiercingbelt2': 'TOOLTIP_FRAGBELT_EFF_BIG_WEP',
 'fugasbelt': 'TOOLTIP_GENERALPURPOSEBELT_EFF_ALL_WEP'}

class IAmmoBeltDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, o, **kw):
        ob = getObject(kw['idTypeList'])
        adaptedOB = super(IAmmoBeltDescriptionAdapter, self).__call__(account, ob, **kw)
        from db.DBLogic import g_instance as db_instance
        guns = db_instance.getBeltSuitableGuns(ob.id)
        planes = []
        globalMaxDamage = maxFireChance = 0
        globalMinDamage = minFireChance = 100000000
        gunNames = []
        gunUpgradeIds = []
        for gun in guns:
            upgrade = db_instance.upgrades.get(gun.name, None)
            if upgrade is None:
                continue
            for upgradeVariant in upgrade.variant:
                planeID = db_instance.getAircraftIDbyName(upgradeVariant.aircraftName)
                planeData = db_instance.getAircraftData(planeID)
                availableAmmoTypes = AVAILABLE_BELTS_BY_PLANE_TYPE[planeData.airplane.planeType]
                if ob.ammo[0] in availableAmmoTypes and planeID not in planes:
                    planes.append(planeID)

            minDamage, maxDamage = db_instance.calculateBeltMinMaxDamage(gun, ob)
            globalMaxDamage = max(maxDamage, globalMaxDamage)
            globalMinDamage = min(minDamage, globalMinDamage)
            fireChance, _ = db_instance.calculateBeltSpec(gun, ob, AMMOBELT_SPECS.FIRE_CHANCE)
            maxFireChance = max(fireChance, maxFireChance)
            minFireChance = min(fireChance, minFireChance)
            gunNames.append(localizeComponents('WEAPON_NAME_' + gun.weapName))
            gunUpgradeIds.append(upgrade.id)

        globalMinDamage = wowpRound(globalMinDamage, 2)
        globalMaxDamage = wowpRound(globalMaxDamage, 2)
        minFireChance = wowpRound(minFireChance, 3)
        maxFireChance = wowpRound(maxFireChance, 3)
        strDamage = str(globalMinDamage) if globalMinDamage == globalMaxDamage else '{0}-{1}'.format(globalMinDamage, globalMaxDamage)
        if maxFireChance > 0:
            strFireChance = '{0}%'.format(minFireChance * 100) if minFireChance == maxFireChance else '{0}-{1}%'.format(minFireChance, maxFireChance)
        else:
            strFireChance = ''
        if guns:
            adaptedOB['caliber'] = wowpRound(guns[0].caliber, 2)
        else:
            adaptedOB['caliber'] = 0.0
        adaptedOB['suitableGunIDs'] = gunUpgradeIds
        adaptedOB['suitablePlaneIDs'] = planes
        adaptedOB['name'] = localizeComponents('WEAPON_NAME_' + ob.ui_name)
        adaptedOB['beltType'] = ob.beltType
        adaptedOB['icoPathSmall'] = ob.hudIcoPath
        adaptedOB['globalMaxDamage'] = globalMaxDamage
        adaptedOB['globalMinDamage'] = globalMinDamage
        adaptedOB['globalMaxFireChance'] = maxFireChance
        adaptedOB['globalMinFireChance'] = minFireChance
        adaptedOB['gunNames'] = ', '.join(set(gunNames))
        adaptedOB['shortDescription'] = '{0} {1}'.format(localizeLobby('MODULES_CHARACTERISTICS_DPS'), strDamage)
        adaptedOB['description'] = ''
        if strFireChance:
            adaptedOB['description'] += '\n{0} {1}'.format(localizeLobby('LOBBY_MAINTENANCE_MODULE_PARAMETER_FIRE_CHANSE'), strFireChance)
        adaptedOB['tooltipDescription'] = localizeTooltips(_BELT_TYPE_DESCRIPTION[ob.beltType]) if ob.beltType in _BELT_TYPE_DESCRIPTION else ''
        adaptedOB['buyAvailable'] = getattr(ob, 'buyAvailable', True)
        return adaptedOB