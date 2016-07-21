# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BattleMessengerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BattleMessengerMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def sendMessageToChannel(self, cid, message):
        """
        :param cid:
        :param message:
        :return Boolean:
        """
        self._printOverrideError('sendMessageToChannel')

    def focusReceived(self):
        """
        :return :
        """
        self._printOverrideError('focusReceived')

    def focusLost(self):
        """
        :return :
        """
        self._printOverrideError('focusLost')

    def as_showGreenMessageS(self, message):
        """
        :param message:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showGreenMessage(message)

    def as_showRedMessageS(self, message):
        """
        :param message:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showRedMessage(message)

    def as_showBlackMessageS(self, message):
        """
        :param message:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showBlackMessage(message)

    def as_showSelfMessageS(self, message):
        """
        :param message:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showSelfMessage(message)

    def as_setupListS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setupList(data)

    def as_setReceiverS(self, data, isResetReceivers):
        """
        :param data:
        :param isResetReceivers:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setReceiver(data, isResetReceivers)

    def as_changeReceiverS(self, receiver):
        """
        :param receiver:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_changeReceiver(receiver)

    def as_setActiveS(self, isActive):
        """
        :param isActive:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setActive(isActive)

    def as_setFocusS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFocus()

    def as_unSetFocusS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_unSetFocus()

    def as_setUserPreferencesS(self, tooltipStr):
        """
        :param tooltipStr:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setUserPreferences(tooltipStr)

    def as_setReceiversS(self, receivers):
        """
        :param receivers:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setReceivers(receivers)

    def as_enableToSendMessageS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_enableToSendMessage()

    def as_toggleCtrlPressFlagS(self, isCtrlPressed):
        """
        :param isCtrlPressed:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_toggleCtrlPressFlag(isCtrlPressed)

    def as_enterPressedS(self, index):
        """
        :param index:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_enterPressed(index)