# Embedded file name: scripts/common/messenger_common.py
try:
    from constants import IS_DEVELOPMENT
except:
    from config_consts import IS_DEVELOPMENT

def makeArgs(**args):
    res = {'int32Arg1': 0,
     'int64Arg1': 0,
     'strArg1': ''}
    for k, v in args.iteritems():
        raise k in res or AssertionError
        res[k] = v

    return res


class MESSENGER_ACTION_IDS:
    RESPONSE_FAILURE = 0
    RESPONSE_SUCCESS = 1
    START_CLIENT_MESSENGER = 2
    GET_NICKNAME_BY_ID = 3
    RECEIVE_NICKNAME_BY_ID = 4
    GET_USERLIST_BY_NAME = 5
    GET_INIT_PARAMS = 6
    SYNC_CLAN_CHAT_CHANNEL = 7
    BC_FIRST_ACTION_ID = 100
    BC_PING = 101
    BC_DESTROY_CHANNEL = 102
    BC_SET_AUTOCLOSE = 103
    BC_LEAVE_CHANNEL = 104
    XMPP_FIRST_ACTION_ID = 200
    XMPP_GET_PASSWORD = 201
    EXT_FIRST_ACTION_ID = 300


MESSENGER_ACTION_NAMES_BY_IDS = dict([ (id, name) for name, id in MESSENGER_ACTION_IDS.__dict__.iteritems() ])

class MESSENGER_ACTION_ERRORS:
    NO_ERROR = 0
    GENERIC_ERROR = 1
    DUPLICATED_REQUEST = 2
    TIMEOUT = 3
    LIMIT_EXCEEDED = 4
    TARGET_BUSY = 5
    FORBIDDEN_ERROR = 6


class MESSENGER_TIMEOUTS:
    XMPP_GET_PASSWORD = 10.0
    GET_USERLIST_BY_NAME = 10.0
    SYNC_CLAN_CHAT_CHANNEL = 10.0


class MESSENGER_LIMITS:
    USERLIST_BY_NAME_TEMPLATE_LEN = (2, 20)
    USERLIST_BY_NAME_MAX_RESULT_SIZE = 50
    BATTLE_CHANNEL_MESSAGE_MAX_SIZE = 140
    COMPANY_CHANNEL_MESSAGE_MAX_SIZE = 512


try:
    from debug_utils import LOG_ERROR, LOG_WARNING, LOG_NOTE, LOG_CURRENT_EXCEPTION, LOG_WRONG_CLIENT
except:
    import sys

    def LOG_ERROR(msg, *kargs):
        _doLog('ERROR', msg, kargs)


    def LOG_WARNING(msg, *kargs):
        _doLog('WARNING', msg, kargs)


    def LOG_NOTE(msg, *kargs):
        _doLog('NOTE', msg, kargs)


    def LOG_CURRENT_EXCEPTION():
        print _makeMsgHeader('EXCEPTION', sys._getframe(1))
        from traceback import print_exc
        print_exc()


    def LOG_WRONG_CLIENT(entity, *kargs):
        if hasattr(entity, 'id'):
            entity = entity.id
        print _makeMsgHeader('WRONG_CLIENT', sys._getframe(1)), entity, kargs


    def _doLog(s, msg, args):
        header = _makeMsgHeader(s, sys._getframe(2))
        if args:
            print header, msg, args
        else:
            print header, msg


    def _makeMsgHeader(s, frame):
        return '[%s] (%s, %d):' % (s, frame.f_code.co_filename, frame.f_lineno)