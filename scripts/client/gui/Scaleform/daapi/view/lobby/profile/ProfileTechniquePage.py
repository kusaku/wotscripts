# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/profile/ProfileTechniquePage.py
from account_helpers import AccountSettings
from account_helpers.AccountSettings import PROFILE_TECHNIQUE
from gui.Scaleform.daapi.view.meta.ProfileTechniquePageMeta import ProfileTechniquePageMeta
from gui.Scaleform.locale.PROFILE import PROFILE
from gui.shared.ItemsCache import g_itemsCache
from helpers.i18n import makeString
from gui.Scaleform.genConsts.PROFILE_DROPDOWN_KEYS import PROFILE_DROPDOWN_KEYS

class ProfileTechniquePage(ProfileTechniquePageMeta):

    def _populate(self):
        super(ProfileTechniquePage, self)._populate()
        if self._selectedData is not None:
            intVehCD = int(self._selectedData.get('itemCD'))
            accountDossier = g_itemsCache.items.getAccountDossier(None)
            if intVehCD in accountDossier.getRandomStats().getVehicles():
                self._battlesType = PROFILE_DROPDOWN_KEYS.ALL
            elif intVehCD in accountDossier.getTeam7x7Stats().getVehicles():
                self._battlesType = PROFILE_DROPDOWN_KEYS.TEAM
            elif intVehCD in accountDossier.getHistoricalStats().getVehicles():
                self._battlesType = PROFILE_DROPDOWN_KEYS.HISTORICAL
            elif intVehCD in accountDossier.getFortBattlesStats().getVehicles():
                self._battlesType = PROFILE_DROPDOWN_KEYS.FORTIFICATIONS_BATTLES
            elif intVehCD in accountDossier.getFortSortiesStats().getVehicles():
                self._battlesType = PROFILE_DROPDOWN_KEYS.FORTIFICATIONS_SORTIES
            elif intVehCD in accountDossier.getRated7x7Stats().getVehicles():
                self._battlesType = PROFILE_DROPDOWN_KEYS.STATICTEAM
            elif intVehCD in accountDossier.getFalloutStats().getVehicles():
                self._battlesType = PROFILE_DROPDOWN_KEYS.FALLOUT
        self.as_setSelectedVehicleIntCDS(int(self._selectedData.get('itemCD')) if self._selectedData else -1)
        return

    def _getInitData(self, accountDossier = None, isFallout = False):
        initDataResult = super(ProfileTechniquePage, self)._getInitData(accountDossier, isFallout)
        initDataResult['hangarVehiclesLabel'] = makeString(PROFILE.SECTION_TECHNIQUE_WINDOW_HANGARVEHICLESLABEL)
        storedData = AccountSettings.getFilter(PROFILE_TECHNIQUE)
        initDataResult['isInHangarSelected'] = storedData['isInHangarSelected']
        initDataResult['selectedColumn'] = storedData['selectedColumn']
        initDataResult['selectedColumnSorting'] = storedData['selectedColumnSorting']
        return initDataResult

    def _getTechniqueListVehicles(self, targetData, addVehiclesThatInHangarOnly = False):
        storedData = AccountSettings.getFilter(PROFILE_TECHNIQUE)
        return super(ProfileTechniquePage, self)._getTechniqueListVehicles(targetData, storedData['isInHangarSelected'])

    def setIsInHangarSelected(self, value):
        storedData = AccountSettings.getFilter(PROFILE_TECHNIQUE)
        storedData['isInHangarSelected'] = value
        AccountSettings.setFilter(PROFILE_TECHNIQUE, storedData)
        if self._data is not None:
            self.as_responseDossierS(self._battlesType, self._getTechniqueListVehicles(self._data), '', self.getEmptyScreenLabel())
        return

    def requestData(self, vehicleId):
        self._receiveVehicleDossier(int(vehicleId), None)
        return

    def setSelectedTableColumn(self, index, sortDirection):
        storedData = AccountSettings.getFilter(PROFILE_TECHNIQUE)
        storedData['selectedColumn'] = index
        storedData['selectedColumnSorting'] = sortDirection
        AccountSettings.setFilter(PROFILE_TECHNIQUE, storedData)
        if self._dossier is not None:
            self.as_setInitDataS(self._getInitData(self._dossier, self._battlesType == PROFILE_DROPDOWN_KEYS.FALLOUT))
        return