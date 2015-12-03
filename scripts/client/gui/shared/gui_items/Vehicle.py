# Embedded file name: scripts/client/gui/shared/gui_items/Vehicle.py
from itertools import izip
import BigWorld
from operator import itemgetter
import constants
from AccountCommands import LOCK_REASON, VEHICLE_SETTINGS_FLAG
from constants import WIN_XP_FACTOR_MODE
from gui.prb_control import prb_getters
from shared_utils import findFirst, CONST_CONTAINER
from gui import makeHtmlString
from gui.shared.economics import calcRentPackages, getActionPrc
from helpers import i18n, time_utils
from items import vehicles, tankmen, getTypeInfoByName
from account_shared import LayoutIterator
from gui.prb_control.settings import PREBATTLE_SETTING_NAME
from gui.shared.gui_items import CLAN_LOCK, HasStrCD, FittingItem, GUI_ITEM_TYPE, getItemIconName, RentalInfoProvider
from gui.shared.gui_items.vehicle_modules import Shell, VehicleChassis, VehicleEngine, VehicleRadio, VehicleFuelTank, VehicleTurret, VehicleGun
from gui.shared.gui_items.artefacts import Equipment, OptionalDevice
from gui.shared.gui_items.Tankman import Tankman
from gui.Scaleform.locale.ITEM_TYPES import ITEM_TYPES

class VEHICLE_CLASS_NAME(CONST_CONTAINER):
    LIGHT_TANK = 'lightTank'
    MEDIUM_TANK = 'mediumTank'
    HEAVY_TANK = 'heavyTank'
    SPG = 'SPG'
    AT_SPG = 'AT-SPG'


VEHICLE_TYPES_ORDER = (VEHICLE_CLASS_NAME.LIGHT_TANK,
 VEHICLE_CLASS_NAME.MEDIUM_TANK,
 VEHICLE_CLASS_NAME.HEAVY_TANK,
 VEHICLE_CLASS_NAME.AT_SPG,
 VEHICLE_CLASS_NAME.SPG)
VEHICLE_TYPES_ORDER_INDICES = dict(((n, i) for i, n in enumerate(VEHICLE_TYPES_ORDER)))

def compareByVehTypeName(vehTypeA, vehTypeB):
    return VEHICLE_TYPES_ORDER_INDICES[vehTypeA] - VEHICLE_TYPES_ORDER_INDICES[vehTypeB]


VEHICLE_TABLE_TYPES_ORDER = (VEHICLE_CLASS_NAME.HEAVY_TANK,
 VEHICLE_CLASS_NAME.MEDIUM_TANK,
 VEHICLE_CLASS_NAME.LIGHT_TANK,
 VEHICLE_CLASS_NAME.AT_SPG,
 VEHICLE_CLASS_NAME.SPG)
VEHICLE_TABLE_TYPES_ORDER_INDICES = dict(((n, i) for i, n in enumerate(VEHICLE_TABLE_TYPES_ORDER)))
VEHICLE_BATTLE_TYPES_ORDER = (VEHICLE_CLASS_NAME.HEAVY_TANK,
 VEHICLE_CLASS_NAME.MEDIUM_TANK,
 VEHICLE_CLASS_NAME.AT_SPG,
 VEHICLE_CLASS_NAME.SPG,
 VEHICLE_CLASS_NAME.LIGHT_TANK)
VEHICLE_BATTLE_TYPES_ORDER_INDICES = dict(((n, i) for i, n in enumerate(VEHICLE_BATTLE_TYPES_ORDER)))

class VEHICLE_TAGS(CONST_CONTAINER):
    PREMIUM = 'premium'
    PREMIUM_IGR = 'premiumIGR'
    CANNOT_BE_SOLD = 'cannot_be_sold'
    SECRET = 'secret'
    SPECIAL = 'special'
    OBSERVER = 'observer'
    DISABLED_IN_ROAMING = 'disabledInRoaming'
    EVENT = 'event_battles'
    EXCLUDED_FROM_SANDBOX = 'excluded_from_sandbox'


