# Embedded file name: scripts/client/InputMapping.py
import inspect
import BigWorld
from Event import Event
import ResMgr
import Keys
import consts
from db.DBHelpers import readValue
from Helpers.i18n import makeString, localizeOptions
from MathExt import *
import math
import threading
from debug_utils import *
from input.ProfileLoader.DummyDeviceLoader import MouseDummy
from input.ProfileLoader.MouseLoader import MouseLoader
from input.ProfileLoader.JoystickLoader import JoystickSettings
from input.ProfileLoader.KeyMapingLoader import Keyboard, prepareLoadMapping
from input.ProfileLoader.GamepadLoader import GamepadProfileLoader
g_instance = None
g_descriptions = None
FORCE_DEFAULT_INPUT_PATH = False
AXES = {'AXIS_LX': Keys.AXIS_LX,
 'AXIS_LY': Keys.AXIS_LY,
 'AXIS_LZ': Keys.AXIS_LZ,
 'AXIS_RX': Keys.AXIS_RX,
 'AXIS_RY': Keys.AXIS_RY,
 'AXIS_RZ': Keys.AXIS_RZ,
 'AXIS_U': Keys.AXIS_U,
 'AXIS_V': Keys.AXIS_V}
MODIFIERS = {'MODIFIER_SHIFT': Keys.MODIFIER_SHIFT,
 'MODIFIER_CTRL': Keys.MODIFIER_CTRL,
 'MODIFIER_ALT': Keys.MODIFIER_ALT}

def initInput(profileName, profilesPresets):
    global g_instance
    global g_descriptions
    g_descriptions = CommandDescriptions()
    g_instance = InputMapping(profileName, profilesPresets)


def translateAxisValue(axisCurve, axisValue):
    return math.copysign(axisCurve.calc(abs(axisValue)), axisValue)


SENSITIVITY_MIN = 0.05
SENSITIVITY_MAX = 2.5
HI_AXIS_BOUND = 0.5
LOW_AXIS_BOUND = 0.3

def convertToRealSensitivity(sliderValue):
    return sliderValue * (SENSITIVITY_MAX - SENSITIVITY_MIN) + SENSITIVITY_MIN


COMMANDS_SKIP_FOR_FIRED_COUNT = []
COMMANDS_TO_REFRESH = []
COMMANDS_TO_NOT_REFRESH = []
CHAT_COMMANDS = []
EQUIPMENT_COMMANDS = []

