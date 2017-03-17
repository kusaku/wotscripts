# Embedded file name: scripts/client/gui/HangarScripts/__init__.py
from HangarScriptBase import HangarScriptBase
from NewYearHangarScript import NewYearHangarScript
from Hangar4Script import Hangar4Script
from Hangar5Script import Hangar5Script
from April1HangarScript import April1HangarScript
from PlaneBirthday import Script as birthday
from HangarNY2016Script import HangarNY2016Script
SCRIPTS_MAP = {'default': HangarScriptBase(),
 'planebirthday': birthday.Script(),
 '00_07_hangar_premium_ny_2016': HangarNY2016Script(),
 '00_09_hangar_premium_ny_china_2016': HangarNY2016Script()}

def getHangarScriptsByName(spaceName):
    return SCRIPTS_MAP.get(spaceName.lower(), SCRIPTS_MAP['default'])