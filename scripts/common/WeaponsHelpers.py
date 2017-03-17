# Embedded file name: scripts/common/WeaponsHelpers.py
from itertools import groupby

def normalizeVictimsPartsMap(victimsMap):
    for victimId, victimPars in victimsMap.iteritems():
        normalizedParts = []
        for key, rows in groupby(victimPars, lambda x: x[0]):
            allDistances = [ dist for _, dist in rows ]
            normalizedParts.append((key, sum(allDistances) / float(len(allDistances))))

        victimsMap[victimId] = normalizedParts


def isGunGroupShooting(fireFlags, groupIndex):
    return fireFlags & 1 << groupIndex