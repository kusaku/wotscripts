# Embedded file name: scripts/client/Helpers/TokenManager.py
from debug_utils import LOG_DEBUG, LOG_TRACE
import BigWorld
import time
from consts import TOKEN_TYPE
from ids_generators import SequenceIDGenerator
WAIT_TOKEN_ANSWER = 20

class TokenManager:
    __idsGen = SequenceIDGenerator()

    def __init__(self):
        self.__nextID = 0
        self.__reqQueue = {}

    def __clearOldRequests(self):
        currTime = int(time.time())
        oldRequests = []
        for key, value in self.__reqQueue.items():
            if value[1] < currTime - WAIT_TOKEN_ANSWER:
                oldRequests.append(key)

        for req in oldRequests:
            self.__reqQueue.pop(req)

    def requestToken(self, callback, tokenType = TOKEN_TYPE.XMPPCS):
        self.__clearOldRequests()
        result = False
        player = BigWorld.player()
        from Account import PlayerAccount
        if player != None and player.__class__ == PlayerAccount and callback:
            self.__requestID = self.__idsGen.next()
            player.base.requestToken(self.__requestID, tokenType)
            self.__reqQueue[self.__requestID] = (callback, int(time.time()))
            LOG_TRACE('TokenManager: token requested, reqId = %d' % self.__requestID)
            result = True
        return result

    def receiveChatToken(self, spaID, token, clientRequestID):
        LOG_TRACE('TokenManager: token received (spaID, token, clientRequestID): ', spaID, token, clientRequestID)
        result = False
        req = self.__reqQueue.get(clientRequestID)
        if req:
            if req[0]:
                req[0](spaID, token)
            self.__reqQueue.pop(clientRequestID)
            result = True
        return result