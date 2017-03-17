# Embedded file name: scripts/client/gui/Scaleform/HUD/EquipmentManager.py
__author__ = 's_karchavets'
import db.DBLogic as DB
from consts import IS_CLIENT, IS_EDITOR
from Helpers.i18n import localizeLobby
import BigWorld
from debug_utils import LOG_DEBUG, LOG_INFO
import InputMapping
from gui.Scaleform.UIHelper import getKeyLocalization
from functools import partial
from audio import GameSound

class _CustomObject:

    def __init__(self, **kargs):
        for k, v in kargs.items():
            setattr(self, k, v)


class EquipmentManager(object):

    def __init__(self, useCheckFunction):
        self.__uiOwner = None
        self.__isEquipmentInited = False
        self.__tickSoundLocked = False
        self.__equipmentCharges = {}
        self.__noEquipmentSounds = set()
        self.__useCheckFunction = useCheckFunction
        return

    def init(self, uiOwner):
        self.__uiOwner = uiOwner

    def destroy(self):
        self.__uiOwner = None
        self.__useCheckFunction = None
        return

    def __initEquipment(self, consumables):
        """
        @param consumables: list
        """
        equipment = list()
        equipmentCommands = InputMapping.EQUIPMENT_COMMANDS
        for index, consumableData in enumerate(consumables):
            key = consumableData['key']
            equipmentObject = _CustomObject(isEmpty=bool(key == -1))
            if key != -1:
                consumable = DB.g_instance.getConsumableByID(key)
                equipmentObject.icoPath = consumable.icoPath
                equipmentObject.icoPathBig = consumable.icoPathBig
                equipmentObject.description = localizeLobby('LOBBY_CONSUMABLES_DESCRIPTION_SHORT_%s' % consumable.localizeTag)
                equipmentObject.chargesCount = consumableData['chargesCount']
                equipmentObject.coolDownTill = consumableData['coolDownTill']
                equipmentObject.activeTill = consumableData['activeTill']
                affectModules = getattr(consumable, 'affectedModules', None)
                if affectModules is not None:
                    equipmentObject.affectModules = affectModules.module
                    equipmentObject.isAnimationEquipment = affectModules.isAnimationEquipment
                    LOG_INFO('--affectedModulePY:', str(affectModules.module))
                equipmentObject.behaviour = consumable.behaviour
                equipmentObject.coolDownTillMax = consumable.coolDownTime
                equipmentObject.activeTillMax = consumable.effectTime
                equipmentObject.keyName = getKeyLocalization(equipmentCommands[index])
                self.__equipmentCharges[key] = equipmentObject.chargesCount
            equipment.append(equipmentObject)

        if equipment:
            self.__uiOwner.call_1('hud.initEquipment', equipment)
        return

    def __updateEquipment(self, consumables):
        """
        @param consumables: list
        """
        LOG_DEBUG('updateEquipment', consumables)
        equipment = list()
        for consumableData in consumables:
            key = consumableData['key']
            equipmentObject = _CustomObject(isEmpty=bool(key == -1))
            if key != -1:
                equipmentObject.chargesCount = consumableData['chargesCount']
                equipmentObject.coolDownTill = consumableData['coolDownTill']
                if consumableData['coolDownTill'] > 0.0:
                    equipmentObject.coolDownTill = consumableData['coolDownTill'] - BigWorld.serverTime()
                equipmentObject.activeTill = consumableData['activeTill']
                if consumableData['activeTill'] > 0.0:
                    equipmentObject.activeTill = consumableData['activeTill'] - BigWorld.serverTime()
                lastCount = self.__equipmentCharges.get(key)
                if lastCount and lastCount > equipmentObject.chargesCount:
                    self.__equipmentCharges[key] = equipmentObject.chargesCount
                    self.__playUseEquipmentSounds(key)
            equipment.append(equipmentObject)

        if equipment:
            self.__uiOwner.call_1('hud.updateEquipment', equipment)

    def updateEquipmentInputMapping(self, consumables):
        """
        @param consumables: list
        """
        LOG_DEBUG('updateEquipmentInputMapping', consumables)
        equipment = list()
        for index, consumableData in enumerate(consumables):
            key = consumableData['key']
            equipmentObject = _CustomObject(isEmpty=bool(key == -1))
            if key != -1:
                equipmentObject.keyName = getKeyLocalization(InputMapping.EQUIPMENT_COMMANDS[index])
            equipment.append(equipmentObject)

        if equipment:
            self.__uiOwner.call_1('hud.updateEquipment', equipment)

    def updateConsumables(self, consumables):
        """
        key = -1 - unused equipment
        @param consumables: list = [{'key':125, 'chargesCount':10, 'coolDownTill': -1, 'activeTill': -1}]
        """
        LOG_DEBUG('updateConsumables', consumables)
        if self.__uiOwner is None:
            return
        else:
            self.__checkNoEquipmentSound(consumables)
            if self.__isEquipmentInited:
                self.__updateEquipment(consumables)
            else:
                self.__isEquipmentInited = True
                self.__initEquipment(consumables)
            return

    def useEquipment(self, command):
        """
        call from keyboard
        @param command:
        """
        equipmentCommands = InputMapping.EQUIPMENT_COMMANDS
        if command in equipmentCommands:
            self.__prepareForUseEquipment(equipmentCommands.index(command))

    def onUseEquipment(self, slotID):
        """
        call from flash
        @param slotID: int
        """
        self.__prepareForUseEquipment(slotID)

    def __prepareForUseEquipment(self, slotID):
        owner = BigWorld.player()
        consumable = owner.consumables[slotID]
        if consumable['key'] != -1 and int(consumable['chargesCount']) > 0:
            if self.__isEnabled(consumable['key']):
                LOG_INFO('requestUseEquipment', slotID)
                if int(consumable['coolDownTill']) <= 0:
                    self.__uiOwner.call_1('hud.useEquipment', slotID)
                else:
                    self.__playNoEquipmentSound(slotID)
                BigWorld.player().cell.useConsumable(slotID, -1)
        else:
            self.__playNoEquipmentSound(slotID)

    def __checkNoEquipmentSound(self, consumables):
        for slotID, consumable in enumerate(consumables):
            if slotID in self.__noEquipmentSounds and consumable['key'] != -1 and int(consumable['chargesCount']) > 0 and int(consumable['coolDownTill']) <= 0:
                self.__noEquipmentSounds.remove(slotID)
                LOG_DEBUG('EquipmentManager:__checkNoEquipmentSound - freedom for:', slotID)

    def __playNoEquipmentSound(self, slotID):
        if slotID not in self.__noEquipmentSounds:
            self.__noEquipmentSounds.add(slotID)
            LOG_DEBUG('EquipmentManager:__playNoEquipmentSound - play for:', slotID)
            GameSound().ui.play('HUDNoEquipment')

    def __playUseEquipmentSounds(self, eqKey):
        consumInfo = DB.g_instance.getConsumableByID(eqKey)
        if hasattr(consumInfo, 'soundEffects'):
            sInfo = consumInfo.soundEffects
            GameSound().ui.play(consumInfo.soundEffects.initSound)
            if sInfo.tickSound and sInfo.tickInterval > 0:
                BigWorld.callback(sInfo.tickInterval, partial(self.__onTickSound, False, 0, consumInfo.effectTime, sInfo.tickInterval, sInfo.tickSound, sInfo.finishSound))
            elif sInfo.finishSound:
                BigWorld.callback(consumInfo.effectTime, lambda : GameSound().ui.play(sInfo.finishSound))
        else:
            GameSound().ui.play('HUDUseEquipment')

    def __onTickSound(self, isLocker, timer, effectTime, tickInterval, tickSound, finishSound):
        if self.__uiOwner is None:
            LOG_DEBUG('__onTickSound canceled: hud destroyed')
            return
        else:
            LOG_DEBUG('__onTickSound', isLocker, timer, effectTime, tickInterval, tickSound, finishSound)
            timer += tickInterval
            if timer < effectTime:
                if not self.__tickSoundLocked:
                    self.__tickSoundLocked = True
                    isLocker = True
                if isLocker:
                    GameSound().ui.play(tickSound)
                BigWorld.callback(tickInterval, partial(self.__onTickSound, isLocker, timer, effectTime, tickInterval, tickSound, finishSound))
            else:
                self.__tickSoundLocked = False
                if finishSound:
                    LOG_DEBUG('GameSound().ui.play(finishSound)', finishSound)
                    GameSound().ui.play(finishSound)
            return

    def __isEnabled(self, key):
        if self.__useCheckFunction is not None:
            consumable = DB.g_instance.getConsumableByID(key)
            for mod in consumable.mods:
                if self.__useCheckFunction(mod.type, mod):
                    return True

        return False