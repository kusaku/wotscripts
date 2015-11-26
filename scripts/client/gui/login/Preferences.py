# Embedded file name: scripts/client/gui/login/Preferences.py
import json
from predefined_hosts import AUTO_LOGIN_QUERY_URL
import BigWorld
import Settings
from debug_utils import LOG_DEBUG, LOG_WARNING

class Preferences(dict):

    def __init__(self):
        dict.__init__(self)
        if not Settings.g_instance.userPrefs.has_key(Settings.KEY_LOGIN_INFO):
            Settings.g_instance.userPrefs.write(Settings.KEY_LOGIN_INFO, '')
        try:
            loginInfo = json.loads(BigWorld.wg_ucpdata(Settings.g_instance.userPrefs[Settings.KEY_LOGIN_INFO].readString('data', '')), encoding='utf-8')
            self.update(loginInfo)
            LOG_DEBUG('Read login info from preferences.xml: {0}'.format(self))
        except ValueError:
            LOG_WARNING('Ignoring login info from preferences.xml')

    def writeLoginInfo(self):
        LOG_DEBUG('Wrote login info into preferences.xml: {0}'.format(self))
        Settings.g_instance.userPrefs[Settings.KEY_LOGIN_INFO].writeString('data', BigWorld.wg_cpdata(json.dumps(dict(self), encoding='utf-8')))

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if key == 'remember_user':
                return False
            elif key == 'server_name':
                return AUTO_LOGIN_QUERY_URL
            elif key == 'login_type':
                return 'credentials'
            elif key == 'password_length':
                return 0
            else:
                return ''