# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PersonalMissionsMapViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class PersonalMissionsMapViewMeta(BaseDAAPIComponent):

    def onRegionClick(self, id):
        self._printOverrideError('onRegionClick')

    def as_setPlanDataS(self, planData):
        """
        :param planData: Represented by PersonalMissionsMapPlanVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPlanData(planData)