# Embedded file name: scripts/client/EffectManager.py
import BigWorld
import Pixie
import db.DBLogic
from debug_utils import *
g_instance = None
from wofdecorators import noexcept
import Math
from MathExt import clamp
from consts import IS_EDITOR
if not IS_EDITOR:
    import CameraEffect
    from EntityHelpers import isClientReadyToPlay
from random import uniform, randint, choice
from consts import WORLD_SCALING
from clientConsts import BLAST_FORCE_DISTANCE_FACTOR, EFFECT_COLLISION_RANGE, BLAST_FORCE_MAX, LOCAL_PARTICLE_ADJUST
from audio import EffectSound
from audio import HitSound
from audio import ExplosionSound
from sets import Set

def Init():
    global g_instance
    if g_instance == None:
        g_instance = EffectManager()
    return g_instance


@noexcept
def Destroy():
    global g_instance
    if g_instance != None:
        g_instance.destroy()
        g_instance = None
    return


class EffectBase:

    def __init__(self, properties, attachProperties, effectManager):
        self.properties = properties
        self.attachProperties = attachProperties
        self.effectManager = effectManager
        self.visible = True
        self.attached = False
        self._sound = None
        self.particleLoaded = False
        self.delayed = False
        self.delayCallbackId = None
        self.modelAttachNode = None
        self.effectAttachNode = None
        self.model = None
        self.sound_container = None
        if 'delay' in self.properties:
            self.delayed = True
            self.delayCallbackId = BigWorld.callback(uniform(self.properties['delay'][0], self.properties['delay'][1]), self.__onDelayEnds)
        else:
            self.__onDelayEnds()
        return

    def __onDelayEnds(self):
        self.delayed = False
        self.delayCallbackId = None
        if self.particleLoaded:
            self.attach()
        return

    def __playSound(self):
        if IS_EDITOR:
            return
        elif 'position' not in self.attachProperties:
            return
        else:
            pos = self.attachProperties['position']
            hitSFX = self.properties.get('sfx')
            if hitSFX and HitSound.canPlayEffect(hitSFX):
                self._hsound = HitSound(None, pos, hitSFX)
            explSFX = self.properties.get('exp')
            if explSFX:
                self._esound = ExplosionSound(explSFX, pos)
            if 'SoundEffectID' not in self.properties:
                return
            self._sound = EffectSound(self.properties['SoundEffectID'], 0, 0, pos)
            return

    def __stopSound(self):
        if self._sound is None:
            return
        else:
            self._sound.stop()
            self._sound = None
            return

    def attach(self):
        if self.delayed or self.attached:
            return
        else:
            self.attached = True
            self.effectManager.registerParticle(self)
            overrideAttachType = self.properties.get('attachType')
            attachType = self.attachProperties['type'] if overrideAttachType is None else overrideAttachType
            if attachType == 'world':
                if self.properties.get('attachToTarget', False) and self.properties.get('entity', None):
                    entity = self.properties['entity']
                    controllers = getattr(self.properties['entity'], 'controllers', None)
                    if controllers:
                        modelManipulator = controllers.get('modelManipulator')
                        if modelManipulator:
                            try:
                                rootModel = modelManipulator.getRootModel()
                                m = Math.Matrix(rootModel.matrix)
                                invRotation = Math.Quaternion()
                                invRotation.fromEuler(m.roll, m.pitch, m.yaw)
                                invRotation.invert()
                                localOffset = invRotation.rotateVec((self.attachProperties['position'] - m.translation) / WORLD_SCALING)
                                self.modelAttachNode = rootModel.node('Scene Root')
                                self.effectAttachNode = self.modelAttachNode
                                matrix = Math.Matrix()
                                rotation = self.properties.get('rotation')
                                if rotation:
                                    matrix.setRotateYPR(rotation)
                                matrix.translation = localOffset + LOCAL_PARTICLE_ADJUST
                                self.effectAttachNode.local = matrix
                            except:
                                LOG_CURRENT_EXCEPTION()

                else:
                    self.modelAttachNode = BigWorld.allocateGlobalNode()
                    self.effectAttachNode = self.modelAttachNode
                    if 'model' in self.attachProperties:
                        self.model = self.attachProperties['model']
                        self.modelAttachNode.attach(self.model)
                    rotation = self.properties.get('rotation')
                    if rotation:
                        matrix = Math.Matrix()
                        matrix.setRotateYPR(rotation)
                        matrix.translation = self.attachProperties['position']
                        self.modelAttachNode.local = matrix
                    else:
                        matrix = Math.Matrix()
                        matrix.translation = self.attachProperties['position']
                        self.modelAttachNode.local = matrix
                self.setVisible(True)
            elif attachType == 'model':
                self.modelAttachNode = self.attachProperties['node']
                self.effectAttachNode = self.modelAttachNode
                self.model = None
                if self.visible:
                    self.__playSound()
            else:
                if attachType == 'camera':
                    self.modelAttachNode = BigWorld.allocateGlobalNode()
                    self.effectAttachNode = self.modelAttachNode
                    self.modelAttachNode.local = BigWorld.camera().billboardMatrix
                    self.setVisible(True)
                    return
                if attachType == 'model_grounded':
                    matrix = self.properties.get('matrix')
                    if matrix is not None:
                        self.modelAttachNode = BigWorld.allocateGlobalNode()
                        self.effectAttachNode = self.modelAttachNode
                        self.modelAttachNode.local = BigWorld.GroundedMatrixProvider(matrix)
                        self.setVisible(True)
                        return
            return

    def reAttachToNode(self, node):
        self.detach()
        self.attachProperties = {'type': 'model',
         'node': node}
        self.visible = True
        self.attach()

    def detach(self):
        if not self.attached:
            return
        else:
            self.attached = False
            self.setVisible(False)
            self.effectManager.unRegisterParticle(self)
            attachType = self.attachProperties['type']
            if attachType == 'world':
                if self.model is not None:
                    self.modelAttachNode.detach(self.model)
            elif attachType == 'model_grounded':
                self.modelAttachNode.local = None
                self.modelAttachNode = None
                self.effectAttachNode = None
            elif attachType == 'model':
                if self.model is not None:
                    self.modelAttachNode.detach(self.model)
            if self.sound_container is not None:
                self.modelAttachNode.detach(self.sound_container)
            self.__stopSound()
            self.modelAttachNode = None
            self.effectAttachNode = None
            self.model = None
            self.sound_container = None
            return

    def destroy(self):
        if self.delayCallbackId != None:
            BigWorld.cancelCallback(self.delayCallbackId)
            self.delayCallbackId = None
        self.detach()
        return

    def setVisible(self, value):
        self.visible = value
        if self.visible:
            self.__playSound()
        else:
            self.__stopSound()
        if self.effectManager.isDbgPrint:
            if self.visible:
                LOG_TRACE('START EFFECT:', self.properties.get('id', None), self.properties.get('sound', None))
            else:
                LOG_TRACE('END EFFECT:', self.properties.get('id', None))
        return

    def getPosition(self):
        return self.attachProperties.get('position', Math.Vector3(0, 0, 0))


