# Embedded file name: scripts/client/eventhandlers/eventIMessage.py
from Account import PlayerAccount
import BigWorld
from gui.WindowsManager import g_windowsManager

def onIMessageCreate(event):
    messageID, messageType = next(((iD, typ) for iD, typ in event.idTypeList if typ in ('message', 'uimessage')), (None, None))
    if messageID is not None:
        player = BigWorld.player()
        if player is not None and player.__class__ == PlayerAccount:
            accountUI = g_windowsManager.getAccountUI()
            if accountUI:
                data = {'storedMessages': [[messageID, messageType]]}
                if messageType == 'message':
                    data['messageIDs'] = [messageID]
                accountUI.editIFace([[{'IMessageSession': data}]])
    return