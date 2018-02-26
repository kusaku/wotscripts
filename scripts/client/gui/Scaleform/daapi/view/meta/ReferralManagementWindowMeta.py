# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ReferralManagementWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class ReferralManagementWindowMeta(AbstractWindowView):

    def onInvitesManagementLinkClick(self):
        self._printOverrideError('onInvitesManagementLinkClick')

    def inviteIntoSquad(self, referralID):
        self._printOverrideError('inviteIntoSquad')

    def as_setDataS(self, data):
        """
        :param data: Represented by RefManagementWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setTableDataS(self, referrals):
        """
        :param referrals: Represented by DataProvider.<ReferralsTableRendererVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTableData(referrals)

    def as_setAwardDataDataS(self, data):
        """
        :param data: Represented by AwardDataDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAwardDataData(data)

    def as_setProgressDataS(self, data):
        """
        :param data: Represented by ComplexProgressIndicatorVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setProgressData(data)

    def as_showAlertS(self, alertStr):
        if self._isDAAPIInited():
            return self.flashObject.as_showAlert(alertStr)