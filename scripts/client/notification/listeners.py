# Embedded file name: scripts/client/notification/listeners.py
import collections
from functools import partial
import weakref
import operator
from debug_utils import LOG_DEBUG
from gui.clans.clan_helpers import ClanListener
from gui.clubs.settings import CLIENT_CLUB_STATE
from gui.clubs.club_helpers import ClubListener
from gui.prb_control.prb_helpers import GlobalListener, prbInvitesProperty
from gui.shared.notifications import MsgCustomEvents
from gui.shared.utils import showInvitationInWindowsBar
from gui.shared.view_helpers.UsersInfoHelper import UsersInfoHelper
from gui.wgnc.settings import WGNC_DATA_PROXY_TYPE
from helpers import time_utils
from messenger.m_constants import PROTO_TYPE, USER_ACTION_ID
from messenger.proto import proto_getter
from messenger.proto.events import g_messengerEvents
from messenger.proto.xmpp.xmpp_constants import XMPP_ITEM_TYPE
from notification import tutorial_helper
from notification.decorators import MessageDecorator, PrbInviteDecorator, FriendshipRequestDecorator, WGNCPopUpDecorator, ClubInviteDecorator, ClubAppsDecorator, ClanAppsDecorator, ClanInvitesDecorator, ClanAppActionDecorator, ClanInvitesActionDecorator, ClanSingleAppDecorator, ClanSingleInviteDecorator
from notification.settings import NOTIFICATION_TYPE, NOTIFICATION_BUTTON_STATE
from gui.wgnc import g_wgncProvider, g_wgncEvents, wgnc_settings

class _NotificationListener(object):

    def __init__(self):
        super(_NotificationListener, self).__init__()
        self._model = lambda : None

    def start(self, model):
        self._model = weakref.ref(model)
        return True

    def stop(self):
        self._model = lambda : None

    def request(self):
        pass


class ServiceChannelListener(_NotificationListener):

    @proto_getter(PROTO_TYPE.BW)
    def proto(self):
        return None

    def start(self, model):
        result = super(ServiceChannelListener, self).start(model)
        if result:
            channel = g_messengerEvents.serviceChannel
            channel.onServerMessageReceived += self.__onMessageReceived
            channel.onClientMessageReceived += self.__onMessageReceived
            serviceChannel = self.proto.serviceChannel
            messages = serviceChannel.getReadMessages()
            addNotification = model.collection.addItem
            for clientID, (_, formatted, settings) in messages:
                addNotification(MessageDecorator(clientID, formatted, settings))

            serviceChannel.handleUnreadMessages()
        return result

    def stop(self):
        super(ServiceChannelListener, self).stop()
        channel = g_messengerEvents.serviceChannel
        channel.onServerMessageReceived -= self.__onMessageReceived
        channel.onClientMessageReceived -= self.__onMessageReceived

    def __onMessageReceived(self, clientID, formatted, settings):
        model = self._model()
        if model:
            model.addNotification(MessageDecorator(clientID, formatted, settings))


class FortServiceChannelListener(_NotificationListener):

    def __init__(self):
        super(FortServiceChannelListener, self).__init__()
        self.__fortInvitesData = {}

    @proto_getter(PROTO_TYPE.BW)
    def proto(self):
        return None

    def start(self, model):
        result = super(FortServiceChannelListener, self).start(model)
        if result:
            g_messengerEvents.serviceChannel.onCustomMessageDataReceived += self.__onMsgReceived
        return result

    def stop(self):
        self.__fortInvitesData = None
        g_messengerEvents.serviceChannel.onCustomMessageDataReceived -= self.__onMsgReceived
        super(FortServiceChannelListener, self).stop()
        return

    def __onMsgReceived(self, clientID, eventData):
        eType, battleID = eventData
        if eType == MsgCustomEvents.FORT_BATTLE_INVITE:
            self.__fortInvitesData[battleID] = clientID
        elif eType == MsgCustomEvents.FORT_BATTLE_FINISHED:
            model = self._model()
            if model:
                storedClientID = self.__fortInvitesData.get(battleID, None)
                if storedClientID:
                    _, formatted, settings = self.proto.serviceChannel.getMessage(storedClientID)
                    if formatted and settings:
                        if formatted['savedData']['battleFinishTime'] - time_utils.getCurrentTimestamp() < 0:
                            buttonsStates = {}
                            buttonsLayout = formatted.get('buttonsLayout', [])
                            for layout in buttonsLayout:
                                buttonsStates[layout['type']] = NOTIFICATION_BUTTON_STATE.VISIBLE

                            formatted['buttonsStates'] = buttonsStates
                            model.updateNotification(NOTIFICATION_TYPE.MESSAGE, storedClientID, formatted, False)
                            del self.__fortInvitesData[battleID]
        return


