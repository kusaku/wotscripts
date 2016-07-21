# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ConsumablesPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ConsumablesPanelMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def onClickedToSlot(self, keyCode):
        """
        :param keyCode:
        :return :
        """
        self._printOverrideError('onClickedToSlot')

    def onPopUpClosed(self):
        """
        :return :
        """
        self._printOverrideError('onPopUpClosed')

    def as_setKeysToSlotsS(self, slots):
        """
        :param slots:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setKeysToSlots(slots)

    def as_setItemQuantityInSlotS(self, idx, quantity):
        """
        :param idx:
        :param quantity:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setItemQuantityInSlot(idx, quantity)

    def as_setItemTimeQuantityInSlotS(self, idx, quantity, timeRemaining, maxTime):
        """
        :param idx:
        :param quantity:
        :param timeRemaining:
        :param maxTime:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setItemTimeQuantityInSlot(idx, quantity, timeRemaining, maxTime)

    def as_setCoolDownTimeS(self, idx, timeRemaining):
        """
        :param idx:
        :param timeRemaining:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCoolDownTime(idx, timeRemaining)

    def as_setCoolDownPosAsPercentS(self, idx, percent):
        """
        :param idx:
        :param percent:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCoolDownPosAsPercent(idx, percent)

    def as_addShellSlotS(self, idx, keyCode, sfKeyCode, quantity, clipCapacity, shellIconPath, noShellIconPath, tooltipText):
        """
        :param idx:
        :param keyCode:
        :param sfKeyCode:
        :param quantity:
        :param clipCapacity:
        :param shellIconPath:
        :param noShellIconPath:
        :param tooltipText:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_addShellSlot(idx, keyCode, sfKeyCode, quantity, clipCapacity, shellIconPath, noShellIconPath, tooltipText)

    def as_setNextShellS(self, idx):
        """
        :param idx:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setNextShell(idx)

    def as_setCurrentShellS(self, idx):
        """
        :param idx:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCurrentShell(idx)

    def as_addEquipmentSlotS(self, idx, keyCode, sfKeyCode, tag, quantity, timeRemaining, iconPath, tooltipText):
        """
        :param idx:
        :param keyCode:
        :param sfKeyCode:
        :param tag:
        :param quantity:
        :param timeRemaining:
        :param iconPath:
        :param tooltipText:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_addEquipmentSlot(idx, keyCode, sfKeyCode, tag, quantity, timeRemaining, iconPath, tooltipText)

    def as_showEquipmentSlotsS(self, show):
        """
        :param show:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showEquipmentSlots(show)

    def as_expandEquipmentSlotS(self, idx, slots):
        """
        :param idx:
        :param slots:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_expandEquipmentSlot(idx, slots)

    def as_collapseEquipmentSlotS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_collapseEquipmentSlot()

    def as_addOptionalDeviceSlotS(self, idx, timeRemaining, iconPath, tooltipText):
        """
        :param idx:
        :param timeRemaining:
        :param iconPath:
        :param tooltipText:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_addOptionalDeviceSlot(idx, timeRemaining, iconPath, tooltipText)

    def as_addOrderSlotS(self, idx, keyCode, sfKeyCode, quantity, iconPath, tooltipText, available, quantityVisible, timeRemaining, maxTime):
        """
        :param idx:
        :param keyCode:
        :param sfKeyCode:
        :param quantity:
        :param iconPath:
        :param tooltipText:
        :param available:
        :param quantityVisible:
        :param timeRemaining:
        :param maxTime:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_addOrderSlot(idx, keyCode, sfKeyCode, quantity, iconPath, tooltipText, available, quantityVisible, timeRemaining, maxTime)

    def as_setOrderAvailableS(self, idx, available):
        """
        :param idx:
        :param available:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setOrderAvailable(idx, available)

    def as_setOrderActivatedS(self, idx):
        """
        :param idx:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setOrderActivated(idx)

    def as_showOrdersSlotsS(self, show):
        """
        :param show:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showOrdersSlots(show)

    def as_isVisibleS(self):
        """
        :return Boolean:
        """
        if self._isDAAPIInited():
            return self.flashObject.as_isVisible()

    def as_resetS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_reset()

    def as_switchToPosmortemS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_switchToPosmortem()

    def as_updateEntityStateS(self, entityName, entityState):
        """
        :param entityName:
        :param entityState:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateEntityState(entityName, entityState)