class EffectLoopParticle(EffectBase):

    def __init__(self, properties, attachProperties, effectManager):
        EffectBase.__init__(self, properties, attachProperties, effectManager)
        self.__pixie = None
        particleFile = self.properties['particleFile']
        if particleFile != None and particleFile != '':
            Pixie.createBG(particleFile, self.__onParticleLoaded)
        return

    def __onParticleLoaded(self, pixie):
        self.__pixie = pixie
        self.particleLoaded = True
        self.attach()

    def attach(self):
        if self.delayed or self.attached:
            return
        else:
            EffectBase.attach(self)
            if self.__pixie != None and self.effectAttachNode != None:
                self.effectAttachNode.attach(self.__pixie)
                self.setVisible(self.visible)
            else:
                self.destroy()
            return

    def detach(self):
        if not self.attached:
            return
        else:
            if self.__pixie != None and self.effectAttachNode != None:
                self.effectAttachNode.detach(self.__pixie)
            EffectBase.detach(self)
            return

    def destroy(self):
        EffectBase.destroy(self)
        self.__pixie = None
        return

    def setVisible(self, value):
        EffectBase.setVisible(self, value)
        try:
            if self.__pixie is not None:
                for i in range(0, self.__pixie.nSystems()):
                    system = self.__pixie.system(i)
                    for action in system.actions:
                        if hasattr(action, 'timeTriggered'):
                            action.timeTriggered = value

        except:
            LOG_CURRENT_EXCEPTION()

        return

    def stopEmission(self):
        if self.__pixie:
            for i in range(0, self.__pixie.nSystems()):
                system = self.__pixie.system(i)
                for action in system.actions:
                    if hasattr(action, 'rate'):
                        action.rate = 0