class CommandDescriptions(object):
    __DATA_PATH = 'scripts/command_mapping_description.xml'

    def __init__(self):
        self.__commands = {}
        rootSection = ResMgr.openSection(self.__DATA_PATH)
        commandIntID = 1
        for commandID, dataSection in rootSection.items():
            if commandID in self.__commands:
                LOG_WARNING('init - command is duplicate', commandID)
            self.__commands[commandID] = CommandDescription(commandIntID)
            self.__commands[commandID].readFromDatasection(dataSection)
            if dataSection.has_key('FIRE_KEYS'):
                self.__commands[commandID].initDefaultMapping(commandID, dataSection)
            globals()[commandID] = commandIntID
            commandIntID += 1

        if consts.IS_DEBUG_IMPORTED:
            from debug.AvatarDebug import DebugCommands
            self.loadMappingFromClass(DebugCommands, commandIntID)
        self.__fillGlobalCommandLists()
        ResMgr.purge(self.__DATA_PATH, True)
        self.defaultMapping = dict([ (self.getCommandIntID(commandName), command.defaultMapping) for commandName, command in self.__commands.iteritems() if command.defaultMapping is not None ])
        return

    def __fillGlobalCommandLists(self):
        global CHAT_COMMANDS
        global COMMANDS_SKIP_FOR_FIRED_COUNT
        global COMMANDS_TO_REFRESH
        global EQUIPMENT_COMMANDS
        global COMMANDS_TO_NOT_REFRESH
        COMMANDS_TO_REFRESH = [CMD_AUTOPILOT]
        COMMANDS_TO_NOT_REFRESH = [CMD_SHOW_TEAMS,
         CMD_INTERMISSION_MENU,
         CMD_VISIBILITY_HUD,
         CMD_SHOW_CURSOR,
         CMD_HELP,
         CMD_SHOW_MAP]
        CHAT_COMMANDS = [CMD_F2_CHAT_COMMAND,
         CMD_F3_CHAT_COMMAND,
         CMD_F4_CHAT_COMMAND,
         CMD_F5_CHAT_COMMAND,
         CMD_F6_CHAT_COMMAND,
         CMD_F7_CHAT_COMMAND,
         CMD_F8_CHAT_COMMAND,
         CMD_F9_CHAT_COMMAND]
        EQUIPMENT_COMMANDS = [CMD_USE_EQUIPMENT_1, CMD_USE_EQUIPMENT_2, CMD_USE_EQUIPMENT_3]
        COMMANDS_SKIP_FOR_FIRED_COUNT = [CMD_PRIMARY_FIRE,
         CMD_SECONDARY_FIRE,
         CMD_FIRE_GROUP_1,
         CMD_FIRE_GROUP_2,
         CMD_FIRE_GROUP_3,
         CMD_WEAPON_GROUP_1,
         CMD_WEAPON_GROUP_2,
         CMD_WEAPON_GROUP_3,
         CMD_WEAPON_GROUP_4,
         CMD_WEAPON_GROUP_ALL]

    def loadMappingFromClass(self, classWithMapping, commandIntID):
        import inspect
        for commandID, value in inspect.getmembers(classWithMapping):
            if commandID.startswith('CMD_'):
                self.__commands[commandID] = CommandDescription(commandIntID, 'DEBUG')
                globals()[commandID] = commandIntID
                commandIntID += 1

    @property
    def commands(self):
        return self.__commands

    def getCommandWaitTime(self, commandName):
        if commandName in self.__commands:
            command = self.__commands[commandName]
            return command.waitTime
        return 0.0

    def getCommandGroupID(self, commandName):
        if commandName in self.__commands:
            command = self.__commands[commandName]
            return command.groupID
        return ''

    def getCommandLocalizationID(self, commandName):
        if commandName in self.__commands:
            command = self.__commands[commandName]
            return command.localizationID
        return ''

    def getLinkedAxisName(self, commandName):
        if commandName in self.__commands:
            command = self.__commands[commandName]
            return command.linkedAxisName
        else:
            return ''

    def getCommandIntID(self, commandName):
        if commandName in self.__commands:
            command = self.__commands[commandName]
            return command.commandID
        return ''

    def getCommandNameByID(self, commandID):
        for commandName, command in self.__commands.items():
            if commandID == command.commandID:
                return (commandName, command.groupName)

        return (None, None)


class COMMAND_DESCRIPTION_TYPES():
    MAIN = 0
    ADDITIONAL = 1


class CommandDescription():

    def __init__(self, commandIntID, groupName = 'MAIN', groupID = 'SETTINGS_BASIC'):
        self.commandID = commandIntID
        self.linkedAxisName = ''
        self.localizationID = ''
        self.groupName = groupName
        self.groupID = groupID
        self.waitTime = 0.0
        self.defaultMapping = None
        self.type = COMMAND_DESCRIPTION_TYPES.ADDITIONAL
        return

    def readFromDatasection(self, dataSection):
        readValue(self, dataSection, 'linkedAxisName', '')
        readValue(self, dataSection, 'localizationID', '')
        readValue(self, dataSection, 'groupName', 'MAIN')
        readValue(self, dataSection, 'groupID', 'SETTINGS_BASIC')
        readValue(self, dataSection, 'waitTime', 0.0)
        readValue(self, dataSection, 'type', COMMAND_DESCRIPTION_TYPES.ADDITIONAL)

    def initDefaultMapping(self, commandName, dataSection):
        fireAxisIndex, fireAxisSign, fireAxisDevice, fireKeyNames, modifier, isBlock, isBase, switchingStyle = prepareLoadMapping(dataSection)
        self.defaultMapping = {'fireAxisIndex': fireAxisIndex,
         'fireAxisSign': fireAxisSign,
         'fireAxisDevice': fireAxisDevice,
         'fireKeyNames': fireKeyNames,
         'modifier': modifier,
         'isBlock': isBlock,
         'isBase': isBase,
         'switchingStyle': switchingStyle,
         'commandName': commandName,
         'linkedAxisName': self.linkedAxisName,
         'type': self.type}


class InputMappingLoader(threading.Thread):

    def __init__(self, threadData, callback):
        threading.Thread.__init__(self)
        self.__threadData = threadData
        self.__callback = callback

    def run(self):
        self.__callback(self.__threadData)


