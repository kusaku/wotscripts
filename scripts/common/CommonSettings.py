# Embedded file name: scripts/common/CommonSettings.py
__author__ = 'm_kobets'
import math
from consts import WORLD_SCALING

def km_to_m(value):
    return value / 3.6


def m_to_km(value):
    return value * 3.6


def dtc(init_diction):
    """
    :param init_diction: diction
    :return: obj
    """

    class DictToCls(object):

        def __init__(self, init_dict):
            self.__dict__ = init_dict

            def __setattr__dummy(*a, **k):
                raise SyntaxError

            DictToCls.__setattr__ = __setattr__dummy

    if isinstance(init_diction, dict):
        return DictToCls(init_diction)
    raise AttributeError


class SensitivityScale_PillowSettings:
    h1 = 2 * WORLD_SCALING
    h2 = 20 * WORLD_SCALING
    min_sens = 0.25


class ModifyDirection_PillowSettings:
    h1 = 1 * WORLD_SCALING
    low_height_timing = 0.5
    h2_speed_norma1 = 10 * WORLD_SCALING
    h2_speed_norma2 = 15 * WORLD_SCALING
    speed_norma1 = 200.0 / 3.6
    speed_norma2 = 500.0 / 3.6
    horizon_angle1 = math.radians(10)
    horizon_angle2 = math.radians(45)


pillowSetting = {'normal_collision_range': 200.0 * WORLD_SCALING,
 'normal_speed': km_to_m(400),
 'stall_speed_cfc1': 1,
 'stall_speed_cfc2': 1.5,
 'up_angle_min': math.radians(45),
 'up_angle_max': math.radians(100),
 'pitch_boost_cfc': 1.75,
 'static_collision_range_cfc': 0.2,
 'back_angle_one': math.radians(90),
 'back_angle_two': math.radians(95),
 'static_normal_speed': km_to_m(1000),
 'static_normal_speed_tau': 2,
 'static_stall_speed_tau': 2.0,
 'absorption_speed_cfc': 1,
 'activate_pitch_rudder_value': 0.2,
 'dive_speed_tau': 0.5,
 'stall_speed_tau': 4,
 'dive_normal_angle1': math.radians(10),
 'dive_normal_angle2': math.radians(95),
 'control_up_effect_angle1': math.radians(30),
 'control_up_effect_angle2': math.radians(80)}