class PrbInvitesListener(_NotificationListener, GlobalListener):

    @prbInvitesProperty
    def prbInvites(self):
        return None

    def start(self, model):
        result = super(PrbInvitesListener, self).start(model)
        self.startGlobalListening()
        prbInvites = self.prbInvites
        if result and prbInvites:
            prbInvites.onInvitesListInited += self.__onInviteListInited
            prbInvites.onReceivedInviteListModified += self.__onInviteListModified
            if prbInvites.isInited():
                self.__addInvites()
        return result

    def stop(self):
        super(PrbInvitesListener, self).stop()
        self.stopGlobalListening()
        prbInvites = self.prbInvites
        if prbInvites:
            prbInvites.onInvitesListInited -= self.__onInviteListInited
            prbInvites.onReceivedInviteListModified -= self.__onInviteListModified

    def onPrbFunctionalInited(self):
        self.__updateInvites()

    def onPrbFunctionalFinished(self):
        self.__updateInvites()

    def onTeamStatesReceived(self, functional, team1State, team2State):
        self.__updateInvites()

    def onIntroUnitFunctionalInited(self):
        self.__updateInvites()

    def onIntroUnitFunctionalFinished(self):
        self.__updateInvites()

    def onUnitFunctionalInited(self):
        self.__updateInvites()

    def onUnitFunctionalFinished(self):
        self.__updateInvites()

    def onUnitFlagsChanged(self, flags, timeLeft):
        self.__updateInvites()

    def onPreQueueFunctionalInited(self):
        self.__updateInvites()

    def onPreQueueFunctionalFinished(self):
        self.__updateInvites()

    def onEnqueued(self, queueType, *args):
        self.__updateInvites()

    def onDequeued(self, queueType, *args):
        self.__updateInvites()

    def __onInviteListInited(self):
        if self.prbInvites.getUnreadCount() > 0:
            showInvitationInWindowsBar()
        self.__addInvites()

    def __onInviteListModified(self, added, changed, deleted):
        showInvitationInWindowsBar()
        model = self._model()
        if model is None:
            return
        else:
            for inviteID in added:
                invite = self.prbInvites.getInvite(inviteID)
                if invite:
                    model.addNotification(PrbInviteDecorator(invite))

            for inviteID in deleted:
                model.removeNotification(NOTIFICATION_TYPE.INVITE, inviteID)

            for inviteID in changed:
                invite = self.prbInvites.getInvite(inviteID)
                if invite:
                    model.updateNotification(NOTIFICATION_TYPE.INVITE, inviteID, invite, True)

            return

    def __addInvites(self):
        model = self._model()
        if model is None:
            return
        else:
            model.removeNotificationsByType(NOTIFICATION_TYPE.INVITE)
            invites = self.prbInvites.getReceivedInvites()
            invites = sorted(invites, cmp=lambda invite, other: cmp(invite.createTime, other.createTime))
            for invite in invites:
                model.addNotification(PrbInviteDecorator(invite))

            return

    def __updateInvites(self):
        model = self._model()
        if model:
            invites = self.prbInvites.getReceivedInvites()
            for invite in invites:
                model.updateNotification(NOTIFICATION_TYPE.INVITE, invite.clientID, invite, False)


