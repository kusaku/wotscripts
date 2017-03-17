# Embedded file name: scripts/client/gui/Scaleform/LobbyAOGASNotifier.py
from Helpers.i18n import localizeAOGAS
from OperationCodes import OPERATION_RETURN_CODE
import BigWorld
from clientConsts import AOGAS_NOTIFY_MSG, AOGAS_NOTIFY_MSG_TITLE, AOGAS_NOTIFY_MSG_OK_BTN
from consts import AOGAS_NOTIFY_TIME, AOGAS_NOTIFY_PERIOD
from debug_utils import LOG_ERROR

class LobbyAOGASNotifier(object):

    def __init__(self, params):
        if params:
            for name, values in params.iteritems():
                if name not in globals():
                    LOG_ERROR('[aogas] Skip unknown aogas params', name, values)
                    continue
                for k, v in values.iteritems():
                    if k not in globals()[name].__dict__:
                        LOG_ERROR('[aogas] Skip unknown param %s in %s ' % (str(k), str(name)))
                        continue
                    globals()[name].__dict__[k] = v

        self.__lobby = None
        self.__sessionStartedAt = None
        self.__isNotifyAccount = False
        self.__lastNotifyMessages = []
        self.__notifier = _AOGASNotifier(self.__handleNotifyAccount)
        return

    def __onAOGASInfoReceived(self, operation, returnCode, accOnline, sessionStartedAt, serverRequestTime):
        if returnCode == OPERATION_RETURN_CODE.SUCCESS:
            self.__sessionStartedAt = sessionStartedAt
            if not accOnline:
                self.__handleNotifyAccount(AOGAS_NOTIFY_MSG.RESET)
            delta = max(round(serverRequestTime - self.__sessionStartedAt), 0)
            AOND = delta + accOnline
            self.__notifier.start(AOND)

    def enableNotifyAccount(self, lobby):
        self.__isNotifyAccount = True
        self.__lobby = lobby
        if self.__sessionStartedAt is None:
            self.__lobby.getPlayer().accountCmd.getAOGASInfo(self.__onAOGASInfoReceived)
        else:
            for message in self.__lastNotifyMessages:
                self.__notifyAccount(message)

            self.__lastNotifyMessages = []
        return

    def disableNotifyAccount(self):
        self.__isNotifyAccount = False
        self.__lobby = None
        return

    def __handleNotifyAccount(self, message, collect = False):
        """
        _AOGASNotifier handler.
        @param message: @see AOGAS_NOTIFY_MSG.
        @param collect: If True than collect messages when a player notify several messages. Otherwise - replace.
        """
        if self.__isNotifyAccount:
            self.__notifyAccount(message)
        elif collect:
            self.__lastNotifyMessages.append(message)
        else:
            self.__lastNotifyMessages = [message]

    def __notifyAccount(self, message):
        self.__lobby.showMessageBox(localizeAOGAS(AOGAS_NOTIFY_MSG_TITLE), localizeAOGAS(message), localizeAOGAS(AOGAS_NOTIFY_MSG_OK_BTN), None, None, None, True)
        return

    def destroy(self):
        self.__notifier.stop()
        self.__notifier = None
        self.__lobby = None
        return


