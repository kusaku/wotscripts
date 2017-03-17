# Embedded file name: scripts/client/gui/HelpHint.py
from random import choice
import Event
import BigWorld
from Singleton import singleton
from gui.Scaleform.windows import CustomObject
import db.DBLogic

@singleton

class HelpHint(object):

    def __init__(self):
        self.timerCallback = None
        self.__hhProvider = db.DBLogic.g_instance.getHelpHints()
        self.__countMessages = self.__hhProvider.count
        self.__usedMessageIndexes = []
        self.receive = Event.Event(Event.EventManager())
        self.reset()
        return

    def setCountMessages(self, countMessages):
        self.__countMessages = countMessages
        self.reset()

    def start(self):
        """  start displaying help tooltips  """
        self.__send()

    def stop(self):
        """  stop displaying help tooltips  """
        if self.timerCallback is not None:
            BigWorld.cancelCallback(self.timerCallback)
            self.timerCallback = None
        self.receive.clear()
        return

    def reset(self):
        """ reset cached indexes """
        self.__usedMessageIndexes = []
        for index in range(self.__countMessages + 1):
            if index not in self.__hhProvider.unusedMessageIndexes:
                self.__usedMessageIndexes.append(index)

    def getRandomLocalizeHint(self):
        """ get one random help tooltip """
        if not len(self.__usedMessageIndexes):
            self.reset()
        curMessageIndex = choice(self.__usedMessageIndexes)
        self.__usedMessageIndexes.remove(curMessageIndex)
        return curMessageIndex

    def __send(self):
        self.receive(self.getRandomLocalizeHint())
        self.timerCallback = BigWorld.callback(self.__hhProvider.time, self.__send)