class FriendshipRqsListener(_NotificationListener):

    @proto_getter(PROTO_TYPE.XMPP)
    def proto(self):
        return None

    def start(self, model):
        result = super(FriendshipRqsListener, self).start(model)
        g_messengerEvents.onPluginDisconnected += self.__me_onPluginDisconnected
        events = g_messengerEvents.users
        events.onFriendshipRequestsAdded += self.__me_onFriendshipRequestsAdded
        events.onFriendshipRequestsUpdated += self.__me_onFriendshipRequestsUpdated
        events.onUserActionReceived += self.__me_onUserActionReceived
        contacts = self.proto.contacts.getFriendshipRqs()
        for contact in contacts:
            self.__setRequest(contact)

        return result

    def stop(self):
        g_messengerEvents.onPluginDisconnected -= self.__me_onPluginDisconnected
        events = g_messengerEvents.users
        events.onFriendshipRequestsAdded -= self.__me_onFriendshipRequestsAdded
        events.onFriendshipRequestsUpdated -= self.__me_onFriendshipRequestsUpdated
        events.onUserActionReceived -= self.__me_onUserActionReceived
        super(FriendshipRqsListener, self).stop()

    def __setRequest(self, contact):
        model = self._model()
        if model:
            if contact.getProtoType() != PROTO_TYPE.XMPP:
                return
            if contact.getItemType() == XMPP_ITEM_TYPE.EMPTY_ITEM:
                return
            contactID = contact.getID()
            if model.hasNotification(NOTIFICATION_TYPE.FRIENDSHIP_RQ, contactID):
                model.updateNotification(NOTIFICATION_TYPE.FRIENDSHIP_RQ, contactID, contact, self.proto.contacts.canApproveFriendship(contact))
            else:
                model.addNotification(FriendshipRequestDecorator(contact))

    def __updateRequest(self, contact):
        model = self._model()
        if model:
            if contact.getProtoType() != PROTO_TYPE.XMPP:
                return
            model.updateNotification(NOTIFICATION_TYPE.FRIENDSHIP_RQ, contact.getID(), contact, False)

    def __updateRequests(self):
        contacts = self.proto.contacts.getFriendshipRqs()
        for contact in contacts:
            self.__updateRequest(contact)

    def __me_onPluginDisconnected(self, protoType):
        if protoType == PROTO_TYPE.XMPP:
            self.__updateRequests()

    def __me_onFriendshipRequestsAdded(self, contacts):
        for contact in contacts:
            self.__setRequest(contact)

    def __me_onFriendshipRequestsUpdated(self, contacts):
        for contact in contacts:
            self.__updateRequest(contact)

    def __me_onUserActionReceived(self, actionID, contact):
        if contact.getProtoType() != PROTO_TYPE.XMPP:
            return
        if actionID in (USER_ACTION_ID.SUBSCRIPTION_CHANGED, USER_ACTION_ID.IGNORED_ADDED):
            self.__updateRequest(contact)
        elif actionID in (USER_ACTION_ID.FRIEND_ADDED, USER_ACTION_ID.FRIEND_REMOVED):
            self.__updateRequests()


