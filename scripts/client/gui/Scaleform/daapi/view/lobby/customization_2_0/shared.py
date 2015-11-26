# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/customization_2_0/shared.py
from gui.Scaleform.daapi.view.dialogs import I18nConfirmDialogMeta, DIALOG_BUTTON_ID
from gui.Scaleform.locale.CUSTOMIZATION import CUSTOMIZATION
from gui.shared.formatters import text_styles

def getDialogRemoveElement(elementName):
    return I18nConfirmDialogMeta('customization/remove_element', messageCtx={'elementName': elementName,
     'delete': text_styles.error(CUSTOMIZATION.DIALOG_REPLACE_ELEMENT_DELETE)}, focusedID=DIALOG_BUTTON_ID.CLOSE)


def getDialogReplaceElement(elementName):
    return I18nConfirmDialogMeta('customization/replace_element', messageCtx={'elementName': elementName,
     'delete': text_styles.error(CUSTOMIZATION.DIALOG_REPLACE_ELEMENT_DELETE)}, focusedID=DIALOG_BUTTON_ID.CLOSE)


def getDialogReplaceElements(elementsName):
    return I18nConfirmDialogMeta('customization/replace_elements', messageCtx={'elementsName': ', '.join(elementsName),
     'delete': text_styles.error(CUSTOMIZATION.DIALOG_REPLACE_ELEMENTS_DELETE)}, focusedID=DIALOG_BUTTON_ID.CLOSE)