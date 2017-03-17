# Embedded file name: scripts/client/audio/SoundObjects/EffectSound.py
from WwiseGameObject import WwiseGameObject, GS
import db.DBLogic

class EffectSound(WwiseGameObject):

    def __init__(self, name, cid, node, position = None):
        if GS().isReplayMute:
            return
        ev = db.DBLogic.g_instance.getEffectSound(name)
        if not ev:
            return
        WwiseGameObject.__init__(self, 'Effect-{0}'.format(name), cid, node, position)
        self.postEvent(ev, self.destroy)

    def stop(self):
        self.stopAll(1000)