# Embedded file name: scripts/client/adapters/IReferralClient.py
from DefaultAdapter import DefaultAdapter
import BWPersonality
import BigWorld

class SOCIAL_NETWORK:
    FACEBOOK = 0
    GOOGLE = 1
    VKONTAKTE = 2


class IReferralInviteLinkAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = super(IReferralInviteLinkAdapter, self).__call__(account, ob, **kw)
        ob['urlLink'] = 'http://google.com/?id={0}'.format(BWPersonality.g_initPlayerInfo.databaseID)
        return ob


class IReferralPublicInviteAdapter(DefaultAdapter):

    def add(self, account, requestID, data, **kw):
        target = data.get('target', SOCIAL_NETWORK.FACEBOOK)
        url = 'http://google.com/?id={0}'.format(BWPersonality.g_initPlayerInfo.databaseID)
        if target == SOCIAL_NETWORK.FACEBOOK:
            url = 'http://google.com/?id={0}'.format(BWPersonality.g_initPlayerInfo.databaseID)
        if target == SOCIAL_NETWORK.GOOGLE:
            url = 'http://google.com/?id={0}'.format(BWPersonality.g_initPlayerInfo.databaseID)
        if target == SOCIAL_NETWORK.VKONTAKTE:
            url = 'http://google.com/?id={0}'.format(BWPersonality.g_initPlayerInfo.databaseID)
        BigWorld.wg_openWebBrowser(url)
        return data