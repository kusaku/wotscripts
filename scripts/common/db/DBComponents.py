# Embedded file name: scripts/common/db/DBComponents.py
import Math
import math
from consts import WORLD_SCALING, AIRCRAFTS_PATH, MAX_WEAPON_GROUP, COMPONENT_TYPE
from DBHelpers import *
from Curve import Curve
from debug_utils import DBLOG_ERROR, DBLOG_NOTE, DBLOG_CRITICAL, LOG_DEBUG, LOG_WARNING

class ComponentsDB:

    def __init__(self, db):
        """database - reference to new-style database, please see _aircrafts_db.py for more
        database structure; also check DBLogic to see how this database is imported."""
        self.__components = {COMPONENT_TYPE.ROCKETS: (self.__convertComponentArray2Map(db.rocket), db.rocket),
         COMPONENT_TYPE.BOMBS: (self.__convertComponentArray2Map(db.bomb), db.bomb),
         COMPONENT_TYPE.GUNS: (self.__convertComponentArray2Map(db.gun), db.gun),
         COMPONENT_TYPE.AMMO: (self.__convertComponentArray2Map(db.ammo), db.ammo),
         COMPONENT_TYPE.AMMOBELT: (self.__convertComponentArray2Map(db.ammoBelt), db.ammoBelt)}

    def __convertComponentArray2Map(self, componentArray):
        d = {}
        for i, component in enumerate(componentArray):
            component.index = i
            d[component.name] = component

        return d

    def findComponent(self, componentsGroupID, componentName):
        return self.__components[componentsGroupID][0].get(componentName, None)

    def getComponentByIndex(self, componentsGroupID, componentIndex):
        """
        It's a critical error if there's no component with given ID.
        """
        componentCategory = self.__components.get(componentsGroupID, None)
        if componentCategory:
            if componentIndex >= 0 and componentIndex < len(componentCategory[1]):
                return componentCategory[1][componentIndex]
            DBLOG_CRITICAL('Cannot find ' + str(componentsGroupID) + ' with illegal index ' + str(componentIndex))
        else:
            DBLOG_CRITICAL('Cannot find invalid component category ID ' + str(componentsGroupID))
        return

    def getComponentsDict(self, componentsGroupID):
        """
        Returns dict of components
        @param componentsGroupID:
        @rtype : dict
        """
        return self.__components[componentsGroupID][0]

    def getComponents(self, componentsGroupID):
        """
        Get components DB
        @param componentsGroupID: some of COMPONENT_TYPE class const
        @return:
        """
        return self.__components[componentsGroupID][1]


class WeaponSettings:

    def __init__(self, data, slotId):
        self.slotId = slotId
        self.readData(data)

    def readData(self, data):
        if data:
            readValue(self, data, 'name', 'n/a')
            self.name = self.name.lower()
            readValue(self, data, 'flamePath', '')
            readValue(self, data, 'shellPath', '_')
            readValue(self, data, 'weaponGroup', 0)
            readValue(self, data, 'dispersionAngle', 0.0)
            readValue(self, data, 'recoilDispersion', 0.0)
            readValue(self, data, 'autoguiderAngle', 0.0)
            readValue(self, data, 'overheatingFullTime', 1000.0)
            readValue(self, data, 'coolingCFC', 1.0)
            if self.weaponGroup <= 0 or self.weaponGroup >= MAX_WEAPON_GROUP:
                LOG_WARNING('Wrong/undefined weaponGroup={0} for weapon={1}, slotId={2}. Should be > 0 and < {3}'.format(self.weaponGroup, self.name, self.slotId, MAX_WEAPON_GROUP))
                self.weaponGroup = 1
            readValue(self, data, 'ammoBelt', '')
            self.ammoBelt = self.ammoBelt.lower()


class WeaponSlotLinkedModel:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data:
            readValue(self, data, 'parentUpgrade', 0)
            readValue(self, data, 'model', '')
            readValue(self, data, 'mountPath', '')


class WeaponTypeSettings:

    def __init__(self, data, slotId):
        self.id = -1
        self.weapons = []
        self.readData(data, slotId)

    def readData(self, data, slotId):
        self.weapons = []
        self.linkedModels = []
        if data:
            readValue(self, data, 'id', -1)
            readValue(self, data, 'name', '')
            for sName, sData in data.items():
                if sName == 'weapon':
                    self.weapons.append(WeaponSettings(sData, slotId))
                elif sName == 'linkedModels':
                    for msName, msData in sData.items():
                        if msName == 'visual':
                            self.linkedModels.append(WeaponSlotLinkedModel(msData))


class WeaponSlotSettings:

    def __init__(self, data = None):
        self.id = -1
        self.name = ''
        self.types = {}
        self.readData(data)

    def readData(self, data = None):
        self.types = {}
        if data != None:
            readValue(self, data, 'id', -1)
            readValue(self, data, 'name', '')
            for sName, sData in data.items():
                if sName == 'type':
                    weaponType = WeaponTypeSettings(sData, self.id)
                    if weaponType.id != -1:
                        if weaponType.id not in self.types:
                            self.types[weaponType.id] = weaponType
                        else:
                            LOG_ERROR('Dublicate weapon weaponType', weaponType)
                    else:
                        LOG_ERROR('Invalid weapon weaponType id', self.id)

        return


class WeaponsSettings:

    def __init__(self, data = None):
        self.slots = {}
        self.readData(data)

    def readData(self, data = None):
        self.slots = {}
        if data != None:
            readValue(self, data, 'reductionPoint', 10000.0)
            if readValue(self, data, 'autoguiderMaxDist', -1.0):
                self.autoguiderMaxDist *= WORLD_SCALING
            for sName, sData in data.items():
                if sName == 'slot':
                    slot = WeaponSlotSettings(sData)
                    if slot.id != -1:
                        if slot.id not in self.slots:
                            self.slots[slot.id] = slot
                        else:
                            LOG_ERROR('Dublicate weapon slot')
                    else:
                        LOG_ERROR('Invalid weapon slot id')

        return


class ComponentsTunes:

    def __init__(self, data = None):
        self.weapons = None
        self.weapons2 = None
        self.readData(data)
        return

    def readData(self, data):
        if data != None:
            componentsData = findSection(data, 'Components')
            if componentsData is not None:
                weapons2Section = findSection(componentsData, 'Weapons2')
                if weapons2Section:
                    if self.weapons2:
                        self.weapons2.readData(weapons2Section)
                    else:
                        self.weapons2 = WeaponsSettings(weapons2Section)
                else:
                    CRITICAL_ERROR('weapons2 section loading error', data.name)
        return


class ShellSoundSettings:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'start', '')
            readValue(self, data, 'flight', '')
            readValue(self, data, 'explosion', '')
        return