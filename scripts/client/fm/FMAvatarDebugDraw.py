# Embedded file name: scripts/client/fm/FMAvatarDebugDraw.py
import BigWorld
import Math
import db

class FMAvatarDebugDraw(object):

    def __init__(self, player):
        self.__group = 'FMAvatarDebugDraw_%d' % id(self)
        self.__bBoxes = []
        data = db.DBLogic.g_instance.getDestructibleObjectData(player)
        partStates = dict(player.partStates)
        partsList = data.partsSettings.getPartsList()
        for partTuple in partsList:
            upgrade = None
            partID = partTuple[0]
            partDB = partTuple[1]
            for it in player.partTypes:
                if it['key'] == partID:
                    upgrade = partDB.getPartType(it['value'])
                    break

            if not upgrade:
                upgrade = partDB.getFirstPartType()
            if upgrade:
                bBoxes = upgrade.bboxes
                partState = partStates.get(partID, 1)
                for i in range(partState, 0, -1):
                    stateObj = upgrade.states.get(i, None)
                    if stateObj and stateObj.bboxes:
                        bBoxes = stateObj.bboxes
                        break

                for bbox in bBoxes.getList():
                    self.__bBoxes.append(bbox)

        return

    def __drawBBox(self, position, rotation, size, color):
        v1 = position + rotation.rotateVec(Math.Vector3(-size.x, -size.y, -size.z))
        v2 = position + rotation.rotateVec(Math.Vector3(size.x, -size.y, -size.z))
        v3 = position + rotation.rotateVec(Math.Vector3(size.x, -size.y, size.z))
        v4 = position + rotation.rotateVec(Math.Vector3(-size.x, -size.y, size.z))
        w1 = position + rotation.rotateVec(Math.Vector3(-size.x, size.y, -size.z))
        w2 = position + rotation.rotateVec(Math.Vector3(size.x, size.y, -size.z))
        w3 = position + rotation.rotateVec(Math.Vector3(size.x, size.y, size.z))
        w4 = position + rotation.rotateVec(Math.Vector3(-size.x, size.y, size.z))
        BigWorld.addDrawLine(self.__group, v1, v2, color)
        BigWorld.addDrawLine(self.__group, v2, v3, color)
        BigWorld.addDrawLine(self.__group, v3, v4, color)
        BigWorld.addDrawLine(self.__group, v4, v1, color)
        BigWorld.addDrawLine(self.__group, w1, w2, color)
        BigWorld.addDrawLine(self.__group, w2, w3, color)
        BigWorld.addDrawLine(self.__group, w3, w4, color)
        BigWorld.addDrawLine(self.__group, w4, w1, color)
        BigWorld.addDrawLine(self.__group, v1, w1, color)
        BigWorld.addDrawLine(self.__group, v2, w2, color)
        BigWorld.addDrawLine(self.__group, v3, w3, color)
        BigWorld.addDrawLine(self.__group, v4, w4, color)

    def __drawBBoxes(self, position, rotation, colors):
        for i, bbox in enumerate(self.__bBoxes):
            self.__drawBBox(position + rotation.rotateVec(bbox.pos), rotation.mul(bbox.rotation), bbox.size, colors[i % len(colors)])

    def draw(self, position, rotation):
        BigWorld.clearGroup(self.__group)
        self.__drawBBoxes(position, rotation, (16744192, 16711680, 65280, 255, 8388352, 65407, 32512))

    def clear(self):
        BigWorld.clearGroup(self.__group)

    def destroy(self):
        BigWorld.clearGroup(self.__group)
        self.__bBoxes = None
        return