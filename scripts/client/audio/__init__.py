# Embedded file name: scripts/client/audio/__init__.py
from consts import IS_EDITOR, IS_CLIENT
from SoundObjects import AircraftEngineSound
from SoundObjects import AircraftSFX
from SoundObjects import AirshowSound
from SoundObjects import EffectSound
from SoundObjects import ExplosionSound
from SoundObjects import HitSound
from SoundObjects import Music
from SoundObjects import ShellSound
from SoundObjects import UI
from SoundObjects import Voiceover
from SoundObjects import WeaponSound
from SoundObjects import WindSound
from SoundObjects import WwiseGameObject
if IS_EDITOR:
    from GameSoundImplStub import GameSound
elif IS_CLIENT:
    from GameSoundImpl import GameSound