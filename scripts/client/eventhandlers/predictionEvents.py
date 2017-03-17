# Embedded file name: scripts/client/eventhandlers/predictionEvents.py
from HelperFunctions import generateID
from exchangeapi.CommonUtils import convertIfaceDataForUI
from exchangeapi.ErrorCodes import SUCCESS

def onAddPrediction(event):
    sendCallback = False
    for data, idTypeList in event.ob['requestBody']:
        if 'ITransaction' in data:
            idTypeList[0][0] = generateID()
            sendCallback = True

    if sendCallback and event.ob['callback']:
        event.ob['window']().call_1(event.ob['callback'], convertIfaceDataForUI(event.ob['requestBody']), SUCCESS)