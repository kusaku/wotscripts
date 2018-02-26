# Embedded file name: scripts/client/messenger/gui/Scaleform/meta/SearchContactViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from messenger.gui.Scaleform.view.lobby.BaseContactView import BaseContactView

class SearchContactViewMeta(BaseContactView):

    def search(self, data):
        self._printOverrideError('search')

    def as_getSearchDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getSearchDP()

    def as_setSearchResultTextS(self, message):
        if self._isDAAPIInited():
            return self.flashObject.as_setSearchResultText(message)

    def as_setSearchDisabledS(self, coolDown):
        if self._isDAAPIInited():
            return self.flashObject.as_setSearchDisabled(coolDown)