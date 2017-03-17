# Embedded file name: scripts/common/_pve_data.py
import Math
import math
import consts
true = True
false = False

class Dummy:
    pass


isServerDatabase = False

class AMMO_TYPE:
    BALL = 0
    AP = 1
    APC = 2
    I = 3
    APHC = 4
    API = 5
    HEI = 6
    APHE = 7
    ALL_TYPES = (BALL,
     AP,
     APC,
     I,
     APHC,
     API,
     HEI,
     APHE)


PvEData = Dummy()
PvEData.interception = Dummy()
PvEData.interception.arenaId = 60
PvEData.interception.botsNearBaseAlertDist = 50.0
PvEData.interception.botsPreSpawnAlertTime = 10.0
PvEData.interception.botsSettings = Dummy()
PvEData.interception.botsSettings.settings = []
PvEData.interception.botsSettings.settings.insert(0, None)
PvEData.interception.botsSettings.settings[0] = Dummy()
PvEData.interception.botsSettings.settings[0].aircraft = []
PvEData.interception.botsSettings.settings[0].aircraft.insert(0, None)
PvEData.interception.botsSettings.settings[0].aircraft[0] = Dummy()
PvEData.interception.botsSettings.settings[0].aircraft[0].aircraftID = 2002
PvEData.interception.botsSettings.settings[0].aircraft[0].presetName = ''
PvEData.interception.botsSettings.settings[0].bombsPerLaunch = 10
PvEData.interception.botsSettings.settings[0].launchingPeriod = 10.0
PvEData.interception.botsSettings.settings[0].maxPlayerLevel = 5
PvEData.interception.botsSettings.settings[0].targetBombingDispersion = 20.0
PvEData.interception.botsSettings.settings.insert(1, None)
PvEData.interception.botsSettings.settings[1] = Dummy()
PvEData.interception.botsSettings.settings[1].aircraft = []
PvEData.interception.botsSettings.settings[1].aircraft.insert(0, None)
PvEData.interception.botsSettings.settings[1].aircraft[0] = Dummy()
PvEData.interception.botsSettings.settings[1].aircraft[0].aircraftID = 2702
PvEData.interception.botsSettings.settings[1].aircraft[0].presetName = ''
PvEData.interception.botsSettings.settings[1].bombsPerLaunch = 10
PvEData.interception.botsSettings.settings[1].launchingPeriod = 10.0
PvEData.interception.botsSettings.settings[1].maxPlayerLevel = 10
PvEData.interception.botsSettings.settings[1].targetBombingDispersion = 20.0
PvEData.interception.botsSpawnMsg = Dummy()
PvEData.interception.botsSpawnMsg.text = 'HUD_PVE_MESSAGE_BOMBERS_SPOTTED'
PvEData.interception.botsSpawnMsg.type = 'completionFightSuperiorityEnemy'
PvEData.interception.briefingMsg = Dummy()
PvEData.interception.briefingMsg.duration = 5.0
PvEData.interception.briefingMsg.text = 'INTERCEPTION'
PvEData.interception.briefingMsg.title = 'INTERCEPTION'
PvEData.interception.messages = Dummy()
PvEData.interception.messages.message = []
PvEData.interception.messages.message.insert(0, None)
PvEData.interception.messages.message[0] = Dummy()
PvEData.interception.messages.message[0].text = 'HUD_PVE_MESSAGE_bOMBERS_NEAR_BASE'
PvEData.interception.messages.message[0].type = 'completionFightSuperiorityEnemy'
PvEData.interception.messages.message.insert(1, None)
PvEData.interception.messages.message[1] = Dummy()
PvEData.interception.messages.message[1].text = 'HUD_PVE_MESSAGE_BOMBERS_ARE_COMING'
PvEData.interception.messages.message[1].type = 'completionFightSuperiorityEnemy'
PvEData.interception.startDelay = 0.0
PvEData.interception.targetBaseGroupName = 'airport'
PvEData.interception.waves = Dummy()
PvEData.interception.waves.wave = []
PvEData.interception.waves.wave.insert(0, None)
PvEData.interception.waves.wave[0] = Dummy()
PvEData.interception.waves.wave[0].botsCountPerPlayer = 1
PvEData.interception.waves.wave[0].spawnTime = 0.0
PvEData.interception.waves.wave[0].splineData = []
PvEData.interception.waves.wave[0].splineData.insert(0, None)
PvEData.interception.waves.wave[0].splineData[0] = Dummy()
PvEData.interception.waves.wave[0].splineData[0].spawnpoint = []
PvEData.interception.waves.wave[0].splineData[0].spawnpoint.insert(0, None)
PvEData.interception.waves.wave[0].splineData[0].spawnpoint[0] = Dummy()
PvEData.interception.waves.wave[0].splineData[0].spawnpoint[0].lookAtPoint = Math.Vector3(737, 180, 570)
PvEData.interception.waves.wave[0].splineData[0].spawnpoint[0].position = Math.Vector3(737, 180, 600)
PvEData.interception.waves.wave[0].splineData[0].spawnpoint.insert(1, None)
PvEData.interception.waves.wave[0].splineData[0].spawnpoint[1] = Dummy()
PvEData.interception.waves.wave[0].splineData[0].spawnpoint[1].lookAtPoint = Math.Vector3(737, 180, 570)
PvEData.interception.waves.wave[0].splineData[0].spawnpoint[1].position = Math.Vector3(737, 180, 650)
PvEData.interception.waves.wave[0].splineData[0].splineName = 'pve_bomber_spline_1'
PvEData.interception.waves.wave[0].splineData.insert(1, None)
PvEData.interception.waves.wave[0].splineData[1] = Dummy()
PvEData.interception.waves.wave[0].splineData[1].spawnpoint = []
PvEData.interception.waves.wave[0].splineData[1].spawnpoint.insert(0, None)
PvEData.interception.waves.wave[0].splineData[1].spawnpoint[0] = Dummy()
PvEData.interception.waves.wave[0].splineData[1].spawnpoint[0].lookAtPoint = Math.Vector3(710, 180, 570)
PvEData.interception.waves.wave[0].splineData[1].spawnpoint[0].position = Math.Vector3(710, 180, 600)
PvEData.interception.waves.wave[0].splineData[1].spawnpoint.insert(1, None)
PvEData.interception.waves.wave[0].splineData[1].spawnpoint[1] = Dummy()
PvEData.interception.waves.wave[0].splineData[1].spawnpoint[1].lookAtPoint = Math.Vector3(710, 180, 570)
PvEData.interception.waves.wave[0].splineData[1].spawnpoint[1].position = Math.Vector3(710, 180, 650)
PvEData.interception.waves.wave[0].splineData[1].splineName = 'pve_bomber_spline_2'
PvEData.interception.waves.wave[0].splineData.insert(2, None)
PvEData.interception.waves.wave[0].splineData[2] = Dummy()
PvEData.interception.waves.wave[0].splineData[2].spawnpoint = []
PvEData.interception.waves.wave[0].splineData[2].spawnpoint.insert(0, None)
PvEData.interception.waves.wave[0].splineData[2].spawnpoint[0] = Dummy()
PvEData.interception.waves.wave[0].splineData[2].spawnpoint[0].lookAtPoint = Math.Vector3(721, 180, 570)
PvEData.interception.waves.wave[0].splineData[2].spawnpoint[0].position = Math.Vector3(721, 180, 600)
PvEData.interception.waves.wave[0].splineData[2].spawnpoint.insert(1, None)
PvEData.interception.waves.wave[0].splineData[2].spawnpoint[1] = Dummy()
PvEData.interception.waves.wave[0].splineData[2].spawnpoint[1].lookAtPoint = Math.Vector3(721, 180, 570)
PvEData.interception.waves.wave[0].splineData[2].spawnpoint[1].position = Math.Vector3(721, 180, 650)
PvEData.interception.waves.wave[0].splineData[2].splineName = 'pve_bomber_spline_3'
PvEData.interception.waves.wave[0].splinePointRadius = 30.0
PvEData.interception.waves.wave.insert(1, None)
PvEData.interception.waves.wave[1] = Dummy()
PvEData.interception.waves.wave[1].botsCountPerPlayer = 1
PvEData.interception.waves.wave[1].spawnTime = 20.0
PvEData.interception.waves.wave[1].splineData = []
PvEData.interception.waves.wave[1].splineData.insert(0, None)
PvEData.interception.waves.wave[1].splineData[0] = Dummy()
PvEData.interception.waves.wave[1].splineData[0].spawnpoint = []
PvEData.interception.waves.wave[1].splineData[0].spawnpoint.insert(0, None)
PvEData.interception.waves.wave[1].splineData[0].spawnpoint[0] = Dummy()
PvEData.interception.waves.wave[1].splineData[0].spawnpoint[0].lookAtPoint = Math.Vector3(737, 180, 570)
PvEData.interception.waves.wave[1].splineData[0].spawnpoint[0].position = Math.Vector3(737, 180, 600)
PvEData.interception.waves.wave[1].splineData[0].spawnpoint.insert(1, None)
PvEData.interception.waves.wave[1].splineData[0].spawnpoint[1] = Dummy()
PvEData.interception.waves.wave[1].splineData[0].spawnpoint[1].lookAtPoint = Math.Vector3(737, 180, 570)
PvEData.interception.waves.wave[1].splineData[0].spawnpoint[1].position = Math.Vector3(737, 180, 650)
PvEData.interception.waves.wave[1].splineData[0].splineName = 'pve_bomber_spline_1'
PvEData.interception.waves.wave[1].splineData.insert(1, None)
PvEData.interception.waves.wave[1].splineData[1] = Dummy()
PvEData.interception.waves.wave[1].splineData[1].spawnpoint = []
PvEData.interception.waves.wave[1].splineData[1].spawnpoint.insert(0, None)
PvEData.interception.waves.wave[1].splineData[1].spawnpoint[0] = Dummy()
PvEData.interception.waves.wave[1].splineData[1].spawnpoint[0].lookAtPoint = Math.Vector3(710, 180, 570)
PvEData.interception.waves.wave[1].splineData[1].spawnpoint[0].position = Math.Vector3(710, 180, 600)
PvEData.interception.waves.wave[1].splineData[1].spawnpoint.insert(1, None)
PvEData.interception.waves.wave[1].splineData[1].spawnpoint[1] = Dummy()
PvEData.interception.waves.wave[1].splineData[1].spawnpoint[1].lookAtPoint = Math.Vector3(710, 180, 570)
PvEData.interception.waves.wave[1].splineData[1].spawnpoint[1].position = Math.Vector3(710, 180, 650)
PvEData.interception.waves.wave[1].splineData[1].splineName = 'pve_bomber_spline_2'
PvEData.interception.waves.wave[1].splineData.insert(2, None)
PvEData.interception.waves.wave[1].splineData[2] = Dummy()
PvEData.interception.waves.wave[1].splineData[2].spawnpoint = []
PvEData.interception.waves.wave[1].splineData[2].spawnpoint.insert(0, None)
PvEData.interception.waves.wave[1].splineData[2].spawnpoint[0] = Dummy()
PvEData.interception.waves.wave[1].splineData[2].spawnpoint[0].lookAtPoint = Math.Vector3(721, 180, 570)
PvEData.interception.waves.wave[1].splineData[2].spawnpoint[0].position = Math.Vector3(721, 180, 600)
PvEData.interception.waves.wave[1].splineData[2].spawnpoint.insert(1, None)
PvEData.interception.waves.wave[1].splineData[2].spawnpoint[1] = Dummy()
PvEData.interception.waves.wave[1].splineData[2].spawnpoint[1].lookAtPoint = Math.Vector3(721, 180, 570)
PvEData.interception.waves.wave[1].splineData[2].spawnpoint[1].position = Math.Vector3(721, 180, 650)
PvEData.interception.waves.wave[1].splineData[2].splineName = 'pve_bomber_spline_3'
PvEData.interception.waves.wave[1].splinePointRadius = 30.0
PvEData.looseMsg = Dummy()
PvEData.looseMsg.text = 'HUD_PVE_MESSAGE_MISSION_LOST'
PvEData.looseMsg.title = 'LOOSE'
PvEData.winMsg = Dummy()
PvEData.winMsg.text = 'HUD_PVE_MESSAGE_MISSION_SUCCESSFUL'
PvEData.winMsg.title = 'WIN'