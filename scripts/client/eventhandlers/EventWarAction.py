# Embedded file name: scripts/client/eventhandlers/EventWarAction.py
import BigWorld
from consts import WAR_STATE

def onStateEdit(event):
    import BWPersonality
    player = BigWorld.player()
    warState = event.ob['currentState']
    currentState = BWPersonality.gameParams.setdefault('warAction', {}).setdefault('state', None)
    warAction = BWPersonality.gameParams['warAction']
    if warAction.get('peaceExtendTime', None) and warState == WAR_STATE.END:
        warState = WAR_STATE.PEACE
    if warState != currentState:
        warAction['state'] = warState
        player.updateHangarSpace()
    return


def onWarActionForce(event):
    score_team_1 = 100 - float(event.ob['current'][0]) / event.ob['max'][0] * 100
    score_team_2 = 100 - float(event.ob['current'][1]) / event.ob['max'][1] * 100
    BigWorld.passEventToVisualScript(None, 'onUpdateHangarState', '', {'scaleValue': max(score_team_1, score_team_2)})
    return