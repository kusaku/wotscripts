# Embedded file name: scripts/client/GameServerMessenger.py
import cPickle
from functools import partial
from collections import deque
import BigWorld
from messenger_common import makeArgs, MESSENGER_ACTION_IDS, MESSENGER_TIMEOUTS, MESSENGER_ACTION_ERRORS
from messenger_common import LOG_CURRENT_EXCEPTION, LOG_WARNING, LOG_ERROR, LOG_NOTE
_PERIODIC_TIMER_SEC = 0.5
_NICKNAME_BY_ID_REQ_CONFIG = (1.5, 20)

class GameServerMessenger(object):

    def __init__(self):
        self.__nextReqID = 1
        self.__timerID = BigWorld.callback(_PERIODIC_TIMER_SEC, self.__onPeriodicTimer)
        self.__reqs = {}
        self.__nicknameReqs = deque(maxlen=200)

    def destroy(self):
        if self.__timerID is not None:
            BigWorld.cancelCallback(self.__timerID)
        self.__timerID = None
        self.__reqs = None
        return

    def onActionByServer(self, processor, actionID, reqID, args):
        IDS = MESSENGER_ACTION_IDS
        if actionID == IDS.RESPONSE_SUCCESS or actionID == IDS.RESPONSE_FAILURE:
            descr = self.__reqs.pop(reqID, None)
            if descr is None:
                return
            responseCallback = descr[1]
            if responseCallback is not None:
                try:
                    responseCallback(actionID == IDS.RESPONSE_SUCCESS, args)
                except:
                    LOG_CURRENT_EXCEPTION()

            return
        elif actionID == IDS.START_CLIENT_MESSENGER:
            processor.startClientMessenger(cPickle.loads(args['strArg1']))
            return
        elif actionID == IDS.RECEIVE_NICKNAME_BY_ID:
            processor.onNicknameByID(args['int64Arg1'], args['strArg1'])
            return
        else:
            return

    def requestXmppPassword(self, callback):
        reqID = self.__addRequest(MESSENGER_TIMEOUTS.XMPP_GET_PASSWORD, partial(_onStringResult, callback))
        BigWorld.player().base.messenger_onActionByClient(MESSENGER_ACTION_IDS.XMPP_GET_PASSWORD, reqID, makeArgs())

    def requestNicknameByID(self, id):
        reqs = self.__nicknameReqs
        for v in reqs:
            if v[0] == id:
                return

        reqs.append((id, BigWorld.time()))

    def cancelRequestNicknameByID(self, id):
        reqs = self.__nicknameReqs
        for idx, v in enumerate(reqs):
            if v[0] == id:
                del reqs[idx]
                return

    def getInitParams(self):
        BigWorld.player().base.messenger_onActionByClient(MESSENGER_ACTION_IDS.GET_INIT_PARAMS, 0, makeArgs())

    def syncClanChatChannel(self, callback):
        reqID = self.__addRequest(MESSENGER_TIMEOUTS.SYNC_CLAN_CHAT_CHANNEL, partial(_onInt32Result, callback))
        BigWorld.player().base.messenger_onActionByClient(MESSENGER_ACTION_IDS.SYNC_CLAN_CHAT_CHANNEL, reqID, makeArgs())

    def requestUserlistByName(self, name, maxCount, callback):
        reqID = self.__addRequest(MESSENGER_TIMEOUTS.GET_USERLIST_BY_NAME, partial(_onUserlistResult, callback))
        BigWorld.player().base.messenger_onActionByClient(MESSENGER_ACTION_IDS.GET_USERLIST_BY_NAME, reqID, makeArgs(int32Arg1=maxCount, strArg1=name))

    def __onPeriodicTimer(self):
        self.__timerID = BigWorld.callback(_PERIODIC_TIMER_SEC, self.__onPeriodicTimer)
        currTime = BigWorld.time()
        reqs = self.__reqs
        if reqs:
            toTimeout = []
            for reqID, descr in reqs.iteritems():
                if descr[0] <= currTime:
                    toTimeout.append(reqID)

            for reqID in toTimeout:
                callback = reqs.pop(reqID)[1]
                if callback is not None:
                    try:
                        callback(False, makeArgs(int32Arg1=MESSENGER_ACTION_ERRORS.TIMEOUT))
                    except:
                        LOG_CURRENT_EXCEPTION()

        reqs = self.__nicknameReqs
        if reqs:
            delay, maxNum = _NICKNAME_BY_ID_REQ_CONFIG
            maxNum = int(maxNum * _PERIODIC_TIMER_SEC)
            maxNum = min(maxNum, len(reqs))
            send = BigWorld.player().base.messenger_onActionByClient
            while maxNum and reqs[0][1] <= currTime - delay:
                maxNum -= 1
                send(MESSENGER_ACTION_IDS.GET_NICKNAME_BY_ID, 0, makeArgs(int64Arg1=reqs.popleft()[0]))

        return

    def __addRequest(self, timeoutSec, callback):
        reqID = self.__nextReqID
        if reqID < 2147483647L:
            self.__nextReqID = reqID + 1
        else:
            self.__nextReqID = 1
        self.__reqs[reqID] = (BigWorld.time() + timeoutSec, callback)
        return reqID


class ActionProcessor(object):

    def startClientMessenger(self, params):
        LOG_WARNING('Method is not implemented', params)

    def onNicknameByID(self, id, nickname):
        LOG_WARNING('Method is not implemented', id, nickname)


def _onStringResult(callback, isSuccess, args):
    if isSuccess:
        callback(args['strArg1'], 0)
    else:
        callback(None, args['int32Arg1'])
    return


def _onUserlistResult(callback, isSuccess, args):
    if isSuccess:
        callback(cPickle.loads(args['strArg1']), 0)
    else:
        callback(None, args['int32Arg1'])
    return


def _onInt32Result(callback, isSuccess, args):
    if isSuccess:
        callback(args['int32Arg1'], 0)
    else:
        callback(None, args['int32Arg1'])
    return


g_instance = GameServerMessenger()