# Embedded file name: scripts/client/gui/HangarScripts/PlaneBirthday/ConfigFactory.py
from debug_utils import LOG_DEBUG

def get(spaceID):
    from BWPersonality import g_settings as bw
    from db.DBLogic import g_instance as db
    from gui.HangarScripts.PlaneBirthday import Config
    hangarSpace = db.userHangarSpaces[spaceID]
    return Config.MAPPING[hangarSpace.get('premiumType', 'basic')]