class ClubsInvitesListener(_NotificationListener, ClubListener):

    def start(self, model):
        result = super(ClubsInvitesListener, self).start(model)
        self.startClubListening()
        self.__addClubInvites()
        self.__requestMyClub()
        return result

    def stop(self):
        self.stopClubListening()
        super(ClubsInvitesListener, self).stop()

    def onAccountClubStateChanged(self, state):
        model = self._model()
        if model and self.clubsState.getStateID() == CLIENT_CLUB_STATE.UNKNOWN:
            model.removeNotificationsByType(NOTIFICATION_TYPE.CLUB_INVITE)
            model.removeNotificationsByType(NOTIFICATION_TYPE.CLUB_APPS)
        else:
            self.__requestMyClub()

    def onAccountClubInvitesInited(self, invites):
        self.__addClubInvites()

    def onAccountClubInvitesChanged(self, added, removed, changed):
        model = self._model()
        if model is None:
            return
        else:
            if len(added):
                showInvitationInWindowsBar()
            for invite in removed:
                model.removeNotification(NOTIFICATION_TYPE.CLUB_INVITE, invite.getID())

            for invite in added:
                model.addNotification(ClubInviteDecorator(invite))

            for invite in changed:
                model.updateNotification(NOTIFICATION_TYPE.CLUB_INVITE, invite.getID(), invite, True)

            return

    def __requestMyClub(self):
        self.clubsCtrl.getProfile().requestMyClub(self.__onMyClubReceived)

    def __onMyClubReceived(self, club):
        model = self._model()
        if model is None:
            return
        else:
            model.removeNotificationsByType(NOTIFICATION_TYPE.CLUB_APPS)
            if club:
                limits = self.clubsCtrl.getLimits()
                if limits.canAcceptApplication(self.clubsCtrl.getProfile(), club).success:
                    activeApps = club.getApplicants(onlyActive=True)
                    if not self.clubsCtrl.isAppsNotificationShown() and len(activeApps):
                        model.addNotification(ClubAppsDecorator(club.getClubDbID(), activeApps))
                        self.clubsCtrl.markAppsNotificationShown()
            return

    def __addClubInvites(self):
        model = self._model()
        profile = self.clubsCtrl.getProfile()
        if model is None or not profile.isInvitesAvailable():
            return
        else:
            model.removeNotificationsByType(NOTIFICATION_TYPE.CLUB_INVITE)
            invites = profile.getInvites().values()
            invites = sorted(invites, cmp=lambda invite, other: cmp(invite.getTimestamp(), other.getTimestamp()))
            activeInvites = filter(operator.methodcaller('isActive'), invites)
            if len(activeInvites):
                showInvitationInWindowsBar()
            for invite in invites:
                model.addNotification(ClubInviteDecorator(invite))

            return


class _ClanNotificationsCommonListener(_NotificationListener, ClanListener):

    def __init__(self):
        super(_ClanNotificationsCommonListener, self).__init__()

    def start(self, model):
        result = super(_ClanNotificationsCommonListener, self).start(model)
        self.startClanListening()
        g_wgncEvents.onProxyDataItemShowByDefault += self._onProxyDataItemShowByDefault
        if self.clansCtrl.isAvailable() and self.clansCtrl.isEnabled():
            self._tryToRequestApps()
        return result

    def stop(self):
        g_wgncEvents.onProxyDataItemShowByDefault -= self._onProxyDataItemShowByDefault
        self.stopClanListening()
        super(_ClanNotificationsCommonListener, self).stop()

    def onAccountClanProfileChanged(self, profile):
        """
        Perform necessarily checking in case of user entrance into clan or leaving from clan
        :param profile:
        """
        super(_ClanNotificationsCommonListener, self).onAccountClanProfileChanged(profile)
        self._tryToRequestApps()

    def onClanStateChanged(self, oldStateID, newStateID):
        super(_ClanNotificationsCommonListener, self).onClanStateChanged(oldStateID, newStateID)
        model = self._model()
        if model:
            if self.clansCtrl.isAvailable() and self.clansCtrl.isEnabled():
                self._tryToRequestApps()
            else:
                self._removeMultiNotification()

    def _onProxyDataItemShowByDefault(self, notifID, item):
        pass

    def _requestAppsCountCallback(self):
        pass

    def _tryToRequestApps(self):
        self._performAction(self._requestAppsCountCallback)

    def _performAction(self, successCallback):
        model = self._model()
        if model is None:
            return
        else:
            if self._canDoAction():
                successCallback()
            else:
                self._removeMultiNotification()
            return

    def _performUpdateMultiNotification(self, notificationEntityID, appsCount):
        model = self._model()
        if not model:
            return
        if self._canDoAction():
            existedDecoratotor = self._getMultiNotification(notificationEntityID)
            if existedDecoratotor:
                decoratorAppsCount = existedDecoratotor.getEntity()
                if decoratorAppsCount < appsCount:
                    self._updateMultiNotification(notificationEntityID, appsCount, False)
                elif decoratorAppsCount > appsCount:
                    if appsCount > 0:
                        self._updateMultiNotification(notificationEntityID, appsCount, False)
                    else:
                        self._removeMultiNotification()
            elif appsCount > 0:
                self._addMultiNotification(notificationEntityID, appsCount)
        else:
            LOG_DEBUG('Have no permisions to handle invites')
            self._removeMultiNotification()

    def _removeMultiNotification(self):
        pass

    def _addMultiNotification(self, notificationEntityID, appsCount):
        pass

    def _updateMultiNotification(self, notificationEntityID, appsCount, upNotification):
        pass

    def _getMultiNotification(self, notificationEntityID):
        pass

    def _canDoAction(self):
        return self.clansCtrl.isAvailable() and self.clansCtrl.isEnabled()

    def _performSingleNotificationAdding(self, item, itemClass, ctx = None):
        self._model().addNotification(itemClass(item.getID(), item, ctx))


