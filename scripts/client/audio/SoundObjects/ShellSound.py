# Embedded file name: scripts/client/audio/SoundObjects/ShellSound.py
from WwiseGameObject import WwiseGameObject, GS
import BigWorld
import db.DBLogic
import math
import GameEnvironment
import Settings
from audio.AKTunes import RTPC_Zoomstate_MAX, FREECAM_DIST_STEP
from debug_utils import LOG_INFO

class ShellSound(WwiseGameObject):

    def __init__(self, name, cid, node, position, sndId, isPlayer = True):
        tag = 'WeaponShooting{0}'.format('Player' if isPlayer else 'NPC', None)
        self.__ev = db.DBLogic.g_instance.getWeaponSoundSet(sndId).get(tag)
        if not self.__ev:
            LOG_INFO('[Audio] missed <{0}> for {1}'.format(tag, sndId))
            return
        else:
            cam = GameEnvironment.getCamera()
            cam.eZoomStateChanged += self.__onZoomStateChanged
            cam.eDistanceChanged += self.__onDistanceChanged
            BigWorld.player().eLeaveWorldEvent += self.stop
            WwiseGameObject.__init__(self, name, cid, node, position)
            self.__onZoomStateChanged(Settings.g_instance.camZoomIndex)
            return

    def play(self):
        if GS().isReplayMute:
            return
        self.postEvent(self.__ev, self.destroy)

    def stop(self):
        self.postEvent(str(self.__ev).replace('Play_', 'Stop_'))

    def __onZoomStateChanged(self, val):
        self.__RTPC_Zoomstate(RTPC_Zoomstate_MAX - val)

    def __onDistanceChanged(self, d):
        self.__RTPC_Zoomstate(math.floor(d / FREECAM_DIST_STEP))

    def __RTPC_Zoomstate(self, val):
        self.setRTPC('RTPC_Aircraft_Camera_Zoomstate', min(max(0, val), RTPC_Zoomstate_MAX), 0)