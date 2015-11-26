# Embedded file name: DamagePanel.py
import BigWorld
import os
import Math
from gui.Scaleform.Battle import Battle
from gui.Scaleform.Battle import DamagePanel
from gui.Scaleform.Battle import VehicleMarkersManager
from gui.WindowsManager import g_windowsManager
from Vehicle import Vehicle
from messenger import MessengerEntry
from items import vehicles
from debug_utils import *
from itertools import izip
from constants import VEHICLE_HIT_EFFECT
version = '[ Damage Panel by GambitER 0.8.11 v.2 ]'
print '           ' + version
Vehicle.__tankHealth = {}
VehicleMarkersManager_showExtendedInfo = VehicleMarkersManager.showExtendedInfo

def add_VehicleMarkersManager_showExtendedInfo(self, value):
    VehicleMarkersManager_showExtendedInfo(self, value)
    g_windowsManager.battleWindow.call('battle.damagePanel.updateKeyStroke', [value])


VehicleMarkersManager.showExtendedInfo = add_VehicleMarkersManager_showExtendedInfo
Vehicle_init = Vehicle.__init__

def add_Vehicle_init(self):
    Vehicle_init(self)
    self.__battleID = 0
    self.__hitType = 0
    self.__compIdx = ''
    self.__splHit = False
    self.__splType = 0


Vehicle.__init__ = add_Vehicle_init
Vehicle_onEnterWorld = Vehicle.onEnterWorld

def add_Vehicle_onEnterWorld(self, prereqs):
    Vehicle_onEnterWorld(self, prereqs)
    player = BigWorld.player()
    for key, vehicle in player.arena.vehicles.iteritems():
        if vehicle['name'] == self.publicInfo.name:
            self.__battleID = key
            break

    if self.__battleID not in self.__tankHealth:
        self.__tankHealth[self.__battleID] = self.typeDescriptor.maxHealth


Vehicle.onEnterWorld = add_Vehicle_onEnterWorld
Vehicle_showDamageFromShot = Vehicle.showDamageFromShot

def add_Vehicle_showDamageFromShot(self, attackerID, points, effectsIndex):
    Vehicle_showDamageFromShot(self, attackerID, points, effectsIndex)
    self.__compIdx = ''
    self.__splHit = False
    if not self.isStarted:
        return
    else:
        self.__hitType = effectsIndex
        descr = self.typeDescriptor
        effectsDescr = vehicles.g_cache.shotEffects[effectsIndex]
        firstHitDir = None
        maxHitEffectCode = None
        hasPiercedHit = False
        for point in points:
            hitEffectCode = int(point & 255)
            self.__compIdx = int(point & 65280) >> 8
            if maxHitEffectCode is None or hitEffectCode > maxHitEffectCode:
                maxHitEffectCode = hitEffectCode
                if not hasPiercedHit:
                    hasPiercedHit = maxHitEffectCode >= VEHICLE_HIT_EFFECT.ARMOR_PIERCED

        if maxHitEffectCode != 3 and self.health > 0:
            DamagePanel_onHealthChanged(self, self.health, attackerID, 4, maxHitEffectCode, self.__compIdx)
        return


Vehicle.showDamageFromShot = add_Vehicle_showDamageFromShot
Vehicle_showDamageFromExplosion = Vehicle.showDamageFromExplosion

def add_Vehicle_showDamageFromExplosion(self, attackerID, center, effectsIndex):
    Vehicle_showDamageFromExplosion(self, attackerID, center, effectsIndex)
    self.__splHit = False
    if not self.isStarted:
        return
    self.__hitType = effectsIndex
    if not self.isAlive():
        return
    self.__splHit = True
    self.__splType = self.__hitType


Vehicle.showDamageFromExplosion = add_Vehicle_showDamageFromExplosion
Vehicle_onHealthChanged = Vehicle.onHealthChanged

def add_Vehicle_onHealthChanged(self, newHealth, attackerID, attackReasonID):
    Vehicle_onHealthChanged(self, newHealth, attackerID, attackReasonID)
    if not self.isStarted:
        return
    self.__tankHealth[self.__battleID] = newHealth
    if self.isPlayer:
        hitReason = 5
        if attackReasonID == 0:
            hitReason = 3
            if self.__splHit:
                if self.__splType == self.__hitType:
                    hitReason = 6
        DamagePanel_onHealthChanged(self, newHealth, attackerID, attackReasonID, hitReason, self.__compIdx if attackReasonID == 0 else '')
    self.__compIdx = ''
    self.__splHit = False


Vehicle.onHealthChanged = add_Vehicle_onHealthChanged

