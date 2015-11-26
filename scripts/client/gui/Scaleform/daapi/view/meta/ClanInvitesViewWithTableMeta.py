# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanInvitesViewWithTableMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ClanInvitesViewWithTableMeta(BaseDAAPIComponent):

    def showMore(self):
        self._printOverrideError('showMore')

    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_getTableDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getTableDP()

    def as_updateDefaultSortFieldS(self, defaultSortField, defaultSortDirection):
        if self._isDAAPIInited():
            return self.flashObject.as_updateDefaultSortField(defaultSortField, defaultSortDirection)

    def as_showDummyS(self, dummyAlias):
        if self._isDAAPIInited():
            return self.flashObject.as_showDummy(dummyAlias)

    def as_hideDummyS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideDummy()