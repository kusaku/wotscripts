# Embedded file name: scripts/client/messenger/proto/migration/MigrationServerSettings.py
from messenger.proto.interfaces import IProtoSettings

class MigrationServerSettings(IProtoSettings):

    def isEnabled(self):
        return True