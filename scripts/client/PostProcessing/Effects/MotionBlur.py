# Embedded file name: scripts/client/PostProcessing/Effects/MotionBlur.py
from PostProcessing.RenderTargets import *
from PostProcessing import Effect
from PostProcessing.Phases import *
from PostProcessing.FilterKernels import *
from PostProcessing import chain
from PostProcessing.Effects.Properties import *
from PostProcessing.Effects import implementEffectFactory
import Math
velocityStrength = MaterialFloatProperty('MotionBlur', 1, 'strength', primary=True)

@implementEffectFactory('MotionBlur', 'MotionBlur')
def sharpen():
    backBufferCopy = rt('backBufferCopy')
    backBufferCopyB = rt('backBufferCopyB')
    velocityBuffer = rt('MotionBlurVelocity')
    c = buildBackBufferCopyPhase(backBufferCopy)
    velocityPhase = Phase()
    velocityPhase.material = Material('shaders/post_processing/motion_blur_velocity.fx')
    velocityPhase.material.inputTexture = backBufferCopy.texture
    velocityPhase.renderTarget = velocityBuffer
    velocityPhase.filterQuad = TransferQuad()
    blurPhase1 = Phase()
    blurPhase1.material = Material('shaders/post_processing/motion_blur_phase1.fx')
    blurPhase1.material.inputTexture = backBufferCopy.texture
    blurPhase1.material.velocityTexture = velocityBuffer.texture
    blurPhase1.renderTarget = backBufferCopyB
    blurPhase1.filterQuad = TransferQuad()
    blurPhase2 = Phase()
    blurPhase2.material = Material('shaders/post_processing/motion_blur_phase2.fx')
    blurPhase2.material.inputTexture = backBufferCopyB.texture
    blurPhase2.material.velocityTexture = velocityBuffer.texture
    blurPhase2.renderTarget = None
    blurPhase2.filterQuad = TransferQuad()
    e = Effect()
    e.name = 'MotionBlur'
    e.phases = [c,
     velocityPhase,
     blurPhase1,
     blurPhase2]
    return e