class Vehicle(FittingItem, HasStrCD):
    NOT_FULL_AMMO_MULTIPLIER = 0.2
    MAX_RENT_MULTIPLIER = 2

    class VEHICLE_STATE:
        DAMAGED = 'damaged'
        EXPLODED = 'exploded'
        DESTROYED = 'destroyed'
        UNDAMAGED = 'undamaged'
        BATTLE = 'battle'
        IN_PREBATTLE = 'inPrebattle'
        LOCKED = 'locked'
        CREW_NOT_FULL = 'crewNotFull'
        AMMO_NOT_FULL = 'ammoNotFull'
        AMMO_NOT_FULL_EVENTS = 'ammoNotFullEvents'
        SERVER_RESTRICTION = 'serverRestriction'
        RENTAL_IS_ORVER = 'rentalIsOver'
        IGR_RENTAL_IS_ORVER = 'igrRentalIsOver'
        IN_PREMIUM_IGR_ONLY = 'inPremiumIgrOnly'
        NOT_SUITABLE = 'not_suitable'
        GROUP_IS_NOT_READY = 'group_is_not_ready'
        NOT_PRESENT = ('notpresent',)
        UNAVAILABLE = ('unavailable',)
        FALLOUT_ONLY = 'fallout_only'
        FALLOUT_MIN = 'fallout_min'
        FALLOUT_MAX = 'fallout_max'
        FALLOUT_REQUIRED = 'fallout_required'
        FALLOUT_BROKEN = 'fallout_broken'
        UNSUITABLE_TO_QUEUE = 'unsuitableToQueue'
        CUSTOM = (NOT_SUITABLE, UNSUITABLE_TO_QUEUE)

    CAN_SELL_STATES = [VEHICLE_STATE.UNDAMAGED,
     VEHICLE_STATE.CREW_NOT_FULL,
     VEHICLE_STATE.AMMO_NOT_FULL,
     VEHICLE_STATE.GROUP_IS_NOT_READY,
     VEHICLE_STATE.FALLOUT_MIN,
     VEHICLE_STATE.FALLOUT_MAX,
     VEHICLE_STATE.FALLOUT_REQUIRED,
     VEHICLE_STATE.FALLOUT_BROKEN,
     VEHICLE_STATE.FALLOUT_ONLY,
     VEHICLE_STATE.UNSUITABLE_TO_QUEUE]
    GROUP_STATES = [VEHICLE_STATE.GROUP_IS_NOT_READY,
     VEHICLE_STATE.FALLOUT_MIN,
     VEHICLE_STATE.FALLOUT_MAX,
     VEHICLE_STATE.FALLOUT_REQUIRED,
     VEHICLE_STATE.FALLOUT_BROKEN]

    class VEHICLE_STATE_LEVEL:
        CRITICAL = 'critical'
        INFO = 'info'
        WARNING = 'warning'
        RENTED = 'rented'

    def __init__(self, strCompactDescr = None, inventoryID = -1, typeCompDescr = None, proxy = None):
        if strCompactDescr is not None:
            vehDescr = vehicles.VehicleDescr(compactDescr=strCompactDescr)
        else:
            raise typeCompDescr is not None or AssertionError
            _, nID, innID = vehicles.parseIntCompactDescr(typeCompDescr)
            vehDescr = vehicles.VehicleDescr(typeID=(nID, innID))
        self.__descriptor = vehDescr
        HasStrCD.__init__(self, strCompactDescr)
        FittingItem.__init__(self, vehDescr.type.compactDescr, proxy)
        self.inventoryID = inventoryID
        self.xp = 0
        self.dailyXPFactor = -1
        self.isElite = False
        self.isFullyElite = False
        self.clanLock = 0
        self.isUnique = self.isHidden
        self.rentPackages = []
        self.hasRentPackages = False
        self.isDisabledForBuy = False
        invData = dict()
        if proxy is not None and proxy.inventory.isSynced() and proxy.stats.isSynced() and proxy.shop.isSynced():
            invDataTmp = proxy.inventory.getItems(GUI_ITEM_TYPE.VEHICLE, inventoryID)
            if invDataTmp is not None:
                invData = invDataTmp
            self.xp = proxy.stats.vehiclesXPs.get(self.intCD, self.xp)
            if proxy.shop.winXPFactorMode == WIN_XP_FACTOR_MODE.ALWAYS or self.intCD not in proxy.stats.multipliedVehicles:
                self.dailyXPFactor = proxy.shop.dailyXPFactor
            self.isElite = len(vehDescr.type.unlocksDescrs) == 0 or self.intCD in proxy.stats.eliteVehicles
            self.isFullyElite = self.isElite and len([ data for data in vehDescr.type.unlocksDescrs if data[1] not in proxy.stats.unlocks ]) == 0
            clanDamageLock = proxy.stats.vehicleTypeLocks.get(self.intCD, {}).get(CLAN_LOCK, 0)
            clanNewbieLock = proxy.stats.globalVehicleLocks.get(CLAN_LOCK, 0)
            self.clanLock = clanDamageLock or clanNewbieLock
            self.isDisabledForBuy = self.intCD in proxy.shop.getNotToBuyVehicles()
            self.hasRentPackages = bool(proxy.shop.getVehicleRentPrices().get(self.intCD, {}))
        self.inventoryCount = 1 if len(invData.keys()) else 0
        data = invData.get('rent')
        if data is not None:
            self.rentInfo = RentalInfoProvider(isRented=True, *data)
        self.settings = invData.get('settings', 0)
        self.lock = invData.get('lock', (0, 0))
        self.repairCost, self.health = invData.get('repair', (0, 0))
        self.gun = VehicleGun(vehDescr.gun['compactDescr'], proxy, vehDescr.gun)
        self.turret = VehicleTurret(vehDescr.turret['compactDescr'], proxy, vehDescr.turret)
        self.engine = VehicleEngine(vehDescr.engine['compactDescr'], proxy, vehDescr.engine)
        self.chassis = VehicleChassis(vehDescr.chassis['compactDescr'], proxy, vehDescr.chassis)
        self.radio = VehicleRadio(vehDescr.radio['compactDescr'], proxy, vehDescr.radio)
        self.fuelTank = VehicleFuelTank(vehDescr.fuelTank['compactDescr'], proxy, vehDescr.fuelTank)
        self.sellPrice = self._calcSellPrice(proxy)
        self.defaultSellPrice = self._calcDefaultSellPrice(proxy)
        self.optDevices = self._parserOptDevs(vehDescr.optionalDevices, proxy)
        gunAmmoLayout = []
        for shell in self.gun.defaultAmmo:
            gunAmmoLayout += (shell.intCD, shell.defaultCount)

        self.shells = self._parseShells(invData.get('shells', list()), invData.get('shellsLayout', dict()).get(self.shellsLayoutIdx, gunAmmoLayout), proxy)
        self.eqs = self._parseEqs(invData.get('eqs') or [0, 0, 0], proxy)
        self.eqsLayout = self._parseEqs(invData.get('eqsLayout') or [0, 0, 0], proxy)
        defaultCrew = [None] * len(vehDescr.type.crewRoles)
        crewList = invData.get('crew', defaultCrew)
        self.bonuses = self._calcCrewBonuses(crewList, proxy)
        self.crewIndices = dict([ (invID, idx) for idx, invID in enumerate(crewList) ])
        self.crew = self._buildCrew(crewList, proxy)
        self.lastCrew = invData.get('lastCrew')
        self.rentPackages = calcRentPackages(self, proxy)
        self.__customState = ''
        return

    @property
    def buyPrice(self):
        if self.isRented and not self.rentalIsOver:
            return (self._buyPrice[0] - self.rentCompensation[0], self._buyPrice[1] - self.rentCompensation[1])
        return self._buyPrice

    def getUnlockDescrByIntCD(self, intCD):
        for unlockIdx, data in enumerate(self.descriptor.type.unlocksDescrs):
            if intCD == data[1]:
                return (unlockIdx, data[0], set(data[2:]))

        return (-1, 0, set())

    def _calcSellPrice(self, proxy):
        if self.isRented:
            return (0, 0)
        price = list(self.sellPrice)
        defaultDevices, installedDevices, _ = self.descriptor.getDevices()
        for defCompDescr, instCompDescr in izip(defaultDevices, installedDevices):
            if defCompDescr == instCompDescr:
                continue
            modulePrice = FittingItem(defCompDescr, proxy).sellPrice
            price = (price[0] - modulePrice[0], price[1] - modulePrice[1])
            modulePrice = FittingItem(instCompDescr, proxy).sellPrice
            price = (price[0] + modulePrice[0], price[1] + modulePrice[1])

        return price

    def _calcDefaultSellPrice(self, proxy):
        if self.isRented:
            return (0, 0)
        price = list(self.defaultSellPrice)
        defaultDevices, installedDevices, _ = self.descriptor.getDevices()
        for defCompDescr, instCompDescr in izip(defaultDevices, installedDevices):
            if defCompDescr == instCompDescr:
                continue
            modulePrice = FittingItem(defCompDescr, proxy).defaultSellPrice
            price = (price[0] - modulePrice[0], price[1] - modulePrice[1])
            modulePrice = FittingItem(instCompDescr, proxy).defaultSellPrice
            price = (price[0] + modulePrice[0], price[1] + modulePrice[1])

        return price

    def _calcCrewBonuses(self, crew, proxy):
        bonuses = dict()
        bonuses['equipment'] = 0
        for eq in self.eqs:
            if eq is not None:
                bonuses['equipment'] += eq.crewLevelIncrease

        bonuses['optDevices'] = self.descriptor.miscAttrs['crewLevelIncrease']
        bonuses['commander'] = 0
        commanderEffRoleLevel = 0
        bonuses['brotherhood'] = tankmen.getSkillsConfig()['brotherhood']['crewLevelIncrease']
        femalesCount = 0
        for tankmanID in crew:
            if tankmanID is None:
                bonuses['brotherhood'] = 0
                continue
            tmanInvData = proxy.inventory.getItems(GUI_ITEM_TYPE.TANKMAN, tankmanID)
            if not tmanInvData:
                continue
            tdescr = tankmen.TankmanDescr(compactDescr=tmanInvData['compDescr'])
            if tdescr.isFemale:
                femalesCount += 1
            if 'brotherhood' not in tdescr.skills or tdescr.skills.index('brotherhood') == len(tdescr.skills) - 1 and tdescr.lastSkillLevel != tankmen.MAX_SKILL_LEVEL:
                bonuses['brotherhood'] = 0
            if tdescr.role == Tankman.ROLES.COMMANDER:
                factor, addition = tdescr.efficiencyOnVehicle(self.descriptor)
                commanderEffRoleLevel = round(tdescr.roleLevel * factor + addition)

        if femalesCount and len(crew) != femalesCount:
            bonuses['brotherhood'] = 0
        bonuses['commander'] += round((commanderEffRoleLevel + bonuses['brotherhood'] + bonuses['equipment']) / tankmen.COMMANDER_ADDITION_RATIO)
        return bonuses

    def _buildCrew(self, crew, proxy):
        crewItems = list()
        crewRoles = self.descriptor.type.crewRoles
        for idx, tankmanID in enumerate(crew):
            tankman = None
            if tankmanID is not None:
                tmanInvData = proxy.inventory.getItems(GUI_ITEM_TYPE.TANKMAN, tankmanID)
                tankman = Tankman(strCompactDescr=tmanInvData['compDescr'], inventoryID=tankmanID, vehicle=self, proxy=proxy)
            crewItems.append((idx, tankman))

        RO = Tankman.TANKMEN_ROLES_ORDER
        return sorted(crewItems, cmp=lambda a, b: RO[crewRoles[a[0]][0]] - RO[crewRoles[b[0]][0]])

    @staticmethod
    def __crewSort(t1, t2):
        if t1 is None or t2 is None:
            return 0
        else:
            return t1.__cmp__(t2)

    def _parseCompDescr(self, compactDescr):
        nId, innID = vehicles.parseVehicleCompactDescr(compactDescr)
        return (vehicles._VEHICLE, nId, innID)

    def _parseShells(self, layoutList, defaultLayoutList, proxy):
        shellsDict = dict(((cd, count) for cd, count, _ in LayoutIterator(layoutList)))
        defaultsDict = dict(((cd, (count, isBoughtForCredits)) for cd, count, isBoughtForCredits in LayoutIterator(defaultLayoutList)))
        layoutList = list(layoutList)
        for shot in self.descriptor.gun['shots']:
            cd = shot['shell']['compactDescr']
            if cd not in shellsDict:
                layoutList.extend([cd, 0])

        result = list()
        for idx, (intCD, count, _) in enumerate(LayoutIterator(layoutList)):
            defaultCount, isBoughtForCredits = defaultsDict.get(intCD, (0, False))
            result.append(Shell(intCD, count, defaultCount, proxy, isBoughtForCredits))

        return result

    @classmethod
    def _parseEqs(cls, layoutList, proxy):
        result = list()
        for i in xrange(len(layoutList)):
            intCD = abs(layoutList[i])
            result.append(Equipment(intCD, proxy, layoutList[i] < 0) if intCD != 0 else None)

        return result

    @classmethod
    def _parserOptDevs(cls, layoutList, proxy):
        result = list()
        for i in xrange(len(layoutList)):
            optDevDescr = layoutList[i]
            result.append(OptionalDevice(optDevDescr['compactDescr'], proxy) if optDevDescr is not None else None)

        return result

    @property
    def iconContour(self):
        return getContourIconPath(self.name)

    @property
    def iconUnique(self):
        return getUniqueIconPath(self.name, withLightning=False)

    @property
    def iconUniqueLight(self):
        return getUniqueIconPath(self.name, withLightning=True)

    @property
    def shellsLayoutIdx(self):
        return (self.turret.descriptor['compactDescr'], self.gun.descriptor['compactDescr'])

    @property
    def invID(self):
        return self.inventoryID

    @property
    def isRentable(self):
        return self.hasRentPackages and not self.isPurchased

    @property
    def isPurchased(self):
        return self.isInInventory and not self.rentInfo.isRented

    @property
    def rentExpiryTime(self):
        return self.rentInfo.rentExpiryTime

    @property
    def rentCompensation(self):
        return self.rentInfo.compensations

    @property
    def isRentAvailable(self):
        return self.maxRentDuration - self.rentLeftTime >= self.minRentDuration

    @property
    def minRentPrice(self):
        minRentPackage = self.getRentPackage()
        if minRentPackage is not None:
            return minRentPackage.get('rentPrice', None)
        else:
            return

    @property
    def isRented(self):
        return self.rentInfo.isRented

    @property
    def rentLeftTime(self):
        return float(time_utils.getTimeDeltaFromNow(time_utils.makeLocalServerTime(self.rentExpiryTime)))

    @property
    def maxRentDuration(self):
        if len(self.rentPackages) > 0:
            return max((item['days'] for item in self.rentPackages)) * self.MAX_RENT_MULTIPLIER * time_utils.ONE_DAY
        return 0

    @property
    def minRentDuration(self):
        if len(self.rentPackages) > 0:
            return min((item['days'] for item in self.rentPackages)) * time_utils.ONE_DAY
        return 0

    @property
    def rentalIsOver(self):
        return self.isRented and self.rentLimitIsReached

    @property
    def rentalIsActive(self):
        return self.isRented and not self.rentLimitIsReached

    @property
    def rentLeftBattles(self):
        return self.rentInfo.battlesLeft

    @property
    def rentLimitIsReached(self):
        return self.rentLeftTime <= 0 and self.rentLeftBattles <= 0

    @property
    def descriptor(self):
        return self.__descriptor

    @property
    def type(self):
        return set(vehicles.VEHICLE_CLASS_TAGS & self.tags).pop()

    @property
    def typeUserName(self):
        return getTypeUserName(self.type, self.isElite)

    @property
    def hasTurrets(self):
        vDescr = self.descriptor
        return len(vDescr.hull['fakeTurrets']['lobby']) != len(vDescr.turrets)

    @property
    def hasBattleTurrets(self):
        vDescr = self.descriptor
        return len(vDescr.hull['fakeTurrets']['battle']) != len(vDescr.turrets)

    @property
    def ammoMaxSize(self):
        return self.descriptor.gun['maxAmmo']

    @property
    def isAmmoFull(self):
        return sum((s.count for s in self.shells)) >= self.ammoMaxSize * self.NOT_FULL_AMMO_MULTIPLIER

    @property
    def hasShells(self):
        return sum((s.count for s in self.shells)) > 0

    @property
    def hasCrew(self):
        return findFirst(lambda x: x[1] is not None, self.crew) is not None

    @property
    def modelState(self):
        if self.health < 0:
            return Vehicle.VEHICLE_STATE.EXPLODED
        if self.repairCost > 0 and self.health == 0:
            return Vehicle.VEHICLE_STATE.DESTROYED
        return Vehicle.VEHICLE_STATE.UNDAMAGED

    def getState(self, isCurrnentPlayer = True):
        ms = self.modelState
        if self.isInBattle:
            ms = Vehicle.VEHICLE_STATE.BATTLE
        elif self.rentalIsOver:
            ms = Vehicle.VEHICLE_STATE.RENTAL_IS_ORVER
            if self.isPremiumIGR:
                ms = Vehicle.VEHICLE_STATE.IGR_RENTAL_IS_ORVER
        elif self.isDisabledInPremIGR:
            ms = Vehicle.VEHICLE_STATE.IN_PREMIUM_IGR_ONLY
        elif self.isInPrebattle:
            ms = Vehicle.VEHICLE_STATE.IN_PREBATTLE
        elif self.isLocked:
            ms = Vehicle.VEHICLE_STATE.LOCKED
        elif self.isDisabledInRoaming:
            ms = Vehicle.VEHICLE_STATE.SERVER_RESTRICTION
        ms = self.__checkUndamagedState(ms, isCurrnentPlayer)
        if ms in Vehicle.CAN_SELL_STATES and self.__customState:
            ms = self.__customState
        return (ms, self.__getStateLevel(ms))

    def setCustomState(self, state):
        raise state in Vehicle.VEHICLE_STATE.CUSTOM or AssertionError('State is not valid')
        self.__customState = state

    def getCustomState(self):
        return self.__customState

    def clearCustomState(self):
        self.__customState = ''

    def __checkUndamagedState(self, state, isCurrnentPlayer = True):
        if state == Vehicle.VEHICLE_STATE.UNDAMAGED and isCurrnentPlayer:
            if self.isBroken:
                return Vehicle.VEHICLE_STATE.DAMAGED
            if not self.isCrewFull:
                return Vehicle.VEHICLE_STATE.CREW_NOT_FULL
            groupIsReady, groupState = self.isGroupReady()
            if self.isFalloutSelected and not groupIsReady:
                return groupState
            if not self.isAmmoFull:
                return Vehicle.VEHICLE_STATE.AMMO_NOT_FULL
            if self.isFalloutOnly() and not self.__isFalloutEnabled():
                return Vehicle.VEHICLE_STATE.FALLOUT_ONLY
        return state

    @classmethod
    def __getEventVehicles(cls):
        from gui.server_events import g_eventsCache
        return g_eventsCache.getEventVehicles()

    @classmethod
    def __getFalloutSelectedVehInvIDs(cls):
        from gui.game_control import getFalloutCtrl
        if Vehicle.__isFalloutEnabled():
            return getFalloutCtrl().getSelectedSlots()
        return ()

    @classmethod
    def __getFalloutAvailableVehIDs(cls):
        from gui.game_control import getFalloutCtrl
        if Vehicle.__isFalloutEnabled():
            return getFalloutCtrl().getConfig().allowedVehicles
        return ()

    @classmethod
    def __isFalloutEnabled(cls):
        from gui.game_control import getFalloutCtrl
        return getFalloutCtrl().isSelected()

    def isFalloutOnly(self):
        return self.isOnlyForEventBattles

    def isGroupReady(self):
        from gui.game_control import getFalloutCtrl
        falloutCtrl = getFalloutCtrl()
        if not falloutCtrl.isSelected():
            return (True, '')
        selectedVehicles = falloutCtrl.getSelectedVehicles()
        selectedVehiclesCount = len(selectedVehicles)
        config = falloutCtrl.getConfig()
        if falloutCtrl.mustSelectRequiredVehicle():
            return (False, Vehicle.VEHICLE_STATE.FALLOUT_REQUIRED)
        if selectedVehiclesCount < config.minVehiclesPerPlayer:
            return (False, Vehicle.VEHICLE_STATE.FALLOUT_MIN)
        if selectedVehiclesCount > config.maxVehiclesPerPlayer:
            return (False, Vehicle.VEHICLE_STATE.FALLOUT_MAX)
        for v in selectedVehicles:
            if v.isBroken or not v.isCrewFull or v.isInBattle or v.rentalIsOver or v.isDisabledInPremIGR:
                return (False, Vehicle.VEHICLE_STATE.FALLOUT_BROKEN)

        return (True, '')

    def __getStateLevel(self, state):
        if state in (Vehicle.VEHICLE_STATE.CREW_NOT_FULL,
         Vehicle.VEHICLE_STATE.DAMAGED,
         Vehicle.VEHICLE_STATE.EXPLODED,
         Vehicle.VEHICLE_STATE.DESTROYED,
         Vehicle.VEHICLE_STATE.SERVER_RESTRICTION,
         Vehicle.VEHICLE_STATE.RENTAL_IS_ORVER,
         Vehicle.VEHICLE_STATE.IGR_RENTAL_IS_ORVER,
         Vehicle.VEHICLE_STATE.AMMO_NOT_FULL_EVENTS,
         Vehicle.VEHICLE_STATE.NOT_SUITABLE):
            return Vehicle.VEHICLE_STATE_LEVEL.CRITICAL
        if state in (Vehicle.VEHICLE_STATE.UNDAMAGED,):
            return Vehicle.VEHICLE_STATE_LEVEL.INFO
        return Vehicle.VEHICLE_STATE_LEVEL.WARNING

    @property
    def isPremium(self):
        return _checkForTags(self.tags, VEHICLE_TAGS.PREMIUM)

    @property
    def isPremiumIGR(self):
        return _checkForTags(self.tags, VEHICLE_TAGS.PREMIUM_IGR)

    @property
    def isSecret(self):
        return _checkForTags(self.tags, VEHICLE_TAGS.SECRET)

    @property
    def isSpecial(self):
        return _checkForTags(self.tags, VEHICLE_TAGS.SPECIAL)

    @property
    def isExcludedFromSandbox(self):
        return _checkForTags(self.tags, VEHICLE_TAGS.EXCLUDED_FROM_SANDBOX)

    @property
    def isObserver(self):
        return _checkForTags(self.tags, VEHICLE_TAGS.OBSERVER)

    @property
    def isEvent(self):
        return self.isOnlyForEventBattles and self in Vehicle.__getEventVehicles()

    @property
    def isFalloutSelected(self):
        return self.invID in self.__getFalloutSelectedVehInvIDs()

    @property
    def isFalloutAvailable(self):
        return self.intCD in self.__getFalloutAvailableVehIDs()

    @property
    def isDisabledInRoaming(self):
        from gui.LobbyContext import g_lobbyContext
        return _checkForTags(self.tags, VEHICLE_TAGS.DISABLED_IN_ROAMING) and g_lobbyContext.getServerSettings().roaming.isInRoaming()

    def canNotBeSold(self):
        return _checkForTags(self.tags, VEHICLE_TAGS.CANNOT_BE_SOLD)

    @property
    def isDisabledInPremIGR(self):
        from gui.game_control import g_instance
        return self.isPremiumIGR and g_instance.igr.getRoomType() != constants.IGR_TYPE.PREMIUM

    @property
    def name(self):
        return self.descriptor.type.name

    @property
    def userName(self):
        return getUserName(self.descriptor.type)

    @property
    def longUserName(self):
        typeInfo = getTypeInfoByName('vehicle')
        tagsDump = [ typeInfo['tags'][tag]['userString'] for tag in self.tags if typeInfo['tags'][tag]['userString'] != '' ]
        return '%s %s' % (''.join(tagsDump), getUserName(self.descriptor.type))

    @property
    def shortUserName(self):
        return getShortUserName(self.descriptor.type)

    @property
    def level(self):
        return self.descriptor.type.level

    @property
    def fullDescription(self):
        if self.descriptor.type.description.find('_descr') == -1:
            return self.descriptor.type.description
        return ''

    @property
    def tags(self):
        return self.descriptor.type.tags

    @property
    def canSell(self):
        st, _ = self.getState()
        if self.isRented:
            if not self.rentalIsOver:
                return False
            if st in (self.VEHICLE_STATE.RENTAL_IS_ORVER, self.VEHICLE_STATE.IGR_RENTAL_IS_ORVER):
                st = self.__checkUndamagedState(self.modelState)
        return st in self.CAN_SELL_STATES and not _checkForTags(self.tags, VEHICLE_TAGS.CANNOT_BE_SOLD)

    @property
    def isLocked(self):
        return self.lock[0] != LOCK_REASON.NONE

    @property
    def isInBattle(self):
        return self.lock[0] == LOCK_REASON.ON_ARENA

    @property
    def isInPrebattle(self):
        return self.lock[0] in (LOCK_REASON.PREBATTLE, LOCK_REASON.UNIT, LOCK_REASON.UNIT_CLUB)

    @property
    def isAwaitingBattle(self):
        return self.lock[0] == LOCK_REASON.IN_QUEUE

    @property
    def isInUnit(self):
        return self.lock[0] in (LOCK_REASON.UNIT, LOCK_REASON.UNIT_CLUB)

    @property
    def typeOfLockingArena(self):
        if not self.isLocked:
            return None
        else:
            return self.lock[1]
            return None

    @property
    def isBroken(self):
        return self.repairCost > 0

    @property
    def isAlive(self):
        return not self.isBroken and not self.isLocked

    @property
    def isCrewFull(self):
        crew = map(lambda (role, tman): tman, self.crew)
        return None not in crew and len(crew)

    @property
    def isOnlyForEventBattles(self):
        return _checkForTags(self.tags, VEHICLE_TAGS.EVENT)

    def hasLockMode(self):
        isBS = prb_getters.isBattleSession()
        if isBS:
            isBSVehicleLockMode = bool(prb_getters.getPrebattleSettings()[PREBATTLE_SETTING_NAME.VEHICLE_LOCK_MODE])
            if isBSVehicleLockMode and self.clanLock > 0:
                return True
        return False

    def isReadyToPrebattle(self, checkForRent = True):
        if checkForRent and self.rentalIsOver:
            return False
        if self.isFalloutOnly() and not self.__isFalloutEnabled():
            return False
        if not self.isGroupReady()[0]:
            return False
        result = not self.hasLockMode()
        if result:
            result = not self.isBroken and self.isCrewFull and not self.isDisabledInPremIGR and not self.isInBattle
        return result

    @property
    def isReadyToFight(self):
        if self.rentalIsOver:
            return False
        if self.isFalloutOnly() and not self.__isFalloutEnabled():
            return False
        if not self.isGroupReady()[0]:
            return False
        result = not self.hasLockMode()
        if result:
            result = self.isAlive and self.isCrewFull and not self.isDisabledInRoaming and not self.isDisabledInPremIGR
        return result

    @property
    def isXPToTman(self):
        return bool(self.settings & VEHICLE_SETTINGS_FLAG.XP_TO_TMAN)

    @property
    def isAutoRepair(self):
        return bool(self.settings & VEHICLE_SETTINGS_FLAG.AUTO_REPAIR)

    @property
    def isAutoLoad(self):
        return bool(self.settings & VEHICLE_SETTINGS_FLAG.AUTO_LOAD)

    @property
    def isAutoEquip(self):
        return bool(self.settings & VEHICLE_SETTINGS_FLAG.AUTO_EQUIP)

    @property
    def isFavorite(self):
        return bool(self.settings & VEHICLE_SETTINGS_FLAG.GROUP_0)

    def isAutoLoadFull(self):
        if self.isAutoLoad:
            for shell in self.shells:
                if shell.count != shell.defaultCount:
                    return False

        return True

    def isAutoEquipFull(self):
        if self.isAutoEquip:
            for i, e in enumerate(self.eqsLayout):
                if e != self.eqs[i]:
                    return False

        return True

    def mayPurchase(self, money):
        if self.isDisabledForBuy:
            return (False, 'isDisabledForBuy')
        if self.isPremiumIGR:
            return (False, 'premiumIGR')
        return super(Vehicle, self).mayPurchase(money)

    def mayRentOrBuy(self, money):
        if self.isDisabledForBuy and not self.isRentable:
            return (False, 'rental_disabled')
        if self.isRentable and not self.isRentAvailable:
            mayPurchase, reason = self.mayPurchase(money)
            if not mayPurchase:
                return (False, 'rental_time_exceeded')
        if self.minRentPrice:
            currency = ''
            if self.minRentPrice[1]:
                currency = 'gold'
                if self.minRentPrice[1] <= money[1]:
                    return (True, '')
            if self.minRentPrice[0]:
                currency = 'credit'
                if self.minRentPrice[0] <= money[0]:
                    return (True, '')
            return (False, '%s_rent_error' % currency)
        return self.mayPurchase(money)

    def getRentPackage(self, days = None):
        if days is not None:
            for package in self.rentPackages:
                if package.get('days', None) == days:
                    return package

        elif len(self.rentPackages) > 0:
            return min(self.rentPackages, key=itemgetter('rentPrice'))
        return

    def getGUIEmblemID(self):
        return self.icon

    def getRentPackageActionPrc(self, days = None):
        package = self.getRentPackage(days)
        if package:
            return getActionPrc(package['rentPrice'], package['defaultRentPrice'])
        return 0

    def getAutoUnlockedItems(self):
        return self.descriptor.type.autounlockedItems[:]

    def getAutoUnlockedItemsMap(self):
        return dict(map(lambda nodeCD: (vehicles.getDictDescr(nodeCD).get('itemTypeName'), nodeCD), self.descriptor.type.autounlockedItems))

    def getUnlocksDescrs(self):
        for unlockIdx, data in enumerate(self.descriptor.type.unlocksDescrs):
            yield (unlockIdx,
             data[0],
             data[1],
             set(data[2:]))

    def getUnlocksDescr(self, unlockIdx):
        try:
            data = self.descriptor.type.unlocksDescrs[unlockIdx]
        except IndexError:
            data = (0, 0, set())

        return (data[0], data[1], set(data[2:]))

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.descriptor.type.id == other.descriptor.type.id

    def __repr__(self):
        return 'Vehicle<id:%d, intCD:%d, nation:%d, lock:%s>' % (self.invID,
         self.intCD,
         self.nationID,
         self.lock)

    def _getShortInfo(self, vehicle = None, expanded = False):
        description = i18n.makeString('#menu:descriptions/' + self.itemTypeName)
        caliber = self.descriptor.gun['shots'][0]['shell']['caliber']
        armor = findVehicleArmorMinMax(self.descriptor)
        return description % {'weight': BigWorld.wg_getNiceNumberFormat(float(self.descriptor.physics['weight']) / 1000),
         'hullArmor': BigWorld.wg_getIntegralFormat(armor[1]),
         'caliber': BigWorld.wg_getIntegralFormat(caliber)}

    def _sortByType(self, other):
        return VEHICLE_TYPES_ORDER_INDICES[self.type] - VEHICLE_TYPES_ORDER_INDICES[other.type]