class _ClanAppsListener(_ClanNotificationsCommonListener, UsersInfoHelper):

    def _requestAppsCountCallback(self):
        self.clansCtrl.getAccountProfile().getClanDossier().requestAppsCount(force=True)

    def onClanAppsCountReceived(self, clanDbID, appsCount):
        super(_ClanAppsListener, self).onClanAppsCountReceived(clanDbID, appsCount)
        model = self._model()
        if not model:
            return
        self._performAction(partial(self._performUpdateMultiNotification, clanDbID, appsCount))

    def onClanAppStateChanged(self, appId, state):
        model = self._model()
        clanSingleAppDecorator = model.getNotification(NOTIFICATION_TYPE.CLAN_APP, appId)
        if clanSingleAppDecorator:
            clanSingleAppDecorator.setState(state)
            model.updateNotification(NOTIFICATION_TYPE.CLAN_APP, appId, clanSingleAppDecorator.getEntity(), False)

    def onUserNamesReceived(self, names):
        pass

    def _canDoAction(self):
        isCtrlrEnabled = super(_ClanAppsListener, self)._canDoAction()
        profile = self.clansCtrl.getAccountProfile()
        return profile.isInClan() and profile.getMyClanPermissions().canHandleClanInvites() and isCtrlrEnabled

    def _onProxyDataItemShowByDefault(self, notifID, item):
        """
        Method handles all actions received from users
        :param notifID:
        :param item: instance of gui.wgnc.proxy_data._ProxyDataItem
        """
        itemType = item.getType()
        if itemType == WGNC_DATA_PROXY_TYPE.CLAN_APP:
            userName = self.getUserName(item.getAccountID())
            if not userName:
                pass
            self._performSingleNotificationAdding(item, ClanSingleAppDecorator, userName)
            if item.getActiveApplicationsCount() != self.clansCtrl.getAccountProfile().getClanDossier().getAppsCount():
                self._tryToRequestApps()
        elif itemType == WGNC_DATA_PROXY_TYPE.CLAN_INVITE_ACCEPTED:
            self._model().addNotification(ClanInvitesActionDecorator(item.getInviteId(), 'inviteAccepted', self.getUserName(item.getAccountId())))
        elif itemType == WGNC_DATA_PROXY_TYPE.CLAN_INVITE_DECLINED:
            self._model().addNotification(ClanInvitesActionDecorator(item.getInviteId(), 'inviteDeclined', self.getUserName(item.getAccountId())))

    def _addMultiNotification(self, notificationEntityID, appsCount):
        self._model().addNotification(ClanAppsDecorator(notificationEntityID, appsCount))

    def _updateMultiNotification(self, notificationEntityID, appsCount, upNotification):
        self._model().updateNotification(NOTIFICATION_TYPE.CLAN_APPS, notificationEntityID, appsCount, upNotification)

    def _getMultiNotification(self, notificationEntityID):
        return self._model().getNotification(NOTIFICATION_TYPE.CLAN_APPS, notificationEntityID)

    def _removeMultiNotification(self):
        self._model().removeNotificationsByType(NOTIFICATION_TYPE.CLAN_APPS)


