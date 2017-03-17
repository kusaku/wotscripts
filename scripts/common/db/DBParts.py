# Embedded file name: scripts/common/db/DBParts.py
from BBoxes import BBoxes
from DBHelpers import readValue, readDataWithDependencies, findSection, writeValue, writeValues, readValues
import Math
from debug_utils import *
from consts import IS_AIRPLANE_EDITOR, PART_STATE_HANGAR, PART_STATE_CRASH, PART_STATE_FALL, PART_STATE_IDHANGAR, PART_STATE_IDCRASH, PART_STATE_IDFALL, ANIMATION_STATE_HEALTH_K
STATE_ACTION_NONE = 0
STATE_ACTION_CRITICAL = 1

class CustomSettings:

    def __init__(self, data = None):
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        self.readData(data)

    def name(self):
        return None

    def readData(self, data = None):
        pass


class CustomSettingsFactory:
    PART_SETTINGS_DICT = {}

    @staticmethod
    def readSettings(data):
        for section in data.values():
            settingsClass = CustomSettingsFactory.PART_SETTINGS_DICT.get(section.name, None)
            if settingsClass is not None:
                settings = settingsClass(section)
                readValues(settings, section, settings.params())
                return settings

        return


class PartsTunes:
    """Keeps all aircraft's parts, each "part" keeps all possible upgrades"""

    def __init__(self, data = None):
        self.__partsByName = {}
        self.__partsByID = {}
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        self.readData(data)

    def readData(self, data = None):
        if data != None:
            self.__data = IS_AIRPLANE_EDITOR and data
        if not data:
            raise AssertionError('no parts found')
            for partData in data.values():
                part = PartSettings(partData)
                self.__partsByName[part.name] = part
                self.__partsByID[part.partId] = part

        return

    def getPartByName(self, partName):
        if partName in self.__partsByName:
            return self.__partsByName[partName]
        else:
            return None

    def getPartByID(self, partID):
        if partID in self.__partsByID:
            return self.__partsByID[partID]
        else:
            return None

    def getPartsList(self):
        return [ part for part in self.__partsByID.iteritems() ]

    def getPartsOnlyList(self):
        return self.__partsByID.values()

    def save(self):
        if IS_AIRPLANE_EDITOR:
            for part in self.__partsByID.values():
                part.save()

    def newPart(self):
        if IS_AIRPLANE_EDITOR:
            partId = 1
            if len(self.__partsByID.keys()) > 0:
                partId = max(self.__partsByID.keys()) + 1
            partName = 'part'
            data = self.__data.createSection(partName)
            data.writeString('name', partName + str(partId))
            data.writeInt('partId', partId)
            part = PartSettings(data)
            part.save()
            part.newType()
            self.__partsByID[part.partId] = part

    def removePart(self, partId):
        if IS_AIRPLANE_EDITOR:
            data = None
            for partData in self.__data.values():
                if partData.readInt('partId') == partId:
                    data = partData
                    break

            if data is not None:
                self.__data.deleteSection(data)
                partName = self.__partsByID[partId].name
                del self.__partsByID[partId]
                del self.__partsByName[partName]
            else:
                DBLOG_ERROR('Error: removePart, part is not exist')
        return


