# Embedded file name: scripts/client/input/InputCommandProcessor.py
import BigWorld
import InputMapping
from InputStatsHelper import InputStatsHelper
from Event import Event
from MathExt import sign
from debug_utils import LOG_DEBUG
from clientConsts import SWITCH_STYLES_BUTTONS

class InputCommandProcessor:
    """process all keyboard and axis input and raise command events"""

    class __DeviceMapping:
        """Helper class for device event mapping"""

        def __init__(self):
            self.commandFromKey = dict()
            self.commandFromAxis = dict()

    class __CommandDescriptor:
        """helper class for command event mapping"""

        def __init__(self, commandStats):
            self.changeEvent = Event()
            self.startEvent = Event()
            self.endEvent = Event()
            self.isFired = False
            self.command = None
            self.__predicates = []
            self.__commandStats = commandStats
            self.firedCount = 0
            return

        def addPredicate(self, predicate):
            self.__predicates.append(predicate)

        def removePredicate(self, predicate):
            self.__predicates.remove(predicate)

        def processEvent(self, isFired):
            if all([ predicate() for predicate in self.__predicates ]) or self.isFired and not isFired:
                oldIsFired = self.isFired
                if self.command.switchingStyle == SWITCH_STYLES_BUTTONS.SWITCH:
                    if isFired:
                        self.isFired = not self.isFired
                else:
                    self.isFired = isFired
                if self.isFired != oldIsFired:
                    waitTime = InputMapping.g_descriptions.getCommandWaitTime(self.command.id)
                    if waitTime > 0.0 and self.isFired:
                        if BigWorld.time() - self.command.lastExecuteTime <= waitTime:
                            LOG_DEBUG('processEvent - wait command(%s)... time=%s ' % (self.command.id, str(BigWorld.time() - self.command.lastExecuteTime)))
                            return False
                    self.changeEvent(self.isFired)
                    if self.isFired:
                        self.firedCount += 1
                        self.startEvent()
                        self.__commandStats.logCommandStart(self.command.id)
                    else:
                        self.endEvent()
                        self.__commandStats.logCommandEnd(self.command.id)
                    if waitTime > 0.0 and self.isFired:
                        self.command.lastExecuteTime = BigWorld.time()
                return self.command.isBlock
            return False

    def __init__(self):
        self.__commandDescriptors = dict()
        self.__devices = dict()
        self.__commandsFilterAllowed = None
        self.__commandsFilterForbid = None
        self.__storedAxisDevice = dict()
        self.__commandStats = InputStatsHelper()
        self.filteredCommandEvent = Event()
        self.__fillEventMap()
        return

    def __fillEventMap(self):
        cmdMap = InputMapping.g_instance
        for commandId in cmdMap.getAllCommandsIds():
            self.__commandDescriptors[commandId] = InputCommandProcessor.__CommandDescriptor(self.__commandStats)

    def __registerCommandEvents(self, command, commandId):
        for keyDesc in command.getMappedKeyCodes():
            if keyDesc['device'] not in self.__devices:
                self.__devices[keyDesc['device']] = InputCommandProcessor.__DeviceMapping()
            if keyDesc['code'] not in self.__devices[keyDesc['device']].commandFromKey:
                self.__devices[keyDesc['device']].commandFromKey[keyDesc['code']] = list()
            if command.isBlock:
                self.__devices[keyDesc['device']].commandFromKey[keyDesc['code']].insert(0, commandId)
            else:
                self.__devices[keyDesc['device']].commandFromKey[keyDesc['code']].append(commandId)

        if command.fireAxisIndex != -1:
            if command.fireAxisDevice not in self.__devices:
                self.__devices[command.fireAxisDevice] = InputCommandProcessor.__DeviceMapping()
            axisAndSignId = command.fireAxisIndex * command.fireAxisSign
            if axisAndSignId not in self.__devices[command.fireAxisDevice].commandFromAxis:
                self.__devices[command.fireAxisDevice].commandFromAxis[axisAndSignId] = list()
            self.__devices[command.fireAxisDevice].commandFromAxis[axisAndSignId].append(commandId)
        self.__commandDescriptors[commandId].command = command

    def __filterCommand(self, commandID):
        return InputMapping.g_instance.keyboardSettings.isDevCommand(commandID) or (self.__commandsFilterAllowed is None or commandID in self.__commandsFilterAllowed) and (self.__commandsFilterForbid is None or commandID not in self.__commandsFilterForbid)

    def __processCommand(self, commandID, isFired):
        if self.__filterCommand(commandID):
            cmdDescriptor = self.__commandDescriptors[commandID]
            if isFired != cmdDescriptor.isFired or cmdDescriptor.command.switchingStyle == SWITCH_STYLES_BUTTONS.SWITCH:
                if isFired:
                    if cmdDescriptor.command.isModifierActive():
                        return cmdDescriptor.processEvent(True)
                elif not cmdDescriptor.command.isCommandActive():
                    return cmdDescriptor.processEvent(False)
        else:
            self.filteredCommandEvent(commandID, isFired)
        return False

    def __processAxisChange(self, deviceId, axisId, axisSign, isFired):
        commandIDlist = None
        if deviceId in self.__devices:
            commandIDlist = self.__devices[deviceId].commandFromAxis.get(axisId * axisSign, None)
        if commandIDlist is None:
            commandIDlist = self.__devices[0].commandFromAxis.get(axisId * axisSign, None)
        if commandIDlist is not None:
            for commandID in commandIDlist:
                self.__processCommand(commandID, isFired)

        return

    def onKeyEvent(self, event):
        """handle keyboard event"""
        if event.key == 0:
            return
        else:
            commandIDlist = self.getCommandIDlist(event.key, event.deviceId)
            if commandIDlist is not None:
                isBlock = False
                for commandID in commandIDlist:
                    if not isBlock:
                        isBlock = self.__processCommand(commandID, event.isKeyDown())
                    else:
                        commandName, commandGroupName = InputMapping.g_descriptions.getCommandNameByID(commandID)
                        LOG_DEBUG('onKeyEvent - command is blocked! name(%s), groupName(%s), commandID(%s), key(%s)' % (commandName,
                         commandGroupName,
                         commandID,
                         event.key))

            return

    def getCommandIDlist(self, key, deviceId):
        commandIDlist = None
        if deviceId in self.__devices:
            commandIDlist = self.__devices[deviceId].commandFromKey.get(key, None)
        if commandIDlist is None:
            commandIDlist = self.__devices[0].commandFromKey.get(key, None)
        return commandIDlist

    def onAxisEvent(self, event):
        """handle joystick event"""
        device = self.__storedAxisDevice.get(event.deviceId, dict())
        lastAxisSign = device.get(event.axis, 0)
        if lastAxisSign == 0:
            if abs(event.value) > InputMapping.HI_AXIS_BOUND:
                newAxisSign = sign(event.value)
            else:
                newAxisSign = 0
        elif abs(event.value) < InputMapping.LOW_AXIS_BOUND:
            newAxisSign = 0
        else:
            newAxisSign = sign(event.value)
        device[event.axis] = newAxisSign
        self.__storedAxisDevice[event.deviceId] = device
        if lastAxisSign != newAxisSign:
            if lastAxisSign != 0:
                self.__processAxisChange(event.deviceId, event.axis, lastAxisSign, False)
            self.__processAxisChange(event.deviceId, event.axis, newAxisSign, True)

    def getCommand(self, commandId):
        return self.__commandDescriptors[commandId]

    def recreateCommandMap(self):
        """recreate Key and Axis mapping for all commands. Use on start and after changing key mapping in InputMapping (after options screen for example) """
        cmdMap = InputMapping.g_instance
        self.__devices.clear()
        for commandId in self.__commandDescriptors:
            command = cmdMap.keyboardSettings.getCommand(commandId)
            if command:
                self.__registerCommandEvents(command, commandId)

    def addListeners(self, commandId, commandStartListener, commandEndListener = None, eventListener = None):
        """
        Add listeners for key\x07xis command
        commandStartListener : on key down function 
        commandEndListener : on key up function 
        eventListener ( isFired ) : on key change function, isFired == isKeyDown
        """
        descriptor = self.__commandDescriptors[commandId]
        if commandStartListener:
            descriptor.startEvent += commandStartListener
        if commandEndListener:
            descriptor.endEvent += commandEndListener
        if eventListener:
            descriptor.changeEvent += eventListener

    def removeListeners(self, commandId, commandStartListener, commandEndListener = None, eventListener = None):
        """
        remove custom listeners for key\x07xis command, used only after addListeners
        """
        descriptor = self.__commandDescriptors[commandId]
        if commandStartListener:
            descriptor.startEvent -= commandStartListener
        if commandEndListener:
            descriptor.endEvent -= commandEndListener
        if eventListener:
            descriptor.changeEvent -= eventListener

    def addStartListener(self, commandId, eventListener):
        descriptor = self.__commandDescriptors[commandId]
        descriptor.startEvent += eventListener

    def addEndListener(self, commandId, eventListener):
        descriptor = self.__commandDescriptors[commandId]
        descriptor.endEvent += eventListener

    def addChangeListener(self, commandId, eventListener):
        descriptor = self.__commandDescriptors[commandId]
        descriptor.changeEvent += eventListener

    def addPredicate(self, commandId, predicate):
        """
        Set up predicate for command event. Command can has many predicates, and run only if all predicates are TRUE 
        commandId : COMMAND ID, 
        predicate : predicate function, should return True or False
        """
        self.__commandDescriptors[commandId].addPredicate(predicate)

    def setFilter(self, filter, allow = True):
        """
        filter: [COMMAND ID, ...]
        set global command filter
        if filter is None : all command is valid
        else only command in filter list is valid
        allow = true - allow filter set, = false - forbid filter set
        """
        if allow:
            self.__commandsFilterAllowed = filter
            for commandID in self.__commandDescriptors:
                if self.__commandsFilterAllowed is None or commandID not in self.__commandsFilterAllowed:
                    cmdDescriptor = self.__commandDescriptors[commandID]
                    if cmdDescriptor.command is not None:
                        cmdDescriptor.processEvent(False)

        else:
            self.__commandsFilterForbid = filter
            if filter is None:
                return
            for commandID in filter:
                cmdDescriptor = self.__commandDescriptors[commandID]
                if cmdDescriptor.command is not None:
                    cmdDescriptor.processEvent(False)

        return

    def getFilter(self, allow = True):
        if allow:
            return self.__commandsFilterAllowed
        else:
            return self.__commandsFilterForbid

    def getCommandDescriptors(self):
        return self.__commandDescriptors

    def destroy(self):
        """
        dispose all references
        """
        self.__commandDescriptors = None
        self.__devices = None
        self.__commandsFilterAllowed = None
        self.__commandsFilterForbid = None
        self.__storedAxisDevice = None
        return

    def isFired(self, commandID):
        command = self.__commandDescriptors[commandID].command
        if command:
            return command.isCommandActive() and self.__filterCommand(commandID)
        else:
            return False

    def resetCommandStats(self):
        self.__commandStats.reset()

    @property
    def isCollectingClientStats(self):
        return self.__commandStats.isGatheringStats

    def startCollectClientStats(self):
        if self.__commandStats.isGatheringStats:
            self.__commandStats.stopGatheringStats()
        self.__commandStats.startGatheringStats()

    def stopCollectClientStats(self):
        self.__commandStats.stopGatheringStats()

    def gatherCommandStats(self):
        return self.__commandStats.gatherStats()

    def getCommandsFiredCount(self):
        """
        @return: <dict>  cmdID : firedCount
        """
        return dict([ (cmdID, cmdDescriptor.firedCount) for cmdID, cmdDescriptor in self.__commandDescriptors.iteritems() if cmdID not in InputMapping.COMMANDS_SKIP_FOR_FIRED_COUNT and cmdDescriptor.firedCount ])