# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CrosshairPanelContainerMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.DAAPISimpleContainerMeta import DAAPISimpleContainerMeta

class CrosshairPanelContainerMeta(DAAPISimpleContainerMeta):

    def as_setSettingsS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setSettings(data)

    def as_setScaleS(self, scale):
        if self._isDAAPIInited():
            return self.flashObject.as_setScale(scale)

    def as_setViewS(self, viewId, settingId):
        if self._isDAAPIInited():
            return self.flashObject.as_setView(viewId, settingId)

    def as_recreateDeviceS(self, offsetX, offsetY):
        if self._isDAAPIInited():
            return self.flashObject.as_recreateDevice(offsetX, offsetY)

    def as_setReloadingCounterShownS(self, visible):
        if self._isDAAPIInited():
            return self.flashObject.as_setReloadingCounterShown(visible)

    def as_setReloadingS(self, duration, baseTime, startTime, isReloading):
        if self._isDAAPIInited():
            return self.flashObject.as_setReloading(duration, baseTime, startTime, isReloading)

    def as_setReloadingAsPercentS(self, percent, isReloading):
        if self._isDAAPIInited():
            return self.flashObject.as_setReloadingAsPercent(percent, isReloading)

    def as_setHealthS(self, percent):
        if self._isDAAPIInited():
            return self.flashObject.as_setHealth(percent)

    def as_setAmmoStockS(self, quantity, quantityInClip, isLow, clipState, clipReloaded = False):
        if self._isDAAPIInited():
            return self.flashObject.as_setAmmoStock(quantity, quantityInClip, isLow, clipState, clipReloaded)

    def as_setClipParamsS(self, clipCapacity, burst):
        if self._isDAAPIInited():
            return self.flashObject.as_setClipParams(clipCapacity, burst)

    def as_setDistanceS(self, dist):
        if self._isDAAPIInited():
            return self.flashObject.as_setDistance(dist)

    def as_clearDistanceS(self, immediate):
        if self._isDAAPIInited():
            return self.flashObject.as_clearDistance(immediate)

    def as_updatePlayerInfoS(self, info):
        if self._isDAAPIInited():
            return self.flashObject.as_updatePlayerInfo(info)

    def as_updateAmmoStateS(self, ammoState):
        if self._isDAAPIInited():
            return self.flashObject.as_updateAmmoState(ammoState)

    def as_setZoomS(self, zoomStr):
        if self._isDAAPIInited():
            return self.flashObject.as_setZoom(zoomStr)

    def as_createGunMarkerS(self, viewID, linkage, name):
        if self._isDAAPIInited():
            return self.flashObject.as_createGunMarker(viewID, linkage, name)

    def as_destroyGunMarkerS(self, name):
        if self._isDAAPIInited():
            return self.flashObject.as_destroyGunMarker(name)

    def as_setGunMarkerColorS(self, name, colorName):
        if self._isDAAPIInited():
            return self.flashObject.as_setGunMarkerColor(name, colorName)

    def as_setNetVisibleS(self, mask):
        if self._isDAAPIInited():
            return self.flashObject.as_setNetVisible(mask)

    def as_setNetTypeS(self, netType):
        if self._isDAAPIInited():
            return self.flashObject.as_setNetType(netType)

    def as_showHintS(self, key, messageLeft, messageRight, offsetX, offsetY):
        if self._isDAAPIInited():
            return self.flashObject.as_showHint(key, messageLeft, messageRight, offsetX, offsetY)

    def as_hideHintS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideHint()