# Embedded file name: scripts/client/gui/Scaleform/LobbyCustomization.py
from consts import CAMOUFLAGE_GROUPS, CAMOUFLAGE_DURATION, CAMOUFLAGE_GROUP_NAME_TO_ID_MAP
import db.DBLogic
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from debug_utils import LOG_DEBUG
from clientConsts import HANGAR_MODE

class CamouflageVO:

    def __init__(self, id, iconPath, isInstalled, isBought, groupID, duration, cost):
        self.id = id
        self.iconPath = iconPath
        self.isInstalled = isInstalled
        self.isBought = isBought
        self.groupID = groupID
        self.duration = duration
        self.cost = cost


class LobbyCustomization:

    def __init__(self, planeID, camouflagesLeftTime, updatePreview = False):
        self.__previewCustomizationVisibility = True
        self.__planeID = planeID
        self.__camouflagesLeftTime = camouflagesLeftTime
        aircraftSettings = db.DBLogic.g_instance.getAircraftData(planeID)
        surfaceSettings = aircraftSettings.airplane.visualSettings.surfaceSettings
        self.__allList = []
        self.__currentCamouflages = dict(((groupID, camouflages[0]['id']) for groupID, camouflages in camouflagesLeftTime.items()))
        presentCamouflagesMap = dict(((groupID, dict(((r['id'], r['timeLeft']) for r in camouflages))) for groupID, camouflages in camouflagesLeftTime.items()))
        for decalGroup in surfaceSettings.decalsSettings.decalGroups.values():
            camouflageGroupID = CAMOUFLAGE_GROUP_NAME_TO_ID_MAP.get(decalGroup.name, -1)
            if camouflageGroupID != -1:
                for decal in decalGroup.decals.values():
                    time = -1
                    isBought = True
                    isInstalled = decal.id == self.__currentCamouflages[camouflageGroupID]
                    self.__allList.append(CamouflageVO(decal.id, decal.icoPath, isInstalled, isBought, camouflageGroupID, time, [1, 2, 1]))

        self.__previewCamouflages = {CAMOUFLAGE_GROUPS.HULL: -1,
         CAMOUFLAGE_GROUPS.NOSE: -1,
         CAMOUFLAGE_GROUPS.WINGS: -1}
        if updatePreview:
            self.__setCustomization(self.__currentCamouflages)

    def destroy(self):
        self.__planeID = None
        self.__camouflagesLeftTime = None
        return

    def __deepcopy__(self, var):
        from copy import deepcopy
        clone = LobbyCustomization(self.__planeID, self.__camouflagesLeftTime)
        for name, value in self.__dict__.iteritems():
            if name != '_LobbyCustomization__lobby':
                setattr(clone, name, deepcopy(value))

        return clone

    @property
    def previewCamouflages(self):
        return self.__previewCamouflages

    @property
    def currentCamouflages(self):
        return self.__currentCamouflages

    def sendCustomizationList(self, lobby):
        if lobby.mode == HANGAR_MODE.CUSTOMIZATION:
            lobby.call_1('hangar.setCustomizationList', self.__allList)

    def sendChangedCustomizationList(self, lobby):
        if lobby.mode == HANGAR_MODE.CUSTOMIZATION:
            lobby.call_1('hangar.updateCustomizationList', self.__allList)

    def setCamouflagesForPreview(self, camouflageHull, camouflageNose, camouflageWings):
        self.__previewCamouflages[CAMOUFLAGE_GROUPS.HULL] = camouflageHull
        self.__previewCamouflages[CAMOUFLAGE_GROUPS.NOSE] = camouflageNose
        self.__previewCamouflages[CAMOUFLAGE_GROUPS.WINGS] = camouflageWings
        if self.__previewCustomizationVisibility:
            self.__setCustomization(self.__previewCamouflages)

    def switchPreviewCustomizationVisibility(self, isVisible):
        self.__previewCustomizationVisibility = isVisible
        self.__setCustomization(isVisible and self.__previewCamouflages or self.__currentCamouflages)

    def __setCustomization(self, previewCamouflages):
        camouflagesToPreview = dict(((groupID, camouflage != -1 and camouflage or self.__currentCamouflages[groupID]) for groupID, camouflage in previewCamouflages.items()))
        if g_hangarSpace.space:
            g_hangarSpace.space.setCustomization(camouflagesToPreview)