def getTypeUserName(vehType, isElite):
    if isElite:
        return i18n.makeString('#menu:header/vehicleType/elite/%s' % vehType)
    else:
        return i18n.makeString('#menu:header/vehicleType/%s' % vehType)


def getTypeShortUserName(vehType):
    return i18n.makeString('#menu:classes/short/%s' % vehType)


def _getLevelIconName(vehLevel, postfix = ''):
    return 'tank_level_%s%d.png' % (postfix, int(vehLevel))


def getLevelBigIconPath(vehLevel):
    return '../maps/icons/levels/%s' % _getLevelIconName(vehLevel, 'big_')


def getLevelSmallIconPath(vehLevel):
    return '../maps/icons/levels/%s' % _getLevelIconName(vehLevel, 'small_')


def getLevelIconPath(vehLevel):
    return '../maps/icons/levels/%s' % _getLevelIconName(vehLevel)


def getIconPath(vehicleName):
    return '../maps/icons/vehicle/%s' % getItemIconName(vehicleName)


def getContourIconPath(vehicleName):
    return '../maps/icons/vehicle/contour/%s' % getItemIconName(vehicleName)


def getSmallIconPath(vehicleName):
    return '../maps/icons/vehicle/small/%s' % getItemIconName(vehicleName)


def getUniqueIconPath(vehicleName, withLightning = False):
    if withLightning:
        return '../maps/icons/vehicle/unique/%s' % getItemIconName(vehicleName)
    else:
        return '../maps/icons/vehicle/unique/normal_%s' % getItemIconName(vehicleName)


