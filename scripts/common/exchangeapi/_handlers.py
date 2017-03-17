# Embedded file name: scripts/common/exchangeapi/_handlers.py
import Math
import math
import consts
true = True
false = False

class Dummy:
    pass


isServerDatabase = False

class AMMO_TYPE:
    BALL = 0
    AP = 1
    APC = 2
    I = 3
    APHC = 4
    API = 5
    HEI = 6
    APHE = 7
    ALL_TYPES = (BALL,
     AP,
     APC,
     I,
     APHC,
     API,
     HEI,
     APHE)


Handlers = Dummy()
Handlers.handler = []
Handlers.handler.insert(0, None)
Handlers.handler[0] = Dummy()
Handlers.handler[0].eventName = []
Handlers.handler[0].eventName.insert(0, None)
Handlers.handler[0].eventName[0] = 'edit'
Handlers.handler[0].ifaceName = 'IInstalledRocket'
Handlers.handler[0].module = 'eventhandlers.refreshCarouselPlane.refreshCarouselPlane'
Handlers.handler[0].priority = 0
Handlers.handler[0].scope = 'client'
Handlers.handler.insert(1, None)
Handlers.handler[1] = Dummy()
Handlers.handler[1].eventName = []
Handlers.handler[1].eventName.insert(0, None)
Handlers.handler[1].eventName[0] = 'edit'
Handlers.handler[1].ifaceName = 'IInstalledBomb'
Handlers.handler[1].module = 'eventhandlers.refreshCarouselPlane.refreshCarouselPlane'
Handlers.handler[1].priority = 0
Handlers.handler[1].scope = 'client'
Handlers.handler.insert(2, None)
Handlers.handler[2] = Dummy()
Handlers.handler[2].eventName = []
Handlers.handler[2].eventName.insert(0, None)
Handlers.handler[2].eventName[0] = 'edit'
Handlers.handler[2].ifaceName = 'IInstalledGlobalID'
Handlers.handler[2].module = 'eventhandlers.updatePlaneSpecs.updatePlaneSpecs'
Handlers.handler[2].priority = 0
Handlers.handler[2].scope = 'client'
Handlers.handler.insert(3, None)
Handlers.handler[3] = Dummy()
Handlers.handler[3].eventName = []
Handlers.handler[3].eventName.insert(0, None)
Handlers.handler[3].eventName[0] = 'edit'
Handlers.handler[3].ifaceName = 'IInstalledEquipment'
Handlers.handler[3].module = 'eventhandlers.onChangeInstalledEquipment.onChangeInstalledEquipment'
Handlers.handler[3].priority = 0
Handlers.handler[3].scope = 'client'
Handlers.handler.insert(4, None)
Handlers.handler[4] = Dummy()
Handlers.handler[4].eventName = []
Handlers.handler[4].eventName.insert(0, None)
Handlers.handler[4].eventName[0] = 'edit'
Handlers.handler[4].eventName.insert(1, None)
Handlers.handler[4].eventName[1] = 'view'
Handlers.handler[4].ifaceName = 'IInstalledCamouflage'
Handlers.handler[4].module = 'eventhandlers.onInstalledCamouflage.onInstalledCamouflage'
Handlers.handler[4].priority = 0
Handlers.handler[4].scope = 'client'
Handlers.handler.insert(5, None)
Handlers.handler[5] = Dummy()
Handlers.handler[5].eventName = []
Handlers.handler[5].eventName.insert(0, None)
Handlers.handler[5].eventName[0] = 'edit'
Handlers.handler[5].ifaceName = 'IDepotCount'
Handlers.handler[5].module = 'eventhandlers.onChangedDepotCount.onChangedDepotCount'
Handlers.handler[5].priority = 0
Handlers.handler[5].scope = 'client'
Handlers.handler.insert(6, None)
Handlers.handler[6] = Dummy()
Handlers.handler[6].eventName = []
Handlers.handler[6].eventName.insert(0, None)
Handlers.handler[6].eventName[0] = 'edit'
Handlers.handler[6].ifaceName = 'IInterface'
Handlers.handler[6].module = 'eventhandlers.responsedataCache.updateResponsedataCache'
Handlers.handler[6].priority = 0
Handlers.handler[6].scope = 'client'
Handlers.handler.insert(7, None)
Handlers.handler[7] = Dummy()
Handlers.handler[7].eventName = []
Handlers.handler[7].eventName.insert(0, None)
Handlers.handler[7].eventName[0] = 'delete'
Handlers.handler[7].ifaceName = 'IInterface'
Handlers.handler[7].module = 'eventhandlers.responsedataCache.deleteResponsedataCache'
Handlers.handler[7].priority = 0
Handlers.handler[7].scope = 'client'
Handlers.handler.insert(8, None)
Handlers.handler[8] = Dummy()
Handlers.handler[8].eventName = []
Handlers.handler[8].eventName.insert(0, None)
Handlers.handler[8].eventName[0] = 'add'
Handlers.handler[8].ifaceName = 'IResponse'
Handlers.handler[8].module = 'eventhandlers.responseEvents.responseAdded'
Handlers.handler[8].priority = 0
Handlers.handler[8].scope = 'client'
Handlers.handler.insert(9, None)
Handlers.handler[9] = Dummy()
Handlers.handler[9].eventName = []
Handlers.handler[9].eventName.insert(0, None)
Handlers.handler[9].eventName[0] = 'delete'
Handlers.handler[9].ifaceName = 'IResponse'
Handlers.handler[9].module = 'eventhandlers.responseEvents.responseDeleted'
Handlers.handler[9].priority = 0
Handlers.handler[9].scope = 'client'
Handlers.handler.insert(10, None)
Handlers.handler[10] = Dummy()
Handlers.handler[10].eventName = []
Handlers.handler[10].eventName.insert(0, None)
Handlers.handler[10].eventName[0] = 'add'
Handlers.handler[10].ifaceName = 'IBattleResult'
Handlers.handler[10].module = 'eventhandlers.onBattleResult.onBattleResultShort'
Handlers.handler[10].priority = 1
Handlers.handler[10].scope = 'client'
Handlers.handler.insert(11, None)
Handlers.handler[11] = Dummy()
Handlers.handler[11].eventName = []
Handlers.handler[11].eventName.insert(0, None)
Handlers.handler[11].eventName[0] = 'add'
Handlers.handler[11].ifaceName = 'IBattleResult'
Handlers.handler[11].module = 'eventhandlers.onBattleResult.onSessionBattleResults'
Handlers.handler[11].priority = 0
Handlers.handler[11].scope = 'client'
Handlers.handler.insert(12, None)
Handlers.handler[12] = Dummy()
Handlers.handler[12].eventName = []
Handlers.handler[12].eventName.insert(0, None)
Handlers.handler[12].eventName[0] = 'edit'
Handlers.handler[12].ifaceName = 'IStatus'
Handlers.handler[12].module = 'eventhandlers.onChangedStatus.onChangedPlaneStatus'
Handlers.handler[12].priority = 0
Handlers.handler[12].scope = 'client'
Handlers.handler.insert(13, None)
Handlers.handler[13] = Dummy()
Handlers.handler[13].eventName = []
Handlers.handler[13].eventName.insert(0, None)
Handlers.handler[13].eventName[0] = 'edit'
Handlers.handler[13].ifaceName = 'IStatus'
Handlers.handler[13].module = 'eventhandlers.onChangedStatus.onChangedAccountStatus'
Handlers.handler[13].priority = 0
Handlers.handler[13].scope = 'server'
Handlers.handler.insert(14, None)
Handlers.handler[14] = Dummy()
Handlers.handler[14].eventName = []
Handlers.handler[14].eventName.insert(0, None)
Handlers.handler[14].eventName[0] = 'edit'
Handlers.handler[14].ifaceName = 'IInstalledAmmoBelt'
Handlers.handler[14].module = 'eventhandlers.EventIInstalledAmmoBelt.onIInstalledAmmoBeltEdit'
Handlers.handler[14].priority = 0
Handlers.handler[14].scope = 'server'
Handlers.handler.insert(15, None)
Handlers.handler[15] = Dummy()
Handlers.handler[15].eventName = []
Handlers.handler[15].eventName.insert(0, None)
Handlers.handler[15].eventName[0] = 'edit'
Handlers.handler[15].ifaceName = 'IInstalledEquipment'
Handlers.handler[15].module = 'eventhandlers.upgradePlane.changeEquipment'
Handlers.handler[15].priority = 0
Handlers.handler[15].scope = 'server'
Handlers.handler.insert(16, None)
Handlers.handler[16] = Dummy()
Handlers.handler[16].eventName = []
Handlers.handler[16].eventName.insert(0, None)
Handlers.handler[16].eventName[0] = 'edit'
Handlers.handler[16].ifaceName = 'IMessage'
Handlers.handler[16].module = 'eventhandlers.upgradePlane.upgradePlane'
Handlers.handler[16].priority = 0
Handlers.handler[16].scope = 'server'
Handlers.handler.insert(17, None)
Handlers.handler[17] = Dummy()
Handlers.handler[17].eventName = []
Handlers.handler[17].eventName.insert(0, None)
Handlers.handler[17].eventName[0] = 'settocache'
Handlers.handler[17].ifaceName = 'IMessage'
Handlers.handler[17].module = 'eventhandlers.eventIMessage.onIMessageCreate'
Handlers.handler[17].priority = 0
Handlers.handler[17].scope = 'client'
Handlers.handler.insert(18, None)
Handlers.handler[18] = Dummy()
Handlers.handler[18].eventName = []
Handlers.handler[18].eventName.insert(0, None)
Handlers.handler[18].eventName[0] = 'update'
Handlers.handler[18].ifaceName = 'IInstalledCount'
Handlers.handler[18].module = 'eventhandlers.EventIInstalledCE.onIInstalledCEEdit'
Handlers.handler[18].priority = 0
Handlers.handler[18].scope = 'server'
Handlers.handler.insert(19, None)
Handlers.handler[19] = Dummy()
Handlers.handler[19].eventName = []
Handlers.handler[19].eventName.insert(0, None)
Handlers.handler[19].eventName[0] = 'before_edit'
Handlers.handler[19].ifaceName = 'IInstalledAmmoBelt'
Handlers.handler[19].module = 'eventhandlers.eventChangeIFace.onChangeIDepot'
Handlers.handler[19].priority = 0
Handlers.handler[19].scope = 'server'
Handlers.handler.insert(20, None)
Handlers.handler[20] = Dummy()
Handlers.handler[20].eventName = []
Handlers.handler[20].eventName.insert(0, None)
Handlers.handler[20].eventName[0] = 'before_edit'
Handlers.handler[20].ifaceName = 'IInstalledBomb'
Handlers.handler[20].module = 'eventhandlers.eventChangeIFace.onChangeIDepot'
Handlers.handler[20].priority = 0
Handlers.handler[20].scope = 'server'
Handlers.handler.insert(21, None)
Handlers.handler[21] = Dummy()
Handlers.handler[21].eventName = []
Handlers.handler[21].eventName.insert(0, None)
Handlers.handler[21].eventName[0] = 'before_edit'
Handlers.handler[21].ifaceName = 'IInstalledRocket'
Handlers.handler[21].module = 'eventhandlers.eventChangeIFace.onChangeIDepot'
Handlers.handler[21].priority = 0
Handlers.handler[21].scope = 'server'
Handlers.handler.insert(22, None)
Handlers.handler[22] = Dummy()
Handlers.handler[22].eventName = []
Handlers.handler[22].eventName.insert(0, None)
Handlers.handler[22].eventName[0] = 'before_edit'
Handlers.handler[22].ifaceName = 'IInstalledConsumables'
Handlers.handler[22].module = 'eventhandlers.eventChangeIFace.onChangeIDepot'
Handlers.handler[22].priority = 0
Handlers.handler[22].scope = 'server'
Handlers.handler.insert(23, None)
Handlers.handler[23] = Dummy()
Handlers.handler[23].eventName = []
Handlers.handler[23].eventName.insert(0, None)
Handlers.handler[23].eventName[0] = 'before_edit'
Handlers.handler[23].ifaceName = 'IInstalledEquipment'
Handlers.handler[23].module = 'eventhandlers.eventChangeIFace.onChangeIDepot'
Handlers.handler[23].priority = 0
Handlers.handler[23].scope = 'server'
Handlers.handler.insert(24, None)
Handlers.handler[24] = Dummy()
Handlers.handler[24].eventName = []
Handlers.handler[24].eventName.insert(0, None)
Handlers.handler[24].eventName[0] = 'before_edit'
Handlers.handler[24].ifaceName = 'IDepotCount'
Handlers.handler[24].module = 'eventhandlers.eventChangeIFace.onChangeIDepot'
Handlers.handler[24].priority = 0
Handlers.handler[24].scope = 'server'
Handlers.handler.insert(25, None)
Handlers.handler[25] = Dummy()
Handlers.handler[25].eventName = []
Handlers.handler[25].eventName.insert(0, None)
Handlers.handler[25].eventName[0] = 'before_edit'
Handlers.handler[25].ifaceName = 'IInstalledAmmoBelt'
Handlers.handler[25].module = 'eventhandlers.eventChangeIFace.onChangePlaneDepot'
Handlers.handler[25].priority = 0
Handlers.handler[25].scope = 'server'
Handlers.handler.insert(26, None)
Handlers.handler[26] = Dummy()
Handlers.handler[26].eventName = []
Handlers.handler[26].eventName.insert(0, None)
Handlers.handler[26].eventName[0] = 'before_edit'
Handlers.handler[26].ifaceName = 'IInstalledBomb'
Handlers.handler[26].module = 'eventhandlers.eventChangeIFace.onChangePlaneDepot'
Handlers.handler[26].priority = 0
Handlers.handler[26].scope = 'server'
Handlers.handler.insert(27, None)
Handlers.handler[27] = Dummy()
Handlers.handler[27].eventName = []
Handlers.handler[27].eventName.insert(0, None)
Handlers.handler[27].eventName[0] = 'before_edit'
Handlers.handler[27].ifaceName = 'IInstalledRocket'
Handlers.handler[27].module = 'eventhandlers.eventChangeIFace.onChangePlaneDepot'
Handlers.handler[27].priority = 0
Handlers.handler[27].scope = 'server'
Handlers.handler.insert(28, None)
Handlers.handler[28] = Dummy()
Handlers.handler[28].eventName = []
Handlers.handler[28].eventName.insert(0, None)
Handlers.handler[28].eventName[0] = 'before_edit'
Handlers.handler[28].ifaceName = 'IInstalledConsumables'
Handlers.handler[28].module = 'eventhandlers.eventChangeIFace.onChangePlaneDepot'
Handlers.handler[28].priority = 0
Handlers.handler[28].scope = 'server'
Handlers.handler.insert(29, None)
Handlers.handler[29] = Dummy()
Handlers.handler[29].eventName = []
Handlers.handler[29].eventName.insert(0, None)
Handlers.handler[29].eventName[0] = 'before_edit'
Handlers.handler[29].ifaceName = 'IInstalledEquipment'
Handlers.handler[29].module = 'eventhandlers.eventChangeIFace.onChangePlaneDepot'
Handlers.handler[29].priority = 0
Handlers.handler[29].scope = 'server'
Handlers.handler.insert(30, None)
Handlers.handler[30] = Dummy()
Handlers.handler[30].eventName = []
Handlers.handler[30].eventName.insert(0, None)
Handlers.handler[30].eventName[0] = 'before_edit'
Handlers.handler[30].ifaceName = 'IInstalledAmmoBelt'
Handlers.handler[30].module = 'eventhandlers.eventChangeIFace.onChangeIAccountResources'
Handlers.handler[30].priority = 0
Handlers.handler[30].scope = 'server'
Handlers.handler.insert(31, None)
Handlers.handler[31] = Dummy()
Handlers.handler[31].eventName = []
Handlers.handler[31].eventName.insert(0, None)
Handlers.handler[31].eventName[0] = 'before_edit'
Handlers.handler[31].ifaceName = 'IInstalledConsumables'
Handlers.handler[31].module = 'eventhandlers.eventChangeIFace.onChangeIAccountResources'
Handlers.handler[31].priority = 0
Handlers.handler[31].scope = 'server'
Handlers.handler.insert(32, None)
Handlers.handler[32] = Dummy()
Handlers.handler[32].eventName = []
Handlers.handler[32].eventName.insert(0, None)
Handlers.handler[32].eventName[0] = 'before_edit'
Handlers.handler[32].ifaceName = 'IInstalledEquipment'
Handlers.handler[32].module = 'eventhandlers.eventChangeIFace.onChangeIAccountResources'
Handlers.handler[32].priority = 0
Handlers.handler[32].scope = 'server'
Handlers.handler.insert(33, None)
Handlers.handler[33] = Dummy()
Handlers.handler[33].eventName = []
Handlers.handler[33].eventName.insert(0, None)
Handlers.handler[33].eventName[0] = 'edit'
Handlers.handler[33].ifaceName = 'IRepair'
Handlers.handler[33].module = 'eventhandlers.refreshCarouselPlane.refreshCarouselPlane'
Handlers.handler[33].priority = 0
Handlers.handler[33].scope = 'client'
Handlers.handler.insert(34, None)
Handlers.handler[34] = Dummy()
Handlers.handler[34].eventName = []
Handlers.handler[34].eventName.insert(0, None)
Handlers.handler[34].eventName[0] = 'before_edit'
Handlers.handler[34].ifaceName = 'IDepotCount'
Handlers.handler[34].module = 'eventhandlers.eventChangeIFace.onChangeIAccountResources'
Handlers.handler[34].priority = 0
Handlers.handler[34].scope = 'server'
Handlers.handler.insert(35, None)
Handlers.handler[35] = Dummy()
Handlers.handler[35].eventName = []
Handlers.handler[35].eventName.insert(0, None)
Handlers.handler[35].eventName[0] = 'market'
Handlers.handler[35].ifaceName = 'IDepotCount'
Handlers.handler[35].module = 'eventhandlers.EventMarket.onBuySell'
Handlers.handler[35].priority = 0
Handlers.handler[35].scope = 'server'
Handlers.handler.insert(36, None)
Handlers.handler[36] = Dummy()
Handlers.handler[36].eventName = []
Handlers.handler[36].eventName.insert(0, None)
Handlers.handler[36].eventName[0] = 'before_edit'
Handlers.handler[36].ifaceName = 'IPlaneCrew'
Handlers.handler[36].module = 'eventhandlers.upgradePlane.onChangePlaneCrewMember'
Handlers.handler[36].priority = 0
Handlers.handler[36].scope = 'server'
Handlers.handler.insert(37, None)
Handlers.handler[37] = Dummy()
Handlers.handler[37].eventName = []
Handlers.handler[37].eventName.insert(0, None)
Handlers.handler[37].eventName[0] = 'edit'
Handlers.handler[37].ifaceName = 'IPlaneCrew'
Handlers.handler[37].module = 'eventhandlers.planeCrewEventHandler.onEditPlaneCrew'
Handlers.handler[37].priority = 0
Handlers.handler[37].scope = 'client'
Handlers.handler.insert(38, None)
Handlers.handler[38] = Dummy()
Handlers.handler[38].eventName = []
Handlers.handler[38].eventName.insert(0, None)
Handlers.handler[38].eventName[0] = 'settocache'
Handlers.handler[38].ifaceName = 'IPlaneCrew'
Handlers.handler[38].module = 'eventhandlers.planeCrewEventHandler.onSetToCachePlaneCrew'
Handlers.handler[38].priority = 0
Handlers.handler[38].scope = 'client'
Handlers.handler.insert(39, None)
Handlers.handler[39] = Dummy()
Handlers.handler[39].eventName = []
Handlers.handler[39].eventName.insert(0, None)
Handlers.handler[39].eventName[0] = 'view_error'
Handlers.handler[39].eventName.insert(1, None)
Handlers.handler[39].eventName[1] = 'add_error'
Handlers.handler[39].eventName.insert(2, None)
Handlers.handler[39].eventName[2] = 'delete_error'
Handlers.handler[39].eventName.insert(3, None)
Handlers.handler[39].eventName[3] = 'edit_error'
Handlers.handler[39].ifaceName = 'IInterface'
Handlers.handler[39].module = 'eventhandlers.errorCommonHandlers.onNotFound'
Handlers.handler[39].priority = 0
Handlers.handler[39].scope = 'server'
Handlers.handler.insert(40, None)
Handlers.handler[40] = Dummy()
Handlers.handler[40].eventName = []
Handlers.handler[40].eventName.insert(0, None)
Handlers.handler[40].eventName[0] = 'view_error'
Handlers.handler[40].eventName.insert(1, None)
Handlers.handler[40].eventName[1] = 'add_error'
Handlers.handler[40].eventName.insert(2, None)
Handlers.handler[40].eventName[2] = 'delete_error'
Handlers.handler[40].eventName.insert(3, None)
Handlers.handler[40].eventName[3] = 'edit_error'
Handlers.handler[40].ifaceName = 'ISquadMember'
Handlers.handler[40].module = 'eventhandlers.errorSquadMemberHandlers.onNotFound'
Handlers.handler[40].priority = 0
Handlers.handler[40].scope = 'server'
Handlers.handler.insert(41, None)
Handlers.handler[41] = Dummy()
Handlers.handler[41].eventName = []
Handlers.handler[41].eventName.insert(0, None)
Handlers.handler[41].eventName[0] = 'view'
Handlers.handler[41].ifaceName = 'IPlayerSummaryStats'
Handlers.handler[41].module = 'eventhandlers.IPlayerStatsEventHandler.onPlayerStatsView'
Handlers.handler[41].priority = 0
Handlers.handler[41].scope = 'client'
Handlers.handler.insert(42, None)
Handlers.handler[42] = Dummy()
Handlers.handler[42].eventName = []
Handlers.handler[42].eventName.insert(0, None)
Handlers.handler[42].eventName[0] = 'edit'
Handlers.handler[42].ifaceName = 'ICrewMember'
Handlers.handler[42].module = 'eventhandlers.crewMemberEventHandler.onEditCrewMember'
Handlers.handler[42].priority = 0
Handlers.handler[42].scope = 'client'
Handlers.handler.insert(43, None)
Handlers.handler[43] = Dummy()
Handlers.handler[43].eventName = []
Handlers.handler[43].eventName.insert(0, None)
Handlers.handler[43].eventName[0] = 'settocache'
Handlers.handler[43].ifaceName = 'ICrewMember'
Handlers.handler[43].module = 'eventhandlers.crewMemberEventHandler.onSetToCacheCrewMember'
Handlers.handler[43].priority = 0
Handlers.handler[43].scope = 'client'
Handlers.handler.insert(44, None)
Handlers.handler[44] = Dummy()
Handlers.handler[44].eventName = []
Handlers.handler[44].eventName.insert(0, None)
Handlers.handler[44].eventName[0] = 'edit'
Handlers.handler[44].ifaceName = 'IQuestList'
Handlers.handler[44].module = 'eventhandlers.onChangedQuestList.onChangedQuestList'
Handlers.handler[44].priority = 0
Handlers.handler[44].scope = 'client'
Handlers.handler.insert(45, None)
Handlers.handler[45] = Dummy()
Handlers.handler[45].eventName = []
Handlers.handler[45].eventName.insert(0, None)
Handlers.handler[45].eventName[0] = 'edit'
Handlers.handler[45].ifaceName = 'IExperience'
Handlers.handler[45].module = 'eventhandlers.onChangeExperience.onChangeExperience'
Handlers.handler[45].priority = 0
Handlers.handler[45].scope = 'client'
Handlers.handler.insert(46, None)
Handlers.handler[46] = Dummy()
Handlers.handler[46].eventName = []
Handlers.handler[46].eventName.insert(0, None)
Handlers.handler[46].eventName[0] = 'edit'
Handlers.handler[46].eventName.insert(1, None)
Handlers.handler[46].eventName[1] = 'view'
Handlers.handler[46].ifaceName = 'IRent'
Handlers.handler[46].module = 'eventhandlers.onRentEvent.onRentEvent'
Handlers.handler[46].priority = 0
Handlers.handler[46].scope = 'client'
Handlers.handler.insert(47, None)
Handlers.handler[47] = Dummy()
Handlers.handler[47].eventName = []
Handlers.handler[47].eventName.insert(0, None)
Handlers.handler[47].eventName[0] = 'delete'
Handlers.handler[47].ifaceName = 'IRequestsLocker'
Handlers.handler[47].module = 'eventhandlers.onRequestsLocker.onRequestsLocker'
Handlers.handler[47].priority = 0
Handlers.handler[47].scope = 'client'
Handlers.handler.insert(48, None)
Handlers.handler[48] = Dummy()
Handlers.handler[48].eventName = []
Handlers.handler[48].eventName.insert(0, None)
Handlers.handler[48].eventName[0] = 'edit'
Handlers.handler[48].eventName.insert(1, None)
Handlers.handler[48].eventName[1] = 'view'
Handlers.handler[48].ifaceName = 'IGameModesParams'
Handlers.handler[48].module = 'eventhandlers.onGameModesParams.onGameModesParams'
Handlers.handler[48].priority = 0
Handlers.handler[48].scope = 'client'
Handlers.handler.insert(49, None)
Handlers.handler[49] = Dummy()
Handlers.handler[49].eventName = []
Handlers.handler[49].eventName.insert(0, None)
Handlers.handler[49].eventName[0] = 'edit'
Handlers.handler[49].ifaceName = 'IIGR'
Handlers.handler[49].module = 'eventhandlers.onIGRChanged.onIGRChanged'
Handlers.handler[49].priority = 0
Handlers.handler[49].scope = 'client'
Handlers.handler.insert(50, None)
Handlers.handler[50] = Dummy()
Handlers.handler[50].eventName = []
Handlers.handler[50].eventName.insert(0, None)
Handlers.handler[50].eventName[0] = 'edit'
Handlers.handler[50].eventName.insert(1, None)
Handlers.handler[50].eventName[1] = 'view'
Handlers.handler[50].ifaceName = 'IClanMembers'
Handlers.handler[50].module = 'eventhandlers.clanEvents.onClanMembersChanged'
Handlers.handler[50].priority = 0
Handlers.handler[50].scope = 'client'
Handlers.handler.insert(51, None)
Handlers.handler[51] = Dummy()
Handlers.handler[51].eventName = []
Handlers.handler[51].eventName.insert(0, None)
Handlers.handler[51].eventName[0] = 'edit'
Handlers.handler[51].eventName.insert(1, None)
Handlers.handler[51].eventName[1] = 'view'
Handlers.handler[51].ifaceName = 'IClanMember'
Handlers.handler[51].module = 'eventhandlers.clanEvents.onClanMemberInfo'
Handlers.handler[51].priority = 0
Handlers.handler[51].scope = 'client'
Handlers.handler.insert(52, None)
Handlers.handler[52] = Dummy()
Handlers.handler[52].eventName = []
Handlers.handler[52].eventName.insert(0, None)
Handlers.handler[52].eventName[0] = 'view'
Handlers.handler[52].eventName.insert(1, None)
Handlers.handler[52].eventName[1] = 'edit'
Handlers.handler[52].ifaceName = 'IClanMotto'
Handlers.handler[52].module = 'eventhandlers.clanEvents.onClanMotto'
Handlers.handler[52].priority = 0
Handlers.handler[52].scope = 'client'
Handlers.handler.insert(53, None)
Handlers.handler[53] = Dummy()
Handlers.handler[53].eventName = []
Handlers.handler[53].eventName.insert(0, None)
Handlers.handler[53].eventName[0] = 'edit'
Handlers.handler[53].eventName.insert(1, None)
Handlers.handler[53].eventName[1] = 'view'
Handlers.handler[53].ifaceName = 'IClanInfoShort'
Handlers.handler[53].module = 'eventhandlers.clanEvents.onClanShortInfo'
Handlers.handler[53].priority = 0
Handlers.handler[53].scope = 'client'
Handlers.handler.insert(54, None)
Handlers.handler[54] = Dummy()
Handlers.handler[54].eventName = []
Handlers.handler[54].eventName.insert(0, None)
Handlers.handler[54].eventName[0] = 'edit'
Handlers.handler[54].ifaceName = 'IHangarSpacesHash'
Handlers.handler[54].module = 'eventhandlers.onHangarSpacesHashChanged.onHangarSpacesHashChanged'
Handlers.handler[54].priority = 0
Handlers.handler[54].scope = 'client'
Handlers.handler.insert(55, None)
Handlers.handler[55] = Dummy()
Handlers.handler[55].eventName = []
Handlers.handler[55].eventName.insert(0, None)
Handlers.handler[55].eventName[0] = 'view'
Handlers.handler[55].ifaceName = 'IQuestSelectConsist'
Handlers.handler[55].module = 'eventhandlers.questEvents.onQuestSelectConsist'
Handlers.handler[55].priority = 0
Handlers.handler[55].scope = 'client'
Handlers.handler.insert(56, None)
Handlers.handler[56] = Dummy()
Handlers.handler[56].eventName = []
Handlers.handler[56].eventName.insert(0, None)
Handlers.handler[56].eventName[0] = 'view'
Handlers.handler[56].ifaceName = 'IQuestDescription'
Handlers.handler[56].module = 'eventhandlers.questEvents.onQuestDescription'
Handlers.handler[56].priority = 0
Handlers.handler[56].scope = 'client'
Handlers.handler.insert(57, None)
Handlers.handler[57] = Dummy()
Handlers.handler[57].eventName = []
Handlers.handler[57].eventName.insert(0, None)
Handlers.handler[57].eventName[0] = 'view'
Handlers.handler[57].ifaceName = 'IQuestResults'
Handlers.handler[57].module = 'eventhandlers.questEvents.onQuestResults'
Handlers.handler[57].priority = 0
Handlers.handler[57].scope = 'client'
Handlers.handler.insert(58, None)
Handlers.handler[58] = Dummy()
Handlers.handler[58].eventName = []
Handlers.handler[58].eventName.insert(0, None)
Handlers.handler[58].eventName[0] = 'view'
Handlers.handler[58].eventName.insert(1, None)
Handlers.handler[58].eventName[1] = 'edit'
Handlers.handler[58].eventName.insert(2, None)
Handlers.handler[58].eventName[2] = 'delete'
Handlers.handler[58].ifaceName = 'IPlaneBirthday'
Handlers.handler[58].module = 'eventhandlers.planeBirthdayEvents.onPlaneBirthdayChanged'
Handlers.handler[58].priority = 0
Handlers.handler[58].scope = 'client'
Handlers.handler.insert(59, None)
Handlers.handler[59] = Dummy()
Handlers.handler[59].eventName = []
Handlers.handler[59].eventName.insert(0, None)
Handlers.handler[59].eventName[0] = 'edit'
Handlers.handler[59].ifaceName = 'IActiveEvents'
Handlers.handler[59].module = 'eventhandlers.serverEvents.onEventsChanged'
Handlers.handler[59].priority = 0
Handlers.handler[59].scope = 'client'
Handlers.handler.insert(60, None)
Handlers.handler[60] = Dummy()
Handlers.handler[60].eventName = []
Handlers.handler[60].eventName.insert(0, None)
Handlers.handler[60].eventName[0] = 'add_prediction'
Handlers.handler[60].ifaceName = 'IClientPrediction'
Handlers.handler[60].module = 'eventhandlers.predictionEvents.onAddPrediction'
Handlers.handler[60].priority = 0
Handlers.handler[60].scope = 'client'
Handlers.handler.insert(61, None)
Handlers.handler[61] = Dummy()
Handlers.handler[61].eventName = []
Handlers.handler[61].eventName.insert(0, None)
Handlers.handler[61].eventName[0] = 'edit'
Handlers.handler[61].ifaceName = 'IWarActionState'
Handlers.handler[61].module = 'eventhandlers.EventWarAction.onStateEdit'
Handlers.handler[61].priority = 0
Handlers.handler[61].scope = 'client'
Handlers.handler.insert(62, None)
Handlers.handler[62] = Dummy()
Handlers.handler[62].eventName = []
Handlers.handler[62].eventName.insert(0, None)
Handlers.handler[62].eventName[0] = 'view'
Handlers.handler[62].eventName.insert(1, None)
Handlers.handler[62].eventName[1] = 'edit'
Handlers.handler[62].ifaceName = 'IWarActionForce'
Handlers.handler[62].module = 'eventhandlers.EventWarAction.onWarActionForce'
Handlers.handler[62].priority = 0
Handlers.handler[62].scope = 'client'
Handlers.handler.insert(63, None)
Handlers.handler[63] = Dummy()
Handlers.handler[63].eventName = []
Handlers.handler[63].eventName.insert(0, None)
Handlers.handler[63].eventName[0] = 'edit'
Handlers.handler[63].ifaceName = 'IFemalePilotPackList'
Handlers.handler[63].module = 'eventhandlers.femalePilotEventHandlers.onIFemalePilotPackListEdit'
Handlers.handler[63].priority = 0
Handlers.handler[63].scope = 'server'
Handlers.handler.insert(64, None)
Handlers.handler[64] = Dummy()
Handlers.handler[64].eventName = []
Handlers.handler[64].eventName.insert(0, None)
Handlers.handler[64].eventName[0] = 'edit'
Handlers.handler[64].ifaceName = 'IStatus'
Handlers.handler[64].module = 'eventhandlers.femalePilotEventHandlers.onChangedPlaneStatus'
Handlers.handler[64].priority = 0
Handlers.handler[64].scope = 'server'
Handlers.handler.insert(65, None)
Handlers.handler[65] = Dummy()
Handlers.handler[65].eventName = []
Handlers.handler[65].eventName.insert(0, None)
Handlers.handler[65].eventName[0] = 'buy'
Handlers.handler[65].ifaceName = 'IPack'
Handlers.handler[65].module = 'eventhandlers.femalePilotEventHandlers.onChangedIPackStatus'
Handlers.handler[65].priority = 0
Handlers.handler[65].scope = 'server'
Handlers.handler.insert(66, None)
Handlers.handler[66] = Dummy()
Handlers.handler[66].eventName = []
Handlers.handler[66].eventName.insert(0, None)
Handlers.handler[66].eventName[0] = 'add'
Handlers.handler[66].ifaceName = 'IPack'
Handlers.handler[66].module = 'eventhandlers.femalePilotEventHandlers.onChangedIPackStatus'
Handlers.handler[66].priority = 0
Handlers.handler[66].scope = 'server'