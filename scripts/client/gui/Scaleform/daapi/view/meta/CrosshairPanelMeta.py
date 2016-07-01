# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CrosshairPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class CrosshairPanelMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def as_populateS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_populate()

    def as_disposeS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_dispose()

    def as_setSettingsS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSettings(data)

    def as_setViewS(self, view):
        """
        :param view:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setView(view)

    def as_recreateDeviceS(self, offsetX, offsetY):
        """
        :param offsetX:
        :param offsetY:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_recreateDevice(offsetX, offsetY)

    def as_setReloadingCounterShownS(self, visible):
        """
        :param visible:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setReloadingCounterShown(visible)

    def as_setReloadingS(self, duration, baseTime, startTime, isReloading):
        """
        :param duration:
        :param baseTime:
        :param startTime:
        :param isReloading:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setReloading(duration, baseTime, startTime, isReloading)

    def as_setReloadingAsPercentS(self, percent, isReloading):
        """
        :param percent:
        :param isReloading:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setReloadingAsPercent(percent, isReloading)

    def as_setHealthS(self, percent):
        """
        :param percent:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHealth(percent)

    def as_setAmmoStockS(self, quantity, quantityInClip, isLow, clipState, clipReloaded):
        """
        :param quantity:
        :param quantityInClip:
        :param isLow:
        :param clipState:
        :param clipReloaded:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAmmoStock(quantity, quantityInClip, isLow, clipState, clipReloaded)

    def as_setClipParamsS(self, clipCapacity, burst):
        """
        :param clipCapacity:
        :param burst:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setClipParams(clipCapacity, burst)

    def as_setDistanceS(self, dist):
        """
        :param dist:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setDistance(dist)

    def as_clearDistanceS(self, immediate):
        """
        :param immediate:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_clearDistance(immediate)

    def as_updatePlayerInfoS(self, info):
        """
        :param info:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updatePlayerInfo(info)

    def as_updateAmmoStateS(self, ammoState):
        """
        :param ammoState:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateAmmoState(ammoState)

    def as_setZoomS(self, zoomStr):
        """
        :param zoomStr:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setZoom(zoomStr)