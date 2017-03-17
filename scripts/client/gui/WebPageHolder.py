# Embedded file name: scripts/client/gui/WebPageHolder.py
from Singleton import singleton
import BigWorld
from debug_utils import LOG_ERROR, LOG_INFO
import Settings

@singleton

class WebPageHolder(object):
    URL_FORUM = 'urlForum'
    URL_SEND_ERROR = 'urlSupport'
    URL_REGISTRATION = 'urlRegistration'
    URL_FORGOT_PASSWORD = 'urlForgotPassword'
    URL_ACHIEVEMENTS = 'urlAchievements'
    URL_TOKENS_HELP = 'urlTokensHelp'
    URL_BUY_GOLD = 'buyGold'
    URL_BUY_QUEST_CHIPS = 'buyQuestChips'

    def __init__(self):
        pass

    def openWebBrowser(self, url_tag, *args):
        url = self.__getUrl(url_tag)
        if url is not None:
            try:
                if args:
                    url = url % args
                self.openUrl(url)
            except:
                LOG_ERROR("openWebBrowser - can't open url", url_tag, url, args)

        else:
            LOG_ERROR('WebPageHolder::openWebBrowser', "Can't find url_tag:%s in scriptConfig file." % url_tag)
        return

    def openUrl(self, url):
        LOG_INFO('WebPageHolder::openUrl', 'url:%s' % url)
        BigWorld.wg_openWebBrowser(url)

    def __getUrl(self, url_tag):
        objUrls = Settings.g_instance.scriptConfig.urls
        url = None
        if url_tag in objUrls:
            url = objUrls[url_tag]
        return url