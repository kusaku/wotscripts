# Embedded file name: scripts/common/CameraEffectsSettings.py
from consts import COLLISION_TYPE_WATER, COLLISION_TYPE_GROUND
AOI_EFFECT_CHECK_FREQUENCY = 0.1
GROUND_EFFECTS_GEN_FREQUENCY = 0.1
MAX_DIST_TO_TERRAIN = 50
DEFAULT_AIR_EFFECTS_FADE_TIME = 1
effects = {COLLISION_TYPE_WATER: (2, 'over_water', 'airplane_over_water'),
 COLLISION_TYPE_GROUND: (0, 'snow_drop', 'airplane_over_ground')}