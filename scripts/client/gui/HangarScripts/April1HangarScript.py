# Embedded file name: scripts/client/gui/HangarScripts/April1HangarScript.py
from HangarScriptBase import HangarScriptBase
import BigWorld
from debug_utils import LOG_DEBUG, LOG_ERROR
import EffectManager
from db.DBEffects import Effects
from modelManipulator.CompoundBuilder import syncHpMap
import Math
from functools import partial
from WWISE_ import SoundObject
MODEL_NAME = 'content/00_05_hangar_premium_april_1/Plane/Plane.model'
HP_NAME = 'content/00_05_hangar_premium_april_1/Plane/Plane_anim_HP.model'
ATTACH_HP = 'HP_smile'
ANIMATION_NAME = 'Plane_anim_action'
PARTICLE_NAME = 'april_hangar_plane_trail'
PLAY_SOUND_NAME = 'Play_hangar_1st_of_April_plane'
STOP_SOUND_NAME = 'Stop_hangar_1st_of_April_plane'
PLANE_SOUND_DESTROY_DELAY = 15.0
HANGAR_INIT_DELAY = 1.0

class April1HangarScript(HangarScriptBase):

    def __init__(self):
        super(HangarScriptBase, self).__init__()
        LOG_DEBUG('April1HangarScript constructor')
        self.__model = None
        self.__effect = None
        self.__hangarLoaded = False
        self.__delayedInitCB = None
        return

    def __clear(self):
        if self.__effect:
            self.__effect.destroy()
            self.__effect = None
        if self.__model:
            BigWorld.delModel(self.__model)
            self.__model = None
        self.__soPlane = None
        return

    def __initHangar(self):
        from gui.Scaleform.utils.HangarSpace import g_hangarSpace
        if self.__delayedInitCB:
            BigWorld.cancelCallback(self.__delayedInitCB)
            self.__delayedInitCB = None
        self.__clear()
        if g_hangarSpace and g_hangarSpace.space:
            self.__model = BigWorld.Model(MODEL_NAME)
            if self.__model:
                self.__model.scale = (0.6, 0.6, 0.6)
                self.__model.actionScale = 0.5
                BigWorld.addModel(self.__model, g_hangarSpace.space.spaceID)
                positionHpMap = syncHpMap(HP_NAME)
                LOG_DEBUG('found HPs', positionHpMap)
                for k, hp in positionHpMap.iteritems():
                    self.__model.position = Math.Matrix(hp).translation
                    break

                self.__model.visible = True
                action = self.__model.action(ANIMATION_NAME)
                action()
                self.__effect = EffectManager.g_instance.createNodeAttachedEffect(Effects.getEffectId(PARTICLE_NAME), self.__model.node(ATTACH_HP), {})
                self.__soPlane = SoundObject('hangar_1st_of_April_plane', 0, 0)
                self.__soPlane.transform = self.__model.node(ATTACH_HP)
                self.__soPlane.postEvent(PLAY_SOUND_NAME, False, None)
                LOG_DEBUG('effect', PARTICLE_NAME, self.__effect)
                self.__hangarLoaded = True
            else:
                LOG_ERROR("can't load 1 april model", MODEL_NAME)
        else:
            self.__delayedInitCB = BigWorld.callback(HANGAR_INIT_DELAY, self.__initHangar)
        return

    def onHangarLoaded(self):
        EffectManager.Init()
        self.__initHangar()

    def __postponeDestroy(self, sound):
        if sound:
            sound.destroy()
            sound = None
        return

    def onHangarUnloaded(self):
        if self.__delayedInitCB:
            BigWorld.cancelCallback(self.__delayedInitCB)
            self.__delayedInitCB = None
        if self.__hangarLoaded:
            if self.__soPlane:
                cam = BigWorld.camera()
                if cam:
                    soundPos = Math.Matrix(self.__soPlane.transform).translation
                    offsMatrix = Math.Matrix()
                    offsMatrix.translation = soundPos - cam.position
                    matProduct = Math.MatrixProduct()
                    matProduct.b = offsMatrix
                    matProduct.a = cam.invViewMatrix
                    self.__soPlane.transform = matProduct
                else:
                    self.__soPlane.position = Math.Vector3(0.0, 0.0, 0.0)
                    self.__soPlane.transform = None
                self.__soPlane.postEvent(STOP_SOUND_NAME, False, None)
                BigWorld.callback(PLANE_SOUND_DESTROY_DELAY, partial(self.__postponeDestroy, self.__soPlane))
                self.__soPlane = None
        self.__clear()
        self.__hangarLoaded = False
        return