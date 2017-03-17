# Embedded file name: scripts/client/Helpers/ExchangeObBuilder.py
from Helpers.cache import setToCache, getFromCache, deleteFromCache, getPlayer
from exchangeapi.AdapterUtils import getAdapter, getOblocation
from exchangeapi.CommonUtils import handler, INDEXTOMETHOD, splitIDTypeList, idFromList, listFromId, joinIDTypeList, COMMAND_TYPES, METHODTOINDEX, iface_name
import debug_utils
import BigWorld
from consts import OB_LOCATION, IS_CLIENT
from exchangeapi import ErrorCodes
from exchangeapi.IfaceUtils import getIface
from functools import partial
from debug_utils import LOG_ERROR
from exchangeapi.ErrorCodes import SUCCESS
_CHUNK_SIZE = 100

def responseEventGenerate(headers, respdata):
    from exchangeapi.EventUtils import generateEvent
    eventName = INDEXTOMETHOD[headers[1]]
    for data, idTypeList in respdata:
        for ifaceName, ob in data.iteritems():
            prevob = getFromCache(idTypeList, ifaceName)
            generateEvent(INDEXTOMETHOD[headers[1]], eventName, ifaceName, idTypeList, None, ob, prevob)

    return


def processIFaceData(headers, respdata):
    for data, idTypeList in respdata:
        typeList = splitIDTypeList(idTypeList)[1]
        for ifacename in data:
            if data[ifacename] and not headers[0] == int(IS_CLIENT) and getOblocation(ifacename, typeList) == OB_LOCATION.MIXED:
                data[ifacename] = getAdapter(ifacename, typeList, silent=True)(getPlayer(), data[ifacename], idTypeList=idTypeList)

    ob = [headers, respdata, ErrorCodes.SUCCESS]
    debug_utils.IfaceDebugOutput(COMMAND_TYPES.RESPONSE, ob=ob)


def cacheIFaceData(respdata):
    for data, idTypeList in respdata:
        for ifacename in data:
            if data[ifacename]:
                setToCache(idTypeList, ifacename, data[ifacename])
            else:
                deleteFromCache(idTypeList, ifacename)