class PartSettings:
    """
    PartSettings class keeps description of all possible upgrades for aircraft's current part.
    For example, an object of this class can store a list of objects [Engine_level_1, Engine_level_2, Engine_level_3],
    meaning that this part is "engine" and can be actually upgraded to any of Engine_level_*
    """
    currentInitedPart = None

    def __init__(self, data = None):
        self.upgrades = {}
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        if data != None:
            params = (('name', ''),
             ('partId', 0),
             ('groupId', 0),
             ('mountPoint', ''))
            if IS_AIRPLANE_EDITOR:
                self.__params = params
            readValues(self, data, params)
            PartSettings.currentInitedPart = self.name
            for sName, sData in data.items():
                if sName == 'upgrade':
                    upgrade = PartUpgrade(sData)
                    self.upgrades[upgrade.id] = upgrade

        return

    def getFirstPartType(self):
        """
        Gets the first part type
        @rtype: PartUpgrade
        @return: PartUpgrade or None
        """
        if len(self.upgrades) == 0:
            return None
        else:
            return self.upgrades.values()[0]

    def getPartType(self, partTypeId):
        """
        Gets part type by id
        @param partTypeId: part type id
        @rtype: PartUpgrade
        @return: PartUpgrade or None
        """
        if partTypeId in self.upgrades:
            return self.upgrades[partTypeId]
        else:
            return None

    def getActualPart(self, partID, upgradesList):
        upgradeId = filter(lambda x: x['key'] == partID, upgradesList)
        if upgradeId:
            return self.getPartType(upgradeId[0]['value'])
        return self.getFirstPartType()

    def save(self):
        if IS_AIRPLANE_EDITOR:
            if self.__data != None:
                writeValues(self, self.__data, self.__params)
            for type in self.upgrades.values():
                type.save()

        return

    def newType(self):
        if IS_AIRPLANE_EDITOR:
            typeId = 1
            if len(self.upgrades.keys()) > 0:
                typeId = max(self.upgrades.keys()) + 1
            data = self.__data.createSection('upgrade')
            data.writeInt('id', typeId)
            data.createSection('states')
            partType = PartUpgrade(data)
            partType.save()
            partType.newState()
            self.upgrades[partType.id] = partType

    def removeType(self, typeId):
        if IS_AIRPLANE_EDITOR:
            for typeName, typeData in self.__data.items():
                if typeName == 'upgrade' and typeData.readInt('id') == typeId:
                    data = typeData
                    break

            if data is not None:
                self.__data.deleteSection(data)
                del self.upgrades[typeId]
            else:
                DBLOG_ERROR('Error: removeType, type is not exist')
        return


class EngineSoundSettings:

    def __init__(self, data = None):
        if data is not None:
            readValue(self, data, 'rotor', '')
            readValue(self, data, 'rotorEnemy', '')
            readValue(self, data, 'rotorDamaged', '')
            readValue(self, data, 'rotorCockpitMono', '')
            readValue(self, data, 'rotorCockpitL', '')
            readValue(self, data, 'rotorCockpitR', '')
            readValue(self, data, 'rotorOverheat', '')
            readValue(self, data, 'rotorOverheatMax', '')
        return


class PartUpgrade:

    def __init__(self, data = None):
        self.states = {}
        self.soundSettings = None
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        if data != None:
            params = (('id', 0),
             ('componentType', ''),
             ('componentTypeQuota', 1.0),
             ('componentXml', ''),
             ('repairDestructedAfter', -1.0),
             ('health', '20.0'),
             ('fireMountPoint', ''),
             ('componentPosition', 'Front'))
            if IS_AIRPLANE_EDITOR:
                self.__params = params
            readValues(self, data, params)
            if data.has_key('gunPartName'):
                readValue(self, data, 'gunPartName', '')
            if self.health.find('%') == -1:
                self.healthValue = float(self.health)
                self.healthPrc = 0.0
            else:
                self.healthPrc = float(self.health[:-1]) / 100.0
                self.healthValue = 0.0
            self.componentXml = self.componentXml.lower()
            self.bboxes = BBoxes(findSection(data, 'bBoxes'))
            self.bodyTypes = BodyTypes(findSection(data, 'bodyTypes'))
            statesSection = findSection(data, 'states')
            if statesSection:
                for stateData in statesSection.values():
                    state = PartTypeStateSettings(stateData)
                    self.states[int(state.id)] = state

            fireSection = findSection(data, 'fire')
            if fireSection:
                self.fire = FireStateSettings(fireSection)
            if not hasattr(self, 'fire'):
                self.fire = None
            soundSection = findSection(data, 'soundSettings')
            if soundSection:
                self.soundSettings = EngineSoundSettings(soundSection)
        return

    def getState(self, stateID):
        if stateID in self.states:
            return self.states[stateID]

    def save(self):
        if IS_AIRPLANE_EDITOR:
            if self.__data != None:
                writeValues(self, self.__data, self.__params)
            self.bboxes.save()
            for state in self.states.values():
                state.save()

        return

    def newState(self):
        if IS_AIRPLANE_EDITOR:
            stateId = 1
            if len(self.states.keys()) > 0:
                stateId = max(self.states.keys()) + 1
            statesSection = findSection(self.__data, 'states')
            data = statesSection.createSection('state')
            data.writeInt('id', stateId)
            state = PartTypeStateSettings(data)
            state.save()
            self.states[stateId] = state

    def removeState(self, stateId):
        if IS_AIRPLANE_EDITOR:
            statesSection = findSection(self.__data, 'states')
            if statesSection is None:
                DBLOG_ERROR("Error: removeState, XML hasn't section states")
                return
            data = None
            for stateData in statesSection.values():
                if stateData.readInt('id') == stateId:
                    data = stateData
                    break

            if data is not None:
                statesSection.deleteSection(data)
                del self.states[stateId]
            else:
                DBLOG_ERROR('Error: removeState, state is not exist')
        return

    def getBboxCount(self):
        return len(self.bboxes.list)

    def getBbox(self, ind):
        if ind < self.getBboxCount():
            bbox = self.bboxes.list[ind]
            return bbox
        else:
            return None