class _ClanPersonalInvitesListener(_ClanNotificationsCommonListener):
    _INVITES_ENTITY_ID = 1

    def onClanInviteStateChanged(self, inviteIds, state):
        model = self._model()
        for inviteId in inviteIds:
            clanSingleInvDecorator = model.getNotification(NOTIFICATION_TYPE.CLAN_INVITE, inviteId)
            if clanSingleInvDecorator:
                clanSingleInvDecorator.setState(state)
                model.updateNotification(NOTIFICATION_TYPE.CLAN_INVITE, inviteId, clanSingleInvDecorator.getEntity(), False)

    def onAccountInvitesReceived(self, invites):
        super(_ClanPersonalInvitesListener, self).onAccountInvitesReceived(invites)
        model = self._model()
        if not model:
            return
        else:
            if invites is not None:
                self._performAction(partial(self._performUpdateMultiNotification, self._INVITES_ENTITY_ID, len(invites)))
            return

    def _onProxyDataItemShowByDefault(self, notifID, item):
        """
        Method handles all actions received from clan
        :param notifID:
        :param item: instance of gui.wgnc.proxy_data._ProxyDataItem
        """
        itemType = item.getType()
        if itemType == WGNC_DATA_PROXY_TYPE.CLAN_INVITE:
            if item.getActiveInvitesCount() != self.clansCtrl.getAccountProfile().getInvitesCount():
                self._tryToRequestApps()
            self._performSingleNotificationAdding(item, ClanSingleInviteDecorator)
        elif itemType == WGNC_DATA_PROXY_TYPE.CLAN_APP_DECLINED:
            self._model().addNotification(ClanAppActionDecorator(item.getApplicationId(), 'appDeclined', (item.getClanName(), item.getClanTag())))
        elif itemType == WGNC_DATA_PROXY_TYPE.CLAN_APP_ACCEPTED:
            self._model().addNotification(ClanAppActionDecorator(item.getApplicationId(), 'appAccepted', (item.getClanName(), item.getClanTag())))

    def _requestAppsCountCallback(self):
        self.clansCtrl.getAccountProfile().resyncInvites(force=True)

    def _addMultiNotification(self, notificationEntityID, appsCount):
        self._model().addNotification(ClanInvitesDecorator(notificationEntityID, appsCount))

    def _updateMultiNotification(self, notificationEntityID, appsCount, upNotification):
        self._model().updateNotification(NOTIFICATION_TYPE.CLAN_INVITES, notificationEntityID, appsCount, upNotification)

    def _getMultiNotification(self, notificationEntityID):
        return self._model().getNotification(NOTIFICATION_TYPE.CLAN_INVITES, notificationEntityID)

    def _removeMultiNotification(self):
        self._model().removeNotificationsByType(NOTIFICATION_TYPE.CLAN_INVITES)

    def _canDoAction(self):
        isCtrlrEnabled = super(_ClanPersonalInvitesListener, self)._canDoAction()
        profile = self.clansCtrl.getAccountProfile()
        return not profile.isInClan() and isCtrlrEnabled


