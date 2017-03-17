# Embedded file name: scripts/client/PostProcessing/Effects/CloudsOverbright.py
from PostProcessing.RenderTargets import *
from PostProcessing.Phases import *
from PostProcessing import Effect
from PostProcessing.Effects import implementEffectFactory

@implementEffectFactory('Clouds edge overbright', 'Highlight semitransparent edges of clouds.')
def cloudsOverbright():
    """This method creates and returns a post-process effect that performs
    clouds edge overbright."""
    cloudThickness = rt('CloudsThicknessInfo')
    p = Phase()
    p.material = Material('shaders/post_processing/clouds_overbright.fx')
    p.material.inputTexture = cloudThickness.texture
    p.renderTarget = None
    p.filterQuad = TransferQuad()
    co = Effect()
    co.name = 'Cloud overbright'
    co.phases = [p]
    return co