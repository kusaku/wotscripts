# Embedded file name: scripts/client/Helpers/ClientCmd.py
import wgPickle
import AccountCommands
from debug_utils import LOG_DEBUG, CRITICAL_ERROR
import BigWorld

def static_var(varname, value):

    def decorate(func):
        setattr(func, varname, value)
        return func

    return decorate


@static_var('requestID', 0)
def getRequestID():
    getRequestID.requestID += 1
    if getRequestID.requestID >= AccountCommands.REQUEST_ID_UNRESERVED_MAX:
        getRequestID.requestID = AccountCommands.REQUEST_ID_UNRESERVED_MIN
    return getRequestID.requestID


class ClientCmd:

    def __init__(self, server, client):
        self.server = server
        self.client = client
        self.__onCmdResponse = {}

    def destroy(self):
        """
        Destroy/release
        """
        self.server = None
        self.client = None
        self.__onCmdResponse.clear()
        return

    def createCmdOperation(self, commandID, callback, targetID, *args):
        """
        Method which create command and send it to the server.
        @param commandID: command id which run on the server part
        @param callback: method(delegate) which is called on respond from the server
                callbackType = onCallback(requestID, resultID, *args) or onCallback(requestID, resultID, arg1, arg2...)
        @param targetID:
        @param args: command parameters (unpickled)
        """
        requestID = getRequestID()
        if callback is None:
            callback = self.__onCmdCallback
        if targetID == -1:
            targetID = self.client.id
        self.__onCmdResponse[requestID] = callback
        arg = wgPickle.dumps(wgPickle.FromClientToServer, args)
        self.server.doCommand(requestID, commandID, targetID, arg)
        return

    def _onCmdResponsePacked(self, requestID, resultID, responseDataStr):
        """
        DO NOT USE THIS! USE onCmdResponse INSTEAD
        
        Method called in response to the doCommand call and return callback call if exists
            requestID - id passed in doCmd method.
            resultID - command result.
            responseDataStr - pickled response data.
        """
        callback = self.__onCmdResponse.pop(requestID, None)
        if callback is None:
            return
        else:
            args = wgPickle.loads(wgPickle.FromServerToClient, responseDataStr)
            callback(requestID, resultID, args)
            return

    def onCmdResponse(self, requestID, resultID, responseDataStr):
        """
        Method called in response to the doCommand call and return callback call if exists
        This function unpacks the args of the response into callback
        @param requestID: id passed in doCmd method.
        @param resultID: command result.
        @param responseDataStr:  pickled response data.
        """
        callback = self.__onCmdResponse.pop(requestID, None)
        if callback is None:
            return
        else:
            args = wgPickle.loads(wgPickle.FromServerToClient, responseDataStr)
            callback(requestID, resultID, *args)
            return

    def __onCmdCallback(self, requestID, resultID, *args):
        """
        Default response callback
            requestID - id passed in doCmd method.
            resultID - command result.
            data - extended information.
        """
        LOG_DEBUG('Default respond callback: ', 'requestID ', requestID, ' resultID ', resultID, ' data ', args)