class BodyTypeState:

    def __init__(self, data = None):
        self.subItems = []
        if data != None:
            params = (('id', 0), ('model', ''), ('animationController', ''))
            readValues(self, data, params)
            subItemsSection = findSection(data, 'subItems')
            if subItemsSection != None:
                for subItemData in subItemsSection.values():
                    subItem = PartTypeStateSubItemSettings(subItemData)
                    self.subItems.append(subItem)

        return

    def save(self):
        pass


class BodyType:

    def __init__(self, data = None):
        self.states = {}
        for stateData in data.values():
            state = BodyTypeState(stateData)
            self.states[int(state.id)] = state

    def save(self):
        pass


class BodyTypes:

    def __init__(self, data = None):
        self.types = {}
        if data is not None:
            for id in data.keys():
                self.types[id] = BodyType(findSection(data, id))

        return

    def save(self):
        pass

    def getBodyType(self, type):
        return self.types.get(type)


class PartTypeStateSubItemSettings:

    def __init__(self, data = None):
        self.customSettings = {}
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        if data != None:
            params = (('name', ''),
             ('model', ''),
             ('mountPoint', ''),
             ('animatorName', ''))
            if IS_AIRPLANE_EDITOR:
                self.__params = params
            readValues(self, data, params)
            settings = CustomSettingsFactory.readSettings(data)
            if settings:
                self.customSettings[settings.name()] = settings
        return

    def save(self):
        if IS_AIRPLANE_EDITOR:
            if self.__data != None:
                writeValues(self, self.__data, self.__params)
        return


