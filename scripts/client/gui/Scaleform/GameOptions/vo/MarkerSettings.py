# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/MarkerSettings.py
from consts import PLANE_TYPE, DB_PATH
import BigWorld
import os
from clientConsts import CombatScreenNames
__g_instaceMarkerDistance = None
SELECTED_MARKERS_LIST = [0,
 1,
 2,
 3]

class MarkerDistanceParam:

    def __init__(self, values):
        self.stepsDistance = values


def createMarkerParams(values):
    global __g_instaceMarkerDistance
    if __g_instaceMarkerDistance is None:
        __g_instaceMarkerDistance = MarkerDistanceParam(values)
    return


def g_instaceMarkerDistance():
    return __g_instaceMarkerDistance


MARKERS_PATH = ['settings', 'hudSettings', 'markers']
MARKERS_VERSIONS = ['1.6.0', '1.7.0']
AVAILABLE_MARKER_PROPERTIES = ['distanceVisible',
 'distanceOpacity',
 'iconSize',
 'showDistanceTo',
 'showStrength',
 'typeStrength',
 'showModelName',
 'showLevel',
 'showPlayerName',
 'showHeight',
 'typeHeight',
 'showShootObject',
 'showArmoredParts',
 'showUnarmoredParts']
MARKER_TARGET_TYPE = ['airMarker', 'groundMarker']
MARKERS_SUB_TYPES = ['basic', 'alt']
MARKERS_ATTRIBUTES = {'planeName': True,
 'indexInList': True,
 'playerName': True,
 'planeLevel': True,
 'planeType': True,
 'distanceToPlane': True,
 'strengthIndicator': True,
 'strength': True,
 'identicallyForAllMarkers': True,
 'strengthIndicatorType': 0}
OLD_MARKERS_TYPES = [CombatScreenNames.ENEMY,
 CombatScreenNames.FRIENDLY,
 CombatScreenNames.SQUADS,
 CombatScreenNames.DEAD,
 CombatScreenNames.TARGET]
OLD_MARKERS_SUB_TYPES = ['basic', 'alt']
OLD_MARKERS_ATTRIBUTES = {'planeName': True,
 'indexInList': True,
 'playerName': True,
 'planeLevel': True,
 'planeType': True,
 'distanceToPlane': True,
 'strengthIndicator': True,
 'strength': True,
 'identicallyForAllMarkers': True,
 'strengthIndicatorType': 0}
LOCALIZATION_VALUE_MATRIX = {'value_-2': 'SETTINGS_MARKERS_COMBOBOX_DONT_SHOW',
 'value_-1': 'SETTINGS_MARKERS_COMBOBOX_ALWAYS_SHOW',
 'distanceOpacity_-2': 'SETTINGS_MARKERS_COMBOBOX_EQUAL_OPACITY',
 'distanceOpacity_-1': 'SETTINGS_MARKERS_COMBOBOX_ALWAYS_OPAQUE',
 'iconSize_0': 'SETTINGS_MARKERS_COMBOBOX_NORMAL',
 'iconSize_1': 'SETTINGS_MARKERS_COMBOBOX_LARGE',
 'iconSize_2': 'SETTINGS_MARKERS_COMBOBOX_HUGE',
 'typeStrength_0': 'SETTINGS_MARKERS_COMBOBOX_BAR',
 'typeStrength_1': 'SETTINGS_MARKERS_COMBOBOX_BAR_NUMBER',
 'typeStrength_2': 'SETTINGS_MARKERS_COMBOBOX_BAR_PERCENT',
 'typeStrength_3': 'SETTINGS_MARKERS_COMBOBOX_NUMBER',
 'typeStrength_4': 'SETTINGS_MARKERS_COMBOBOX_PERCENT',
 'typeHeight_0': 'SETTINGS_ALTIMETER_DROPDOWN_MENU_VARIANT_RADIO',
 'typeHeight_1': 'SETTINGS_ALTIMETER_DROPDOWN_MENU_VARIANT_BARO',
 'typeHeight_2': 'SETTINGS_MARKERS_COMBOBOX_REF_PLANE'}