class EffectTimedParticle(EffectBase):

    def __init__(self, properties, attachProperties, effectManager):
        EffectBase.__init__(self, properties, attachProperties, effectManager)
        self.callbackId = None
        self.__pixie = None
        self.__triggered = properties.get('alias', None) is not None
        self.force = 0
        if 'force' in self.properties:
            self.force = int(self.properties['force'])
        particleFile = self.properties['particleFile']
        if particleFile != None and particleFile != '':
            Pixie.createBG(particleFile, self.__onParticleLoaded)
        return

    def attach(self):
        if self.delayed or self.attached:
            return
        else:
            EffectBase.attach(self)
            if self.__pixie != None and self.effectAttachNode != None:
                self.effectAttachNode.attach(self.__pixie)
                if self.force == 0:
                    self.__pixie.force()
                else:
                    self.__pixie.force(self.force)
                effectDuration = self.__pixie.duration()
                self.callbackId = BigWorld.callback(effectDuration * 1.1, self.__onParticleTimeEnd)
            else:
                self.destroy()
            return

    def detach(self):
        if not self.attached:
            return
        else:
            if self.__pixie != None and self.effectAttachNode != None and self.attached:
                self.effectAttachNode.detach(self.__pixie)
            if self.callbackId != None:
                BigWorld.cancelCallback(self.callbackId)
                self.callbackId = None
            EffectBase.detach(self)
            return

    def setVisible(self, value):
        if self.__triggered:
            if self.visible == value:
                return
            if value:
                self.attach()
        EffectBase.setVisible(self, value)

    def clearPixie(self):
        if self.__pixie != None:
            self.__pixie.clear()
        return

    def __onParticleLoaded(self, pixie):
        self.__pixie = pixie
        self.particleLoaded = True
        if not self.__triggered:
            self.attach()

    def __onParticleTimeEnd(self):
        self.callbackId = None
        self.detach()
        return

    def destroy(self):
        self.detach()
        EffectBase.destroy(self)
        self.__pixie = None
        self.callbackId = None
        return

    def collidesWithPoint(self, v3point):
        if not self.__pixie:
            return False
        self.__pixie.point_collide(v3point.x, v3point.y, v3point.z)


class EffectLoft(EffectBase):

    def __init__(self, properties, attachProperties, effectManager):
        EffectBase.__init__(self, properties, attachProperties, effectManager)
        self.__loft = None
        if IS_EDITOR:
            return
        else:
            loftTexture = self.properties['loftTexture']
            loftHeight = float(self.properties['loftHeight'])
            loftAge = float(self.properties['loftAge'])
            loftGrownStage = int(self.properties['loftGrownStage'])
            self.__loft = BigWorld.Loft(loftTexture)
            self.__loft.maxAge = loftAge
            self.__loft.height = loftHeight
            self.__loft.colour = (255, 255, 255, 25)
            self.__loft.grownStage = loftGrownStage
            self.attach()
            return

    def attach(self):
        EffectBase.attach(self)
        if self.__loft != None and self.effectAttachNode != None:
            self.effectAttachNode.attach(self.__loft)
            self.__loft.enabled = self.visible
        else:
            self.destroy()
        return

    def detach(self):
        if self.__loft != None and self.effectAttachNode != None:
            self.effectAttachNode.detach(self.__loft)
        EffectBase.detach(self)
        return

    def setVisible(self, value):
        if self.visible == value:
            return
        else:
            EffectBase.setVisible(self, value)
            if self.__loft != None:
                self.__loft.enabled = self.visible
            return

    def destroy(self):
        EffectBase.destroy(self)
        if self.__loft != None:
            self.__loft.enabled = False
            self.__loft = None
        return