class ExchangeObBuilder(object):

    def __init__(self, requestob, generateEvent = True):
        self.__requestob = requestob
        self.__onBuildFinishedCallback = None
        self.__servsender = BigWorld.player().interfaceSender
        self.__requestCount = 1
        self.__chunkCount = 0
        self.__respObFromChunks = []
        self.__chunksValid = True
        self.__generateEvent = generateEvent
        return

    def setFinishCallback(self, callback):
        self.__onBuildFinishedCallback = callback

    def build(self):
        headers, args, method = self.__requestob
        debug_utils.IfaceDebugOutput(COMMAND_TYPES.REQUEST, ob=self.__requestob)

        def cacheHandler(request, reqFromCache):
            newrequest = []
            for data, idTypeList in request:
                requestifaces = {}
                idList, typeList = splitIDTypeList(idTypeList)
                ids = idFromList(idList)
                types = idFromList(typeList)
                for ifacename in data:
                    ifacedata = getFromCache(idTypeList, ifacename)
                    if ifacedata is None:
                        requestifaces[ifacename] = data[ifacename]
                    else:
                        reqFromCache.append([{ifacename: data[ifacename]}, idTypeList])

                if requestifaces:
                    newrequest.append([requestifaces, idTypeList])

            return newrequest

        def transformRequestFromAS(request):
            transformedRequest = {}
            for arg in request:
                ifaces, idTypeList = arg + [None] * (2 - len(arg))
                if idTypeList is None:
                    idTypeList = []
                for ifacename in ifaces:
                    self.__separateBuilder(ifacename, ifacename, ifaces[ifacename], idTypeList, transformedRequest)

            return transformedRequest

        def constructRequestOb(transformedRequest):
            clientRequestob, serverRequestob = [], []
            viewClientRequestob, viewServerRequestob = [], []

            def fillifaces(ifacedict1, ifacedict2, ifacename, obtype, ifacedata):
                if getOblocation(ifacename, listFromId(obtype)) == OB_LOCATION.CLIENT:
                    ifacedict1[ifacename] = ifacedata
                else:
                    ifacedict2[ifacename] = ifacedata

            def fillob(ifacedict, requestob, obid, obtype):
                if ifacedict:
                    requestob.append([ifacedict, joinIDTypeList(listFromId(obid), listFromId(obtype))])

            for obid in transformedRequest:
                for obtype in transformedRequest[obid]:
                    clientObtypeIfaces, serverObtypeIfaces = {}, {}
                    viewClientObypteIfaces, viewServerObtypeIfaces = {}, {}
                    for parent, ifacenames in transformedRequest[obid][obtype].iteritems():
                        clientIfaces, serverIfaces = {}, {}
                        viewClientIfaces, viewServerIfaces = {}, {}
                        for ifacename, data in ifacenames.iteritems():
                            iface = getIface(ifacename)
                            ifacedata = dict(((attr, value) for attr, value in data.iteritems() if attr in iface.attr))
                            if len(ifacenames) > 1:
                                ifacename = '%s:%s' % (parent, ifacename)
                            if INDEXTOMETHOD[method] == 'edit' and not ifacedata and parent != ifacename:
                                fillifaces(viewClientIfaces, viewServerIfaces, ifacename, obtype, ifacedata)
                            else:
                                fillifaces(clientIfaces, serverIfaces, ifacename, obtype, ifacedata)

                        clientObtypeIfaces.update(clientIfaces)
                        serverObtypeIfaces.update(serverIfaces)
                        viewClientObypteIfaces.update(viewClientIfaces)
                        viewServerObtypeIfaces.update(viewServerIfaces)

                    fillob(clientObtypeIfaces, clientRequestob, obid, obtype)
                    fillob(serverObtypeIfaces, serverRequestob, obid, obtype)
                    fillob(viewClientObypteIfaces, viewClientRequestob, obid, obtype)
                    fillob(viewServerObtypeIfaces, viewServerRequestob, obid, obtype)

            return (clientRequestob,
             serverRequestob,
             viewClientRequestob,
             viewServerRequestob)

        def saveIfaceData(transformedResponse, ifacesdata):
            for ifacedata in ifacesdata:
                ifaces, idTypeList = ifacedata
                idList, typeList = splitIDTypeList(idTypeList)
                ids = idFromList(idList)
                types = idFromList(typeList)
                for parentIfacename in ifaces:
                    names = parentIfacename.split(':')
                    try:
                        parent, ifacename = (parentIfacename, parentIfacename) if len(names) == 1 else names
                    except ValueError:
                        LOG_ERROR('names: {0}'.format(names))
                        parent, ifacename = names[0], names[-1]

                    transformedResponse.setdefault(ids, {}).setdefault(types, {}).setdefault(parent, {}).setdefault(ifacename, {}).update(ifaces[parentIfacename] or {})

        def responseObBuilder(transformedResponse, reqFromCache, responseob):
            self.__requestCount -= 1
            headers, data, code = responseob
            if code == ErrorCodes.SUCCESS:
                processIFaceData(headers, data)
                saveIfaceData(transformedResponse, data)
            else:
                debug_utils.LOG_DEBUG('Iface:resonse:error:', responseob, code)
            onResponseObBuilt(transformedResponse, reqFromCache, headers, code)

        def onResponseObBuilt(transformedResponse, reqFromCache, headers, code):
            if self.__requestCount:
                return

            def data():
                for obid in transformedResponse:
                    for obtype in transformedResponse[obid]:
                        idTypeList = joinIDTypeList(listFromId(obid), listFromId(obtype))
                        ifacesdata = {}
                        for parent, ifaces in transformedResponse[obid][obtype].iteritems():
                            ifacedata = {}
                            for attrs in ifaces.itervalues():
                                ifacedata.update(attrs)

                            ifacesdata[parent] = ifacedata

                        yield [ifacesdata, idTypeList]

            def cachedata(ifacesFromCache):
                for obid in transformedResponse:
                    for obtype in transformedResponse[obid]:
                        idTypeList = joinIDTypeList(listFromId(obid), listFromId(obtype))
                        idList, typeList = splitIDTypeList(idTypeList)
                        ids = idFromList(idList)
                        types = idFromList(typeList)
                        for parentName, ifaces in transformedResponse[obid][obtype].iteritems():
                            for ifacename, attrs in ifaces.iteritems():
                                if not ifacesFromCache.get(ids, {}).get(types, {}).get(ifacename, False):
                                    if attrs:
                                        setToCache(idTypeList, ifacename, attrs)
                                    else:
                                        deleteFromCache(idTypeList, ifacename)
                                else:
                                    transformedResponse[obid][obtype][parentName][ifacename] = getFromCache(idTypeList, ifacename) or {}

            ifacesFromCache = {}
            for reqData, idTypeList in reqFromCache:
                idList, typeList = splitIDTypeList(idTypeList)
                ids = idFromList(idList)
                types = idFromList(typeList)
                for ifacename in reqData:
                    reqData[ifacename] = getFromCache(idTypeList, ifacename) or {}
                    ifacesFromCache.setdefault(ids, {}).setdefault(types, {})[iface_name(ifacename)] = True

            saveIfaceData(transformedResponse, reqFromCache)
            idata = list(data())
            if code == ErrorCodes.SUCCESS:
                if self.__generateEvent:
                    responseEventGenerate(headers, idata)
                cachedata(ifacesFromCache)
            responseob = [headers, idata if code == ErrorCodes.SUCCESS else ErrorCodes.ERROR_DESCRIPTION.get(code, 'Unknown error'), code]
            self.__onBuildFinishedCallback(responseob)

        def buildClientResponse(transformedResponse, headers, clientRequestob, method, reqFromCache):
            if INDEXTOMETHOD[method] == 'view':
                clientRequestob = cacheHandler(clientRequestob, reqFromCache)
            responseob = handler(None, [headers, clientRequestob, method], None, False)
            responseObBuilder(transformedResponse, reqFromCache, responseob)
            return

        def processRequests(clientRequestob, serverRequestob, method, transformedResponse, reqFromCache):
            fromCache = INDEXTOMETHOD[method] == 'view'
            if fromCache:
                if serverRequestob:
                    serverRequestob = cacheHandler(serverRequestob, reqFromCache)
            if clientRequestob:
                self.__requestCount += 1
                if not serverRequestob:
                    buildClientResponse(transformedResponse, headers, clientRequestob, method, reqFromCache)
            if serverRequestob:

                def chunkResponse(clientRequestob, transformedRequest, reqFromCache, op, code, servResponseOb):
                    code = servResponseOb[2]
                    if not self.__chunksValid:
                        return
                    if code != SUCCESS:
                        self.__chunksValid = False
                        responseObBuilder(transformedRequest, reqFromCache, servResponseOb)
                        return
                    self.__respObFromChunks += servResponseOb[1]
                    self.__chunkCount -= 1
                    if not self.__chunkCount:
                        responseObBuilder(transformedRequest, reqFromCache, [servResponseOb[0], self.__respObFromChunks, servResponseOb[2]])
                        if clientRequestob:
                            buildClientResponse(transformedResponse, headers, clientRequestob, method, reqFromCache)

                self.__requestCount += 1
                for i in xrange(len(serverRequestob) / _CHUNK_SIZE + 1):
                    chunk = serverRequestob[i * _CHUNK_SIZE:(i + 1) * _CHUNK_SIZE]
                    if chunk:
                        self.__chunkCount += 1
                        self.__servsender.queueQuery([headers, chunk, method], partial(chunkResponse, clientRequestob, transformedResponse, reqFromCache))

        self.__requestCount = 1
        transformedResponse = {}
        reqFromCache = []
        clientRequestob, serverRequestob, viewClientRequestob, viewServerRequestob = constructRequestOb(transformRequestFromAS(args))
        processRequests(clientRequestob, serverRequestob, method, transformedResponse, reqFromCache)
        processRequests(viewClientRequestob, viewServerRequestob, METHODTOINDEX['view'], transformedResponse, reqFromCache)
        self.__requestCount -= 1
        onResponseObBuilt(transformedResponse, reqFromCache, [int(IS_CLIENT), method], ErrorCodes.SUCCESS)
        return None

    def __separateBuilder(self, ifacename, parentIfacename, ifacedata, idTypeList, result):
        idList, typeList = splitIDTypeList(idTypeList)
        ids = idFromList(idList)
        types = idFromList(typeList)
        piface = getIface(parentIfacename)
        parentdata = {}
        for attr in piface.attr:
            attrdata = ifacedata.get(attr, None)
            if attrdata is not None:
                parentdata[attr] = attrdata

        result.setdefault(ids, {}).setdefault(types, {}).setdefault(ifacename, {}).setdefault(parentIfacename, {}).update(parentdata)
        for parentIfacename in getIface(parentIfacename).parent:
            self.__separateBuilder(ifacename, parentIfacename, ifacedata, idTypeList, result)

        return