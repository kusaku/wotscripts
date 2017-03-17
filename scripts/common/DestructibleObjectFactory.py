# Embedded file name: scripts/common/DestructibleObjectFactory.py
import BigWorld
from modelManipulator.ModelManipulator3 import ModelManipulator3
from Weapons import Weapons
from ShellController import ShellController
from EntityHelpers import buildAndGetWeaponsInfo, filterPivots
from db.DBParts import buildPartsMapByPartName
from ClientTurretLogic import ClientTurretLogic
import db.DBLogic

class DestructibleObjectFactory:

    @staticmethod
    def createControllers(objID, settingsRoot, logicSettings, partTypes, partStates, weaponsSlot = None, owner = None, fullLoading = True, callback = None, turretName = '', camouflage = None, decals = None, bodyType = None):
        """
        create Weapons, ShellController and ModelManipulator controllers
        @param objID:
        @param settingsRoot: object settings (result of db.DBLogic.g_instance.getAircraftData() for Avatar for example)
        @param logicSettings: same with settingsRoot for TeamObjects but settingsRoot.airplane for Avatars
        @param partTypes:
        @param partStates:
        @param weaponsSlot: must be set for objects with MainWeaponController - like Avatar
        @return created controllers dictionary
        """
        player = BigWorld.player()
        isPlayer = player and objID == player.id
        controllersData = {'settings': settingsRoot,
         'copyFromAvatarID': 0,
         'avatarID': objID}
        weaponsSettings = hasattr(settingsRoot, 'components') and settingsRoot.components.weapons2 or None
        weapons = None
        gunsData = []
        shelsData = dict()
        weaponSoundID = None
        turretSoundID = None
        if weaponsSettings:
            if weaponsSlot is not None:
                if hasattr(BigWorld.player(), 'globalID'):
                    data = settingsRoot.airplane.flightModel.weaponSlot
                    mainWeaponsInfo = buildAndGetWeaponsInfo(weaponsSettings, weaponsSlot, data)
                else:
                    mainWeaponsInfo = buildAndGetWeaponsInfo(weaponsSettings, weaponsSlot)
                pivots = filterPivots(settingsRoot.pivots, partTypes, weaponsSlot)
                beltsMap = None
                if isPlayer and player.__class__.__name__ == 'PlayerAvatar':
                    beltsMap = dict(((record['key'], record['value']) for record in player.ammoBelts))
                weapons = Weapons(None, mainWeaponsInfo, settingsRoot, pivots, beltsMap)
                controllersData['weapons'] = weapons
                weaponSoundID = []
                for group in weapons.guns.groups:
                    weaponSoundID.append(group.gunProfile.sounds.weaponSoundID)

                controllersData['shellController'] = ShellController(owner, mainWeaponsInfo, pivots)
                shelsData = controllersData['shellController'].getShelsModels()
                gunsData = [ (gun.flamePath,
                 group.gunProfile.bulletShot,
                 gun.uniqueId,
                 gun.shellPath,
                 getattr(group.gunDescription, 'bulletShell', '')) for group in weapons.getGunGroups() for gun in group.guns ]
        if turretName and db.DBLogic.g_instance.getTurretData(turretName) is not None:
            gunnersPartsMap = buildPartsMapByPartName('Gunner', logicSettings.partsSettings, partTypes)
            if gunnersPartsMap:
                gunnersParts = dict(((partID, (True, partType)) for partID, partType in gunnersPartsMap.items()))
                turrets = ClientTurretLogic(owner, gunnersParts, turretName)
                controllersData['turretsLogic'] = turrets
                profile = db.DBLogic.g_instance.getGunProfileData(turrets.gunDescription.gunProfileName)
                for gunner in turrets.gunners.values():
                    if turrets.settings.flamePathes:
                        for i, flamePath in enumerate(turrets.settings.flamePathes):
                            path = flamePath
                            shellPath = turrets.settings.shellPathes[i] if turrets.settings.shellPathes and i < len(turrets.settings.shellPathes) else ''
                            gunsData.append((path,
                             profile.bulletShot[0],
                             gunner.gun.uniqueId + i,
                             shellPath,
                             profile.bulletShell))

                turretSoundID = []
                for group in turrets.gunners.values():
                    profile = db.DBLogic.g_instance.getGunProfileData(group.ammoBelt.gunDescription.gunProfileName)
                    turretSoundID.append(profile.sounds.weaponSoundID)

        modelManipulator = ModelManipulator3(isPlayer, objID, logicSettings, partTypes, partStates, gunsData, shelsData, weaponsSettings, weaponsSlot, fullLoading, callback, 0, weaponSoundID, turretSoundID, camouflage=camouflage, decals=decals, bodyType=bodyType)
        controllersData['modelManipulator'] = modelManipulator
        return controllersData