class EffectJet(EffectBase):

    def __init__(self, properties, attachProperties, effectManager):
        EffectBase.__init__(self, properties, attachProperties, effectManager)
        if 'uniqueId' not in properties:
            LOG_ERROR('Unknown uniqueId property for Jet effect!', properties['id'])
            properties['uniqueId'] = ''
        self.__jet = BigWorld.Jet(properties['uniqueId'] + self.attachProperties['node'].name, self.properties['texture'])
        self.__jet.threshold = float(self.properties['threshold'])
        self.__jet.animDuration = float(self.properties['animDuration'])
        self.__jet.angleScale = float(self.properties['angleScale'])
        self.__jet.fadeInTime = float(self.properties['fadeInTime'])
        self.__jet.radiusMin = float(self.properties['radiusMin'])
        self.__jet.radiusMul = float(self.properties['radiusMul'])
        self.__jet.radiusPow = float(self.properties['radiusPow'])
        self.__jet.scaleMin = float(self.properties['scaleMin'])
        self.__jet.scaleMul = float(self.properties['scaleMul'])
        self.__jet.scalePow = float(self.properties['scalePow'])
        self.__jet.alphaMin = float(self.properties['alphaMin'])
        self.__jet.alphaMul = float(self.properties['alphaMul'])
        self.__jet.alphaPow = float(self.properties['alphaPow'])
        self.__jet.colorR = float(self.properties['colorR'])
        self.__jet.colorG = float(self.properties['colorG'])
        self.__jet.colorB = float(self.properties['colorB'])
        self.__jet.colorA = float(self.properties['colorA'])
        self.__jet.particleWidth = float(self.properties['particleWidth'])
        self.__jet.particleLen = float(self.properties['particleLen'])
        self.attach()

    def attach(self):
        EffectBase.attach(self)
        if self.__jet != None and self.effectAttachNode != None:
            self.effectAttachNode.attach(self.__jet)
            self.__jet.enabled = self.visible
        else:
            self.destroy()
        return

    def detach(self):
        if self.__jet != None and self.effectAttachNode != None:
            self.effectAttachNode.detach(self.__jet)
        EffectBase.detach(self)
        return

    def setVisible(self, value):
        if self.visible == value:
            return
        else:
            EffectBase.setVisible(self, value)
            if self.__jet != None:
                self.__jet.enabled = self.visible
            return

    def destroy(self):
        EffectBase.destroy(self)
        if self.__jet != None:
            self.__jet.enabled = False
            self.__jet = None
        return


class EffectModel(EffectBase):

    def __init__(self, properties, attachProperties, effectManager):
        EffectBase.__init__(self, properties, attachProperties, effectManager)


