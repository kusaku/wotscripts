# Embedded file name: scripts/client/Helpers/reliableDelivery.py
from exchangeapi.CompactDescriptor import compactDescriptorToResponse
_RESPONSE_CALLBACKS = {}

def popMappedCallback(callbackId, defaultCallback):
    return _RESPONSE_CALLBACKS.pop(callbackId, defaultCallback)


def clearMappedCallbacks():
    _RESPONSE_CALLBACKS.clear()


def ifaceDataCallback(callback, op, code, servResponseOb):
    servResponseOb = compactDescriptorToResponse(servResponseOb)
    headers = servResponseOb[0]
    responseId = headers[2]
    if responseId not in _RESPONSE_CALLBACKS:
        _RESPONSE_CALLBACKS[responseId] = callback
    from exchangeapi.AdapterUtils import getAdapter
    getAdapter('IResponse', ['response']).add(None, None, {'data': servResponseOb}, idTypeList=[[responseId, 'response']])
    return