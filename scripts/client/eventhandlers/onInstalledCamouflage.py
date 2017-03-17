# Embedded file name: scripts/client/eventhandlers/onInstalledCamouflage.py
from debug_utils import LOG_WARNING

def onInstalledCamouflage(event):

    def previewmodelCamouflage(event):
        from BWPersonality import g_lobbyCarouselHelper as lch
        plane = lch.getCarouselAirplaneSelected()
        if plane is not None and event.idTypeList[0][0] != plane.planeID:
            LOG_WARNING('Current plane {0} is not the same to event plane {1}'.format(plane.planeID, event.idTypeList[0][0]))
            return
        else:
            from gui.Scaleform.utils.HangarSpace import g_hangarSpace
            if g_hangarSpace.space:
                g_hangarSpace.space.setCustomization(event.ob['ids'])
            return

    def planeCamouflage(event):
        from exchangeapi.CommonUtils import generateID
        from Helpers import memcache as memCacheUtility
        idTypeList = event.idTypeList
        idTypeList = [[idTypeList[0][0], 'previewmodel']]
        cacheID = generateID(idTypeList, event.iface.ifacename)
        memCacheUtility.setToCache(cacheID, event.ob)

    handlers = dict(plane=planeCamouflage, previewmodel=previewmodelCamouflage)
    for idtype in event.idTypeList:
        handlers[idtype[1]](event)