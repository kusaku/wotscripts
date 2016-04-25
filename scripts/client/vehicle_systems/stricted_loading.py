# Embedded file name: scripts/client/vehicle_systems/stricted_loading.py
import BigWorld
import functools
import debug_utils

def restrictBySpace(callback, *args, **kwargs):
    return functools.partial(_restrictedLoadCall, BigWorld.player().spaceID, None, callback, args=args, kwargs=kwargs)


def restrictBySpaceAndNode(node, callback, *args, **kwargs):
    return functools.partial(_restrictedLoadCall, BigWorld.player().spaceID, node, callback, args=args, kwargs=kwargs)


def _restrictedLoadCall(spaceID, node, callback, resource, args, kwargs):
    player = BigWorld.player()
    fail = player is None or player.spaceID != spaceID
    fail |= node is not None and node.isDangling
    if fail:
        debug_utils.LOG_DEBUG('Background loading callback is too late, stopping logic')
        return
    else:
        callback(*(args + (resource,)), **kwargs)
        return