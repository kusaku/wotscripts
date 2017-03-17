# Embedded file name: scripts/client/gui/HangarScripts/PlaneBirthday/Script.py
import BigWorld
import EffectManager
from debug_utils import LOG_ERROR, LOG_DEBUG
from db.DBEffects import Effects
from gui.HangarScripts import HangarScriptBase

class Script(HangarScriptBase):

    def __init__(self):
        super(Script, self).__init__()
        self.__model = None
        self.__effects = None
        self.__isEnabled = False
        return

    def onHangarLoaded(self):
        from gui.Scaleform.utils.HangarSpace import g_hangarSpace
        from gui.HangarScripts.PlaneBirthday import ConfigFactory
        if self.__isEnabled or not g_hangarSpace.space:
            return
        config = ConfigFactory.get(g_hangarSpace.space.spaceName)
        self.__model = BigWorld.Model(config.MODEL_NAME)
        if self.__model:
            EffectManager.Init()
            self.__model.scale = config.SCALE
            self.__model.actionScale = 4.0
            self.__model.visible = False
            BigWorld.addModel(self.__model, BigWorld.player().spaceID)
            self.__model.position = g_hangarSpace.space.getHangarPos() + config.TRANSLATION_VECTOR
            self.__model.visible = True
            action = self.__model.action(config.ANIMATION_NAME)
            action()
            LOG_DEBUG('onHangarLoaded hp', [ (hp, self.__model.node(hp)) for i, hp in enumerate(config.PARTICLE_HPS) ])
            self.__effects = [ EffectManager.g_instance.createNodeAttachedEffect(Effects.getEffectId(config.PARTICLE_NAMES[i]), self.__model.node(hp), {}) for i, hp in enumerate(config.PARTICLE_HPS) ]
        else:
            LOG_ERROR("can't load model", config.MODEL_NAME)
        self.__isEnabled = True

    def onHangarUnloaded(self):
        if not self.__isEnabled:
            return
        else:
            if self.__model:
                for effect in self.__effects:
                    effect.destroy()

                self.__effects = None
                BigWorld.delModel(self.__model)
                self.__model = None
            self.__isEnabled = False
            return