# Embedded file name: scripts/client/ConnectionManager.py
import config_consts
from config_consts import IS_DEVELOPMENT
import consts
from clientConsts import CLIENT_INACTIVITY_TIMEOUT
import BigWorld
from Event import Event
from Singleton import singleton
from enumerations import Enumeration
from debug_utils import LOG_UNEXPECTED, LOG_MX, LOG_DEBUG, LOG_INFO
from predefined_hosts import g_preDefinedHosts
import datetime
from functools import partial
import Settings
import hashlib
import json
import ClientLog
CONNECTION_STATUS = Enumeration('Connection status', ('disconnected', 'connected', 'connectionInProgress'))

def getHardwareID():
    import ResMgr, Settings
    up = Settings.g_instance.userPrefs
    loginInfo = None
    if up.has_key(Settings.KEY_LOGIN_INFO):
        loginInfo = up[Settings.KEY_LOGIN_INFO]
    else:
        loginInfo = up.write(Settings.KEY_LOGIN_INFO, '')
    prevSalt = loginInfo.readString('salt', '')
    newSalt = BigWorld.wg_cpsalt(prevSalt)
    loginInfo.writeString('salt', newSalt)
    return newSalt


def md5hex(concealed_value):
    m = hashlib.md5()
    m.update(concealed_value)
    return m.hexdigest()


class AUTH_METHODS:
    BASIC = 'basic'
    EBANK = 'ebank'
    TOKEN2 = 'token2'
    TOKEN1 = 'token'


@singleton

