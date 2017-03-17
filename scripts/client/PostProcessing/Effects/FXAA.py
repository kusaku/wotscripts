# Embedded file name: scripts/client/PostProcessing/Effects/FXAA.py
from PostProcessing.RenderTargets import *
from PostProcessing.Phases import *
from PostProcessing import Effect
from PostProcessing.Effects import implementEffectFactory

@implementEffectFactory('FXAA', 'Perform Fast Approximate Anti-Aliasing on the contents of the back buffer.')
def fxaa():
    """This method creates and returns an effect that performs
    Fast Approximate Anti-Aliasing (FXAA) on the contents of the back buffer."""
    backBufferCopy = rt('backBufferCopy')
    e = Effect()
    e.name = 'FXAA'
    c = buildBackBufferCopyPhase(backBufferCopy)
    p = buildFXAAPhase(backBufferCopy.texture, None)
    phases = [c, p]
    e.phases = phases
    return e