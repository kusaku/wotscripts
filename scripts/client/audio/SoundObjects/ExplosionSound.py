# Embedded file name: scripts/client/audio/SoundObjects/ExplosionSound.py
from WwiseGameObject import WwiseGameObject
import BigWorld

class ExplosionSound(WwiseGameObject):
    AVATAR_EXPLOSION = 'Play_explosion_avatar'
    NPC_EXPLOSION = 'Play_explosion_npc'
    NPC_EXPOSION_FRAG = 'Play_explosion_npc_frag'

    def __init__(self, ev, pos):
        WwiseGameObject.__init__(self, 'ExplosionSound-{0}'.format(ev), 0, 0, pos)
        if hasattr(BigWorld.player(), 'eLeaveWorldEvent'):
            BigWorld.player().eLeaveWorldEvent += self.destroy
        self.postEvent(ev, self.destroy)