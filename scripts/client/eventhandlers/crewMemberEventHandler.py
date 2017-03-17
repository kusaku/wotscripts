# Embedded file name: scripts/client/eventhandlers/crewMemberEventHandler.py
from gui.WindowsManager import g_windowsManager
import Settings
import BWPersonality
import BigWorld
import db.DBLogic

def onEditCrewMember(event):
    if event.prevob and event.ob['skills'] != event.prevob['skills']:
        accountUI = g_windowsManager.getAccountUI()
        if accountUI:
            accountUI.viewIFace([[{'ICrewMemberDroppedSkills': {}}, event.idTypeList]])
    changeParams = ['planeSpecializedOn',
     'specialization',
     'expLeftToMain',
     'experience',
     'skills',
     'mainExp',
     'currentPlane',
     'skillValue',
     'bodyType',
     'icoIndex']
    if event.prevob and any((event.prevob[param] != event.ob[param] for param in changeParams)):
        accountUI = g_windowsManager.getAccountUI()
        if accountUI:
            penalyTypeList = event.idTypeList + [[event.ob['currentPlane'], 'plane']]
            accountUI.viewIFace([[{'ISkillPenalty': {}}, penalyTypeList]])
            lch = BWPersonality.g_lobbyCarouselHelper
            planeData = lch.getCarouselAirplaneSelected()
            globalID = lch.inventory.getInstalledUpgradesGlobalID(planeData.planeID) if planeData is not None else None
            if globalID is not None:
                shortConfigSpec = [[globalID, 'planePreset']]
                measurementSystem = Settings.g_instance.gameUI['measurementSystem']
                configSpec = shortConfigSpec + [[measurementSystem, 'measurementSystem']]
                accountUI.editIFace([[{'IConfigSpecs': {}}, configSpec]])
                accountUI.editIFace([[{'IShortConfigSpecs': {}}, shortConfigSpec]])
                if event.prevob['bodyType'] != event.ob['bodyType'] or planeData.planeID in (event.prevob['currentPlane'], event.ob['currentPlane']):
                    lch.checkLobbyCrewAnimation()
    return


def onSetToCacheCrewMember(event):
    lch = BWPersonality.g_lobbyCarouselHelper
    planeData = lch.getCarouselAirplaneSelected()
    if planeData is not None and event.ob['currentPlane'] == planeData.planeID:
        lch.checkLobbyCrewAnimation()
    return