def DamagePanel_onHealthChanged(self, newHealth, attackerID, attackReasonID, hitReason, compName):
    player = BigWorld.player()
    current = player.arena.vehicles.get(self.__battleID)
    attacker = player.arena.vehicles.get(attackerID)
    try:
        if attackerID not in self.__tankHealth:
            self.__tankHealth[attackerID] = self.typeDescriptor.maxHealth
    except Exception:
        if attackerID not in self.__tankHealth:
            self.__tankHealth[attackerID] = 0

    def DamagePanel_calculateReload(vehicle):
        try:
            loader_skill = 126.5
            other_bonus = 1.0
            for item in attacker['vehicleType'].optionalDevices:
                if item is not None and 'improvedVentilation' in item.name:
                    loader_skill = 132.0
                if item is not None and 'TankRammer' in item.name:
                    other_bonus *= 0.9

            return attacker['vehicleType'].gun['reloadTime'] * 0.875 / (0.00375 * loader_skill + 0.5) * other_bonus
        except Exception as err:
            return 0

        return

    def DamagePanel_getShellPrice(nationID, shellID):
        try:
            import ResMgr, nations
            from items import _xml, vehicles
            from constants import ITEM_DEFS_PATH
            price = {}
            xmlPath = ITEM_DEFS_PATH + 'vehicles/' + nations.NAMES[nationID] + '/components/shells.xml'
            for name, subsection in ResMgr.openSection(xmlPath).items():
                if name != 'icons':
                    xmlCtx = (None, xmlPath + '/' + name)
                    if _xml.readInt(xmlCtx, subsection, 'id', 0, 65535) == shellID:
                        price = _xml.readPrice(xmlCtx, subsection, 'price')
                        break

            ResMgr.purge(xmlPath, True)
            return price
        except Exception as err:
            return

        return

    def DamagePanel_updateHealth_Flash(newHealth, defenderID, attackerID, attackReasonID, hitReason, compName):
        player = BigWorld.player()
        current = player.arena.vehicles.get(defenderID)
        attacker = player.arena.vehicles.get(attackerID)
        try:
            attackerName = ''
            attackerName = attacker['name']
        except Exception as err:
            attackerName = ''

        try:
            attackerTeam = 1
            attackerTeam = 0 if player.team == attacker['team'] else 1
        except Exception as err:
            attackerTeam = 1

        try:
            attackerLevel = 0
            attackerLevel = str(attacker['vehicleType'].level)
        except Exception as err:
            attackerLevel = 0

        try:
            attackerVehicle = ''
            attackerVehicle = unicode(attacker['vehicleType'].type.userString, 'utf-8')
        except Exception as err:
            attackerVehicle = ''

        try:
            attackerVehicleShort = ''
            attackerVehicleShort = unicode(attacker['vehicleType'].type.shortUserString, 'utf-8')
        except Exception as err:
            attackerVehicleShort = ''

        try:
            vClass = ''
            tags = set(attacker['vehicleType'].type.tags & vehicles.VEHICLE_CLASS_TAGS)
            vClass = tags.pop() if len(tags) > 0 else ''
        except Exception as err:
            vClass = ''

        try:
            goldShell = 0
            typeShell = ''
            for shell in attacker['vehicleType'].gun['shots']:
                if self.__hitType == shell['shell']['effectsIndex']:
                    price = DamagePanel_getShellPrice(shell['shell']['id'][0], shell['shell']['id'][1])
                    goldShell = 1 if price[1] != 0 else 0
                    typeShell = shell['shell']['kind']
                    break

        except Exception as err:
            goldShell = 0
            typeShell = ''

        try:
            clipSize = 1
            burstSize = 0
            clipSize = attacker['vehicleType'].gun['clip'][0]
            burstSize = attacker['vehicleType'].gun['burst'][0]
        except Exception as err:
            clipSize = 1
            burstSize = 0

        try:
            attackerReloadClip = '0.0'
            if attacker['vehicleType'].gun['clip'][0] != 1:
                attackerReloadClip = '{0:.1f}'.format(attacker['vehicleType'].gun['clip'][1])
        except Exception as err:
            attackerReloadClip = '0.0'

        try:
            attackerReload = '0.0'
            attackerReload = '{0:.1f}'.format(DamagePanel_calculateReload(attacker['vehicleType']))
        except Exception as err:
            attackerReload = '0.0'

        try:
            attackerHealth = 0
            attackerMaxHealth = 0
            attackerMaxHealth = attacker['vehicleType'].maxHealth
            self.__tankHealth[attackerID] = attackerMaxHealth if attackerMaxHealth < self.__tankHealth[attackerID] else self.__tankHealth[attackerID]
            attackerHealth = self.__tankHealth[attackerID]
        except Exception as err:
            attackerHealth = 0
            attackerMaxHealth = 0

        try:
            iconName = ''
            iconName = attacker['vehicleType'].name.replace(':', '-')
        except Exception as err:
            iconName = ''

        g_windowsManager.battleWindow.call('battle.damagePanel.updateHealthAdd', [newHealth,
         current['name'],
         hitReason,
         compName,
         attackReasonID,
         attackerName,
         attackerLevel,
         attackerVehicle,
         attackerVehicleShort,
         vClass,
         goldShell,
         typeShell,
         attackerTeam,
         attackerReload,
         current['vehicleType'].maxHealth,
         attackerHealth,
         attackerMaxHealth,
         iconName,
         attackerReloadClip,
         clipSize,
         burstSize])

    currentVehicleID = player.playerVehicleID
    if hasattr(player.inputHandler.ctrl, 'curVehicleID'):
        vehicleID = player.inputHandler.ctrl.curVehicleID
        if vehicleID is not None:
            currentVehicleID = vehicleID
    if self.__battleID == currentVehicleID:
        DamagePanel_updateHealth_Flash(newHealth, self.__battleID, attackerID, attackReasonID, hitReason, compName)
    return