TEMPLATES_FOR_PLANES_TYPES = [PLANE_TYPE.FIGHTER,
 PLANE_TYPE.NAVY,
 PLANE_TYPE.HFIGHTER,
 PLANE_TYPE.ASSAULT]
MATRIX_POSITION_SELECTED_PLANE = {0: 0,
 1: 1,
 2: 2,
 3: 3,
 4: 0,
 5: 1,
 6: 2,
 7: 3}
LOCALIZATION_PLANE_MATRIX = {'plane_base_0': 'SETTINGS_PLANE_TYPE_FIGHTER',
 'plane_base_1': 'SETTINGS_PLANE_TYPE_NAVY',
 'plane_base_2': 'SETTINGS_PLANE_TYPE_HEAVY_FIGHTER',
 'plane_base_3': 'SETTINGS_PLANE_TYPE_ASSAULT',
 'plane_modify_0': 'SETTINGS_USER_MARKER_TEMPLATE_FIGHTER',
 'plane_modify_1': 'SETTINGS_USER_MARKER_TEMPLATE_NAVY',
 'plane_modify_2': 'SETTINGS_USER_MARKER_TEMPLATE_HEAVY_FIGHTER',
 'plane_modify_3': 'SETTINGS_USER_MARKER_TEMPLATE_ASSAULT'}
MATRIX_VERIONS = {'distanceVisible': 'planeType',
 'showDistanceTo': 'distanceToPlane',
 'showStrength': 'strengthIndicator',
 'typeStrength': 'strengthIndicatorType',
 'showLevel': 'planeLevel',
 'showModelName': 'planeName',
 'showPlayerName': 'playerName'}
PATH_MODIFY_MARKER = 'markers/'
MARKERS_BASE_XML = DB_PATH + 'hud_markers_base.xml'
MARKERS_DATA_XML = DB_PATH + 'hud_markers_data.xml'
MARKERS_MODIFY_XML = 'hud_markers_modify.xml'
matrixSystems = dict()

def setMatrixSystem(metrSystem, footSystem):
    if metrSystem:
        matrixSystems[0] = metrSystem
    if footSystem:
        matrixSystems[1] = footSystem


def getValueBySystem(systemType, id):
    if matrixSystems and matrixSystems.get(systemType, None) is not None and matrixSystems.get(systemType, None).get(id, None) is not None:
        return matrixSystems[systemType][id]
    else:
        return 0


def localizeMarkerByPlane(isDefault, typePlane):
    return LOCALIZATION_PLANE_MATRIX.get('plane_' + ('base_' if isDefault else 'modify_') + typePlane.__str__(), '_empty_')


def localizeMarkerValues(key, value):
    v = value.__str__()
    return LOCALIZATION_VALUE_MATRIX.get(key + '_' + v, LOCALIZATION_VALUE_MATRIX.get('value_' + v, v))


def getTemplateIndexByPlaneType(planeType):
    if planeType not in TEMPLATES_FOR_PLANES_TYPES:
        return None
    else:
        return TEMPLATES_FOR_PLANES_TYPES.index(planeType)


def createAppMarkerPath():
    path = os.path.join(BigWorld.getUserDataDirectory(), PATH_MODIFY_MARKER)
    try:
        os.mkdir(path)
    except OSError:
        pass


def convertStrengthVisible(typeMarker, target, state, strength, strengthIndicator):
    if strength == False and strengthIndicator == False:
        return {'showStrength': 0}
    if typeMarker == 'airMarker':
        if state == 'basic':
            return {'showStrength': 3}
        if state == 'alt':
            return {'showStrength': 8}
    if typeMarker == 'groundMarker':
        if target == 'enemy' or target == 'friendly':
            if state == 'basic':
                return {'showStrength': 3}
            if state == 'alt':
                return {'showStrength': 6}
        if target == 'target':
            return {'showStrength': 6}
    return False


def convertStrength(strengthIndicator, strength, strengthIndicatorType):
    if strengthIndicator == False:
        if strength == True:
            if strengthIndicatorType == 1:
                return {'typeStrength': 0}
            if strengthIndicatorType == 0:
                return {'typeStrength': 0}
    if strengthIndicator == True:
        if strength == False:
            if strengthIndicatorType == 1:
                return {'typeStrength': 4}
            if strengthIndicatorType == 0:
                return {'typeStrength': 3}
        if strength == True:
            if strengthIndicatorType == 1:
                return {'typeStrength': 2}
            if strengthIndicatorType == 0:
                return {'typeStrength': 1}
    return 0


