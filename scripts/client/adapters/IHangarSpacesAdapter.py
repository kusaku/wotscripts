# Embedded file name: scripts/client/adapters/IHangarSpacesAdapter.py
import db.DBLogic
from adapters.DefaultAdapter import DefaultAdapter
from operator import itemgetter
from clientConsts import GUI_TYPES_DICT
from debug_utils import LOG_WARNING

class IHangarSpacesAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        from db.DBLogic import g_instance as dbInstance
        import BWPersonality
        ob = super(IHangarSpacesAdapter, self).__call__(account, ob, **kw)
        spaces = ((v['index'], (k, v)) for k, v in dbInstance.userHangarSpaces.iteritems())
        ob['spaces'] = []
        ob['spaceTypes'] = []
        ob['spaceImages'] = []
        selSpaces = 0
        forceNoWindow = False
        for spaceID, space in map(itemgetter(1), sorted(spaces, key=itemgetter(0))):
            if validateSpaceID(spaceID):
                if space.get('isModal', False):
                    ob['spaces'] = [space['spaceID']]
                    ob['spaceTypes'] = [space.get('loc', '')]
                    ob['spaceimages'] = [space.get('img', '')]
                    ob['showWindow'] = False
                    selSpaces = 1
                    break
                ob['spaces'].append(spaceID)
                ob['spaceTypes'].append(space.get('loc', ''))
                ob['spaceImages'].append(space.get('img', ''))
                if not space.get('switchOnActivation', False):
                    selSpaces += 1
                else:
                    forceNoWindow = True

        if 'showWindow' not in ob:
            ob['showWindow'] = True
        ob['showWindow'] = ob['showWindow'] and selSpaces > 1 and not forceNoWindow
        return ob

    def edit(self, account, requestID, idTypeList, data, ob = None, **kw):
        return data


def validateSpaceID(spaceID, accountType = None):
    import BWPersonality
    import BigWorld
    if not spaceID:
        return False
    hangarSpace = getHangarSpaceByID(spaceID)
    return BigWorld.player().checkAccessibility(hangarSpace, accountType or GUI_TYPES_DICT[BWPersonality.g_initPlayerInfo.useGUIType], [ e.upper() for e in BWPersonality.g_initPlayerInfo.activeEvents ])


def getDefaultSpaceID(accountType):
    __db = db.DBLogic.g_instance
    spaces = ((v['index'], k) for k, v in __db.userHangarSpaces.iteritems())
    defaultSpaceID = next(iter(filter(lambda spaceID: validateSpaceID(spaceID, accountType), map(itemgetter(1), sorted(spaces, key=itemgetter(0))))), None)
    if defaultSpaceID not in __db.userHangarSpaces:
        LOG_WARNING('Space for defaultSpaceID={0} not found in db'.format(defaultSpaceID))
    return defaultSpaceID


def getHangarSpaceByID(spaceID):
    __db = db.DBLogic.g_instance
    return __db.userHangarSpaces.get(spaceID, None)