def getTypeIconName(vehicleType):
    return '%s.png' % vehicleType


def getTypeSmallIconPath(vehicleType):
    return '../maps/icons/vehicleTypes/%s' % getTypeIconName(vehicleType)


def getUserName(vehicleType, textPrefix = False):
    return _getActualName(vehicleType.userString, vehicleType.tags, textPrefix)


def getShortUserName(vehicleType, textPrefix = False):
    return _getActualName(vehicleType.shortUserString, vehicleType.tags, textPrefix)


def _getActualName(name, tags, textPrefix = False):
    if _checkForTags(tags, VEHICLE_TAGS.PREMIUM_IGR):
        if textPrefix:
            return i18n.makeString(ITEM_TYPES.MARKER_IGR, vehName=name)
        return makeHtmlString('html_templates:igr/premium-vehicle', 'name', {'vehicle': name})
    return name


def _checkForTags(vTags, tags):
    if not hasattr(tags, '__iter__'):
        tags = (tags,)
    return bool(vTags & frozenset(tags))


def findVehicleArmorMinMax(vd):

    def findComponentArmorMinMax(armor, minMax):
        for value in armor:
            if value != 0:
                if minMax is None:
                    minMax = [value, value]
                else:
                    minMax[0] = min(minMax[0], value)
                    minMax[1] = max(minMax[1], value)

        return minMax

    minMax = None
    minMax = findComponentArmorMinMax(vd.hull['primaryArmor'], minMax)
    for turrets in vd.type.turrets:
        for turret in turrets:
            minMax = findComponentArmorMinMax(turret['primaryArmor'], minMax)

    return minMax