class EffectManager:
    EFFECT_CLASSES = {'LoopParticle': EffectLoopParticle,
     'TimedParticle': EffectTimedParticle,
     'Loft': EffectLoft,
     'Model': EffectModel,
     'Jet': EffectJet}

    def __init__(self):
        self.__particles = Set()
        self.__isFreeze = False
        self.__particleCache = {}
        self.__particleCount = {}
        self.__screenParticles = {}
        self.isDbgPrint = False

    def setFreeze(self, freeze):
        BigWorld.setPaticlesActive(not freeze)
        BigWorld.setBulletsActive(not freeze)
        self.__isFreeze = freeze

    def isFreeze(self):
        return self.__isFreeze

    def switchDebugPrinting(self):
        self.isDbgPrint = not self.isDbgPrint
        LOG_TRACE('Start EffectManager debug printing:', self.isDbgPrint)

    def getPreloadingResources(self):
        resourceList = []
        for effectID in db.DBLogic.g_instance.getEffectIds():
            varnames = db.DBLogic.g_instance.getEffectDataVariantNames(effectID)
            for name in varnames:
                effectDB = db.DBLogic.g_instance.getEffectDataVariant(effectID, name)
                if effectDB:
                    resourceFile = ''
                    if 'particleFile' in effectDB:
                        resourceFile = effectDB['particleFile']
                    if 'loftTexture' in effectDB:
                        resourceFile = effectDB['loftTexture']
                    if 'texture' in effectDB:
                        resourceFile = effectDB['texture']
                    if resourceFile != '':
                        resourceList.append(resourceFile)

        return resourceList

    def createWorldEffect(self, effectID, worldPos, properties, wasDelayed = False):
        effectDB = db.DBLogic.g_instance.getEffectDataVariant(effectID, properties.get('variant', 'OWN'))
        if effectDB == None:
            return ()
        else:
            count = int(effectDB.get('drawChance', 0))
            if count and count < randint(1, 100):
                return ()
            count = int(effectDB.get('maxCount', 0))
            if count:
                if effectID in self.__particleCount:
                    if self.__particleCount[effectID] > randint(1, int(count)):
                        return ()
                    self.__particleCount[effectID] += 1
                else:
                    self.__particleCount[effectID] = 1
            if worldPos is None:
                LOG_ERROR('Particle position is not Vector3 or tuple of 3')
                worldPos = Math.Vector3()
            if len(properties) > 0:
                effectProps = effectDB.copy()
                effectProps.update(properties)
            else:
                effectProps = effectDB
            attachData = {'type': 'world',
             'position': worldPos}
            if 'rotation' in properties:
                attachData['rotation'] = properties['rotation']
            if 'attachType' in properties:
                attachData['type'] = properties['attachType']
            if effectID in self.__particleCache and len(self.__particleCache[effectID]) > 0:
                effect = self.__particleCache[effectID].pop()
                effect.attachProperties = attachData
                effect.properties = effectProps
                if isinstance(effect, EffectTimedParticle):
                    effect.clearPixie()
                effect.attach()
            else:
                effect = self.__createEffect(effectDB['type'], effectProps, attachData)
            effect.effectID = effectID
            effects = [effect]
            if 'decal' in effectProps:
                decalData = effectProps['decal']
                decalTextureId = BigWorld.deferredImpactTextureIndex(decalData['texture'])
                if decalTextureId >= 0:
                    pos = Math.Vector3(worldPos)
                    decalStartRay = (pos[0], pos[1] + EFFECT_COLLISION_RANGE, pos[2])
                    decalEndRay = (pos[0], pos[1] - EFFECT_COLLISION_RANGE, pos[2])
                    BigWorld.addDeferredImpact(decalStartRay, decalEndRay, decalData['size'], decalTextureId)
            if 'blastForce' in effectProps:
                player = BigWorld.player()
                effectVec = worldPos - player.position
                effectBlastForce = effectProps['blastForce']
                if effectBlastForce > BLAST_FORCE_MAX:
                    effectBlastForce = clamp(0.0, effectBlastForce, BLAST_FORCE_MAX)
                force = (effectBlastForce - BLAST_FORCE_DISTANCE_FACTOR * (effectVec.length / WORLD_SCALING)) / BLAST_FORCE_MAX
                if CameraEffect.g_instance and force > 0 and not IS_EDITOR:
                    CameraEffect.g_instance.onCameraEffect('NEAR_EXPLOSION', True, force, effectVec)
            if 'screenEffectID' in effectProps and not IS_EDITOR:
                self.setScreenParticle(effectProps['screenEffectID'], worldPos)
            if 'effectSet' in effectProps:
                if 'selectOne' in effectProps and effectProps['selectOne']:
                    effects += self.createWorldEffect(choice(effectProps['effectSet']), worldPos, properties)
                else:
                    for addEffect in effectProps['effectSet']:
                        effects += self.createWorldEffect(addEffect, worldPos, properties)

            return effects

    def createNodeAttachedEffect(self, effectID, node, properties, wasDelayed = False):
        effectDB = db.DBLogic.g_instance.getEffectDataVariant(effectID, properties.get('variant', 'OWN'))
        if effectDB == None:
            LOG_ERROR("can't find effect", effectID)
            return
        else:
            effectProps = effectDB.copy()
            effectProps.update(properties)
            attachData = {'type': 'model',
             'node': node}
            return self.__createEffect(effectDB['type'], effectProps, attachData)

    def createModelGroundedEffect(self, effectID, properties):
        effectDB = db.DBLogic.g_instance.getEffectDataVariant(effectID, properties.get('variant', 'OWN'))
        if effectDB is None:
            LOG_ERROR("can't find effect", effectID)
            return
        else:
            effectProps = effectDB.copy()
            effectProps.update(properties)
            attachData = {'type': 'model_grounded'}
            return self.__createEffect(effectDB['type'], effectProps, attachData)

    def createCameraAttachedEffect(self, effectID, sourcePos, properties, wasDelayed = False):
        effectDB = db.DBLogic.g_instance.getEffectDataVariant(effectID, properties.get('variant', 'OWN'))
        if effectDB == None or sourcePos and (sourcePos - BigWorld.player().position).length / WORLD_SCALING > effectDB['distance']:
            return
        else:
            effectProps = effectDB.copy()
            effectProps.update(properties)
            attachData = {'type': 'camera',
             'node': None}
            return self.__createEffect(effectDB['type'], effectProps, attachData)

    def setScreenParticle(self, effectName, sourcePos = None, active = True):
        effectID = db.DBLogic.g_instance.getEffectId(effectName)
        if effectID:
            if active:
                particle = self.createCameraAttachedEffect(effectID, sourcePos, {})
                if particle:
                    if effectID in self.__screenParticles:
                        self.__screenParticles[effectID].append(particle)
                    else:
                        self.__screenParticles[effectID] = [particle]
                    particle.effectID = effectID
            else:
                particleType = self.__screenParticles.get(effectID)
                if particleType:
                    for particle in particleType:
                        particle.destroy()

    def showScreenParticle(self, effectName):
        effectID = db.DBLogic.g_instance.getEffectId(effectName)
        if effectID in self.__screenParticles:
            for particle in self.__screenParticles[effectID]:
                particle.setVisible(True)

        else:
            self.setScreenParticle(effectName)

    def hideScreenParticle(self, effectName):
        effectID = db.DBLogic.g_instance.getEffectId(effectName)
        if effectID in self.__screenParticles:
            for particle in self.__screenParticles[effectID]:
                particle.setVisible(False)

    def clearScreenParticles(self):
        for particleType in self.__screenParticles.values():
            particles = list(particleType)
            for particle in particles:
                particle.destroy()

        self.__screenParticles = {}

    def clearParticlesCache(self):
        for particleType in self.__particleCache.values():
            for particle in particleType:
                particle.destroy()

        self.__particleCache = {}

    def destroy(self):
        particles = Set(self.__particles)
        for particle in particles:
            particle.destroy()

        self.clearParticlesCache()
        self.clearScreenParticles()
        if len(self.__particles):
            raise Exception, 'Not all particles deleted, error'

    def registerParticle(self, particle):
        self.__particles.add(particle)

    def getAllParticles(self):
        return self.__particles

    def unRegisterParticle(self, particle):
        self.__particles.discard(particle)
        if particle.attachProperties['type'] == 'world':
            if particle.effectID in self.__particleCache:
                self.__particleCache[particle.effectID].append(particle)
            else:
                self.__particleCache[particle.effectID] = [particle]
            if particle.effectID in self.__particleCount:
                self.__particleCount[particle.effectID] -= 1
        elif particle.attachProperties['type'] == 'camera':
            if particle.effectID in self.__screenParticles and particle in self.__screenParticles[particle.effectID]:
                self.__screenParticles[particle.effectID].remove(particle)

    def __createEffect(self, typeName, effectProps, attachData):
        if typeName in EffectManager.EFFECT_CLASSES:
            effectClass = EffectManager.EFFECT_CLASSES[typeName]
            return effectClass(effectProps, attachData, self)
        else:
            return None