class PartTypeStateSettings:

    def __init__(self, data):
        self.subItems = []
        self.effectSettings = None
        self.affectedParts = []
        self.customSettings = {}
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        if data != None:
            params = (('id', 0),
             ('usage', ''),
             ('model', ''),
             ('animationController', ''),
             ('stateHelthCfc', 0.0),
             ('stateFireChance', 0.2),
             ('stateAction', STATE_ACTION_NONE),
             ('fallingOutModel', ''),
             ('stateAnimation', ''))
            if IS_AIRPLANE_EDITOR:
                self.__params = params
            readValues(self, data, params)
            if self.id == 0:
                DBLOG_ERROR('state id missed for part')
            if self.stateHelthCfc < 0 and self.stateHelthCfc != ANIMATION_STATE_HEALTH_K:
                DBLOG_ERROR('invalid stateHelthCfc')
            bBoxesData = findSection(data, 'bBoxes')
            self.bboxes = bBoxesData and BBoxes(bBoxesData) or None
            affectedPartsData = findSection(data, 'affectedParts')
            if affectedPartsData:
                for partData in affectedPartsData.values():
                    partID = partData.readInt('partID', -1)
                    if partID != -1:
                        minimalPartState = partData.readInt('minimalPartState', 1)
                        self.affectedParts.append((partID, minimalPartState))

            usagestr = self.usage.lower()
            self.stateFlag = 0
            if usagestr.find(PART_STATE_HANGAR) != -1:
                self.stateFlag = self.stateFlag | PART_STATE_IDHANGAR
            if usagestr.find(PART_STATE_CRASH) != -1:
                self.stateFlag = self.stateFlag | PART_STATE_IDCRASH
            if usagestr.find(PART_STATE_FALL) != -1:
                self.stateFlag = self.stateFlag | PART_STATE_IDFALL
            subItemsSection = findSection(data, 'subItems')
            if subItemsSection != None:
                for subItemData in subItemsSection.values():
                    subItem = PartTypeStateSubItemSettings(subItemData)
                    self.subItems.append(subItem)

            self.effectSettings = EffectsSettings(data)
            decalSection = findSection(data, 'groundDecal')
            if decalSection:
                self.groundDecal = GroundDecal(decalSection)
            settings = CustomSettingsFactory.readSettings(data)
            if settings:
                self.customSettings[settings.name()] = settings
        return

    def save(self):
        if IS_AIRPLANE_EDITOR:
            if self.__data != None:
                writeValues(self, self.__data, self.__params)
            if self.effectSettings:
                self.effectSettings.save()
            for subitem in self.subItems:
                subitem.save()

            if hasattr(self, 'groundDecal'):
                self.groundDecal.save()
        return

    def newSubitem(self):
        if IS_AIRPLANE_EDITOR:
            subItemsSection = findSection(self.__data, 'subItems')
            data = subItemsSection.createSection('item')
            subitem = PartTypeStateSubItemSettings(data)
            subitem.save()
            self.subItems.append(subitem)

    def removeSubitem(self, subitemId):
        if IS_AIRPLANE_EDITOR:
            subItemsSection = findSection(self.__data, 'subItems')
            if subItemsSection is None:
                DBLOG_ERROR("Error: removeSubitem, XML hasn't section subItems")
                return
            data = None
            i = 0
            for subitemData in subItemsSection.values():
                if i == subitemId:
                    data = subitemData
                    break
                i += 1

            if data is not None:
                subItemsSection.deleteSection(data)
                del self.subItems[subitemId]
            else:
                DBLOG_ERROR('Error: removeState, state is not exist')
        return

    def newEffect(self, effectType):
        if IS_AIRPLANE_EDITOR:
            if self.effectSettings:
                self.effectSettings.newEffect(effectType)

    def removeEffect(self, effectName):
        if IS_AIRPLANE_EDITOR:
            if self.effectSettings:
                self.effectSettings.removeEffect(effectName)


class FireStateSettings:

    def __init__(self, data):
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        if data:
            params = (('extinguish_time', 5.0),
             ('fire_damage', '2.0'),
             ('tickLength', 2.0),
             ('effectFire', ''),
             ('fire_chance', 0.0))
            if IS_AIRPLANE_EDITOR:
                self.__params = params
            readValues(self, data, params)
            if self.fire_damage.find('%') == -1:
                self.fire_damage = float(self.fire_damage)
                self.fire_damagePrc = 0.0
            else:
                self.fire_damagePrc = float(self.fire_damage[:-1]) / 100.0
                self.fire_damage = 0.0
            self.extinguish_chance = FireExtinguishChance(findSection(data, 'extinguish_chance'))


class FireExtinguishChance:

    def __init__(self, data):
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        if data:
            params = (('baseChance', 0.1),
             ('vMin', 250.0),
             ('pMin', 1.0),
             ('vMax', 500.0),
             ('pMax', 3.0))
            if IS_AIRPLANE_EDITOR:
                self.__params = params
            readValues(self, data, params)


class EffectSettings:

    def __init__(self, data, triggered = False):
        if data != None:
            params = (('name', ''), ('mountPoint', ''), ('trigger', ''))
            readValues(self, data, params)
            if not triggered:
                self.trigger = None
            self.delay = data.readVector2('delay') if data.has_key('delay') else None
            if self.mountPoint.find(PartSettings.currentInitedPart + '/') == 0:
                mountData = self.mountPoint.split('/')
                if len(mountData) > 1:
                    self.mountPoint = mountData[1]
            if IS_AIRPLANE_EDITOR:
                self.ed_data = data
                self.__params = params
        return

    def save(self):
        if IS_AIRPLANE_EDITOR:
            if self.ed_data:
                writeValues(self, self.ed_data, self.__params)
            if self.delay:
                writeValue(self, self.ed_data, 'delay')


