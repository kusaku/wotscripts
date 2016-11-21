# Embedded file name: scripts/common/items/vehicle_config_types.py
from collections import namedtuple
LodSettings = namedtuple('LodSettings', ['maxLodDistance', 'maxPriority'])
LeveredSuspensionConfig = namedtuple('LeveredSuspensionConfig', ['levers', 'interpolationSpeedMul', 'lodSettings'])
SuspensionLever = namedtuple('SuspensionLever', ['startNodeName',
 'jointNodeName',
 'trackNodeName',
 'minAngle',
 'maxAngle'])
SoundSiegeModeStateChange = namedtuple('SoundSiegeModeStateChange', ['on', 'off'])