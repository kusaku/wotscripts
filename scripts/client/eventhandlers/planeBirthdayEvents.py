# Embedded file name: scripts/client/eventhandlers/planeBirthdayEvents.py
from debug_utils import LOG_DEBUG
from gui.HangarScripts import getHangarScriptsByName

def onPlaneBirthdayChanged(event):
    import BWPersonality
    lch = BWPersonality.g_lobbyCarouselHelper
    planeID = event.idTypeList[0][0]
    curPlane = lch.getCarouselAirplaneSelected()
    if curPlane is None or planeID != curPlane.planeID:
        return
    else:
        planeOB = lch.getCarouselAirplane(planeID)
        if planeOB:
            planeOB.planeBirthdayOb = event.ob
            if getattr(planeOB, 'isVehicleLoaded', False):
                updateHangar(planeOB)
        return


def updateHangar(planeOB):
    planeBirthdayOb = getattr(planeOB, 'planeBirthdayOb', None)
    if planeBirthdayOb and planeBirthdayOb['birthdayTime']:
        birthdayIndex, dayCountFromPrevBirthday, _ = planeBirthdayOb['prevBirthday']
        if birthdayIndex and dayCountFromPrevBirthday <= planeBirthdayOb['duration']:
            getHangarScriptsByName('planeBirthday').onHangarLoaded()
        else:
            getHangarScriptsByName('planeBirthday').onHangarUnloaded()
    return