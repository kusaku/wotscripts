# Embedded file name: scripts/common/Interfaces.py


class ISYNC_PLANE_LIST:
    ELITE_PLANES_LIST = 0


class ISYNC_INVENTORY:
    DEPOT_UPGRADES_DICT = 0
    DEPOT_EQUIPMENT_DICT = 1
    DEPOT_CONSUMABLES_DICT = 2
    OPENED_AIRCRAFTS_LIST = 3
    BOUGHT_AIRCRAFTS_LIST = 4
    CUSTOM_PRESETS = 5
    BATTLE_AIRCRAFTS_LIST = 6
    UNLOCK_AIRCRAFTS = 7


class ISYNC_AIRCRAFT:
    AIRCRAFT_ID = 0
    SLOT_INDEX = 1
    PDATA_AIRCRAFT_DICT = 2
    CAMOUFLAGES_DICT = 3
    EXPERIENCE = 4
    DAILY_FIRST_WIN_XP_FACTOR = 5
    DAILY_FIRST_WIN_REMAINS = 6


class ISYNC_STATS:
    CREDITS = 0
    GOLD = 1
    SLOTS_COUNT = 2
    SELECTED_AIRCRAFT = 3
    EXPERIENCE = 4
    CREATED_AT = 5


from debug_utils import LOG_CURRENT_EXCEPTION

def create_ob(iface, *data):
    try:
        return dict([ (getattr(iface, attrname), data[getattr(iface, attrname)]) for attrname in dir(iface) if not attrname.startswith('__') and not callable(getattr(iface, attrname)) ])
    except IndexError:
        LOG_CURRENT_EXCEPTION()
        raise NotObCreated('invalid data %s for %s interface' % (str(data), str(iface.__name__)))


class NotObCreated(Exception):

    def __init__(self, value):
        self.parameter = 'NotObCreatedError: %s' % str(value)