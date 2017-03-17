# Embedded file name: scripts/common/db/DBBaseObject.py
from BBoxes import BBoxes
from DBHelpers import readValue, findSection, readDataWithDependencies
from consts import WORLD_SCALING, TYPE_TEAM_OBJECT_STR_MAP, TYPE_TEAM_OBJECT, AIRCRAFT_MODEL_SCALING, IS_AIRPLANE_EDITOR, SUPERIORITY_POINTS_GROUPS_MAX, IS_BASEAPP
from DBParts import PartsTunes
from debug_utils import LOG_ERROR, LOG_WARNING, DBLOG_NOTE
from VisibilityTunes import VisibilityTunes
from DBBaseClass import DBBaseClass
from config_consts import IS_DEVELOPMENT

class BattleLevelsSettings:
    DEFAULT_VALUE = {'hpK': 1.0,
     'armorK': 1.0}

    def __init__(self, data):
        self.__data = {}
        if data:
            for sectionData in data.values():
                battleLevel = sectionData.readInt('battleLevel', -1)
                if battleLevel != -1:
                    self.__data[battleLevel] = {'hpK': sectionData.readFloat('hpK', 1.0),
                     'armorK': sectionData.readFloat('armorK', 1.0)}

    def getDataForLevel(self, battleLevel):
        return self.__data.get(battleLevel, BattleLevelsSettings.DEFAULT_VALUE)


class DamageEffects:

    def __init__(self, data = None):
        self.destroy = 'EFFECT_BASE_DESTROY'
        self.receive_damage_1 = 'EFFECT_AIRCRAFT_RECEIVE_DAMAGE_1'
        self.receive_damage_2 = 'EFFECT_AIRCRAFT_RECEIVE_DAMAGE_2'
        self.effectFire = 'FIRING'
        self.readData(data)

    def readData(self, data):
        if data:
            readValue(self, data, 'destroy', '')
            readValue(self, data, 'receive_damage_1', '')
            readValue(self, data, 'receive_damage_2', '')
            readValue(self, data, 'effectFire', '')


class DBBaseObject(DBBaseClass):

    def __init__(self, typeID, fileName, data = None):
        DBBaseClass.__init__(self, typeID, fileName)
        DBLOG_NOTE('loading data for %s' % fileName)
        self.damageEffects = DamageEffects()
        self.fileName = fileName
        self.sounds = None
        readDataWithDependencies(self, data, 'bases')
        if IS_AIRPLANE_EDITOR:
            self.__data = data
        return

    def checkPartsTunes(self):
        """
        indicates invalid rotation of bboxes in partUpgrades
        """
        if IS_DEVELOPMENT and IS_BASEAPP:
            try:

                def checkAffectedPartsMissedStates(upgrade):
                    for state in upgrade.states.itervalues():
                        for aPartID, aPartMinState in state.affectedParts:
                            aPart = self.partsSettings.getPartByID(aPartID)
                            if aPart:
                                for aUpgrade in aPart.upgrades.itervalues():
                                    if aPartMinState not in set(aUpgrade.states):
                                        yield (upgrade.id,
                                         aPartID,
                                         aUpgrade.id,
                                         aPartMinState)

                            else:
                                yield (upgrade.id, aPartID)

                for part in self.partsSettings.getPartsOnlyList():
                    for upgrade in part.upgrades.itervalues():
                        missedStates = list(checkAffectedPartsMissedStates(upgrade))
                        if missedStates:
                            LOG_ERROR(part.partId, part.name, upgrade.id, 'PARTS_VALIDATION_ERROR part has no such affected states:', missedStates)

            except Exception as e:
                import sys
                LOG_ERROR(sys.exc_info())

        fixedQuaternions = 0
        for partSettings in self.partsSettings.getPartsOnlyList():
            for upgrade in partSettings.upgrades.values():
                fixedQuaternions += upgrade.bboxes.fixedBBoxesCounter

        if fixedQuaternions:
            LOG_WARNING(str(fixedQuaternions) + ' zero quaternions in file ' + self.fileName + '.xml')

    def readData(self, data):
        if data:
            readValue(self, data, 'name', '')
            readValue(self, data, 'turretName', '')
            readValue(self, data, 'maxHealth', 200.0)
            readValue(self, data, 'stealthFactor', 1.0)
            readValue(self, data, 'alignToGround', False)
            readValue(self, data, 'superiorityPoints', 0)
            for groupID in range(SUPERIORITY_POINTS_GROUPS_MAX):
                readValue(self, data, 'superiorityPointsGroup%d' % groupID, 0)

            readValue(self, data, 'mass', 100000.0)
            readValue(self, data, 'type', '')
            readValue(self, data, 'modelScaling', AIRCRAFT_MODEL_SCALING)
            self.type = TYPE_TEAM_OBJECT_STR_MAP.get(self.type, TYPE_TEAM_OBJECT.INVALID)
            if self.type == TYPE_TEAM_OBJECT.INVALID:
                LOG_ERROR('invalid object type for', self.typeID, self.typeName, self.name)
            visibilityData = findSection(data, 'visibility')
            self.visibility = visibilityData and VisibilityTunes(visibilityData) or None
            self.bboxes = BBoxes(findSection(data, 'bBoxes'), self.modelScaling)
            self.partsSettings = PartsTunes(findSection(data, 'parts'))
            self.checkPartsTunes()
            battleLevelsSettingsSection = findSection(data, 'battleLevelsSettings')
            if battleLevelsSettingsSection:
                self.battleLevelsSettings = BattleLevelsSettings(battleLevelsSettingsSection)
            elif not hasattr(self, 'battleLevelsSettings'):
                self.battleLevelsSettings = None
            damageEffectsSection = findSection(data, 'damageEffects')
            if damageEffectsSection:
                self.damageEffects = DamageEffects(damageEffectsSection)
            elif not hasattr(self, 'damageEffects'):
                self.damageEffects = None
            self.__calculateSuperiorityPoints()
        return

    def __calculateSuperiorityPoints(self):
        self.superiorityPoints = 0
        for groupID in range(SUPERIORITY_POINTS_GROUPS_MAX):
            self.superiorityPoints += self.__getSuperiorityPointsByGroupPartId(groupID)

    def __getSuperiorityPointsByGroupPartId(self, groupID):
        return getattr(self, 'superiorityPointsGroup%d' % groupID, 0)

    def save(self):
        if IS_AIRPLANE_EDITOR:
            self.partsSettings.save()
            self.__data.save()