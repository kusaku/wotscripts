# Embedded file name: scripts/client/audio/AKConsts.py
AkCurveInterpolation_Log3 = 0
AkCurveInterpolation_Sine = 1
AkCurveInterpolation_Log1 = 2
AkCurveInterpolation_InvSCurve = 3
AkCurveInterpolation_Linear = 4
AkCurveInterpolation_SCurve = 5
AkCurveInterpolation_Exp1 = 6
AkCurveInterpolation_SineRecip = 7
AkCurveInterpolation_Exp3 = 8
AkCurveInterpolation_LastFadeCurve = 8
AkCurveInterpolation_Constant = 9

class PartState:
    Normal = 1
    Damaged = 2
    Destructed = 3
    RepairedPartly = 4
    Repaired = 5


SPEEDOMETER_DATA_SIZE = 7
SPEEDOMETER_STALL_SPEED_IDX = 1
SPEEDOMETER_CRITICAL_SPEED_IDX = 5
SPEEDOMETER_MAX_SPEED_IDX = 6
PART_STATE_SPEECH = {}
PART_STATE_SPEECH['Engine'] = {}
PART_STATE_SPEECH['Engine'][PartState.Damaged] = 'voice_engine_damaged'
PART_STATE_SPEECH['Engine'][PartState.Destructed] = 'voice_engine_destroyed'
PART_STATE_SPEECH['Engine'][PartState.RepairedPartly] = 'voice_engine_repaired_partly'
PART_STATE_SPEECH['Engine'][PartState.Repaired] = 'voice_engine_repaired'
PART_STATE_SPEECH['LeftWing'] = {}
PART_STATE_SPEECH['LeftWing'][PartState.Damaged] = 'voice_wing_damaged'
PART_STATE_SPEECH['RightWing'] = {}
PART_STATE_SPEECH['RightWing'][PartState.Damaged] = 'voice_wing_damaged'
PART_STATE_SPEECH['Tail'] = {}
PART_STATE_SPEECH['Tail'][PartState.Damaged] = 'voice_tail_damaged'
PART_STATE_SPEECH['Pilot'] = {}
PART_STATE_SPEECH['Gunner1'] = {}
PART_STATE_SPEECH['Gunner1'][PartState.Damaged] = 'voice_tailgunner_damaged'
PART_STATE_SPEECH['Gunner1'][PartState.Destructed] = 'voice_tailgunner_damaged'
PART_STATE_SPEECH['Radioman'] = {}
PART_STATE_SPEECH['Radioman'][PartState.Damaged] = 'voice_navigator_damaged'
PART_STATE_SPEECH['Radioman'][PartState.Destructed] = 'voice_navigator_damaged'
PART_STATE_SPEECH['Hull'] = {}
PART_STATE_SPEECH['Hull'][PartState.Damaged] = 'voice_fuselage_damaged'
PART_STATE_SPEECH['FuelTank'] = {}
PART_STATE_SPEECH['FuelTank'][PartState.Damaged] = 'voice_fuel_tank_damaged'
OVERHEAT_STARTED = 1
OVERHEAT_MID = 2
OVERHEAT_COOLDOWN = 3

class CAMERA_AIR_EFFECT:
    PLAY_EVENT_ID = 'Play_Camera_FX'
    STOP_EVENT_ID = 'Stop_Camera_FX'
    SWITCH_MATERIAL = 'SWITCH_Camera_FX_Material'
    RTPC_CRITICAL_SPEED = 'RTPC_Critical_Speed_Feedback'
    RTPC_CRITICAL_SPEED_MAX = 100


DEBUG_AUDIO_TAG = '[AUDIO]'
SPEED_OF_SOUND = 1191

class SOUND_MODES:
    SWITCH = 'SWITCH_Sound_Mode'
    SPECTATOR = 0
    AVATAR = 1
    PLAYER = 2
    WWISE = {SPECTATOR: 'Spectator',
     AVATAR: 'NPC',
     PLAYER: 'Player'}


CURRENT_PLAYER_MODE = SOUND_MODES.PLAYER

class SOUND_CASES:
    HANGAR = 0
    ARENA = 1
    VOICEOVER = 2


INIT_BANK_NAME = 'init_wowp'
WEAPONS_BANK_NAME = 'wpn'