# Embedded file name: scripts/client/gui/social_network_login/DataServer.py
import base64
import os
import hashlib
from RequestHandler import RequestHandler
from Crypto.Cipher import AES
from Crypto.Util import Counter
import BigWorld
from debug_utils import LOG_DEBUG
from Server import Server

class DataServer(Server):

    def __init__(self, name, dataReceivedHandler, encryptToken):
        Server.__init__(self, name, RequestHandler)
        self.__encryptToken = encryptToken
        if self.__encryptToken:
            self.__tokenSecret = hashlib.sha1(os.urandom(128)).hexdigest()[:16]
        self.__dataReceivedHandler = dataReceivedHandler

    def keepData(self, token, spaID):
        self.__dataReceivedHandler(token, spaID, self.__decryptToken(token))

    @property
    def tokenSecret(self):
        if self.__encryptToken:
            return self.__tokenSecret

    def _logStatus(self):
        LOG_DEBUG(self._currentStatus)

    def __decryptToken(self, token):
        if self.__encryptToken:
            cipher = AES.new(self.__tokenSecret, AES.MODE_CTR, counter=Counter.new(128))
            return cipher.decrypt(base64.urlsafe_b64decode(token))
        else:
            return token