# Embedded file name: scripts/client/audio/SoundObjects/__init__.py
from consts import IS_EDITOR, IS_CLIENT
if IS_EDITOR:
    from Stubs import AircraftEngineSound
    from Stubs import AircraftSFX
    from Stubs import AirshowSound
    from Stubs import EffectSound
    from Stubs import ExplosionSound
    from Stubs import HitSound
    from Stubs import Music
    from Stubs import ShellSound
    from Stubs import TurretSound
    from Stubs import UI
    from Stubs import Voiceover
    from Stubs import WeaponSound
    from Stubs import WindSound
    from Stubs import WwiseGameObject
    from Stubs import AircraftEngineSoundFactory
    from Stubs import AircraftSFXFactory
    from Stubs import AirshowSoundFactory
    from Stubs import TurretSoundFactory
    from Stubs import WeaponSoundFactory
    from Stubs import WindSoundFactory
elif IS_CLIENT:
    from AircraftEngineSound import AircraftEngineSound
    from AircraftSFX import AircraftSFX
    from AirshowSound import AirshowSound
    from EffectSound import EffectSound
    from ExplosionSound import ExplosionSound
    from HitSound import HitSound
    from Music import Music
    from ShellSound import ShellSound
    from TurretSound import TurretSound
    from UI import UI
    from Voiceover import Voiceover
    from WeaponSound import WeaponSound
    from WindSound import WindSound
    from WwiseGameObject import WwiseGameObject
    from AircraftEngineSound import AircraftEngineSoundFactory
    from AircraftSFX import AircraftSFXFactory
    from AirshowSound import AirshowSoundFactory
    from TurretSound import TurretSoundFactory
    from WeaponSound import WeaponSoundFactory
    from WindSound import WindSoundFactory
AircraftSoundObjectsFactories = [AircraftEngineSoundFactory,
 AircraftSFXFactory,
 AirshowSoundFactory,
 WeaponSoundFactory,
 WindSoundFactory]
TurretSoundObjectsFactories = [TurretSoundFactory]