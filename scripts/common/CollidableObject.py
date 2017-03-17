# Embedded file name: scripts/common/CollidableObject.py
import db
from consts import IS_CELLAPP, COLLISION_RECORDER
from bwdebug import DEBUG_MSG
from db.DBParts import buildPresentPartsMap

def collisionMethod(func):
    if IS_CELLAPP:
        func.isGhost = True
    return func


class CollidableObject(object):
    STATIC_COLLISION = 1
    DYNAMIC_COLLISION = 2
    DEFAULT_PARTS_TYPES = []

    def __init__(self):
        self.presentPartsMap = None
        return

    def initPartsMap(self, partsSettings):
        self.presentPartsMap = buildPresentPartsMap(partsSettings, self.partTypes)

    @property
    def partTypes(self):
        return CollidableObject.DEFAULT_PARTS_TYPES

    @collisionMethod
    def initCollision(self, restore):
        collisionBBoxes = []
        partsData = []
        partStatesMap = dict(self.partStates)
        presentPartsMap = buildPresentPartsMap(db.DBLogic.g_instance.getDestructibleObjectData(self).partsSettings, self.partTypes)
        for partID, upgrade in presentPartsMap.iteritems():
            bBoxes = upgrade.bboxes
            partState = partStatesMap[partID]
            partsData.append({'partId': partID,
             'upgradeId': upgrade.id,
             'stateId': partState})
            for i in range(partState, 0, -1):
                stateObj = upgrade.states.get(i, None)
                if stateObj and stateObj.bboxes:
                    bBoxes = stateObj.bboxes
                    break

            for bbox in bBoxes.getList():
                collisionBBoxes.append({'partId': partID,
                 'bbox': bbox,
                 'aimable': self.isPartStateAimable(presentPartsMap, partID, partState)})

        if self.useCollisionModel():
            data = db.DBLogic.g_instance.getDestructibleObjectData(self)
            self.collisionModel(partsData, data)
            if COLLISION_RECORDER:
                msgs = ['typeName = "{0}"'.format(data.typeName)]
                for partData in partsData:
                    msgs.append('partId = {0}, upgradeId = {1}, stateId = {2}'.format(partData['partId'], partData['upgradeId'], partData['stateId']))

                self.markPosition(0, self.position, '\n'.join(msgs))
                DEBUG_MSG('[{0}]'.format(']['.join(msgs)))
        self.collisionBBoxes(collisionBBoxes)
        self.staticCollision(self.useStaticCollision())
        self.autoAimMode(self.useAutoAimMode())
        if not restore:
            self.deflectionMode(self.useDeflectionMode())
        return

    @collisionMethod
    def useCollisionModel(self):
        return True

    @collisionMethod
    def useStaticCollision(self):
        return False

    @collisionMethod
    def useAutoAimMode(self):
        return 0

    @collisionMethod
    def useDeflectionMode(self):
        return 0

    def onCollide(self, collidedContacts):
        pass

    def onAfterCollide(self):
        pass