class _AOGASNotifier(object):
    """
    Class performs the following functions:
        - determination of period notification.
        - determination notification text. @see: AOGAS_NOTIFY_MSG.
        - start/stop cycle for process of notifying.
    """

    def __init__(self, notifyFunction):
        """
        @param notifyFunction: notify function handler.
        @return:
        """
        self.__function = notifyFunction
        self.__started = False
        self.__AOND = 0
        self.__callbackID = None
        return

    def start(self, AOND):
        """
        Start time loop
        @param AOND: account online duration
        """
        if self.__started:
            return
        self.__started = True
        self.__AOND = AOND
        notificated = False
        if AOND > AOGAS_NOTIFY_TIME.AOND_1:
            prevAOND = self.__getPrevNotifyTime(AOND)
            self.__doNotify(self.__getNotifyMessages(prevAOND))
            notificated = prevAOND == AOND
        if notificated:
            notifyPeriod = self.__getNotifyPeriod(self.__AOND)
            self.__callbackID = BigWorld.callback(notifyPeriod, lambda : self.__notify(notifyPeriod))
        else:
            notifyTime = self.__getNextNotifyTime(AOND)
            nextNotifyDelay = abs(notifyTime - AOND)
            self.__callbackID = BigWorld.callback(nextNotifyDelay, lambda : self.__notify(nextNotifyDelay))

    def stop(self):
        """
        Stop time loop
        """
        self.__started = False
        if self.__callbackID is not None:
            BigWorld.cancelCallback(self.__callbackID)
            self.__callbackID = None
        return

    def isStarted(self):
        return self.__started

    def __getNotifyPeriod(self, AOND):
        """
        Gets notify period by AOND (accumulated online duration)
        Return value determined by AOND:
            - AOND < AOGAS_NOTIFY_TIME.AOND_1: notify each 50 minutes
            - AOND < AOGAS_NOTIFY_TIME.AOND_3: notify each 1 hour
            - AOND < AOGAS_NOTIFY_TIME.AOND_5: notify each 30 minutes
            - AOND > AOGAS_NOTIFY_TIME.AOND_5: notify each 15 minutes
        @param AOND: account online duration
        """
        if AOND < AOGAS_NOTIFY_TIME.AOND_1:
            notifyPeriod = AOGAS_NOTIFY_PERIOD.AOND_START
        elif AOND < AOGAS_NOTIFY_TIME.AOND_3:
            notifyPeriod = AOGAS_NOTIFY_PERIOD.AOND_2_3
        elif AOND < AOGAS_NOTIFY_TIME.AOND_5:
            notifyPeriod = AOGAS_NOTIFY_PERIOD.AOND_3_5
        else:
            notifyPeriod = AOGAS_NOTIFY_PERIOD.AOND_END
        return notifyPeriod

    def __getNextNotifyTime(self, AOND):
        """
        Gets next notify time by AOND (accumulated online duration). -------------
        @param AOND: account online duration
        """
        notifyTime = 0
        while notifyTime < AOND:
            notifyPeriod = self.__getNotifyPeriod(notifyTime)
            notifyTime += notifyPeriod

        return notifyTime

    def __getPrevNotifyTime(self, AOND):
        """
        Gets previous notify time by AOND (accumulated online duration). ---------
        @param AOND: account online duration
        """
        notifyTime = 0
        notifyPeriod = 0
        while notifyTime < AOND:
            notifyPeriod = self.__getNotifyPeriod(notifyTime)
            notifyTime += notifyPeriod

        return notifyTime - notifyPeriod

    def __getNotifyMessages(self, AOND):
        """
        Gets notify messages by AOND (accumulated online duration)
        If user is online he must have prompts when AOND reachs following values:
         - AOND == <{AOGAS_NOTIFY_TIME.AOND_1}:1 hours>: AOGS/AOND_1
         - AOND == <{AOGAS_NOTIFY_TIME.AOND_2}:2 hours>: AOGS/AOND_2
         - AOND == <{AOGAS_NOTIFY_TIME.AOND_3}:3 hours>: AOGS/AOND_3;
             AOGS/AOND_MORE_3
         - AOND > <{AOGAS_NOTIFY_TIME.AOND_3}:3 hours>: AOGS/AOND_MORE_3
         - AOND >= <{AOGAS_NOTIFY_TIME.AOND_5}:5 hours>: AOGS/AOND_MORE_5
        
        @param AOND: account online duration
        """
        if AOND == AOGAS_NOTIFY_TIME.AOND_1:
            messages = (AOGAS_NOTIFY_MSG.AOND_1,)
        elif AOND == AOGAS_NOTIFY_TIME.AOND_2:
            messages = (AOGAS_NOTIFY_MSG.AOND_2,)
        elif AOND == AOGAS_NOTIFY_TIME.AOND_3:
            messages = (AOGAS_NOTIFY_MSG.AOND_3, AOGAS_NOTIFY_MSG.AOND_MORE_3)
        elif AOND < AOGAS_NOTIFY_TIME.AOND_5:
            messages = (AOGAS_NOTIFY_MSG.AOND_MORE_3,)
        else:
            messages = (AOGAS_NOTIFY_MSG.AOND_MORE_5,)
        return messages

    def __doNotify(self, messages):
        if self.__function is not None:
            collect = len(messages) > 1
            for message in messages:
                self.__function(message, collect)

        else:
            LOG_ERROR('Not found notify handler ')
        return

    def __notify(self, notifyPeriod):
        self.__AOND += notifyPeriod
        self.__doNotify(self.__getNotifyMessages(self.__AOND))
        notifyPeriod = self.__getNotifyPeriod(self.__AOND)
        self.__callbackID = BigWorld.callback(notifyPeriod, lambda : self.__notify(notifyPeriod))