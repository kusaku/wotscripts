# Embedded file name: scripts/client/PostProcessing/Effects/LightShafts.py
from PostProcessing.RenderTargets import *
from PostProcessing.Phases import *
from PostProcessing import Effect
from PostProcessing.Effects import implementEffectFactory

@implementEffectFactory('Volumetric Light Shafts', 'Volumetric light shafts effect (god rays)')
def lightShafts():
    """This method creates and returns a post-process effect that performs
    light shafts effect."""
    backBufferCopy = rt('backBufferCopy')
    downSample2 = rt('downSample2')
    downSample2B = rt('downSample2B')
    cloudsThickness = rt('CloudsThicknessInfo')
    pre = buildBackBufferCopyPhase(backBufferCopy)
    d1 = buildDownSamplePhase(backBufferCopy.texture, downSample2)
    bh = buildBlurPhase(downSample2.texture, downSample2B, True, 0, 1.0)
    bv = buildBlurPhase(downSample2B.texture, downSample2, False, 0, 1.0)
    sgm = Phase()
    sgm.name = 'Sun glow mask'
    sgm.material = Material('shaders/post_processing/light_shafts_sun_glow_mask.fx')
    sgm.material.inputTexture = downSample2.texture
    sgm.material.sunGlowMask = 'system/maps/post_processing/SunRadialGlow_Mask.dds'
    sgm.material.cloudsDepthInfo = cloudsThickness.texture
    sgm.renderTarget = downSample2B
    sgm.filterQuad = TransferQuad()
    rb = Phase()
    rb.name = 'Radial blur'
    rb.material = Material('shaders/post_processing/light_shafts_radial_blur.fx')
    rb.material.inputTexture = backBufferCopy.texture
    rb.material.glowMaskTexture = downSample2B.texture
    rb.renderTarget = None
    rb.filterQuad = TransferQuad()
    e = Effect()
    e.name = 'Light Shafts'
    phases = [pre,
     d1,
     bh,
     bv,
     sgm,
     rb]
    e.phases = phases
    return e