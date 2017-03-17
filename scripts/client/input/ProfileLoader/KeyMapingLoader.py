# Embedded file name: scripts/client/input/ProfileLoader/KeyMapingLoader.py
import BigWorld
import Keys
from Curve import Curve
import InputMapping
from db.DBHelpers import readValue
from debug_utils import LOG_ERROR
from clientConsts import SWITCH_STYLES_BUTTONS
import consts

class Keyboard:

    def __init__(self, section, defaultMapping):
        self.__commands = {}
        self.__additionalCommands = {}
        self.readDataFromSection(section)
        self.__checkAndAddDefaultMapping(defaultMapping)

    def __checkAndAddDefaultMapping(self, defaultMapping):
        """
        @param defaultMapping: <dict>
        """
        for commandId, cmdData in defaultMapping.iteritems():
            if self.getCommand(commandId) is None:
                container = self.__commands if cmdData['type'] == InputMapping.COMMAND_DESCRIPTION_TYPES.MAIN else self.__additionalCommands
                self.add(container, cmdData['commandName'], cmdData['linkedAxisName'], cmdData['fireAxisIndex'], cmdData['fireAxisSign'], cmdData['fireAxisDevice'], cmdData['fireKeyNames'], cmdData['modifier'], cmdData['isBlock'], cmdData['isBase'], cmdData['switchingStyle'])

        return

    def readDataFromSection(self, section):
        self.readMappingData(section)

    def readMappingData(self, section):
        mappingSection = section['MAPPING']
        self.__loadMapping(mappingSection['MAIN'], self.__commands)
        if consts.IS_DEBUG_IMPORTED:
            from debug.AvatarDebug import DebugCommands
            self.__loadMappingFromClass(DebugCommands, self.__additionalCommands)

    def __loadMappingFromClass(self, mappingClass, container):
        import inspect
        for commandID, keyData in inspect.getmembers(mappingClass):
            if commandID.startswith('CMD_'):
                if not self.add(container, commandID, '', -1, 0, 0, [{'name': keyData[0],
                  'device': 0}], keyData[1], keyData[3], 0, SWITCH_STYLES_BUTTONS.DISABLED):
                    LOG_ERROR('Add debug command: command ' + commandID + ' was not added')

    def setLining(self, value):
        self.ENABLE_LINING = value

    def getLining(self):
        return self.ENABLE_LINING

    def getCurMapping(self, joystickSettings):
        d = {}
        for commandID, command in self.__commands.items():
            keyNames = command.getMappedKeyCodes()[:]
            keyNames.extend([{'name': 'KEY_NONE',
              'device': 0}] * (3 - len(keyNames)))
            linkedAxisIndex = -1
            linkedAxisDevice = 0
            linkedAxisInverted = 0
            linkedAxisSensitivity = 0.1
            linkedAxisDeadZone = 0.0
            linkedAxisSmoothWindow = 0.0
            if command.linkedAxisName != '':
                linkedAxisIndex = getattr(joystickSettings, command.linkedAxisName + '_AXIS')
                linkedAxisDevice = getattr(joystickSettings, command.linkedAxisName + '_DEVICE', 0)
                linkedAxisInverted = getattr(joystickSettings, 'INVERT_' + command.linkedAxisName)
                linkedAxisSensitivity = getattr(joystickSettings, command.linkedAxisName + '_SENSITIVITY')
                linkedAxisDeadZone = getattr(joystickSettings, command.linkedAxisName + '_DEAD_ZONE')
                linkedAxisSmoothWindow = getattr(joystickSettings, command.linkedAxisName + '_SMOOTH_WINDOW', 0.0)
            d[commandID] = {'cmdName': command.id,
             'keyNames': keyNames,
             'linkedAxisName': command.linkedAxisName,
             'linkedAxisIndex': linkedAxisIndex,
             'linkedAxisDevice': linkedAxisDevice,
             'linkedAxisInverted': linkedAxisInverted,
             'linkedAxisSensitivity': linkedAxisSensitivity,
             'linkedAxisDeadZone': linkedAxisDeadZone,
             'fireAxisIndex': command.fireAxisIndex,
             'fireAxisSign': command.fireAxisSign,
             'fireAxisDevice': command.fireAxisDevice,
             'fireAxisDeviceName': BigWorld.getDeviceName(command.fireAxisDevice),
             'linkedAxisDeviceName': BigWorld.getDeviceName(linkedAxisDevice),
             'isBase': command.isBase,
             'switchingStyle': command.switchingStyle,
             'linkedAxisSmoothWindow': linkedAxisSmoothWindow}

        return d

    def getCommandsKeys(self):
        return dict([ (commandID, (command.id, command.switchingStyle, command.getMappedKeyCodes())) for commandID, command in self.__commands.items() ])

    def changeCommandData(self, cmdID, record, container):
        command = self.__commands[cmdID]
        command.applyNewKeys(record['keyNames'])
        command.switchingStyle = record['switchingStyle']
        if len(command.linkedAxisName) > 0:
            setattr(container, command.linkedAxisName + '_AXIS', record['linkedAxisIndex'])
            setattr(container, command.linkedAxisName + '_DEVICE', record['linkedAxisDevice'])
            setattr(container, 'INVERT_' + command.linkedAxisName, record['linkedAxisInverted'])
            setattr(container, command.linkedAxisName + '_SENSITIVITY', record['linkedAxisSensitivity'])
            setattr(container, command.linkedAxisName + '_DEAD_ZONE', record['linkedAxisDeadZone'])
            if record['linkedAxisSmoothWindow'] is not None:
                setattr(container, command.linkedAxisName + '_SMOOTH_WINDOW', record['linkedAxisSmoothWindow'])
        else:
            command.fireAxisIndex = record['fireAxisIndex']
            command.fireAxisDevice = record['fireAxisDevice']
            command.fireAxisSign = record['fireAxisSign']
        return

    def flash(self, section):

        def save(section, commands):
            for command in commands.values():
                command.flash(section)

        save(section['MAPPING']['MAIN'], self.__commands)

    def getSwitchingStyle(self, commandIndex):
        if commandIndex in self.__commands:
            return self.__commands[commandIndex].switchingStyle
        else:
            return None

    def isCommandKey(self, commandIndex, key, keyDevice, axisIndex, axisDevice):
        if commandIndex in self.__commands:
            if axisIndex != -1:
                command = self.__commands[commandIndex]
                return command.checkAxis(axisIndex, axisDevice)
            return self.__commands[commandIndex].checkKey(key, keyDevice)
        if commandIndex in self.__additionalCommands:
            return self.__additionalCommands[commandIndex].checkKey(key, keyDevice)
        return False

    def isDevCommand(self, commandID):
        return commandID in self.__additionalCommands

    def getCommandKeys(self, commandID):
        if commandID in self.__commands:
            return self.__commands[commandID].getMappedKeyCodes()
        if commandID in self.__additionalCommands:
            return self.__additionalCommands[commandID].getMappedKeyCodes()

    def getCommand(self, commandID):
        if commandID in self.__commands:
            return self.__commands[commandID]
        elif commandID in self.__additionalCommands:
            return self.__additionalCommands[commandID]
        else:
            return None

    def add(self, container, commandName, linkedAxisName, fireAxisIndex, fireAxisSign, fireAxisDevice, fireKeyNames, modifier, isBlock, isBase, switchingStyle):
        command = InputMapping.g_descriptions.getCommandIntID(commandName)
        if command is not None:
            container[command] = InputMapping.Command(commandName, linkedAxisName, fireAxisIndex, fireAxisSign, fireAxisDevice, fireKeyNames, modifier, isBlock, isBase, switchingStyle)
            return True
        else:
            return False
            return

    def clear(self):
        self.__clearContainer(self.__commands)
        self.__clearContainer(self.__additionalCommands)

    def __loadMapping(self, section, container):
        for commandName, subsec in section.items():
            fireAxisIndex, fireAxisSign, fireAxisDevice, fireKeyNames, modifier, isBlock, isBase, switchingStyle = prepareLoadMapping(subsec)
            linkedAxisName = InputMapping.g_descriptions.getLinkedAxisName(commandName)
            if not self.add(container, commandName, linkedAxisName, fireAxisIndex, fireAxisSign, fireAxisDevice, fireKeyNames, modifier, isBlock, isBase, switchingStyle):
                LOG_ERROR('<__loadFromSection>: command ' + str(commandName) + ' was not loaded')

    def __clearContainer(self, container):
        for command in container.values():
            command.clear()

        container.clear()


def prepareLoadMapping(subsec):
    fireKeysSection = subsec['FIRE_KEYS']
    fireKeyNames = []
    if fireKeysSection is None:
        fireKeys = subsec.readStrings('fireKey')
        for fireKey in fireKeys:
            fireKeyNames.append({'name': fireKey,
             'device': 0})

    else:
        for fireKeysSection in fireKeysSection.values():
            fireKeyName = fireKeysSection.readString('fireKeyName')
            fireKeyDevice = fireKeysSection.readInt64('fireKeyDevice')
            fireKeyNames.append({'name': fireKeyName,
             'device': fireKeyDevice})

    fireAxisIndex = subsec.readInt('fireAxisIndex', -1)
    fireAxisSign = subsec.readInt('fireAxisSign', 0)
    fireAxisDevice = subsec.readInt64('fireAxisDevice', 0)
    isBase = subsec.readInt('isBase', 1)
    switchingStyle = subsec.readInt('switchingStyle', SWITCH_STYLES_BUTTONS.DISABLED)
    return (fireAxisIndex,
     fireAxisSign,
     fireAxisDevice,
     fireKeyNames,
     '',
     False,
     isBase,
     switchingStyle)