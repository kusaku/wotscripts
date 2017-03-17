# Embedded file name: scripts/client/VOIP/PrivateConsts.py


class ENGINE_PROTOCOL:
    """ Data dictionary keys and commands for communication with the C++ part of VOIP engine implementation. """
    KEY_NUM_CHANNEL_TYPES = 'num_channel_types'
    KEY_CHANNEL_TYPE_INDEXED = 'channel_type_%d'
    KEY_TS_IDENTITY_INDEXED = 'ts_identity_%d'
    KEY_CHANNEL_TYPE = 'channel_type'
    KEY_PROVISIONING_KEY = 'provisioning_key'
    KEY_SECURITY_HASH = 'security_hash'
    KEY_TS_CHANNEL_ID = 'ts_channel_id'
    KEY_OLD_TS_CHANNEL_ID = 'old_ts_channel_id'
    KEY_COUNT = 'count'
    KEY_CAPTURE_DEVICE_INDEXED = 'capture_device_%d'
    KEY_CURRENT_CAPTURE_DEVICE = 'current_capture_device'
    KEY_PLAYER_DATABASE_ID = 'dbid'
    KEY_VOLUME = 'volume'
    KEY_STATE = 'state'
    KEY_STATUS_CODE = 'status_code'
    KEY_COMMAND = 'command'
    CMD_REQUEST_CAPTURE_DEVICES = 'request_capture_devices'
    CMD_SELECT_CAPTURE_DEVICE = 'select_capture_device'
    CMD_TEST = 'test_voice'
    CMD_SET_ACTIVE_CHANNEL = 'set_active_channel'
    CMD_SET_CLIENT_MUTE = 'set_client_mute'
    CMD_SET_CLIENT_VOLUME = 'set_client_volume'
    CMD_REQUEST_CLIENT_STATUS = 'request_client_status'

    class MESSAGES:
        """ Event message codes (passed from C++ to Python via ChannelsMgr.__call__ method) """
        vmCaptureDevices = 1000
        vmLoggedIn = 1001
        vmLoginFailed = 1002
        vmLoggedOut = 1003
        vmClientMoved = 1004
        vmClientTalkingStatus = 1005
        vmTick = 1006

        @staticmethod
        def getConstNameByValue(const):
            for k, v in ENGINE_PROTOCOL.MESSAGES.__dict__.items():
                if v == const:
                    return k


class CHANNEL_STATES:
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTING = 3

    @staticmethod
    def getConstNameByValue(const):
        for k, v in CHANNEL_STATES.__dict__.items():
            if v == const:
                return k


class MEMBER_STATES:
    UNKNOWN = 0
    DISCONNECTED = 1
    CONNECTED = 2
    TALKING = 3

    @staticmethod
    def getConstNameByValue(const):
        for k, v in MEMBER_STATES.__dict__.items():
            if v == const:
                return k