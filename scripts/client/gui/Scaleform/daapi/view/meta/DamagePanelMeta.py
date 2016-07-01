# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/DamagePanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class DamagePanelMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def clickToTankmanIcon(self, entityName):
        """
        :param entityName:
        :return :
        """
        self._printOverrideError('clickToTankmanIcon')

    def clickToDeviceIcon(self, entityName):
        """
        :param entityName:
        :return :
        """
        self._printOverrideError('clickToDeviceIcon')

    def clickToFireIcon(self):
        """
        :return :
        """
        self._printOverrideError('clickToFireIcon')

    def getTooltipData(self, entityName, state):
        """
        :param entityName:
        :param state:
        :return String:
        """
        self._printOverrideError('getTooltipData')

    def as_setPlayerInfoS(self, playerName, clanName, regionName, vehicleTypeName):
        """
        :param playerName:
        :param clanName:
        :param regionName:
        :param vehicleTypeName:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPlayerInfo(playerName, clanName, regionName, vehicleTypeName)

    def as_setupS(self, healthStr, progress, indicatorType, crewLayout, yawLimits, hasTurretRotator, isAutoRotationOn):
        """
        :param healthStr:
        :param progress:
        :param indicatorType:
        :param crewLayout:
        :param yawLimits:
        :param hasTurretRotator:
        :param isAutoRotationOn:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setup(healthStr, progress, indicatorType, crewLayout, yawLimits, hasTurretRotator, isAutoRotationOn)

    def as_updateHealthS(self, healthStr, progress):
        """
        :param healthStr:
        :param progress:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateHealth(healthStr, progress)

    def as_updateSpeedS(self, speed):
        """
        :param speed:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateSpeed(speed)

    def as_setMaxSpeedS(self, maxSpeed):
        """
        :param maxSpeed:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setMaxSpeed(maxSpeed)

    def as_setRpmVibrationS(self, intensity):
        """
        :param intensity:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setRpmVibration(intensity)

    def as_playEngineStartAnimS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_playEngineStartAnim()

    def as_startVehicleStartAnimS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_startVehicleStartAnim()

    def as_finishVehicleStartAnimS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_finishVehicleStartAnim()

    def as_setNormalizedEngineRpmS(self, value):
        """
        :param value:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setNormalizedEngineRpm(value)

    def as_setCruiseModeS(self, mode):
        """
        :param mode:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCruiseMode(mode)

    def as_setAutoRotationS(self, isOn):
        """
        :param isOn:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAutoRotation(isOn)

    def as_updateDeviceStateS(self, deviceName, deviceState):
        """
        :param deviceName:
        :param deviceState:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateDeviceState(deviceName, deviceState)

    def as_updateRepairingDeviceS(self, deviceName, percents, seconds):
        """
        :param deviceName:
        :param percents:
        :param seconds:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateRepairingDevice(deviceName, percents, seconds)

    def as_setVehicleDestroyedS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicleDestroyed()

    def as_setCrewDeactivatedS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCrewDeactivated()

    def as_showS(self, isShow):
        """
        :param isShow:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_show(isShow)

    def as_setFireInVehicleS(self, isInFire):
        """
        :param isInFire:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFireInVehicle(isInFire)

    def as_setStaticDataS(self, fireMsg):
        """
        :param fireMsg:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStaticData(fireMsg)

    def as_resetS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_reset()

    def as_setPlaybackSpeedS(self, value):
        """
        :param value:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPlaybackSpeed(value)