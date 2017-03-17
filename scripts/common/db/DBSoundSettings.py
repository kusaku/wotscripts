# Embedded file name: scripts/common/db/DBSoundSettings.py
from db.DBHelpers import *
from consts import WORLD_SCALING, SPEED_SCALING
from math import radians

class EventSet:

    def __init__(self, root):
        self.__entries = dict()
        fillDictionaryByValues(self.entries, root)

    @property
    def entries(self):
        return self.__entries


class AircraftEventSet:

    def __init__(self, root):
        self.entries = dict()
        fillDictionaryByValues(self.entries, root)
        for k in self.entries.keys():
            self.entries[k] = dict()
            fillDictionaryByValues(self.entries[k], findSection(root, k, False))


class AircraftSounds:

    def __init__(self, root):
        self.aircrafts = Aircrafts(root)
        self.engineSet = AircraftEventSet(findSection(root, 'EngineSet'))
        self.misc = AircraftEventSet(findSection(root, 'Misc'))
        self.air = AircraftEventSet(findSection(root, 'Air'))
        self.states = AircraftEventSet(findSection(root, 'States'))


class WeaponProfiles:

    def __init__(self, root):
        self.__profiles = {}
        for wpn in root.items():
            fd = {}
            fillDictionaryByValues(fd, wpn[1])
            if 'WeaponSoundID' not in fd:
                continue
            wpnSndId = fd.pop('WeaponSoundID')
            self.__profiles[wpnSndId] = fd

    @property
    def profiles(self):
        return self.__profiles


class EffectProfiles:

    def __init__(self, root):
        self.__effects = {}
        for eff in root.items():
            fd = {}
            fillDictionaryByValues(fd, eff[1])
            if 'SoundEffectID' not in fd or 'Event' not in fd:
                continue
            snd = fd.pop('SoundEffectID')
            self.__effects[snd] = fd['Event']

    @property
    def sounds(self):
        return self.__effects


class Aircrafts:

    def __init__(self, root):
        self.entries = {}
        for i in root.items():
            if i[0] != 'Aircraft':
                continue
            name = str(i[1].readString('Name')).lower()
            self.entries[name] = AircraftSound(i[1])


class AircraftSound:

    def __init__(self, root):
        self.engineSet = root.readString('EngineSet')
        self.mointPoint = root.readString('EngineMountPosition')
        self.air = root.readString('Air')
        self.misc = root.readString('Misc')
        self.states = root.readString('States')
        self.weapons = []
        wpnMntPts = findSection(root, 'WeaponMountPoints')
        if wpnMntPts is None:
            return
        else:
            for i in wpnMntPts.values():
                slot = i.readInt('Slot')
                HPs = []
                for j in i.items():
                    if str(j[0]).lower() == 'slot':
                        continue
                    if str(j[0]).lower() == 'mountpoint':
                        HPs.append(j[1].readString(''))

                self.weapons.insert(slot, HPs)

            return


class Ambient:

    def __init__(self, root):
        self.__events = {}
        for i in root.items():
            fd = {}
            fillDictionaryByValues(fd, i[1])
            id = fd.pop('name')
            self.__events[id] = fd

    @property
    def events(self):
        return self.__events


class Voiceovers:

    def __init__(self, root):
        self.threshold = root.readInt('VOLengthThreshold')
        self.spawnDelay = root.readFloat('VOSpawnDelay')
        self.soundOn = root.readString('VOSoundOn')
        self.soundOff = root.readString('VOSoundOff')
        self.noise = root.readString('VONoiseLayer')
        self.battles = root.readInt('VOSkilledPlayerBattleQuantity')
        self.__entries = {}
        self.__entries['tutorial'] = {}
        self.__entries['gameplay'] = {}
        for i in root.items():
            name = str(i[0]).lower()
            if name == 'tutorial' or name == 'gameplay':
                fd = {}
                fillDictionaryByValues(fd, i[1])
                id = fd.pop('VOScriptID')
                if not id:
                    continue
                if name == 'gameplay':
                    fd['VOCooldown'] = float(fd['VOCooldown'])
                    fd['VOPriority'] = int(fd['VOPriority'])
                self.__entries[name][id] = fd

    def gameplay(self, name):
        return self.__entries['gameplay'].get(name, None)

    def tutorial(self, name):
        return self.__entries['tutorial'].get(name, None)


