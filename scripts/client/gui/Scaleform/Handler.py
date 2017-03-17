# Embedded file name: scripts/client/gui/Scaleform/Handler.py
import json
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION
from gui.Scaleform.CallbacksHandler import CallbacksHandler
from config_consts import IS_DEVELOPMENT

class Handler(CallbacksHandler):

    def __init__(self):
        CallbacksHandler.__init__(self)

    def afterCreate(self):
        pass

    def beforeDelete(self):
        self.removeAllCallbacks()

    def setMovieVariable(self, path, value):
        if not isinstance(value, list):
            value = [value]
        try:
            self.movie.invoke('_root._level0.' + path, json.dumps(value, default=lambda o: o.__dict__), None)
        except:
            LOG_ERROR('Error to set movie variable "' + '_root._level0.' + path + '"')

        return

    def call(self, methodName, args = None):
        """
        Game-initiated Communication. Invoke the installed callback in Flash.
        Who in Flash is installed with the GameDelegate that listens for calls from the backend:
            GameDelegate.addCallback("methodName", this, "callbackMethodName");
        
        @param methodName: method name witch installed in Flash
        @param args: argument list
        """
        if args is None:
            args = []
        args.insert(0, methodName)
        self.movie.invoke('call', json.dumps(args, default=lambda o: o.__dict__), None)
        return

    def call_1(self, methodName, *methodArgs):
        jsonArgs = json.dumps(list(methodArgs), default=lambda o: o.__dict__)
        try:
            self.movie.invoke(methodName, jsonArgs, None)
        except:
            LOG_ERROR('call_1: cannot invoke method ', methodName)
            if IS_DEVELOPMENT:
                LOG_CURRENT_EXCEPTION()
                import traceback
                traceback.print_stack()

        return

    def respond(self, args = None):
        """
        Flash-initiated Communication. Return a result by unique ID in callbackMethodName method in Flash.
        When in Flash with the GameDelegate call method:
            GameDelegate.call("methodName", argumentList, this, "callbackMethodName");
        
        @param args: argument list
        """
        if args is None:
            args = []
        self.movie.invoke('respond', json.dumps(args), None)
        return