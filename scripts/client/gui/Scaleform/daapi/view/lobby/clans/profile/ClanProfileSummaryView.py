# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/clans/profile/ClanProfileSummaryView.py
import BigWorld
from adisp import process
from gui import SystemMessages
from gui.clans.clan_controller import g_clanCtrl
from gui.clans.contexts import CreateApplicationCtx
from helpers import i18n
from gui.clans.settings import CLIENT_CLAN_RESTRICTIONS as _RES
from gui.clans import formatters as clans_fmts
from gui.shared.formatters import icons, text_styles
from gui.shared.view_helpers.UsersInfoHelper import UsersInfoHelper
from gui.shared.events import OpenLinkEvent
from gui.Scaleform.genConsts.TEXT_MANAGER_STYLES import TEXT_MANAGER_STYLES as _STYLE
from gui.Scaleform.locale.CLANS import CLANS
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.daapi.view.lobby.fortifications.fort_utils import fort_formatters
from gui.Scaleform.daapi.view.meta.ClanProfileSummaryViewMeta import ClanProfileSummaryViewMeta

def _stateVO(showRequestBtn, mainStatus = None, tooltip = '', enabledRequestBtn = False, addStatus = None, showPersonalBtn = False):
    return {'isShowRequestBtn': showRequestBtn,
     'isEnabledRequestBtn': enabledRequestBtn,
     'isShowPersonnelBtn': showPersonalBtn,
     'mainStatus': mainStatus or '',
     'additionalStatus': addStatus or '',
     'tooltip': tooltip}


def _status(i18nKey, style, icon = None):
    message = CLANS.clanprofile_summaryview_statusmsg(i18nKey)
    if icon is not None:
        message = i18n.makeString(message, icon=icons.makeImageTag(icon, 16, 16, -4, 0))
    else:
        message = i18n.makeString(message)
    return style(message)


_STATES = {_RES.NO_RESTRICTIONS: _stateVO(True, enabledRequestBtn=True),
 _RES.OWN_CLAN: _stateVO(False, showPersonalBtn=True),
 _RES.ALREADY_IN_CLAN: _stateVO(False, addStatus=_status('inAnotherClan', text_styles.success)),
 _RES.FORBIDDEN_ACCOUNT_TYPE: _stateVO(False, addStatus=_status('banned', text_styles.error)),
 _RES.CLAN_LEAVE_COOLDOWN: _stateVO(True, mainStatus=_status('isInCooldown', text_styles.alert, RES_ICONS.MAPS_ICONS_LIBRARY_ALERTICON), tooltip=CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_JOINUNAVAILABLE_AFTERCLANLEAVE),
 _RES.CLAN_APPLICATION_ALREADY_SENT: _stateVO(False, addStatus=_status('requestSubmitted', text_styles.success)),
 _RES.CLAN_INVITE_ALREADY_RECEIVED: _stateVO(False, addStatus=_status('invitationSubmitted', text_styles.success)),
 _RES.SENT_INVITES_LIMIT_REACHED: _stateVO(True, mainStatus=_status('inviteLimit', text_styles.alert, RES_ICONS.MAPS_ICONS_LIBRARY_ALERTICON), tooltip=CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_JOINUNAVAILABLE_INVITESHASBEENREACHED),
 _RES.CLAN_CONSCRIPTION_CLOSED: _stateVO(True, mainStatus=_status('requestNotBeConsidered', text_styles.main, RES_ICONS.MAPS_ICONS_LIBRARY_INFORMATIONICON), tooltip=CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_JOINUNAVAILABLE_RECEIVINGREQUESTSCLOSED),
 _RES.RESYNCHRONIZE: _stateVO(False, addStatus=_status('resynchronize', text_styles.main)),
 _RES.DEFAULT: _stateVO(False)}