class Airshow:

    def __init__(self, root):
        self.externalSphereRadius = root.readInt('ExternalSphereRadius') * WORLD_SCALING
        self.internalShpereRadius = root.readFloat('InternalShpereRadius') * WORLD_SCALING
        self.externalSphereRange = root.readFloat('ExternalSphereRange')
        self.minSpeed = root.readInt('MinSpeed') * WORLD_SCALING * WORLD_SCALING
        self.cooldownTime = root.readFloat('CooldownTime')
        self.timeIntervals = {}
        for timeInterval in findSection(root, 'TimeIntervals').items():
            temp = {}
            fillDictionaryByValues(temp, timeInterval[1])
            self.timeIntervals[float(temp['Time'])] = temp['Switch']

    @property
    def externalSphereRadius(self):
        return self.externalSphereRadius

    @property
    def internalShpereRadius(self):
        return self.internalShpereRadius

    @property
    def externalSphereRange(self):
        return self.externalSphereRange

    @property
    def minSpeed(self):
        return self.minSpeed

    @property
    def cooldownTime(self):
        return self.cooldownTime

    @property
    def timeIntervals(self):
        return self.timeIntervals


class Wind:

    def __init__(self, root):
        self.altitudeTop = root.readInt('AltitudeTop')
        self.altitudeBottom = root.readInt('AltitudeBottom')
        self.maneuversAngleTop = root.readInt('ManeuversAngleTop')
        self.maneuversAngleBottom = root.readInt('ManeuversAngleBottom')
        self.cameraSpeedTop = root.readInt('CameraSpeedTop')
        self.cameraSpeedBottom = root.readInt('CameraSpeedBottom')
        self.onDestroyFadeTime = root.readInt('OnDestroyFadeTime')

    @property
    def altitudeTop(self):
        return self.altitudeTop

    @property
    def altitudeBottom(self):
        return self.altitudeBottom

    @property
    def maneuversAngleTop(self):
        return self.maneuversAngleTop

    @property
    def maneuversAngleBottom(self):
        return self.maneuversAngleBottom

    @property
    def cameraSpeedTop(self):
        return self.cameraSpeedTop

    @property
    def cameraSpeedBottom(self):
        return self.cameraSpeedBottom

    @property
    def onDestroyFadeTime(self):
        return self.onDestroyFadeTime


class InteractiveMix:

    def __init__(self, root):
        self.gamePhases = self.fillDictionaryFull(findSection(root, 'GamePhases'))

    def __fillDictionaryFull(self, root):
        items = root.items()
        tempDict = {}
        finBit = False
        if items:
            for item in [ i[1] for i in items ]:
                childDict, isFin = self.__fillDictionaryFull(item)
                if isFin:
                    tempDict[item.name] = childDict[item.name]
                else:
                    tempDict[item.name] = childDict

        else:
            tempDict[root.name] = root.asString
            finBit = True
        return (tempDict, finBit)

    def fillDictionaryFull(self, root):
        return self.__fillDictionaryFull(root)[0]

    @property
    def gamePhases(self):
        return self.gamePhases


class SoundSettings:

    def __init__(self, data):
        self.__aircraftSounds = AircraftSounds(findSection(data, 'AircraftSounds'))
        self.weapons = WeaponProfiles(findSection(data, 'Weapons'))
        self.hangar = EventSet(findSection(data, 'Hangar'))
        self.effects = EffectProfiles(findSection(data, 'Effects'))
        self.ambient = Ambient(findSection(data, 'Ambient'))
        self.wooshSphere = EventSet(findSection(data, 'WooshSphere'))
        self.voice = Voiceovers(findSection(data, 'Voiceovers'))
        self.ui = EventSet(findSection(data, 'UI'))
        self.airshow = Airshow(findSection(data, 'Airshow'))
        self.wind = Wind(findSection(data, 'Wind'))
        self.interactiveMix = InteractiveMix(findSection(data, 'InteractiveMix'))

    def aircraftSound(self, name):
        k = str(name).lower()
        if k not in self.__aircraftSounds.aircrafts.entries:
            return None
        else:
            return self.__aircraftSounds.aircrafts.entries[k]

    @property
    def engineSet(self):
        return self.__aircraftSounds.engineSet

    @property
    def aircraftSFX(self):
        return self.__aircraftSounds.misc

    @property
    def aircraftStates(self):
        return self.__aircraftSounds.states

    @property
    def aircraftAir(self):
        return self.__aircraftSounds.air

    @property
    def ambient(self):
        return self.ambient

    @property
    def weapons(self):
        return self.ambient

    @property
    def woosh(self):
        return self.wooshSphere

    @property
    def voice(self):
        return self.voice

    @property
    def ui(self):
        return self.ui

    @property
    def airshow(self):
        return self.airshow

    @property
    def wind(self):
        return self.wind