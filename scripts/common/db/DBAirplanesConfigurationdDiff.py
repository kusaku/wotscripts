# Embedded file name: scripts/common/db/DBAirplanesConfigurationdDiff.py
import sys, os, json
sys.path.append(os.path.abspath('./../../server_common'))
sys.path.append(os.path.abspath('./../../common'))
sys.path.append(os.path.abspath('./../../surrogates'))
map(sys.path.append, sys.argv[1:])
import consts
from DBLogic import initDB
try:
    from airplanesConfigurationsOld import airplanesConfigurations as old
    from airplanesConfigurationsNew import airplanesConfigurations as new
except ImportError:
    new = {}
    old = {}

old_out = sys.stdout

class CustomOut(object):

    def write(self, s, *args, **kw):
        pass


sys.stdout = CustomOut()
aircraftdb = initDB()
sys.stdout = old_out
addGID = {}
delGID = {}

def compare(new = new, old = old):
    addGID = {}
    delGID = {}
    for globalID in set(new) - set(old):
        AC = new[globalID]
        try:
            name = aircraftdb.getAircraftData(AC.planeID).airplane.name
        except:
            name = AC.planeID

        addGID.setdefault(name, {})[globalID] = str((AC.modules, AC.weaponSlots))

    for globalID in set(old) - set(new):
        AC = old[globalID]
        try:
            name = aircraftdb.getAircraftData(AC.planeID).airplane.name
        except:
            name = AC.planeID

        delGID.setdefault(name, {})[globalID] = str((AC.modules, AC.weaponSlots))

    return (addGID, delGID)


if __name__ == '__main__':
    print json.dumps(compare())