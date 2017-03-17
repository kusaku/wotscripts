# Embedded file name: scripts/client/gui/Scaleform/CallbacksHandler.py
import json
from debug_utils import *
SKIP_OUTPUT_KEYS = ['requestOwnerInfo', 'SpaceMove']

def _bytify(data, ignore_dicts = False):
    if isinstance(data, list):
        return [ _bytify(item, ignore_dicts=True) for item in data ]
    if isinstance(data, dict) and not ignore_dicts:
        return {_bytify(key, ignore_dicts=True):_bytify(value, ignore_dicts=True) for key, value in data.iteritems()}
    return data


def ConvertJsonToPyobject(args_json):
    temp = _bytify(json.loads(args_json), ignore_dicts=True)
    args = list()

    def process_list(somelist):
        for i, v in enumerate(somelist):
            if isinstance(v, dict):
                somelist[i] = process_dict(v)
                continue
                somelist[i] = isinstance(v, list) and process_list(v)

        return somelist

    def process_dict(somedict):
        classname = somedict.pop('classtag', None)
        for k, v in somedict.iteritems():
            if isinstance(v, dict):
                somedict.pop(k, None)
                somedict[k] = process_dict(v)
            elif isinstance(v, list):
                somedict.pop(k, None)
                somedict[k] = process_list(v)

        object = somedict
        if classname is not None:
            object = BigWorld.createObjectByClassName(classname)
            object.__dict__.update(**somedict)
        return object

    for arg in temp:
        if isinstance(arg, dict):
            args.append(process_dict(arg))
        elif isinstance(arg, list):
            args.append(process_list(arg))
        else:
            args.append(arg)

    return tuple(args)


def ConvertPyobjectToJson(object):

    def default_handler(o):
        r = {}
        if hasattr(o, '__dict__'):
            r = o.__dict__
        return r

    return json.dumps(object, default=default_handler)


class CallbacksHandler(object):

    def __init__(self):
        self.__fsCallbacks = {}
        self.__externalCallbacks = {}

    def addFsCallback(self, command, function):
        self.__fsCallbacks.setdefault(command, set())
        self.__fsCallbacks[command].add(function)

    def removeFsCallback(self, command):
        if self.__fsCallbacks.has_key(command):
            self.__fsCallbacks.pop(command)

    def addFsCallbacks(self, commands):
        for command, function in commands.items():
            self.addFsCallback(command, function)

    def removeFsCallbacks(self, *args):
        for command in args:
            self.removeFsCallback(command)

    def addExternalCallback(self, command, function):
        self.__externalCallbacks.setdefault(command, set())
        self.__externalCallbacks[command].add(function)

    def removeExternalCallback(self, command, function = None):
        if self.__externalCallbacks.has_key(command):
            if function is None:
                self.__externalCallbacks.pop(command)
            elif function in self.__externalCallbacks[command]:
                self.__externalCallbacks[command].remove(function)
        return

    def addExternalCallbacks(self, commands):
        for command, function in commands.items():
            self.addExternalCallback(command, function)

    def removeExternalCallbacks(self, *args):
        for command in args:
            self.removeExternalCallback(command)

    def removeAllCallbacks(self):
        self.__fsCallbacks.clear()
        self.__externalCallbacks.clear()

    def handleFsCommandCallback(self, command, arg):
        if self.__fsCallbacks.has_key(command):
            for fsCallback in self.__fsCallbacks[command]:
                fsCallback(arg)

            return True
        LOG_DEBUG('FsCommandCallback "%s" not found' % command, arg)
        return False

    def handleExternalInterfaceCallback(self, command, args_json):
        args = ConvertJsonToPyobject(args_json)
        if self.__externalCallbacks.has_key(command):
            logOutputAccepted = True
            for key in SKIP_OUTPUT_KEYS:
                logOutputAccepted = logOutputAccepted and command.find(key) == -1

            if logOutputAccepted:
                LOG_TRACE('ExternalInterfaceCallback "%s" ' % command)
            for externalCallback in self.__externalCallbacks[command]:
                retobj = externalCallback(*args)
                return ConvertPyobjectToJson(retobj)

        LOG_ERROR('ExternalInterfaceCallback "%s" not found' % command)
        return None