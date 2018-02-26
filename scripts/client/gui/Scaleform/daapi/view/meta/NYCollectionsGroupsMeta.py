# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYCollectionsGroupsMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class NYCollectionsGroupsMeta(View):

    def onClose(self):
        self._printOverrideError('onClose')

    def onAlbumClick(self, settingsId):
        self._printOverrideError('onAlbumClick')

    def as_setDataS(self, data):
        """
        :param data: Represented by NYCollectionsGroupsVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)