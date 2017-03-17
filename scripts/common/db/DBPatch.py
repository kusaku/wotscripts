# Embedded file name: scripts/common/db/DBPatch.py
import debug_utils
import types
import inspect

def obj2xml(dataObject):
    """
    Output xml representation of an arbitrary object to debug output, for debug purposes.
    """
    if dataObject == None:
        pass
    elif dataObject == '__call__':
        pass
    elif dataObject == '__add__':
        pass
    elif isinstance(dataObject, types.IntType):
        debug_utils.LOG_NOTE(str(dataObject))
    elif isinstance(dataObject, types.LongType):
        debug_utils.LOG_NOTE(str(dataObject))
    elif isinstance(dataObject, types.FloatType):
        debug_utils.LOG_NOTE(str(dataObject))
    elif isinstance(dataObject, types.StringTypes):
        debug_utils.LOG_NOTE(str(dataObject))
    elif isinstance(dataObject, types.BooleanType):
        debug_utils.LOG_NOTE(str(dataObject))
    elif isinstance(dataObject, types.ListType):
        for item in dataObject:
            debug_utils.LOG_NOTE('<__listitem>')
            obj2xml(item)
            debug_utils.LOG_NOTE('</__listitem>')

    elif isinstance(dataObject, types.DictType):
        for key in dataObject.keys():
            debug_utils.LOG_NOTE('<__dictitem key="' + str(key) + '">')
            obj2xml(dataObject[key])
            debug_utils.LOG_NOTE('</__dictitem>')

    elif isinstance(dataObject, object):
        for attributeName, attributeValue in inspect.getmembers(dataObject):
            if len(attributeName) > 4 and attributeName[0:2] == '__' and attributeName[-2:] == '__':
                continue
            if attributeName == 'asBlob':
                continue
            if isinstance(attributeValue, types.TypeType):
                continue
            if isinstance(attributeValue, types.MethodType):
                debug_utils.LOG_NOTE('<method name="' + attributeName + '" />')
            else:
                debug_utils.LOG_NOTE('<' + attributeName + '>')
                obj2xml(attributeValue)
                debug_utils.LOG_NOTE('</' + attributeName + '>')

    else:
        debug_utils.LOG_NOTE('ERROR unknown type unknown data.')
    return


def patch(dataObject, patchObject):
    """
    Data inheritance implementation; every attribute of dataObject is updated with similar attribute of patchObject.
    
    dataObject  - object to be "patched" (updated)
    patchObject - well, it's a patch-object :)
    
    Examples:
        dataObject.x == 0, patchObject.x == 1 results in dataObject.x == 1
        dataObject.x == 0, patchObject.x == None results in dataObject.x == 0
        dataObject.x == None, patchObject.x == 1 results in dataObject.x == 1
        dataObject.x == [1, 2], patchObject.x == [3] results in dataObject.x == [1, 2, 3]
        dataObject.x == ['a':1, 'b':2], patchObject.x == ['c':3] results in dataObject.x == ['a':1, 'b':2, 'c':3]
    """
    if isinstance(patchObject, types.IntType):
        dataObject = patchObject
    elif isinstance(patchObject, types.LongType):
        dataObject = patchObject
    elif isinstance(patchObject, types.FloatType):
        dataObject = patchObject
    elif isinstance(patchObject, types.StringTypes):
        dataObject = patchObject
    elif isinstance(patchObject, types.BooleanType):
        dataObject = patchObject
    elif isinstance(patchObject, types.ListType):
        for item in patchObject:
            dataObject.append(item)

    elif isinstance(patchObject, types.DictType):
        for key in patchObject.keys():
            patch(dataObject[key], patchObject[key])

    elif isinstance(patchObject, object):
        for attributeName, attributeValue in inspect.getmembers(patchObject):
            if attributeName[0:1] == '_' or isinstance(attributeValue, types.MethodType):
                continue
            elif hasattr(dataObject, attributeName):
                patch(getattr(dataObject, attributeName), attributeValue)
            else:
                dataObject.__dict__[attributeName] = attributeValue


def update(dataObject, updateObject):
    """
    "Force" copy of every data field from updateObject to data object.
    dataObject and updateObject should be actual objects, not simple types like strings, integers, etc.
    
    dataObject  - object to be updated (fields are rewrited/added, as necessary)
    updateObject - well, it's a update-object :)
    
    Examples:
        dataObject.x == 0, updateObject.x == 1 results in dataObject.x == 1
        dataObject.x == 0, updateObject.x == None results in dataObject.x == 0
        dataObject.x == None, updateObject.x == 1 results in dataObject.x == 1
    """
    for attributeName, attributeValue in inspect.getmembers(updateObject):
        if attributeName[0:1] == '_' or isinstance(attributeValue, types.MethodType):
            continue
        else:
            dataObject.__dict__[attributeName] = attributeValue