def convertMarkerByType(altState):
    if altState:
        return 8
    return 6


MATRIX_VERIONS_VALUES_PLANE = {'distanceVisible': 8,
 'distanceOpacity': 6,
 'iconSize': {'target': 2,
              'enemy': 1,
              'friendly': 1,
              'squads': 1},
 'showLevel': {'True': convertMarkerByType,
               'False': 0},
 'showModelName': {'True': convertMarkerByType,
                   'False': 0},
 'showPlayerName': {'True': convertMarkerByType,
                    'False': 0},
 'showDistanceTo': {'True': convertMarkerByType,
                    'False': 0},
 'typeHeight': 2,
 'showStrength': convertStrengthVisible,
 'typeStrength': convertStrength}
MATRIX_VERIONS_VALUES_GROUND = {'distanceVisible': 6,
 'distanceOpacity': 4,
 'iconSize': {'target': 2,
              'enemy': 1,
              'friendly': 1,
              'squads': 1},
 'showDistanceTo': {'True': 6,
                    'False': 0},
 'showStrength': convertStrengthVisible,
 'typeStrength': convertStrength,
 'showShootObject': 3,
 'showArmoredParts': 3,
 'showUnarmoredParts': 3,
 'showModelName': {'True': 6,
                   'False': 0}}
MATRIX_MARKER_TARGET_TYPE = {MARKER_TARGET_TYPE[0]: MATRIX_VERIONS_VALUES_PLANE,
 MARKER_TARGET_TYPE[1]: MATRIX_VERIONS_VALUES_GROUND}

def convertMarkersVersion(targetMarker, typeMarker, altState, param, preMarkers, values):
    res = list()
    if param == 'typeHeight':
        return values
    elif targetMarker == 'groundMarker' and typeMarker == 'squads':
        return values
    else:
        if param == 'showShootObject' or param == 'showArmoredParts' or param == 'showUnarmoredParts':
            if typeMarker != 'target':
                return values
        preMarkParam = MATRIX_VERIONS.get(param, None)
        matrixVersion = MATRIX_MARKER_TARGET_TYPE.get(targetMarker, None)
        if preMarkParam is None:
            m = matrixVersion.get(param, None)
            if param == 'iconSize':
                val = m.get(typeMarker, None)
                if val is not None:
                    return __setValueAtMarker(len(values), val)
            if m is not None and type(m) in [int,
             float,
             bool,
             str]:
                res = __setValueAtMarker(len(values), m)
                return res
            else:
                return values
        else:
            m = matrixVersion.get(param, None)
            v = preMarkers[typeMarker][altState][preMarkParam]
            if param == 'typeStrength':
                sIndicatorType = preMarkers[typeMarker][altState].get('strengthIndicatorType', None)
                sIndicator = preMarkers[typeMarker][altState].get('strengthIndicator', None)
                sStrength = preMarkers[typeMarker][altState].get('strength', None)
                if sIndicator is not None:
                    val = m(sIndicator, sStrength, sIndicatorType)
                    if type(val) in [dict]:
                        return __setValueAtMarker(len(values), val.get(param, None))
            if param == 'showStrength':
                sIndicator = preMarkers[typeMarker][altState].get('strengthIndicator', None)
                sStrength = preMarkers[typeMarker][altState].get('strength', None)
                val = m(targetMarker, typeMarker, altState, sStrength, sIndicator)
                if type(val) in [dict]:
                    return __setValueAtMarker(len(values), val.get(param, None))
            if m is not None and type(m) in [dict]:
                val = m.get(str(v), None)
                if val is not None and type(val) in [int,
                 float,
                 bool,
                 str]:
                    res = __setValueAtMarker(len(values), val)
                else:
                    res = __setValueAtMarker(len(values), val(altState == 'alt'))
            if m is not None and type(m) in [int,
             float,
             bool,
             str]:
                res = __setValueAtMarker(len(values), m)
            if res and len(res) > 1:
                return res
        return values


def __setValueAtMarker(l, v):
    return [v] * l