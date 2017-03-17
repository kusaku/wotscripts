# Embedded file name: scripts/common/db/DBPostInit.py
from consts import IS_CLIENT, IS_EDITOR, IS_CELLAPP
from config_consts import IS_DEVELOPMENT
from debug_utils import DBLOG_ERROR, DBLOG_NOTE
import DBPatch
import math

class _Dummy:
    pass


def postInitAircrafts(priority = 0):
    """postinit decorator for database transform funcs.
    priority - integer arg to queue func. Funcs will be run from lowset to highest priority.
    Example of usage:
    
        @postInitAircraft(10)
        def f(db):
            db.aircraft[0] = None
        
        f(db()) # db is dbManager implementation from DBLogic
    """

    def decorated(fn):

        def wrapped(db):
            """Get db from dbManager if db is None and add it to args"""
            return fn(db)

        wrapped.__name__ = fn.__name__
        wrapped.decorator = postInitAircrafts
        wrapped.priority = priority
        return wrapped

    return decorated


def postInitWeapons(priority = 0):
    """postinit decorator for database transform funcs.
    priority - integer arg to queue func. Funcs will be run from lowset to highest priority.
    Example of usage:
    
        @postInitWeapons(10)
        def f(db):
            db.aircraft[0] = None
    
        f(db()) # db is dbManager implementation from DBLogic
    """

    def decorated(fn):

        def wrapped(db):
            """Get db from dbManager if db is None and add it to args"""
            return fn(db)

        wrapped.__name__ = fn.__name__
        wrapped.decorator = postInitWeapons
        wrapped.priority = priority
        return wrapped

    return decorated


def postInitGunProfiles(priority = 0):
    """postinit decorator for database transform funcs.
    priority - integer arg to queue func. Funcs will be run from lowset to highest priority.
    Example of usage:
    
        @postInitWeapons(10)
        def f(db):
            db.aircraft[0] = None
    
        f(db()) # db is dbManager implementation from DBLogic
    """

    def decorated(fn):

        def wrapped(weaponsDB, gunsProfilesDB):
            """Get db from dbManager if db is None and add it to args"""
            return fn(weaponsDB, gunsProfilesDB)

        wrapped.__name__ = fn.__name__
        wrapped.decorator = postInitGunProfiles
        wrapped.priority = priority
        return wrapped

    return decorated


def __getPostInitFuncs(fType):
    result = map(lambda x: (x.priority, x), filter(lambda f: getattr(f, 'decorator', None) is fType, globals().values()))
    result.sort()
    return map(lambda x: x[1], result)


def posInitDB(aircraftsDB, weaponsDB, gunsProfilesDB):
    """Gets all registered to globals() postinit funcs and run them by priority from lowest to
    highest.
    """
    for postInitFunc in __getPostInitFuncs(postInitAircrafts):
        postInitFunc(aircraftsDB)

    posInitWeapons(weaponsDB, gunsProfilesDB)


def posInitWeapons(weaponsDB, gunsProfilesDB):
    for postInitFunc in __getPostInitFuncs(postInitGunProfiles):
        postInitFunc(weaponsDB, gunsProfilesDB)

    for postInitFunc in __getPostInitFuncs(postInitWeapons):
        postInitFunc(weaponsDB)


def patchItem(item, baseItem):
    """Patch item with baseItem
    """
    patchedUpgrade = _Dummy()
    DBPatch.patch(patchedUpgrade, item)
    DBPatch.patch(patchedUpgrade, baseItem)
    return patchedUpgrade


@postInitAircrafts(1)
def aircraftPostInit(db):
    """Post postinit for aicrafts
    """
    for aircraft in db.aircraft:
        for i, weaponSlot in enumerate(aircraft.flightModel.weaponSlot):
            baseConfiguration = weaponSlot.configuration[0]
            aircraft.flightModel.weaponSlot[i] = [baseConfiguration] + map(lambda x: patchItem(x, baseConfiguration), weaponSlot.configuration[1:])

        if aircraft.options.isDev and not IS_DEVELOPMENT:
            continue
        baseHull = aircraft.flightModel.hull[0]
        aircraft.flightModel.hull = [baseHull] + map(lambda x: patchItem(x, baseHull), aircraft.flightModel.hull[1:])
        baseEngine = aircraft.flightModel.engine[0]
        aircraft.flightModel.engine = [baseEngine] + map(lambda x: patchItem(x, baseEngine), aircraft.flightModel.engine[1:])
        aircraft.price = (getattr(aircraft, 'price', 0), getattr(aircraft, 'gold', 0))
        try:
            del aircraft.gold
        except AttributeError:
            pass


@postInitGunProfiles()
def gunProfilesPostInit(weaponsDB, gunsProfilesDB):
    """Post postinit for guns"""
    for index, gun in enumerate(weaponsDB.gun):
        for gunProfile in gunsProfilesDB.gunProfile:
            if gunProfile.name == gun.gunProfileName:
                weaponsDB.gun[index] = patchItem(gun, gunProfile)
                DBLOG_NOTE("Gun '%s' successfully updated with gun profile '%s'" % (gun.name, gunProfile.name))
                break
        else:
            DBLOG_ERROR("No gun profile '%s' found for gun '%s', please fix aircrafts.xml." % (gun.gunProfileName, gun.name))


@postInitWeapons(3)
def ammoPostInit(db):
    pass