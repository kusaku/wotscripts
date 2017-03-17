# Embedded file name: scripts/client/gui/HangarScripts/PlaneBirthday/Config.py
import Math

class HangarConfig(object):
    PARTICLE_NAMES = ['angar_birthday_dust', 'angar_birthday_volcano']
    PARTICLE_HPS = ['HP_dust', 'HP_volcano_1']


class HangarBasicConfig(HangarConfig):
    TRANSLATION_VECTOR = Math.Vector3(0.2, 0.0, -0.2)
    SCALE = (0.22, 0.22, 0.22)
    MODEL_NAME = 'content/Event_planes_birthday_02/Event_planes_birthday_02_base.model'
    ANIMATION_NAME = 'Event_planes_birthday_02'


class HangarPremCLConfig(HangarConfig):
    TRANSLATION_VECTOR = Math.Vector3(0.2, 0.0, -0.2)
    SCALE = (0.22, 0.22, 0.22)
    MODEL_NAME = 'content/Event_planes_birthday_02/Event_planes_birthday_02.model'
    ANIMATION_NAME = 'Event_planes_birthday_02'


class HangarPremOPConfig(HangarConfig):
    TRANSLATION_VECTOR = Math.Vector3(0.0, 0.0, 0.0)
    SCALE = (0.22, 0.22, 0.22)
    MODEL_NAME = 'content/Event_planes_birthday_02/Event_planes_birthday_02.model'
    ANIMATION_NAME = 'Event_planes_birthday_02'


class HangarPrem2OPConfig(HangarConfig):
    TRANSLATION_VECTOR = Math.Vector3(0.0, 0.0, 0.0)
    MODEL_NAME = 'content/Event_planes_birthday_02/Event_planes_birthday_02.model'
    SCALE = (0.22, 0.22, 0.22)
    ANIMATION_NAME = 'Event_planes_birthday_02'


MAPPING = dict(basic=HangarBasicConfig, CL=HangarPremCLConfig, OP=HangarPremOPConfig, OPNY=HangarPrem2OPConfig)