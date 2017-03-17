# Embedded file name: scripts/common/exchangeapi/_adapters.py
import Math
import math
import consts
true = True
false = False

class Dummy():
    pass


isServerDatabase = False

class AMMO_TYPE():
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


Adapters = Dummy()
Adapters.adpater = []
Adapters.adpater.insert(0, None)
Adapters.adpater[0] = Dummy()
Adapters.adpater[0].ifacename = 'ISquad'
Adapters.adpater[0].module = 'adapters.ISquadAdapter.ISquadAdapter'
Adapters.adpater[0].obtype = []
Adapters.adpater[0].obtype.insert(0, None)
Adapters.adpater[0].obtype[0] = 'squad'
Adapters.adpater.insert(1, None)
Adapters.adpater[1] = Dummy()
Adapters.adpater[1].ifacename = 'ISquadMember'
Adapters.adpater[1].module = 'adapters.ISquadMemberAdapter.ISquadMemberAdapter'
Adapters.adpater[1].obtype = []
Adapters.adpater[1].obtype.insert(0, None)
Adapters.adpater[1].obtype[0] = 'squadmember'
Adapters.adpater.insert(2, None)
Adapters.adpater[2] = Dummy()
Adapters.adpater[2].ifacename = 'ISquadMember'
Adapters.adpater[2].module = 'adapters.ISquadMemberAdapter.ISquadMemberICAdapter'
Adapters.adpater[2].obtype = []
Adapters.adpater[2].obtype.insert(0, None)
Adapters.adpater[2].obtype[0] = 'squadmember'
Adapters.adpater[2].obtype.insert(1, None)
Adapters.adpater[2].obtype[1] = 'periphery'
Adapters.adpater.insert(3, None)
Adapters.adpater[3] = Dummy()
Adapters.adpater[3].ifacename = 'ISquadInvitation'
Adapters.adpater[3].module = 'adapters.ISquadInvitationAdapter.ISquadInvitationAdapter'
Adapters.adpater[3].obtype = []
Adapters.adpater[3].obtype.insert(0, None)
Adapters.adpater[3].obtype[0] = 'squadmember'
Adapters.adpater.insert(4, None)
Adapters.adpater[4] = Dummy()
Adapters.adpater[4].ifacename = 'ISquadInvitation'
Adapters.adpater[4].module = 'adapters.ISquadInvitationAdapter.ISquadInvitationICAdapter'
Adapters.adpater[4].obtype = []
Adapters.adpater[4].obtype.insert(0, None)
Adapters.adpater[4].obtype[0] = 'squadmember'
Adapters.adpater[4].obtype.insert(1, None)
Adapters.adpater[4].obtype[1] = 'periphery'
Adapters.adpater.insert(5, None)
Adapters.adpater[5] = Dummy()
Adapters.adpater[5].ifacename = 'IBattleState'
Adapters.adpater[5].module = 'adapters.ISquadBattleStateAdapter.ISquadBattleStateAdapter'
Adapters.adpater[5].obtype = []
Adapters.adpater[5].obtype.insert(0, None)
Adapters.adpater[5].obtype[0] = 'squad'
Adapters.adpater.insert(6, None)
Adapters.adpater[6] = Dummy()
Adapters.adpater[6].ifacename = 'IBattleState'
Adapters.adpater[6].module = 'adapters.IBattleStateAdapter.IBattleStateAdapter'
Adapters.adpater[6].obtype = []
Adapters.adpater[6].obtype.insert(0, None)
Adapters.adpater[6].obtype[0] = 'account'
Adapters.adpater.insert(7, None)
Adapters.adpater[7] = Dummy()
Adapters.adpater[7].ifacename = 'ISquadChatChannel'
Adapters.adpater[7].module = 'adapters.ISquadChatChannel.ISquadChatChannel'
Adapters.adpater[7].obtype = []
Adapters.adpater[7].obtype.insert(0, None)
Adapters.adpater[7].obtype[0] = 'squad'
Adapters.adpater.insert(8, None)
Adapters.adpater[8] = Dummy()
Adapters.adpater[8].ifacename = 'ICurrentPatch'
Adapters.adpater[8].module = 'adapters.ICurrentPatchAdapter.ICurrentPatchAdapter'
Adapters.adpater[8].obtype = []
Adapters.adpater[8].obtype.insert(0, None)
Adapters.adpater[8].obtype[0] = 'patch'
Adapters.adpater.insert(9, None)
Adapters.adpater[9] = Dummy()
Adapters.adpater[9].ifacename = 'IPatch'
Adapters.adpater[9].module = 'adapters.IPatchAdapter.IPatchAdapter'
Adapters.adpater[9].obtype = []
Adapters.adpater[9].obtype.insert(0, None)
Adapters.adpater[9].obtype[0] = 'patch'
Adapters.adpater.insert(10, None)
Adapters.adpater[10] = Dummy()
Adapters.adpater[10].ifacename = 'IPatch'
Adapters.adpater[10].module = 'adapters.IPatchAdapter.IPatchPlanePricesAdapter'
Adapters.adpater[10].obtype = []
Adapters.adpater[10].obtype.insert(0, None)
Adapters.adpater[10].obtype[0] = 'patch'
Adapters.adpater[10].obtype.insert(1, None)
Adapters.adpater[10].obtype[1] = 'plane'
Adapters.adpater.insert(11, None)
Adapters.adpater[11] = Dummy()
Adapters.adpater[11].ifacename = 'IPatch'
Adapters.adpater[11].module = 'adapters.IPatchAdapter.IPatchConsumablePricesAdapter'
Adapters.adpater[11].obtype = []
Adapters.adpater[11].obtype.insert(0, None)
Adapters.adpater[11].obtype[0] = 'patch'
Adapters.adpater[11].obtype.insert(1, None)
Adapters.adpater[11].obtype[1] = 'consumable'
Adapters.adpater.insert(12, None)
Adapters.adpater[12] = Dummy()
Adapters.adpater[12].ifacename = 'IPatch'
Adapters.adpater[12].module = 'adapters.IPatchAdapter.IPatchEquipmentPricesAdapter'
Adapters.adpater[12].obtype = []
Adapters.adpater[12].obtype.insert(0, None)
Adapters.adpater[12].obtype[0] = 'patch'
Adapters.adpater[12].obtype.insert(1, None)
Adapters.adpater[12].obtype[1] = 'equipment'
Adapters.adpater.insert(13, None)
Adapters.adpater[13] = Dummy()
Adapters.adpater[13].ifacename = 'IPatch'
Adapters.adpater[13].module = 'adapters.IPatchAdapter.IPatchAmmobeltPricesAdapter'
Adapters.adpater[13].obtype = []
Adapters.adpater[13].obtype.insert(0, None)
Adapters.adpater[13].obtype[0] = 'patch'
Adapters.adpater[13].obtype.insert(1, None)
Adapters.adpater[13].obtype[1] = 'ammobelt'
Adapters.adpater.insert(14, None)
Adapters.adpater[14] = Dummy()
Adapters.adpater[14].ifacename = 'IPatch'
Adapters.adpater[14].module = 'adapters.IPatchAdapter.IPatchGoldPriceAdapter'
Adapters.adpater[14].obtype = []
Adapters.adpater[14].obtype.insert(0, None)
Adapters.adpater[14].obtype[0] = 'patch'
Adapters.adpater[14].obtype.insert(1, None)
Adapters.adpater[14].obtype[1] = 'goldPrice'
Adapters.adpater.insert(15, None)
Adapters.adpater[15] = Dummy()
Adapters.adpater[15].ifacename = 'ILastMessages'
Adapters.adpater[15].module = 'adapters.ILastMessagesAdapter.ILastMessagesAdapter'
Adapters.adpater[15].obtype = []
Adapters.adpater[15].obtype.insert(0, None)
Adapters.adpater[15].obtype[0] = 'account'
Adapters.adpater.insert(16, None)
Adapters.adpater[16] = Dummy()
Adapters.adpater[16].ifacename = 'IMessage'
Adapters.adpater[16].module = 'adapters.IMessageAdapter.IMessageAdapter'
Adapters.adpater[16].obtype = []
Adapters.adpater[16].obtype.insert(0, None)
Adapters.adpater[16].obtype[0] = 'message'
Adapters.adpater.insert(17, None)
Adapters.adpater[17] = Dummy()
Adapters.adpater[17].ifacename = 'IMessage'
Adapters.adpater[17].module = 'adapters.IMessageAdapter.IMessageUIAdapter'
Adapters.adpater[17].obtype = []
Adapters.adpater[17].obtype.insert(0, None)
Adapters.adpater[17].obtype[0] = 'uimessage'
Adapters.adpater.insert(18, None)
Adapters.adpater[18] = Dummy()
Adapters.adpater[18].ifacename = 'IMessageSession'
Adapters.adpater[18].module = 'adapters.IMessageSessionAdapter.IMessageSessionAdapter'
Adapters.adpater[18].obtype = []
Adapters.adpater[18].obtype.insert(0, None)
Adapters.adpater[18].obtype[0] = 'account'
Adapters.adpater.insert(19, None)
Adapters.adpater[19] = Dummy()
Adapters.adpater[19].ifacename = 'IMessageAction'
Adapters.adpater[19].module = 'adapters.IMessageActionAdapter.IMessageActionAdapter'
Adapters.adpater[19].obtype = []
Adapters.adpater[19].obtype.insert(0, None)
Adapters.adpater[19].obtype[0] = 'messageAction'
Adapters.adpater.insert(20, None)
Adapters.adpater[20] = Dummy()
Adapters.adpater[20].ifacename = 'IPlanes'
Adapters.adpater[20].module = 'adapters.IPlanesAdapter.IPlanesAdapter'
Adapters.adpater[20].obtype = []
Adapters.adpater[20].obtype.insert(0, None)
Adapters.adpater[20].obtype[0] = 'account'
Adapters.adpater.insert(21, None)
Adapters.adpater[21] = Dummy()
Adapters.adpater[21].ifacename = 'IPlanes'
Adapters.adpater[21].module = 'adapters.IPlanesAdapter.IPlanesByEquipmentAdapter'
Adapters.adpater[21].obtype = []
Adapters.adpater[21].obtype.insert(0, None)
Adapters.adpater[21].obtype[0] = 'equipment'
Adapters.adpater.insert(22, None)
Adapters.adpater[22] = Dummy()
Adapters.adpater[22].ifacename = 'IClass'
Adapters.adpater[22].module = 'adapters.IClassPlaneAdapter.IClassPlaneAdapter'
Adapters.adpater[22].obtype = []
Adapters.adpater[22].obtype.insert(0, None)
Adapters.adpater[22].obtype[0] = 'plane'
Adapters.adpater.insert(23, None)
Adapters.adpater[23] = Dummy()
Adapters.adpater[23].ifacename = 'IStatus'
Adapters.adpater[23].module = 'adapters.IStatusPlaneAdapter.IStatusPlaneAdapter'
Adapters.adpater[23].obtype = []
Adapters.adpater[23].obtype.insert(0, None)
Adapters.adpater[23].obtype[0] = 'plane'
Adapters.adpater.insert(24, None)
Adapters.adpater[24] = Dummy()
Adapters.adpater[24].ifacename = 'IStatus'
Adapters.adpater[24].module = 'adapters.IStatusShellAdapter.IStatusShellAdapter'
Adapters.adpater[24].obtype = []
Adapters.adpater[24].obtype.insert(0, None)
Adapters.adpater[24].obtype[0] = 'bomb'
Adapters.adpater.insert(25, None)
Adapters.adpater[25] = Dummy()
Adapters.adpater[25].ifacename = 'IStatus'
Adapters.adpater[25].module = 'adapters.IStatusShellAdapter.IStatusShellAdapter'
Adapters.adpater[25].obtype = []
Adapters.adpater[25].obtype.insert(0, None)
Adapters.adpater[25].obtype[0] = 'rocket'
Adapters.adpater.insert(26, None)
Adapters.adpater[26] = Dummy()
Adapters.adpater[26].ifacename = 'IStatus'
Adapters.adpater[26].module = 'adapters.IStatusShellAdapter.IStatusShellAdapter'
Adapters.adpater[26].obtype = []
Adapters.adpater[26].obtype.insert(0, None)
Adapters.adpater[26].obtype[0] = 'upgrade'
Adapters.adpater.insert(27, None)
Adapters.adpater[27] = Dummy()
Adapters.adpater[27].ifacename = 'IStatus'
Adapters.adpater[27].module = 'adapters.IStatusAccountAdapter.IStatusAccountAdapter'
Adapters.adpater[27].obtype = []
Adapters.adpater[27].obtype.insert(0, None)
Adapters.adpater[27].obtype[0] = 'account'
Adapters.adpater.insert(28, None)
Adapters.adpater[28] = Dummy()
Adapters.adpater[28].ifacename = 'IPrice'
Adapters.adpater[28].module = 'adapters.IPricePlaneAdapter.IPricePlaneAdapter'
Adapters.adpater[28].obtype = []
Adapters.adpater[28].obtype.insert(0, None)
Adapters.adpater[28].obtype[0] = 'plane'
Adapters.adpater.insert(29, None)
Adapters.adpater[29] = Dummy()
Adapters.adpater[29].ifacename = 'IPrice'
Adapters.adpater[29].module = 'adapters.IPriceUpgradeAdapter.IPriceUpgradeAdapter'
Adapters.adpater[29].obtype = []
Adapters.adpater[29].obtype.insert(0, None)
Adapters.adpater[29].obtype[0] = 'upgrade'
Adapters.adpater.insert(30, None)
Adapters.adpater[30] = Dummy()
Adapters.adpater[30].ifacename = 'IPrice'
Adapters.adpater[30].module = 'adapters.IPriceSlotAdapter.IPriceSlotAdapter'
Adapters.adpater[30].obtype = []
Adapters.adpater[30].obtype.insert(0, None)
Adapters.adpater[30].obtype[0] = 'slot'
Adapters.adpater.insert(31, None)
Adapters.adpater[31] = Dummy()
Adapters.adpater[31].ifacename = 'ISellPrice'
Adapters.adpater[31].module = 'adapters.ISellPricePlaneAdapter.ISellPricePlaneAdapter'
Adapters.adpater[31].obtype = []
Adapters.adpater[31].obtype.insert(0, None)
Adapters.adpater[31].obtype[0] = 'plane'
Adapters.adpater.insert(32, None)
Adapters.adpater[32] = Dummy()
Adapters.adpater[32].ifacename = 'ISellPrice'
Adapters.adpater[32].module = 'adapters.ISellPriceUpgradeAdapter.ISellPriceUpgradeAdapter'
Adapters.adpater[32].obtype = []
Adapters.adpater[32].obtype.insert(0, None)
Adapters.adpater[32].obtype[0] = 'upgrade'
Adapters.adpater.insert(33, None)
Adapters.adpater[33] = Dummy()
Adapters.adpater[33].ifacename = 'IType'
Adapters.adpater[33].module = 'adapters.ITypePlaneAdapter.ITypePlaneAdapter'
Adapters.adpater[33].obtype = []
Adapters.adpater[33].obtype.insert(0, None)
Adapters.adpater[33].obtype[0] = 'plane'
Adapters.adpater.insert(34, None)
Adapters.adpater[34] = Dummy()
Adapters.adpater[34].ifacename = 'INation'
Adapters.adpater[34].module = 'adapters.INationAdapter.INationPlaneAdapter'
Adapters.adpater[34].obtype = []
Adapters.adpater[34].obtype.insert(0, None)
Adapters.adpater[34].obtype[0] = 'plane'
Adapters.adpater.insert(35, None)
Adapters.adpater[35] = Dummy()
Adapters.adpater[35].ifacename = 'INation'
Adapters.adpater[35].module = 'adapters.INationAdapter.INationAmmoBeltAdapter'
Adapters.adpater[35].obtype = []
Adapters.adpater[35].obtype.insert(0, None)
Adapters.adpater[35].obtype[0] = 'ammobelt'
Adapters.adpater.insert(36, None)
Adapters.adpater[36] = Dummy()
Adapters.adpater[36].ifacename = 'INation'
Adapters.adpater[36].module = 'adapters.INationAdapter.INationShellAdapter'
Adapters.adpater[36].obtype = []
Adapters.adpater[36].obtype.insert(0, None)
Adapters.adpater[36].obtype[0] = 'bomb'
Adapters.adpater.insert(37, None)
Adapters.adpater[37] = Dummy()
Adapters.adpater[37].ifacename = 'INation'
Adapters.adpater[37].module = 'adapters.INationAdapter.INationShellAdapter'
Adapters.adpater[37].obtype = []
Adapters.adpater[37].obtype.insert(0, None)
Adapters.adpater[37].obtype[0] = 'rocket'
Adapters.adpater.insert(38, None)
Adapters.adpater[38] = Dummy()
Adapters.adpater[38].ifacename = 'INation'
Adapters.adpater[38].module = 'adapters.INationAdapter.INationUpgradeAdapter'
Adapters.adpater[38].obtype = []
Adapters.adpater[38].obtype.insert(0, None)
Adapters.adpater[38].obtype[0] = 'upgrade'
Adapters.adpater.insert(39, None)
Adapters.adpater[39] = Dummy()
Adapters.adpater[39].ifacename = 'INationList'
Adapters.adpater[39].module = 'adapters.INationAdapter.INationListAdapter'
Adapters.adpater[39].obtype = []
Adapters.adpater[39].obtype.insert(0, None)
Adapters.adpater[39].obtype[0] = 'consumable'
Adapters.adpater.insert(40, None)
Adapters.adpater[40] = Dummy()
Adapters.adpater[40].ifacename = 'INationList'
Adapters.adpater[40].module = 'adapters.INationAdapter.INationListAdapter'
Adapters.adpater[40].obtype = []
Adapters.adpater[40].obtype.insert(0, None)
Adapters.adpater[40].obtype[0] = 'equipment'
Adapters.adpater.insert(41, None)
Adapters.adpater[41] = Dummy()
Adapters.adpater[41].ifacename = 'IPlaneDescription'
Adapters.adpater[41].module = 'adapters.IPlaneDescriptionAdapter.IPlaneDescriptionAdapter'
Adapters.adpater[41].obtype = []
Adapters.adpater[41].obtype.insert(0, None)
Adapters.adpater[41].obtype[0] = 'plane'
Adapters.adpater.insert(42, None)
Adapters.adpater[42] = Dummy()
Adapters.adpater[42].ifacename = 'IPlanePreset'
Adapters.adpater[42].module = 'adapters.IPlanePresetAdapter.IPlanePresetAdapter'
Adapters.adpater[42].obtype = []
Adapters.adpater[42].obtype.insert(0, None)
Adapters.adpater[42].obtype[0] = 'planePreset'
Adapters.adpater.insert(43, None)
Adapters.adpater[43] = Dummy()
Adapters.adpater[43].ifacename = 'IModuleDescription'
Adapters.adpater[43].module = 'adapters.IModuleDescriptionAdapter.IModuleDescriptionAdapter'
Adapters.adpater[43].obtype = []
Adapters.adpater[43].obtype.insert(0, None)
Adapters.adpater[43].obtype[0] = 'upgrade'
Adapters.adpater[43].obtype.insert(1, None)
Adapters.adpater[43].obtype[1] = 'measurementSystem'
Adapters.adpater.insert(44, None)
Adapters.adpater[44] = Dummy()
Adapters.adpater[44].ifacename = 'IModuleDescription'
Adapters.adpater[44].module = 'adapters.IModuleDescriptionAdapter.IModuleDescriptionAdapter'
Adapters.adpater[44].obtype = []
Adapters.adpater[44].obtype.insert(0, None)
Adapters.adpater[44].obtype[0] = 'upgrade'
Adapters.adpater[44].obtype.insert(1, None)
Adapters.adpater[44].obtype[1] = 'plane'
Adapters.adpater[44].obtype.insert(2, None)
Adapters.adpater[44].obtype[2] = 'measurementSystem'
Adapters.adpater.insert(45, None)
Adapters.adpater[45] = Dummy()
Adapters.adpater[45].ifacename = 'IModuleDescription'
Adapters.adpater[45].module = 'adapters.IModuleDescriptionAdapter.IModuleDescriptionAdapter'
Adapters.adpater[45].obtype = []
Adapters.adpater[45].obtype.insert(0, None)
Adapters.adpater[45].obtype[0] = 'upgrade'
Adapters.adpater[45].obtype.insert(1, None)
Adapters.adpater[45].obtype[1] = 'weaponslot'
Adapters.adpater[45].obtype.insert(2, None)
Adapters.adpater[45].obtype[2] = 'weaponConfig'
Adapters.adpater[45].obtype.insert(3, None)
Adapters.adpater[45].obtype[3] = 'plane'
Adapters.adpater[45].obtype.insert(4, None)
Adapters.adpater[45].obtype[4] = 'measurementSystem'
Adapters.adpater.insert(46, None)
Adapters.adpater[46] = Dummy()
Adapters.adpater[46].ifacename = 'IModuleDescription'
Adapters.adpater[46].module = 'adapters.IModuleDescriptionAdapter.IModuleDescriptionAdapter'
Adapters.adpater[46].obtype = []
Adapters.adpater[46].obtype.insert(0, None)
Adapters.adpater[46].obtype[0] = 'upgrade'
Adapters.adpater[46].obtype.insert(1, None)
Adapters.adpater[46].obtype[1] = 'weaponslot'
Adapters.adpater[46].obtype.insert(2, None)
Adapters.adpater[46].obtype[2] = 'weaponConfig'
Adapters.adpater[46].obtype.insert(3, None)
Adapters.adpater[46].obtype[3] = 'upgrade'
Adapters.adpater[46].obtype.insert(4, None)
Adapters.adpater[46].obtype[4] = 'plane'
Adapters.adpater[46].obtype.insert(5, None)
Adapters.adpater[46].obtype[5] = 'measurementSystem'
Adapters.adpater.insert(47, None)
Adapters.adpater[47] = Dummy()
Adapters.adpater[47].ifacename = 'IConfigSpecs'
Adapters.adpater[47].module = 'adapters.IConfigSpecsAdapter.IConfigSpecsAdapter'
Adapters.adpater[47].obtype = []
Adapters.adpater[47].obtype.insert(0, None)
Adapters.adpater[47].obtype[0] = 'planePreset'
Adapters.adpater[47].obtype.insert(1, None)
Adapters.adpater[47].obtype[1] = 'measurementSystem'
Adapters.adpater.insert(48, None)
Adapters.adpater[48] = Dummy()
Adapters.adpater[48].ifacename = 'IConfigSpecs'
Adapters.adpater[48].module = 'adapters.IConfigSpecsAdapter.IConfigSpecsAdapter'
Adapters.adpater[48].obtype = []
Adapters.adpater[48].obtype.insert(0, None)
Adapters.adpater[48].obtype[0] = 'planePreset'
Adapters.adpater[48].obtype.insert(1, None)
Adapters.adpater[48].obtype[1] = 'planePreset'
Adapters.adpater[48].obtype.insert(2, None)
Adapters.adpater[48].obtype[2] = 'measurementSystem'
Adapters.adpater.insert(49, None)
Adapters.adpater[49] = Dummy()
Adapters.adpater[49].ifacename = 'IShortConfigSpecs'
Adapters.adpater[49].module = 'adapters.IShortConfigSpecsAdapter.IShortConfigSpecsAdapter'
Adapters.adpater[49].obtype = []
Adapters.adpater[49].obtype.insert(0, None)
Adapters.adpater[49].obtype[0] = 'planePreset'
Adapters.adpater.insert(50, None)
Adapters.adpater[50] = Dummy()
Adapters.adpater[50].ifacename = 'IInstalledGlobalID'
Adapters.adpater[50].module = 'adapters.IInstalledGlobalIDAdapter.IInstalledGlobalIDAdapter'
Adapters.adpater[50].obtype = []
Adapters.adpater[50].obtype.insert(0, None)
Adapters.adpater[50].obtype[0] = 'plane'
Adapters.adpater.insert(51, None)
Adapters.adpater[51] = Dummy()
Adapters.adpater[51].ifacename = 'ISuitableAmmoBelts'
Adapters.adpater[51].module = 'adapters.ISuitableAmmoBeltsAdapter.ISuitableAmmoBeltsAdapter'
Adapters.adpater[51].obtype = []
Adapters.adpater[51].obtype.insert(0, None)
Adapters.adpater[51].obtype[0] = 'plane'
Adapters.adpater[51].obtype.insert(1, None)
Adapters.adpater[51].obtype[1] = 'gun'
Adapters.adpater.insert(52, None)
Adapters.adpater[52] = Dummy()
Adapters.adpater[52].ifacename = 'IAmmoBeltDescription'
Adapters.adpater[52].module = 'adapters.IAmmoBeltDescriptionAdapter.IAmmoBeltDescriptionAdapter'
Adapters.adpater[52].obtype = []
Adapters.adpater[52].obtype.insert(0, None)
Adapters.adpater[52].obtype[0] = 'ammobelt'
Adapters.adpater.insert(53, None)
Adapters.adpater[53] = Dummy()
Adapters.adpater[53].ifacename = 'IPrice'
Adapters.adpater[53].module = 'adapters.IPriceUpgradeAdapter.IPriceUpgradeAdapter'
Adapters.adpater[53].obtype = []
Adapters.adpater[53].obtype.insert(0, None)
Adapters.adpater[53].obtype[0] = 'ammobelt'
Adapters.adpater.insert(54, None)
Adapters.adpater[54] = Dummy()
Adapters.adpater[54].ifacename = 'IPrice'
Adapters.adpater[54].module = 'adapters.IPriceUpgradeAdapter.IPriceUpgradeAdapter'
Adapters.adpater[54].obtype = []
Adapters.adpater[54].obtype.insert(0, None)
Adapters.adpater[54].obtype[0] = 'rocket'
Adapters.adpater.insert(55, None)
Adapters.adpater[55] = Dummy()
Adapters.adpater[55].ifacename = 'IPrice'
Adapters.adpater[55].module = 'adapters.IPriceUpgradeAdapter.IPriceUpgradeAdapter'
Adapters.adpater[55].obtype = []
Adapters.adpater[55].obtype.insert(0, None)
Adapters.adpater[55].obtype[0] = 'bomb'
Adapters.adpater.insert(56, None)
Adapters.adpater[56] = Dummy()
Adapters.adpater[56].ifacename = 'IPrice'
Adapters.adpater[56].module = 'adapters.IPriceUpgradeAdapter.IPriceUpgradeAdapter'
Adapters.adpater[56].obtype = []
Adapters.adpater[56].obtype.insert(0, None)
Adapters.adpater[56].obtype[0] = 'consumable'
Adapters.adpater.insert(57, None)
Adapters.adpater[57] = Dummy()
Adapters.adpater[57].ifacename = 'IPrice'
Adapters.adpater[57].module = 'adapters.IPriceUpgradeAdapter.IPriceUpgradeAdapter'
Adapters.adpater[57].obtype = []
Adapters.adpater[57].obtype.insert(0, None)
Adapters.adpater[57].obtype[0] = 'equipment'
Adapters.adpater.insert(58, None)
Adapters.adpater[58] = Dummy()
Adapters.adpater[58].ifacename = 'ISellPrice'
Adapters.adpater[58].module = 'adapters.ISellPriceUpgradeAdapter.ISellPriceUpgradeAdapter'
Adapters.adpater[58].obtype = []
Adapters.adpater[58].obtype.insert(0, None)
Adapters.adpater[58].obtype[0] = 'ammobelt'
Adapters.adpater.insert(59, None)
Adapters.adpater[59] = Dummy()
Adapters.adpater[59].ifacename = 'ISellPrice'
Adapters.adpater[59].module = 'adapters.ISellPriceUpgradeAdapter.ISellPriceUpgradeAdapter'
Adapters.adpater[59].obtype = []
Adapters.adpater[59].obtype.insert(0, None)
Adapters.adpater[59].obtype[0] = 'rocket'
Adapters.adpater.insert(60, None)
Adapters.adpater[60] = Dummy()
Adapters.adpater[60].ifacename = 'ISellPrice'
Adapters.adpater[60].module = 'adapters.ISellPriceUpgradeAdapter.ISellPriceUpgradeAdapter'
Adapters.adpater[60].obtype = []
Adapters.adpater[60].obtype.insert(0, None)
Adapters.adpater[60].obtype[0] = 'bomb'
Adapters.adpater.insert(61, None)
Adapters.adpater[61] = Dummy()
Adapters.adpater[61].ifacename = 'ISellPrice'
Adapters.adpater[61].module = 'adapters.ISellPriceUpgradeAdapter.ISellPriceUpgradeAdapter'
Adapters.adpater[61].obtype = []
Adapters.adpater[61].obtype.insert(0, None)
Adapters.adpater[61].obtype[0] = 'consumable'
Adapters.adpater.insert(62, None)
Adapters.adpater[62] = Dummy()
Adapters.adpater[62].ifacename = 'ISellPrice'
Adapters.adpater[62].module = 'adapters.ISellPriceUpgradeAdapter.ISellPriceUpgradeAdapter'
Adapters.adpater[62].obtype = []
Adapters.adpater[62].obtype.insert(0, None)
Adapters.adpater[62].obtype[0] = 'equipment'
Adapters.adpater.insert(63, None)
Adapters.adpater[63] = Dummy()
Adapters.adpater[63].ifacename = 'IDepot'
Adapters.adpater[63].module = 'adapters.IDepotAdapter.IDepotAdapter'
Adapters.adpater[63].obtype = []
Adapters.adpater[63].obtype.insert(0, None)
Adapters.adpater[63].obtype[0] = 'account'
Adapters.adpater.insert(64, None)
Adapters.adpater[64] = Dummy()
Adapters.adpater[64].ifacename = 'IDepot'
Adapters.adpater[64].module = 'adapters.IConfigPlaneAdapter.IConfigPlaneAdapter'
Adapters.adpater[64].obtype = []
Adapters.adpater[64].obtype.insert(0, None)
Adapters.adpater[64].obtype[0] = 'plane'
Adapters.adpater.insert(65, None)
Adapters.adpater[65] = Dummy()
Adapters.adpater[65].ifacename = 'IAvailableEquipment'
Adapters.adpater[65].module = 'adapters.IAvailableEquipmentAdapter.IAvailableEquipmentAdapter'
Adapters.adpater[65].obtype = []
Adapters.adpater[65].obtype.insert(0, None)
Adapters.adpater[65].obtype[0] = 'plane'
Adapters.adpater.insert(66, None)
Adapters.adpater[66] = Dummy()
Adapters.adpater[66].ifacename = 'IEquipment'
Adapters.adpater[66].module = 'adapters.IEquipmentAdapter.IEquipmentAdapter'
Adapters.adpater[66].obtype = []
Adapters.adpater[66].obtype.insert(0, None)
Adapters.adpater[66].obtype[0] = 'equipment'
Adapters.adpater.insert(67, None)
Adapters.adpater[67] = Dummy()
Adapters.adpater[67].ifacename = 'IInstalledAmmoBelt'
Adapters.adpater[67].module = 'adapters.IInstalledAmmoBeltAdapter.IInstalledAmmoBeltAdapter'
Adapters.adpater[67].obtype = []
Adapters.adpater[67].obtype.insert(0, None)
Adapters.adpater[67].obtype[0] = 'plane'
Adapters.adpater[67].obtype.insert(1, None)
Adapters.adpater[67].obtype[1] = 'weaponslot'
Adapters.adpater.insert(68, None)
Adapters.adpater[68] = Dummy()
Adapters.adpater[68].ifacename = 'IAvailableConsumables'
Adapters.adpater[68].module = 'adapters.IAvailableConsumablesAdapter.IAvailableConsumablesAdapter'
Adapters.adpater[68].obtype = []
Adapters.adpater[68].obtype.insert(0, None)
Adapters.adpater[68].obtype[0] = 'plane'
Adapters.adpater.insert(69, None)
Adapters.adpater[69] = Dummy()
Adapters.adpater[69].ifacename = 'IConsumable'
Adapters.adpater[69].module = 'adapters.IConsumableAdapter.IConsumableAdapter'
Adapters.adpater[69].obtype = []
Adapters.adpater[69].obtype.insert(0, None)
Adapters.adpater[69].obtype[0] = 'consumable'
Adapters.adpater.insert(70, None)
Adapters.adpater[70] = Dummy()
Adapters.adpater[70].ifacename = 'IAccountResources'
Adapters.adpater[70].module = 'adapters.IAccountResourcesAdapter.IAccountResourcesAdapter'
Adapters.adpater[70].obtype = []
Adapters.adpater[70].obtype.insert(0, None)
Adapters.adpater[70].obtype[0] = 'account'
Adapters.adpater.insert(71, None)
Adapters.adpater[71] = Dummy()
Adapters.adpater[71].ifacename = 'IGunDescription'
Adapters.adpater[71].module = 'adapters.IWeaponDescriptionAdapter.IGunDescriptionAdapter'
Adapters.adpater[71].obtype = []
Adapters.adpater[71].obtype.insert(0, None)
Adapters.adpater[71].obtype[0] = 'gun'
Adapters.adpater[71].obtype.insert(1, None)
Adapters.adpater[71].obtype[1] = 'measurementSystem'
Adapters.adpater.insert(72, None)
Adapters.adpater[72] = Dummy()
Adapters.adpater[72].ifacename = 'IInstalledGunSlots'
Adapters.adpater[72].module = 'adapters.IInstalledWeaponSlotsAdapter.IInstalledGunSlotsAdapter'
Adapters.adpater[72].obtype = []
Adapters.adpater[72].obtype.insert(0, None)
Adapters.adpater[72].obtype[0] = 'plane'
Adapters.adpater.insert(73, None)
Adapters.adpater[73] = Dummy()
Adapters.adpater[73].ifacename = 'IInstalledBombSlots'
Adapters.adpater[73].module = 'adapters.IInstalledWeaponSlotsAdapter.IInstalledBombSlotsAdapter'
Adapters.adpater[73].obtype = []
Adapters.adpater[73].obtype.insert(0, None)
Adapters.adpater[73].obtype[0] = 'plane'
Adapters.adpater.insert(74, None)
Adapters.adpater[74] = Dummy()
Adapters.adpater[74].ifacename = 'IInstalledRocketSlots'
Adapters.adpater[74].module = 'adapters.IInstalledWeaponSlotsAdapter.IInstalledRocketSlotsAdapter'
Adapters.adpater[74].obtype = []
Adapters.adpater[74].obtype.insert(0, None)
Adapters.adpater[74].obtype[0] = 'plane'
Adapters.adpater.insert(75, None)
Adapters.adpater[75] = Dummy()
Adapters.adpater[75].ifacename = 'IInstalledGun'
Adapters.adpater[75].module = 'adapters.IInstalledGunAdapter.IInstalledGunAdapter'
Adapters.adpater[75].obtype = []
Adapters.adpater[75].obtype.insert(0, None)
Adapters.adpater[75].obtype[0] = 'plane'
Adapters.adpater[75].obtype.insert(1, None)
Adapters.adpater[75].obtype[1] = 'weaponslot'
Adapters.adpater.insert(76, None)
Adapters.adpater[76] = Dummy()
Adapters.adpater[76].ifacename = 'IInstalledEquipment'
Adapters.adpater[76].module = 'adapters.IInstalledEquipmentAdapter.IInstalledEquipmentAdapter'
Adapters.adpater[76].obtype = []
Adapters.adpater[76].obtype.insert(0, None)
Adapters.adpater[76].obtype[0] = 'plane'
Adapters.adpater.insert(77, None)
Adapters.adpater[77] = Dummy()
Adapters.adpater[77].ifacename = 'IInstalledBomb'
Adapters.adpater[77].module = 'adapters.IInstalledShellAdapter.IInstalledBombAdapter'
Adapters.adpater[77].obtype = []
Adapters.adpater[77].obtype.insert(0, None)
Adapters.adpater[77].obtype[0] = 'plane'
Adapters.adpater[77].obtype.insert(1, None)
Adapters.adpater[77].obtype[1] = 'weaponslot'
Adapters.adpater.insert(78, None)
Adapters.adpater[78] = Dummy()
Adapters.adpater[78].ifacename = 'IInstalledRocket'
Adapters.adpater[78].module = 'adapters.IInstalledShellAdapter.IInstalledRocketAdapter'
Adapters.adpater[78].obtype = []
Adapters.adpater[78].obtype.insert(0, None)
Adapters.adpater[78].obtype[0] = 'plane'
Adapters.adpater[78].obtype.insert(1, None)
Adapters.adpater[78].obtype[1] = 'weaponslot'
Adapters.adpater.insert(79, None)
Adapters.adpater[79] = Dummy()
Adapters.adpater[79].ifacename = 'IBombDescription'
Adapters.adpater[79].module = 'adapters.IWeaponDescriptionAdapter.IBombDescriptionAdapter'
Adapters.adpater[79].obtype = []
Adapters.adpater[79].obtype.insert(0, None)
Adapters.adpater[79].obtype[0] = 'bomb'
Adapters.adpater[79].obtype.insert(1, None)
Adapters.adpater[79].obtype[1] = 'measurementSystem'
Adapters.adpater.insert(80, None)
Adapters.adpater[80] = Dummy()
Adapters.adpater[80].ifacename = 'IRocketDescription'
Adapters.adpater[80].module = 'adapters.IWeaponDescriptionAdapter.IRocketDescriptionAdapter'
Adapters.adpater[80].obtype = []
Adapters.adpater[80].obtype.insert(0, None)
Adapters.adpater[80].obtype[0] = 'rocket'
Adapters.adpater[80].obtype.insert(1, None)
Adapters.adpater[80].obtype[1] = 'measurementSystem'
Adapters.adpater.insert(81, None)
Adapters.adpater[81] = Dummy()
Adapters.adpater[81].ifacename = 'IAmmoBeltCharacteristics'
Adapters.adpater[81].module = 'adapters.IAmmoBeltCharacteristicsAdapter.IAmmoBeltCharacteristicsAdapter'
Adapters.adpater[81].obtype = []
Adapters.adpater[81].obtype.insert(0, None)
Adapters.adpater[81].obtype[0] = 'ammobelt'
Adapters.adpater[81].obtype.insert(1, None)
Adapters.adpater[81].obtype[1] = 'gun'
Adapters.adpater.insert(82, None)
Adapters.adpater[82] = Dummy()
Adapters.adpater[82].ifacename = 'IAmmoBeltCharacteristics'
Adapters.adpater[82].module = 'adapters.IAmmoBeltCharacteristicsAdapter.IAmmoBeltCharacteristicsAdapter'
Adapters.adpater[82].obtype = []
Adapters.adpater[82].obtype.insert(0, None)
Adapters.adpater[82].obtype[0] = 'ammobelt'
Adapters.adpater.insert(83, None)
Adapters.adpater[83] = Dummy()
Adapters.adpater[83].ifacename = 'IServiceStates'
Adapters.adpater[83].module = 'adapters.IServiceStatesAdapter.IServiceStatesAdapter'
Adapters.adpater[83].obtype = []
Adapters.adpater[83].obtype.insert(0, None)
Adapters.adpater[83].obtype[0] = 'plane'
Adapters.adpater.insert(84, None)
Adapters.adpater[84] = Dummy()
Adapters.adpater[84].ifacename = 'IRepair'
Adapters.adpater[84].module = 'adapters.IRepairAdapter.IRepairAdapter'
Adapters.adpater[84].obtype = []
Adapters.adpater[84].obtype.insert(0, None)
Adapters.adpater[84].obtype[0] = 'plane'
Adapters.adpater.insert(85, None)
Adapters.adpater[85] = Dummy()
Adapters.adpater[85].ifacename = 'IInstalledConsumables'
Adapters.adpater[85].module = 'adapters.IInstalledConsumablesAdapter.IInstalledConsumablesAdapter'
Adapters.adpater[85].obtype = []
Adapters.adpater[85].obtype.insert(0, None)
Adapters.adpater[85].obtype[0] = 'plane'
Adapters.adpater.insert(86, None)
Adapters.adpater[86] = Dummy()
Adapters.adpater[86].ifacename = 'IName'
Adapters.adpater[86].module = 'adapters.IPlaneNameAdapter.IPlaneNameAdapter'
Adapters.adpater[86].obtype = []
Adapters.adpater[86].obtype.insert(0, None)
Adapters.adpater[86].obtype[0] = 'plane'
Adapters.adpater.insert(87, None)
Adapters.adpater[87] = Dummy()
Adapters.adpater[87].ifacename = 'IPlaneCrew'
Adapters.adpater[87].module = 'adapters.IPlaneCrewAdapter.IPlaneCrewAdapter'
Adapters.adpater[87].obtype = []
Adapters.adpater[87].obtype.insert(0, None)
Adapters.adpater[87].obtype[0] = 'plane'
Adapters.adpater.insert(88, None)
Adapters.adpater[88] = Dummy()
Adapters.adpater[88].ifacename = 'ICrewMember'
Adapters.adpater[88].module = 'adapters.ICrewMemberAdapter.ICrewMemberAdapter'
Adapters.adpater[88].obtype = []
Adapters.adpater[88].obtype.insert(0, None)
Adapters.adpater[88].obtype[0] = 'crewmember'
Adapters.adpater.insert(89, None)
Adapters.adpater[89] = Dummy()
Adapters.adpater[89].ifacename = 'IAvailableSkills'
Adapters.adpater[89].module = 'adapters.IAvailableSkillsAdapter.IAvailableSkillsAdapter'
Adapters.adpater[89].obtype = []
Adapters.adpater[89].obtype.insert(0, None)
Adapters.adpater[89].obtype[0] = 'crewmember'
Adapters.adpater.insert(90, None)
Adapters.adpater[90] = Dummy()
Adapters.adpater[90].ifacename = 'ISkillDescription'
Adapters.adpater[90].module = 'adapters.ISkillDescriptionAdapter.ISkillDescriptionAdapter'
Adapters.adpater[90].obtype = []
Adapters.adpater[90].obtype.insert(0, None)
Adapters.adpater[90].obtype[0] = 'skill'
Adapters.adpater.insert(91, None)
Adapters.adpater[91] = Dummy()
Adapters.adpater[91].ifacename = 'ICrewSpecializationResearchCost'
Adapters.adpater[91].module = 'adapters.ICrewSpecializationResearchCostAdapter.ICrewSpecializationResearchCostAdapter'
Adapters.adpater[91].obtype = []
Adapters.adpater[91].obtype.insert(0, None)
Adapters.adpater[91].obtype[0] = 'account'
Adapters.adpater.insert(92, None)
Adapters.adpater[92] = Dummy()
Adapters.adpater[92].ifacename = 'IAwards'
Adapters.adpater[92].module = 'adapters.IAwardsAdapter.IAwardsAdapter'
Adapters.adpater[92].obtype = []
Adapters.adpater[92].obtype.insert(0, None)
Adapters.adpater[92].obtype[0] = 'account'
Adapters.adpater.insert(93, None)
Adapters.adpater[93] = Dummy()
Adapters.adpater[93].ifacename = 'IAwards'
Adapters.adpater[93].module = 'adapters.IAwardsAdapter.IAwardsPlaneAdapter'
Adapters.adpater[93].obtype = []
Adapters.adpater[93].obtype.insert(0, None)
Adapters.adpater[93].obtype[0] = 'plane'
Adapters.adpater.insert(94, None)
Adapters.adpater[94] = Dummy()
Adapters.adpater[94].ifacename = 'IAwardDescription'
Adapters.adpater[94].module = 'adapters.IAwardDescriptionAdapter.IAwardDescriptionAdapter'
Adapters.adpater[94].obtype = []
Adapters.adpater[94].obtype.insert(0, None)
Adapters.adpater[94].obtype[0] = 'medal'
Adapters.adpater.insert(95, None)
Adapters.adpater[95] = Dummy()
Adapters.adpater[95].ifacename = 'IAwardDescription'
Adapters.adpater[95].module = 'adapters.IAwardDescriptionAdapter.IAwardDescriptionAdapter'
Adapters.adpater[95].obtype = []
Adapters.adpater[95].obtype.insert(0, None)
Adapters.adpater[95].obtype[0] = 'ribbon'
Adapters.adpater.insert(96, None)
Adapters.adpater[96] = Dummy()
Adapters.adpater[96].ifacename = 'IAwardDescription'
Adapters.adpater[96].module = 'adapters.IAwardDescriptionAdapter.IAwardDescriptionAdapter'
Adapters.adpater[96].obtype = []
Adapters.adpater[96].obtype.insert(0, None)
Adapters.adpater[96].obtype[0] = 'achievement'
Adapters.adpater.insert(97, None)
Adapters.adpater[97] = Dummy()
Adapters.adpater[97].ifacename = 'IAwardDailyBonus'
Adapters.adpater[97].module = 'adapters.IAwardDailyBonusAdapter.IAwardDailyBonusAdapter'
Adapters.adpater[97].obtype = []
Adapters.adpater[97].obtype.insert(0, None)
Adapters.adpater[97].obtype[0] = 'achievement'
Adapters.adpater.insert(98, None)
Adapters.adpater[98] = Dummy()
Adapters.adpater[98].ifacename = 'IExperience'
Adapters.adpater[98].module = 'adapters.IExperiencePlaneAdapter.IExperiencePlaneAdapter'
Adapters.adpater[98].obtype = []
Adapters.adpater[98].obtype.insert(0, None)
Adapters.adpater[98].obtype[0] = 'plane'
Adapters.adpater.insert(99, None)
Adapters.adpater[99] = Dummy()
Adapters.adpater[99].ifacename = 'ICrewSkillsDropCost'
Adapters.adpater[99].module = 'adapters.ICrewSkillsDropCostAdapter.ICrewSkillsDropCostAdapter'
Adapters.adpater[99].obtype = []
Adapters.adpater[99].obtype.insert(0, None)
Adapters.adpater[99].obtype[0] = 'account'
Adapters.adpater.insert(100, None)
Adapters.adpater[100] = Dummy()
Adapters.adpater[100].ifacename = 'ICrewSPFromExp'
Adapters.adpater[100].module = 'adapters.ICrewSPFromExpAdapter.ICrewSPFromExpAdapter'
Adapters.adpater[100].obtype = []
Adapters.adpater[100].obtype.insert(0, None)
Adapters.adpater[100].obtype[0] = 'account'
Adapters.adpater.insert(101, None)
Adapters.adpater[101] = Dummy()
Adapters.adpater[101].ifacename = 'ICrewRanks'
Adapters.adpater[101].module = 'adapters.ICrewRanksAdapter.ICrewRanksAdapter'
Adapters.adpater[101].obtype = []
Adapters.adpater[101].obtype.insert(0, None)
Adapters.adpater[101].obtype[0] = 'crewmember'
Adapters.adpater.insert(102, None)
Adapters.adpater[102] = Dummy()
Adapters.adpater[102].ifacename = 'ICrewMemberDroppedSkills'
Adapters.adpater[102].module = 'adapters.ICrewMemberDroppedSkillsAdapter.ICrewMemberDroppedSkillsAdapter'
Adapters.adpater[102].obtype = []
Adapters.adpater[102].obtype.insert(0, None)
Adapters.adpater[102].obtype[0] = 'crewmember'
Adapters.adpater.insert(103, None)
Adapters.adpater[103] = Dummy()
Adapters.adpater[103].ifacename = 'IPlaneDynamicDataPack'
Adapters.adpater[103].module = 'adapters.IPlaneDynamicDataPackAdapter.IPlaneDynamicDataPackAdapter'
Adapters.adpater[103].obtype = []
Adapters.adpater[103].obtype.insert(0, None)
Adapters.adpater[103].obtype[0] = 'plane'
Adapters.adpater.insert(104, None)
Adapters.adpater[104] = Dummy()
Adapters.adpater[104].ifacename = 'IPlanes'
Adapters.adpater[104].module = 'adapters.IPlanesCrewMemberAdapter.IPlanesCrewMemberAdapter'
Adapters.adpater[104].obtype = []
Adapters.adpater[104].obtype.insert(0, None)
Adapters.adpater[104].obtype[0] = 'crewmember'
Adapters.adpater.insert(105, None)
Adapters.adpater[105] = Dummy()
Adapters.adpater[105].ifacename = 'IListAmmoBelts'
Adapters.adpater[105].module = 'adapters.IListAmmoBeltsAdapter.IListAmmoBeltsAdapter'
Adapters.adpater[105].obtype = []
Adapters.adpater[105].obtype.insert(0, None)
Adapters.adpater[105].obtype[0] = 'account'
Adapters.adpater.insert(106, None)
Adapters.adpater[106] = Dummy()
Adapters.adpater[106].ifacename = 'IListBombs'
Adapters.adpater[106].module = 'adapters.IListSuspensionArmsAdapter.IListBombsAdapter'
Adapters.adpater[106].obtype = []
Adapters.adpater[106].obtype.insert(0, None)
Adapters.adpater[106].obtype[0] = 'account'
Adapters.adpater.insert(107, None)
Adapters.adpater[107] = Dummy()
Adapters.adpater[107].ifacename = 'IListRockets'
Adapters.adpater[107].module = 'adapters.IListSuspensionArmsAdapter.IListRocketsAdapter'
Adapters.adpater[107].obtype = []
Adapters.adpater[107].obtype.insert(0, None)
Adapters.adpater[107].obtype[0] = 'account'
Adapters.adpater.insert(108, None)
Adapters.adpater[108] = Dummy()
Adapters.adpater[108].ifacename = 'IListUpgrades'
Adapters.adpater[108].module = 'adapters.IListUpgradesAdapter.IListUpgradesAdapter'
Adapters.adpater[108].obtype = []
Adapters.adpater[108].obtype.insert(0, None)
Adapters.adpater[108].obtype[0] = 'account'
Adapters.adpater.insert(109, None)
Adapters.adpater[109] = Dummy()
Adapters.adpater[109].ifacename = 'IListBoughtUpgrades'
Adapters.adpater[109].module = 'adapters.IListBoughtUpgradesAdapter.IListBoughtUpgradesAdapter'
Adapters.adpater[109].obtype = []
Adapters.adpater[109].obtype.insert(0, None)
Adapters.adpater[109].obtype[0] = 'account'
Adapters.adpater.insert(110, None)
Adapters.adpater[110] = Dummy()
Adapters.adpater[110].ifacename = 'IInstalledCount'
Adapters.adpater[110].module = 'adapters.IInstalledCountAmmoBeltsAdapter.IInstalledCountAmmoBeltsAdapter'
Adapters.adpater[110].obtype = []
Adapters.adpater[110].obtype.insert(0, None)
Adapters.adpater[110].obtype[0] = 'ammobelt'
Adapters.adpater.insert(111, None)
Adapters.adpater[111] = Dummy()
Adapters.adpater[111].ifacename = 'IDepotCount'
Adapters.adpater[111].module = 'adapters.IDepotCountAmmoBeltsAdapter.IDepotCountAmmoBeltsAdapter'
Adapters.adpater[111].obtype = []
Adapters.adpater[111].obtype.insert(0, None)
Adapters.adpater[111].obtype[0] = 'ammobelt'
Adapters.adpater.insert(112, None)
Adapters.adpater[112] = Dummy()
Adapters.adpater[112].ifacename = 'IInstalledCount'
Adapters.adpater[112].module = 'adapters.IInstalledCountShellsAdapter.IInstalledCountShellsAdapter'
Adapters.adpater[112].obtype = []
Adapters.adpater[112].obtype.insert(0, None)
Adapters.adpater[112].obtype[0] = 'bomb'
Adapters.adpater.insert(113, None)
Adapters.adpater[113] = Dummy()
Adapters.adpater[113].ifacename = 'IDepotCount'
Adapters.adpater[113].module = 'adapters.IDepotCountShellsAdapter.IDepotCountShellsAdapter'
Adapters.adpater[113].obtype = []
Adapters.adpater[113].obtype.insert(0, None)
Adapters.adpater[113].obtype[0] = 'bomb'
Adapters.adpater.insert(114, None)
Adapters.adpater[114] = Dummy()
Adapters.adpater[114].ifacename = 'IInstalledCount'
Adapters.adpater[114].module = 'adapters.IInstalledCountShellsAdapter.IInstalledCountShellsAdapter'
Adapters.adpater[114].obtype = []
Adapters.adpater[114].obtype.insert(0, None)
Adapters.adpater[114].obtype[0] = 'rocket'
Adapters.adpater.insert(115, None)
Adapters.adpater[115] = Dummy()
Adapters.adpater[115].ifacename = 'IDepotCount'
Adapters.adpater[115].module = 'adapters.IDepotCountShellsAdapter.IDepotCountShellsAdapter'
Adapters.adpater[115].obtype = []
Adapters.adpater[115].obtype.insert(0, None)
Adapters.adpater[115].obtype[0] = 'rocket'
Adapters.adpater.insert(116, None)
Adapters.adpater[116] = Dummy()
Adapters.adpater[116].ifacename = 'IInstalledCount'
Adapters.adpater[116].module = 'adapters.IInstalledCountConsumablesAdapter.IInstalledCountConsumablesAdapter'
Adapters.adpater[116].obtype = []
Adapters.adpater[116].obtype.insert(0, None)
Adapters.adpater[116].obtype[0] = 'consumable'
Adapters.adpater.insert(117, None)
Adapters.adpater[117] = Dummy()
Adapters.adpater[117].ifacename = 'IDepotCount'
Adapters.adpater[117].module = 'adapters.IDepotCountCEAdapter.IDepotCountCEAdapter'
Adapters.adpater[117].obtype = []
Adapters.adpater[117].obtype.insert(0, None)
Adapters.adpater[117].obtype[0] = 'consumable'
Adapters.adpater.insert(118, None)
Adapters.adpater[118] = Dummy()
Adapters.adpater[118].ifacename = 'IDepotCount'
Adapters.adpater[118].module = 'adapters.IDepotCountCEAdapter.IDepotCountCEAdapter'
Adapters.adpater[118].obtype = []
Adapters.adpater[118].obtype.insert(0, None)
Adapters.adpater[118].obtype[0] = 'equipment'
Adapters.adpater.insert(119, None)
Adapters.adpater[119] = Dummy()
Adapters.adpater[119].ifacename = 'IInstalledCount'
Adapters.adpater[119].module = 'adapters.IInstalledCountEquipmentAdapter.IInstalledCountEquipmentAdapter'
Adapters.adpater[119].obtype = []
Adapters.adpater[119].obtype.insert(0, None)
Adapters.adpater[119].obtype[0] = 'equipment'
Adapters.adpater.insert(120, None)
Adapters.adpater[120] = Dummy()
Adapters.adpater[120].ifacename = 'IDepotCount'
Adapters.adpater[120].module = 'adapters.IDepotCountUpgradeAdapter.IDepotCountUpgradeAdapter'
Adapters.adpater[120].obtype = []
Adapters.adpater[120].obtype.insert(0, None)
Adapters.adpater[120].obtype[0] = 'upgrade'
Adapters.adpater.insert(121, None)
Adapters.adpater[121] = Dummy()
Adapters.adpater[121].ifacename = 'IInstalledCount'
Adapters.adpater[121].module = 'adapters.IInstalledCountUpgradeAdapter.IInstalledCountUpgradeAdapter'
Adapters.adpater[121].obtype = []
Adapters.adpater[121].obtype.insert(0, None)
Adapters.adpater[121].obtype[0] = 'upgrade'
Adapters.adpater.insert(122, None)
Adapters.adpater[122] = Dummy()
Adapters.adpater[122].ifacename = 'IListConsumables'
Adapters.adpater[122].module = 'adapters.IListConsumablesAdapter.IListConsumablesAdapter'
Adapters.adpater[122].obtype = []
Adapters.adpater[122].obtype.insert(0, None)
Adapters.adpater[122].obtype[0] = 'account'
Adapters.adpater.insert(123, None)
Adapters.adpater[123] = Dummy()
Adapters.adpater[123].ifacename = 'IListEquipment'
Adapters.adpater[123].module = 'adapters.IListEquipmentAdapter.IListEquipmentAdapter'
Adapters.adpater[123].obtype = []
Adapters.adpater[123].obtype.insert(0, None)
Adapters.adpater[123].obtype[0] = 'account'
Adapters.adpater.insert(124, None)
Adapters.adpater[124] = Dummy()
Adapters.adpater[124].ifacename = 'ISlotsCount'
Adapters.adpater[124].module = 'adapters.ISlotsCountAdapter.ISlotsCountAdapter'
Adapters.adpater[124].obtype = []
Adapters.adpater[124].obtype.insert(0, None)
Adapters.adpater[124].obtype[0] = 'account'
Adapters.adpater.insert(125, None)
Adapters.adpater[125] = Dummy()
Adapters.adpater[125].ifacename = 'IBarrack'
Adapters.adpater[125].module = 'adapters.IBarrackAdapter.IBarrackAdapter'
Adapters.adpater[125].obtype = []
Adapters.adpater[125].obtype.insert(0, None)
Adapters.adpater[125].obtype[0] = 'account'
Adapters.adpater.insert(126, None)
Adapters.adpater[126] = Dummy()
Adapters.adpater[126].ifacename = 'IBarrack'
Adapters.adpater[126].module = 'adapters.IBarrackAdapter.INationBarrackAdapter'
Adapters.adpater[126].obtype = []
Adapters.adpater[126].obtype.insert(0, None)
Adapters.adpater[126].obtype[0] = 'nation'
Adapters.adpater[126].obtype.insert(1, None)
Adapters.adpater[126].obtype[1] = 'skill'
Adapters.adpater.insert(127, None)
Adapters.adpater[127] = Dummy()
Adapters.adpater[127].ifacename = 'IBarrackSlots'
Adapters.adpater[127].module = 'adapters.IBarrackAdapter.IBarrackSlotsAdapter'
Adapters.adpater[127].obtype = []
Adapters.adpater[127].obtype.insert(0, None)
Adapters.adpater[127].obtype[0] = 'account'
Adapters.adpater.insert(128, None)
Adapters.adpater[128] = Dummy()
Adapters.adpater[128].ifacename = 'IBarrackPrice'
Adapters.adpater[128].module = 'adapters.IBarrackAdapter.IBarrackPriceAdapter'
Adapters.adpater[128].obtype = []
Adapters.adpater[128].obtype.insert(0, None)
Adapters.adpater[128].obtype[0] = 'account'
Adapters.adpater.insert(129, None)
Adapters.adpater[129] = Dummy()
Adapters.adpater[129].ifacename = 'ISkillPenalty'
Adapters.adpater[129].module = 'adapters.ISkillPenaltyAdapter.ISkillPenaltyAdapter'
Adapters.adpater[129].obtype = []
Adapters.adpater[129].obtype.insert(0, None)
Adapters.adpater[129].obtype[0] = 'crewmember'
Adapters.adpater[129].obtype.insert(1, None)
Adapters.adpater[129].obtype[1] = 'plane'
Adapters.adpater.insert(130, None)
Adapters.adpater[130] = Dummy()
Adapters.adpater[130].ifacename = 'ICrewSpecializationRetrainPrc'
Adapters.adpater[130].module = 'adapters.ICrewSpecializationRetrainPrcAdapter.ICrewSpecializationRetrainPrcAdapter'
Adapters.adpater[130].obtype = []
Adapters.adpater[130].obtype.insert(0, None)
Adapters.adpater[130].obtype[0] = 'crewmember'
Adapters.adpater[130].obtype.insert(1, None)
Adapters.adpater[130].obtype[1] = 'plane'
Adapters.adpater.insert(131, None)
Adapters.adpater[131] = Dummy()
Adapters.adpater[131].ifacename = 'ICrewSpecializationRetrainCost'
Adapters.adpater[131].module = 'adapters.ICrewSpecializationRetrainCostAdapter.ICrewSpecializationRetrainCostAdapter'
Adapters.adpater[131].obtype = []
Adapters.adpater[131].obtype.insert(0, None)
Adapters.adpater[131].obtype[0] = 'account'
Adapters.adpater.insert(132, None)
Adapters.adpater[132] = Dummy()
Adapters.adpater[132].ifacename = 'IPlaneStats'
Adapters.adpater[132].module = 'adapters.IStatsAdapter.IPlaneStatsAdapter'
Adapters.adpater[132].obtype = []
Adapters.adpater[132].obtype.insert(0, None)
Adapters.adpater[132].obtype[0] = 'plane'
Adapters.adpater.insert(133, None)
Adapters.adpater[133] = Dummy()
Adapters.adpater[133].ifacename = 'ISummaryStats'
Adapters.adpater[133].module = 'adapters.IStatsAdapter.ISummaryStatsAdapter'
Adapters.adpater[133].obtype = []
Adapters.adpater[133].obtype.insert(0, None)
Adapters.adpater[133].obtype[0] = 'account'
Adapters.adpater.insert(134, None)
Adapters.adpater[134] = Dummy()
Adapters.adpater[134].ifacename = 'IShortPlaneDescription'
Adapters.adpater[134].module = 'adapters.IStatsAdapter.IShortPlaneDescription'
Adapters.adpater[134].obtype = []
Adapters.adpater[134].obtype.insert(0, None)
Adapters.adpater[134].obtype[0] = 'plane'
Adapters.adpater.insert(135, None)
Adapters.adpater[135] = Dummy()
Adapters.adpater[135].ifacename = 'IShortPlaneStats'
Adapters.adpater[135].module = 'adapters.IStatsAdapter.IShortPlaneStats'
Adapters.adpater[135].obtype = []
Adapters.adpater[135].obtype.insert(0, None)
Adapters.adpater[135].obtype[0] = 'plane'
Adapters.adpater.insert(136, None)
Adapters.adpater[136] = Dummy()
Adapters.adpater[136].ifacename = 'IStatsPlanesList'
Adapters.adpater[136].module = 'adapters.IStatsPlanesListAdapter.IStatsPlanesListAdapter'
Adapters.adpater[136].obtype = []
Adapters.adpater[136].obtype.insert(0, None)
Adapters.adpater[136].obtype[0] = 'account'
Adapters.adpater.insert(137, None)
Adapters.adpater[137] = Dummy()
Adapters.adpater[137].ifacename = 'ILocalizationLanguage'
Adapters.adpater[137].module = 'adapters.ILocalizationLanguageAdapter.ILocalizationLanguageAdapter'
Adapters.adpater[137].obtype = []
Adapters.adpater[137].obtype.insert(0, None)
Adapters.adpater[137].obtype[0] = 'account'
Adapters.adpater.insert(138, None)
Adapters.adpater[138] = Dummy()
Adapters.adpater[138].ifacename = 'ICamouflages'
Adapters.adpater[138].module = 'adapters.ICamouflagesAdapter.ICamouflagesAdapter'
Adapters.adpater[138].obtype = []
Adapters.adpater[138].obtype.insert(0, None)
Adapters.adpater[138].obtype[0] = 'plane'
Adapters.adpater.insert(139, None)
Adapters.adpater[139] = Dummy()
Adapters.adpater[139].ifacename = 'ICamouflageDescription'
Adapters.adpater[139].module = 'adapters.ICamouflageDescriptionAdapter.ICamouflageDescriptionAdapter'
Adapters.adpater[139].obtype = []
Adapters.adpater[139].obtype.insert(0, None)
Adapters.adpater[139].obtype[0] = 'camouflage'
Adapters.adpater.insert(140, None)
Adapters.adpater[140] = Dummy()
Adapters.adpater[140].ifacename = 'ICamouflageStatus'
Adapters.adpater[140].module = 'adapters.ICamouflageStatusAdapter.ICamouflageStatusAdapter'
Adapters.adpater[140].obtype = []
Adapters.adpater[140].obtype.insert(0, None)
Adapters.adpater[140].obtype[0] = 'camouflage'
Adapters.adpater.insert(141, None)
Adapters.adpater[141] = Dummy()
Adapters.adpater[141].ifacename = 'IPriceSchemes'
Adapters.adpater[141].module = 'adapters.IPriceSchemesAdapter.IPriceSchemesAdapter'
Adapters.adpater[141].obtype = []
Adapters.adpater[141].obtype.insert(0, None)
Adapters.adpater[141].obtype[0] = 'account'
Adapters.adpater.insert(142, None)
Adapters.adpater[142] = Dummy()
Adapters.adpater[142].ifacename = 'IBonusSchemes'
Adapters.adpater[142].module = 'adapters.IBonusSchemesAdapter.IBonusSchemesAdapter'
Adapters.adpater[142].obtype = []
Adapters.adpater[142].obtype.insert(0, None)
Adapters.adpater[142].obtype[0] = 'account'
Adapters.adpater.insert(143, None)
Adapters.adpater[143] = Dummy()
Adapters.adpater[143].ifacename = 'ITimeDelta'
Adapters.adpater[143].module = 'adapters.ITimeDeltaAdapter.ITimeDeltaAdapter'
Adapters.adpater[143].obtype = []
Adapters.adpater[143].obtype.insert(0, None)
Adapters.adpater[143].obtype[0] = 'account'
Adapters.adpater.insert(144, None)
Adapters.adpater[144] = Dummy()
Adapters.adpater[144].ifacename = 'IPlaneSalesLeft'
Adapters.adpater[144].module = 'adapters.IPlaneSalesLeftAdapter.IPlaneSalesLeftAdapter'
Adapters.adpater[144].obtype = []
Adapters.adpater[144].obtype.insert(0, None)
Adapters.adpater[144].obtype[0] = 'account'
Adapters.adpater.insert(145, None)
Adapters.adpater[145] = Dummy()
Adapters.adpater[145].ifacename = 'IInstalledCamouflage'
Adapters.adpater[145].module = 'adapters.IInstalledCamouflageAdapter.IInstalledCamouflageAdapter'
Adapters.adpater[145].obtype = []
Adapters.adpater[145].obtype.insert(0, None)
Adapters.adpater[145].obtype[0] = 'plane'
Adapters.adpater.insert(146, None)
Adapters.adpater[146] = Dummy()
Adapters.adpater[146].ifacename = 'IInstalledCamouflage'
Adapters.adpater[146].module = 'adapters.IInstalledCamouflageAdapter.IInstalledCamouflageAdapter'
Adapters.adpater[146].obtype = []
Adapters.adpater[146].obtype.insert(0, None)
Adapters.adpater[146].obtype[0] = 'previewmodel'
Adapters.adpater.insert(147, None)
Adapters.adpater[147] = Dummy()
Adapters.adpater[147].ifacename = 'IPlayerSummaryStats'
Adapters.adpater[147].module = 'adapters.IStatsAdapter.IPlayerSummaryStatsAdapter'
Adapters.adpater[147].obtype = []
Adapters.adpater[147].obtype.insert(0, None)
Adapters.adpater[147].obtype[0] = 'account'
Adapters.adpater.insert(148, None)
Adapters.adpater[148] = Dummy()
Adapters.adpater[148].ifacename = 'IPlayerPlaneStats'
Adapters.adpater[148].module = 'adapters.IStatsAdapter.IPlayerPlaneStatsAdapter'
Adapters.adpater[148].obtype = []
Adapters.adpater[148].obtype.insert(0, None)
Adapters.adpater[148].obtype[0] = 'account'
Adapters.adpater[148].obtype.insert(1, None)
Adapters.adpater[148].obtype[1] = 'plane'
Adapters.adpater.insert(149, None)
Adapters.adpater[149] = Dummy()
Adapters.adpater[149].ifacename = 'IPlayerShortPlaneDescription'
Adapters.adpater[149].module = 'adapters.IStatsAdapter.IPlayerShortPlaneDescriptionAdapter'
Adapters.adpater[149].obtype = []
Adapters.adpater[149].obtype.insert(0, None)
Adapters.adpater[149].obtype[0] = 'account'
Adapters.adpater[149].obtype.insert(1, None)
Adapters.adpater[149].obtype[1] = 'plane'
Adapters.adpater.insert(150, None)
Adapters.adpater[150] = Dummy()
Adapters.adpater[150].ifacename = 'IPlayerShortPlaneStats'
Adapters.adpater[150].module = 'adapters.IStatsAdapter.IPlayerShortPlaneStatsAdapter'
Adapters.adpater[150].obtype = []
Adapters.adpater[150].obtype.insert(0, None)
Adapters.adpater[150].obtype[0] = 'account'
Adapters.adpater[150].obtype.insert(1, None)
Adapters.adpater[150].obtype[1] = 'plane'
Adapters.adpater.insert(151, None)
Adapters.adpater[151] = Dummy()
Adapters.adpater[151].ifacename = 'IPaymentType'
Adapters.adpater[151].module = 'adapters.IPaymentTypeAdapter.PaymentTypeBase'
Adapters.adpater[151].obtype = []
Adapters.adpater[151].obtype.insert(0, None)
Adapters.adpater[151].obtype[0] = 'consumable'
Adapters.adpater.insert(152, None)
Adapters.adpater[152] = Dummy()
Adapters.adpater[152].ifacename = 'IPaymentType'
Adapters.adpater[152].module = 'adapters.IPaymentTypeAdapter.PaymentTypeBase'
Adapters.adpater[152].obtype = []
Adapters.adpater[152].obtype.insert(0, None)
Adapters.adpater[152].obtype[0] = 'consumable'
Adapters.adpater[152].obtype.insert(1, None)
Adapters.adpater[152].obtype[1] = 'plane'
Adapters.adpater.insert(153, None)
Adapters.adpater[153] = Dummy()
Adapters.adpater[153].ifacename = 'IPaymentType'
Adapters.adpater[153].module = 'adapters.IPaymentTypeAdapter.PaymentTypeBase'
Adapters.adpater[153].obtype = []
Adapters.adpater[153].obtype.insert(0, None)
Adapters.adpater[153].obtype[0] = 'ammobelt'
Adapters.adpater[153].obtype.insert(1, None)
Adapters.adpater[153].obtype[1] = 'plane'
Adapters.adpater[153].obtype.insert(2, None)
Adapters.adpater[153].obtype[2] = 'slot'
Adapters.adpater[153].obtype.insert(3, None)
Adapters.adpater[153].obtype[3] = 'slotConfig'
Adapters.adpater.insert(154, None)
Adapters.adpater[154] = Dummy()
Adapters.adpater[154].ifacename = 'IPaymentType'
Adapters.adpater[154].module = 'adapters.IPaymentTypeAdapter.PaymentTypeBase'
Adapters.adpater[154].obtype = []
Adapters.adpater[154].obtype.insert(0, None)
Adapters.adpater[154].obtype[0] = 'ammobelt'
Adapters.adpater.insert(155, None)
Adapters.adpater[155] = Dummy()
Adapters.adpater[155].ifacename = 'IWalletSettings'
Adapters.adpater[155].module = 'adapters.IWalletSettingsAdapter.IWalletSettingsAdapter'
Adapters.adpater[155].obtype = []
Adapters.adpater[155].obtype.insert(0, None)
Adapters.adpater[155].obtype[0] = 'account'
Adapters.adpater.insert(156, None)
Adapters.adpater[156] = Dummy()
Adapters.adpater[156].ifacename = 'IAwardsList'
Adapters.adpater[156].module = 'adapters.IAwardsListAdapter.IAwardsListAdapter'
Adapters.adpater[156].obtype = []
Adapters.adpater[156].obtype.insert(0, None)
Adapters.adpater[156].obtype[0] = 'account'
Adapters.adpater.insert(157, None)
Adapters.adpater[157] = Dummy()
Adapters.adpater[157].ifacename = 'ILastProcessedResponse'
Adapters.adpater[157].module = 'adapters.ILastProcessedResponseAdapter.ILastProcessedResponseAdapter'
Adapters.adpater[157].obtype = []
Adapters.adpater[157].obtype.insert(0, None)
Adapters.adpater[157].obtype[0] = 'account'
Adapters.adpater.insert(158, None)
Adapters.adpater[158] = Dummy()
Adapters.adpater[158].ifacename = 'IResponse'
Adapters.adpater[158].module = 'adapters.IResponseAdapter.IResponseAdapter'
Adapters.adpater[158].obtype = []
Adapters.adpater[158].obtype.insert(0, None)
Adapters.adpater[158].obtype[0] = 'response'
Adapters.adpater.insert(159, None)
Adapters.adpater[159] = Dummy()
Adapters.adpater[159].ifacename = 'IName'
Adapters.adpater[159].module = 'adapters.IPeripheryNameAdapter.IPeripheryNameAdapter'
Adapters.adpater[159].obtype = []
Adapters.adpater[159].obtype.insert(0, None)
Adapters.adpater[159].obtype[0] = 'periphery'
Adapters.adpater.insert(160, None)
Adapters.adpater[160] = Dummy()
Adapters.adpater[160].ifacename = 'IBattleResult'
Adapters.adpater[160].module = 'adapters.IBattleResultAdapter.IBattleResultAdapter'
Adapters.adpater[160].obtype = []
Adapters.adpater[160].obtype.insert(0, None)
Adapters.adpater[160].obtype[0] = 'battleResult'
Adapters.adpater.insert(161, None)
Adapters.adpater[161] = Dummy()
Adapters.adpater[161].ifacename = 'IBattleResultShort'
Adapters.adpater[161].module = 'adapters.IBattleResultAdapter.IBattleResultShortAdapter'
Adapters.adpater[161].obtype = []
Adapters.adpater[161].obtype.insert(0, None)
Adapters.adpater[161].obtype[0] = 'battleResult'
Adapters.adpater.insert(162, None)
Adapters.adpater[162] = Dummy()
Adapters.adpater[162].ifacename = 'ISessionBattleResults'
Adapters.adpater[162].module = 'adapters.ISessionBattleResultsAdapter.ISessionBattleResultsAdapter'
Adapters.adpater[162].obtype = []
Adapters.adpater[162].obtype.insert(0, None)
Adapters.adpater[162].obtype[0] = 'account'
Adapters.adpater.insert(163, None)
Adapters.adpater[163] = Dummy()
Adapters.adpater[163].ifacename = 'IQuestList'
Adapters.adpater[163].module = 'adapters.IQuestListAdapter.IQuestListAccountAdapter'
Adapters.adpater[163].obtype = []
Adapters.adpater[163].obtype.insert(0, None)
Adapters.adpater[163].obtype[0] = 'account'
Adapters.adpater.insert(164, None)
Adapters.adpater[164] = Dummy()
Adapters.adpater[164].ifacename = 'IQuestList'
Adapters.adpater[164].module = 'adapters.IQuestListAdapter.IQuestListPlaneAdapter'
Adapters.adpater[164].obtype = []
Adapters.adpater[164].obtype.insert(0, None)
Adapters.adpater[164].obtype[0] = 'plane'
Adapters.adpater.insert(165, None)
Adapters.adpater[165] = Dummy()
Adapters.adpater[165].ifacename = 'IQuestDescription'
Adapters.adpater[165].module = 'adapters.IQuestDescriptionAdapter.IQuestDescriptionAdapter'
Adapters.adpater[165].obtype = []
Adapters.adpater[165].obtype.insert(0, None)
Adapters.adpater[165].obtype[0] = 'battlequest'
Adapters.adpater.insert(166, None)
Adapters.adpater[166] = Dummy()
Adapters.adpater[166].ifacename = 'IQuestRead'
Adapters.adpater[166].module = 'adapters.IQuestReadAdapter.IQuestReadAdapter'
Adapters.adpater[166].obtype = []
Adapters.adpater[166].obtype.insert(0, None)
Adapters.adpater[166].obtype[0] = 'battlequest'
Adapters.adpater.insert(167, None)
Adapters.adpater[167] = Dummy()
Adapters.adpater[167].ifacename = 'IQuestHidden'
Adapters.adpater[167].module = 'adapters.IQuestHiddenAdapter.IQuestHiddenAdapter'
Adapters.adpater[167].obtype = []
Adapters.adpater[167].obtype.insert(0, None)
Adapters.adpater[167].obtype[0] = 'battlequest'
Adapters.adpater.insert(168, None)
Adapters.adpater[168] = Dummy()
Adapters.adpater[168].ifacename = 'IQuestDynDescription'
Adapters.adpater[168].module = 'adapters.IQuestDynDescriptionAdapter.IQuestDynDescriptionAdapter'
Adapters.adpater[168].obtype = []
Adapters.adpater[168].obtype.insert(0, None)
Adapters.adpater[168].obtype[0] = 'battlequest'
Adapters.adpater.insert(169, None)
Adapters.adpater[169] = Dummy()
Adapters.adpater[169].ifacename = 'IQuestAvaiblePlanes'
Adapters.adpater[169].module = 'adapters.IQuestAvaiblePlanesAdapter.IQuestAvaiblePlanesAdapter'
Adapters.adpater[169].obtype = []
Adapters.adpater[169].obtype.insert(0, None)
Adapters.adpater[169].obtype[0] = 'battlequest'
Adapters.adpater.insert(170, None)
Adapters.adpater[170] = Dummy()
Adapters.adpater[170].ifacename = 'IQuestResults'
Adapters.adpater[170].module = 'adapters.IQuestResultAdapter.IQuestResultAdapter'
Adapters.adpater[170].obtype = []
Adapters.adpater[170].obtype.insert(0, None)
Adapters.adpater[170].obtype[0] = 'battlequest'
Adapters.adpater.insert(171, None)
Adapters.adpater[171] = Dummy()
Adapters.adpater[171].ifacename = 'IQuestSelectConsist'
Adapters.adpater[171].module = 'adapters.IQuestSelectConsistAdapter.IQuestSelectConsistAdapter'
Adapters.adpater[171].obtype = []
Adapters.adpater[171].obtype.insert(0, None)
Adapters.adpater[171].obtype[0] = 'account'
Adapters.adpater.insert(172, None)
Adapters.adpater[172] = Dummy()
Adapters.adpater[172].ifacename = 'IQuestListAvailableConsist'
Adapters.adpater[172].module = 'adapters.IQuestListAvailableConsistAdapter.IQuestListAvailableConsistAdapter'
Adapters.adpater[172].obtype = []
Adapters.adpater[172].obtype.insert(0, None)
Adapters.adpater[172].obtype[0] = 'account'
Adapters.adpater.insert(173, None)
Adapters.adpater[173] = Dummy()
Adapters.adpater[173].ifacename = 'IQuestConsistEndAction'
Adapters.adpater[173].module = 'adapters.IQuestConsistEndActionAdapter.IQuestConsistEndActionAdapter'
Adapters.adpater[173].obtype = []
Adapters.adpater[173].obtype.insert(0, None)
Adapters.adpater[173].obtype[0] = 'account'
Adapters.adpater.insert(174, None)
Adapters.adpater[174] = Dummy()
Adapters.adpater[174].ifacename = 'IQuestPool'
Adapters.adpater[174].module = 'adapters.IQuestPoolAdapter.IQuestPoolAdapter'
Adapters.adpater[174].obtype = []
Adapters.adpater[174].obtype.insert(0, None)
Adapters.adpater[174].obtype[0] = 'account'
Adapters.adpater.insert(175, None)
Adapters.adpater[175] = Dummy()
Adapters.adpater[175].ifacename = 'IQuestBuy'
Adapters.adpater[175].module = 'adapters.IQuestBuyAdapter.IQuestBuyAdapter'
Adapters.adpater[175].obtype = []
Adapters.adpater[175].obtype.insert(0, None)
Adapters.adpater[175].obtype[0] = 'questoperation'
Adapters.adpater.insert(176, None)
Adapters.adpater[176] = Dummy()
Adapters.adpater[176].ifacename = 'IQuestProlong'
Adapters.adpater[176].module = 'adapters.IQuestBuyAdapter.IQuestProlongAdapter'
Adapters.adpater[176].obtype = []
Adapters.adpater[176].obtype.insert(0, None)
Adapters.adpater[176].obtype[0] = 'questoperation'
Adapters.adpater.insert(177, None)
Adapters.adpater[177] = Dummy()
Adapters.adpater[177].ifacename = 'IQuestChangeGroup'
Adapters.adpater[177].module = 'adapters.IQuestBuyAdapter.IQuestChangeGroupAdapter'
Adapters.adpater[177].obtype = []
Adapters.adpater[177].obtype.insert(0, None)
Adapters.adpater[177].obtype[0] = 'questoperation'
Adapters.adpater.insert(178, None)
Adapters.adpater[178] = Dummy()
Adapters.adpater[178].ifacename = 'IQuestDebugProcess'
Adapters.adpater[178].module = 'adapters.IQuestDebugProcessAdapter.IQuestDebugProcessAdapter'
Adapters.adpater[178].obtype = []
Adapters.adpater[178].obtype.insert(0, None)
Adapters.adpater[178].obtype[0] = 'questoperation'
Adapters.adpater.insert(179, None)
Adapters.adpater[179] = Dummy()
Adapters.adpater[179].ifacename = 'IRentConf'
Adapters.adpater[179].module = 'adapters.IRentConfAdapter.IRentConfAdapter'
Adapters.adpater[179].obtype = []
Adapters.adpater[179].obtype.insert(0, None)
Adapters.adpater[179].obtype[0] = 'plane'
Adapters.adpater.insert(180, None)
Adapters.adpater[180] = Dummy()
Adapters.adpater[180].ifacename = 'IRent'
Adapters.adpater[180].module = 'adapters.IRentAdapter.IRentAdapter'
Adapters.adpater[180].obtype = []
Adapters.adpater[180].obtype.insert(0, None)
Adapters.adpater[180].obtype[0] = 'plane'
Adapters.adpater.insert(181, None)
Adapters.adpater[181] = Dummy()
Adapters.adpater[181].ifacename = 'IActionUIList'
Adapters.adpater[181].module = 'adapters.IActionUIListAdapter.IActionUIListAdapter'
Adapters.adpater[181].obtype = []
Adapters.adpater[181].obtype.insert(0, None)
Adapters.adpater[181].obtype[0] = 'account'
Adapters.adpater.insert(182, None)
Adapters.adpater[182] = Dummy()
Adapters.adpater[182].ifacename = 'IActionUI'
Adapters.adpater[182].module = 'adapters.IActionUIAdapter.IActionUIAdapter'
Adapters.adpater[182].obtype = []
Adapters.adpater[182].obtype.insert(0, None)
Adapters.adpater[182].obtype[0] = 'actionui'
Adapters.adpater.insert(183, None)
Adapters.adpater[183] = Dummy()
Adapters.adpater[183].ifacename = 'IMeasurementSystem'
Adapters.adpater[183].module = 'adapters.IMeasurementSystemAdapter.IMeasurementSystemAdapter'
Adapters.adpater[183].obtype = []
Adapters.adpater[183].obtype.insert(0, None)
Adapters.adpater[183].obtype[0] = 'account'
Adapters.adpater.insert(184, None)
Adapters.adpater[184] = Dummy()
Adapters.adpater[184].ifacename = 'IMeasurementSystemInfo'
Adapters.adpater[184].module = 'adapters.IMeasurementSystemAdapter.IMeasurementSystemInfoAdapter'
Adapters.adpater[184].obtype = []
Adapters.adpater[184].obtype.insert(0, None)
Adapters.adpater[184].obtype[0] = 'measurementSystem'
Adapters.adpater.insert(185, None)
Adapters.adpater[185] = Dummy()
Adapters.adpater[185].ifacename = 'IMeasurementSystemsList'
Adapters.adpater[185].module = 'adapters.IMeasurementSystemAdapter.IMeasurementSystemsListAdapter'
Adapters.adpater[185].obtype = []
Adapters.adpater[185].obtype.insert(0, None)
Adapters.adpater[185].obtype[0] = 'account'
Adapters.adpater.insert(186, None)
Adapters.adpater[186] = Dummy()
Adapters.adpater[186].ifacename = 'ITransaction'
Adapters.adpater[186].module = 'adapters.ITransactionAdapter.ITransactionAdapter'
Adapters.adpater[186].obtype = []
Adapters.adpater[186].obtype.insert(0, None)
Adapters.adpater[186].obtype[0] = 'transaction'
Adapters.adpater.insert(187, None)
Adapters.adpater[187] = Dummy()
Adapters.adpater[187].ifacename = 'ITransaction'
Adapters.adpater[187].module = 'adapters.ITransactionAdapter.IVTransactionAdapter'
Adapters.adpater[187].obtype = []
Adapters.adpater[187].obtype.insert(0, None)
Adapters.adpater[187].obtype[0] = 'vtransaction'
Adapters.adpater.insert(188, None)
Adapters.adpater[188] = Dummy()
Adapters.adpater[188].ifacename = 'IGameModesParams'
Adapters.adpater[188].module = 'adapters.IGameModesParamsAdapter.IGameModesParamsAdapter'
Adapters.adpater[188].obtype = []
Adapters.adpater[188].obtype.insert(0, None)
Adapters.adpater[188].obtype[0] = 'account'
Adapters.adpater.insert(189, None)
Adapters.adpater[189] = Dummy()
Adapters.adpater[189].ifacename = 'IPvEPlanes'
Adapters.adpater[189].module = 'adapters.IPvEPlanesAdapter.IPvEPlanesAdapter'
Adapters.adpater[189].obtype = []
Adapters.adpater[189].obtype.insert(0, None)
Adapters.adpater[189].obtype[0] = 'account'
Adapters.adpater.insert(190, None)
Adapters.adpater[190] = Dummy()
Adapters.adpater[190].ifacename = 'IRestartTime'
Adapters.adpater[190].module = 'adapters.IRestartTimeAdapter.IRestartTimeAdapter'
Adapters.adpater[190].obtype = []
Adapters.adpater[190].obtype.insert(0, None)
Adapters.adpater[190].obtype[0] = 'account'
Adapters.adpater.insert(191, None)
Adapters.adpater[191] = Dummy()
Adapters.adpater[191].ifacename = 'IIGR'
Adapters.adpater[191].module = 'adapters.IIGRAdapter.IIGRAdapter'
Adapters.adpater[191].obtype = []
Adapters.adpater[191].obtype.insert(0, None)
Adapters.adpater[191].obtype[0] = 'account'
Adapters.adpater.insert(192, None)
Adapters.adpater[192] = Dummy()
Adapters.adpater[192].ifacename = 'IPvEAvailable'
Adapters.adpater[192].module = 'adapters.IPvEAvailableAdapter.IPvEAvailableAdapter'
Adapters.adpater[192].obtype = []
Adapters.adpater[192].obtype.insert(0, None)
Adapters.adpater[192].obtype[0] = 'account'
Adapters.adpater.insert(193, None)
Adapters.adpater[193] = Dummy()
Adapters.adpater[193].ifacename = 'IClanInfoShort'
Adapters.adpater[193].module = 'adapters.IClanInfoShortAdapter.IClanInfoShortAdapter'
Adapters.adpater[193].obtype = []
Adapters.adpater[193].obtype.insert(0, None)
Adapters.adpater[193].obtype[0] = 'account'
Adapters.adpater.insert(194, None)
Adapters.adpater[194] = Dummy()
Adapters.adpater[194].ifacename = 'IClanMotto'
Adapters.adpater[194].module = 'adapters.IClanMottoAdapter.IClanMottoAdapter'
Adapters.adpater[194].obtype = []
Adapters.adpater[194].obtype.insert(0, None)
Adapters.adpater[194].obtype[0] = 'account'
Adapters.adpater.insert(195, None)
Adapters.adpater[195] = Dummy()
Adapters.adpater[195].ifacename = 'IClanInfo'
Adapters.adpater[195].module = 'adapters.IClanInfoAdapter.IClanInfoAdapter'
Adapters.adpater[195].obtype = []
Adapters.adpater[195].obtype.insert(0, None)
Adapters.adpater[195].obtype[0] = 'account'
Adapters.adpater.insert(196, None)
Adapters.adpater[196] = Dummy()
Adapters.adpater[196].ifacename = 'IClanMembers'
Adapters.adpater[196].module = 'adapters.IClanMembersAdapter.IClanMembersAdapter'
Adapters.adpater[196].obtype = []
Adapters.adpater[196].obtype.insert(0, None)
Adapters.adpater[196].obtype[0] = 'account'
Adapters.adpater.insert(197, None)
Adapters.adpater[197] = Dummy()
Adapters.adpater[197].ifacename = 'IClanMember'
Adapters.adpater[197].module = 'adapters.IClanMemberAdapter.IClanMemberAdapter'
Adapters.adpater[197].obtype = []
Adapters.adpater[197].obtype.insert(0, None)
Adapters.adpater[197].obtype[0] = 'account'
Adapters.adpater.insert(198, None)
Adapters.adpater[198] = Dummy()
Adapters.adpater[198].ifacename = 'IExchangeXPRate'
Adapters.adpater[198].module = 'adapters.IExchangeXPRateAdapter.IExchangeXPRateAdapter'
Adapters.adpater[198].obtype = []
Adapters.adpater[198].obtype.insert(0, None)
Adapters.adpater[198].obtype[0] = 'account'
Adapters.adpater.insert(199, None)
Adapters.adpater[199] = Dummy()
Adapters.adpater[199].ifacename = 'IAchieveGroups'
Adapters.adpater[199].module = 'adapters.IAchieveGroupsAdapter.IAchieveGroupsAdapter'
Adapters.adpater[199].obtype = []
Adapters.adpater[199].obtype.insert(0, None)
Adapters.adpater[199].obtype[0] = 'account'
Adapters.adpater.insert(200, None)
Adapters.adpater[200] = Dummy()
Adapters.adpater[200].ifacename = 'IHangarSpaces'
Adapters.adpater[200].module = 'adapters.IHangarSpacesAdapter.IHangarSpacesAdapter'
Adapters.adpater[200].obtype = []
Adapters.adpater[200].obtype.insert(0, None)
Adapters.adpater[200].obtype[0] = 'account'
Adapters.adpater.insert(201, None)
Adapters.adpater[201] = Dummy()
Adapters.adpater[201].ifacename = 'IHangarSpacesHash'
Adapters.adpater[201].module = 'adapters.IHangarSpacesHashAdapter.IHangarSpacesHashAdapter'
Adapters.adpater[201].obtype = []
Adapters.adpater[201].obtype.insert(0, None)
Adapters.adpater[201].obtype[0] = 'account'
Adapters.adpater.insert(202, None)
Adapters.adpater[202] = Dummy()
Adapters.adpater[202].ifacename = 'ICurrentHangarSpace'
Adapters.adpater[202].module = 'adapters.ICurrentHangarSpaceAdapter.ICurrentHangarSpaceAccountAdapter'
Adapters.adpater[202].obtype = []
Adapters.adpater[202].obtype.insert(0, None)
Adapters.adpater[202].obtype[0] = 'account'
Adapters.adpater.insert(203, None)
Adapters.adpater[203] = Dummy()
Adapters.adpater[203].ifacename = 'ICurrentHangarSpace'
Adapters.adpater[203].module = 'adapters.ICurrentHangarSpaceAdapter.ICurrentHangarSpacePreviewAdapter'
Adapters.adpater[203].obtype = []
Adapters.adpater[203].obtype.insert(0, None)
Adapters.adpater[203].obtype[0] = 'preview'
Adapters.adpater.insert(204, None)
Adapters.adpater[204] = Dummy()
Adapters.adpater[204].ifacename = 'IError'
Adapters.adpater[204].module = 'adapters.IErrorAdapter.IErrorAdapter'
Adapters.adpater[204].obtype = []
Adapters.adpater[204].obtype.insert(0, None)
Adapters.adpater[204].obtype[0] = 'error'
Adapters.adpater.insert(205, None)
Adapters.adpater[205] = Dummy()
Adapters.adpater[205].ifacename = 'IActiveEvents'
Adapters.adpater[205].module = 'adapters.IActiveEventsAdapter.IActiveEventsAdapter'
Adapters.adpater[205].obtype = []
Adapters.adpater[205].obtype.insert(0, None)
Adapters.adpater[205].obtype[0] = 'account'
Adapters.adpater.insert(206, None)
Adapters.adpater[206] = Dummy()
Adapters.adpater[206].ifacename = 'IAccountClanData'
Adapters.adpater[206].module = 'adapters.IAccountClanDataAdapter.IAccountClanDataAdapter'
Adapters.adpater[206].obtype = []
Adapters.adpater[206].obtype.insert(0, None)
Adapters.adpater[206].obtype[0] = 'account'
Adapters.adpater.insert(207, None)
Adapters.adpater[207] = Dummy()
Adapters.adpater[207].ifacename = 'IAutoFindSquad'
Adapters.adpater[207].module = 'adapters.IAutoFindSquadAdapter.IAutoFindSquadAdapter'
Adapters.adpater[207].obtype = []
Adapters.adpater[207].obtype.insert(0, None)
Adapters.adpater[207].obtype[0] = 'account'
Adapters.adpater.insert(208, None)
Adapters.adpater[208] = Dummy()
Adapters.adpater[208].ifacename = 'IAutoFindSquadList'
Adapters.adpater[208].module = 'adapters.IAutoFindSquadListAdapter.IAutoFindSquadListAdapter'
Adapters.adpater[208].obtype = []
Adapters.adpater[208].obtype.insert(0, None)
Adapters.adpater[208].obtype[0] = 'account'
Adapters.adpater.insert(209, None)
Adapters.adpater[209] = Dummy()
Adapters.adpater[209].ifacename = 'IPlaneBirthday'
Adapters.adpater[209].module = 'adapters.IPlaneBirthdayAdapter.IPlaneBirthdayAdapter'
Adapters.adpater[209].obtype = []
Adapters.adpater[209].obtype.insert(0, None)
Adapters.adpater[209].obtype[0] = 'plane'
Adapters.adpater.insert(210, None)
Adapters.adpater[210] = Dummy()
Adapters.adpater[210].ifacename = 'IPlaneBirthdayBonus'
Adapters.adpater[210].module = 'adapters.IPlaneBirthdayBonusAdapter.IPlaneBirthdayBonusAdapter'
Adapters.adpater[210].obtype = []
Adapters.adpater[210].obtype.insert(0, None)
Adapters.adpater[210].obtype[0] = 'plane'
Adapters.adpater[210].obtype.insert(1, None)
Adapters.adpater[210].obtype[1] = 'birthday'
Adapters.adpater.insert(211, None)
Adapters.adpater[211] = Dummy()
Adapters.adpater[211].ifacename = 'IPlaneBirthdayProgress'
Adapters.adpater[211].module = 'adapters.IPlaneBirthdayProgressAdapter.IPlaneBirthdayProgressAdapter'
Adapters.adpater[211].obtype = []
Adapters.adpater[211].obtype.insert(0, None)
Adapters.adpater[211].obtype[0] = 'plane'
Adapters.adpater[211].obtype.insert(1, None)
Adapters.adpater[211].obtype[1] = 'birthday'
Adapters.adpater.insert(212, None)
Adapters.adpater[212] = Dummy()
Adapters.adpater[212].ifacename = 'IInterview'
Adapters.adpater[212].module = 'adapters.IInterviewAdapter.IInterviewAdapter'
Adapters.adpater[212].obtype = []
Adapters.adpater[212].obtype.insert(0, None)
Adapters.adpater[212].obtype[0] = 'account'
Adapters.adpater.insert(213, None)
Adapters.adpater[213] = Dummy()
Adapters.adpater[213].ifacename = 'ITicketPrice'
Adapters.adpater[213].module = 'adapters.ITicketPriceAdapter.ITicketPriceAdapter'
Adapters.adpater[213].obtype = []
Adapters.adpater[213].obtype.insert(0, None)
Adapters.adpater[213].obtype[0] = 'plane'
Adapters.adpater.insert(214, None)
Adapters.adpater[214] = Dummy()
Adapters.adpater[214].ifacename = 'ITicketPrice'
Adapters.adpater[214].module = 'adapters.ITicketPriceAdapter.ITicketPriceUpgradeAdapter'
Adapters.adpater[214].obtype = []
Adapters.adpater[214].obtype.insert(0, None)
Adapters.adpater[214].obtype[0] = 'consumable'
Adapters.adpater.insert(215, None)
Adapters.adpater[215] = Dummy()
Adapters.adpater[215].ifacename = 'ITicketPrice'
Adapters.adpater[215].module = 'adapters.ITicketPriceAdapter.ITicketPriceUpgradeAdapter'
Adapters.adpater[215].obtype = []
Adapters.adpater[215].obtype.insert(0, None)
Adapters.adpater[215].obtype[0] = 'equipment'
Adapters.adpater.insert(216, None)
Adapters.adpater[216] = Dummy()
Adapters.adpater[216].ifacename = 'IModifiers'
Adapters.adpater[216].module = 'adapters.IModifiersAdapter.IModifiersUpgradeAdapter'
Adapters.adpater[216].obtype = []
Adapters.adpater[216].obtype.insert(0, None)
Adapters.adpater[216].obtype[0] = 'consumable'
Adapters.adpater.insert(217, None)
Adapters.adpater[217] = Dummy()
Adapters.adpater[217].ifacename = 'IModifiers'
Adapters.adpater[217].module = 'adapters.IModifiersAdapter.IModifiersUpgradeAdapter'
Adapters.adpater[217].obtype = []
Adapters.adpater[217].obtype.insert(0, None)
Adapters.adpater[217].obtype[0] = 'equipment'
Adapters.adpater.insert(218, None)
Adapters.adpater[218] = Dummy()
Adapters.adpater[218].ifacename = 'IGoldDiscount'
Adapters.adpater[218].module = 'adapters.IGoldDiscountAdapter.IGoldDiscountAdapter'
Adapters.adpater[218].obtype = []
Adapters.adpater[218].obtype.insert(0, None)
Adapters.adpater[218].obtype[0] = 'plane'
Adapters.adpater.insert(219, None)
Adapters.adpater[219] = Dummy()
Adapters.adpater[219].ifacename = 'ITicketPlanes'
Adapters.adpater[219].module = 'adapters.ITicketPlanesAdapter.ITicketPlanesAdapter'
Adapters.adpater[219].obtype = []
Adapters.adpater[219].obtype.insert(0, None)
Adapters.adpater[219].obtype[0] = 'account'
Adapters.adpater.insert(220, None)
Adapters.adpater[220] = Dummy()
Adapters.adpater[220].ifacename = 'IExchangeTicketPrice'
Adapters.adpater[220].module = 'adapters.IExchangeTicketPriceAdapter.IExchangeTicketPriceAdapter'
Adapters.adpater[220].obtype = []
Adapters.adpater[220].obtype.insert(0, None)
Adapters.adpater[220].obtype[0] = 'account'
Adapters.adpater.insert(221, None)
Adapters.adpater[221] = Dummy()
Adapters.adpater[221].ifacename = 'IExchangeGoldTicket'
Adapters.adpater[221].module = 'adapters.IExchangeGoldTicketAdapter.IExchangeGoldTicketAdapter'
Adapters.adpater[221].obtype = []
Adapters.adpater[221].obtype.insert(0, None)
Adapters.adpater[221].obtype[0] = 'account'
Adapters.adpater.insert(222, None)
Adapters.adpater[222] = Dummy()
Adapters.adpater[222].ifacename = 'ISkinnerBoxEndAction'
Adapters.adpater[222].module = 'adapters.ISkinnerBoxEndActionAdapter.ISkinnerBoxEndActionAdapter'
Adapters.adpater[222].obtype = []
Adapters.adpater[222].obtype.insert(0, None)
Adapters.adpater[222].obtype[0] = 'account'
Adapters.adpater.insert(223, None)
Adapters.adpater[223] = Dummy()
Adapters.adpater[223].ifacename = 'IPlaneBirthdayEnabled'
Adapters.adpater[223].module = 'adapters.IPlaneBirthdayEnabledAdapter.IPlaneBirthdayEnabledAdapter'
Adapters.adpater[223].obtype = []
Adapters.adpater[223].obtype.insert(0, None)
Adapters.adpater[223].obtype[0] = 'account'
Adapters.adpater.insert(224, None)
Adapters.adpater[224] = Dummy()
Adapters.adpater[224].ifacename = 'IRequiredExperience'
Adapters.adpater[224].module = 'adapters.IRequiredExperienceAdapter.IRequiredExperienceAdapter'
Adapters.adpater[224].obtype = []
Adapters.adpater[224].obtype.insert(0, None)
Adapters.adpater[224].obtype[0] = 'plane'
Adapters.adpater.insert(225, None)
Adapters.adpater[225] = Dummy()
Adapters.adpater[225].ifacename = 'IPlaneWeapons'
Adapters.adpater[225].module = 'adapters.IPlaneWeaponsAdapter.IPlaneWeaponsAdapter'
Adapters.adpater[225].obtype = []
Adapters.adpater[225].obtype.insert(0, None)
Adapters.adpater[225].obtype[0] = 'plane'
Adapters.adpater.insert(226, None)
Adapters.adpater[226] = Dummy()
Adapters.adpater[226].ifacename = 'IPlaneWeapons'
Adapters.adpater[226].module = 'adapters.IPlaneWeaponsAdapter.IPlaneWeaponsForConfigAdapter'
Adapters.adpater[226].obtype = []
Adapters.adpater[226].obtype.insert(0, None)
Adapters.adpater[226].obtype[0] = 'planePreset'
Adapters.adpater.insert(227, None)
Adapters.adpater[227] = Dummy()
Adapters.adpater[227].ifacename = 'IWeaponInfo'
Adapters.adpater[227].module = 'adapters.IWeaponInfoAdapter.IWeaponInfoAdapter'
Adapters.adpater[227].obtype = []
Adapters.adpater[227].obtype.insert(0, None)
Adapters.adpater[227].obtype[0] = 'plane'
Adapters.adpater[227].obtype.insert(1, None)
Adapters.adpater[227].obtype[1] = 'weaponslot'
Adapters.adpater[227].obtype.insert(2, None)
Adapters.adpater[227].obtype[2] = 'weaponConfig'
Adapters.adpater.insert(228, None)
Adapters.adpater[228] = Dummy()
Adapters.adpater[228].ifacename = 'IPremiumCost'
Adapters.adpater[228].module = 'adapters.IPremiumCostAdapter.IPremiumCostAdapter'
Adapters.adpater[228].obtype = []
Adapters.adpater[228].obtype.insert(0, None)
Adapters.adpater[228].obtype[0] = 'account'
Adapters.adpater.insert(229, None)
Adapters.adpater[229] = Dummy()
Adapters.adpater[229].ifacename = 'IWaitingScreen'
Adapters.adpater[229].module = 'adapters.IWaitingScreenAdapter.IWaitingScreenAdapter'
Adapters.adpater[229].obtype = []
Adapters.adpater[229].obtype.insert(0, None)
Adapters.adpater[229].obtype[0] = 'account'
Adapters.adpater.insert(230, None)
Adapters.adpater[230] = Dummy()
Adapters.adpater[230].ifacename = 'IAvaregeTime'
Adapters.adpater[230].module = 'adapters.IAvaregeTimeAdapter.IAvaregeTimeAdapter'
Adapters.adpater[230].obtype = []
Adapters.adpater[230].obtype.insert(0, None)
Adapters.adpater[230].obtype[0] = 'plane'
Adapters.adpater[230].obtype.insert(1, None)
Adapters.adpater[230].obtype[1] = 'arenaType'
Adapters.adpater.insert(231, None)
Adapters.adpater[231] = Dummy()
Adapters.adpater[231].ifacename = 'IAvaregeTime'
Adapters.adpater[231].module = 'adapters.IAvaregeTimeAdapter.IAvaregeTimeAdapter'
Adapters.adpater[231].obtype = []
Adapters.adpater[231].obtype.insert(0, None)
Adapters.adpater[231].obtype[0] = 'squad'
Adapters.adpater[231].obtype.insert(1, None)
Adapters.adpater[231].obtype[1] = 'arenaType'
Adapters.adpater.insert(232, None)
Adapters.adpater[232] = Dummy()
Adapters.adpater[232].ifacename = 'IReferralStatus'
Adapters.adpater[232].module = 'adapters.IReferral.IReferralStatusAdapter'
Adapters.adpater[232].obtype = []
Adapters.adpater[232].obtype.insert(0, None)
Adapters.adpater[232].obtype[0] = 'account'
Adapters.adpater.insert(233, None)
Adapters.adpater[233] = Dummy()
Adapters.adpater[233].ifacename = 'IReferralDescription'
Adapters.adpater[233].module = 'adapters.IReferral.IReferralDescriptionAdapter'
Adapters.adpater[233].obtype = []
Adapters.adpater[233].obtype.insert(0, None)
Adapters.adpater[233].obtype[0] = 'account'
Adapters.adpater.insert(234, None)
Adapters.adpater[234] = Dummy()
Adapters.adpater[234].ifacename = 'IReferralLinks'
Adapters.adpater[234].module = 'adapters.IReferral.IReferralLinksAdapter'
Adapters.adpater[234].obtype = []
Adapters.adpater[234].obtype.insert(0, None)
Adapters.adpater[234].obtype[0] = 'account'
Adapters.adpater.insert(235, None)
Adapters.adpater[235] = Dummy()
Adapters.adpater[235].ifacename = 'IReferralRecruitStatus'
Adapters.adpater[235].module = 'adapters.IReferral.IReferralRecruitStatusAdapter'
Adapters.adpater[235].obtype = []
Adapters.adpater[235].obtype.insert(0, None)
Adapters.adpater[235].obtype[0] = 'account'
Adapters.adpater.insert(236, None)
Adapters.adpater[236] = Dummy()
Adapters.adpater[236].ifacename = 'IReferralRecruitArchiveStatus'
Adapters.adpater[236].module = 'adapters.IReferral.IReferralRecruitArchiveStatusAdapter'
Adapters.adpater[236].obtype = []
Adapters.adpater[236].obtype.insert(0, None)
Adapters.adpater[236].obtype[0] = 'account'
Adapters.adpater.insert(237, None)
Adapters.adpater[237] = Dummy()
Adapters.adpater[237].ifacename = 'IReferralRecruitOnlineStatus'
Adapters.adpater[237].module = 'adapters.IReferral.IReferralRecruitOnlineStatusAdapter'
Adapters.adpater[237].obtype = []
Adapters.adpater[237].obtype.insert(0, None)
Adapters.adpater[237].obtype[0] = 'account'
Adapters.adpater.insert(238, None)
Adapters.adpater[238] = Dummy()
Adapters.adpater[238].ifacename = 'IReferralInviteLink'
Adapters.adpater[238].module = 'adapters.IReferralClient.IReferralInviteLinkAdapter'
Adapters.adpater[238].obtype = []
Adapters.adpater[238].obtype.insert(0, None)
Adapters.adpater[238].obtype[0] = 'account'
Adapters.adpater.insert(239, None)
Adapters.adpater[239] = Dummy()
Adapters.adpater[239].ifacename = 'IReferralRecruitTasks'
Adapters.adpater[239].module = 'adapters.IReferralRecruitTasks.IReferralRecruitTasksAdapter'
Adapters.adpater[239].obtype = []
Adapters.adpater[239].obtype.insert(0, None)
Adapters.adpater[239].obtype[0] = 'account'
Adapters.adpater.insert(240, None)
Adapters.adpater[240] = Dummy()
Adapters.adpater[240].ifacename = 'IReferralCheckpointBonus'
Adapters.adpater[240].module = 'adapters.IReferralRecruitTasks.IReferralCheckpointBonusAdapter'
Adapters.adpater[240].obtype = []
Adapters.adpater[240].obtype.insert(0, None)
Adapters.adpater[240].obtype[0] = 'refcheckpoint'
Adapters.adpater.insert(241, None)
Adapters.adpater[241] = Dummy()
Adapters.adpater[241].ifacename = 'IReferralCheckpointGetBonus'
Adapters.adpater[241].module = 'adapters.IReferralRecruitTasks.IReferralCheckpointGetBonusAdapter'
Adapters.adpater[241].obtype = []
Adapters.adpater[241].obtype.insert(0, None)
Adapters.adpater[241].obtype[0] = 'questoperation'
Adapters.adpater.insert(242, None)
Adapters.adpater[242] = Dummy()
Adapters.adpater[242].ifacename = 'IReferralRecruiterQuests'
Adapters.adpater[242].module = 'adapters.IReferralRecruiterQuests.IReferralRecruiterQuestsAdapter'
Adapters.adpater[242].obtype = []
Adapters.adpater[242].obtype.insert(0, None)
Adapters.adpater[242].obtype[0] = 'account'
Adapters.adpater.insert(243, None)
Adapters.adpater[243] = Dummy()
Adapters.adpater[243].ifacename = 'IReferralQuestDescription'
Adapters.adpater[243].module = 'adapters.IReferralRecruiterQuests.IReferralQuestDescriptionAdapter'
Adapters.adpater[243].obtype = []
Adapters.adpater[243].obtype.insert(0, None)
Adapters.adpater[243].obtype[0] = 'referralquest'
Adapters.adpater.insert(244, None)
Adapters.adpater[244] = Dummy()
Adapters.adpater[244].ifacename = 'IReferralQuestStatus'
Adapters.adpater[244].module = 'adapters.IReferralRecruiterQuests.IReferralQuestStatusAdapter'
Adapters.adpater[244].obtype = []
Adapters.adpater[244].obtype.insert(0, None)
Adapters.adpater[244].obtype[0] = 'referralquest'
Adapters.adpater.insert(245, None)
Adapters.adpater[245] = Dummy()
Adapters.adpater[245].ifacename = 'IReferralQuestGetBonus'
Adapters.adpater[245].module = 'adapters.IReferralRecruiterQuests.IReferralQuestGetBonusAdapter'
Adapters.adpater[245].obtype = []
Adapters.adpater[245].obtype.insert(0, None)
Adapters.adpater[245].obtype[0] = 'questoperation'
Adapters.adpater.insert(246, None)
Adapters.adpater[246] = Dummy()
Adapters.adpater[246].ifacename = 'IReferralSendInvite'
Adapters.adpater[246].module = 'adapters.IReferral.IReferralSendInviteAdapter'
Adapters.adpater[246].obtype = []
Adapters.adpater[246].obtype.insert(0, None)
Adapters.adpater[246].obtype[0] = 'referralinvite'
Adapters.adpater.insert(247, None)
Adapters.adpater[247] = Dummy()
Adapters.adpater[247].ifacename = 'IReferralPublicInvite'
Adapters.adpater[247].module = 'adapters.IReferralClient.IReferralPublicInviteAdapter'
Adapters.adpater[247].obtype = []
Adapters.adpater[247].obtype.insert(0, None)
Adapters.adpater[247].obtype[0] = 'referralinvite'
Adapters.adpater.insert(248, None)
Adapters.adpater[248] = Dummy()
Adapters.adpater[248].ifacename = 'IWarActionState'
Adapters.adpater[248].module = 'adapters.IWarAction.IWarActionState'
Adapters.adpater[248].obtype = []
Adapters.adpater[248].obtype.insert(0, None)
Adapters.adpater[248].obtype[0] = 'account'
Adapters.adpater.insert(249, None)
Adapters.adpater[249] = Dummy()
Adapters.adpater[249].ifacename = 'IWarActionForce'
Adapters.adpater[249].module = 'adapters.IWarAction.IWarActionForce'
Adapters.adpater[249].obtype = []
Adapters.adpater[249].obtype.insert(0, None)
Adapters.adpater[249].obtype[0] = 'account'
Adapters.adpater.insert(250, None)
Adapters.adpater[250] = Dummy()
Adapters.adpater[250].ifacename = 'IWarActionFraction'
Adapters.adpater[250].module = 'adapters.IWarAction.IWarActionFraction'
Adapters.adpater[250].obtype = []
Adapters.adpater[250].obtype.insert(0, None)
Adapters.adpater[250].obtype[0] = 'account'
Adapters.adpater.insert(251, None)
Adapters.adpater[251] = Dummy()
Adapters.adpater[251].ifacename = 'IWarActionInfo'
Adapters.adpater[251].module = 'adapters.IWarAction.IWarActionInfo'
Adapters.adpater[251].obtype = []
Adapters.adpater[251].obtype.insert(0, None)
Adapters.adpater[251].obtype[0] = 'account'
Adapters.adpater.insert(252, None)
Adapters.adpater[252] = Dummy()
Adapters.adpater[252].ifacename = 'IWarActionBattleStats'
Adapters.adpater[252].module = 'adapters.IWarAction.IWarActionBattleStats'
Adapters.adpater[252].obtype = []
Adapters.adpater[252].obtype.insert(0, None)
Adapters.adpater[252].obtype[0] = 'account'
Adapters.adpater.insert(253, None)
Adapters.adpater[253] = Dummy()
Adapters.adpater[253].ifacename = 'IWarActionAgregatedBattleStats'
Adapters.adpater[253].module = 'adapters.IWarAction.IWarActionAgregatedBattleStats'
Adapters.adpater[253].obtype = []
Adapters.adpater[253].obtype.insert(0, None)
Adapters.adpater[253].obtype[0] = 'account'
Adapters.adpater.insert(254, None)
Adapters.adpater[254] = Dummy()
Adapters.adpater[254].ifacename = 'IWarActionTrophiesStatus'
Adapters.adpater[254].module = 'adapters.IWarAction.IWarActionTrophiesStatus'
Adapters.adpater[254].obtype = []
Adapters.adpater[254].obtype.insert(0, None)
Adapters.adpater[254].obtype[0] = 'account'
Adapters.adpater.insert(255, None)
Adapters.adpater[255] = Dummy()
Adapters.adpater[255].ifacename = 'IWarActionPlaneQuestStatus'
Adapters.adpater[255].module = 'adapters.IWarAction.IWarActionPlaneQuestStatus'
Adapters.adpater[255].obtype = []
Adapters.adpater[255].obtype.insert(0, None)
Adapters.adpater[255].obtype[0] = 'plane'
Adapters.adpater.insert(256, None)
Adapters.adpater[256] = Dummy()
Adapters.adpater[256].ifacename = 'IWarCash'
Adapters.adpater[256].module = 'adapters.IWarCash.IWarCash'
Adapters.adpater[256].obtype = []
Adapters.adpater[256].obtype.insert(0, None)
Adapters.adpater[256].obtype[0] = 'warCash'
Adapters.adpater.insert(257, None)
Adapters.adpater[257] = Dummy()
Adapters.adpater[257].ifacename = 'ILTOStatus'
Adapters.adpater[257].module = 'adapters.ILTOStatusAdapter.ILTOStatusAdapter'
Adapters.adpater[257].obtype = []
Adapters.adpater[257].obtype.insert(0, None)
Adapters.adpater[257].obtype[0] = 'account'
Adapters.adpater.insert(258, None)
Adapters.adpater[258] = Dummy()
Adapters.adpater[258].ifacename = 'ITutorialLessonServer'
Adapters.adpater[258].module = 'adapters.ITutorialLesson.ITutorialLessonServerAdapter'
Adapters.adpater[258].obtype = []
Adapters.adpater[258].obtype.insert(0, None)
Adapters.adpater[258].obtype[0] = 'tutorial'
Adapters.adpater.insert(259, None)
Adapters.adpater[259] = Dummy()
Adapters.adpater[259].ifacename = 'ITutorialLessonClient'
Adapters.adpater[259].module = 'adapters.ITutorialLesson.ITutorialLessonClientAdapter'
Adapters.adpater[259].obtype = []
Adapters.adpater[259].obtype.insert(0, None)
Adapters.adpater[259].obtype[0] = 'tutorial'
Adapters.adpater.insert(260, None)
Adapters.adpater[260] = Dummy()
Adapters.adpater[260].ifacename = 'ITutorialLessonList'
Adapters.adpater[260].module = 'adapters.ITutorialLesson.ITutorialLessonListAdapter'
Adapters.adpater[260].obtype = []
Adapters.adpater[260].obtype.insert(0, None)
Adapters.adpater[260].obtype[0] = 'account'
Adapters.adpater.insert(261, None)
Adapters.adpater[261] = Dummy()
Adapters.adpater[261].ifacename = 'ITutorialPromptParams'
Adapters.adpater[261].module = 'adapters.ITutorialLesson.ITutorialPromptParamsAdapter'
Adapters.adpater[261].obtype = []
Adapters.adpater[261].obtype.insert(0, None)
Adapters.adpater[261].obtype[0] = 'tutorial'
Adapters.adpater.insert(262, None)
Adapters.adpater[262] = Dummy()
Adapters.adpater[262].ifacename = 'ITutorialLessonWindow'
Adapters.adpater[262].module = 'adapters.ITutorialLesson.ITutorialLessonWindowAdapter'
Adapters.adpater[262].obtype = []
Adapters.adpater[262].obtype.insert(0, None)
Adapters.adpater[262].obtype[0] = 'account'
Adapters.adpater.insert(263, None)
Adapters.adpater[263] = Dummy()
Adapters.adpater[263].ifacename = 'IDebugCommand'
Adapters.adpater[263].module = 'adapters.IDebugCommand.IDebugCommand'
Adapters.adpater[263].obtype = []
Adapters.adpater[263].obtype.insert(0, None)
Adapters.adpater[263].obtype[0] = 'account'
Adapters.adpater.insert(264, None)
Adapters.adpater[264] = Dummy()
Adapters.adpater[264].ifacename = 'IPack'
Adapters.adpater[264].module = 'adapters.IPackAdapter.IPackAdapter'
Adapters.adpater[264].obtype = []
Adapters.adpater[264].obtype.insert(0, None)
Adapters.adpater[264].obtype[0] = 'pack'
Adapters.adpater.insert(265, None)
Adapters.adpater[265] = Dummy()
Adapters.adpater[265].ifacename = 'IStatus'
Adapters.adpater[265].module = 'adapters.IPackAdapter.IPackStatusAdapter'
Adapters.adpater[265].obtype = []
Adapters.adpater[265].obtype.insert(0, None)
Adapters.adpater[265].obtype[0] = 'pack'
Adapters.adpater.insert(266, None)
Adapters.adpater[266] = Dummy()
Adapters.adpater[266].ifacename = 'IPrice'
Adapters.adpater[266].module = 'adapters.IPackAdapter.IPackPriceAdapter'
Adapters.adpater[266].obtype = []
Adapters.adpater[266].obtype.insert(0, None)
Adapters.adpater[266].obtype[0] = 'pack'
Adapters.adpater.insert(267, None)
Adapters.adpater[267] = Dummy()
Adapters.adpater[267].ifacename = 'IFemalePilotPackList'
Adapters.adpater[267].module = 'adapters.IFemalePilotPackListAdapter.IFemalePilotPackListAdapter'
Adapters.adpater[267].obtype = []
Adapters.adpater[267].obtype.insert(0, None)
Adapters.adpater[267].obtype[0] = 'account'