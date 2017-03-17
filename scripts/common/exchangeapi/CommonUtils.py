# Embedded file name: scripts/common/exchangeapi/CommonUtils.py
import time
from consts import IS_CLIENT, EMPTY_IDTYPELIST
from config_consts import IS_DEVELOPMENT
from exchangeapi import ErrorCodes
from debug_utils import LOG_WRONG_CLIENT, LOG_ERROR
import zlib
import json
METHODS = ['view',
 'add',
 'edit',
 'delete']
INDEXTOMETHOD = dict(enumerate(METHODS))
METHODTOINDEX = dict(((v, k) for k, v in INDEXTOMETHOD.iteritems()))
LOG_ENABLED = IS_DEVELOPMENT
IFACES_USAGE_LOG = {}
OBJECTS = {}

class COMMAND_TYPES:
    REQUEST = 0
    RESPONSE = 1
    SUBSCRIBE = 2
    UNSUBSCRIBE = 3


def idFromList(ob):
    if ob is None:
        return ob
    elif len(ob) == 1:
        return ob[0]
    else:
        return tuple(ob)


def listFromId(ob):
    if ob is None:
        return ob
    elif isinstance(ob, tuple):
        return list(ob)
    else:
        return [ob]


def import_string(adapter, force = IS_CLIENT):
    try:
        i = adapter.module.rfind('.')
        module, cls = adapter.module[:i], adapter.module[i + 1:] if i != -1 else ('', adapter.module)
        return getattr(__import__(module, None, None, cls) if module else '__main__', cls)
    except (ImportError, AttributeError, IndexError) as ex:
        if not force:
            from traceback import print_exc
            import StringIO
            f = StringIO.StringIO()
            print_exc(file=f)
            f.pos = 0
            raise ImportError(f.read())
        else:
            LOG_ERROR('Cannot import adapter: {0}. Error: {1}'.format(adapter.module, ex))

    return


class Headers(object):

    def __init__(self):
        self.user_agent = None
        return


class Request(object):

    def __init__(self):
        self.headers = Headers()
        self.args = None
        self.method = None
        return


def requestBuilder(headers, args, method):
    request = Request()
    request.headers.user_agent = headers[0]
    request.args = args
    request.method = INDEXTOMETHOD.get(method)
    if request.method is None:
        return request.method
    else:
        return request


def wrongDataResponse(account, operation):
    LOG_WRONG_CLIENT(account, 'Wrong data format, operation: {0}'.format(operation.__dict__ if operation is not None else operation))
    invocationId = operation.invocationId if operation is not None else -1
    account.responseSender([[0, '']], '', {}, invocationId, ErrorCodes.WRONG_DATA_FORMAT)
    return


def handler(account, ob, operation = None, isServer = True, initByServer = False, callback = None):
    if LOG_ENABLED:
        IFACES_USAGE_LOG['requestCount'] = IFACES_USAGE_LOG.get('requestCount', 0) + 1
    request = requestBuilder(*ob)
    if request is None:
        return wrongDataResponse(account, operation)
    else:
        requestID = operation.invocationId if isServer and operation else -1

        def processBaseItem(idTypeList, ifacename, data):
            from exchangeapi.AdapterUtils import getAdapter
            from exchangeapi.Connectors import getObject
            idList, typeList = splitIDTypeList(idTypeList)
            adapter = getAdapter(ifacename, typeList)
            ob = getattr(adapter, request.method)(account=account, data=data, requestID=requestID, initByServer=initByServer, idTypeList=idTypeList, ob=OBJECTS.setdefault(idFromList(typeList), {}).setdefault(idFromList(idList), getObject(idTypeList, account))) if adapter else None
            return (ob, adapter)

        processItem = processBaseItem
        if isServer:
            requestID = account.exchangeapiHelper.addRequest(requestID, operation, request.method, initByServer, callback)

            def processServerItem(idTypeList, ifacename, data):
                account.exchangeapiHelper.addRequestItem(requestID, processBaseItem, idTypeList, ifacename, data)

            processItem = processServerItem
        else:
            response = [[int(IS_CLIENT), METHODTOINDEX[request.method]], [], ErrorCodes.SUCCESS]

            def processClientItem(idTypeList, ifacename, data):
                ob, adapter = processBaseItem(idTypeList, ifacename, data)
                data = adapter(account, ob, idTypeList=idTypeList)
                response[1].append([{ifacename: data}, idTypeList])

            processItem = processClientItem

        def convertIDType(obID, obType):
            return [obID, obType if obID is not None or obType != 'account' else None]

        for ifaces, idTypeList in request.args:
            idTypeList = [ convertIDType(obID, obType) for obID, obType in idTypeList ]
            for ifacename, data in ifaces.iteritems():
                processItem(idTypeList, ifacename, data)

        if not isServer:
            return response
        OBJECTS.clear()
        return


