# Embedded file name: scripts/common/AvatarControllerBase.py


class AvatarControllerBase(object):

    def __init__(self, owner):
        """
        :type owner: Avatar
        """
        self._owner = owner

    def onControllersCreated(self):
        pass

    def destroy(self):
        self._owner = None
        return

    def backup(self):
        return None

    def restore(self, container):
        pass

    def bin(self):
        return ''

    def onParentSetState(self, stateID, data):
        pass

    def update(self, dt):
        pass

    def update1sec(self, ms):
        pass

    def restart(self):
        pass

    def setOwner(self, owner):
        self._owner = owner

    def getOwner(self):
        return self._owner