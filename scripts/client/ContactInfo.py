# Embedded file name: scripts/client/ContactInfo.py
import BigWorld, Settings
from Helpers.obfuscators import PasswordObfuscator

class ContactInfo:
    KEY_USER = 'user'
    KEY_HOST = 'host'
    KEY_SERVER_NAME = 'serverName'
    KEY_EMAIL = 'email'
    KEY_PASSWORD = 'password'
    KEY_REMEMBER = 'rememberPwd'
    KEY_AUTOLOGIN = 'autoLogin'
    KEY_ACCOUNT_NAME = 'accountName'

    def __init__(self, userPrefs):
        self.__userPrefs = userPrefs
        self.__checkLoginDataSection()
        self.readLocalLoginData()

    def updateAccountName(self, accountName):
        self.__checkLoginDataSection()
        self.readLocalLoginData()
        ds = self.getLoginDataSection()
        self.accountName = accountName
        ds.writeString(self.KEY_ACCOUNT_NAME, self.accountName)

    def readLocalLoginData(self):
        ds = self.getLoginDataSection()
        self.host = ds.readString(self.KEY_HOST)
        self.serverName = ds.readString(self.KEY_SERVER_NAME)
        self.user = ds.readString(self.KEY_USER)
        self.email = ds.readString(self.KEY_EMAIL)
        self.rememberPassword = ds.readBool(self.KEY_REMEMBER)
        self.password = ds.readString(self.KEY_PASSWORD)
        self.autoLogin = ds.readBool(self.KEY_AUTOLOGIN)
        self.accountName = ds.readString(self.KEY_ACCOUNT_NAME)

    def writeLocalLoginData(self):
        ds = self.getLoginDataSection()
        ds.writeString(self.KEY_HOST, self.host)
        ds.writeString(self.KEY_SERVER_NAME, self.serverName)
        ds.writeString(self.KEY_USER, self.user)
        ds.writeString(self.KEY_EMAIL, self.email)
        ds.writeBool(self.KEY_REMEMBER, self.rememberPassword)
        ds.writeString(self.KEY_PASSWORD, self.password)
        ds.writeBool(self.KEY_AUTOLOGIN, self.autoLogin)
        ds.writeString(self.KEY_ACCOUNT_NAME, self.accountName)

    def getLoginDataSection(self):
        return self.__userPrefs[Settings.KEY_LOGIN_INFO]

    def __checkLoginDataSection(self):
        if not self.__userPrefs.has_key(Settings.KEY_LOGIN_INFO):
            self.__userPrefs.write(Settings.KEY_LOGIN_INFO, '')