class EffectsSettings:

    def __init__(self, data):
        self.onStart = []
        self.state = []
        self.triggered = []
        effectOnStart = findSection(data, 'effectOnStart')
        if effectOnStart:
            for effect in effectOnStart.values():
                parsedEffect = EffectSettings(effect)
                self.onStart.append(parsedEffect)

        effectState = findSection(data, 'effectState')
        if effectState:
            for effect in effectState.values():
                parsedEffect = EffectSettings(effect)
                self.state.append(parsedEffect)

        effectsTriggered = findSection(data, 'effectsTriggered')
        if effectsTriggered:
            for effect in effectsTriggered.values():
                parsedEffect = EffectSettings(effect, True)
                self.triggered.append(parsedEffect)

        if IS_AIRPLANE_EDITOR:
            self.__data = data
            self.__effectSection = {}
            self.__effectSection['effectOnStart'] = effectOnStart
            self.__effectSection['effectState'] = effectState
            self.__effectSection['effectsTriggered'] = effectsTriggered
            self.__effects = {}
            self.__effects['effectOnStart'] = self.onStart
            self.__effects['effectState'] = self.state
            self.__effects['effectsTriggered'] = self.triggered

    def save(self):
        if IS_AIRPLANE_EDITOR:
            for effectList in self.__effects.values():
                for effect in effectList:
                    effect.save()

    def newEffect(self, effectType):
        if IS_AIRPLANE_EDITOR:
            if self.__data:
                if self.__effectSection[effectType] is None:
                    self.__effectSection[effectType] = self.__data.createSection(effectType)
                effectsCount = len(self.__effects['effectOnStart']) + len(self.__effects['effectState']) + len(self.__effects['effectsTriggered'])
                effectSection = self.__effectSection[effectType].createSection('effect')
                effectSection.writeString('name', 'effect' + str(effectsCount))
                effect = EffectSettings(effectSection)
                effect.save()
                self.__effects[effectType].append(effect)
        return

    def removeEffect(self, effectName):
        if IS_AIRPLANE_EDITOR:
            for effectType, effectList in self.__effects.items():
                for effect in effectList:
                    if effect.name == effectName:
                        self.__effectSection[effectType].deleteSection(effect.ed_data)
                        effectList.remove(effect)
                        break


class GroundDecal:

    def __init__(self, data = None):
        if data:
            params = (('texture', ''), ('mountPoint', ''))
            readValues(self, data, params)
            self.scale = data.readVector3('scale')
            if IS_AIRPLANE_EDITOR:
                self.ed_data = data
                self.__params = params

    def save(self):
        if IS_AIRPLANE_EDITOR:
            if self.texture:
                writeValue(self, self.ed_data, 'texture', '')
            if self.scale:
                writeValue(self, self.ed_data, 'scale', Math.Vector3(1, 1, 1))


def getPartType(partsSettings, partID):
    partDB = next((partDB for partID_, partDB in partsSettings.getPartsList() if partID_ == partID))
    return partDB.getFirstPartType()


def buildPresentPartsMap(partsSettings, ownerPartTypes):

    def generateList():
        partsList = partsSettings.getPartsList()
        for partID, partDB in partsList:
            partType = None
            for it in ownerPartTypes:
                if it['key'] == partID:
                    partType = partDB.getPartType(it['value'])
                    break

            if not partType:
                partType = partDB.getFirstPartType()
            if partType:
                yield (partID, partType)

        return

    return dict(((partID, partType) for partID, partType in generateList()))


def buildPartsMapByPartName(partName, partsSettings, ownerPartTypes):

    def generateList():
        partsList = partsSettings.getPartsList()
        for partTuple in partsList:
            partType = None
            partID = partTuple[0]
            partDB = partTuple[1]
            for it in ownerPartTypes:
                if it['key'] == partID:
                    partType = partDB.getPartType(it['value'])
                    break

            if not partType:
                partType = partDB.getFirstPartType()
            if partType and partType.componentType.find(partName) != -1:
                yield (partID, partType)

        return

    return dict(((partID, partType) for partID, partType in generateList()))