class ConnectionManager(object):

    @staticmethod
    def instance():
        return ConnectionManager()

    def __init__(self):
        self.__loginName = None
        self.__areaID = None
        self.__host = g_preDefinedHosts._makeHostItem('', '')
        self.searchServersCallbacks = Event()
        self.connectionStatusCallbacks = Event()
        self.connectionStatusCallbacks += self.__connectionStatusCallback
        self.__connectionStatus = CONNECTION_STATUS.disconnected
        self.onConnected = Event()
        self.onDisconnected = Event()
        self.__rawStatus = ''
        self.loginPriority = 0
        BigWorld.serverDiscovery.changeNotifier = self._searchServersHandler
        return

    @property
    def loginName(self):
        if not self.isDisconnected():
            return self.__loginName
        else:
            return None

    @property
    def areaID(self):
        if not self.isDisconnected():
            return self.__areaID
        else:
            return None

    def startSearchServers(self):
        BigWorld.serverDiscovery.searching = 1

    def stopSearchServers(self):
        BigWorld.serverDiscovery.searching = 0

    def _searchServersHandler(self):

        def _serverDottedHost(ip):
            return '%d.%d.%d.%d' % (ip >> 24 & 255,
             ip >> 16 & 255,
             ip >> 8 & 255,
             ip >> 0 & 255)

        def _serverNetName(details):
            name = _serverDottedHost(details.ip)
            if details.port:
                name += ':%d' % details.port
                return name

        def _serverNiceName(details):
            name = details.hostName
            if not name:
                name = _serverNetName(details)
            elif details.port:
                name += ':%d' % details.port
            if details.ownerName:
                name += ' (' + details.ownerName + ')'
            return name

        servers = [ (_serverNiceName(server), server.serverString) for server in BigWorld.serverDiscovery.servers ]
        self.searchServersCallbacks(servers)

    def connect(self, url, login, password, publicKeyPath = None, areaID = None, nickName = None, token2 = '', rememberPassword = False, authMethod = None, token1 = '', spaID = None):
        self.disconnect()
        if url is not None:

            class LoginInfo:
                pass

            loginInfo = LoginInfo()
            dct = {'login': '',
             'auth_method': '',
             'session': md5hex(getHardwareID())}
            loginInfo.inactivityTimeout = CLIENT_INACTIVITY_TIMEOUT
            if publicKeyPath is not None:
                loginInfo.publicKeyPath = publicKeyPath
            if authMethod == AUTH_METHODS.TOKEN1:
                dct['temporary'] = '0'
                dct['account_id'] = spaID
                dct['ip'] = '127.0.0.1'
                dct['game'] = 'wowp'
                dct['requested_for'] = 'wowp'
                dct['token'] = token1
                dct['auth_method'] = AUTH_METHODS.TOKEN1
                loginInfo.username = json.dumps(dct).encode('utf8')
                loginInfo.password = ''
            elif len(login) > 0 or token2:
                self.__setConnectionStatus(CONNECTION_STATUS.connectionInProgress)
                if nickName is not None:
                    dct['nickname'] = nickName
                    dct['auto_registration'] = 'true'
                if token2:
                    dct['login'] = ''
                    dct['token2'] = token2
                    dct['auth_method'] = AUTH_METHODS.TOKEN2
                else:
                    dct['login'] = login
                    dct['auth_method'] = AUTH_METHODS.EBANK if config_consts.IS_VIETNAM else AUTH_METHODS.BASIC
                if config_consts.IS_IGR_ENABLED:
                    dct['is_igr'] = '1'
                dct['game'] = 'wowp'
                dct['temporary'] = str(int(not rememberPassword))
                loginInfo.username = json.dumps(dct).encode('utf8')
                if not token2:
                    loginInfo.password = password
                if len(login) > 0 and IS_DEVELOPMENT and login[0] == '@':
                    try:
                        loginInfo.username = login[1:]
                    except Exception:
                        loginInfo.username = login

            else:
                return
            BigWorld.connect(url, loginInfo, partial(self.connectionWatcher, nickName is not None))
            self.__setConnectionStatus(CONNECTION_STATUS.connectionInProgress)
            self.__loginName = login
            self.__areaID = areaID
            if g_preDefinedHosts.predefined(url):
                host = g_preDefinedHosts.byUrl(url)
                self.__host = host
            else:
                for server in BigWorld.serverDiscovery.servers:
                    if server.serverString == url:
                        self.__host = self.__host._replace(name=server.ownerName)
                        break

        return

    def disconnect(self):
        if not self.isDisconnected():
            BigWorld.disconnect()

    def connectionWatcher(self, isAutoRegister, stage, status, serverMsg):
        LOG_DEBUG('connectionWatcher: ', stage, '   ', status, serverMsg, isAutoRegister)
        self.connectionStatusCallbacks(stage, status, serverMsg, isAutoRegister)

    def __connectionStatusCallback(self, stage, status, serverMsg, isAutoRegister):
        LOG_MX('__connectionStatusCallback', stage, status)
        self.__rawStatus = status
        if stage == 0:
            pass
        elif stage == 1:
            if status != 'LOGGED_ON':
                self.__setConnectionStatus(CONNECTION_STATUS.disconnected)
        elif stage == 2:
            self.__setConnectionStatus(CONNECTION_STATUS.connected)
            loginInfo = Settings.g_instance.userPrefs[Settings.KEY_LOGIN_INFO]
            ClientLog.g_instance.general('Client login: (%s, %s, %s), localtime=%s, servertime=%s' % (loginInfo.readString('host'),
             hashlib.sha1(loginInfo.readString('user')).hexdigest(),
             loginInfo.readString('name'),
             datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
             '{servertime}'))
            self.onConnected()
        elif stage == 6:
            LOG_INFO('ConnectionManager: Disconnect ')
            self.__setConnectionStatus(CONNECTION_STATUS.disconnected)
            ClientLog.g_instance.general('Client disconnected.')
            self.onDisconnected()
        else:
            LOG_UNEXPECTED('stage:%d, status:%s, serverMsg:%s' % (stage, status, serverMsg))

    def __setConnectionStatus(self, status):
        self.__connectionStatus = status

    def isDisconnected(self):
        return self.__connectionStatus != CONNECTION_STATUS.connected

    def isUpdateClientSoftwareNeeded(self):
        return self.__rawStatus in ('LOGIN_BAD_PROTOCOL_VERSION', 'LOGIN_REJECTED_BAD_DIGEST')


def _getClientUpdateUrl():
    import ResMgr, Settings
    updateUrl = Settings.g_instance.scriptConfig.scriptData.readString(Settings.KEY_UPDATE_URL)
    return updateUrl


connectionManager = ConnectionManager.instance()