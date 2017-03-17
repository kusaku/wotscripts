# Embedded file name: scripts/common/exchangeapi/_oblocations.py
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


Objects = Dummy()
Objects.object = []
Objects.object.insert(0, None)
Objects.object[0] = Dummy()
Objects.object[0].ifacename = 'ISquad'
Objects.object[0].oblocation = 'server'
Objects.object[0].obtype = []
Objects.object[0].obtype.insert(0, None)
Objects.object[0].obtype[0] = 'squad'
Objects.object[0].requestsRate = []
Objects.object.insert(1, None)
Objects.object[1] = Dummy()
Objects.object[1].ifacename = 'ISquadMember'
Objects.object[1].oblocation = 'server'
Objects.object[1].obtype = []
Objects.object[1].obtype.insert(0, None)
Objects.object[1].obtype[0] = 'squadmember'
Objects.object[1].requestsRate = []
Objects.object.insert(2, None)
Objects.object[2] = Dummy()
Objects.object[2].ifacename = 'ISquadMember'
Objects.object[2].oblocation = 'server'
Objects.object[2].obtype = []
Objects.object[2].obtype.insert(0, None)
Objects.object[2].obtype[0] = 'squadmember'
Objects.object[2].obtype.insert(1, None)
Objects.object[2].obtype[1] = 'periphery'
Objects.object[2].requestsRate = []
Objects.object.insert(3, None)
Objects.object[3] = Dummy()
Objects.object[3].ifacename = 'ISquadInvitation'
Objects.object[3].oblocation = 'server'
Objects.object[3].obtype = []
Objects.object[3].obtype.insert(0, None)
Objects.object[3].obtype[0] = 'squadmember'
Objects.object[3].requestsRate = []
Objects.object.insert(4, None)
Objects.object[4] = Dummy()
Objects.object[4].ifacename = 'ISquadInvitation'
Objects.object[4].oblocation = 'server'
Objects.object[4].obtype = []
Objects.object[4].obtype.insert(0, None)
Objects.object[4].obtype[0] = 'squadmember'
Objects.object[4].obtype.insert(1, None)
Objects.object[4].obtype[1] = 'periphery'
Objects.object[4].requestsRate = []
Objects.object.insert(5, None)
Objects.object[5] = Dummy()
Objects.object[5].ifacename = 'IBattleState'
Objects.object[5].oblocation = 'server'
Objects.object[5].obtype = []
Objects.object[5].obtype.insert(0, None)
Objects.object[5].obtype[0] = 'squad'
Objects.object[5].requestsRate = []
Objects.object.insert(6, None)
Objects.object[6] = Dummy()
Objects.object[6].ifacename = 'IBattleState'
Objects.object[6].oblocation = 'server'
Objects.object[6].obtype = []
Objects.object[6].obtype.insert(0, None)
Objects.object[6].obtype[0] = 'account'
Objects.object[6].requestsRate = []
Objects.object.insert(7, None)
Objects.object[7] = Dummy()
Objects.object[7].ifacename = 'ISquadChatChannel'
Objects.object[7].oblocation = 'server'
Objects.object[7].obtype = []
Objects.object[7].obtype.insert(0, None)
Objects.object[7].obtype[0] = 'squad'
Objects.object[7].requestsRate = []
Objects.object.insert(8, None)
Objects.object[8] = Dummy()
Objects.object[8].ifacename = 'ICurrentPatch'
Objects.object[8].oblocation = 'server'
Objects.object[8].obtype = []
Objects.object[8].obtype.insert(0, None)
Objects.object[8].obtype[0] = 'patch'
Objects.object[8].requestsRate = []
Objects.object.insert(9, None)
Objects.object[9] = Dummy()
Objects.object[9].ifacename = 'ISlotsCount'
Objects.object[9].oblocation = 'server'
Objects.object[9].obtype = []
Objects.object[9].obtype.insert(0, None)
Objects.object[9].obtype[0] = 'account'
Objects.object[9].requestsRate = []
Objects.object.insert(10, None)
Objects.object[10] = Dummy()
Objects.object[10].ifacename = 'IPatch'
Objects.object[10].oblocation = 'server'
Objects.object[10].obtype = []
Objects.object[10].obtype.insert(0, None)
Objects.object[10].obtype[0] = 'patch'
Objects.object[10].requestsRate = []
Objects.object.insert(11, None)
Objects.object[11] = Dummy()
Objects.object[11].ifacename = 'IPatch'
Objects.object[11].oblocation = 'server'
Objects.object[11].obtype = []
Objects.object[11].obtype.insert(0, None)
Objects.object[11].obtype[0] = 'patch'
Objects.object[11].obtype.insert(1, None)
Objects.object[11].obtype[1] = 'plane'
Objects.object[11].requestsRate = []
Objects.object.insert(12, None)
Objects.object[12] = Dummy()
Objects.object[12].ifacename = 'IPatch'
Objects.object[12].oblocation = 'server'
Objects.object[12].obtype = []
Objects.object[12].obtype.insert(0, None)
Objects.object[12].obtype[0] = 'patch'
Objects.object[12].obtype.insert(1, None)
Objects.object[12].obtype[1] = 'consumable'
Objects.object[12].requestsRate = []
Objects.object.insert(13, None)
Objects.object[13] = Dummy()
Objects.object[13].ifacename = 'IPatch'
Objects.object[13].oblocation = 'server'
Objects.object[13].obtype = []
Objects.object[13].obtype.insert(0, None)
Objects.object[13].obtype[0] = 'patch'
Objects.object[13].obtype.insert(1, None)
Objects.object[13].obtype[1] = 'equipment'
Objects.object[13].requestsRate = []
Objects.object.insert(14, None)
Objects.object[14] = Dummy()
Objects.object[14].ifacename = 'IPatch'
Objects.object[14].oblocation = 'server'
Objects.object[14].obtype = []
Objects.object[14].obtype.insert(0, None)
Objects.object[14].obtype[0] = 'patch'
Objects.object[14].obtype.insert(1, None)
Objects.object[14].obtype[1] = 'ammobelt'
Objects.object[14].requestsRate = []
Objects.object.insert(15, None)
Objects.object[15] = Dummy()
Objects.object[15].ifacename = 'IPatch'
Objects.object[15].oblocation = 'server'
Objects.object[15].obtype = []
Objects.object[15].obtype.insert(0, None)
Objects.object[15].obtype[0] = 'patch'
Objects.object[15].obtype.insert(1, None)
Objects.object[15].obtype[1] = 'goldPrice'
Objects.object[15].requestsRate = []
Objects.object.insert(16, None)
Objects.object[16] = Dummy()
Objects.object[16].ifacename = 'ILastMessages'
Objects.object[16].oblocation = 'server'
Objects.object[16].obtype = []
Objects.object[16].obtype.insert(0, None)
Objects.object[16].obtype[0] = 'account'
Objects.object[16].requestsRate = []
Objects.object.insert(17, None)
Objects.object[17] = Dummy()
Objects.object[17].ifacename = 'IMessage'
Objects.object[17].oblocation = 'mixed'
Objects.object[17].obtype = []
Objects.object[17].obtype.insert(0, None)
Objects.object[17].obtype[0] = 'message'
Objects.object[17].requestsRate = []
Objects.object.insert(18, None)
Objects.object[18] = Dummy()
Objects.object[18].ifacename = 'IMessage'
Objects.object[18].oblocation = 'client'
Objects.object[18].obtype = []
Objects.object[18].obtype.insert(0, None)
Objects.object[18].obtype[0] = 'uimessage'
Objects.object[18].requestsRate = []
Objects.object.insert(19, None)
Objects.object[19] = Dummy()
Objects.object[19].ifacename = 'IMessageAction'
Objects.object[19].oblocation = 'mixed'
Objects.object[19].obtype = []
Objects.object[19].obtype.insert(0, None)
Objects.object[19].obtype[0] = 'messageAction'
Objects.object[19].requestsRate = []
Objects.object.insert(20, None)
Objects.object[20] = Dummy()
Objects.object[20].ifacename = 'IMessageSession'
Objects.object[20].oblocation = 'client'
Objects.object[20].obtype = []
Objects.object[20].obtype.insert(0, None)
Objects.object[20].obtype[0] = 'account'
Objects.object[20].requestsRate = []
Objects.object.insert(21, None)
Objects.object[21] = Dummy()
Objects.object[21].ifacename = 'IPlanes'
Objects.object[21].oblocation = 'client'
Objects.object[21].obtype = []
Objects.object[21].obtype.insert(0, None)
Objects.object[21].obtype[0] = 'account'
Objects.object[21].requestsRate = []
Objects.object.insert(22, None)
Objects.object[22] = Dummy()
Objects.object[22].ifacename = 'IPlanes'
Objects.object[22].oblocation = 'server'
Objects.object[22].obtype = []
Objects.object[22].obtype.insert(0, None)
Objects.object[22].obtype[0] = 'equipment'
Objects.object[22].requestsRate = []
Objects.object.insert(23, None)
Objects.object[23] = Dummy()
Objects.object[23].ifacename = 'IClass'
Objects.object[23].oblocation = 'mixed'
Objects.object[23].obtype = []
Objects.object[23].obtype.insert(0, None)
Objects.object[23].obtype[0] = 'plane'
Objects.object[23].requestsRate = []
Objects.object.insert(24, None)
Objects.object[24] = Dummy()
Objects.object[24].ifacename = 'IStatus'
Objects.object[24].oblocation = 'server'
Objects.object[24].obtype = []
Objects.object[24].obtype.insert(0, None)
Objects.object[24].obtype[0] = 'plane'
Objects.object[24].requestsRate = []
Objects.object.insert(25, None)
Objects.object[25] = Dummy()
Objects.object[25].ifacename = 'IStatus'
Objects.object[25].oblocation = 'server'
Objects.object[25].obtype = []
Objects.object[25].obtype.insert(0, None)
Objects.object[25].obtype[0] = 'bomb'
Objects.object[25].requestsRate = []
Objects.object.insert(26, None)
Objects.object[26] = Dummy()
Objects.object[26].ifacename = 'IStatus'
Objects.object[26].oblocation = 'server'
Objects.object[26].obtype = []
Objects.object[26].obtype.insert(0, None)
Objects.object[26].obtype[0] = 'rocket'
Objects.object[26].requestsRate = []
Objects.object.insert(27, None)
Objects.object[27] = Dummy()
Objects.object[27].ifacename = 'IStatus'
Objects.object[27].oblocation = 'server'
Objects.object[27].obtype = []
Objects.object[27].obtype.insert(0, None)
Objects.object[27].obtype[0] = 'upgrade'
Objects.object[27].requestsRate = []
Objects.object.insert(28, None)
Objects.object[28] = Dummy()
Objects.object[28].ifacename = 'IStatus'
Objects.object[28].oblocation = 'server'
Objects.object[28].obtype = []
Objects.object[28].obtype.insert(0, None)
Objects.object[28].obtype[0] = 'account'
Objects.object[28].requestsRate = []
Objects.object.insert(29, None)
Objects.object[29] = Dummy()
Objects.object[29].ifacename = 'IName'
Objects.object[29].oblocation = 'client'
Objects.object[29].obtype = []
Objects.object[29].obtype.insert(0, None)
Objects.object[29].obtype[0] = 'plane'
Objects.object[29].requestsRate = []
Objects.object.insert(30, None)
Objects.object[30] = Dummy()
Objects.object[30].ifacename = 'IName'
Objects.object[30].oblocation = 'client'
Objects.object[30].obtype = []
Objects.object[30].obtype.insert(0, None)
Objects.object[30].obtype[0] = 'upgrade'
Objects.object[30].requestsRate = []
Objects.object.insert(31, None)
Objects.object[31] = Dummy()
Objects.object[31].ifacename = 'ILevel'
Objects.object[31].oblocation = 'client'
Objects.object[31].obtype = []
Objects.object[31].obtype.insert(0, None)
Objects.object[31].obtype[0] = 'plane'
Objects.object[31].requestsRate = []
Objects.object.insert(32, None)
Objects.object[32] = Dummy()
Objects.object[32].ifacename = 'ILevel'
Objects.object[32].oblocation = 'client'
Objects.object[32].obtype = []
Objects.object[32].obtype.insert(0, None)
Objects.object[32].obtype[0] = 'upgrade'
Objects.object[32].requestsRate = []
Objects.object.insert(33, None)
Objects.object[33] = Dummy()
Objects.object[33].ifacename = 'IType'
Objects.object[33].oblocation = 'client'
Objects.object[33].obtype = []
Objects.object[33].obtype.insert(0, None)
Objects.object[33].obtype[0] = 'plane'
Objects.object[33].requestsRate = []
Objects.object.insert(34, None)
Objects.object[34] = Dummy()
Objects.object[34].ifacename = 'INation'
Objects.object[34].oblocation = 'client'
Objects.object[34].obtype = []
Objects.object[34].obtype.insert(0, None)
Objects.object[34].obtype[0] = 'plane'
Objects.object[34].requestsRate = []
Objects.object.insert(35, None)
Objects.object[35] = Dummy()
Objects.object[35].ifacename = 'INation'
Objects.object[35].oblocation = 'client'
Objects.object[35].obtype = []
Objects.object[35].obtype.insert(0, None)
Objects.object[35].obtype[0] = 'ammobelt'
Objects.object[35].requestsRate = []
Objects.object.insert(36, None)
Objects.object[36] = Dummy()
Objects.object[36].ifacename = 'INation'
Objects.object[36].oblocation = 'client'
Objects.object[36].obtype = []
Objects.object[36].obtype.insert(0, None)
Objects.object[36].obtype[0] = 'bomb'
Objects.object[36].requestsRate = []
Objects.object.insert(37, None)
Objects.object[37] = Dummy()
Objects.object[37].ifacename = 'INation'
Objects.object[37].oblocation = 'client'
Objects.object[37].obtype = []
Objects.object[37].obtype.insert(0, None)
Objects.object[37].obtype[0] = 'rocket'
Objects.object[37].requestsRate = []
Objects.object.insert(38, None)
Objects.object[38] = Dummy()
Objects.object[38].ifacename = 'INation'
Objects.object[38].oblocation = 'client'
Objects.object[38].obtype = []
Objects.object[38].obtype.insert(0, None)
Objects.object[38].obtype[0] = 'upgrade'
Objects.object[38].requestsRate = []
Objects.object.insert(39, None)
Objects.object[39] = Dummy()
Objects.object[39].ifacename = 'INationList'
Objects.object[39].oblocation = 'client'
Objects.object[39].obtype = []
Objects.object[39].obtype.insert(0, None)
Objects.object[39].obtype[0] = 'consumable'
Objects.object[39].requestsRate = []
Objects.object.insert(40, None)
Objects.object[40] = Dummy()
Objects.object[40].ifacename = 'INationList'
Objects.object[40].oblocation = 'client'
Objects.object[40].obtype = []
Objects.object[40].obtype.insert(0, None)
Objects.object[40].obtype[0] = 'equipment'
Objects.object[40].requestsRate = []
Objects.object.insert(41, None)
Objects.object[41] = Dummy()
Objects.object[41].ifacename = 'IPrice'
Objects.object[41].oblocation = 'client'
Objects.object[41].obtype = []
Objects.object[41].obtype.insert(0, None)
Objects.object[41].obtype[0] = 'plane'
Objects.object[41].requestsRate = []
Objects.object.insert(42, None)
Objects.object[42] = Dummy()
Objects.object[42].ifacename = 'IPrice'
Objects.object[42].oblocation = 'client'
Objects.object[42].obtype = []
Objects.object[42].obtype.insert(0, None)
Objects.object[42].obtype[0] = 'upgrade'
Objects.object[42].requestsRate = []
Objects.object.insert(43, None)
Objects.object[43] = Dummy()
Objects.object[43].ifacename = 'IPrice'
Objects.object[43].oblocation = 'client'
Objects.object[43].obtype = []
Objects.object[43].obtype.insert(0, None)
Objects.object[43].obtype[0] = 'consumable'
Objects.object[43].requestsRate = []
Objects.object.insert(44, None)
Objects.object[44] = Dummy()
Objects.object[44].ifacename = 'IPrice'
Objects.object[44].oblocation = 'client'
Objects.object[44].obtype = []
Objects.object[44].obtype.insert(0, None)
Objects.object[44].obtype[0] = 'equipment'
Objects.object[44].requestsRate = []
Objects.object.insert(45, None)
Objects.object[45] = Dummy()
Objects.object[45].ifacename = 'IPrice'
Objects.object[45].oblocation = 'server'
Objects.object[45].obtype = []
Objects.object[45].obtype.insert(0, None)
Objects.object[45].obtype[0] = 'slot'
Objects.object[45].requestsRate = []
Objects.object.insert(46, None)
Objects.object[46] = Dummy()
Objects.object[46].ifacename = 'ISellPrice'
Objects.object[46].oblocation = 'server'
Objects.object[46].obtype = []
Objects.object[46].obtype.insert(0, None)
Objects.object[46].obtype[0] = 'plane'
Objects.object[46].requestsRate = []
Objects.object.insert(47, None)
Objects.object[47] = Dummy()
Objects.object[47].ifacename = 'ISellPrice'
Objects.object[47].oblocation = 'client'
Objects.object[47].obtype = []
Objects.object[47].obtype.insert(0, None)
Objects.object[47].obtype[0] = 'upgrade'
Objects.object[47].requestsRate = []
Objects.object.insert(48, None)
Objects.object[48] = Dummy()
Objects.object[48].ifacename = 'ISellPrice'
Objects.object[48].oblocation = 'client'
Objects.object[48].obtype = []
Objects.object[48].obtype.insert(0, None)
Objects.object[48].obtype[0] = 'consumable'
Objects.object[48].requestsRate = []
Objects.object.insert(49, None)
Objects.object[49] = Dummy()
Objects.object[49].ifacename = 'ISellPrice'
Objects.object[49].oblocation = 'client'
Objects.object[49].obtype = []
Objects.object[49].obtype.insert(0, None)
Objects.object[49].obtype[0] = 'equipment'
Objects.object[49].requestsRate = []
Objects.object.insert(50, None)
Objects.object[50] = Dummy()
Objects.object[50].ifacename = 'IPlaneDescription'
Objects.object[50].oblocation = 'client'
Objects.object[50].obtype = []
Objects.object[50].obtype.insert(0, None)
Objects.object[50].obtype[0] = 'plane'
Objects.object[50].requestsRate = []
Objects.object.insert(51, None)
Objects.object[51] = Dummy()
Objects.object[51].ifacename = 'IPlanePreset'
Objects.object[51].oblocation = 'client'
Objects.object[51].obtype = []
Objects.object[51].obtype.insert(0, None)
Objects.object[51].obtype[0] = 'planePreset'
Objects.object[51].requestsRate = []
Objects.object.insert(52, None)
Objects.object[52] = Dummy()
Objects.object[52].ifacename = 'IModuleDescription'
Objects.object[52].oblocation = 'client'
Objects.object[52].obtype = []
Objects.object[52].obtype.insert(0, None)
Objects.object[52].obtype[0] = 'upgrade'
Objects.object[52].obtype.insert(1, None)
Objects.object[52].obtype[1] = 'measurementSystem'
Objects.object[52].requestsRate = []
Objects.object.insert(53, None)
Objects.object[53] = Dummy()
Objects.object[53].ifacename = 'IModuleDescription'
Objects.object[53].oblocation = 'client'
Objects.object[53].obtype = []
Objects.object[53].obtype.insert(0, None)
Objects.object[53].obtype[0] = 'upgrade'
Objects.object[53].obtype.insert(1, None)
Objects.object[53].obtype[1] = 'plane'
Objects.object[53].obtype.insert(2, None)
Objects.object[53].obtype[2] = 'measurementSystem'
Objects.object[53].requestsRate = []
Objects.object.insert(54, None)
Objects.object[54] = Dummy()
Objects.object[54].ifacename = 'IModuleDescription'
Objects.object[54].oblocation = 'client'
Objects.object[54].obtype = []
Objects.object[54].obtype.insert(0, None)
Objects.object[54].obtype[0] = 'upgrade'
Objects.object[54].obtype.insert(1, None)
Objects.object[54].obtype[1] = 'weaponslot'
Objects.object[54].obtype.insert(2, None)
Objects.object[54].obtype[2] = 'weaponConfig'
Objects.object[54].obtype.insert(3, None)
Objects.object[54].obtype[3] = 'plane'
Objects.object[54].obtype.insert(4, None)
Objects.object[54].obtype[4] = 'measurementSystem'
Objects.object[54].requestsRate = []
Objects.object.insert(55, None)
Objects.object[55] = Dummy()
Objects.object[55].ifacename = 'IModuleDescription'
Objects.object[55].oblocation = 'client'
Objects.object[55].obtype = []
Objects.object[55].obtype.insert(0, None)
Objects.object[55].obtype[0] = 'upgrade'
Objects.object[55].obtype.insert(1, None)
Objects.object[55].obtype[1] = 'weaponslot'
Objects.object[55].obtype.insert(2, None)
Objects.object[55].obtype[2] = 'weaponConfig'
Objects.object[55].obtype.insert(3, None)
Objects.object[55].obtype[3] = 'upgrade'
Objects.object[55].obtype.insert(4, None)
Objects.object[55].obtype[4] = 'plane'
Objects.object[55].obtype.insert(5, None)
Objects.object[55].obtype[5] = 'measurementSystem'
Objects.object[55].requestsRate = []
Objects.object.insert(56, None)
Objects.object[56] = Dummy()
Objects.object[56].ifacename = 'IConfigSpecs'
Objects.object[56].oblocation = 'client'
Objects.object[56].obtype = []
Objects.object[56].obtype.insert(0, None)
Objects.object[56].obtype[0] = 'planePreset'
Objects.object[56].obtype.insert(1, None)
Objects.object[56].obtype[1] = 'measurementSystem'
Objects.object[56].requestsRate = []
Objects.object.insert(57, None)
Objects.object[57] = Dummy()
Objects.object[57].ifacename = 'IConfigSpecs'
Objects.object[57].oblocation = 'client'
Objects.object[57].obtype = []
Objects.object[57].obtype.insert(0, None)
Objects.object[57].obtype[0] = 'planePreset'
Objects.object[57].obtype.insert(1, None)
Objects.object[57].obtype[1] = 'planePreset'
Objects.object[57].obtype.insert(2, None)
Objects.object[57].obtype[2] = 'measurementSystem'
Objects.object[57].requestsRate = []
Objects.object.insert(58, None)
Objects.object[58] = Dummy()
Objects.object[58].ifacename = 'IShortConfigSpecs'
Objects.object[58].oblocation = 'client'
Objects.object[58].obtype = []
Objects.object[58].obtype.insert(0, None)
Objects.object[58].obtype[0] = 'planePreset'
Objects.object[58].requestsRate = []
Objects.object.insert(59, None)
Objects.object[59] = Dummy()
Objects.object[59].ifacename = 'IInstalledGlobalID'
Objects.object[59].oblocation = 'server'
Objects.object[59].obtype = []
Objects.object[59].obtype.insert(0, None)
Objects.object[59].obtype[0] = 'plane'
Objects.object[59].requestsRate = []
Objects.object.insert(60, None)
Objects.object[60] = Dummy()
Objects.object[60].ifacename = 'ISuitableAmmoBelts'
Objects.object[60].oblocation = 'client'
Objects.object[60].obtype = []
Objects.object[60].obtype.insert(0, None)
Objects.object[60].obtype[0] = 'plane'
Objects.object[60].obtype.insert(1, None)
Objects.object[60].obtype[1] = 'gun'
Objects.object[60].requestsRate = []
Objects.object.insert(61, None)
Objects.object[61] = Dummy()
Objects.object[61].ifacename = 'IAmmoBeltDescription'
Objects.object[61].oblocation = 'client'
Objects.object[61].obtype = []
Objects.object[61].obtype.insert(0, None)
Objects.object[61].obtype[0] = 'ammobelt'
Objects.object[61].requestsRate = []
Objects.object.insert(62, None)
Objects.object[62] = Dummy()
Objects.object[62].ifacename = 'IPrice'
Objects.object[62].oblocation = 'client'
Objects.object[62].obtype = []
Objects.object[62].obtype.insert(0, None)
Objects.object[62].obtype[0] = 'ammobelt'
Objects.object[62].requestsRate = []
Objects.object.insert(63, None)
Objects.object[63] = Dummy()
Objects.object[63].ifacename = 'IPrice'
Objects.object[63].oblocation = 'client'
Objects.object[63].obtype = []
Objects.object[63].obtype.insert(0, None)
Objects.object[63].obtype[0] = 'bomb'
Objects.object[63].requestsRate = []
Objects.object.insert(64, None)
Objects.object[64] = Dummy()
Objects.object[64].ifacename = 'IPrice'
Objects.object[64].oblocation = 'client'
Objects.object[64].obtype = []
Objects.object[64].obtype.insert(0, None)
Objects.object[64].obtype[0] = 'rocket'
Objects.object[64].requestsRate = []
Objects.object.insert(65, None)
Objects.object[65] = Dummy()
Objects.object[65].ifacename = 'ISellPrice'
Objects.object[65].oblocation = 'client'
Objects.object[65].obtype = []
Objects.object[65].obtype.insert(0, None)
Objects.object[65].obtype[0] = 'ammobelt'
Objects.object[65].requestsRate = []
Objects.object.insert(66, None)
Objects.object[66] = Dummy()
Objects.object[66].ifacename = 'ISellPrice'
Objects.object[66].oblocation = 'client'
Objects.object[66].obtype = []
Objects.object[66].obtype.insert(0, None)
Objects.object[66].obtype[0] = 'bomb'
Objects.object[66].requestsRate = []
Objects.object.insert(67, None)
Objects.object[67] = Dummy()
Objects.object[67].ifacename = 'ISellPrice'
Objects.object[67].oblocation = 'client'
Objects.object[67].obtype = []
Objects.object[67].obtype.insert(0, None)
Objects.object[67].obtype[0] = 'rocket'
Objects.object[67].requestsRate = []
Objects.object.insert(68, None)
Objects.object[68] = Dummy()
Objects.object[68].ifacename = 'IDepot'
Objects.object[68].oblocation = 'server'
Objects.object[68].obtype = []
Objects.object[68].obtype.insert(0, None)
Objects.object[68].obtype[0] = 'account'
Objects.object[68].requestsRate = []
Objects.object.insert(69, None)
Objects.object[69] = Dummy()
Objects.object[69].ifacename = 'IDepot'
Objects.object[69].oblocation = 'server'
Objects.object[69].obtype = []
Objects.object[69].obtype.insert(0, None)
Objects.object[69].obtype[0] = 'plane'
Objects.object[69].requestsRate = []
Objects.object.insert(70, None)
Objects.object[70] = Dummy()
Objects.object[70].ifacename = 'IAvailableConsumables'
Objects.object[70].oblocation = 'client'
Objects.object[70].obtype = []
Objects.object[70].obtype.insert(0, None)
Objects.object[70].obtype[0] = 'plane'
Objects.object[70].requestsRate = []
Objects.object.insert(71, None)
Objects.object[71] = Dummy()
Objects.object[71].ifacename = 'IAvailableEquipment'
Objects.object[71].oblocation = 'client'
Objects.object[71].obtype = []
Objects.object[71].obtype.insert(0, None)
Objects.object[71].obtype[0] = 'plane'
Objects.object[71].requestsRate = []
Objects.object.insert(72, None)
Objects.object[72] = Dummy()
Objects.object[72].ifacename = 'IEquipment'
Objects.object[72].oblocation = 'client'
Objects.object[72].obtype = []
Objects.object[72].obtype.insert(0, None)
Objects.object[72].obtype[0] = 'equipment'
Objects.object[72].requestsRate = []
Objects.object.insert(73, None)
Objects.object[73] = Dummy()
Objects.object[73].ifacename = 'IInstalledAmmoBelt'
Objects.object[73].oblocation = 'server'
Objects.object[73].obtype = []
Objects.object[73].obtype.insert(0, None)
Objects.object[73].obtype[0] = 'plane'
Objects.object[73].obtype.insert(1, None)
Objects.object[73].obtype[1] = 'weaponslot'
Objects.object[73].requestsRate = []
Objects.object.insert(74, None)
Objects.object[74] = Dummy()
Objects.object[74].ifacename = 'IConsumable'
Objects.object[74].oblocation = 'client'
Objects.object[74].obtype = []
Objects.object[74].obtype.insert(0, None)
Objects.object[74].obtype[0] = 'consumable'
Objects.object[74].requestsRate = []
Objects.object.insert(75, None)
Objects.object[75] = Dummy()
Objects.object[75].ifacename = 'IAccountResources'
Objects.object[75].oblocation = 'mixed'
Objects.object[75].obtype = []
Objects.object[75].obtype.insert(0, None)
Objects.object[75].obtype[0] = 'account'
Objects.object[75].requestsRate = []
Objects.object.insert(76, None)
Objects.object[76] = Dummy()
Objects.object[76].ifacename = 'IGunDescription'
Objects.object[76].oblocation = 'client'
Objects.object[76].obtype = []
Objects.object[76].obtype.insert(0, None)
Objects.object[76].obtype[0] = 'gun'
Objects.object[76].obtype.insert(1, None)
Objects.object[76].obtype[1] = 'measurementSystem'
Objects.object[76].requestsRate = []
Objects.object.insert(77, None)
Objects.object[77] = Dummy()
Objects.object[77].ifacename = 'IInstalledGunSlots'
Objects.object[77].oblocation = 'server'
Objects.object[77].obtype = []
Objects.object[77].obtype.insert(0, None)
Objects.object[77].obtype[0] = 'plane'
Objects.object[77].requestsRate = []
Objects.object.insert(78, None)
Objects.object[78] = Dummy()
Objects.object[78].ifacename = 'IInstalledBombSlots'
Objects.object[78].oblocation = 'server'
Objects.object[78].obtype = []
Objects.object[78].obtype.insert(0, None)
Objects.object[78].obtype[0] = 'plane'
Objects.object[78].requestsRate = []
Objects.object.insert(79, None)
Objects.object[79] = Dummy()
Objects.object[79].ifacename = 'IInstalledRocketSlots'
Objects.object[79].oblocation = 'server'
Objects.object[79].obtype = []
Objects.object[79].obtype.insert(0, None)
Objects.object[79].obtype[0] = 'plane'
Objects.object[79].requestsRate = []
Objects.object.insert(80, None)
Objects.object[80] = Dummy()
Objects.object[80].ifacename = 'IInstalledGun'
Objects.object[80].oblocation = 'server'
Objects.object[80].obtype = []
Objects.object[80].obtype.insert(0, None)
Objects.object[80].obtype[0] = 'plane'
Objects.object[80].obtype.insert(1, None)
Objects.object[80].obtype[1] = 'weaponslot'
Objects.object[80].requestsRate = []
Objects.object.insert(81, None)
Objects.object[81] = Dummy()
Objects.object[81].ifacename = 'IInstalledEquipment'
Objects.object[81].oblocation = 'server'
Objects.object[81].obtype = []
Objects.object[81].obtype.insert(0, None)
Objects.object[81].obtype[0] = 'plane'
Objects.object[81].requestsRate = []
Objects.object.insert(82, None)
Objects.object[82] = Dummy()
Objects.object[82].ifacename = 'IInstalledBomb'
Objects.object[82].oblocation = 'server'
Objects.object[82].obtype = []
Objects.object[82].obtype.insert(0, None)
Objects.object[82].obtype[0] = 'plane'
Objects.object[82].obtype.insert(1, None)
Objects.object[82].obtype[1] = 'weaponslot'
Objects.object[82].requestsRate = []
Objects.object.insert(83, None)
Objects.object[83] = Dummy()
Objects.object[83].ifacename = 'IInstalledRocket'
Objects.object[83].oblocation = 'server'
Objects.object[83].obtype = []
Objects.object[83].obtype.insert(0, None)
Objects.object[83].obtype[0] = 'plane'
Objects.object[83].obtype.insert(1, None)
Objects.object[83].obtype[1] = 'weaponslot'
Objects.object[83].requestsRate = []
Objects.object.insert(84, None)
Objects.object[84] = Dummy()
Objects.object[84].ifacename = 'IBombDescription'
Objects.object[84].oblocation = 'client'
Objects.object[84].obtype = []
Objects.object[84].obtype.insert(0, None)
Objects.object[84].obtype[0] = 'bomb'
Objects.object[84].obtype.insert(1, None)
Objects.object[84].obtype[1] = 'measurementSystem'
Objects.object[84].requestsRate = []
Objects.object.insert(85, None)
Objects.object[85] = Dummy()
Objects.object[85].ifacename = 'IRocketDescription'
Objects.object[85].oblocation = 'client'
Objects.object[85].obtype = []
Objects.object[85].obtype.insert(0, None)
Objects.object[85].obtype[0] = 'rocket'
Objects.object[85].obtype.insert(1, None)
Objects.object[85].obtype[1] = 'measurementSystem'
Objects.object[85].requestsRate = []
Objects.object.insert(86, None)
Objects.object[86] = Dummy()
Objects.object[86].ifacename = 'IAmmoBeltCharacteristics'
Objects.object[86].oblocation = 'client'
Objects.object[86].obtype = []
Objects.object[86].obtype.insert(0, None)
Objects.object[86].obtype[0] = 'ammobelt'
Objects.object[86].obtype.insert(1, None)
Objects.object[86].obtype[1] = 'gun'
Objects.object[86].requestsRate = []
Objects.object.insert(87, None)
Objects.object[87] = Dummy()
Objects.object[87].ifacename = 'IAmmoBeltCharacteristics'
Objects.object[87].oblocation = 'client'
Objects.object[87].obtype = []
Objects.object[87].obtype.insert(0, None)
Objects.object[87].obtype[0] = 'ammobelt'
Objects.object[87].requestsRate = []
Objects.object.insert(88, None)
Objects.object[88] = Dummy()
Objects.object[88].ifacename = 'IServiceStates'
Objects.object[88].oblocation = 'server'
Objects.object[88].obtype = []
Objects.object[88].obtype.insert(0, None)
Objects.object[88].obtype[0] = 'plane'
Objects.object[88].requestsRate = []
Objects.object.insert(89, None)
Objects.object[89] = Dummy()
Objects.object[89].ifacename = 'IRepair'
Objects.object[89].oblocation = 'server'
Objects.object[89].obtype = []
Objects.object[89].obtype.insert(0, None)
Objects.object[89].obtype[0] = 'plane'
Objects.object[89].requestsRate = []
Objects.object.insert(90, None)
Objects.object[90] = Dummy()
Objects.object[90].ifacename = 'IInstalledConsumables'
Objects.object[90].oblocation = 'server'
Objects.object[90].obtype = []
Objects.object[90].obtype.insert(0, None)
Objects.object[90].obtype[0] = 'plane'
Objects.object[90].requestsRate = []
Objects.object.insert(91, None)
Objects.object[91] = Dummy()
Objects.object[91].ifacename = 'IPlaneCrew'
Objects.object[91].oblocation = 'mixed'
Objects.object[91].obtype = []
Objects.object[91].obtype.insert(0, None)
Objects.object[91].obtype[0] = 'plane'
Objects.object[91].requestsRate = []
Objects.object.insert(92, None)
Objects.object[92] = Dummy()
Objects.object[92].ifacename = 'ICrewMember'
Objects.object[92].oblocation = 'mixed'
Objects.object[92].obtype = []
Objects.object[92].obtype.insert(0, None)
Objects.object[92].obtype[0] = 'crewmember'
Objects.object[92].requestsRate = []
Objects.object.insert(93, None)
Objects.object[93] = Dummy()
Objects.object[93].ifacename = 'ISkillDescription'
Objects.object[93].oblocation = 'client'
Objects.object[93].obtype = []
Objects.object[93].obtype.insert(0, None)
Objects.object[93].obtype[0] = 'skill'
Objects.object[93].requestsRate = []
Objects.object.insert(94, None)
Objects.object[94] = Dummy()
Objects.object[94].ifacename = 'IAvailableSkills'
Objects.object[94].oblocation = 'mixed'
Objects.object[94].obtype = []
Objects.object[94].obtype.insert(0, None)
Objects.object[94].obtype[0] = 'crewmember'
Objects.object[94].requestsRate = []
Objects.object.insert(95, None)
Objects.object[95] = Dummy()
Objects.object[95].ifacename = 'ICrewSpecializationResearchCost'
Objects.object[95].oblocation = 'server'
Objects.object[95].obtype = []
Objects.object[95].obtype.insert(0, None)
Objects.object[95].obtype[0] = 'account'
Objects.object[95].requestsRate = []
Objects.object.insert(96, None)
Objects.object[96] = Dummy()
Objects.object[96].ifacename = 'IAwards'
Objects.object[96].oblocation = 'mixed'
Objects.object[96].obtype = []
Objects.object[96].obtype.insert(0, None)
Objects.object[96].obtype[0] = 'account'
Objects.object[96].requestsRate = []
Objects.object.insert(97, None)
Objects.object[97] = Dummy()
Objects.object[97].ifacename = 'IAwards'
Objects.object[97].oblocation = 'mixed'
Objects.object[97].obtype = []
Objects.object[97].obtype.insert(0, None)
Objects.object[97].obtype[0] = 'plane'
Objects.object[97].requestsRate = []
Objects.object.insert(98, None)
Objects.object[98] = Dummy()
Objects.object[98].ifacename = 'IAwardDescription'
Objects.object[98].oblocation = 'client'
Objects.object[98].obtype = []
Objects.object[98].obtype.insert(0, None)
Objects.object[98].obtype[0] = 'medal'
Objects.object[98].requestsRate = []
Objects.object.insert(99, None)
Objects.object[99] = Dummy()
Objects.object[99].ifacename = 'IAwardDescription'
Objects.object[99].oblocation = 'client'
Objects.object[99].obtype = []
Objects.object[99].obtype.insert(0, None)
Objects.object[99].obtype[0] = 'ribbon'
Objects.object[99].requestsRate = []
Objects.object.insert(100, None)
Objects.object[100] = Dummy()
Objects.object[100].ifacename = 'IAwardDescription'
Objects.object[100].oblocation = 'client'
Objects.object[100].obtype = []
Objects.object[100].obtype.insert(0, None)
Objects.object[100].obtype[0] = 'achievement'
Objects.object[100].requestsRate = []
Objects.object.insert(101, None)
Objects.object[101] = Dummy()
Objects.object[101].ifacename = 'IAwardDailyBonus'
Objects.object[101].oblocation = 'server'
Objects.object[101].obtype = []
Objects.object[101].obtype.insert(0, None)
Objects.object[101].obtype[0] = 'achievement'
Objects.object[101].requestsRate = []
Objects.object.insert(102, None)
Objects.object[102] = Dummy()
Objects.object[102].ifacename = 'IExperience'
Objects.object[102].oblocation = 'server'
Objects.object[102].obtype = []
Objects.object[102].obtype.insert(0, None)
Objects.object[102].obtype[0] = 'plane'
Objects.object[102].requestsRate = []
Objects.object.insert(103, None)
Objects.object[103] = Dummy()
Objects.object[103].ifacename = 'ICrewSkillsDropCost'
Objects.object[103].oblocation = 'server'
Objects.object[103].obtype = []
Objects.object[103].obtype.insert(0, None)
Objects.object[103].obtype[0] = 'account'
Objects.object[103].requestsRate = []
Objects.object.insert(104, None)
Objects.object[104] = Dummy()
Objects.object[104].ifacename = 'ICrewSPFromExp'
Objects.object[104].oblocation = 'client'
Objects.object[104].obtype = []
Objects.object[104].obtype.insert(0, None)
Objects.object[104].obtype[0] = 'account'
Objects.object[104].requestsRate = []
Objects.object.insert(105, None)
Objects.object[105] = Dummy()
Objects.object[105].ifacename = 'ICrewRanks'
Objects.object[105].oblocation = 'client'
Objects.object[105].obtype = []
Objects.object[105].obtype.insert(0, None)
Objects.object[105].obtype[0] = 'crewmember'
Objects.object[105].requestsRate = []
Objects.object.insert(106, None)
Objects.object[106] = Dummy()
Objects.object[106].ifacename = 'ICrewMemberDroppedSkills'
Objects.object[106].oblocation = 'client'
Objects.object[106].obtype = []
Objects.object[106].obtype.insert(0, None)
Objects.object[106].obtype[0] = 'crewmember'
Objects.object[106].requestsRate = []
Objects.object.insert(107, None)
Objects.object[107] = Dummy()
Objects.object[107].ifacename = 'IPlaneDynamicDataPack'
Objects.object[107].oblocation = 'server'
Objects.object[107].obtype = []
Objects.object[107].obtype.insert(0, None)
Objects.object[107].obtype[0] = 'plane'
Objects.object[107].requestsRate = []
Objects.object.insert(108, None)
Objects.object[108] = Dummy()
Objects.object[108].ifacename = 'IPlanes'
Objects.object[108].oblocation = 'server'
Objects.object[108].obtype = []
Objects.object[108].obtype.insert(0, None)
Objects.object[108].obtype[0] = 'crewmember'
Objects.object[108].requestsRate = []
Objects.object.insert(109, None)
Objects.object[109] = Dummy()
Objects.object[109].ifacename = 'IListAmmoBelts'
Objects.object[109].oblocation = 'server'
Objects.object[109].obtype = []
Objects.object[109].obtype.insert(0, None)
Objects.object[109].obtype[0] = 'account'
Objects.object[109].requestsRate = []
Objects.object.insert(110, None)
Objects.object[110] = Dummy()
Objects.object[110].ifacename = 'IListBombs'
Objects.object[110].oblocation = 'client'
Objects.object[110].obtype = []
Objects.object[110].obtype.insert(0, None)
Objects.object[110].obtype[0] = 'account'
Objects.object[110].requestsRate = []
Objects.object.insert(111, None)
Objects.object[111] = Dummy()
Objects.object[111].ifacename = 'IListRockets'
Objects.object[111].oblocation = 'client'
Objects.object[111].obtype = []
Objects.object[111].obtype.insert(0, None)
Objects.object[111].obtype[0] = 'account'
Objects.object[111].requestsRate = []
Objects.object.insert(112, None)
Objects.object[112] = Dummy()
Objects.object[112].ifacename = 'IListUpgrades'
Objects.object[112].oblocation = 'client'
Objects.object[112].obtype = []
Objects.object[112].obtype.insert(0, None)
Objects.object[112].obtype[0] = 'account'
Objects.object[112].requestsRate = []
Objects.object.insert(113, None)
Objects.object[113] = Dummy()
Objects.object[113].ifacename = 'IListBoughtUpgrades'
Objects.object[113].oblocation = 'server'
Objects.object[113].obtype = []
Objects.object[113].obtype.insert(0, None)
Objects.object[113].obtype[0] = 'account'
Objects.object[113].requestsRate = []
Objects.object.insert(114, None)
Objects.object[114] = Dummy()
Objects.object[114].ifacename = 'IInstalledCount'
Objects.object[114].oblocation = 'server'
Objects.object[114].obtype = []
Objects.object[114].obtype.insert(0, None)
Objects.object[114].obtype[0] = 'ammobelt'
Objects.object[114].requestsRate = []
Objects.object.insert(115, None)
Objects.object[115] = Dummy()
Objects.object[115].ifacename = 'IDepotCount'
Objects.object[115].oblocation = 'server'
Objects.object[115].obtype = []
Objects.object[115].obtype.insert(0, None)
Objects.object[115].obtype[0] = 'ammobelt'
Objects.object[115].requestsRate = []
Objects.object.insert(116, None)
Objects.object[116] = Dummy()
Objects.object[116].ifacename = 'IInstalledCount'
Objects.object[116].oblocation = 'server'
Objects.object[116].obtype = []
Objects.object[116].obtype.insert(0, None)
Objects.object[116].obtype[0] = 'bomb'
Objects.object[116].requestsRate = []
Objects.object.insert(117, None)
Objects.object[117] = Dummy()
Objects.object[117].ifacename = 'IDepotCount'
Objects.object[117].oblocation = 'server'
Objects.object[117].obtype = []
Objects.object[117].obtype.insert(0, None)
Objects.object[117].obtype[0] = 'bomb'
Objects.object[117].requestsRate = []
Objects.object.insert(118, None)
Objects.object[118] = Dummy()
Objects.object[118].ifacename = 'IInstalledCount'
Objects.object[118].oblocation = 'server'
Objects.object[118].obtype = []
Objects.object[118].obtype.insert(0, None)
Objects.object[118].obtype[0] = 'rocket'
Objects.object[118].requestsRate = []
Objects.object.insert(119, None)
Objects.object[119] = Dummy()
Objects.object[119].ifacename = 'IDepotCount'
Objects.object[119].oblocation = 'server'
Objects.object[119].obtype = []
Objects.object[119].obtype.insert(0, None)
Objects.object[119].obtype[0] = 'rocket'
Objects.object[119].requestsRate = []
Objects.object.insert(120, None)
Objects.object[120] = Dummy()
Objects.object[120].ifacename = 'IInstalledCount'
Objects.object[120].oblocation = 'server'
Objects.object[120].obtype = []
Objects.object[120].obtype.insert(0, None)
Objects.object[120].obtype[0] = 'consumable'
Objects.object[120].requestsRate = []
Objects.object.insert(121, None)
Objects.object[121] = Dummy()
Objects.object[121].ifacename = 'IDepotCount'
Objects.object[121].oblocation = 'server'
Objects.object[121].obtype = []
Objects.object[121].obtype.insert(0, None)
Objects.object[121].obtype[0] = 'consumable'
Objects.object[121].requestsRate = []
Objects.object.insert(122, None)
Objects.object[122] = Dummy()
Objects.object[122].ifacename = 'IInstalledCount'
Objects.object[122].oblocation = 'server'
Objects.object[122].obtype = []
Objects.object[122].obtype.insert(0, None)
Objects.object[122].obtype[0] = 'equipment'
Objects.object[122].requestsRate = []
Objects.object.insert(123, None)
Objects.object[123] = Dummy()
Objects.object[123].ifacename = 'IDepotCount'
Objects.object[123].oblocation = 'server'
Objects.object[123].obtype = []
Objects.object[123].obtype.insert(0, None)
Objects.object[123].obtype[0] = 'equipment'
Objects.object[123].requestsRate = []
Objects.object.insert(124, None)
Objects.object[124] = Dummy()
Objects.object[124].ifacename = 'IDepotCount'
Objects.object[124].oblocation = 'server'
Objects.object[124].obtype = []
Objects.object[124].obtype.insert(0, None)
Objects.object[124].obtype[0] = 'upgrade'
Objects.object[124].requestsRate = []
Objects.object.insert(125, None)
Objects.object[125] = Dummy()
Objects.object[125].ifacename = 'IInstalledCount'
Objects.object[125].oblocation = 'server'
Objects.object[125].obtype = []
Objects.object[125].obtype.insert(0, None)
Objects.object[125].obtype[0] = 'upgrade'
Objects.object[125].requestsRate = []
Objects.object.insert(126, None)
Objects.object[126] = Dummy()
Objects.object[126].ifacename = 'IListConsumables'
Objects.object[126].oblocation = 'client'
Objects.object[126].obtype = []
Objects.object[126].obtype.insert(0, None)
Objects.object[126].obtype[0] = 'account'
Objects.object[126].requestsRate = []
Objects.object.insert(127, None)
Objects.object[127] = Dummy()
Objects.object[127].ifacename = 'IListEquipment'
Objects.object[127].oblocation = 'client'
Objects.object[127].obtype = []
Objects.object[127].obtype.insert(0, None)
Objects.object[127].obtype[0] = 'account'
Objects.object[127].requestsRate = []
Objects.object.insert(128, None)
Objects.object[128] = Dummy()
Objects.object[128].ifacename = 'IBarrack'
Objects.object[128].oblocation = 'server'
Objects.object[128].obtype = []
Objects.object[128].obtype.insert(0, None)
Objects.object[128].obtype[0] = 'account'
Objects.object[128].requestsRate = []
Objects.object.insert(129, None)
Objects.object[129] = Dummy()
Objects.object[129].ifacename = 'IBarrack'
Objects.object[129].oblocation = 'server'
Objects.object[129].obtype = []
Objects.object[129].obtype.insert(0, None)
Objects.object[129].obtype[0] = 'nation'
Objects.object[129].obtype.insert(1, None)
Objects.object[129].obtype[1] = 'skill'
Objects.object[129].requestsRate = []
Objects.object.insert(130, None)
Objects.object[130] = Dummy()
Objects.object[130].ifacename = 'IBarrackSlots'
Objects.object[130].oblocation = 'server'
Objects.object[130].obtype = []
Objects.object[130].obtype.insert(0, None)
Objects.object[130].obtype[0] = 'account'
Objects.object[130].requestsRate = []
Objects.object.insert(131, None)
Objects.object[131] = Dummy()
Objects.object[131].ifacename = 'IBarrackPrice'
Objects.object[131].oblocation = 'server'
Objects.object[131].obtype = []
Objects.object[131].obtype.insert(0, None)
Objects.object[131].obtype[0] = 'account'
Objects.object[131].requestsRate = []
Objects.object.insert(132, None)
Objects.object[132] = Dummy()
Objects.object[132].ifacename = 'ISkillPenalty'
Objects.object[132].oblocation = 'client'
Objects.object[132].obtype = []
Objects.object[132].obtype.insert(0, None)
Objects.object[132].obtype[0] = 'crewmember'
Objects.object[132].obtype.insert(1, None)
Objects.object[132].obtype[1] = 'plane'
Objects.object[132].requestsRate = []
Objects.object.insert(133, None)
Objects.object[133] = Dummy()
Objects.object[133].ifacename = 'ICrewSpecializationRetrainPrc'
Objects.object[133].oblocation = 'client'
Objects.object[133].obtype = []
Objects.object[133].obtype.insert(0, None)
Objects.object[133].obtype[0] = 'crewmember'
Objects.object[133].obtype.insert(1, None)
Objects.object[133].obtype[1] = 'plane'
Objects.object[133].requestsRate = []
Objects.object.insert(134, None)
Objects.object[134] = Dummy()
Objects.object[134].ifacename = 'ICrewSpecializationRetrainCost'
Objects.object[134].oblocation = 'server'
Objects.object[134].obtype = []
Objects.object[134].obtype.insert(0, None)
Objects.object[134].obtype[0] = 'account'
Objects.object[134].requestsRate = []
Objects.object.insert(135, None)
Objects.object[135] = Dummy()
Objects.object[135].expiringTime = 300
Objects.object[135].ifacename = 'IPlaneStats'
Objects.object[135].oblocation = 'mixed'
Objects.object[135].obtype = []
Objects.object[135].obtype.insert(0, None)
Objects.object[135].obtype[0] = 'plane'
Objects.object[135].requestsRate = []
Objects.object[135].requestsRate.insert(0, None)
Objects.object[135].requestsRate[0] = Dummy()
Objects.object[135].requestsRate[0].count = 1
Objects.object[135].requestsRate[0].method = 'view'
Objects.object[135].requestsRate[0].timelapse = 2.0
Objects.object.insert(136, None)
Objects.object[136] = Dummy()
Objects.object[136].ifacename = 'ISummaryStats'
Objects.object[136].oblocation = 'mixed'
Objects.object[136].obtype = []
Objects.object[136].obtype.insert(0, None)
Objects.object[136].obtype[0] = 'account'
Objects.object[136].requestsRate = []
Objects.object[136].requestsRate.insert(0, None)
Objects.object[136].requestsRate[0] = Dummy()
Objects.object[136].requestsRate[0].count = 1
Objects.object[136].requestsRate[0].method = 'view'
Objects.object[136].requestsRate[0].timelapse = 2.0
Objects.object.insert(137, None)
Objects.object[137] = Dummy()
Objects.object[137].ifacename = 'IShortPlaneDescription'
Objects.object[137].oblocation = 'client'
Objects.object[137].obtype = []
Objects.object[137].obtype.insert(0, None)
Objects.object[137].obtype[0] = 'plane'
Objects.object[137].requestsRate = []
Objects.object.insert(138, None)
Objects.object[138] = Dummy()
Objects.object[138].ifacename = 'IShortPlaneStats'
Objects.object[138].oblocation = 'server'
Objects.object[138].obtype = []
Objects.object[138].obtype.insert(0, None)
Objects.object[138].obtype[0] = 'plane'
Objects.object[138].requestsRate = []
Objects.object[138].requestsRate.insert(0, None)
Objects.object[138].requestsRate[0] = Dummy()
Objects.object[138].requestsRate[0].count = 1
Objects.object[138].requestsRate[0].method = 'view'
Objects.object[138].requestsRate[0].timelapse = 2.0
Objects.object.insert(139, None)
Objects.object[139] = Dummy()
Objects.object[139].ifacename = 'IStatsPlanesList'
Objects.object[139].oblocation = 'server'
Objects.object[139].obtype = []
Objects.object[139].obtype.insert(0, None)
Objects.object[139].obtype[0] = 'account'
Objects.object[139].requestsRate = []
Objects.object.insert(140, None)
Objects.object[140] = Dummy()
Objects.object[140].ifacename = 'ILocalizationLanguage'
Objects.object[140].oblocation = 'client'
Objects.object[140].obtype = []
Objects.object[140].obtype.insert(0, None)
Objects.object[140].obtype[0] = 'account'
Objects.object[140].requestsRate = []
Objects.object.insert(141, None)
Objects.object[141] = Dummy()
Objects.object[141].ifacename = 'ICamouflages'
Objects.object[141].oblocation = 'client'
Objects.object[141].obtype = []
Objects.object[141].obtype.insert(0, None)
Objects.object[141].obtype[0] = 'plane'
Objects.object[141].requestsRate = []
Objects.object.insert(142, None)
Objects.object[142] = Dummy()
Objects.object[142].ifacename = 'ICamouflageDescription'
Objects.object[142].oblocation = 'client'
Objects.object[142].obtype = []
Objects.object[142].obtype.insert(0, None)
Objects.object[142].obtype[0] = 'camouflage'
Objects.object[142].requestsRate = []
Objects.object.insert(143, None)
Objects.object[143] = Dummy()
Objects.object[143].ifacename = 'ICamouflageStatus'
Objects.object[143].oblocation = 'server'
Objects.object[143].obtype = []
Objects.object[143].obtype.insert(0, None)
Objects.object[143].obtype[0] = 'camouflage'
Objects.object[143].requestsRate = []
Objects.object.insert(144, None)
Objects.object[144] = Dummy()
Objects.object[144].ifacename = 'IPriceSchemes'
Objects.object[144].oblocation = 'server'
Objects.object[144].obtype = []
Objects.object[144].obtype.insert(0, None)
Objects.object[144].obtype[0] = 'account'
Objects.object[144].requestsRate = []
Objects.object.insert(145, None)
Objects.object[145] = Dummy()
Objects.object[145].ifacename = 'IBonusSchemes'
Objects.object[145].oblocation = 'client'
Objects.object[145].obtype = []
Objects.object[145].obtype.insert(0, None)
Objects.object[145].obtype[0] = 'account'
Objects.object[145].requestsRate = []
Objects.object.insert(146, None)
Objects.object[146] = Dummy()
Objects.object[146].ifacename = 'ITimeDelta'
Objects.object[146].oblocation = 'mixed'
Objects.object[146].obtype = []
Objects.object[146].obtype.insert(0, None)
Objects.object[146].obtype[0] = 'account'
Objects.object[146].requestsRate = []
Objects.object.insert(147, None)
Objects.object[147] = Dummy()
Objects.object[147].ifacename = 'IPlaneSalesLeft'
Objects.object[147].oblocation = 'server'
Objects.object[147].obtype = []
Objects.object[147].obtype.insert(0, None)
Objects.object[147].obtype[0] = 'account'
Objects.object[147].requestsRate = []
Objects.object.insert(148, None)
Objects.object[148] = Dummy()
Objects.object[148].ifacename = 'IInstalledCamouflage'
Objects.object[148].oblocation = 'server'
Objects.object[148].obtype = []
Objects.object[148].obtype.insert(0, None)
Objects.object[148].obtype[0] = 'plane'
Objects.object[148].requestsRate = []
Objects.object.insert(149, None)
Objects.object[149] = Dummy()
Objects.object[149].ifacename = 'IInstalledCamouflage'
Objects.object[149].oblocation = 'client'
Objects.object[149].obtype = []
Objects.object[149].obtype.insert(0, None)
Objects.object[149].obtype[0] = 'previewmodel'
Objects.object[149].requestsRate = []
Objects.object.insert(150, None)
Objects.object[150] = Dummy()
Objects.object[150].ifacename = 'IPlayerSummaryStats'
Objects.object[150].oblocation = 'mixed'
Objects.object[150].obtype = []
Objects.object[150].obtype.insert(0, None)
Objects.object[150].obtype[0] = 'account'
Objects.object[150].requestsRate = []
Objects.object[150].requestsRate.insert(0, None)
Objects.object[150].requestsRate[0] = Dummy()
Objects.object[150].requestsRate[0].count = 1
Objects.object[150].requestsRate[0].method = 'view'
Objects.object[150].requestsRate[0].timelapse = 2.0
Objects.object.insert(151, None)
Objects.object[151] = Dummy()
Objects.object[151].ifacename = 'IPlayerPlaneStats'
Objects.object[151].oblocation = 'mixed'
Objects.object[151].obtype = []
Objects.object[151].obtype.insert(0, None)
Objects.object[151].obtype[0] = 'account'
Objects.object[151].obtype.insert(1, None)
Objects.object[151].obtype[1] = 'plane'
Objects.object[151].requestsRate = []
Objects.object[151].requestsRate.insert(0, None)
Objects.object[151].requestsRate[0] = Dummy()
Objects.object[151].requestsRate[0].count = 1
Objects.object[151].requestsRate[0].method = 'view'
Objects.object[151].requestsRate[0].timelapse = 2.0
Objects.object.insert(152, None)
Objects.object[152] = Dummy()
Objects.object[152].ifacename = 'IPlayerShortPlaneDescription'
Objects.object[152].oblocation = 'client'
Objects.object[152].obtype = []
Objects.object[152].obtype.insert(0, None)
Objects.object[152].obtype[0] = 'account'
Objects.object[152].obtype.insert(1, None)
Objects.object[152].obtype[1] = 'plane'
Objects.object[152].requestsRate = []
Objects.object.insert(153, None)
Objects.object[153] = Dummy()
Objects.object[153].ifacename = 'IPlayerShortPlaneStats'
Objects.object[153].oblocation = 'server'
Objects.object[153].obtype = []
Objects.object[153].obtype.insert(0, None)
Objects.object[153].obtype[0] = 'account'
Objects.object[153].obtype.insert(1, None)
Objects.object[153].obtype[1] = 'plane'
Objects.object[153].requestsRate = []
Objects.object[153].requestsRate.insert(0, None)
Objects.object[153].requestsRate[0] = Dummy()
Objects.object[153].requestsRate[0].count = 1
Objects.object[153].requestsRate[0].method = 'view'
Objects.object[153].requestsRate[0].timelapse = 2.0
Objects.object.insert(154, None)
Objects.object[154] = Dummy()
Objects.object[154].ifacename = 'IPaymentType'
Objects.object[154].oblocation = 'server'
Objects.object[154].obtype = []
Objects.object[154].obtype.insert(0, None)
Objects.object[154].obtype[0] = 'consumable'
Objects.object[154].requestsRate = []
Objects.object.insert(155, None)
Objects.object[155] = Dummy()
Objects.object[155].ifacename = 'IPaymentType'
Objects.object[155].oblocation = 'server'
Objects.object[155].obtype = []
Objects.object[155].obtype.insert(0, None)
Objects.object[155].obtype[0] = 'consumable'
Objects.object[155].obtype.insert(1, None)
Objects.object[155].obtype[1] = 'plane'
Objects.object[155].requestsRate = []
Objects.object.insert(156, None)
Objects.object[156] = Dummy()
Objects.object[156].ifacename = 'IPaymentType'
Objects.object[156].oblocation = 'server'
Objects.object[156].obtype = []
Objects.object[156].obtype.insert(0, None)
Objects.object[156].obtype[0] = 'ammobelt'
Objects.object[156].requestsRate = []
Objects.object.insert(157, None)
Objects.object[157] = Dummy()
Objects.object[157].ifacename = 'IPaymentType'
Objects.object[157].oblocation = 'server'
Objects.object[157].obtype = []
Objects.object[157].obtype.insert(0, None)
Objects.object[157].obtype[0] = 'ammobelt'
Objects.object[157].obtype.insert(1, None)
Objects.object[157].obtype[1] = 'plane'
Objects.object[157].obtype.insert(2, None)
Objects.object[157].obtype[2] = 'slot'
Objects.object[157].obtype.insert(3, None)
Objects.object[157].obtype[3] = 'slotConfig'
Objects.object[157].requestsRate = []
Objects.object.insert(158, None)
Objects.object[158] = Dummy()
Objects.object[158].ifacename = 'IWalletSettings'
Objects.object[158].oblocation = 'server'
Objects.object[158].obtype = []
Objects.object[158].obtype.insert(0, None)
Objects.object[158].obtype[0] = 'account'
Objects.object[158].requestsRate = []
Objects.object.insert(159, None)
Objects.object[159] = Dummy()
Objects.object[159].ifacename = 'IAwardsList'
Objects.object[159].oblocation = 'client'
Objects.object[159].obtype = []
Objects.object[159].obtype.insert(0, None)
Objects.object[159].obtype[0] = 'account'
Objects.object[159].requestsRate = []
Objects.object.insert(160, None)
Objects.object[160] = Dummy()
Objects.object[160].ifacename = 'ILastProcessedResponse'
Objects.object[160].oblocation = 'client'
Objects.object[160].obtype = []
Objects.object[160].obtype.insert(0, None)
Objects.object[160].obtype[0] = 'account'
Objects.object[160].requestsRate = []
Objects.object.insert(161, None)
Objects.object[161] = Dummy()
Objects.object[161].ifacename = 'IResponse'
Objects.object[161].oblocation = 'client'
Objects.object[161].obtype = []
Objects.object[161].obtype.insert(0, None)
Objects.object[161].obtype[0] = 'response'
Objects.object[161].requestsRate = []
Objects.object.insert(162, None)
Objects.object[162] = Dummy()
Objects.object[162].ifacename = 'IName'
Objects.object[162].oblocation = 'client'
Objects.object[162].obtype = []
Objects.object[162].obtype.insert(0, None)
Objects.object[162].obtype[0] = 'periphery'
Objects.object[162].requestsRate = []
Objects.object.insert(163, None)
Objects.object[163] = Dummy()
Objects.object[163].ifacename = 'IBattleResult'
Objects.object[163].oblocation = 'client'
Objects.object[163].obtype = []
Objects.object[163].obtype.insert(0, None)
Objects.object[163].obtype[0] = 'battleResult'
Objects.object[163].requestsRate = []
Objects.object.insert(164, None)
Objects.object[164] = Dummy()
Objects.object[164].ifacename = 'IBattleResultShort'
Objects.object[164].oblocation = 'client'
Objects.object[164].obtype = []
Objects.object[164].obtype.insert(0, None)
Objects.object[164].obtype[0] = 'battleResult'
Objects.object[164].requestsRate = []
Objects.object.insert(165, None)
Objects.object[165] = Dummy()
Objects.object[165].ifacename = 'ISessionBattleResults'
Objects.object[165].oblocation = 'client'
Objects.object[165].obtype = []
Objects.object[165].obtype.insert(0, None)
Objects.object[165].obtype[0] = 'account'
Objects.object[165].requestsRate = []
Objects.object.insert(166, None)
Objects.object[166] = Dummy()
Objects.object[166].ifacename = 'IQuestDebugProcess'
Objects.object[166].oblocation = 'server'
Objects.object[166].obtype = []
Objects.object[166].obtype.insert(0, None)
Objects.object[166].obtype[0] = 'questoperation'
Objects.object[166].requestsRate = []
Objects.object.insert(167, None)
Objects.object[167] = Dummy()
Objects.object[167].ifacename = 'IQuestList'
Objects.object[167].oblocation = 'server'
Objects.object[167].obtype = []
Objects.object[167].obtype.insert(0, None)
Objects.object[167].obtype[0] = 'account'
Objects.object[167].requestsRate = []
Objects.object.insert(168, None)
Objects.object[168] = Dummy()
Objects.object[168].ifacename = 'IQuestList'
Objects.object[168].oblocation = 'server'
Objects.object[168].obtype = []
Objects.object[168].obtype.insert(0, None)
Objects.object[168].obtype[0] = 'plane'
Objects.object[168].requestsRate = []
Objects.object.insert(169, None)
Objects.object[169] = Dummy()
Objects.object[169].ifacename = 'IQuest'
Objects.object[169].oblocation = 'client'
Objects.object[169].obtype = []
Objects.object[169].obtype.insert(0, None)
Objects.object[169].obtype[0] = 'battlequest'
Objects.object[169].requestsRate = []
Objects.object.insert(170, None)
Objects.object[170] = Dummy()
Objects.object[170].ifacename = 'IQuestResults'
Objects.object[170].oblocation = 'server'
Objects.object[170].obtype = []
Objects.object[170].obtype.insert(0, None)
Objects.object[170].obtype[0] = 'battlequest'
Objects.object[170].requestsRate = []
Objects.object.insert(171, None)
Objects.object[171] = Dummy()
Objects.object[171].ifacename = 'IQuestAvaiblePlanes'
Objects.object[171].oblocation = 'server'
Objects.object[171].obtype = []
Objects.object[171].obtype.insert(0, None)
Objects.object[171].obtype[0] = 'battlequest'
Objects.object[171].requestsRate = []
Objects.object.insert(172, None)
Objects.object[172] = Dummy()
Objects.object[172].ifacename = 'IQuestDescription'
Objects.object[172].oblocation = 'mixed'
Objects.object[172].obtype = []
Objects.object[172].obtype.insert(0, None)
Objects.object[172].obtype[0] = 'battlequest'
Objects.object[172].requestsRate = []
Objects.object.insert(173, None)
Objects.object[173] = Dummy()
Objects.object[173].ifacename = 'IQuestDynDescription'
Objects.object[173].oblocation = 'mixed'
Objects.object[173].obtype = []
Objects.object[173].obtype.insert(0, None)
Objects.object[173].obtype[0] = 'battlequest'
Objects.object[173].requestsRate = []
Objects.object.insert(174, None)
Objects.object[174] = Dummy()
Objects.object[174].ifacename = 'IQuestRead'
Objects.object[174].oblocation = 'server'
Objects.object[174].obtype = []
Objects.object[174].obtype.insert(0, None)
Objects.object[174].obtype[0] = 'battlequest'
Objects.object[174].requestsRate = []
Objects.object.insert(175, None)
Objects.object[175] = Dummy()
Objects.object[175].ifacename = 'IQuestHidden'
Objects.object[175].oblocation = 'server'
Objects.object[175].obtype = []
Objects.object[175].obtype.insert(0, None)
Objects.object[175].obtype[0] = 'battlequest'
Objects.object[175].requestsRate = []
Objects.object.insert(176, None)
Objects.object[176] = Dummy()
Objects.object[176].ifacename = 'IQuestSelectConsist'
Objects.object[176].oblocation = 'server'
Objects.object[176].obtype = []
Objects.object[176].obtype.insert(0, None)
Objects.object[176].obtype[0] = 'account'
Objects.object[176].requestsRate = []
Objects.object.insert(177, None)
Objects.object[177] = Dummy()
Objects.object[177].ifacename = 'IQuestListAvailableConsist'
Objects.object[177].oblocation = 'server'
Objects.object[177].obtype = []
Objects.object[177].obtype.insert(0, None)
Objects.object[177].obtype[0] = 'account'
Objects.object[177].requestsRate = []
Objects.object.insert(178, None)
Objects.object[178] = Dummy()
Objects.object[178].ifacename = 'IQuestConsistEndAction'
Objects.object[178].oblocation = 'server'
Objects.object[178].obtype = []
Objects.object[178].obtype.insert(0, None)
Objects.object[178].obtype[0] = 'account'
Objects.object[178].requestsRate = []
Objects.object.insert(179, None)
Objects.object[179] = Dummy()
Objects.object[179].ifacename = 'IQuestPool'
Objects.object[179].oblocation = 'server'
Objects.object[179].obtype = []
Objects.object[179].obtype.insert(0, None)
Objects.object[179].obtype[0] = 'account'
Objects.object[179].requestsRate = []
Objects.object.insert(180, None)
Objects.object[180] = Dummy()
Objects.object[180].ifacename = 'IQuestBuy'
Objects.object[180].oblocation = 'server'
Objects.object[180].obtype = []
Objects.object[180].obtype.insert(0, None)
Objects.object[180].obtype[0] = 'questoperation'
Objects.object[180].requestsRate = []
Objects.object.insert(181, None)
Objects.object[181] = Dummy()
Objects.object[181].ifacename = 'IQuestProlong'
Objects.object[181].oblocation = 'server'
Objects.object[181].obtype = []
Objects.object[181].obtype.insert(0, None)
Objects.object[181].obtype[0] = 'questoperation'
Objects.object[181].requestsRate = []
Objects.object.insert(182, None)
Objects.object[182] = Dummy()
Objects.object[182].ifacename = 'IQuestChangeGroup'
Objects.object[182].oblocation = 'server'
Objects.object[182].obtype = []
Objects.object[182].obtype.insert(0, None)
Objects.object[182].obtype[0] = 'questoperation'
Objects.object[182].requestsRate = []
Objects.object.insert(183, None)
Objects.object[183] = Dummy()
Objects.object[183].ifacename = 'IRentConf'
Objects.object[183].oblocation = 'server'
Objects.object[183].obtype = []
Objects.object[183].obtype.insert(0, None)
Objects.object[183].obtype[0] = 'plane'
Objects.object[183].requestsRate = []
Objects.object.insert(184, None)
Objects.object[184] = Dummy()
Objects.object[184].ifacename = 'IRent'
Objects.object[184].oblocation = 'server'
Objects.object[184].obtype = []
Objects.object[184].obtype.insert(0, None)
Objects.object[184].obtype[0] = 'plane'
Objects.object[184].requestsRate = []
Objects.object.insert(185, None)
Objects.object[185] = Dummy()
Objects.object[185].ifacename = 'IActionUI'
Objects.object[185].oblocation = 'server'
Objects.object[185].obtype = []
Objects.object[185].obtype.insert(0, None)
Objects.object[185].obtype[0] = 'actionui'
Objects.object[185].requestsRate = []
Objects.object.insert(186, None)
Objects.object[186] = Dummy()
Objects.object[186].ifacename = 'IActionUIList'
Objects.object[186].oblocation = 'server'
Objects.object[186].obtype = []
Objects.object[186].obtype.insert(0, None)
Objects.object[186].obtype[0] = 'account'
Objects.object[186].requestsRate = []
Objects.object.insert(187, None)
Objects.object[187] = Dummy()
Objects.object[187].ifacename = 'IMeasurementSystem'
Objects.object[187].oblocation = 'client'
Objects.object[187].obtype = []
Objects.object[187].obtype.insert(0, None)
Objects.object[187].obtype[0] = 'account'
Objects.object[187].requestsRate = []
Objects.object.insert(188, None)
Objects.object[188] = Dummy()
Objects.object[188].ifacename = 'IMeasurementSystemInfo'
Objects.object[188].oblocation = 'client'
Objects.object[188].obtype = []
Objects.object[188].obtype.insert(0, None)
Objects.object[188].obtype[0] = 'measurementSystem'
Objects.object[188].requestsRate = []
Objects.object.insert(189, None)
Objects.object[189] = Dummy()
Objects.object[189].ifacename = 'IMeasurementSystemsList'
Objects.object[189].oblocation = 'client'
Objects.object[189].obtype = []
Objects.object[189].obtype.insert(0, None)
Objects.object[189].obtype[0] = 'account'
Objects.object[189].requestsRate = []
Objects.object.insert(190, None)
Objects.object[190] = Dummy()
Objects.object[190].ifacename = 'ITransaction'
Objects.object[190].oblocation = 'server'
Objects.object[190].obtype = []
Objects.object[190].obtype.insert(0, None)
Objects.object[190].obtype[0] = 'transaction'
Objects.object[190].requestsRate = []
Objects.object.insert(191, None)
Objects.object[191] = Dummy()
Objects.object[191].ifacename = 'ITransaction'
Objects.object[191].oblocation = 'server'
Objects.object[191].obtype = []
Objects.object[191].obtype.insert(0, None)
Objects.object[191].obtype[0] = 'vtransaction'
Objects.object[191].requestsRate = []
Objects.object.insert(192, None)
Objects.object[192] = Dummy()
Objects.object[192].ifacename = 'IRequestsLocker'
Objects.object[192].oblocation = 'server'
Objects.object[192].obtype = []
Objects.object[192].obtype.insert(0, None)
Objects.object[192].obtype[0] = 'account'
Objects.object[192].requestsRate = []
Objects.object.insert(193, None)
Objects.object[193] = Dummy()
Objects.object[193].ifacename = 'IGameModesParams'
Objects.object[193].oblocation = 'server'
Objects.object[193].obtype = []
Objects.object[193].obtype.insert(0, None)
Objects.object[193].obtype[0] = 'account'
Objects.object[193].requestsRate = []
Objects.object.insert(194, None)
Objects.object[194] = Dummy()
Objects.object[194].ifacename = 'IPvEPlanes'
Objects.object[194].oblocation = 'server'
Objects.object[194].obtype = []
Objects.object[194].obtype.insert(0, None)
Objects.object[194].obtype[0] = 'account'
Objects.object[194].requestsRate = []
Objects.object.insert(195, None)
Objects.object[195] = Dummy()
Objects.object[195].ifacename = 'IRestartTime'
Objects.object[195].oblocation = 'server'
Objects.object[195].obtype = []
Objects.object[195].obtype.insert(0, None)
Objects.object[195].obtype[0] = 'account'
Objects.object[195].requestsRate = []
Objects.object.insert(196, None)
Objects.object[196] = Dummy()
Objects.object[196].ifacename = 'IIGR'
Objects.object[196].oblocation = 'server'
Objects.object[196].obtype = []
Objects.object[196].obtype.insert(0, None)
Objects.object[196].obtype[0] = 'account'
Objects.object[196].requestsRate = []
Objects.object.insert(197, None)
Objects.object[197] = Dummy()
Objects.object[197].ifacename = 'IPvEAvailable'
Objects.object[197].oblocation = 'server'
Objects.object[197].obtype = []
Objects.object[197].obtype.insert(0, None)
Objects.object[197].obtype[0] = 'account'
Objects.object[197].requestsRate = []
Objects.object.insert(198, None)
Objects.object[198] = Dummy()
Objects.object[198].ifacename = 'IClanInfoShort'
Objects.object[198].oblocation = 'server'
Objects.object[198].obtype = []
Objects.object[198].obtype.insert(0, None)
Objects.object[198].obtype[0] = 'account'
Objects.object[198].requestsRate = []
Objects.object.insert(199, None)
Objects.object[199] = Dummy()
Objects.object[199].ifacename = 'IClanMotto'
Objects.object[199].oblocation = 'server'
Objects.object[199].obtype = []
Objects.object[199].obtype.insert(0, None)
Objects.object[199].obtype[0] = 'account'
Objects.object[199].requestsRate = []
Objects.object.insert(200, None)
Objects.object[200] = Dummy()
Objects.object[200].ifacename = 'IClanInfo'
Objects.object[200].oblocation = 'server'
Objects.object[200].obtype = []
Objects.object[200].obtype.insert(0, None)
Objects.object[200].obtype[0] = 'account'
Objects.object[200].requestsRate = []
Objects.object.insert(201, None)
Objects.object[201] = Dummy()
Objects.object[201].expiringTime = 300
Objects.object[201].ifacename = 'IAccountClanData'
Objects.object[201].oblocation = 'server'
Objects.object[201].obtype = []
Objects.object[201].obtype.insert(0, None)
Objects.object[201].obtype[0] = 'account'
Objects.object[201].requestsRate = []
Objects.object[201].requestsRate.insert(0, None)
Objects.object[201].requestsRate[0] = Dummy()
Objects.object[201].requestsRate[0].count = 1
Objects.object[201].requestsRate[0].method = 'view'
Objects.object[201].requestsRate[0].timelapse = 2.0
Objects.object.insert(202, None)
Objects.object[202] = Dummy()
Objects.object[202].ifacename = 'IClanMembers'
Objects.object[202].oblocation = 'server'
Objects.object[202].obtype = []
Objects.object[202].obtype.insert(0, None)
Objects.object[202].obtype[0] = 'account'
Objects.object[202].requestsRate = []
Objects.object.insert(203, None)
Objects.object[203] = Dummy()
Objects.object[203].ifacename = 'IClanMember'
Objects.object[203].oblocation = 'server'
Objects.object[203].obtype = []
Objects.object[203].obtype.insert(0, None)
Objects.object[203].obtype[0] = 'account'
Objects.object[203].requestsRate = []
Objects.object.insert(204, None)
Objects.object[204] = Dummy()
Objects.object[204].ifacename = 'IExchangeXPRate'
Objects.object[204].oblocation = 'server'
Objects.object[204].obtype = []
Objects.object[204].obtype.insert(0, None)
Objects.object[204].obtype[0] = 'account'
Objects.object[204].requestsRate = []
Objects.object.insert(205, None)
Objects.object[205] = Dummy()
Objects.object[205].ifacename = 'IAchieveGroups'
Objects.object[205].oblocation = 'client'
Objects.object[205].obtype = []
Objects.object[205].obtype.insert(0, None)
Objects.object[205].obtype[0] = 'account'
Objects.object[205].requestsRate = []
Objects.object.insert(206, None)
Objects.object[206] = Dummy()
Objects.object[206].ifacename = 'IHangarSpaces'
Objects.object[206].oblocation = 'client'
Objects.object[206].obtype = []
Objects.object[206].obtype.insert(0, None)
Objects.object[206].obtype[0] = 'account'
Objects.object[206].requestsRate = []
Objects.object.insert(207, None)
Objects.object[207] = Dummy()
Objects.object[207].ifacename = 'IHangarSpacesHash'
Objects.object[207].oblocation = 'server'
Objects.object[207].obtype = []
Objects.object[207].obtype.insert(0, None)
Objects.object[207].obtype[0] = 'account'
Objects.object[207].requestsRate = []
Objects.object.insert(208, None)
Objects.object[208] = Dummy()
Objects.object[208].ifacename = 'ICurrentHangarSpace'
Objects.object[208].oblocation = 'client'
Objects.object[208].obtype = []
Objects.object[208].obtype.insert(0, None)
Objects.object[208].obtype[0] = 'account'
Objects.object[208].requestsRate = []
Objects.object.insert(209, None)
Objects.object[209] = Dummy()
Objects.object[209].ifacename = 'ICurrentHangarSpace'
Objects.object[209].oblocation = 'client'
Objects.object[209].obtype = []
Objects.object[209].obtype.insert(0, None)
Objects.object[209].obtype[0] = 'preview'
Objects.object[209].requestsRate = []
Objects.object.insert(210, None)
Objects.object[210] = Dummy()
Objects.object[210].ifacename = 'IError'
Objects.object[210].oblocation = 'mixed'
Objects.object[210].obtype = []
Objects.object[210].obtype.insert(0, None)
Objects.object[210].obtype[0] = 'error'
Objects.object[210].requestsRate = []
Objects.object.insert(211, None)
Objects.object[211] = Dummy()
Objects.object[211].ifacename = 'IActiveEvents'
Objects.object[211].oblocation = 'server'
Objects.object[211].obtype = []
Objects.object[211].obtype.insert(0, None)
Objects.object[211].obtype[0] = 'account'
Objects.object[211].requestsRate = []
Objects.object.insert(212, None)
Objects.object[212] = Dummy()
Objects.object[212].ifacename = 'IAutoFindSquad'
Objects.object[212].oblocation = 'server'
Objects.object[212].obtype = []
Objects.object[212].obtype.insert(0, None)
Objects.object[212].obtype[0] = 'account'
Objects.object[212].requestsRate = []
Objects.object.insert(213, None)
Objects.object[213] = Dummy()
Objects.object[213].ifacename = 'IAutoFindSquadList'
Objects.object[213].oblocation = 'server'
Objects.object[213].obtype = []
Objects.object[213].obtype.insert(0, None)
Objects.object[213].obtype[0] = 'account'
Objects.object[213].requestsRate = []
Objects.object.insert(214, None)
Objects.object[214] = Dummy()
Objects.object[214].ifacename = 'IPlaneBirthday'
Objects.object[214].oblocation = 'mixed'
Objects.object[214].obtype = []
Objects.object[214].obtype.insert(0, None)
Objects.object[214].obtype[0] = 'plane'
Objects.object[214].requestsRate = []
Objects.object.insert(215, None)
Objects.object[215] = Dummy()
Objects.object[215].ifacename = 'IPlaneBirthdayBonus'
Objects.object[215].oblocation = 'client'
Objects.object[215].obtype = []
Objects.object[215].obtype.insert(0, None)
Objects.object[215].obtype[0] = 'plane'
Objects.object[215].obtype.insert(1, None)
Objects.object[215].obtype[1] = 'birthday'
Objects.object[215].requestsRate = []
Objects.object.insert(216, None)
Objects.object[216] = Dummy()
Objects.object[216].ifacename = 'IPlaneBirthdayProgress'
Objects.object[216].oblocation = 'server'
Objects.object[216].obtype = []
Objects.object[216].obtype.insert(0, None)
Objects.object[216].obtype[0] = 'plane'
Objects.object[216].obtype.insert(1, None)
Objects.object[216].obtype[1] = 'birthday'
Objects.object[216].requestsRate = []
Objects.object.insert(217, None)
Objects.object[217] = Dummy()
Objects.object[217].ifacename = 'IInterview'
Objects.object[217].oblocation = 'mixed'
Objects.object[217].obtype = []
Objects.object[217].obtype.insert(0, None)
Objects.object[217].obtype[0] = 'account'
Objects.object[217].requestsRate = []
Objects.object.insert(218, None)
Objects.object[218] = Dummy()
Objects.object[218].ifacename = 'ISkinnerBoxEndAction'
Objects.object[218].oblocation = 'server'
Objects.object[218].obtype = []
Objects.object[218].obtype.insert(0, None)
Objects.object[218].obtype[0] = 'account'
Objects.object[218].requestsRate = []
Objects.object.insert(219, None)
Objects.object[219] = Dummy()
Objects.object[219].ifacename = 'ITicketPrice'
Objects.object[219].oblocation = 'server'
Objects.object[219].obtype = []
Objects.object[219].obtype.insert(0, None)
Objects.object[219].obtype[0] = 'plane'
Objects.object[219].requestsRate = []
Objects.object.insert(220, None)
Objects.object[220] = Dummy()
Objects.object[220].ifacename = 'IModifiers'
Objects.object[220].oblocation = 'client'
Objects.object[220].obtype = []
Objects.object[220].obtype.insert(0, None)
Objects.object[220].obtype[0] = 'consumable'
Objects.object[220].requestsRate = []
Objects.object.insert(221, None)
Objects.object[221] = Dummy()
Objects.object[221].ifacename = 'IModifiers'
Objects.object[221].oblocation = 'client'
Objects.object[221].obtype = []
Objects.object[221].obtype.insert(0, None)
Objects.object[221].obtype[0] = 'equipment'
Objects.object[221].requestsRate = []
Objects.object.insert(222, None)
Objects.object[222] = Dummy()
Objects.object[222].ifacename = 'ITicketPrice'
Objects.object[222].oblocation = 'client'
Objects.object[222].obtype = []
Objects.object[222].obtype.insert(0, None)
Objects.object[222].obtype[0] = 'consumable'
Objects.object[222].requestsRate = []
Objects.object.insert(223, None)
Objects.object[223] = Dummy()
Objects.object[223].ifacename = 'ITicketPrice'
Objects.object[223].oblocation = 'client'
Objects.object[223].obtype = []
Objects.object[223].obtype.insert(0, None)
Objects.object[223].obtype[0] = 'equipment'
Objects.object[223].requestsRate = []
Objects.object.insert(224, None)
Objects.object[224] = Dummy()
Objects.object[224].expiringTime = 86400
Objects.object[224].ifacename = 'IExchangeTicketPrice'
Objects.object[224].oblocation = 'server'
Objects.object[224].obtype = []
Objects.object[224].obtype.insert(0, None)
Objects.object[224].obtype[0] = 'account'
Objects.object[224].requestsRate = []
Objects.object.insert(225, None)
Objects.object[225] = Dummy()
Objects.object[225].ifacename = 'IGoldDiscount'
Objects.object[225].oblocation = 'server'
Objects.object[225].obtype = []
Objects.object[225].obtype.insert(0, None)
Objects.object[225].obtype[0] = 'plane'
Objects.object[225].requestsRate = []
Objects.object.insert(226, None)
Objects.object[226] = Dummy()
Objects.object[226].ifacename = 'IExchangeGoldTicket'
Objects.object[226].oblocation = 'server'
Objects.object[226].obtype = []
Objects.object[226].obtype.insert(0, None)
Objects.object[226].obtype[0] = 'account'
Objects.object[226].requestsRate = []
Objects.object.insert(227, None)
Objects.object[227] = Dummy()
Objects.object[227].ifacename = 'ITicketPlanes'
Objects.object[227].oblocation = 'server'
Objects.object[227].obtype = []
Objects.object[227].obtype.insert(0, None)
Objects.object[227].obtype[0] = 'account'
Objects.object[227].requestsRate = []
Objects.object.insert(228, None)
Objects.object[228] = Dummy()
Objects.object[228].ifacename = 'IPlaneBirthdayEnabled'
Objects.object[228].oblocation = 'server'
Objects.object[228].obtype = []
Objects.object[228].obtype.insert(0, None)
Objects.object[228].obtype[0] = 'account'
Objects.object[228].requestsRate = []
Objects.object.insert(229, None)
Objects.object[229] = Dummy()
Objects.object[229].ifacename = 'IRequiredExperience'
Objects.object[229].oblocation = 'client'
Objects.object[229].obtype = []
Objects.object[229].obtype.insert(0, None)
Objects.object[229].obtype[0] = 'plane'
Objects.object[229].requestsRate = []
Objects.object.insert(230, None)
Objects.object[230] = Dummy()
Objects.object[230].ifacename = 'IPlaneWeapons'
Objects.object[230].oblocation = 'client'
Objects.object[230].obtype = []
Objects.object[230].obtype.insert(0, None)
Objects.object[230].obtype[0] = 'plane'
Objects.object[230].requestsRate = []
Objects.object.insert(231, None)
Objects.object[231] = Dummy()
Objects.object[231].ifacename = 'IPlaneWeapons'
Objects.object[231].oblocation = 'client'
Objects.object[231].obtype = []
Objects.object[231].obtype.insert(0, None)
Objects.object[231].obtype[0] = 'planePreset'
Objects.object[231].requestsRate = []
Objects.object.insert(232, None)
Objects.object[232] = Dummy()
Objects.object[232].ifacename = 'IWeaponInfo'
Objects.object[232].oblocation = 'client'
Objects.object[232].obtype = []
Objects.object[232].obtype.insert(0, None)
Objects.object[232].obtype[0] = 'plane'
Objects.object[232].obtype.insert(1, None)
Objects.object[232].obtype[1] = 'weaponslot'
Objects.object[232].obtype.insert(2, None)
Objects.object[232].obtype[2] = 'weaponConfig'
Objects.object[232].requestsRate = []
Objects.object.insert(233, None)
Objects.object[233] = Dummy()
Objects.object[233].ifacename = 'IPremiumCost'
Objects.object[233].oblocation = 'client'
Objects.object[233].obtype = []
Objects.object[233].obtype.insert(0, None)
Objects.object[233].obtype[0] = 'account'
Objects.object[233].requestsRate = []
Objects.object.insert(234, None)
Objects.object[234] = Dummy()
Objects.object[234].ifacename = 'IWaitingScreen'
Objects.object[234].oblocation = 'client'
Objects.object[234].obtype = []
Objects.object[234].obtype.insert(0, None)
Objects.object[234].obtype[0] = 'account'
Objects.object[234].requestsRate = []
Objects.object.insert(235, None)
Objects.object[235] = Dummy()
Objects.object[235].ifacename = 'IAvaregeTime'
Objects.object[235].oblocation = 'server'
Objects.object[235].obtype = []
Objects.object[235].obtype.insert(0, None)
Objects.object[235].obtype[0] = 'plane'
Objects.object[235].obtype.insert(1, None)
Objects.object[235].obtype[1] = 'arenaType'
Objects.object[235].requestsRate = []
Objects.object.insert(236, None)
Objects.object[236] = Dummy()
Objects.object[236].ifacename = 'IAvaregeTime'
Objects.object[236].oblocation = 'server'
Objects.object[236].obtype = []
Objects.object[236].obtype.insert(0, None)
Objects.object[236].obtype[0] = 'squad'
Objects.object[236].obtype.insert(1, None)
Objects.object[236].obtype[1] = 'arenaType'
Objects.object[236].requestsRate = []
Objects.object.insert(237, None)
Objects.object[237] = Dummy()
Objects.object[237].ifacename = 'ICamouflageStatus'
Objects.object[237].oblocation = 'server'
Objects.object[237].obtype = []
Objects.object[237].obtype.insert(0, None)
Objects.object[237].obtype[0] = 'camouflageID'
Objects.object[237].requestsRate = []
Objects.object.insert(238, None)
Objects.object[238] = Dummy()
Objects.object[238].ifacename = 'IReferralStatus'
Objects.object[238].oblocation = 'server'
Objects.object[238].obtype = []
Objects.object[238].obtype.insert(0, None)
Objects.object[238].obtype[0] = 'account'
Objects.object[238].requestsRate = []
Objects.object.insert(239, None)
Objects.object[239] = Dummy()
Objects.object[239].ifacename = 'IReferralDescription'
Objects.object[239].oblocation = 'server'
Objects.object[239].obtype = []
Objects.object[239].obtype.insert(0, None)
Objects.object[239].obtype[0] = 'account'
Objects.object[239].requestsRate = []
Objects.object.insert(240, None)
Objects.object[240] = Dummy()
Objects.object[240].ifacename = 'IReferralInviteLink'
Objects.object[240].oblocation = 'client'
Objects.object[240].obtype = []
Objects.object[240].obtype.insert(0, None)
Objects.object[240].obtype[0] = 'account'
Objects.object[240].requestsRate = []
Objects.object.insert(241, None)
Objects.object[241] = Dummy()
Objects.object[241].ifacename = 'IReferralLinks'
Objects.object[241].oblocation = 'server'
Objects.object[241].obtype = []
Objects.object[241].obtype.insert(0, None)
Objects.object[241].obtype[0] = 'account'
Objects.object[241].requestsRate = []
Objects.object.insert(242, None)
Objects.object[242] = Dummy()
Objects.object[242].ifacename = 'IReferralRecruitStatus'
Objects.object[242].oblocation = 'server'
Objects.object[242].obtype = []
Objects.object[242].obtype.insert(0, None)
Objects.object[242].obtype[0] = 'account'
Objects.object[242].requestsRate = []
Objects.object.insert(243, None)
Objects.object[243] = Dummy()
Objects.object[243].ifacename = 'IReferralRecruitArchiveStatus'
Objects.object[243].oblocation = 'server'
Objects.object[243].obtype = []
Objects.object[243].obtype.insert(0, None)
Objects.object[243].obtype[0] = 'account'
Objects.object[243].requestsRate = []
Objects.object.insert(244, None)
Objects.object[244] = Dummy()
Objects.object[244].ifacename = 'IReferralRecruitOnlineStatus'
Objects.object[244].oblocation = 'server'
Objects.object[244].obtype = []
Objects.object[244].obtype.insert(0, None)
Objects.object[244].obtype[0] = 'account'
Objects.object[244].requestsRate = []
Objects.object.insert(245, None)
Objects.object[245] = Dummy()
Objects.object[245].ifacename = 'IReferralRecruitTasks'
Objects.object[245].oblocation = 'server'
Objects.object[245].obtype = []
Objects.object[245].obtype.insert(0, None)
Objects.object[245].obtype[0] = 'account'
Objects.object[245].requestsRate = []
Objects.object.insert(246, None)
Objects.object[246] = Dummy()
Objects.object[246].ifacename = 'IReferralCheckpointBonus'
Objects.object[246].oblocation = 'server'
Objects.object[246].obtype = []
Objects.object[246].obtype.insert(0, None)
Objects.object[246].obtype[0] = 'refcheckpoint'
Objects.object[246].requestsRate = []
Objects.object.insert(247, None)
Objects.object[247] = Dummy()
Objects.object[247].ifacename = 'IReferralCheckpointGetBonus'
Objects.object[247].oblocation = 'server'
Objects.object[247].obtype = []
Objects.object[247].obtype.insert(0, None)
Objects.object[247].obtype[0] = 'questoperation'
Objects.object[247].requestsRate = []
Objects.object.insert(248, None)
Objects.object[248] = Dummy()
Objects.object[248].ifacename = 'IReferralRecruiterQuests'
Objects.object[248].oblocation = 'server'
Objects.object[248].obtype = []
Objects.object[248].obtype.insert(0, None)
Objects.object[248].obtype[0] = 'account'
Objects.object[248].requestsRate = []
Objects.object.insert(249, None)
Objects.object[249] = Dummy()
Objects.object[249].ifacename = 'IReferralQuestDescription'
Objects.object[249].oblocation = 'server'
Objects.object[249].obtype = []
Objects.object[249].obtype.insert(0, None)
Objects.object[249].obtype[0] = 'referralquest'
Objects.object[249].requestsRate = []
Objects.object.insert(250, None)
Objects.object[250] = Dummy()
Objects.object[250].ifacename = 'IReferralQuestStatus'
Objects.object[250].oblocation = 'server'
Objects.object[250].obtype = []
Objects.object[250].obtype.insert(0, None)
Objects.object[250].obtype[0] = 'referralquest'
Objects.object[250].requestsRate = []
Objects.object.insert(251, None)
Objects.object[251] = Dummy()
Objects.object[251].ifacename = 'IReferralQuestGetBonus'
Objects.object[251].oblocation = 'server'
Objects.object[251].obtype = []
Objects.object[251].obtype.insert(0, None)
Objects.object[251].obtype[0] = 'questoperation'
Objects.object[251].requestsRate = []
Objects.object.insert(252, None)
Objects.object[252] = Dummy()
Objects.object[252].ifacename = 'IReferralSendInvite'
Objects.object[252].oblocation = 'server'
Objects.object[252].obtype = []
Objects.object[252].obtype.insert(0, None)
Objects.object[252].obtype[0] = 'referralinvite'
Objects.object[252].requestsRate = []
Objects.object.insert(253, None)
Objects.object[253] = Dummy()
Objects.object[253].ifacename = 'IReferralPublicInvite'
Objects.object[253].oblocation = 'client'
Objects.object[253].obtype = []
Objects.object[253].obtype.insert(0, None)
Objects.object[253].obtype[0] = 'referralinvite'
Objects.object[253].requestsRate = []
Objects.object.insert(254, None)
Objects.object[254] = Dummy()
Objects.object[254].expiringTime = 300
Objects.object[254].ifacename = 'IWarActionState'
Objects.object[254].oblocation = 'server'
Objects.object[254].obtype = []
Objects.object[254].obtype.insert(0, None)
Objects.object[254].obtype[0] = 'account'
Objects.object[254].requestsRate = []
Objects.object.insert(255, None)
Objects.object[255] = Dummy()
Objects.object[255].ifacename = 'IWarActionForce'
Objects.object[255].oblocation = 'server'
Objects.object[255].obtype = []
Objects.object[255].obtype.insert(0, None)
Objects.object[255].obtype[0] = 'account'
Objects.object[255].requestsRate = []
Objects.object.insert(256, None)
Objects.object[256] = Dummy()
Objects.object[256].expiringTime = 300
Objects.object[256].ifacename = 'IWarActionFraction'
Objects.object[256].oblocation = 'server'
Objects.object[256].obtype = []
Objects.object[256].obtype.insert(0, None)
Objects.object[256].obtype[0] = 'account'
Objects.object[256].requestsRate = []
Objects.object.insert(257, None)
Objects.object[257] = Dummy()
Objects.object[257].expiringTime = 300
Objects.object[257].ifacename = 'IWarActionInfo'
Objects.object[257].oblocation = 'server'
Objects.object[257].obtype = []
Objects.object[257].obtype.insert(0, None)
Objects.object[257].obtype[0] = 'account'
Objects.object[257].requestsRate = []
Objects.object.insert(258, None)
Objects.object[258] = Dummy()
Objects.object[258].expiringTime = 300
Objects.object[258].ifacename = 'IWarActionBattleStats'
Objects.object[258].oblocation = 'server'
Objects.object[258].obtype = []
Objects.object[258].obtype.insert(0, None)
Objects.object[258].obtype[0] = 'account'
Objects.object[258].requestsRate = []
Objects.object.insert(259, None)
Objects.object[259] = Dummy()
Objects.object[259].expiringTime = 300
Objects.object[259].ifacename = 'IWarActionAgregatedBattleStats'
Objects.object[259].oblocation = 'server'
Objects.object[259].obtype = []
Objects.object[259].obtype.insert(0, None)
Objects.object[259].obtype[0] = 'account'
Objects.object[259].requestsRate = []
Objects.object.insert(260, None)
Objects.object[260] = Dummy()
Objects.object[260].expiringTime = 300
Objects.object[260].ifacename = 'IWarActionTrophiesStatus'
Objects.object[260].oblocation = 'server'
Objects.object[260].obtype = []
Objects.object[260].obtype.insert(0, None)
Objects.object[260].obtype[0] = 'account'
Objects.object[260].requestsRate = []
Objects.object.insert(261, None)
Objects.object[261] = Dummy()
Objects.object[261].ifacename = 'IWarActionPlaneQuestStatus'
Objects.object[261].oblocation = 'server'
Objects.object[261].obtype = []
Objects.object[261].obtype.insert(0, None)
Objects.object[261].obtype[0] = 'plane'
Objects.object[261].requestsRate = []
Objects.object.insert(262, None)
Objects.object[262] = Dummy()
Objects.object[262].ifacename = 'IWarCash'
Objects.object[262].oblocation = 'server'
Objects.object[262].obtype = []
Objects.object[262].obtype.insert(0, None)
Objects.object[262].obtype[0] = 'warCash'
Objects.object[262].requestsRate = []
Objects.object.insert(263, None)
Objects.object[263] = Dummy()
Objects.object[263].ifacename = 'ILTOStatus'
Objects.object[263].oblocation = 'server'
Objects.object[263].obtype = []
Objects.object[263].obtype.insert(0, None)
Objects.object[263].obtype[0] = 'account'
Objects.object[263].requestsRate = []
Objects.object.insert(264, None)
Objects.object[264] = Dummy()
Objects.object[264].ifacename = 'ITutorialLessonList'
Objects.object[264].oblocation = 'client'
Objects.object[264].obtype = []
Objects.object[264].obtype.insert(0, None)
Objects.object[264].obtype[0] = 'account'
Objects.object[264].requestsRate = []
Objects.object.insert(265, None)
Objects.object[265] = Dummy()
Objects.object[265].ifacename = 'ITutorialLessonServer'
Objects.object[265].oblocation = 'server'
Objects.object[265].obtype = []
Objects.object[265].obtype.insert(0, None)
Objects.object[265].obtype[0] = 'tutorial'
Objects.object[265].requestsRate = []
Objects.object.insert(266, None)
Objects.object[266] = Dummy()
Objects.object[266].ifacename = 'ITutorialLessonClient'
Objects.object[266].oblocation = 'client'
Objects.object[266].obtype = []
Objects.object[266].obtype.insert(0, None)
Objects.object[266].obtype[0] = 'tutorial'
Objects.object[266].requestsRate = []
Objects.object.insert(267, None)
Objects.object[267] = Dummy()
Objects.object[267].ifacename = 'ITutorialLesson'
Objects.object[267].oblocation = 'client'
Objects.object[267].obtype = []
Objects.object[267].obtype.insert(0, None)
Objects.object[267].obtype[0] = 'tutorial'
Objects.object[267].requestsRate = []
Objects.object.insert(268, None)
Objects.object[268] = Dummy()
Objects.object[268].ifacename = 'ITutorialPromptParams'
Objects.object[268].oblocation = 'client'
Objects.object[268].obtype = []
Objects.object[268].obtype.insert(0, None)
Objects.object[268].obtype[0] = 'tutorial'
Objects.object[268].requestsRate = []
Objects.object.insert(269, None)
Objects.object[269] = Dummy()
Objects.object[269].ifacename = 'ITutorialLessonWindow'
Objects.object[269].oblocation = 'server'
Objects.object[269].obtype = []
Objects.object[269].obtype.insert(0, None)
Objects.object[269].obtype[0] = 'account'
Objects.object[269].requestsRate = []
Objects.object.insert(270, None)
Objects.object[270] = Dummy()
Objects.object[270].ifacename = 'IDebugCommand'
Objects.object[270].oblocation = 'server'
Objects.object[270].obtype = []
Objects.object[270].obtype.insert(0, None)
Objects.object[270].obtype[0] = 'account'
Objects.object[270].requestsRate = []
Objects.object.insert(271, None)
Objects.object[271] = Dummy()
Objects.object[271].ifacename = 'IPack'
Objects.object[271].oblocation = 'client'
Objects.object[271].obtype = []
Objects.object[271].obtype.insert(0, None)
Objects.object[271].obtype[0] = 'pack'
Objects.object[271].requestsRate = []
Objects.object.insert(272, None)
Objects.object[272] = Dummy()
Objects.object[272].ifacename = 'IPrice'
Objects.object[272].oblocation = 'server'
Objects.object[272].obtype = []
Objects.object[272].obtype.insert(0, None)
Objects.object[272].obtype[0] = 'pack'
Objects.object[272].requestsRate = []
Objects.object.insert(273, None)
Objects.object[273] = Dummy()
Objects.object[273].ifacename = 'IStatus'
Objects.object[273].oblocation = 'server'
Objects.object[273].obtype = []
Objects.object[273].obtype.insert(0, None)
Objects.object[273].obtype[0] = 'pack'
Objects.object[273].requestsRate = []
Objects.object.insert(274, None)
Objects.object[274] = Dummy()
Objects.object[274].ifacename = 'IFemalePilotPackList'
Objects.object[274].oblocation = 'server'
Objects.object[274].obtype = []
Objects.object[274].obtype.insert(0, None)
Objects.object[274].obtype[0] = 'account'
Objects.object[274].requestsRate = []