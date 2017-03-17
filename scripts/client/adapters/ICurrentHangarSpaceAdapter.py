# Embedded file name: scripts/client/adapters/ICurrentHangarSpaceAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from consts import EMPTY_IDTYPELIST
from adapters.IHangarSpacesAdapter import getHangarSpaceByID

class ICurrentHangarSpaceAccountAdapter(DefaultAdapter):

    def view(self, account, requestID, idTypeList, ob = None, **kw):
        import BWPersonality
        spaceID = BWPersonality.g_settings.hangarSpaceSettings['spaceID']
        hangarSpace = getHangarSpaceByID(spaceID)
        return dict(spaceID=spaceID, isModal=hangarSpace.get('isModal', False))

    def edit(self, account, requestID, idTypeList, data, ob = None, **kw):
        from adapters.IHangarSpacesAdapter import validateSpaceID
        from Helpers.cache import getFromCache
        import BWPersonality
        spaceID = data.get('spaceID', '')
        if validateSpaceID(spaceID):
            import BigWorld
            from Account import PlayerAccount
            player = BigWorld.player()
            if player and player.__class__ == PlayerAccount:
                from db.DBLogic import g_instance as dbInstance
                switchSpaces = (hangarSpace for spaceID, hangarSpace in dbInstance.userHangarSpaces.iteritems() if hangarSpace.get('switchOnActivation', False))
                switchSpace = player.findSuitableHangarSpace(switchSpaces)
                BWPersonality.g_settings.hangarSpaceSettings['ignoreEventHangar'] = switchSpace is not None and switchSpace['spaceID'] != spaceID
            BWPersonality.g_settings.hangarSpaceSettings['spaceID'] = spaceID
            return data
        else:
            return getFromCache(idTypeList, self._ifacename)


class ICurrentHangarSpacePreviewAdapter(DefaultAdapter):

    def add(self, account, requestID, data, **kw):
        from Helpers.cache import getFromCache
        spaceID = data.get('spaceID', '')
        if spaceID:
            from adapters.IHangarSpacesAdapter import validateSpaceID
            from exchangeapi.AdapterUtils import getAdapter
            if validateSpaceID(spaceID):
                currentHangarSpaceData = getFromCache(kw['idTypeList'], self._ifacename) or getAdapter(self._ifacename, ['account']).view(None, None, EMPTY_IDTYPELIST)
                if currentHangarSpaceData is None or currentHangarSpaceData.get('spaceID', '') != spaceID:
                    from gui.Scaleform.utils.HangarSpace import g_hangarSpace
                    from BWPersonality import g_lobbyCarouselHelper
                    from db.DBLogic import g_instance as dbInstance
                    hangarSpace = dbInstance.userHangarSpaces[spaceID]
                    g_hangarSpace.refreshSpace(hangarSpace['hangarType'], spaceID)
                    g_lobbyCarouselHelper.queryRefresh3DModel(g_lobbyCarouselHelper.getCarouselAirplaneSelected())
                    return data
        return getFromCache(kw['idTypeList'], self._ifacename)

    def delete(self, account, requestID, idTypeList, **kw):
        from exchangeapi.AdapterUtils import getAdapter
        self.add(None, None, getAdapter(self._ifacename, ['account']).view(None, None, EMPTY_IDTYPELIST), idTypeList=idTypeList)
        return