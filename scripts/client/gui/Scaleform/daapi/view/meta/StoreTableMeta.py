# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/StoreTableMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class StoreTableMeta(BaseDAAPIComponent):

    def refreshStoreTableDataProvider(self):
        self._printOverrideError('refreshStoreTableDataProvider')

    def as_getTableDataProviderS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getTableDataProvider()

    def as_setDataS(self, data):
        """
        :param data: Represented by StoreTableVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)