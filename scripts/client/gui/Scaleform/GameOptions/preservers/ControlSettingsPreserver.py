# Embedded file name: scripts/client/gui/Scaleform/GameOptions/preservers/ControlSettingsPreserver.py
__author__ = 's_karchavets'
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_CURRENT_EXCEPTION
from gui.Scaleform.GameOptions.utils import BasePreserver, parseBracket
from gui.Scaleform.GameOptions.utils import MOUSE_TIGHTENING_KEYS, MOUSE_INTENSITY_SPLINE_KEY
import InputMapping
from clientConsts import INPUT_SYSTEM_PROFILES_REV
from consts import INPUT_SYSTEM_PROFILES_LIST_REVERT, INPUT_SYSTEM_STATE
import Settings
import Math
import config_consts

class ControlBasePreserver(BasePreserver):

    def __init__(self, profileName, primaryKey = None):
        self._profileName = profileName
        self._primaryKey = primaryKey

    @property
    def keyboard(self):
        return InputMapping.g_instance.getKeyboardFromProfile(self._profileName, 'current')

    @property
    def primary(self):
        return InputMapping.g_instance.getPrimaryFromProfile(self._profileName, 'current')


class ProfilePresetPreserver(ControlBasePreserver):

    def save(self, value):
        newPresetName = Settings.g_instance.inputProfilesPresets[self._profileName][value]['name']
        Settings.g_instance.inputProfilesPresetsCurrent[self._profileName] = newPresetName
        InputMapping.g_instance.updateProfilesPresets(Settings.g_instance.inputProfilesPresetsCurrent)


class ControlProfilesPreserver(BasePreserver):

    def save(self, value):
        profileID = InputMapping.g_instance.currentProfileType
        try:
            profileID = INPUT_SYSTEM_PROFILES_REV[value.data[value.index].key]
        except:
            LOG_ERROR('save', value.index, value.data, INPUT_SYSTEM_PROFILES_REV)
            LOG_CURRENT_EXCEPTION()

        InputMapping.g_instance.setCurProfileName(INPUT_SYSTEM_PROFILES_LIST_REVERT[profileID])


class ActiveFastFMPreserver(BasePreserver):

    def save(self, value):
        Settings.g_instance.setGameUIValue('fastFM', value)


class PrimaryPreserver(ControlBasePreserver):

    def save(self, value):
        if hasattr(self.primary, self._primaryKey):
            setattr(self.primary, self._primaryKey, value)
            if value is None:
                LOG_ERROR('save - value is None', self._profileName, self._primaryKey, value)
                if config_consts.IS_DEVELOPMENT:
                    import traceback
                    traceback.print_stack()
        else:
            LOG_ERROR('save - bad key', self._primaryKey, value)
        return


class MethodOfMixingPreserver(ControlBasePreserver):

    def save(self, value):
        self.primary.METHOD_OF_MIXING = value


class MousePointsPreserver(ControlBasePreserver):

    def save(self, value):
        spline = getattr(self.primary, MOUSE_INTENSITY_SPLINE_KEY)
        splinePointsList = list(spline.p)
        splinePointsList[MOUSE_TIGHTENING_KEYS.index(self._primaryKey)] = Math.Vector2(value.x, value.y)
        spline.p = tuple(splinePointsList)
        spline.refresh()


class JoystickPointsPreserver(ControlBasePreserver):

    def save(self, value):
        spline = getattr(self.primary, self._primaryKey)
        spline.setPoints(tuple((Math.Vector2(el) for el in value)))


class InputCommandPreserver(ControlBasePreserver):

    def save(self, value):
        for groupControlVO in value:
            for commandVO in groupControlVO.controls:
                self.__applyNewMappingForCommand(commandVO)

    def __applyNewMappingForCommand(self, commandVO):
        command = self.keyboard.getCommand(commandVO.id)
        mapping = dict(keyNames=[ dict(name=buttonEntryVO.id, device=long(buttonEntryVO.deviceId)) for buttonEntryVO in commandVO.buttons ], switchingStyle=commandVO.switchingStyle, fireAxisIndex=commandVO.axes.axisId, fireAxisDevice=long(commandVO.axes.axisDeviceId), fireAxisSign=commandVO.axes.sign)
        if len(command.linkedAxisName) > 0:
            mapping.update({'linkedAxisIndex': commandVO.axes.axisId,
             'linkedAxisDevice': long(commandVO.axes.axisDeviceId),
             'linkedAxisInverted': commandVO.axes.axisInverted,
             'linkedAxisSensitivity': commandVO.axes.axisSensitivity,
             'linkedAxisDeadZone': commandVO.axes.axisDeadzone,
             'linkedAxisSmoothWindow': commandVO.axes.axisSmoothing})
        self.keyboard.changeCommandData(commandVO.id, mapping, self.primary)