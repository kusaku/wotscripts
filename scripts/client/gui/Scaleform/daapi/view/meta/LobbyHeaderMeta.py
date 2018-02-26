# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/LobbyHeaderMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class LobbyHeaderMeta(BaseDAAPIComponent):

    def menuItemClick(self, alias):
        self._printOverrideError('menuItemClick')

    def showLobbyMenu(self):
        self._printOverrideError('showLobbyMenu')

    def showExchangeWindow(self):
        self._printOverrideError('showExchangeWindow')

    def showExchangeXPWindow(self):
        self._printOverrideError('showExchangeXPWindow')

    def showPremiumDialog(self):
        self._printOverrideError('showPremiumDialog')

    def onPremShopClick(self):
        self._printOverrideError('onPremShopClick')

    def onCrystalClick(self):
        self._printOverrideError('onCrystalClick')

    def onPayment(self):
        self._printOverrideError('onPayment')

    def showSquad(self):
        self._printOverrideError('showSquad')

    def fightClick(self, mapID, actionName):
        self._printOverrideError('fightClick')

    def as_updateNYVisibilityS(self, isShowMainMenu, isShowGlow, isShowMainMenuGlow):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYVisibility(isShowMainMenu, isShowGlow, isShowMainMenuGlow)

    def as_setScreenS(self, alias):
        if self._isDAAPIInited():
            return self.flashObject.as_setScreen(alias)

    def as_updateWalletBtnS(self, btnID, data):
        """
        :param data: Represented by HBC_FinanceVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateWalletBtn(btnID, data)

    def as_doDisableNavigationS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_doDisableNavigation()

    def as_doDisableHeaderButtonS(self, btnId, isEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_doDisableHeaderButton(btnId, isEnabled)

    def as_doDeselectHeaderButtonS(self, alias):
        if self._isDAAPIInited():
            return self.flashObject.as_doDeselectHeaderButton(alias)

    def as_setGoldFishEnabledS(self, isEnabled, playAnimation, tooltip, tooltipType):
        if self._isDAAPIInited():
            return self.flashObject.as_setGoldFishEnabled(isEnabled, playAnimation, tooltip, tooltipType)

    def as_updateSquadS(self, isInSquad, tooltip, tooltipType, isEvent, icon):
        if self._isDAAPIInited():
            return self.flashObject.as_updateSquad(isInSquad, tooltip, tooltipType, isEvent, icon)

    def as_nameResponseS(self, data):
        """
        :param data: Represented by AccountDataVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_nameResponse(data)

    def as_setBadgeIconS(self, tID):
        if self._isDAAPIInited():
            return self.flashObject.as_setBadgeIcon(tID)

    def as_setPremiumParamsS(self, btnLabel, doLabel, isHasAction, tooltip, tooltipType):
        if self._isDAAPIInited():
            return self.flashObject.as_setPremiumParams(btnLabel, doLabel, isHasAction, tooltip, tooltipType)

    def as_setPremShopDataS(self, iconSrc, premShopText, tooltip, tooltipType):
        if self._isDAAPIInited():
            return self.flashObject.as_setPremShopData(iconSrc, premShopText, tooltip, tooltipType)

    def as_updateBattleTypeS(self, battleTypeName, battleTypeIcon, isEnabled, tooltip, tooltipType, battleTypeID, eventBgEnabled, eventAnimEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_updateBattleType(battleTypeName, battleTypeIcon, isEnabled, tooltip, tooltipType, battleTypeID, eventBgEnabled, eventAnimEnabled)

    def as_setServerS(self, name, tooltip, tooltipType):
        if self._isDAAPIInited():
            return self.flashObject.as_setServer(name, tooltip, tooltipType)

    def as_updatePingStatusS(self, pingStatus, isColorBlind):
        if self._isDAAPIInited():
            return self.flashObject.as_updatePingStatus(pingStatus, isColorBlind)

    def as_updateNYEnabledS(self, isNYEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYEnabled(isNYEnabled)

    def as_updateNYAvailableS(self, isNYAvailable):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYAvailable(isNYAvailable)

    def as_setWalletStatusS(self, walletStatus):
        if self._isDAAPIInited():
            return self.flashObject.as_setWalletStatus(walletStatus)

    def as_disableFightButtonS(self, isDisabled):
        if self._isDAAPIInited():
            return self.flashObject.as_disableFightButton(isDisabled)

    def as_setFightButtonS(self, label):
        if self._isDAAPIInited():
            return self.flashObject.as_setFightButton(label)

    def as_setCoolDownForReadyS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCoolDownForReady(value)

    def as_showBubbleTooltipS(self, message, duration):
        if self._isDAAPIInited():
            return self.flashObject.as_showBubbleTooltip(message, duration)

    def as_setFightBtnTooltipS(self, tooltip):
        if self._isDAAPIInited():
            return self.flashObject.as_setFightBtnTooltip(tooltip)

    def as_updateOnlineCounterS(self, clusterStats, regionStats, tooltip, isAvailable):
        if self._isDAAPIInited():
            return self.flashObject.as_updateOnlineCounter(clusterStats, regionStats, tooltip, isAvailable)

    def as_initOnlineCounterS(self, visible):
        if self._isDAAPIInited():
            return self.flashObject.as_initOnlineCounter(visible)

    def as_setHangarMenuDataS(self, data):
        """
        :param data: Represented by DataProvider.<HangarMenuTabItemVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHangarMenuData(data)

    def as_setButtonCounterS(self, btnAlias, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setButtonCounter(btnAlias, value)

    def as_removeButtonCounterS(self, btnAlias):
        if self._isDAAPIInited():
            return self.flashObject.as_removeButtonCounter(btnAlias)