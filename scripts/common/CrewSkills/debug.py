# Embedded file name: scripts/common/CrewSkills/debug.py
from config_consts import IS_DEVELOPMENT
from _skills_data import SpecializationEnum
ENABLED = False
DEBUG_SKILLS = {SpecializationEnum.PILOT: ['PILOT_S_CRUISEFLIGHT', 'PILOT_S_FIREMANUVER'],
 SpecializationEnum.GUNNER: ['GUNNER']}
PRESETS = {'P-40': ['PILOT_S_BLOODLUST', 'PILOT_S_BOOMZOOM', 'PILOT_S_CRUISEFLIGHT'],
 'P-40-M-105': ['PILOT_S_DIEHARD', 'PILOT_S_EVASIONMANUVER', 'PILOT_S_FIREMANUVER'],
 'Tomahawk-IIB': ['PILOT_S_BLOODLUST', 'PILOT_S_CRUISEFLIGHT', 'PILOT_S_EVASIONMANUVER'],
 'IL-2mod': ['PILOT_S_DIEHARD',
             'PILOT_S_EVASIONMANUVER',
             'PILOT_S_CRUISEFLIGHT',
             'GUNNER_PROTECTOR',
             'GUNNER_PUNISHER',
             'GUNNER_VOLLEY'],
 'Ju-87G': ['PILOT_S_DIEHARD',
            'PILOT_S_EVASIONMANUVER',
            'PILOT_S_CRUISEFLIGHT',
            'GUNNER_KILLER',
            'GUNNER_NIMBLE',
            'GUNNER_LONGRANGE']}

def __xreload_old_new__(namespace, name, oldObj, newObj):
    namespace[name] = newObj