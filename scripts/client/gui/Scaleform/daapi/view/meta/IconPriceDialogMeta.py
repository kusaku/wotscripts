# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/IconPriceDialogMeta.py
from gui.Scaleform.daapi.view.dialogs.IconDialog import IconDialog

class IconPriceDialogMeta(IconDialog):

    def as_setMessagePriceS(self, dialogData):
        """
        :param dialogData: Represented by IconPriceDialogVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setMessagePrice(dialogData)

    def as_setPriceLabelS(self, label):
        if self._isDAAPIInited():
            return self.flashObject.as_setPriceLabel(label)

    def as_setOperationAllowedS(self, isAllowed):
        if self._isDAAPIInited():
            return self.flashObject.as_setOperationAllowed(isAllowed)