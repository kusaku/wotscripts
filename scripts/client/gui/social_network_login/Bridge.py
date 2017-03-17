# Embedded file name: scripts/client/gui/social_network_login/Bridge.py
__author__ = 'm_antipov'
import os
import urllib, hashlib, base64
import BigWorld
from DataServer import DataServer

class _SOCIAL_NETWORKS:
    FACEBOOK = 'facebook'
    GOOGLE = 'google'
    WGNI = 'wgni'
    VKONTAKTE = 'vkontakte'
    YAHOO = 'yahoo'
    NAVER = 'naver'
    TWITTER = 'twitter'
    ODNOKLASSNIKI = 'odnoklassniki'


class SOCIAL_NETWORKS:
    FACEBOOK = 'facebook'
    GOOGLE = 'google'
    WGNI = 'wgni'
    VKONTAKTE = 'vkontakte'


class Bridge:

    def __init__(self):
        self.__server = None
        self.__authToken = None
        self.__loginDataAcquired = False
        self.__loginData = None
        self.__loginCallback = None
        self.__loginCallbackHandle = None
        return

    def __callback(self, rawToken, spaID, token):

        class Dummy:
            pass

        self.__loginData = Dummy()
        self.__loginData.rawToken = rawToken
        self.__loginData.spaID = spaID
        self.__loginData.token = token
        self.__loginDataAcquired = True

    def __checkDataReceived(self):
        if self.__loginCallback and self.__loginDataAcquired and self.__loginData:
            if self.__loginCallbackHandle:
                BigWorld.cancelCallback(self.__loginCallbackHandle)
                self.__loginCallbackHandle = None
            self.__loginCallback(self.__loginData.rawToken, self.__loginData.spaID, self.__loginData.token)
        else:
            self.__loginCallbackHandle = BigWorld.callback(0.1, self.__checkDataReceived)
        return

    def startLogin(self, loginUrl, socialNetworkName, remember, encryptToken, callback):
        try:
            self.__loginCallback = callback
            if self.__loginCallback:
                self.__loginCallbackHandle = BigWorld.callback(0.1, self.__checkDataReceived)
            else:
                return False
            self.__server = DataServer('SocialNetworkLoginServer', self.__callback, encryptToken)
            url_params = {'game': 'wowp',
             'game_port': str(self.__server.server_port),
             'remember': '1' if remember else '0',
             'token_secret': base64.b64encode(self.__server.tokenSecret) if encryptToken else ''}
            if socialNetworkName != _SOCIAL_NETWORKS.WGNI:
                url_params['external'] = socialNetworkName
            self.__server.start()
            BigWorld.wg_openWebBrowser(loginUrl + '?' + urllib.urlencode(url_params))
        except Exception as e:
            return False

        return True

    def stopLogin(self):
        if self.__server is None:
            return
        else:
            if self.__loginCallbackHandle:
                BigWorld.cancelCallback(self.__loginCallbackHandle)
                self.__loginCallbackHandle = None
            self.__loginData = None
            self.__loginCallback = None
            self.__server.stop()
            self.__server = None
            return


socialNetworkLogin = Bridge()