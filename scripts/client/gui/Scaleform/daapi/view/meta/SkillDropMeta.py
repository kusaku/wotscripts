# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/SkillDropMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class SkillDropMeta(AbstractWindowView):

    def calcDropSkillsParams(self, tmanCompDescr, xpReuseFraction):
        self._printOverrideError('calcDropSkillsParams')

    def dropSkills(self, dropSkillCostIdx):
        self._printOverrideError('dropSkills')

    def as_setDataS(self, data):
        """
        :param data: Represented by SkillDropModel (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setGoldS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setGold(value)

    def as_setCreditsS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCredits(value)