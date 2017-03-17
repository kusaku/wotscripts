# Embedded file name: scripts/common/exchangeapi/CompactDescriptor.py
from IfaceUtils import IfacesDB, ObTypes, ObTypesDB
from CommonUtils import METHODTOINDEX
from _ifaces import Ifaces
from debug_utils import LOG_ERROR
from config_consts import IS_DEVELOPMENT
from exchangeapi.ErrorCodes import SUCCESS
deleteIndex = METHODTOINDEX['delete']
viewIndex = METHODTOINDEX['view']

def __valueResponseDumps(headers, code, iface, values):
    if headers[1] is not deleteIndex:
        for attr in iface.attr:
            if IS_DEVELOPMENT and attr not in values:
                LOG_ERROR("CompactDescriptor can't find value for attr %s in %s interface" % (attr, iface.ifacename))
            yield values.get(attr, None)

    return


def __valueRequestDumps(headers, code, iface, values):
    if code not in (deleteIndex, viewIndex):
        yield values


def __dataDumps(headers, body, code, valueDumps, checkCode):
    for item in headers:
        yield item

    if not checkCode or code is SUCCESS:
        for ifaces, idTypeList in body:
            yield len(ifaces)
            for ifacenames, values in ifaces.iteritems():
                ifaces = tuple((IfacesDB[name] for name in ifacenames.split(':')))
                iface = ifaces[-1]
                yield iface.index if len(ifaces) is 1 else tuple((item.index for item in ifaces))
                for item in valueDumps(headers, code, iface, values):
                    yield item

            yield len(idTypeList)
            for id_, type_ in idTypeList:
                yield id_
                yield ObTypesDB[type_ or 'account']

    else:
        yield body
    yield code


def __valueResponseLoads(compactDescriptor, iface, ifacename, ifacedict, currentIndex):
    count = 0
    if compactDescriptor[1] is not deleteIndex:
        for attr in iface.attr:
            ifacedict[ifacename][attr] = compactDescriptor[currentIndex]
            count += 1
            currentIndex += 1

    return count


def __valueRequestLoads(compactDescriptor, iface, ifacename, ifacedict, currentIndex):
    count = 0
    if compactDescriptor[-1] not in (deleteIndex, viewIndex):
        ifacedict[ifacename] = compactDescriptor[currentIndex]
        count += 1
    return count


def __dataLoads(compactDescriptor, headersLen, valueLoads, checkCode):

    def body():
        currentIndex = headersLen
        while currentIndex < len(compactDescriptor) - 1:
            ifacelen = compactDescriptor[currentIndex]
            currentIndex += 1
            ifacedict = {}
            while ifacelen:
                ifaces = compactDescriptor[currentIndex]
                ifaces = tuple((Ifaces.iface[ind] for ind in (ifaces if isinstance(ifaces, (tuple, list)) else (ifaces,))))
                currentIndex += 1
                ifacename = ':'.join((iface.ifacename for iface in ifaces))
                ifacedict[ifacename] = {}
                iface = ifaces[-1]
                currentIndex += valueLoads(compactDescriptor, iface, ifacename, ifacedict, currentIndex)
                ifacelen -= 1

            idTypeListLen = compactDescriptor[currentIndex]
            currentIndex += 1
            idTypeList = []
            while idTypeListLen:
                type_ = ObTypes[compactDescriptor[currentIndex + 1]]
                id_ = compactDescriptor[currentIndex]
                idTypeList.append([id_, type_ if type_ != 'account' or id_ is not None else None])
                idTypeListLen -= 1
                currentIndex += 2

            yield [ifacedict, idTypeList]

        return

    return [list(compactDescriptor[:headersLen]), list(body()) if not checkCode or compactDescriptor[-1] is SUCCESS else compactDescriptor[headersLen], compactDescriptor[-1]]


def responseToCompactDescriptor(response):
    return list(__dataDumps(valueDumps=__valueResponseDumps, checkCode=True, *response))


def compactDescriptorToResponse(compactDescriptor):
    return __dataLoads(compactDescriptor, 3, valueLoads=__valueResponseLoads, checkCode=True)


def requestToCompactDescriptor(request):
    return list(__dataDumps(valueDumps=__valueRequestDumps, checkCode=False, *request))


def compactDescriptorToRequest(compactDescriptor):
    return __dataLoads(compactDescriptor, 1, valueLoads=__valueRequestLoads, checkCode=False)