class InputMapping(object):
    __USER_PATH = 'input_mapping/'
    __DATA_PATH = 'scripts/input_mapping/'
    __DEFAULTS = 'defaults/'
    __DEFAULTS_PATH = __DATA_PATH + __DEFAULTS
    __DEFAULT_CONFIG_FILE_NAME = 'mouse_directional'
    __PRIMARY_SETTINGS_LOADERS = {consts.INPUT_SYSTEM_STATE.KEYBOARD: MouseDummy,
     consts.INPUT_SYSTEM_STATE.JOYSTICK: JoystickSettings,
     consts.INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL: GamepadProfileLoader,
     consts.INPUT_SYSTEM_STATE.MOUSE: MouseLoader}

    @property
    def descriptions(self):
        return g_descriptions

    def __init__(self, currentProfileName, profilesPresets):
        self.__profilesPresets = profilesPresets
        self.__profilesNeedResolve = list()
        self.__profileNames = self.loadProfileNames()
        if FORCE_DEFAULT_INPUT_PATH:
            self.__dataPath = self.__DATA_PATH
        else:
            self.__dataPath = self.__USER_PATH
            self.__prepareUserDir(self.__dataPath)
        self.__checkInputFiles(self.__DEFAULTS_PATH, self.__dataPath)
        LOG_INFO('InputMapping::init', currentProfileName, self.__dataPath)
        if currentProfileName not in self.__profileNames:
            if self.__DEFAULT_CONFIG_FILE_NAME in self.__profileNames:
                currentProfileName = self.__DEFAULT_CONFIG_FILE_NAME
            elif self.__profileNames:
                currentProfileName = self.__profileNames[0]
            else:
                LOG_ERROR('InputMapping::__init__ - can"t load current profile name:', currentProfileName)
        self.onDefaultMappingRestored = Event()
        self.onProfileLoaded = Event()
        self.__loadLock = threading.Lock()
        self.__loadInProgressProfile = None
        self.__currentProfileType = consts.INPUT_SYSTEM_PROFILES_LIST.get(currentProfileName, consts.INPUT_SYSTEM_STATE.MOUSE)
        self.__curProfileName = consts.INPUT_SYSTEM_PROFILES_LIST_REVERT[self.__currentProfileType]
        self.__profileObjects = dict(current={}, default={})
        self.__loadAll()
        self.onSaveControls = Event()
        return

    def fini(self):
        self.__profileObjects = None
        return

    def __loadLockAcquire(self):
        self.__loadLock.acquire()

    def __loadLockRelease(self):
        self.__loadLock.release()

    def __getCallbackClient(self):
        return self.__callbackClient

    def __setCallbackClient(self, val):
        self.__callbackClient = val

    callbackClient = property(__getCallbackClient, __setCallbackClient)

    def __restoreDir(self):
        dirNew = os.path.join(BigWorld.getUserDataDirectory(), self.__USER_PATH)
        dirOld = os.path.join(BigWorld.getUserDataDirectory())
        try:
            dirDefaultsOld = dirOld + self.__DEFAULTS
            dirDefaultsNew = dirNew + self.__DEFAULTS
            if os.access(dirDefaultsOld, os.F_OK):
                import shutil
                shutil.rmtree(dirDefaultsNew)
                os.rename(dirDefaultsOld, dirDefaultsNew)
        except OSError:
            LOG_CURRENT_EXCEPTION()

        for profile in self.__profileNames:
            fileName = profile + '.xml'
            fileNameTarget = dirNew + fileName
            fileNameSource = dirOld + fileName
            try:
                if os.access(fileNameSource, os.F_OK):
                    if os.access(fileNameTarget, os.F_OK):
                        os.remove(fileNameTarget)
                    os.rename(fileNameSource, fileNameTarget)
                    LOG_INFO('Restore input mapping: ' + fileName)
            except OSError:
                LOG_CURRENT_EXCEPTION()

    def __prepareUserDir(self, dataPath):
        path = os.path.join(BigWorld.getUserDataDirectory(), dataPath)
        try:
            os.mkdir(path)
        except OSError:
            pass

        self.__restoreDir()

    def __checkInputFiles(self, defaultDataPath, actualDataPath):
        if defaultDataPath == actualDataPath:
            LOG_ERROR('defaultDataPath equals actualDataPath:', defaultDataPath)
        else:
            previousDefaultDataPath = actualDataPath + self.__DEFAULTS
            previousDefaultDataSection = ResMgr.openSection(previousDefaultDataPath)
            if previousDefaultDataSection is None:
                previousDefaultDataSectionBackup = ResMgr.openSection(''.join([self.__DATA_PATH, 'previousDefaultProviders']))
                for fileName in previousDefaultDataSectionBackup.keys():
                    previousDefaultFilePath = ''.join([self.__dataPath, self.__DEFAULTS, fileName])
                    previousDefaultDataSection = ResMgr.openSection(previousDefaultFilePath, True)
                    if previousDefaultDataSection is not None:
                        previousDefaultDataSection.copy(previousDefaultDataSectionBackup[fileName])
                        previousDefaultDataSection.save()

                ResMgr.purge(previousDefaultDataPath)
                previousDefaultDataSection = ResMgr.openSection(previousDefaultDataPath)
            defaultlDataSection = ResMgr.openSection(defaultDataPath)
            if defaultlDataSection == None:
                LOG_ERROR('default data section does not exist')
            else:
                actualDataSection = ResMgr.openSection(actualDataPath)
                if actualDataSection == None:
                    LOG_ERROR('data section must already exist', actualDataPath)
                else:
                    for profile in self.__profileNames:
                        self.__checkInputFile(defaultlDataSection, actualDataSection, previousDefaultDataSection, profile)

        return

    def __checkInputFile(self, defaultlDataSection, actualDataSection, previousDefaultDataSection, profile):
        try:
            fileName = profile + '.xml'
            if not defaultlDataSection.has_key(fileName):
                LOG_ERROR('default data section does not contain file', fileName)
            else:
                defaultProfile = defaultlDataSection[fileName]
                if defaultProfile == None:
                    LOG_ERROR('cannot open default file', fileName)
                elif actualDataSection.has_key(fileName):
                    actualProfile = actualDataSection[fileName]
                    if actualProfile == None:
                        LOG_ERROR('cannot open file', fileName)
                    else:
                        defaultVersion = defaultProfile.readInt('FILE_VERSION', 0)
                        actualVersion = actualProfile.readInt('FILE_VERSION', 0)
                        if actualVersion < defaultVersion:
                            diff = None
                            differ = None
                            if previousDefaultDataSection is not None and previousDefaultDataSection.has_key(fileName):
                                import ProfileDiffer
                                differ = ProfileDiffer.ProfileDiffer(previousDefaultDataSection[fileName], actualProfile)
                                diff = differ.getDiff()
                                self.__profilesNeedResolve.append(profile)
                            actualProfile.copy(defaultProfile)
                            actualProfile.save()
                            if diff is not None:
                                profilePath = ''.join([self.__dataPath, profile, '.xml'])
                                ResMgr.purge(profilePath)
                                differ.applyDiff(diff)
                            if previousDefaultDataSection is not None:
                                previousDefaultProfile = previousDefaultDataSection.createSection(fileName)
                                if previousDefaultProfile is None:
                                    LOG_ERROR('cannot create new section', fileName)
                                else:
                                    previousDefaultProfile.copy(defaultProfile)
                                    previousDefaultProfile.save()
                            LOG_INFO('version mismatch, replaced', fileName, defaultVersion, actualVersion)
                else:
                    actualProfile = actualDataSection.createSection(fileName)
                    if actualProfile is None:
                        LOG_ERROR('cannot create new section', fileName)
                    else:
                        actualProfile.copy(defaultProfile)
                        actualProfile.save()
                        LOG_INFO('created profile from default', fileName)
                    previousDefaultDataPath = ''.join([self.__dataPath, self.__DEFAULTS, fileName])
                    previousDefaultDataSection = ResMgr.openSection(previousDefaultDataPath, True)
                    if previousDefaultDataSection is None:
                        LOG_ERROR('cannot create folder for save current version of default input mapping files')
                    else:
                        previousDefaultDataSection.copy(defaultProfile)
                        previousDefaultDataSection.save()
        except IOError:
            LOG_CURRENT_EXCEPTION()

        return

    def getAllCommandsIds(self):
        commadIds = list()
        for command in g_descriptions.commands.values():
            commadIds.append(command.commandID)

        return commadIds

    def getCommandsButtonsList(self, commandIDsList):
        from input.InputController import UserKeyEvent
        keys = []
        for commandID in commandIDsList:
            keyCodes = self.keyboardSettings.getCommandKeys(commandID)
            if keyCodes and len(keyCodes) > 0:
                keyInfo = keyCodes[0]
                keys.append(UserKeyEvent(keyInfo['code'], keyInfo['device']))

        return keys

    def getAllCommandsButtonsList(self, ignoreCommandIDsList):
        from input.InputController import UserKeyEvent
        keys = []
        for command in g_descriptions.commands.values():
            keyCodes = None
            if command.commandID not in ignoreCommandIDsList:
                keyCodes = self.keyboardSettings.getCommandKeys(command.commandID)
            if keyCodes and len(keyCodes) > 0:
                keyInfo = keyCodes[0]
                keys.append(UserKeyEvent(keyInfo['code'], keyInfo['device']))

        return keys

    def getProfileNames(self):
        return self.__profileNames

    def loadProfileNames(self):
        """
        @return: <list>
        """
        profiles = []
        rootSection = ResMgr.openSection(self.__DEFAULTS_PATH)
        for fileName in rootSection.keys():
            extentionPos = fileName.find('.xml')
            if extentionPos != -1:
                profileName = fileName[0:extentionPos]
                profiles.append(profileName)

        ResMgr.purge(self.__DEFAULTS_PATH, True)
        return profiles

    def getLocalizedProfileNameCaps(self, profileName = None):
        if profileName is None:
            profileName = self.getCurProfileName()
        return localizeOptions('CONTROL_PROFILE_%s_CAPS' % profileName.upper())

    def getLocalizedProfileName(self, profileName = None):
        if profileName is None:
            profileName = self.getCurProfileName()
        return localizeOptions('CONTROL_PROFILE_%s' % profileName.upper())

    def getLocalizedProfileNames(self):
        locProfiles = []
        profiles = self.getProfileNames()
        for profile in profiles:
            locProfiles.append(localizeOptions('CONTROL_PROFILE_' + profile.upper()))

        return locProfiles

    def getProfileNameByIndex(self, index):
        profiles = self.getProfileNames()
        return profiles[index]

    def isCommandKey(self, command, key, keyDevice, axisIndex = -1, axisDevice = 0):
        return self.keyboardSettings.isCommandKey(command, key, keyDevice, axisIndex, axisDevice)

    def isMouseActivateEvent(self, key, event):
        if isinstance(event, BigWorld.KeyEvent):
            return event.wg_isMouseActivateEvent
        return False

    def getSwitchingStyle(self, command):
        return self.keyboardSettings.getSwitchingStyle(command)

    def invertY(self):
        self.keyboardSettings.INVERT_Y = 1 - self.keyboardSettings.INVERT_Y
        self.primarySettings.INVERT_Y = 1 - self.primarySettings.INVERT_Y

    @property
    def primarySettings(self):
        return self.mouseSettings

    @property
    def mouseSettings(self):
        if self.__curProfileName in self.__profilesPresets:
            return self.getPrimaryFromProfile(self.__profilesPresets[self.__curProfileName])
        return self.getPrimaryFromProfile(self.__curProfileName)

    @property
    def joystickSettings(self):
        return self.mouseSettings

    @property
    def keyboardSettings(self):
        if self.__curProfileName.find('mouse_') == -1:
            if self.__curProfileName in self.__profilesPresets:
                return self.getKeyboardFromProfile(self.__profilesPresets[self.__curProfileName])
            return self.getKeyboardFromProfile(self.__curProfileName)
        else:
            return self.getKeyboardFromProfile('mouse_directional')

    def updateProfilesPresets(self, profilesPresets):
        self.__profilesPresets = profilesPresets

    def getPrimaryFromProfile(self, profileName, objectType = 'current'):
        return self.__profileObjects[objectType][profileName]['PRIMARY']

    def getKeyboardFromProfile(self, profileName, objectType = 'current'):
        return self.__profileObjects[objectType][profileName]['KEYBOARD']

    def __saveProfile(self, rootSection, profilePath):
        try:
            rootSection.save()
        except IOError:
            LOG_ERROR("Couldn't save profile: " + profilePath)
        else:
            LOG_DEBUG('Controls saved to ' + profilePath)

        ResMgr.purge(profilePath, True)

    def saveControlls(self, profileNames = None):
        """
        save ALL profiles or profiles in list 'profileNames'
        @param profileNames: <list>
        @return: None
        """
        if self.__loadInProgressProfile:
            LOG_INFO('::saveControlls: Save rejected. Profile %s is loading' % self.__loadInProgressProfile)
            return
        else:
            try:
                self.__loadLockAcquire()
                for profileName in self.__profileNames:
                    if profileNames is not None and profileName not in profileNames:
                        continue
                    profilePath = ''.join([self.__dataPath, profileName, '.xml'])
                    rootSection = ResMgr.openSection(profilePath)
                    primary = self.getPrimaryFromProfile(profileName)
                    if primary is not None:
                        primary.flash(rootSection['PRIMARY'])
                    keyboard = self.getKeyboardFromProfile(profileName)
                    if keyboard is not None:
                        keyboard.flash(rootSection['KEYBOARD'])
                    self.__saveProfile(rootSection, profilePath)

                self.onSaveControls()
            except:
                LOG_CURRENT_EXCEPTION()
            finally:
                self.__loadLockRelease()

            return

    def getCurPresetName(self):
        return self.__profilesPresets.get(self.__curProfileName, self.__curProfileName)

    def getCurProfileName(self):
        return self.__curProfileName

    def setCurProfileName(self, ProfileName):
        LOG_INFO('setCurProfileName - old=(%s), new=(%s)' % (self.__curProfileName, ProfileName))
        self.__curProfileName = ProfileName
        self.__currentProfileType = consts.INPUT_SYSTEM_PROFILES_LIST.get(self.__curProfileName)
        self.onProfileLoaded()

    def getCurProfileIndex(self):
        profiles = self.getProfileNames()
        return profiles.index(self.__curProfileName)

    def getCurCommandsKeys(self):
        return self.keyboardSettings.getCommandsKeys()

    def getCurMapping(self):
        return self.keyboardSettings.getCurMapping(self.joystickSettings)

    def applyNewMappingForCommand(self, commandID, mapping, primary):
        self.keyboardSettings.changeCommandData(commandID, mapping, primary)

    def setKeyboardLining(self, value):
        self.keyboardSettings.setLining(value)

    def getKeyboardLining(self):
        return self.keyboardSettings.getLining()

    def getLocalizedCommandKeysAndAxes(self, commandName):
        """
        Returns list with localized names of keys/axes that correspond to given command or empty list
        @param commandName: command name from command_mapping_description.xml
        @rtype: list
        """
        keysControls = []
        curMapping = self.getCurMapping()
        record = curMapping.get(g_descriptions.getCommandIntID(commandName), None)
        if record is not None:
            for key in record['keyNames']:
                if 'KEY_NONE' != key['name']:
                    keysControls.append(getKeyLocalization(key['name']))

            if not (self.currentProfileType == consts.INPUT_SYSTEM_STATE.KEYBOARD or self.currentProfileType == consts.INPUT_SYSTEM_STATE.MOUSE):
                if record['linkedAxisIndex'] != -1:
                    keysControls.append(getAxisLocalization(record['linkedAxisIndex']))
                if record['fireAxisIndex'] != -1:
                    keysControls.append(getAxisLocalization(record['fireAxisIndex']))
        return keysControls

    def getKeyControlsHelp(self, dataKeysControls):
        keysControls = {}
        curMapping = self.getCurMapping()
        for cmdID, record in curMapping.items():
            cmdLabel = getCommandLocalization(record['cmdName'])
            if cmdLabel is not None and cmdID in dataKeysControls:
                keysControls[cmdID] = {'keys': [],
                 'isFireAxis': [],
                 'axisSign': []}
                for key in record['keyNames']:
                    if 'KEY_NONE' != key['name']:
                        keysControls[cmdID]['keys'].append(key['name'])
                        keysControls[cmdID]['isFireAxis'].append(False)
                        keysControls[cmdID]['axisSign'].append(0)

                if self.currentProfileType != consts.INPUT_SYSTEM_STATE.MOUSE:
                    if record['linkedAxisIndex'] != -1:
                        keysControls[cmdID]['keys'].append('_'.join(['AXIS', str(record['linkedAxisIndex'])]))
                        keysControls[cmdID]['isFireAxis'].append(False)
                        keysControls[cmdID]['axisSign'].append(0)
                    elif record['fireAxisIndex'] != -1:
                        keysControls[cmdID]['keys'].append('_'.join(['AXIS', str(record['fireAxisIndex'])]))
                        keysControls[cmdID]['isFireAxis'].append(True)
                        keysControls[cmdID]['axisSign'].append(record['fireAxisSign'])

        return keysControls

    def __loadAll(self):
        resources = list()
        extraData = dict()
        for profileName in self.__profileNames:
            LOG_DEBUG("Try to load config profile '%s'" % profileName)
            profilePath = self.__dataPath + profileName + '.xml'
            extraData[len(resources)] = {'profileName': profileName,
             'loadFromDefaults': False}
            resources.append(profilePath)
            profilePathDefaullt = self.__DEFAULTS_PATH + profileName + '.xml'
            extraData[len(resources)] = {'profileName': profileName,
             'loadFromDefaults': True}
            resources.append(profilePathDefaullt)

        if resources:
            self.__loadInProgressProfile = extraData
            BigWorld.loadResourceListBG(tuple(resources), self.__profileDataSectionLoaded, 64, extraData)

    def profileLoadInProgress(self):
        return self.__loadInProgressProfile != None

    @property
    def currentProfileType(self):
        return self.__currentProfileType

    def __profileDataSectionLoaded(self, resourceRefs):
        for index, profileData in resourceRefs.extraData.iteritems():
            loadFromDefaults = profileData['loadFromDefaults']
            profileName = profileData['profileName']
            profilePath = resourceRefs.resourceIDs[index]
            LOG_DEBUG("Loading config profile from '%s'" % profilePath, resourceRefs.has_key(profilePath))
            if not resourceRefs.has_key(profilePath):
                LOG_DEBUG("Can't load '%s'" % profilePath)
            else:
                LOG_DEBUG('Profile successfully loaded')
                rootSection = resourceRefs[profilePath]
                if self.__loadInProgressProfile == resourceRefs.extraData:
                    self.__loadLockAcquire()
                    try:
                        s = rootSection.readString('TYPE')
                        try:
                            currentProfileType = consts.INPUT_SYSTEM_STATE.__dict__[s]
                        except KeyError:
                            LOG_DEBUG('Bad profile type - [' + str(s) + '] in ' + profilePath)
                            raise

                        key = 'current' if not loadFromDefaults else 'default'
                        if self.__profileObjects is not None:
                            temporary = dict()
                            self.__profileObjects[key][profileName] = dict()
                            self.__profileObjects[key][profileName]['KEYBOARD'] = Keyboard(rootSection['KEYBOARD'], self.descriptions.defaultMapping)
                            profileLoaderClass = self.__PRIMARY_SETTINGS_LOADERS.get(currentProfileType, None)
                            if profileLoaderClass is not None:
                                self.__profileObjects[key][profileName]['PRIMARY'] = profileLoaderClass(rootSection['PRIMARY'])
                            else:
                                LOG_INFO('::__profileDataSectionLoaded: Profile [%s],ProfileType[%s] ignored as an obsolete loading' % (profilePath, currentProfileType))
                        else:
                            LOG_DEBUG("The input profile hasn't been created, if shutting down this isn't an issue")
                        ResMgr.purge(profilePath, True)
                    except:
                        LOG_CURRENT_EXCEPTION()
                    finally:
                        self.__loadLockRelease()

                else:
                    LOG_INFO('::__profileDataSectionLoaded: Profile [%s] ignored as an obsolete loading' % profilePath)

        self.__loadInProgressProfile = None
        self.__simplifiedConflictResolution()
        self.onProfileLoaded()
        return

    def __simplifiedConflictResolution(self):
        for profile in self.__profilesNeedResolve:
            key_map = dict()
            for command in self.__profileObjects['current'][profile]['KEYBOARD']._Keyboard__commands.values():
                for key in command.getMappedKeyCodes():
                    if key['name'] != 'KEY_NONE':
                        if not key_map.has_key(key['name']):
                            key_map[key['name']] = key
                        elif self.__checkIfThisNewCommand(key['name'], command.id, profile):
                            key['name'] = 'KEY_NONE'
                        else:
                            key_map[key['name']]['name'] = 'KEY_NONE'

    def __checkIfThisNewCommand(self, key_name, command_id, profile):
        for command in self.__profileObjects['default'][profile]['KEYBOARD']._Keyboard__commands.values():
            for key in command.getMappedKeyCodes():
                if key_name == key['name'] and command_id == command.id:
                    return True

        return False


