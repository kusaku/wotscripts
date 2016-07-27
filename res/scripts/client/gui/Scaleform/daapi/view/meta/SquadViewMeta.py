# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/SquadViewMeta.py
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyRoomView import BaseRallyRoomView

class SquadViewMeta(BaseRallyRoomView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseRallyRoomView
    null
    """

    def leaveSquad(self):
        """
        :return :
        """
        self._printOverrideError('leaveSquad')

    def as_updateBattleTypeS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateBattleType(data)

    def as_isFalloutS(self, isFallout):
        """
        :param isFallout:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_isFallout(isFallout)

    def as_updateInviteBtnStateS(self, isEnabled):
        """
        :param isEnabled:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateInviteBtnState(isEnabled)

    def as_setCoolDownForReadyButtonS(self, timer):
        """
        :param timer:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCoolDownForReadyButton(timer)

    def as_setSimpleTeamSectionDataS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSimpleTeamSectionData(data)