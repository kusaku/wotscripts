# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FittingSelectPopoverMeta.py
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class FittingSelectPopoverMeta(SmartPopOverView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends SmartPopOverView
    null
    """

    def setVehicleModule(self, newId, oldId, isRemove):
        """
        :param newId:
        :param oldId:
        :param isRemove:
        :return :
        """
        self._printOverrideError('setVehicleModule')

    def showModuleInfo(self, moduleId):
        """
        :param moduleId:
        :return :
        """
        self._printOverrideError('showModuleInfo')

    def as_updateS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)