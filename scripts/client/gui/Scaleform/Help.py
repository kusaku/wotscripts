# Embedded file name: scripts/client/gui/Scaleform/Help.py
import InputMapping
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem
from clientConsts import BATTLE_NAME_BY_TYPE_HUD_LOC_ID, BATTLE_DESC_BY_TYPE_HUD_LOC_ID, INPUT_SYSTEM_PROFILES
from UIHelper import BattleInfo
from debug_utils import LOG_WARNING
from Helpers.i18n import localizeLobby
import Settings, BigWorld
from consts import INPUT_SYSTEM_STATE

class HelpSettingsKeys:
    HUD = 'showHelpOnStart'
    HANGAR = 'showHelpOnStartHangar'
    HUD_ALWAYS = 'showHelpOnStartAlways'
    HANGAR_OBT_INTRO = 'showHangarObtIntro'
    HANGAR_RELEASE_INTRO = 'showHangarReleaseIntro'
    HANGAR_SINGLE_EXP_INTRO = 'showHangarSingleExpIntro'
    HANGAR_GENERAL_TEST_INTRO = 'showHangarGeneralTestIntro'
    HANGAR_PVE_INTRO = 'showHangarPveIntro'


class _HelpKeyVO:

    def __init__(self, id, label, isFireAxis = False, axisSign = 0):
        self.id = id
        self.label = label
        self.isFireAxis = isFireAxis
        self.axisSign = axisSign


class _HelpVO:

    def __init__(self):
        ms = MeasurementSystem()
        self.txtDistance = ms.localizeHUD('ui_meter')
        self.txtSpeed = ms.localizeHUD('ui_speed')
        self.txtAlt = ms.localizeHUD('ui_vario')
        self.intBattleType = -1
        self.txtBattleType = ''
        self.battleDescription = ''
        self.curProfileName = ''


class Help:

    def __init__(self):
        self.__vo = _HelpVO()
        self.__keys = None
        self.__DATA_KEY_CONTROLS = {'keyFire': InputMapping.CMD_PRIMARY_FIRE,
         'keyTightenLeft': InputMapping.CMD_TURN_LEFT,
         'keyTightenRight': InputMapping.CMD_TURN_RIGHT,
         'keyForcing': InputMapping.CMD_INCREASE_FORCE,
         'keyTurnOffEngine': InputMapping.CMD_ENGINE_OFF,
         'keyTiltForward': InputMapping.CMD_PITCH_UP,
         'keyTiltBack': InputMapping.CMD_PITCH_DOWN,
         'keyRollLeft': InputMapping.CMD_ROLL_LEFT,
         'keyRollRight': InputMapping.CMD_ROLL_RIGHT,
         'keyToAttack': InputMapping.CMD_F2_CHAT_COMMAND,
         'keyToBase': InputMapping.CMD_F3_CHAT_COMMAND,
         'keyFollowMe': InputMapping.CMD_F4_CHAT_COMMAND,
         'keySoAccurately': InputMapping.CMD_F5_CHAT_COMMAND,
         'keyNoWay': InputMapping.CMD_F6_CHAT_COMMAND,
         'keyNeedHelp': InputMapping.CMD_F7_CHAT_COMMAND,
         'keyAttack': InputMapping.CMD_F8_CHAT_COMMAND,
         'keyAttack2': InputMapping.CMD_F9_CHAT_COMMAND,
         'keyFlaps': InputMapping.CMD_FLAPS_UP}
        return

    def getData(self):
        """
        @return: _HelpVO , list[_HelpKeyVO]
        """
        self.__vo.intBattleType, self.__vo.txtBattleType, mapName, teamTask, playerTask = BattleInfo().getBattleInfo()
        self.__vo.battleDescription = localizeLobby(BATTLE_DESC_BY_TYPE_HUD_LOC_ID[self.__vo.intBattleType])
        self.__vo.curProfileName = INPUT_SYSTEM_PROFILES[InputMapping.g_instance.currentProfileType]
        keysControls = InputMapping.g_instance.getKeyControlsHelp(self.__DATA_KEY_CONTROLS.values())
        keys = list()
        for key, value in self.__DATA_KEY_CONTROLS.items():
            if value in keysControls:
                keysData = keysControls[value]['keys']
                fireAxisData = keysControls[value]['isFireAxis']
                axisSignData = keysControls[value]['axisSign']
                if not keysData:
                    LOG_WARNING('getData - keysControls is empty', key)
                else:
                    index = 0 if InputMapping.g_instance.currentProfileType in [INPUT_SYSTEM_STATE.MOUSE, INPUT_SYSTEM_STATE.KEYBOARD] else len(keysData) - 1
                    keys.append(_HelpKeyVO(key, keysData[index], fireAxisData[index], axisSignData[index]))
            else:
                LOG_WARNING('getData - CMD ID not in keysControls (key=%s,CMD ID=%s)' % (key, str(value)))

        if InputMapping.g_instance.currentProfileType == INPUT_SYSTEM_STATE.MOUSE:
            keys.append(_HelpKeyVO('keyTurnsPlane', 'SETTINGS_MOUSE'))
        keys.append(_HelpKeyVO('keyExitChat', 'KEY_ESCAPE'))
        keys.append(_HelpKeyVO('keyIntoChat', 'KEY_RETURN'))
        keys.append(_HelpKeyVO('keyMessageToCommand', 'KEY_RETURN'))
        keys.append(_HelpKeyVO('keyMessageToAllPlayers', 'KEY_TAB'))
        return (self.__vo, keys)

    @staticmethod
    def checkShowHelpOnStart(keyID, defValue = True):
        isNeedShowHelp = False
        isNeedShowHelpAlways = False
        res = Settings.g_instance.userPrefs
        if res:
            isNeedShowHelp = res.readBool(keyID, defValue)
            if keyID == HelpSettingsKeys.HUD:
                isNeedShowHelpAlways = res.readBool(HelpSettingsKeys.HUD_ALWAYS, False)
            if isNeedShowHelp:
                res.writeBool(keyID, False)
            BigWorld.savePreferences()
        return isNeedShowHelp or isNeedShowHelpAlways