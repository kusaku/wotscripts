# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/HUDSettingsVO.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import ArrayIndex
from gui.Scaleform.GameOptions.vo import MarkerSettings

class GeneralVO:

    def __init__(self):
        self.isLazy = False
        self.blockWinButton = False
        self.blockAltTAB = False
        self.cinemaCamera = False
        self.freezeCamera = False
        self.collisionWarningSystem = False
        self.alternativeColorMode = False
        self.isSniperMode = False
        self.preIntroEnabled = True
        self.FOVCamera = 90.0


class DevicesVO:

    def __init__(self):
        self.isLazy = False
        self.aviaHorizon = False
        self.aviaHorizonType = ArrayIndex()
        self.playerList = False
        self.playerListType = ArrayIndex()
        self.navigationWindowRadar = False
        self.navigationWindowMinimap = False
        self.additionalView = False
        self.heightMode = ArrayIndex()
        self.speedometerAndVariometer = False
        self.combatInterfaceType = False


class AimVO:

    def __init__(self):
        self.isLazy = False
        self.crosshairShape = ArrayIndex()
        self.crosshairColor = ArrayIndex()
        self.targetAreaShape = ArrayIndex()
        self.targetAreaColor = ArrayIndex()
        self.externalAimShape = ArrayIndex()
        self.crosshairTransparency = True
        self.targetAreaTransparency = True
        self.externalAimTransparency = True
        self.dynamycAim = True


class MarkerListVO:

    def __init__(self):
        self.isLazy = False
        self.label = ''
        self.num = -1


class MarkerVO:

    def __init__(self):
        for key in MarkerSettings.MARKER_TARGET_TYPE:
            setattr(self, key, MarkerDataVO())


class MarkerDataVO:

    def __init__(self):
        self.isLazy = False
        for key in MarkerSettings.AVAILABLE_MARKER_PROPERTIES:
            setattr(self, key, MarkerAdditionalVO())


class MarkerAdditionalVO:

    def __init__(self):
        self.isLazy = False
        self.title = ''
        self.tooltip = 'test tooltip'
        self.data = list()


class MarkerIndexVO:

    def __init__(self):
        self.isLazy = False
        for key in MarkerSettings.AVAILABLE_MARKER_PROPERTIES:
            setattr(self, key, -1)


class MarkerBasicAltVO:

    def __init__(self):
        self.isLazy = False
        self.basic = MarkerIndexVO()
        self.alt = MarkerIndexVO()


class MarkerAllVO:

    def __init__(self):
        self.isLazy = False
        self.enemy = MarkerBasicAltVO()
        self.target = MarkerBasicAltVO()
        self.friendly = MarkerBasicAltVO()
        self.squads = MarkerBasicAltVO()
        self.altCmd = -1


class MarkerTargetsVO:

    def __init__(self):
        self.label = 'test label'
        self.airMarker = MarkerAllVO()
        self.groundMarker = MarkerAllVO()


class MarkerTypeSystemVO:

    def __init__(self):
        self.isLazy = False
        self.selectIDS = [0,
         1,
         2,
         3]
        self.selectedSystemType = 0
        self.templates = list()
        self.systemType = list()


class MarkerTypeVO:

    def __init__(self):
        self.isLazy = False
        self.stepsDistance = list()
        self.data = MarkerVO()


class ForestallingPointVO:

    def __init__(self):
        self.isShowAdvancePoint = True
        self.isToBoundary = True
        self.isSize = True
        self.isBestTime = True
        self.colorPoint = ArrayIndex()
        self.isEnabled = True


class AimsVO:

    def __init__(self):
        self.mouseAim = AimVO()
        self.joystickAim = AimVO()
        self.gamepadAim = AimVO()


class HUDSettingsVO:

    def __init__(self):
        self.isLazy = False
        self.general = GeneralVO()
        self.devices = DevicesVO()
        self.aim = AimsVO()
        self.markers = MarkerTypeSystemVO()
        self.forestallingPoint = ForestallingPointVO()