class WGNCListener(_NotificationListener):

    def __init__(self):
        super(WGNCListener, self).__init__()
        self.__offset = 0

    def start(self, model):
        result = super(WGNCListener, self).start(model)
        g_wgncEvents.onItemShowByDefault += self.__onItemShowByDefault
        g_wgncEvents.onItemShowByAction += self.__onItemShowByAction
        g_wgncEvents.onItemUpdatedByAction += self.__onItemUpdatedByAction
        addNotification = model.collection.addItem
        for notification in g_wgncProvider.getMarkedNots():
            popUp = notification.getItemByType(wgnc_settings.WGNC_GUI_TYPE.POP_UP)
            if popUp is None:
                continue
            addNotification(WGNCPopUpDecorator(notification.notID, popUp))

        self.__offset = 0.1
        g_wgncProvider.showNoMarkedNots()
        g_wgncProvider.setEnabled(True)
        self.__offset = 0
        return result

    def stop(self):
        g_wgncEvents.onItemShowByDefault -= self.__onItemShowByDefault
        g_wgncEvents.onItemShowByAction -= self.__onItemShowByAction
        g_wgncEvents.onItemUpdatedByAction -= self.__onItemUpdatedByAction
        g_wgncProvider.setNotsAsMarked()
        super(WGNCListener, self).stop()

    def __onItemShowByDefault(self, notID, item):
        model = self._model()
        if model and item.getType() == wgnc_settings.WGNC_GUI_TYPE.POP_UP:
            model.addNotification(WGNCPopUpDecorator(notID, item, self.__offset))

    def __onItemShowByAction(self, notID, target):
        g_wgncProvider.showNotItemByName(notID, target)

    def __onItemUpdatedByAction(self, notID, item):
        model = self._model()
        if model and item.getType() == wgnc_settings.WGNC_GUI_TYPE.POP_UP:
            model.updateNotification(NOTIFICATION_TYPE.WGNC_POP_UP, notID, item, False)


class BattleTutorialListener(_NotificationListener, GlobalListener):
    _messagesIDs = tutorial_helper.TutorialGlobalStorage(tutorial_helper.TUTORIAL_GLOBAL_VAR.SERVICE_MESSAGES_IDS, [])

    @proto_getter(PROTO_TYPE.BW)
    def proto(self):
        return None

    def start(self, model):
        self.startGlobalListening()
        return super(BattleTutorialListener, self).start(model)

    def stop(self):
        super(BattleTutorialListener, self).stop()
        self.stopGlobalListening()

    def onEnqueued(self, queueType, *args):
        self.__updateBattleResultMessage(True)

    def onDequeued(self, queueType, *args):
        self.__updateBattleResultMessage(False)

    def __updateBattleResultMessage(self, locked):
        model = self._model()
        if not model:
            return
        else:
            ids = self._messagesIDs
            if not isinstance(ids, collections.Iterable):
                return
            for messageID in ids:
                _, formatted, settings = self.proto.serviceChannel.getMessage(messageID)
                if formatted and settings:
                    if 'buttonsStates' not in formatted:
                        return
                    submit = formatted['buttonsStates'].get('submit')
                    if submit is None or submit != NOTIFICATION_BUTTON_STATE.HIDDEN:
                        if locked:
                            submit = NOTIFICATION_BUTTON_STATE.VISIBLE
                        else:
                            submit = NOTIFICATION_BUTTON_STATE.VISIBLE | NOTIFICATION_BUTTON_STATE.ENABLED
                        formatted['buttonsStates']['submit'] = submit
                    model.updateNotification(NOTIFICATION_TYPE.MESSAGE, messageID, formatted, False)

            return


class NotificationsListeners(_NotificationListener):

    def __init__(self):
        super(NotificationsListeners, self).__init__()
        self.__serviceListener = ServiceChannelListener()
        self.__fortMsgsListener = FortServiceChannelListener()
        self.__invitesListener = PrbInvitesListener()
        self.__friendshipRqs = FriendshipRqsListener()
        self.__wgnc = WGNCListener()
        self.__clubsInvitesListener = ClubsInvitesListener()
        self.__clanAppsListener = _ClanAppsListener()
        self.__clanInvitesListener = _ClanPersonalInvitesListener()
        self.__tutorialListener = BattleTutorialListener()

    def start(self, model):
        self.__serviceListener.start(model)
        self.__fortMsgsListener.start(model)
        self.__invitesListener.start(model)
        self.__friendshipRqs.start(model)
        self.__wgnc.start(model)
        self.__clubsInvitesListener.start(model)
        self.__clanAppsListener.start(model)
        self.__clanInvitesListener.start(model)
        self.__tutorialListener.start(model)

    def stop(self):
        self.__serviceListener.stop()
        self.__fortMsgsListener.stop()
        self.__invitesListener.stop()
        self.__friendshipRqs.stop()
        self.__wgnc.stop()
        self.__clanAppsListener.stop()
        self.__clanInvitesListener.stop()
        self.__tutorialListener.stop()