class ClanProfileSummaryView(ClanProfileSummaryViewMeta, UsersInfoHelper):

    def __init__(self):
        ClanProfileSummaryViewMeta.__init__(self)
        UsersInfoHelper.__init__(self)
        self.__stateMask = 0

    @process
    def setClanDossier(self, clanDossier):
        super(ClanProfileSummaryView, self).setClanDossier(clanDossier)
        self._showWaiting()
        clanInfo = yield clanDossier.requestClanInfo()
        ratings = yield clanDossier.requestClanRatings()
        globalMapStats = yield clanDossier.requestGlobalMapStats()
        strongholdInfo = yield clanDossier.requestStrongholdInfo()
        if self.isDisposed():
            return
        self._updateClanInfo(clanInfo)
        ratingStrBuilder = text_styles.builder(delimiter='\n')
        ratingStrBuilder.addStyledText(text_styles.promoTitle, BigWorld.wg_getIntegralFormat(ratings.getEfficiency()))
        ratingStrBuilder.addStyledText(text_styles.stats, CLANS.CLANPROFILE_SUMMARYVIEW_TOTALRAGE)
        motto = clanInfo.getMotto()
        if motto:
            description = text_styles.main(motto)
        else:
            description = text_styles.standard(CLANS.CLANPROFILE_SUMMARYVIEW_DEFAULTCLANDESCR)
        hasGlobalMap = globalMapStats.hasGlobalMap()
        self.as_setDataS({'totalRating': ratingStrBuilder.render(),
         'totalRatingTooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_TOTALRATING,
         'clanDescription': description,
         'isShowFortBtn': True,
         'isShowClanNavBtn': hasGlobalMap,
         'isShowUrlString': not hasGlobalMap})
        self.as_updateGeneralBlockS(self.__makeGeneralBlock(clanInfo, syncUserInfo=True))
        self.as_updateFortBlockS(self.__makeFortBlock(ratings, strongholdInfo))
        self.as_updateGlobalMapBlockS(self.__makeGlobalMapBlock(globalMapStats, ratings))
        self.__updateStatus()
        self._hideWaiting()

    def onAccountWebVitalInfoChanged(self, fieldName, value):
        self.__updateStatus()

    def onClanWebVitalInfoChanged(self, clanDbID, fieldName, value):
        if clanDbID == self._clanDossier.getDbID():
            self.__updateStatus()

    @process
    def onAccountClanProfileChanged(self, profile):
        clanInfo = yield self._clanDossier.requestClanInfo()
        if not self.isDisposed():
            self.as_updateGeneralBlockS(self.__makeGeneralBlock(clanInfo))

    def onClanEmblem128x128Received(self, clanDbID, emblem):
        pass

    def onClanEmblem256x256Received(self, clanDbID, emblem):
        if emblem:
            self.as_setClanEmblemS(self.getMemoryTexturePath(emblem))

    @process
    def onUserNamesReceived(self, names):
        clanInfo = yield self._clanDossier.requestClanInfo()
        if not self.isDisposed():
            self.as_updateGeneralBlockS(self.__makeGeneralBlock(clanInfo))

    @process
    def sendRequestHandler(self):
        self.as_showWaitingS(True)
        context = CreateApplicationCtx([self._clanDossier.getDbID()])
        result = yield g_clanCtrl.sendRequest(context, allowDelay=True)
        if result.isSuccess():
            clanInfo = yield self._clanDossier.requestClanInfo()
            SystemMessages.pushMessage(clans_fmts.getAppSentSysMsg(clanInfo.getClanName(), clanInfo.getTag()))
            self.__updateStatus()
        self.as_showWaitingS(False)

    def hyperLinkGotoDetailsMap(self):
        self.fireEvent(OpenLinkEvent(OpenLinkEvent.GLOBAL_MAP_PROMO_SUMMARY))

    def hyperLinkGotoMap(self):
        self.fireEvent(OpenLinkEvent(OpenLinkEvent.GLOBAL_MAP_SUMMARY))

    def _updateClanEmblem(self, clanDbID):
        self.requestClanEmblem256x256(clanDbID)

    def _updateHeaderState(self):
        pass

    def __makeFortBlock(self, ratings, strongholdInfo):
        notActual = ratings.getBattlesFor28Days() + ratings.getSortiesFor28Days() <= 0
        stats = [{'local': 'rageLevel10',
          'value': ratings.getEloRating10(),
          'timeExpired': notActual,
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_FORT_ELO_RAGE_10_BODY},
         {'local': 'rageLevel8',
          'value': ratings.getEloRating8(),
          'timeExpired': notActual,
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_FORT_ELO_RAGE_8_BODY},
         {'local': 'sortiesPerDay',
          'value': ratings.getSortiesFor28Days(),
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_FORT_SORTIE_COUNT_28_BODY},
         {'local': 'battlesPerDay',
          'value': ratings.getBattlesFor28Days(),
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_FORT_BATTLES_COUNT_28_BODY},
         {'local': 'fortLevel',
          'value': fort_formatters.getTextLevel(strongholdInfo.getLevel()),
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_FORT_LEVEL_BODY}]
        return {'isShowHeader': True,
         'header': text_styles.highTitle(CLANS.CLANPROFILE_MAINWINDOWTAB_FORTIFICATION),
         'statBlocks': self.__makeStatsBlock(stats),
         'emptyLbl': text_styles.standard(CLANS.CLANPROFILE_SUMMARYVIEW_BLOCKLBL_EMPTYFORT),
         'isActivated': strongholdInfo.hasFort()}

    def __makeGeneralBlock(self, clanInfo, syncUserInfo = False):
        stats = [{'local': 'commander',
          'value': self.getGuiUserName(clanInfo.getLeaderDbID()),
          'textStyle': _STYLE.STATS_TEXT}, {'local': 'totalPlayers',
          'value': clanInfo.getMembersCount()}]
        canSeeTreasury = self.clansCtrl.getLimits().canSeeTreasury(self._clanDossier)
        if canSeeTreasury.success:
            stats.append({'local': 'gold',
             'value': clanInfo.getTreasuryValue(),
             'icon': RES_ICONS.MAPS_ICONS_LIBRARY_GOLDICON_2})
        if syncUserInfo:
            self.syncUsersInfo()
        return {'isShowHeader': False,
         'header': '',
         'statBlocks': self.__makeStatsBlock(stats),
         'isActivated': True}

    def __makeGlobalMapBlock(self, globalMapStats, ratings):
        battles28d = ratings.getGlobalMapBattlesFor28Days()
        notActual = battles28d <= 0
        stats = [{'local': 'rageLevel10',
          'value': ratings.getGlobalMapEloRating10(),
          'timeExpired': notActual,
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_GMAP_ELO_RAGE_10_BODY},
         {'local': 'rageLevel8',
          'value': ratings.getGlobalMapEloRating8(),
          'timeExpired': notActual,
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_GMAP_ELO_RAGE_8_BODY},
         {'local': 'rageLevel6',
          'value': ratings.getGlobalMapEloRating6(),
          'timeExpired': notActual,
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_GMAP_ELO_RAGE_6_BODY},
         {'local': 'battlesCount',
          'value': battles28d,
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_GMAP_BATTLES_COUNT_BODY},
         {'local': 'provinces',
          'value': globalMapStats.getCapturedProvincesCount(),
          'tooltip': CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_GMAP_PROVINCE_BODY}]
        return {'isShowHeader': True,
         'header': text_styles.highTitle(CLANS.CLANPROFILE_MAINWINDOWTAB_GLOBALMAP),
         'statBlocks': self.__makeStatsBlock(stats),
         'emptyLbl': text_styles.standard(CLANS.CLANPROFILE_SUMMARYVIEW_BLOCKLBL_EMPTYGLOBALMAP),
         'isActivated': globalMapStats.hasGlobalMap()}

    def __makeStatsBlock(self, listValues):
        lst = []
        for item in listValues:
            flag = item.get('flag', None)
            if flag is not None and not bool(self.__stateMask & flag):
                continue
            localKey = item.get('local', None)
            value = item.get('value', None)
            isTimeExpired = item.get('timeExpired', False)
            tooltipBody = item.get('tooltip', None)
            textStyle = item.get('textStyle', None)
            isUseTextStylePattern = textStyle is not None
            valueStyle = text_styles.stats
            localKey = i18n.makeString(CLANS.clanprofile_summaryview_blocklbl(localKey))
            tooltipHeader = localKey
            if isTimeExpired:
                valueStyle = text_styles.disabled
                tooltipBody = CLANS.CLANPROFILE_SUMMARYVIEW_TOOLTIP_RATINGOUTDATED_BODY
            elif tooltipBody is None:
                tooltipBody = None
                tooltipHeader = None
            if not isinstance(value, str):
                value = BigWorld.wg_getIntegralFormat(value)
            icon = item.get('icon', None)
            if icon is not None:
                icon = icons.makeImageTag(icon, 16, 16, -4, 0)
                value = icon + ' ' + value
            if isUseTextStylePattern:
                truncateVo = {'isUseTruncate': isUseTextStylePattern,
                 'textStyle': textStyle,
                 'maxWidthTF': 140}
            else:
                truncateVo = None
            lst.append({'label': text_styles.main(localKey),
             'value': valueStyle(str(value)) if not isUseTextStylePattern else value,
             'tooltipHeader': tooltipHeader,
             'tooltipBody': i18n.makeString(tooltipBody) if tooltipBody is not None else '',
             'isUseTextStyle': isUseTextStylePattern,
             'truncateVo': truncateVo})

        return lst

    def __updateStatus(self):
        reason = self.clansCtrl.getLimits().canSendApplication(self._clanDossier).reason
        raise reason in _STATES or AssertionError('Unknown reason, ' + reason)
        self.as_updateStatusS(_STATES[reason])