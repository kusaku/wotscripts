# Embedded file name: scripts/client/modelManipulator/HierarchyWorker.py
import weakref

class HardpointNotFound(Exception):
    pass


class FreeHierarchyNode:
    """Simple node without parent"""

    def __init__(self, name, nodeId):
        self.id = nodeId
        self.name = name
        self._childs = dict()
        self.hardpoints = dict()

    @property
    def path(self):
        return ''

    @property
    def childs(self):
        return self._childs

    @property
    def parent(self):
        return None

    @property
    def localMatrix(self):
        return None


class LeafHierarchyNode(FreeHierarchyNode):
    """Leaf node with parent"""

    def __init__(self, name, parent, nodeId):
        FreeHierarchyNode.__init__(self, name, nodeId)
        self.__parent = weakref.ref(parent)
        parent._childs[name] = self

    @property
    def localMatrix(self):
        if self.name not in self.parent.hardpoints:
            raise HardpointNotFound("Can't find hardpoint {0}".format(self.path))
        return self.parent.hardpoints[self.name]

    def parents(self):
        node = self
        while node != None:
            yield node
            node = node.parent

        return

    @property
    def path(self):
        return '/'.join(reversed(tuple((node.name for node in self.parents()))))

    @property
    def matrix(self):
        node = self.parent
        res = self.localMatrix
        while node is not None:
            parentMatrix = node.localMatrix
            if parentMatrix:
                res.preMultiply(parentMatrix)
            else:
                return
            node = node.parent

        return res

    @property
    def parent(self):
        return self.__parent()


class MainHierarchyNode(FreeHierarchyNode):
    """Main node of compound object"""

    def __init__(self):
        FreeHierarchyNode.__init__(self, 'root', 0)
        self.linearHierarchy = [(-1, self)]

    def __createNode(self, name, parent, freeNode):
        if freeNode:
            node = FreeHierarchyNode(name, len(self.linearHierarchy))
            parentId = -1
        else:
            node = LeafHierarchyNode(name, parent, len(self.linearHierarchy))
            parentId = parent.id
        self.linearHierarchy.append((parentId, node))
        return node

    def resolvePath(self, pathList, freeNode = False):
        currentNode = self
        while pathList and pathList[0] != '':
            nodeName = pathList[0]
            if nodeName not in currentNode._childs:
                currentNode = self.__createNode(nodeName, currentNode, freeNode)
            else:
                currentNode = currentNode._childs[nodeName]
            pathList = pathList[1:]

        return currentNode

    def clear(self):
        self.linearHierarchy = None
        return