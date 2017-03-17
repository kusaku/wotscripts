# Embedded file name: scripts/common/packsCommon.py
from collections import defaultdict
from _packs_db import Packs
from _crewnations_data import CrewUniqueDB

def itemGenerator(items):
    """ Generate items from pack
    """
    for item in items:
        if item['type'] in {'gift', 'add'}:
            yield item
            for i in itemGenerator(item.get('related', [])):
                yield i


def giftGenerator(items):
    """ Generate items from pack
    """
    for item in itemGenerator(items):
        gift = item['idTypeList'][0]
        yield {'id': gift[0],
         'type': gift[1],
         'count': item['count']}


packLists = defaultdict(set)
plane2Packs = defaultdict(list)

def buildLists():
    """ Build structure:
        {'all': <all packs>,
         'pilot': <packs with pilotes>,
         'plane': <packs with planes and pilotes>,
         <pilotID>: <packs with this pilot>,
         ...
         }
    """
    pilotToPack = dict()
    for packID, pack in Packs.packs.iteritems():
        pilotID = planeID = None
        for item in itemGenerator(pack['items']):
            gift = item['idTypeList'][0]
            if gift[1] == 'crewmember' and gift[0] in CrewUniqueDB:
                pilotID = gift[0]
            if gift[1] == 'plane':
                planeID = gift[0]

        if pilotID:
            packLists['all'].add(packID)
            if planeID:
                packLists['plane'].add(packID)
                plane2Packs[planeID].append(packID)
            else:
                packLists['pilot'].add(packID)
            if pilotID in pilotToPack:
                packID2 = pilotToPack[pilotID]
                packLists[packID2] = packID
                packLists[packID] = packID2
                del pilotToPack[pilotID]
            else:
                pilotToPack[pilotID] = packID

    raise not pilotToPack or AssertionError
    return


buildLists()