class Command():
    MODIFIERS = {'ALT': lambda : BigWorld.isKeyDown(Keys.KEY_RALT, 0) or BigWorld.isKeyDown(Keys.KEY_LALT, 0),
     'SHIFT': lambda : BigWorld.isKeyDown(Keys.KEY_RSHIFT, 0) or BigWorld.isKeyDown(Keys.KEY_LSHIFT, 0),
     'CTRL': lambda : BigWorld.isKeyDown(Keys.KEY_RCONTROL, 0) or BigWorld.isKeyDown(Keys.KEY_LCONTROL, 0),
     'RALT': lambda : BigWorld.isKeyDown(Keys.KEY_RALT, 0),
     'LALT': lambda : BigWorld.isKeyDown(Keys.KEY_LALT, 0),
     'LCTRL': lambda : BigWorld.isKeyDown(Keys.KEY_LCONTROL, 0),
     'RCTRL': lambda : BigWorld.isKeyDown(Keys.KEY_RCONTROL, 0)}

    def __init__(self, id, linkedAxisName, fireAxisIndex, fireAxisSign, fireAxisDevice, keyNames, modifier, isBlock, isBase, switchingStyle):
        self.id = id
        self.linkedAxisName = linkedAxisName
        self.fireAxisIndex = fireAxisIndex
        self.fireAxisSign = fireAxisSign
        self.fireAxisDevice = fireAxisDevice
        self.__modifierFnc = Command.MODIFIERS.get(modifier, None)
        self.applyNewKeys(keyNames)
        self.isBlock = isBlock
        self.isBase = isBase
        self.switchingStyle = switchingStyle
        self.lastExecuteTime = 0.0
        return

    def checkKey(self, key, keyDevice):
        for keyRecord in self.__keys:
            if key == keyRecord['code'] and (keyDevice == keyRecord['device'] or keyRecord['device'] == 0):
                return keyRecord

        return False

    def checkAxis(self, axisIndex, axisDevice):
        import BWPersonality
        if axisIndex != -1 and self.fireAxisIndex != -1:
            if self.fireAxisDevice == 0 or self.fireAxisDevice == axisDevice:
                return self.fireAxisIndex == axisIndex and axisIndex in BWPersonality.axis[axisDevice]
        return False

    def isModifierActive(self):
        return self.__modifierFnc is None or self.__modifierFnc()

    def isCommandActive(self):
        import BWPersonality
        if self.fireAxisIndex != -1:
            for device, axes in BWPersonality.axis.items():
                if (device == self.fireAxisDevice or self.fireAxisDevice == 0) and self.fireAxisIndex in axes:
                    axisValue = axes[self.fireAxisIndex]
                    if sign(axisValue) == sign(self.fireAxisSign) and abs(axisValue) > HI_AXIS_BOUND:
                        return True

        for key in self.__keys:
            if key['code'] != 0 and BigWorld.isKeyDown(key['code'], key['device']):
                return True

        return False

    def clear(self):
        self.__keys = []

    def flash(self, rootSection):
        rootSection.deleteSection(self.id)
        section = rootSection.createSection(self.id)
        keysSection = section.createSection('FIRE_KEYS')
        for key in self.__keys:
            keySection = keysSection.createSection('FIRE_KEY')
            keySection.writeString('fireKeyName', key['name'])
            keySection.writeInt64('fireKeyDevice', key['device'])

        section.writeInt('fireAxisIndex', self.fireAxisIndex)
        section.writeInt('fireAxisSign', self.fireAxisSign)
        section.writeInt64('fireAxisDevice', self.fireAxisDevice)
        section.writeInt('isBase', self.isBase)
        section.writeInt('switchingStyle', self.switchingStyle)

    def getMappedKeyCodes(self):
        return self.__keys

    def applyNewKeys(self, keyNames):
        """
        Fill 'code'(int keyCode) for all keys in record and drop all last empty keys
        
        keyNames : {'name':str,'device':UINT}
        
        """
        self.__keys = keyNames
        if not self.__keys:
            self.__keys = [{'name': 'KEY_NONE',
              'device': 0,
              'code': getKeyCodeByName('KEY_NONE')}]
        elif len(self.__keys) > 1:
            keyIndex = 0
            lastValidKeyIndex = 0
            for key in self.__keys:
                key['code'] = getKeyCodeByName(key['name'])
                keyIndex += 1
                if key['name'] != 'KEY_NONE':
                    lastValidKeyIndex = keyIndex

            self.__keys = self.__keys[:lastValidKeyIndex]
        else:
            self.__keys[0]['code'] = getKeyCodeByName(self.__keys[0]['name'])


def getKeyNameByCode(keyCode, fromAxis = False):
    if keyCode == 0:
        return 'KEY_NONE'
    if fromAxis:
        for axisName, axisCode in AXES.iteritems():
            if keyCode == axisCode:
                return axisName

    else:
        for k, v in Keys.__dict__.items():
            if v == keyCode and k not in AXES.keys() and k not in MODIFIERS.keys():
                return k

    return 'KEY_NONE'


def getKeyCodeByName(keyName):
    if keyName in Keys.__dict__:
        return int(Keys.__dict__.get(keyName))
    else:
        return 0


def getKeyLocalization(keyName):
    return makeString('#keys:' + keyName)


def getAxisLocalization(axisIndex):
    if axisIndex == -1:
        return ''
    return getKeyLocalization('_'.join(['AXIS', str(axisIndex)]))


def getCommandLocalization(commandName):
    localizationID = g_descriptions.getCommandLocalizationID(commandName)
    if localizationID == '':
        return None
    else:
        return makeString('#options:KEYMAPPING/' + localizationID)
        return None