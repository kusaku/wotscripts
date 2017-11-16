# Embedded file name: scripts/client/messenger/proto/bw/BWServerSettings.py
from messenger.proto.interfaces import IProtoSettings

class BWServerSettings(IProtoSettings):

    def isEnabled(self):
        return True