def convertObIdForUI(obid):
    if obid is not None:
        return str(obid)
    else:
        return obid


def convertIDTypeListForUI(idTypeList):
    if idTypeList is None:
        return idTypeList
    else:
        return map(lambda x: [convertObIdForUI(x[0]), x[1]], idTypeList)


def convertIfaceDataForUI(data):

    def convert():
        for item in data:
            ifacedata, idTypeList = item + [None] * (2 - len(item))
            convertedIDTypeList = convertIDTypeListForUI(idTypeList)
            if idTypeList is not None and len(idTypeList) < 2:
                if not convertedIDTypeList:
                    obid = None
                    obtype = None
                else:
                    obid = convertedIDTypeList[0][0]
                    obtype = convertedIDTypeList[0][1]
                ret = [dict(((key, ifacedata.__dict__[key].__dict__) for key in ifacedata.__dict__)) if not isinstance(ifacedata, dict) else ifacedata, obid, obtype]
            else:
                ret = [dict(((key, ifacedata.__dict__[key].__dict__) for key in ifacedata.__dict__)) if not isinstance(ifacedata, dict) else ifacedata, convertedIDTypeList]
            yield ret

        return

    return list(convert())


def convertObIdFromUI(obid):
    if isinstance(obid, basestring):
        try:
            obid = int(obid)
        except ValueError:
            pass

    return obid


def convertIDTypeListFromUI(idTypeList):
    if idTypeList is None:
        return
    else:
        return map(lambda x: [convertObIdFromUI(x[0]), x[1]], idTypeList)


class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        return obj.__dict__


def convertIfaceDataFromUI(data):

    def convert():
        for item in data:
            if len(item) > 1 and isinstance(item[1], list):
                ifacedata = item[0]
                idTypeList = item[1]
            else:
                ifacedata, obid, obtype = item + [None] * (3 - len(item))
                idTypeList = [[obid, obtype]]
            yield [json.loads(json.dumps(ifacedata, cls=ComplexEncoder)) if not isinstance(ifacedata, dict) else ifacedata, convertIDTypeListFromUI(idTypeList)]

        return

    return list(convert())


def splitIDTypeList(idTypeList):
    if idTypeList is not None:
        return zip(*idTypeList)
    else:
        return (None, None)


def joinIDTypeList(idList, typeList):
    if typeList is None:
        return EMPTY_IDTYPELIST
    else:
        if idList is None:
            idList = [None] * len(typeList)
        return map(lambda x, y: [x, y], idList, typeList)


def iface_name(ifacename):
    return ifacename.split(':')[-1]


def validateRequestsRate(account, requestobserv):
    from exchangeapi.AdapterUtils import getOblocationDBObject, adapter_id
    request = requestBuilder(*requestobserv)
    if request is not None:
        for ifaces, idTypeList in request.args:
            for ifacename in ifaces:
                idList, typeList = splitIDTypeList(idTypeList)
                for rate in getattr(getOblocationDBObject(ifacename, typeList), 'requestsRate', []):
                    if rate.method == request.method:
                        requestID = '%s:%s:%s' % (ifacename, idFromList(typeList), idFromList(idList))
                        if requestID not in account.ifacesRequestsCounter or time.time() - account.ifacesRequestsCounter[requestID][1] > rate.timelapse:
                            account.ifacesRequestsCounter[requestID] = [0, time.time()]
                        if account.ifacesRequestsCounter[requestID][0] >= rate.count:
                            return False
                        account.ifacesRequestsCounter[requestID][0] += 1
                        break

    return True


def generateUUID(idTypeList, ifaceName):
    return '%s_%s' % ('_'.join(map(lambda entry: '{0}_{1}'.format(*((item if item != 'account' else None) for item in entry)), idTypeList if idTypeList else EMPTY_IDTYPELIST)), iface_name(ifaceName))


def generateID(idTypeList, ifaceName):
    return zlib.crc32(generateUUID(idTypeList, ifaceName))