# Embedded file name: scripts/client/gui/Scaleform/utils/HangarSpace.py
from gui.ClientHangarSpace import ClientHangarSpace
from gui.Scaleform.Waiting import Waiting, WaitingFlags
from debug_utils import LOG_DEBUG, LOG_TRACE
import Event
import BigWorld
from consts import *
from clientConsts import HANGAR_LOBBY_WAITING_SCREEN_MESSAGE, HANGAR_VEHICLE_SWITCHING_WAIT_FRAMES
from functools import partial
import GlobalEvents

class _HangarSpace(object):
    profiler_vehicle = BigWorld.ProfilerEvent('VehicleLoading')

    def __init__(self):
        self.__space = ClientHangarSpace()
        self.__inited = False
        self.__isSpacePremium = False
        self.__spaceLoaded = False
        self.__delayedSpaceData = None
        self.__isVechicleLoading = False
        self.__delayedVechicleData = None
        self.__freeze = False
        self.eOnVehicleStart = Event.Event()
        self.eOnVehicleLoaded = Event.Event()
        self.__dbgHangarFlyingMode = False
        return

    def init(self, hangarConfig, overrideSpace = None):
        if not self.__inited:
            LOG_TRACE('_HangarSpace::init')
            self.setFreeze(False)
            self.__inited = True
            self.__loadHangarSpace(hangarConfig, overrideSpace)

    def destroy(self):
        self.__inited = False
        self.__isVechicleLoading = False
        self.__delayedSpaceData = None
        self.__delayedVechicleData = None
        self.eOnVehicleStart.clear()
        self.eOnVehicleLoaded.clear()
        if self.__spaceLoaded:
            LOG_TRACE('_HangarSpace::destroy')
            self.__spaceLoaded = False
            self.__space.destroy()
        return

    @property
    def isVSEPlansStarted(self):
        if self.space:
            return self.space.vsePlansStarted
        return False

    def refreshDecals(self):
        modelManipulator = self.space.getModelManipulator() if self.space else None
        if modelManipulator is not None:
            modelManipulator.surface.refreshClanEmblem()
        return

    def refreshSpace(self, hangarConfig, overrideSpace = None):
        LOG_TRACE('_HangarSpace::refreshSpace', hangarConfig, self.__inited, self.__freeze, self.__hangarConfig)
        if self.__inited and not self.__freeze:
            if self.__hangarConfig != hangarConfig or overrideSpace:
                self.__loadHangarSpace(hangarConfig, overrideSpace)

    @property
    def isAircraftLoaded(self):
        return self.space is not None and self.space.getModelManipulator() is not None and not self.__inLoading()

    def refreshVehicle(self, vehicleInfo):
        if self.__inited and not self.__freeze:
            if self.__inLoading():
                self.__delayedVechicleData = (vehicleInfo,)
            elif vehicleInfo:
                vehicleInfo.isVehicleLoaded = False
                self.__isVechicleLoading = True
                _HangarSpace.profiler_vehicle.start()
                self.eOnVehicleStart()
                self.__space.recreateVehicle(vehicleInfo, self.__vechicleDone, self.__dbgHangarFlyingMode)
            else:
                self.__space.removeVehicle()

    @property
    def space(self):
        if self.__spaceLoaded:
            return self.__space
        else:
            return None

    def setFreeze(self, freeze):
        LOG_TRACE('_HangarSpace::setFreeze', freeze)
        self.__freeze = freeze

    def refreshSpaceSound(self, category, value):
        if category == 'music':
            self.__space.refreshSpaceSound(value)

    def __vechicleDone(self):
        LOG_TRACE('_HangarSpace::__vechicleDone')
        self.__isVechicleLoading = False
        self.__checkDelayedData()
        self.eOnVehicleLoaded()
        _HangarSpace.profiler_vehicle.end()

    def __inLoading(self):
        return self.__space.spaceLoading() or self.__isVechicleLoading

    def __loadHangarSpace(self, hangarConfig, overrideSpace = None):
        LOG_TRACE('_HangarSpace::__loadHangarSpace', self.__space.spaceLoading(), self.__isVechicleLoading)
        if self.__inLoading():
            LOG_TRACE('_HangarSpace::__loadHangarSpace(hangarConfig=' + str(hangarConfig) + ') - is delayed until space load is done')
            self.__delayedSpaceData = (hangarConfig, overrideSpace)
        else:
            camTargetShifted = False
            if self.__spaceLoaded:
                camTargetShifted = self.__space.hangarCamera.getStateObject().targetShifted
                self.__spaceLoaded = False
                self.__space.destroy()
            waitingID = Waiting.show(HANGAR_LOBBY_WAITING_SCREEN_MESSAGE, WaitingFlags.WORLD_DRAW_DISABLE | WaitingFlags.LOADING_FPS_MODE)
            self.__hangarConfig = hangarConfig
            self.__space.create(hangarConfig, partial(self.__spaceDone, waitingID), overrideSpace=overrideSpace)
            self.__space.hangarCamera.getStateObject().setCameraTargetShift(camTargetShifted)

    def __spaceDone(self, waitingID):
        LOG_TRACE('_HangarSpace::__spaceDone', self.__inited)
        self.__spaceLoaded = True
        self.__space.onSpaceLoaded()
        if not self.__inited:
            self.destroy()
        else:
            self.__checkDelayedData()
        GlobalEvents.onHangarLoaded()
        Waiting.hide(waitingID)

    def __checkDelayedData(self):
        LOG_TRACE('_HangarSpace::__checkDelayedData', self.__inited, self.__delayedSpaceData, self.__delayedVechicleData)
        if self.__inited:
            if self.__delayedSpaceData is not None:
                self.__loadHangarSpace(*self.__delayedSpaceData)
                self.__delayedSpaceData = None
            elif self.__delayedVechicleData:
                vechicleData = self.__delayedVechicleData[0]
                self.__delayedVechicleData = None
                self.refreshVehicle(vechicleData)
        return

    def dbgChangeSpace(self, name):
        if self.__inited and not self.__freeze:
            self.__loadHangarSpace(self.__hangarConfig, overrideSpace=name)
            self.dbgHangarFlyingMode(self.__dbgHangarFlyingMode, forceReload=True)

    def dbgHangarFlyingMode(self, enable = True, forceReload = False):
        if self.__dbgHangarFlyingMode == enable and not forceReload:
            return
        self.__dbgHangarFlyingMode = enable
        from BWPersonality import g_lobbyCarouselHelper
        vehicleInfo = g_lobbyCarouselHelper.getCarouselAirplaneSelected()
        if self.__inited and not self.__freeze:
            self.refreshVehicle(vehicleInfo)

    def dbgSwitchCameraView(self, camView):
        if self.__inited and not self.__freeze:
            self.__space.dbgSwitchCameraView(camView)

    def dbgRotateTurrets(self, command):
        if self.__inited and not self.__freeze:
            self.__space.dbgRotateTurrets(command)

    def dbgShowBBoxes(self, show):
        self.__space.dbgShowBBoxes(show)

    def switchHangarPremiumType(self):
        self.refreshSpace('premium' if self.__hangarConfig == 'basic' else 'basic')


g_hangarSpace = _HangarSpace()