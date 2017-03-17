# Embedded file name: scripts/client/adapters/IModuleDescriptionAdapter.py
import db
from adapters.DefaultAdapter import DefaultAdapter
from consts import UPGRADE_TYPE, MIN_CALIBER, EFFECTIVE_AGAINST_ARMORED_OBJECTS, COMPONENT_TYPE, UPGRADE_TYPE_TO_COMPONENT_TYPE
from Helpers.i18n import localizeComponents, localizeLobby, localizeAirplane
from gui.Scaleform.LobbyAirplaneHelper import getUpgradeSpecs, getLobbyAirplane, adjustPlaneConfig, getDiffModules
from _airplanesConfigurations_db import airplanesConfigurations, airplanesDefaultConfigurations
from exchangeapi.CommonUtils import splitIDTypeList

class IModuleDescriptionAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        if ob is None:
            return
        else:
            cmpUpgrade = None
            cmpUpgradeID = None
            weaponConfig = None
            slotID = None
            upgrade = None
            upgradeID = None
            plane = None
            _, typeList = splitIDTypeList(kw['idTypeList'])
            if isinstance(ob, list):
                for idx in xrange(0, len(typeList)):
                    if typeList[idx] == 'plane':
                        plane = ob[idx]
                    elif typeList[idx] == 'upgrade':
                        if upgradeID is None:
                            upgrade = ob[idx]
                            upgradeID = kw['idTypeList'][idx][0]
                        else:
                            cmpUpgrade = ob[idx]
                            cmpUpgradeID = kw['idTypeList'][idx][0]
                    elif typeList[idx] == 'weaponConfig':
                        weaponConfig = ob[idx]
                    elif typeList[idx] == 'weaponslot':
                        slotID = ob[idx].id

            else:
                upgrade = ob
            adaptedOb = super(IModuleDescriptionAdapter, self).__call__(account, ob, **kw)
            if upgrade is not None:
                outName, specs, planesSet, shortDescription = getUpgradeSpecs(upgrade, plane.id if plane is not None else None, cmpUpgrade, slotID, weaponConfig)
            elif weaponConfig is None or slotID is None or cmpUpgradeID is None or cmpUpgrade.type not in UPGRADE_TYPE.WEAPON:
                return adaptedOb
            adaptedOb['configComparison'] = []
            adaptedOb['requiredModules'] = []
            dbInstance = db.DBLogic.g_instance
            cmpGlobalID = 0
            if cmpUpgradeID is not None:
                import BWPersonality
                lch = BWPersonality.g_lobbyCarouselHelper
                lobbyAirplane = lch.getCarouselAirplane(plane.id) or getLobbyAirplane(plane.id)
                upgradeName = upgrade.name if upgrade is not None else None
                cmpName = cmpUpgrade.name if cmpUpgrade is not None else None
                if lobbyAirplane is not None:
                    upgrades = [ x['name'] for x in lobbyAirplane.modules.getInstalled() ]
                    weaponList = lobbyAirplane.weapons.getInstalledWeaponsList()
                    if not upgrades:
                        planeConfig = airplanesConfigurations[airplanesDefaultConfigurations[plane.id]]
                        upgrades = planeConfig.modules
                        weaponList = planeConfig.weaponSlots
                    cmpGlobalID, newUpgrades, newWeaponList = adjustPlaneConfig(lobbyAirplane.planeID, upgrades, weaponList, upgradeName, cmpName, slotID, weaponConfig)
                    oldGlobalID = db.DBLogic.createGlobalID(lobbyAirplane.planeID, upgrades, weaponList)
                    requiredModules = getDiffModules(oldGlobalID, cmpGlobalID, upgradeName, (slotID, weaponConfig))
                    for upgradeName in requiredModules:
                        reqUpgrade = dbInstance.getUpgradeByName(upgradeName)
                        name, _, _, _ = getUpgradeSpecs(reqUpgrade, plane.id if plane is not None else None, None, slotID, weaponConfig)
                        adaptedOb['requiredModules'].append(name)

                    cmpLobbyAirplane = lobbyAirplane.previewPreset(newUpgrades, [ {'slot': x[0],
                     'configuration': x[1]} for x in newWeaponList ])
                    comparisonSpecs = cmpLobbyAirplane.getGroupedDescriptionFields(True, lobbyAirplane, cmpGlobalID, False)
                    for el in comparisonSpecs:
                        for i, j in el.__dict__.iteritems():
                            if i != 'main':
                                continue
                            specObj = None
                            if j is not None:
                                specObj = j.__dict__
                            if specObj and specObj['comparisonValue']:
                                adaptedOb['configComparison'].append(specObj)

            if not adaptedOb['configComparison']:
                adaptedOb['configComparison'] = None
            if upgrade is not None:
                gunData = dbInstance.getGunData(upgrade.name)
                if gunData is None:
                    moduleType = localizeComponents(UPGRADE_TYPE.DESCRIPTION_MAP[upgrade.type])
                else:
                    profileName = gunData.gunProfileName.upper()
                    if profileName == 'MACHINEGUN_SMALL':
                        profileName = 'MACHINE_GUN_LOW'
                    else:
                        profileName = profileName.replace('MACHINEGUN_SMALL', 'MACHINE_GUN')
                    profileName = profileName.replace('CANNON_HIGH_VULCAN', 'CANNON_HIGH')
                    moduleType = localizeLobby('{0}_DESCRIPTION'.format(profileName))
                adaptedOb['name'] = '{0} {1}'.format(moduleType, outName)
                adaptedOb['type'] = upgrade.type
                adaptedOb['description'] = shortDescription
                if hasattr(upgrade, 'level'):
                    adaptedOb['level'] = upgrade.level
                else:
                    adaptedOb['level'] = 0
                adaptedOb['specsList'] = [ spec.__dict__ for spec in specs ]
                adaptedOb['airplanesList'] = map(lambda x: localizeAirplane(dbInstance.getAircraftName(x)), filter(lambda x: x in planesSet, dbInstance.getShopPlaneList()))
                adaptedOb['suitablePlaneIDs'] = list(planesSet)
                adaptedOb['icoPath'] = upgrade.typeIconPath
                isArmoredTargetEffective = EFFECTIVE_AGAINST_ARMORED_OBJECTS.NORMAL
                if upgrade.type in [UPGRADE_TYPE.BOMB, UPGRADE_TYPE.ROCKET]:
                    isArmoredTargetEffective = EFFECTIVE_AGAINST_ARMORED_OBJECTS.IS_EFFECTIVE
                if upgrade.type == UPGRADE_TYPE.GUN:
                    isArmoredTargetEffective = EFFECTIVE_AGAINST_ARMORED_OBJECTS.NOT_EFFECTIVE if gunData.caliber < MIN_CALIBER else EFFECTIVE_AGAINST_ARMORED_OBJECTS.LOW_EFFECTIVE
                adaptedOb['armoredTargetEffective'] = isArmoredTargetEffective
                adaptedOb['buyAvailable'] = getattr(upgrade, 'buyAvailable', True)
                if upgrade.type == UPGRADE_TYPE.GUN:
                    compData = gunData
                elif upgrade.type in UPGRADE_TYPE.SHELL:
                    compData = dbInstance.getComponentByName(UPGRADE_TYPE_TO_COMPONENT_TYPE[upgrade.type], upgrade.name)
                elif upgrade.type == UPGRADE_TYPE.TURRET:
                    turret = dbInstance.getTurretData(upgrade.name)
                    compData = dbInstance.getGunData(turret.hangarSimilarGun)
                else:
                    compData = None
                if compData is not None and hasattr(compData, 'tag'):
                    adaptedOb['propsList'] = [ [localizeLobby(x.name), x.type] for x in compData.tag ]
                else:
                    adaptedOb['propsList'] = []
                adaptedOb['cmpGlobalID'] = cmpGlobalID
            else:
                adaptedOb['name'] = ''
                adaptedOb['type'] = -1
                adaptedOb['description'] = ''
                adaptedOb['level'] = 0
                adaptedOb['specsList'] = []
                adaptedOb['airplanesList'] = []
                adaptedOb['suitablePlaneIDs'] = []
                adaptedOb['icoPath'] = ''
                adaptedOb['armoredTargetEffective'] = False
                adaptedOb['buyAvailable'] = False
                adaptedOb['cmpGlobalID'] = 0
            return adaptedOb