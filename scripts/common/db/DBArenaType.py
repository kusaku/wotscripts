# Embedded file name: scripts/common/db/DBArenaType.py
import ResMgr
from debug_utils import *
from consts import IS_CLIENT, IS_BASEAPP, CAMOUFLAGE_ARENA_TYPE, ARENA_TYPE, LANDSCAPE_PATH
from DBHelpers import readValue, readDataWithDependencies, findSection
from Curve import Curve
from DBObjectGroups import ObjectGroups
from DBSoundsStingers import SoundsStingers
from ArenaObjects import ArenaObjects
from DBBaseClass import DBBaseClass
from DBSpawnGroup import DBSpawnGroup
if IS_CLIENT:
    from Helpers import i18n

class ArenaType(DBBaseClass):

    def __init__(self, typeID, fileName, data):
        DBBaseClass.__init__(self, typeID, fileName)
        self.__arenaObjects = ArenaObjects(fileName)
        self.__bounds = None
        self._textureMaterials = {}
        if IS_BASEAPP:
            self.objectGroups = ObjectGroups()
        if IS_CLIENT:
            self._loadTextureMaterials(fileName)
        readDataWithDependencies(self, data, 'arena_defs')
        self.camouflageArenaTypeID = CAMOUFLAGE_ARENA_TYPE.getValueByName(self.camouflageArenaType)
        if not self.camouflageArenaTypeID:
            self.__raiseWrongXml("wrong 'camouflageArenaType' value %s" % self.camouflageArenaType)
        return

    @property
    def bounds(self):
        return self.__bounds

    @property
    def arenaObjects(self):
        return self.__arenaObjects

    @property
    def spawnGroupDescription(self):
        try:
            return self.__spawnGroupDescription
        except:
            LOG_ERROR("Can't find spawnGroup for arena", self.typeName)

    def getTeamObjectData(self, objID):
        return self.__arenaObjects.getTeamObjectData(objID)

    def __parseBounds(self, geometry):
        bounds = ResMgr.openSection(geometry + '/space.settings/bounds', False)
        if bounds:
            minX = bounds.readInt('minX')
            maxX = bounds.readInt('maxX')
            minY = bounds.readInt('minY')
            maxY = bounds.readInt('maxY')
            normalize = lambda x: x * 100.0
            self.__bounds = ((normalize(minX), normalize(minY)), (normalize(maxX), normalize(maxY)))

    def __parseSpaceScripts(self, geometry):
        scriptsSection = ResMgr.openSection(geometry + '/space.settings/spaceScripts', False)
        if scriptsSection:
            self.spaceScripts = scriptsSection.readStrings('scrips')
        else:
            self.spaceScripts = []

    def readData(self, data):
        if not data:
            return
        else:
            for propName in ['exclusiveGameMods', 'excludeArenaType']:
                propData = findSection(data, propName)
                if propData:
                    setattr(self, propName, set([ ARENA_TYPE.getValueByName(k) for k in propData.keys() ]))
                else:
                    setattr(self, propName, set())

            spawnGroupData = findSection(data, 'spawnGroup')
            if spawnGroupData:
                self.__spawnGroupDescription = DBSpawnGroup(spawnGroupData)
            readValue(self, data, 'camouflageArenaType', '')
            readValue(self, data, 'hudIcoPath', '')
            readValue(self, data, 'geometry', '')
            self.__parseBounds(self.geometry)
            self.__parseSpaceScripts(self.geometry)
            readValue(self, data, 'minPlayersInTeam', 0)
            self.trainingRoomIcoPathSelected = data.readString('trainingRoomIcoPath/selected', '')
            self.trainingRoomIcoPathUnselected = data.readString('trainingRoomIcoPath/unselected', '')
            self.trainingRoomIcoPathPreview = data.readString('trainingRoomIcoPath/preview', '')
            self.trainingRoomIcoPathPreviewBig = data.readString('trainingRoomIcoPath/previewBig', '')
            readValue(self, data, 'trainingRoomDescription', '')
            if self.minPlayersInTeam < 0:
                self.__raiseWrongXml("wrong 'minPlayersInTeam' value")
            readValue(self, data, 'maxPlayersInTeam', 0)
            if self.maxPlayersInTeam < 0:
                self.__raiseWrongXml("wrong 'maxPlayersInTeam' value")
            if self.maxPlayersInTeam < self.minPlayersInTeam:
                self.__raiseWrongXml("'maxPlayersInTeam' value < 'minPlayersInTeam' value")
            readValue(self, data, 'roundLength', 0)
            if self.roundLength < 0:
                self.__raiseWrongXml("wrong 'roundLength' value")
            bottomLeft = data.readVector2('boundingBox/bottomLeft')
            upperRight = data.readVector2('boundingBox/upperRight')
            if bottomLeft[0] >= upperRight[0] or bottomLeft[1] >= upperRight[1]:
                LOG_UNEXPECTED("wrong 'boundingBox' values", self.typeName)
            self.boundingBox = (bottomLeft, upperRight)
            readValue(self, data, 'isPvEReady', True)
            readValue(self, data, 'visibleEnable', 1)
            readValue(self, data, 'gameType', 'SaD')
            readValue(self, data, 'minPlayerCount', 0)
            readValue(self, data, 'selectionPriority', 0)
            readValue(self, data, 'minAircraftLevel', 1)
            readValue(self, data, 'maxAircraftLevel', 10)
            readValue(self, data, 'sunAngle', 70.0)
            readValue(self, data, 'daytime', 8.31)
            readValue(self, data, 'sunStealthFactor', Curve())
            readValue(self, data, 'cloudStealthFactorDistance', 120.0)
            readValue(self, data, 'seaLevelForFlightMdel', 0.0)
            readValue(self, data, 'altitudeMap', 0.0)
            readValue(self, data, 'anyTeamObjectsCount', 5)
            readValue(self, data, 'randomObjectsCount', 5)
            if IS_CLIENT:
                readValue(self, data, 'name', '')
                readValue(self, data, 'description', '')
                readValue(self, data, 'outroScenario', '')
                readValue(self, data, 'outroTimeline', '')
                readValue(self, data, 'music', '')
                readValue(self, data, 'musicPrefix', '')
                readValue(self, data, 'ambientSound', '')
                readValue(self, data, 'umbraEnabled', 0)
                readValue(self, data, 'batchingEnabled', 0)
                stingersSection = findSection(data, 'stingers')
                self.stingers = SoundsStingers(stingersSection) if stingersSection else None
                self.waterTexScale = data.readFloat('water/texScale', 0.5)
                self.waterFreqX = data.readFloat('water/freqX', 1.0)
                self.waterFreqZ = data.readFloat('water/freqZ', 1.0)
            if IS_BASEAPP:
                readValue(self, data, 'kickAfterFinishWaitTime', 0)
                if self.kickAfterFinishWaitTime < 0:
                    self.__raiseWrongXml("wrong 'kickAfterFinishWaitTime' value")
                readValue(self, data, 'arenaStartDelay', 0)
                if self.arenaStartDelay <= 0:
                    self.__raiseWrongXml("wrong 'arenaStartDelay' value")
                groups = findSection(data, 'objectGroups')
                if groups:
                    for groupID, groupData in groups.items():
                        self.objectGroups.addGroup(groupID, groupData)

                selectGroups = findSection(data, 'selectGroups')
                if selectGroups:
                    self.objectGroups.readSpawnSequence(selectGroups)
            if IS_CLIENT:
                weatherPath = self.geometry + '/space.settings/weatherSettings/'
                weatherData = ResMgr.openSection(weatherPath)
                if weatherData:
                    self.weatherWindSpeed = weatherData.readVector2('windSpeed')
                    self.weatherWindGustiness = weatherData.readFloat('windGustiness', 0.0)
                    ResMgr.purge(weatherPath)
                else:
                    self.weatherWindSpeed = (0.0, 0.0)
                    self.weatherWindGustiness = 0.0
            return

    def _loadTextureMaterials(self, fileName):
        path = LANDSCAPE_PATH + fileName + '/textures_materials.xml'
        materials = ResMgr.openSection(path)
        if materials is None:
            return
        else:
            self._textureMaterials = {v['texutre_name'].asString:v['material_id'].asInt for v in materials.values()}
            ResMgr.purge(path)
            return

    def getTextureMaterialID(self, textureName):
        return self._textureMaterials.get(textureName)

    def __raiseWrongXml(self, msg):
        raise Exception, "wrong arena type XML '%s': %s" % (self.typeID, msg)