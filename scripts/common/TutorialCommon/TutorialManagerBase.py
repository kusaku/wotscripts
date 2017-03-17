# Embedded file name: scripts/common/TutorialCommon/TutorialManagerBase.py
from abc import ABCMeta, abstractmethod
from AvatarControllerBase import AvatarControllerBase
from OperationCodes import OPERATION_CODE, OPERATION_RETURN_CODE
from _tutorial_data import TutorialData
from consts import LESSON_PART_STATE
from debug_utils import LOG_ERROR, LOG_WARNING, LOG_DEBUG
SUB_TRIGGER_CONST = 10000

class TutorialManagerBase(AvatarControllerBase):
    """
    TutorialClient manager
    """
    __metaclass__ = ABCMeta

    def __init__(self, owner, executorType, opReceiver):
        """
        """
        AvatarControllerBase.__init__(self, owner)
        self._tutorialData = TutorialData
        self._triggers = dict()
        self._currentLessonIndex = 0
        self._currentLessonPartIndex = 0
        self.operationReceiver = opReceiver
        self.operationReceiver.onReceiveOperation += self._onReceiveOperation
        self.operationReceiver.onOperationRestoredEvent += self._onReceiveOperation
        self.__executorType = executorType
        self._subTriggers = []

    def _clearSubTriggers(self):
        for val in range(len(self._subTriggers)):
            found = False
            for v in self._triggers.iterkeys():
                if self._subTriggers[val] == v:
                    found = True
                    break

            if found:
                self.__deleteTrigger(self._triggers[self._subTriggers[val]])

        self._subTriggers = []

    def _onReceiveOperation(self, operation):
        """
        Receives operation
        @param operation: received operation
        @type operation: ReceivedOperation
        """
        clearSubTriggers = True
        if operation.operationCode == OPERATION_CODE.TUTORIAL_START_LESSON:
            self._currentLessonIndex = operation.args[0]
            self._onStartLessonRequest(operation)
            self.__executeActionsSequence(self._tutorialData.lesson[self._currentLessonIndex].preStartActions)
        elif operation.operationCode == OPERATION_CODE.TUTORIAL_START_LESSON_REAL:
            self._onStartLessonRealRequest(operation)
        elif operation.operationCode == OPERATION_CODE.TUTORIAL_REQUEST_FINISH_LESSON:
            self._onRequestFinishLesson(operation)
        elif operation.operationCode == OPERATION_CODE.TUTORIAL_LESSON_PART_RESTART:
            self._onRequestPartRestart(operation)
            for v in self._triggers.itervalues():
                v.destroy()

            self._triggers.clear()
            operation.destroy()
        elif operation.operationCode == OPERATION_CODE.TUTORIAL_LESSON_PART:
            self._currentLessonPartIndex = operation.args[0]
            operation.destroy()
        elif operation.operationCode == OPERATION_CODE.TUTORIAL_ACTION:
            concreteType, data, subTrigger = self.__parseOperation(operation)
            if data.type == 'trigger':
                self._addNewTrigger(concreteType, data, operation)
                if subTrigger:
                    clearSubTriggers = False
                    self._subTriggers.append(operation.invocationId)
            elif data.type == 'action':
                self._handleAction(concreteType, data)
                operation.destroy()
        elif operation.operationCode == OPERATION_CODE.TUTORIAL_FINISH_LESSON:
            self._onFinishLesson()
            operation.destroy()
        elif operation.operationCode == OPERATION_CODE.TUTORIAL_EXECUTE_ACTION_SEQUENCE:
            self.__executeLessonPartActions(operation.args[0])
            operation.destroy()
        if len(self._subTriggers) > 0 and clearSubTriggers:
            self._clearSubTriggers()

    def _onStartLessonRequest(self, operation):
        operation.destroy()

    def _onRequestFinishLesson(self, operation):
        pass

    def _onFinishLesson(self):
        pass

    def _onRequestPartRestart(self, operation):
        pass

    def _handleAction(self, type, data):
        handler = getattr(self, '_%s__%sHandler' % (self.__class__.__name__, type), None)
        if handler:
            handler(type, data)
        else:
            LOG_ERROR('Unhandled action received (type = {0}, executor = {1})'.format(str(type), str(self.__executorType)))
        return

    def __executeLessonPartActions(self, sequenceIndex):
        lessonPartData = self._tutorialData.lesson[self._currentLessonIndex].lessonPart[self._currentLessonPartIndex]
        if sequenceIndex < 0 or sequenceIndex >= len(lessonPartData.actions):
            LOG_ERROR('Trying to execute not existing actions sequence in lesson index = {0}, part index = {1} '.format(self._currentLessonIndex, self._currentLessonPartIndex))
            return
        self.__executeActionsSequence(lessonPartData.actions[sequenceIndex])

    def __executeActionsSequence(self, sequence):
        for element in sequence.element:
            actionType, data = element.__dict__.items()[0]
            if data.executor == self.__executorType:
                self._handleAction(actionType, data)

    def destroy(self):
        """
        Destructor
        """
        self._tutorialData = None
        for v in self._triggers.itervalues():
            v.destroy()

        self._triggers.clear()
        self._triggers = None
        self.operationReceiver.onReceiveOperation -= self._onReceiveOperation
        self.operationReceiver.onOperationRestoredEvent -= self._onReceiveOperation
        self.operationReceiver = None
        AvatarControllerBase.destroy(self)
        return

    def backup(self):
        """
        Backup data
        @return: data
        @rtype: dict
        """
        return [self._currentLessonIndex, self._currentLessonPartIndex]

    def restore(self, container):
        """
        Restore
        @param container:
        @type container: dict
        """
        self._currentLessonIndex = container[0]
        self._currentLessonPartIndex = container[1]

    @abstractmethod
    def _createTrigger(self, type, data, operation):
        """
        Override to create trigger
        @param type:
        @param data:
        @param operation:
        @return: TriggerBase
        @rtype: TriggerBase
        """
        pass

    def update(self, dt):
        for trigger in self._triggers.values():
            trigger.update(dt)

    def __deleteTrigger(self, trigger):
        del self._triggers[trigger.operation.invocationId]
        trigger.destroy()

    def _addNewTrigger(self, type, data, operation):
        """
        @param type:
        @param data:
        @param operation:
        @type operation: ReceivedOperation
        """
        trigger = self._createTrigger(type, data, operation)
        if not trigger:
            LOG_WARNING('Trigger was not created (type)', type)
            return
        trigger.onStateChanged += self.__onTriggerState
        trigger.onFailed += self.__onTriggerFailed
        operation.onTimeout += self.__onOperationTimeout
        self._triggers[operation.invocationId] = trigger
        trigger.initialize()

    def __parseOperation(self, operation):
        lessonPartState, elementIndex = operation.args
        subIndex = -1
        if elementIndex > SUB_TRIGGER_CONST:
            subIndex = int(elementIndex) % SUB_TRIGGER_CONST
            elementIndex = int(elementIndex / SUB_TRIGGER_CONST) - 1
        lessonPart = self._tutorialData.lesson[self._currentLessonIndex].lessonPart[self._currentLessonPartIndex]
        if elementIndex >= len(lessonPart.__dict__[LESSON_PART_STATE.INT_TO_STRING_MAP[lessonPartState]].element):
            LOG_ERROR('Wrong subtrigger index currentLessson, partIndex, partState, element', self._currentLessonIndex, self._currentLessonPartIndex, lessonPartState, elementIndex)
            elementIndex = 0
            lessonPartState = LESSON_PART_STATE.RESTART
        sequenceElement = lessonPart.__dict__[LESSON_PART_STATE.INT_TO_STRING_MAP[lessonPartState]].element[elementIndex]
        pair = sequenceElement.__dict__.items()[0]
        if subIndex >= 0:
            pair = pair[1].trigger[subIndex].__dict__.items()[0]
        return (pair[0], pair[1], subIndex >= 0)

    def __onTriggerFailed(self, trigger):
        trigger.operation.sendResponse(OPERATION_RETURN_CODE.FAILED)
        self.__deleteTrigger(trigger)

    def __onTriggerState(self, trigger, isConditionsComplete):
        """
        @type trigger: TriggerBase
        """
        if isConditionsComplete:
            trigger.operation.sendResponse(OPERATION_RETURN_CODE.SUCCESS)
            self.__deleteTrigger(trigger)

    def __onOperationTimeout(self, operation):
        trigger = self._triggers.get(operation.invocationId, None)
        if not trigger:
            LOG_ERROR('Associated trigger was not found on operation timeout')
            return
        else:
            self.__deleteTrigger(trigger)
            return