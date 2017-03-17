# Embedded file name: scripts/common/exchangeapi/_ifaces.py
import Math
import math
import consts
true = True
false = False

class Dummy():
    pass


isServerDatabase = False

class CACHE_TYPE():
    NONE = 0
    FULL_CACHE = 1
    MEM_CACHE = 2
    ALL_TYPES = (NONE, FULL_CACHE, MEM_CACHE)


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


Ifaces = Dummy()
Ifaces.iface = []
Ifaces.iface.insert(0, None)
Ifaces.iface[0] = Dummy()
Ifaces.iface[0].attr = []
Ifaces.iface[0].attr.insert(0, None)
Ifaces.iface[0].attr[0] = 'experience'
Ifaces.iface[0].attr.insert(1, None)
Ifaces.iface[0].attr[1] = 'exchangeFreeXPRate'
Ifaces.iface[0].attr.insert(2, None)
Ifaces.iface[0].attr[2] = 'planeXPList'
Ifaces.iface[0].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[0].callbackSubscriable = false
Ifaces.iface[0].defaultCallback = ''
Ifaces.iface[0].ifacename = 'IXPExchange'
Ifaces.iface[0].parent = []
Ifaces.iface.insert(1, None)
Ifaces.iface[1] = Dummy()
Ifaces.iface[1].attr = []
Ifaces.iface[1].attr.insert(0, None)
Ifaces.iface[1].attr[0] = 'ownerID'
Ifaces.iface[1].attr.insert(1, None)
Ifaces.iface[1].attr[1] = 'accountIDs'
Ifaces.iface[1].attr.insert(2, None)
Ifaces.iface[1].attr[2] = 'maxSquadSize'
Ifaces.iface[1].attr.insert(3, None)
Ifaces.iface[1].attr[3] = 'memberIDs'
Ifaces.iface[1].attr.insert(4, None)
Ifaces.iface[1].attr[4] = 'arenaType'
Ifaces.iface[1].attr.insert(5, None)
Ifaces.iface[1].attr[5] = 'autoSquadFinder'
Ifaces.iface[1].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[1].callbackSubscriable = true
Ifaces.iface[1].defaultCallback = 'FlightModel.ISquad'
Ifaces.iface[1].ifacename = 'ISquad'
Ifaces.iface[1].parent = []
Ifaces.iface.insert(2, None)
Ifaces.iface[2] = Dummy()
Ifaces.iface[2].attr = []
Ifaces.iface[2].attr.insert(0, None)
Ifaces.iface[2].attr[0] = 'name'
Ifaces.iface[2].attr.insert(1, None)
Ifaces.iface[2].attr[1] = 'clanAbbrev'
Ifaces.iface[2].attr.insert(2, None)
Ifaces.iface[2].attr[2] = 'state'
Ifaces.iface[2].attr.insert(3, None)
Ifaces.iface[2].attr[3] = 'airplaneGlobalID'
Ifaces.iface[2].attr.insert(4, None)
Ifaces.iface[2].attr[4] = 'isMe'
Ifaces.iface[2].attr.insert(5, None)
Ifaces.iface[2].attr[5] = 'accountID'
Ifaces.iface[2].attr.insert(6, None)
Ifaces.iface[2].attr[6] = 'squadID'
Ifaces.iface[2].attr.insert(7, None)
Ifaces.iface[2].attr[7] = 'accountState'
Ifaces.iface[2].attr.insert(8, None)
Ifaces.iface[2].attr[8] = 'supportedModes'
Ifaces.iface[2].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[2].callbackSubscriable = false
Ifaces.iface[2].defaultCallback = ''
Ifaces.iface[2].ifacename = 'ISquadMember'
Ifaces.iface[2].parent = []
Ifaces.iface.insert(3, None)
Ifaces.iface[3] = Dummy()
Ifaces.iface[3].attr = []
Ifaces.iface[3].attr.insert(0, None)
Ifaces.iface[3].attr[0] = 'ownerName'
Ifaces.iface[3].attr.insert(1, None)
Ifaces.iface[3].attr[1] = 'ownerClanAbbrev'
Ifaces.iface[3].attr.insert(2, None)
Ifaces.iface[3].attr[2] = 'time'
Ifaces.iface[3].attr.insert(3, None)
Ifaces.iface[3].attr[3] = 'squadID'
Ifaces.iface[3].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[3].callbackSubscriable = true
Ifaces.iface[3].defaultCallback = 'iface.listener'
Ifaces.iface[3].ifacename = 'ISquadInvitation'
Ifaces.iface[3].parent = []
Ifaces.iface.insert(4, None)
Ifaces.iface[4] = Dummy()
Ifaces.iface[4].attr = []
Ifaces.iface[4].attr.insert(0, None)
Ifaces.iface[4].attr[0] = 'arenaType'
Ifaces.iface[4].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[4].callbackSubscriable = false
Ifaces.iface[4].defaultCallback = ''
Ifaces.iface[4].ifacename = 'IBattleState'
Ifaces.iface[4].parent = []
Ifaces.iface.insert(5, None)
Ifaces.iface[5] = Dummy()
Ifaces.iface[5].attr = []
Ifaces.iface[5].attr.insert(0, None)
Ifaces.iface[5].attr[0] = 'password'
Ifaces.iface[5].attr.insert(1, None)
Ifaces.iface[5].attr[1] = 'jid'
Ifaces.iface[5].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[5].callbackSubscriable = false
Ifaces.iface[5].defaultCallback = ''
Ifaces.iface[5].ifacename = 'ISquadChatChannel'
Ifaces.iface[5].parent = []
Ifaces.iface.insert(6, None)
Ifaces.iface[6] = Dummy()
Ifaces.iface[6].attr = []
Ifaces.iface[6].attr.insert(0, None)
Ifaces.iface[6].attr[0] = 'patchID'
Ifaces.iface[6].attr.insert(1, None)
Ifaces.iface[6].attr[1] = 'components'
Ifaces.iface[6].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[6].callbackSubscriable = false
Ifaces.iface[6].defaultCallback = ''
Ifaces.iface[6].ifacename = 'ICurrentPatch'
Ifaces.iface[6].parent = []
Ifaces.iface.insert(7, None)
Ifaces.iface[7] = Dummy()
Ifaces.iface[7].attr = []
Ifaces.iface[7].attr.insert(0, None)
Ifaces.iface[7].attr[0] = 'patchData'
Ifaces.iface[7].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[7].callbackSubscriable = false
Ifaces.iface[7].defaultCallback = ''
Ifaces.iface[7].ifacename = 'IPatch'
Ifaces.iface[7].parent = []
Ifaces.iface.insert(8, None)
Ifaces.iface[8] = Dummy()
Ifaces.iface[8].attr = []
Ifaces.iface[8].attr.insert(0, None)
Ifaces.iface[8].attr[0] = 'patchID'
Ifaces.iface[8].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[8].callbackSubscriable = false
Ifaces.iface[8].defaultCallback = ''
Ifaces.iface[8].ifacename = 'IComponents'
Ifaces.iface[8].parent = []
Ifaces.iface.insert(9, None)
Ifaces.iface[9] = Dummy()
Ifaces.iface[9].attr = []
Ifaces.iface[9].attr.insert(0, None)
Ifaces.iface[9].attr[0] = 'messageIDs'
Ifaces.iface[9].cacheType = CACHE_TYPE.NONE
Ifaces.iface[9].callbackSubscriable = false
Ifaces.iface[9].defaultCallback = ''
Ifaces.iface[9].ifacename = 'ILastMessages'
Ifaces.iface[9].parent = []
Ifaces.iface.insert(10, None)
Ifaces.iface[10] = Dummy()
Ifaces.iface[10].attr = []
Ifaces.iface[10].attr.insert(0, None)
Ifaces.iface[10].attr[0] = 'utcTime'
Ifaces.iface[10].attr.insert(1, None)
Ifaces.iface[10].attr[1] = 'msgType'
Ifaces.iface[10].attr.insert(2, None)
Ifaces.iface[10].attr[2] = 'msgHeader'
Ifaces.iface[10].attr.insert(3, None)
Ifaces.iface[10].attr[3] = 'msgData'
Ifaces.iface[10].attr.insert(4, None)
Ifaces.iface[10].attr[4] = 'chain'
Ifaces.iface[10].attr.insert(5, None)
Ifaces.iface[10].attr[5] = 'senderName'
Ifaces.iface[10].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[10].callbackSubscriable = false
Ifaces.iface[10].defaultCallback = 'iface.listener'
Ifaces.iface[10].ifacename = 'IMessage'
Ifaces.iface[10].parent = []
Ifaces.iface.insert(11, None)
Ifaces.iface[11] = Dummy()
Ifaces.iface[11].attr = []
Ifaces.iface[11].attr.insert(0, None)
Ifaces.iface[11].attr[0] = 'msgType'
Ifaces.iface[11].attr.insert(1, None)
Ifaces.iface[11].attr[1] = 'msgData'
Ifaces.iface[11].attr.insert(2, None)
Ifaces.iface[11].attr[2] = 'senderName'
Ifaces.iface[11].cacheType = CACHE_TYPE.NONE
Ifaces.iface[11].callbackSubscriable = false
Ifaces.iface[11].defaultCallback = ''
Ifaces.iface[11].ifacename = 'IMessageAction'
Ifaces.iface[11].parent = []
Ifaces.iface.insert(12, None)
Ifaces.iface[12] = Dummy()
Ifaces.iface[12].attr = []
Ifaces.iface[12].attr.insert(0, None)
Ifaces.iface[12].attr[0] = 'planeIDs'
Ifaces.iface[12].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[12].callbackSubscriable = false
Ifaces.iface[12].defaultCallback = ''
Ifaces.iface[12].ifacename = 'IPlanes'
Ifaces.iface[12].parent = []
Ifaces.iface.insert(13, None)
Ifaces.iface[13] = Dummy()
Ifaces.iface[13].attr = []
Ifaces.iface[13].attr.insert(0, None)
Ifaces.iface[13].attr[0] = 'classValue'
Ifaces.iface[13].attr.insert(1, None)
Ifaces.iface[13].attr[1] = 'classIcoPath'
Ifaces.iface[13].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[13].callbackSubscriable = false
Ifaces.iface[13].defaultCallback = ''
Ifaces.iface[13].ifacename = 'IClass'
Ifaces.iface[13].parent = []
Ifaces.iface.insert(14, None)
Ifaces.iface[14] = Dummy()
Ifaces.iface[14].attr = []
Ifaces.iface[14].attr.insert(0, None)
Ifaces.iface[14].attr[0] = 'status'
Ifaces.iface[14].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[14].callbackSubscriable = false
Ifaces.iface[14].defaultCallback = ''
Ifaces.iface[14].ifacename = 'IStatus'
Ifaces.iface[14].parent = []
Ifaces.iface.insert(15, None)
Ifaces.iface[15] = Dummy()
Ifaces.iface[15].attr = []
Ifaces.iface[15].attr.insert(0, None)
Ifaces.iface[15].attr[0] = 'name'
Ifaces.iface[15].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[15].callbackSubscriable = false
Ifaces.iface[15].defaultCallback = ''
Ifaces.iface[15].ifacename = 'IName'
Ifaces.iface[15].parent = []
Ifaces.iface.insert(16, None)
Ifaces.iface[16] = Dummy()
Ifaces.iface[16].attr = []
Ifaces.iface[16].attr.insert(0, None)
Ifaces.iface[16].attr[0] = 'level'
Ifaces.iface[16].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[16].callbackSubscriable = false
Ifaces.iface[16].defaultCallback = ''
Ifaces.iface[16].ifacename = 'ILevel'
Ifaces.iface[16].parent = []
Ifaces.iface.insert(17, None)
Ifaces.iface[17] = Dummy()
Ifaces.iface[17].attr = []
Ifaces.iface[17].attr.insert(0, None)
Ifaces.iface[17].attr[0] = 'type'
Ifaces.iface[17].attr.insert(1, None)
Ifaces.iface[17].attr[1] = 'typeString'
Ifaces.iface[17].attr.insert(2, None)
Ifaces.iface[17].attr[2] = 'typeIcoPath'
Ifaces.iface[17].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[17].callbackSubscriable = false
Ifaces.iface[17].defaultCallback = ''
Ifaces.iface[17].ifacename = 'IType'
Ifaces.iface[17].parent = []
Ifaces.iface.insert(18, None)
Ifaces.iface[18] = Dummy()
Ifaces.iface[18].attr = []
Ifaces.iface[18].attr.insert(0, None)
Ifaces.iface[18].attr[0] = 'nationID'
Ifaces.iface[18].attr.insert(1, None)
Ifaces.iface[18].attr[1] = 'flagPath'
Ifaces.iface[18].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[18].callbackSubscriable = false
Ifaces.iface[18].defaultCallback = ''
Ifaces.iface[18].ifacename = 'INation'
Ifaces.iface[18].parent = []
Ifaces.iface.insert(19, None)
Ifaces.iface[19] = Dummy()
Ifaces.iface[19].attr = []
Ifaces.iface[19].attr.insert(0, None)
Ifaces.iface[19].attr[0] = 'nationIDList'
Ifaces.iface[19].attr.insert(1, None)
Ifaces.iface[19].attr[1] = 'flagPathList'
Ifaces.iface[19].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[19].callbackSubscriable = false
Ifaces.iface[19].defaultCallback = ''
Ifaces.iface[19].ifacename = 'INationList'
Ifaces.iface[19].parent = []
Ifaces.iface.insert(20, None)
Ifaces.iface[20] = Dummy()
Ifaces.iface[20].attr = []
Ifaces.iface[20].attr.insert(0, None)
Ifaces.iface[20].attr[0] = 'price'
Ifaces.iface[20].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[20].callbackSubscriable = false
Ifaces.iface[20].defaultCallback = ''
Ifaces.iface[20].ifacename = 'IPrice'
Ifaces.iface[20].parent = []
Ifaces.iface.insert(21, None)
Ifaces.iface[21] = Dummy()
Ifaces.iface[21].attr = []
Ifaces.iface[21].attr.insert(0, None)
Ifaces.iface[21].attr[0] = 'credits'
Ifaces.iface[21].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[21].callbackSubscriable = false
Ifaces.iface[21].defaultCallback = ''
Ifaces.iface[21].ifacename = 'ISellPrice'
Ifaces.iface[21].parent = []
Ifaces.iface.insert(22, None)
Ifaces.iface[22] = Dummy()
Ifaces.iface[22].attr = []
Ifaces.iface[22].attr.insert(0, None)
Ifaces.iface[22].attr[0] = 'name'
Ifaces.iface[22].attr.insert(1, None)
Ifaces.iface[22].attr[1] = 'longName'
Ifaces.iface[22].attr.insert(2, None)
Ifaces.iface[22].attr[2] = 'middleName'
Ifaces.iface[22].attr.insert(3, None)
Ifaces.iface[22].attr[3] = 'description'
Ifaces.iface[22].attr.insert(4, None)
Ifaces.iface[22].attr[4] = 'level'
Ifaces.iface[22].attr.insert(5, None)
Ifaces.iface[22].attr[5] = 'presetsList'
Ifaces.iface[22].attr.insert(6, None)
Ifaces.iface[22].attr[6] = 'defaultPreset'
Ifaces.iface[22].attr.insert(7, None)
Ifaces.iface[22].attr[7] = 'icoPath'
Ifaces.iface[22].attr.insert(8, None)
Ifaces.iface[22].attr[8] = 'bigIcoPath'
Ifaces.iface[22].attr.insert(9, None)
Ifaces.iface[22].attr[9] = 'hudIcoPath'
Ifaces.iface[22].attr.insert(10, None)
Ifaces.iface[22].attr[10] = 'treeIcoPath'
Ifaces.iface[22].attr.insert(11, None)
Ifaces.iface[22].attr[11] = 'battleLoadingIcoPath'
Ifaces.iface[22].attr.insert(12, None)
Ifaces.iface[22].attr[12] = 'isExclusive'
Ifaces.iface[22].attr.insert(13, None)
Ifaces.iface[22].attr[13] = 'isTest'
Ifaces.iface[22].attr.insert(14, None)
Ifaces.iface[22].attr[14] = 'tagsList'
Ifaces.iface[22].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[22].callbackSubscriable = false
Ifaces.iface[22].defaultCallback = ''
Ifaces.iface[22].ifacename = 'IPlaneDescription'
Ifaces.iface[22].parent = []
Ifaces.iface.insert(23, None)
Ifaces.iface[23] = Dummy()
Ifaces.iface[23].attr = []
Ifaces.iface[23].attr.insert(0, None)
Ifaces.iface[23].attr[0] = 'messageIDs'
Ifaces.iface[23].attr.insert(1, None)
Ifaces.iface[23].attr[1] = 'storedMessages'
Ifaces.iface[23].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[23].callbackSubscriable = false
Ifaces.iface[23].defaultCallback = ''
Ifaces.iface[23].ifacename = 'IMessageSession'
Ifaces.iface[23].parent = []
Ifaces.iface.insert(24, None)
Ifaces.iface[24] = Dummy()
Ifaces.iface[24].attr = []
Ifaces.iface[24].attr.insert(0, None)
Ifaces.iface[24].attr[0] = 'name'
Ifaces.iface[24].attr.insert(1, None)
Ifaces.iface[24].attr[1] = 'modulesList'
Ifaces.iface[24].attr.insert(2, None)
Ifaces.iface[24].attr[2] = 'weaponsList'
Ifaces.iface[24].attr.insert(3, None)
Ifaces.iface[24].attr[3] = 'weaponSlotsList'
Ifaces.iface[24].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[24].callbackSubscriable = false
Ifaces.iface[24].defaultCallback = ''
Ifaces.iface[24].ifacename = 'IPlanePreset'
Ifaces.iface[24].parent = []
Ifaces.iface.insert(25, None)
Ifaces.iface[25] = Dummy()
Ifaces.iface[25].attr = []
Ifaces.iface[25].attr.insert(0, None)
Ifaces.iface[25].attr[0] = 'name'
Ifaces.iface[25].attr.insert(1, None)
Ifaces.iface[25].attr[1] = 'type'
Ifaces.iface[25].attr.insert(2, None)
Ifaces.iface[25].attr[2] = 'description'
Ifaces.iface[25].attr.insert(3, None)
Ifaces.iface[25].attr[3] = 'level'
Ifaces.iface[25].attr.insert(4, None)
Ifaces.iface[25].attr[4] = 'icoPath'
Ifaces.iface[25].attr.insert(5, None)
Ifaces.iface[25].attr[5] = 'airplanesList'
Ifaces.iface[25].attr.insert(6, None)
Ifaces.iface[25].attr[6] = 'specsList'
Ifaces.iface[25].attr.insert(7, None)
Ifaces.iface[25].attr[7] = 'suitablePlaneIDs'
Ifaces.iface[25].attr.insert(8, None)
Ifaces.iface[25].attr[8] = 'configComparison'
Ifaces.iface[25].attr.insert(9, None)
Ifaces.iface[25].attr[9] = 'requiredModules'
Ifaces.iface[25].attr.insert(10, None)
Ifaces.iface[25].attr[10] = 'armoredTargetEffective'
Ifaces.iface[25].attr.insert(11, None)
Ifaces.iface[25].attr[11] = 'buyAvailable'
Ifaces.iface[25].attr.insert(12, None)
Ifaces.iface[25].attr[12] = 'propsList'
Ifaces.iface[25].attr.insert(13, None)
Ifaces.iface[25].attr[13] = 'cmpGlobalID'
Ifaces.iface[25].cacheType = CACHE_TYPE.NONE
Ifaces.iface[25].callbackSubscriable = false
Ifaces.iface[25].defaultCallback = ''
Ifaces.iface[25].ifacename = 'IModuleDescription'
Ifaces.iface[25].parent = []
Ifaces.iface.insert(26, None)
Ifaces.iface[26] = Dummy()
Ifaces.iface[26].attr = []
Ifaces.iface[26].attr.insert(0, None)
Ifaces.iface[26].attr[0] = 'specs'
Ifaces.iface[26].attr.insert(1, None)
Ifaces.iface[26].attr[1] = 'dps'
Ifaces.iface[26].attr.insert(2, None)
Ifaces.iface[26].attr[2] = 'speedFactor'
Ifaces.iface[26].attr.insert(3, None)
Ifaces.iface[26].attr[3] = 'maneuverability'
Ifaces.iface[26].attr.insert(4, None)
Ifaces.iface[26].attr[4] = 'controllability'
Ifaces.iface[26].attr.insert(5, None)
Ifaces.iface[26].attr[5] = 'hp'
Ifaces.iface[26].attr.insert(6, None)
Ifaces.iface[26].attr[6] = 'mass'
Ifaces.iface[26].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[26].callbackSubscriable = false
Ifaces.iface[26].defaultCallback = ''
Ifaces.iface[26].ifacename = 'IConfigSpecs'
Ifaces.iface[26].parent = []
Ifaces.iface.insert(27, None)
Ifaces.iface[27] = Dummy()
Ifaces.iface[27].attr = []
Ifaces.iface[27].attr.insert(0, None)
Ifaces.iface[27].attr[0] = 'dps'
Ifaces.iface[27].attr.insert(1, None)
Ifaces.iface[27].attr[1] = 'speedFactor'
Ifaces.iface[27].attr.insert(2, None)
Ifaces.iface[27].attr[2] = 'maneuverability'
Ifaces.iface[27].attr.insert(3, None)
Ifaces.iface[27].attr[3] = 'hp'
Ifaces.iface[27].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[27].callbackSubscriable = false
Ifaces.iface[27].defaultCallback = ''
Ifaces.iface[27].ifacename = 'IShortConfigSpecs'
Ifaces.iface[27].parent = []
Ifaces.iface.insert(28, None)
Ifaces.iface[28] = Dummy()
Ifaces.iface[28].attr = []
Ifaces.iface[28].attr.insert(0, None)
Ifaces.iface[28].attr[0] = 'globalID'
Ifaces.iface[28].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[28].callbackSubscriable = false
Ifaces.iface[28].defaultCallback = ''
Ifaces.iface[28].ifacename = 'IInstalledGlobalID'
Ifaces.iface[28].parent = []
Ifaces.iface.insert(29, None)
Ifaces.iface[29] = Dummy()
Ifaces.iface[29].attr = []
Ifaces.iface[29].attr.insert(0, None)
Ifaces.iface[29].attr[0] = 'compatibleBeltIDs'
Ifaces.iface[29].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[29].callbackSubscriable = false
Ifaces.iface[29].defaultCallback = ''
Ifaces.iface[29].ifacename = 'ISuitableAmmoBelts'
Ifaces.iface[29].parent = []
Ifaces.iface.insert(30, None)
Ifaces.iface[30] = Dummy()
Ifaces.iface[30].attr = []
Ifaces.iface[30].attr.insert(0, None)
Ifaces.iface[30].attr[0] = 'name'
Ifaces.iface[30].attr.insert(1, None)
Ifaces.iface[30].attr[1] = 'hudIcoPath'
Ifaces.iface[30].attr.insert(2, None)
Ifaces.iface[30].attr[2] = 'suitableGunIDs'
Ifaces.iface[30].attr.insert(3, None)
Ifaces.iface[30].attr[3] = 'suitablePlaneIDs'
Ifaces.iface[30].attr.insert(4, None)
Ifaces.iface[30].attr[4] = 'beltType'
Ifaces.iface[30].attr.insert(5, None)
Ifaces.iface[30].attr[5] = 'caliber'
Ifaces.iface[30].attr.insert(6, None)
Ifaces.iface[30].attr[6] = 'globalMinDamage'
Ifaces.iface[30].attr.insert(7, None)
Ifaces.iface[30].attr[7] = 'globalMaxDamage'
Ifaces.iface[30].attr.insert(8, None)
Ifaces.iface[30].attr[8] = 'globalMinFireChance'
Ifaces.iface[30].attr.insert(9, None)
Ifaces.iface[30].attr[9] = 'globalMaxFireChance'
Ifaces.iface[30].attr.insert(10, None)
Ifaces.iface[30].attr[10] = 'gunNames'
Ifaces.iface[30].attr.insert(11, None)
Ifaces.iface[30].attr[11] = 'description'
Ifaces.iface[30].attr.insert(12, None)
Ifaces.iface[30].attr[12] = 'shortDescription'
Ifaces.iface[30].attr.insert(13, None)
Ifaces.iface[30].attr[13] = 'icoPathSmall'
Ifaces.iface[30].attr.insert(14, None)
Ifaces.iface[30].attr[14] = 'buyAvailable'
Ifaces.iface[30].attr.insert(15, None)
Ifaces.iface[30].attr[15] = 'tooltipDescription'
Ifaces.iface[30].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[30].callbackSubscriable = false
Ifaces.iface[30].defaultCallback = ''
Ifaces.iface[30].ifacename = 'IAmmoBeltDescription'
Ifaces.iface[30].parent = []
Ifaces.iface.insert(31, None)
Ifaces.iface[31] = Dummy()
Ifaces.iface[31].attr = []
Ifaces.iface[31].attr.insert(0, None)
Ifaces.iface[31].attr[0] = 'equipment'
Ifaces.iface[31].attr.insert(1, None)
Ifaces.iface[31].attr[1] = 'consumables'
Ifaces.iface[31].attr.insert(2, None)
Ifaces.iface[31].attr[2] = 'weapons'
Ifaces.iface[31].attr.insert(3, None)
Ifaces.iface[31].attr[3] = 'belts'
Ifaces.iface[31].attr.insert(4, None)
Ifaces.iface[31].attr[4] = 'rockets'
Ifaces.iface[31].attr.insert(5, None)
Ifaces.iface[31].attr[5] = 'bombs'
Ifaces.iface[31].attr.insert(6, None)
Ifaces.iface[31].attr[6] = 'rocketsIDs'
Ifaces.iface[31].attr.insert(7, None)
Ifaces.iface[31].attr[7] = 'bombsIDs'
Ifaces.iface[31].attr.insert(8, None)
Ifaces.iface[31].attr[8] = 'modules'
Ifaces.iface[31].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[31].callbackSubscriable = false
Ifaces.iface[31].defaultCallback = ''
Ifaces.iface[31].ifacename = 'IDepot'
Ifaces.iface[31].parent = []
Ifaces.iface.insert(32, None)
Ifaces.iface[32] = Dummy()
Ifaces.iface[32].attr = []
Ifaces.iface[32].attr.insert(0, None)
Ifaces.iface[32].attr[0] = 'equipmentIDs'
Ifaces.iface[32].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[32].callbackSubscriable = false
Ifaces.iface[32].defaultCallback = ''
Ifaces.iface[32].ifacename = 'IAvailableEquipment'
Ifaces.iface[32].parent = []
Ifaces.iface.insert(33, None)
Ifaces.iface[33] = Dummy()
Ifaces.iface[33].attr = []
Ifaces.iface[33].attr.insert(0, None)
Ifaces.iface[33].attr[0] = 'mass'
Ifaces.iface[33].attr.insert(1, None)
Ifaces.iface[33].attr[1] = 'detachPrice'
Ifaces.iface[33].attr.insert(2, None)
Ifaces.iface[33].attr[2] = 'name'
Ifaces.iface[33].attr.insert(3, None)
Ifaces.iface[33].attr[3] = 'description'
Ifaces.iface[33].attr.insert(4, None)
Ifaces.iface[33].attr[4] = 'suitablePlaneIDs'
Ifaces.iface[33].attr.insert(5, None)
Ifaces.iface[33].attr[5] = 'nations'
Ifaces.iface[33].attr.insert(6, None)
Ifaces.iface[33].attr[6] = 'minLevel'
Ifaces.iface[33].attr.insert(7, None)
Ifaces.iface[33].attr[7] = 'maxLevel'
Ifaces.iface[33].attr.insert(8, None)
Ifaces.iface[33].attr[8] = 'buyAvailable'
Ifaces.iface[33].attr.insert(9, None)
Ifaces.iface[33].attr[9] = 'isNew'
Ifaces.iface[33].attr.insert(10, None)
Ifaces.iface[33].attr[10] = 'isDiscount'
Ifaces.iface[33].attr.insert(11, None)
Ifaces.iface[33].attr[11] = 'icoPath'
Ifaces.iface[33].attr.insert(12, None)
Ifaces.iface[33].attr[12] = 'icoPathSmall'
Ifaces.iface[33].attr.insert(13, None)
Ifaces.iface[33].attr[13] = 'uiIndex'
Ifaces.iface[33].attr.insert(14, None)
Ifaces.iface[33].attr[14] = 'planeType'
Ifaces.iface[33].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[33].callbackSubscriable = false
Ifaces.iface[33].defaultCallback = ''
Ifaces.iface[33].ifacename = 'IEquipment'
Ifaces.iface[33].parent = []
Ifaces.iface.insert(34, None)
Ifaces.iface[34] = Dummy()
Ifaces.iface[34].attr = []
Ifaces.iface[34].attr.insert(0, None)
Ifaces.iface[34].attr[0] = 'objID'
Ifaces.iface[34].attr.insert(1, None)
Ifaces.iface[34].attr[1] = 'count'
Ifaces.iface[34].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[34].callbackSubscriable = false
Ifaces.iface[34].defaultCallback = ''
Ifaces.iface[34].ifacename = 'IInstalledAmmoBelt'
Ifaces.iface[34].parent = []
Ifaces.iface.insert(35, None)
Ifaces.iface[35] = Dummy()
Ifaces.iface[35].attr = []
Ifaces.iface[35].attr.insert(0, None)
Ifaces.iface[35].attr[0] = 'name'
Ifaces.iface[35].attr.insert(1, None)
Ifaces.iface[35].attr[1] = 'description'
Ifaces.iface[35].attr.insert(2, None)
Ifaces.iface[35].attr[2] = 'fullDescription'
Ifaces.iface[35].attr.insert(3, None)
Ifaces.iface[35].attr[3] = 'effectContinuous'
Ifaces.iface[35].attr.insert(4, None)
Ifaces.iface[35].attr[4] = 'effectOnUse'
Ifaces.iface[35].attr.insert(5, None)
Ifaces.iface[35].attr[5] = 'suitablePlaneIDs'
Ifaces.iface[35].attr.insert(6, None)
Ifaces.iface[35].attr[6] = 'nations'
Ifaces.iface[35].attr.insert(7, None)
Ifaces.iface[35].attr[7] = 'minLevel'
Ifaces.iface[35].attr.insert(8, None)
Ifaces.iface[35].attr[8] = 'maxLevel'
Ifaces.iface[35].attr.insert(9, None)
Ifaces.iface[35].attr[9] = 'behaviour'
Ifaces.iface[35].attr.insert(10, None)
Ifaces.iface[35].attr[10] = 'planeTypes'
Ifaces.iface[35].attr.insert(11, None)
Ifaces.iface[35].attr[11] = 'buyAvailable'
Ifaces.iface[35].attr.insert(12, None)
Ifaces.iface[35].attr[12] = 'isNew'
Ifaces.iface[35].attr.insert(13, None)
Ifaces.iface[35].attr[13] = 'isDiscount'
Ifaces.iface[35].attr.insert(14, None)
Ifaces.iface[35].attr[14] = 'icoPath'
Ifaces.iface[35].attr.insert(15, None)
Ifaces.iface[35].attr[15] = 'icoPathSmall'
Ifaces.iface[35].attr.insert(16, None)
Ifaces.iface[35].attr[16] = 'uiIndex'
Ifaces.iface[35].attr.insert(17, None)
Ifaces.iface[35].attr[17] = 'coolDownTime'
Ifaces.iface[35].attr.insert(18, None)
Ifaces.iface[35].attr[18] = 'effectTime'
Ifaces.iface[35].attr.insert(19, None)
Ifaces.iface[35].attr[19] = 'chargesCount'
Ifaces.iface[35].attr.insert(20, None)
Ifaces.iface[35].attr[20] = 'planeType'
Ifaces.iface[35].attr.insert(21, None)
Ifaces.iface[35].attr[21] = 'group'
Ifaces.iface[35].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[35].callbackSubscriable = false
Ifaces.iface[35].defaultCallback = ''
Ifaces.iface[35].ifacename = 'IConsumable'
Ifaces.iface[35].parent = []
Ifaces.iface.insert(36, None)
Ifaces.iface[36] = Dummy()
Ifaces.iface[36].attr = []
Ifaces.iface[36].attr.insert(0, None)
Ifaces.iface[36].attr[0] = 'modsList'
Ifaces.iface[36].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[36].callbackSubscriable = false
Ifaces.iface[36].defaultCallback = ''
Ifaces.iface[36].ifacename = 'IModifiers'
Ifaces.iface[36].parent = []
Ifaces.iface.insert(37, None)
Ifaces.iface[37] = Dummy()
Ifaces.iface[37].attr = []
Ifaces.iface[37].attr.insert(0, None)
Ifaces.iface[37].attr[0] = 'consumableIDs'
Ifaces.iface[37].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[37].callbackSubscriable = false
Ifaces.iface[37].defaultCallback = ''
Ifaces.iface[37].ifacename = 'IAvailableConsumables'
Ifaces.iface[37].parent = []
Ifaces.iface.insert(38, None)
Ifaces.iface[38] = Dummy()
Ifaces.iface[38].attr = []
Ifaces.iface[38].attr.insert(0, None)
Ifaces.iface[38].attr[0] = 'exp'
Ifaces.iface[38].attr.insert(1, None)
Ifaces.iface[38].attr[1] = 'credits'
Ifaces.iface[38].attr.insert(2, None)
Ifaces.iface[38].attr[2] = 'gold'
Ifaces.iface[38].attr.insert(3, None)
Ifaces.iface[38].attr[3] = 'tickets'
Ifaces.iface[38].attr.insert(4, None)
Ifaces.iface[38].attr[4] = 'questChips'
Ifaces.iface[38].attr.insert(5, None)
Ifaces.iface[38].attr[5] = 'freeClicks'
Ifaces.iface[38].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[38].callbackSubscriable = false
Ifaces.iface[38].defaultCallback = ''
Ifaces.iface[38].ifacename = 'IAccountResources'
Ifaces.iface[38].parent = []
Ifaces.iface.insert(39, None)
Ifaces.iface[39] = Dummy()
Ifaces.iface[39].attr = []
Ifaces.iface[39].attr.insert(0, None)
Ifaces.iface[39].attr[0] = 'name'
Ifaces.iface[39].attr.insert(1, None)
Ifaces.iface[39].attr[1] = 'description'
Ifaces.iface[39].attr.insert(2, None)
Ifaces.iface[39].attr[2] = 'shortDescription'
Ifaces.iface[39].attr.insert(3, None)
Ifaces.iface[39].attr[3] = 'caliber'
Ifaces.iface[39].attr.insert(4, None)
Ifaces.iface[39].attr[4] = 'maxDistance'
Ifaces.iface[39].attr.insert(5, None)
Ifaces.iface[39].attr[5] = 'iconPath'
Ifaces.iface[39].attr.insert(6, None)
Ifaces.iface[39].attr[6] = 'compatibleBeltIDs'
Ifaces.iface[39].attr.insert(7, None)
Ifaces.iface[39].attr[7] = 'suitablePlaneIDs'
Ifaces.iface[39].attr.insert(8, None)
Ifaces.iface[39].attr[8] = 'buyAvailable'
Ifaces.iface[39].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[39].callbackSubscriable = false
Ifaces.iface[39].defaultCallback = ''
Ifaces.iface[39].ifacename = 'IGunDescription'
Ifaces.iface[39].parent = []
Ifaces.iface.insert(40, None)
Ifaces.iface[40] = Dummy()
Ifaces.iface[40].attr = []
Ifaces.iface[40].attr.insert(0, None)
Ifaces.iface[40].attr[0] = 'slots'
Ifaces.iface[40].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[40].callbackSubscriable = false
Ifaces.iface[40].defaultCallback = ''
Ifaces.iface[40].ifacename = 'IInstalledGunSlots'
Ifaces.iface[40].parent = []
Ifaces.iface.insert(41, None)
Ifaces.iface[41] = Dummy()
Ifaces.iface[41].attr = []
Ifaces.iface[41].attr.insert(0, None)
Ifaces.iface[41].attr[0] = 'slots'
Ifaces.iface[41].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[41].callbackSubscriable = false
Ifaces.iface[41].defaultCallback = ''
Ifaces.iface[41].ifacename = 'IInstalledBombSlots'
Ifaces.iface[41].parent = []
Ifaces.iface.insert(42, None)
Ifaces.iface[42] = Dummy()
Ifaces.iface[42].attr = []
Ifaces.iface[42].attr.insert(0, None)
Ifaces.iface[42].attr[0] = 'slots'
Ifaces.iface[42].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[42].callbackSubscriable = false
Ifaces.iface[42].defaultCallback = ''
Ifaces.iface[42].ifacename = 'IInstalledRocketSlots'
Ifaces.iface[42].parent = []
Ifaces.iface.insert(43, None)
Ifaces.iface[43] = Dummy()
Ifaces.iface[43].attr = []
Ifaces.iface[43].attr.insert(0, None)
Ifaces.iface[43].attr[0] = 'configID'
Ifaces.iface[43].attr.insert(1, None)
Ifaces.iface[43].attr[1] = 'objID'
Ifaces.iface[43].attr.insert(2, None)
Ifaces.iface[43].attr[2] = 'count'
Ifaces.iface[43].attr.insert(3, None)
Ifaces.iface[43].attr[3] = 'weaponGroup'
Ifaces.iface[43].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[43].callbackSubscriable = false
Ifaces.iface[43].defaultCallback = ''
Ifaces.iface[43].ifacename = 'IInstalledGun'
Ifaces.iface[43].parent = []
Ifaces.iface.insert(44, None)
Ifaces.iface[44] = Dummy()
Ifaces.iface[44].attr = []
Ifaces.iface[44].attr.insert(0, None)
Ifaces.iface[44].attr[0] = 'equipmentIDs'
Ifaces.iface[44].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[44].callbackSubscriable = false
Ifaces.iface[44].defaultCallback = ''
Ifaces.iface[44].ifacename = 'IInstalledEquipment'
Ifaces.iface[44].parent = []
Ifaces.iface.insert(45, None)
Ifaces.iface[45] = Dummy()
Ifaces.iface[45].attr = []
Ifaces.iface[45].attr.insert(0, None)
Ifaces.iface[45].attr[0] = 'objID'
Ifaces.iface[45].attr.insert(1, None)
Ifaces.iface[45].attr[1] = 'count'
Ifaces.iface[45].attr.insert(2, None)
Ifaces.iface[45].attr[2] = 'maxCount'
Ifaces.iface[45].attr.insert(3, None)
Ifaces.iface[45].attr[3] = 'storedCount'
Ifaces.iface[45].attr.insert(4, None)
Ifaces.iface[45].attr[4] = 'updates'
Ifaces.iface[45].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[45].callbackSubscriable = false
Ifaces.iface[45].defaultCallback = ''
Ifaces.iface[45].ifacename = 'IInstalledBomb'
Ifaces.iface[45].parent = []
Ifaces.iface.insert(46, None)
Ifaces.iface[46] = Dummy()
Ifaces.iface[46].attr = []
Ifaces.iface[46].attr.insert(0, None)
Ifaces.iface[46].attr[0] = 'objID'
Ifaces.iface[46].attr.insert(1, None)
Ifaces.iface[46].attr[1] = 'count'
Ifaces.iface[46].attr.insert(2, None)
Ifaces.iface[46].attr[2] = 'maxCount'
Ifaces.iface[46].attr.insert(3, None)
Ifaces.iface[46].attr[3] = 'storedCount'
Ifaces.iface[46].attr.insert(4, None)
Ifaces.iface[46].attr[4] = 'updates'
Ifaces.iface[46].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[46].callbackSubscriable = false
Ifaces.iface[46].defaultCallback = ''
Ifaces.iface[46].ifacename = 'IInstalledRocket'
Ifaces.iface[46].parent = []
Ifaces.iface.insert(47, None)
Ifaces.iface[47] = Dummy()
Ifaces.iface[47].attr = []
Ifaces.iface[47].attr.insert(0, None)
Ifaces.iface[47].attr[0] = 'name'
Ifaces.iface[47].attr.insert(1, None)
Ifaces.iface[47].attr[1] = 'iconPath'
Ifaces.iface[47].attr.insert(2, None)
Ifaces.iface[47].attr[2] = 'suitablePlaneIDs'
Ifaces.iface[47].attr.insert(3, None)
Ifaces.iface[47].attr[3] = 'description'
Ifaces.iface[47].attr.insert(4, None)
Ifaces.iface[47].attr[4] = 'shortDescription'
Ifaces.iface[47].attr.insert(5, None)
Ifaces.iface[47].attr[5] = 'caliber'
Ifaces.iface[47].attr.insert(6, None)
Ifaces.iface[47].attr[6] = 'upgradeID'
Ifaces.iface[47].attr.insert(7, None)
Ifaces.iface[47].attr[7] = 'iconPathSmall'
Ifaces.iface[47].attr.insert(8, None)
Ifaces.iface[47].attr[8] = 'buyAvailable'
Ifaces.iface[47].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[47].callbackSubscriable = false
Ifaces.iface[47].defaultCallback = ''
Ifaces.iface[47].ifacename = 'IBombDescription'
Ifaces.iface[47].parent = []
Ifaces.iface.insert(48, None)
Ifaces.iface[48] = Dummy()
Ifaces.iface[48].attr = []
Ifaces.iface[48].attr.insert(0, None)
Ifaces.iface[48].attr[0] = 'name'
Ifaces.iface[48].attr.insert(1, None)
Ifaces.iface[48].attr[1] = 'iconPath'
Ifaces.iface[48].attr.insert(2, None)
Ifaces.iface[48].attr[2] = 'suitablePlaneIDs'
Ifaces.iface[48].attr.insert(3, None)
Ifaces.iface[48].attr[3] = 'description'
Ifaces.iface[48].attr.insert(4, None)
Ifaces.iface[48].attr[4] = 'shortDescription'
Ifaces.iface[48].attr.insert(5, None)
Ifaces.iface[48].attr[5] = 'caliber'
Ifaces.iface[48].attr.insert(6, None)
Ifaces.iface[48].attr[6] = 'upgradeID'
Ifaces.iface[48].attr.insert(7, None)
Ifaces.iface[48].attr[7] = 'iconPathSmall'
Ifaces.iface[48].attr.insert(8, None)
Ifaces.iface[48].attr[8] = 'buyAvailable'
Ifaces.iface[48].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[48].callbackSubscriable = false
Ifaces.iface[48].defaultCallback = ''
Ifaces.iface[48].ifacename = 'IRocketDescription'
Ifaces.iface[48].parent = []
Ifaces.iface.insert(49, None)
Ifaces.iface[49] = Dummy()
Ifaces.iface[49].attr = []
Ifaces.iface[49].attr.insert(0, None)
Ifaces.iface[49].attr[0] = 'minDamage'
Ifaces.iface[49].attr.insert(1, None)
Ifaces.iface[49].attr[1] = 'maxDamage'
Ifaces.iface[49].attr.insert(2, None)
Ifaces.iface[49].attr[2] = 'isDefault'
Ifaces.iface[49].attr.insert(3, None)
Ifaces.iface[49].attr[3] = 'specsList'
Ifaces.iface[49].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[49].callbackSubscriable = false
Ifaces.iface[49].defaultCallback = ''
Ifaces.iface[49].ifacename = 'IAmmoBeltCharacteristics'
Ifaces.iface[49].parent = []
Ifaces.iface.insert(50, None)
Ifaces.iface[50] = Dummy()
Ifaces.iface[50].attr = []
Ifaces.iface[50].attr.insert(0, None)
Ifaces.iface[50].attr[0] = 'autoRepair'
Ifaces.iface[50].attr.insert(1, None)
Ifaces.iface[50].attr[1] = 'autoRefill'
Ifaces.iface[50].attr.insert(2, None)
Ifaces.iface[50].attr[2] = 'consumablesAutoRefill'
Ifaces.iface[50].attr.insert(3, None)
Ifaces.iface[50].attr[3] = 'beltsAutoRefill'
Ifaces.iface[50].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[50].callbackSubscriable = false
Ifaces.iface[50].defaultCallback = ''
Ifaces.iface[50].ifacename = 'IServiceStates'
Ifaces.iface[50].parent = []
Ifaces.iface.insert(51, None)
Ifaces.iface[51] = Dummy()
Ifaces.iface[51].attr = []
Ifaces.iface[51].attr.insert(0, None)
Ifaces.iface[51].attr[0] = 'curHealth'
Ifaces.iface[51].attr.insert(1, None)
Ifaces.iface[51].attr[1] = 'fullHealth'
Ifaces.iface[51].attr.insert(2, None)
Ifaces.iface[51].attr[2] = 'price'
Ifaces.iface[51].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[51].callbackSubscriable = false
Ifaces.iface[51].defaultCallback = ''
Ifaces.iface[51].ifacename = 'IRepair'
Ifaces.iface[51].parent = []
Ifaces.iface.insert(52, None)
Ifaces.iface[52] = Dummy()
Ifaces.iface[52].attr = []
Ifaces.iface[52].attr.insert(0, None)
Ifaces.iface[52].attr[0] = 'consumables'
Ifaces.iface[52].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[52].callbackSubscriable = false
Ifaces.iface[52].defaultCallback = ''
Ifaces.iface[52].ifacename = 'IInstalledConsumables'
Ifaces.iface[52].parent = []
Ifaces.iface.insert(53, None)
Ifaces.iface[53] = Dummy()
Ifaces.iface[53].attr = []
Ifaces.iface[53].attr.insert(0, None)
Ifaces.iface[53].attr[0] = 'quantity'
Ifaces.iface[53].attr.insert(1, None)
Ifaces.iface[53].attr[1] = 'crewMembers'
Ifaces.iface[53].attr.insert(2, None)
Ifaces.iface[53].attr[2] = 'acceleratedCrewPumping'
Ifaces.iface[53].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[53].callbackSubscriable = false
Ifaces.iface[53].defaultCallback = ''
Ifaces.iface[53].ifacename = 'IPlaneCrew'
Ifaces.iface[53].parent = []
Ifaces.iface.insert(54, None)
Ifaces.iface[54] = Dummy()
Ifaces.iface[54].attr = []
Ifaces.iface[54].attr.insert(0, None)
Ifaces.iface[54].attr[0] = 'firstName'
Ifaces.iface[54].attr.insert(1, None)
Ifaces.iface[54].attr[1] = 'lastName'
Ifaces.iface[54].attr.insert(2, None)
Ifaces.iface[54].attr[2] = 'specialization'
Ifaces.iface[54].attr.insert(3, None)
Ifaces.iface[54].attr[3] = 'specializationResearchPercent'
Ifaces.iface[54].attr.insert(4, None)
Ifaces.iface[54].attr[4] = 'bodyType'
Ifaces.iface[54].attr.insert(5, None)
Ifaces.iface[54].attr[5] = 'ranks'
Ifaces.iface[54].attr.insert(6, None)
Ifaces.iface[54].attr[6] = 'skills'
Ifaces.iface[54].attr.insert(7, None)
Ifaces.iface[54].attr[7] = 'icoIndex'
Ifaces.iface[54].attr.insert(8, None)
Ifaces.iface[54].attr[8] = 'crewIcoPath'
Ifaces.iface[54].attr.insert(9, None)
Ifaces.iface[54].attr[9] = 'miniIcoPath'
Ifaces.iface[54].attr.insert(10, None)
Ifaces.iface[54].attr[10] = 'infoIcoPath'
Ifaces.iface[54].attr.insert(11, None)
Ifaces.iface[54].attr[11] = 'planeSpecializedOn'
Ifaces.iface[54].attr.insert(12, None)
Ifaces.iface[54].attr[12] = 'nationIcoPath'
Ifaces.iface[54].attr.insert(13, None)
Ifaces.iface[54].attr[13] = 'mainExp'
Ifaces.iface[54].attr.insert(14, None)
Ifaces.iface[54].attr[14] = 'experience'
Ifaces.iface[54].attr.insert(15, None)
Ifaces.iface[54].attr[15] = 'rankIcoPath'
Ifaces.iface[54].attr.insert(16, None)
Ifaces.iface[54].attr[16] = 'rankSmallIcoPath'
Ifaces.iface[54].attr.insert(17, None)
Ifaces.iface[54].attr[17] = 'nextRankIcoPath'
Ifaces.iface[54].attr.insert(18, None)
Ifaces.iface[54].attr[18] = 'nextRank'
Ifaces.iface[54].attr.insert(19, None)
Ifaces.iface[54].attr[19] = 'currentPlane'
Ifaces.iface[54].attr.insert(20, None)
Ifaces.iface[54].attr[20] = 'freeSP'
Ifaces.iface[54].attr.insert(21, None)
Ifaces.iface[54].attr[21] = 'expLeftToMain'
Ifaces.iface[54].attr.insert(22, None)
Ifaces.iface[54].attr[22] = 'expLeftToSP'
Ifaces.iface[54].attr.insert(23, None)
Ifaces.iface[54].attr[23] = 'expForSP'
Ifaces.iface[54].attr.insert(24, None)
Ifaces.iface[54].attr[24] = 'SP'
Ifaces.iface[54].attr.insert(25, None)
Ifaces.iface[54].attr[25] = 'maxSP'
Ifaces.iface[54].attr.insert(26, None)
Ifaces.iface[54].attr[26] = 'skillPenaltyPrc'
Ifaces.iface[54].attr.insert(27, None)
Ifaces.iface[54].attr[27] = 'skillValue'
Ifaces.iface[54].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[54].callbackSubscriable = false
Ifaces.iface[54].defaultCallback = ''
Ifaces.iface[54].ifacename = 'ICrewMember'
Ifaces.iface[54].parent = []
Ifaces.iface.insert(55, None)
Ifaces.iface[55] = Dummy()
Ifaces.iface[55].attr = []
Ifaces.iface[55].attr.insert(0, None)
Ifaces.iface[55].attr[0] = 'icoPath'
Ifaces.iface[55].attr.insert(1, None)
Ifaces.iface[55].attr[1] = 'smallIcoPath'
Ifaces.iface[55].attr.insert(2, None)
Ifaces.iface[55].attr[2] = 'name'
Ifaces.iface[55].attr.insert(3, None)
Ifaces.iface[55].attr[3] = 'description'
Ifaces.iface[55].attr.insert(4, None)
Ifaces.iface[55].attr[4] = 'fullDescription'
Ifaces.iface[55].attr.insert(5, None)
Ifaces.iface[55].attr[5] = 'middleDescription'
Ifaces.iface[55].attr.insert(6, None)
Ifaces.iface[55].attr[6] = 'infotipsIcoPath'
Ifaces.iface[55].attr.insert(7, None)
Ifaces.iface[55].attr[7] = 'uiIndex'
Ifaces.iface[55].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[55].callbackSubscriable = false
Ifaces.iface[55].defaultCallback = ''
Ifaces.iface[55].ifacename = 'ISkillDescription'
Ifaces.iface[55].parent = []
Ifaces.iface.insert(56, None)
Ifaces.iface[56] = Dummy()
Ifaces.iface[56].attr = []
Ifaces.iface[56].attr.insert(0, None)
Ifaces.iface[56].attr[0] = 'skills'
Ifaces.iface[56].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[56].callbackSubscriable = false
Ifaces.iface[56].defaultCallback = ''
Ifaces.iface[56].ifacename = 'IAvailableSkills'
Ifaces.iface[56].parent = []
Ifaces.iface.insert(57, None)
Ifaces.iface[57] = Dummy()
Ifaces.iface[57].attr = []
Ifaces.iface[57].attr.insert(0, None)
Ifaces.iface[57].attr[0] = 'items'
Ifaces.iface[57].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[57].callbackSubscriable = false
Ifaces.iface[57].defaultCallback = ''
Ifaces.iface[57].ifacename = 'ICrewSpecializationResearchCost'
Ifaces.iface[57].parent = []
Ifaces.iface.insert(58, None)
Ifaces.iface[58] = Dummy()
Ifaces.iface[58].attr = []
Ifaces.iface[58].attr.insert(0, None)
Ifaces.iface[58].attr[0] = 'achievements'
Ifaces.iface[58].attr.insert(1, None)
Ifaces.iface[58].attr[1] = 'medals'
Ifaces.iface[58].attr.insert(2, None)
Ifaces.iface[58].attr[2] = 'ribbons'
Ifaces.iface[58].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[58].callbackSubscriable = false
Ifaces.iface[58].defaultCallback = ''
Ifaces.iface[58].ifacename = 'IAwards'
Ifaces.iface[58].parent = []
Ifaces.iface.insert(59, None)
Ifaces.iface[59] = Dummy()
Ifaces.iface[59].attr = []
Ifaces.iface[59].attr.insert(0, None)
Ifaces.iface[59].attr[0] = 'name'
Ifaces.iface[59].attr.insert(1, None)
Ifaces.iface[59].attr[1] = 'description'
Ifaces.iface[59].attr.insert(2, None)
Ifaces.iface[59].attr[2] = 'history'
Ifaces.iface[59].attr.insert(3, None)
Ifaces.iface[59].attr[3] = 'icoPath'
Ifaces.iface[59].attr.insert(4, None)
Ifaces.iface[59].attr[4] = 'icoPath_Outline'
Ifaces.iface[59].attr.insert(5, None)
Ifaces.iface[59].attr[5] = 'icoBigPath'
Ifaces.iface[59].attr.insert(6, None)
Ifaces.iface[59].attr[6] = 'group'
Ifaces.iface[59].attr.insert(7, None)
Ifaces.iface[59].attr[7] = 'outBlock'
Ifaces.iface[59].attr.insert(8, None)
Ifaces.iface[59].attr[8] = 'index'
Ifaces.iface[59].attr.insert(9, None)
Ifaces.iface[59].attr[9] = 'page'
Ifaces.iface[59].attr.insert(10, None)
Ifaces.iface[59].attr[10] = 'enable'
Ifaces.iface[59].attr.insert(11, None)
Ifaces.iface[59].attr[11] = 'gameMode'
Ifaces.iface[59].attr.insert(12, None)
Ifaces.iface[59].attr[12] = 'inSingleBattle'
Ifaces.iface[59].attr.insert(13, None)
Ifaces.iface[59].attr[13] = 'multiple'
Ifaces.iface[59].attr.insert(14, None)
Ifaces.iface[59].attr[14] = 'perPlane'
Ifaces.iface[59].attr.insert(15, None)
Ifaces.iface[59].attr[15] = 'ribbon'
Ifaces.iface[59].attr.insert(16, None)
Ifaces.iface[59].attr[16] = 'saveStats'
Ifaces.iface[59].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[59].callbackSubscriable = false
Ifaces.iface[59].defaultCallback = ''
Ifaces.iface[59].ifacename = 'IAwardDescription'
Ifaces.iface[59].parent = []
Ifaces.iface.insert(60, None)
Ifaces.iface[60] = Dummy()
Ifaces.iface[60].attr = []
Ifaces.iface[60].attr.insert(0, None)
Ifaces.iface[60].attr[0] = 'hasBonus'
Ifaces.iface[60].attr.insert(1, None)
Ifaces.iface[60].attr[1] = 'tickets'
Ifaces.iface[60].attr.insert(2, None)
Ifaces.iface[60].attr[2] = 'count'
Ifaces.iface[60].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[60].callbackSubscriable = false
Ifaces.iface[60].defaultCallback = ''
Ifaces.iface[60].ifacename = 'IAwardDailyBonus'
Ifaces.iface[60].parent = []
Ifaces.iface.insert(61, None)
Ifaces.iface[61] = Dummy()
Ifaces.iface[61].attr = []
Ifaces.iface[61].attr.insert(0, None)
Ifaces.iface[61].attr[0] = 'exp'
Ifaces.iface[61].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[61].callbackSubscriable = false
Ifaces.iface[61].defaultCallback = ''
Ifaces.iface[61].ifacename = 'IExperience'
Ifaces.iface[61].parent = []
Ifaces.iface.insert(62, None)
Ifaces.iface[62] = Dummy()
Ifaces.iface[62].attr = []
Ifaces.iface[62].attr.insert(0, None)
Ifaces.iface[62].attr[0] = 'items'
Ifaces.iface[62].attr.insert(1, None)
Ifaces.iface[62].attr[1] = 'dropCosts'
Ifaces.iface[62].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[62].callbackSubscriable = false
Ifaces.iface[62].defaultCallback = ''
Ifaces.iface[62].ifacename = 'ICrewSkillsDropCost'
Ifaces.iface[62].parent = []
Ifaces.iface.insert(63, None)
Ifaces.iface[63] = Dummy()
Ifaces.iface[63].attr = []
Ifaces.iface[63].attr.insert(0, None)
Ifaces.iface[63].attr[0] = 'items'
Ifaces.iface[63].attr.insert(1, None)
Ifaces.iface[63].attr[1] = 'changeRate'
Ifaces.iface[63].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[63].callbackSubscriable = false
Ifaces.iface[63].defaultCallback = ''
Ifaces.iface[63].ifacename = 'ICrewSPFromExp'
Ifaces.iface[63].parent = []
Ifaces.iface.insert(64, None)
Ifaces.iface[64] = Dummy()
Ifaces.iface[64].attr = []
Ifaces.iface[64].attr.insert(0, None)
Ifaces.iface[64].attr[0] = 'ranks'
Ifaces.iface[64].cacheType = CACHE_TYPE.NONE
Ifaces.iface[64].callbackSubscriable = false
Ifaces.iface[64].defaultCallback = ''
Ifaces.iface[64].ifacename = 'ICrewRanks'
Ifaces.iface[64].parent = []
Ifaces.iface.insert(65, None)
Ifaces.iface[65] = Dummy()
Ifaces.iface[65].attr = []
Ifaces.iface[65].attr.insert(0, None)
Ifaces.iface[65].attr[0] = 'dropResults'
Ifaces.iface[65].cacheType = CACHE_TYPE.NONE
Ifaces.iface[65].callbackSubscriable = false
Ifaces.iface[65].defaultCallback = ''
Ifaces.iface[65].ifacename = 'ICrewMemberDroppedSkills'
Ifaces.iface[65].parent = []
Ifaces.iface.insert(66, None)
Ifaces.iface[66] = Dummy()
Ifaces.iface[66].attr = []
Ifaces.iface[66].attr.insert(0, None)
Ifaces.iface[66].attr[0] = 'isResearchAvailable'
Ifaces.iface[66].attr.insert(1, None)
Ifaces.iface[66].attr[1] = 'buyAvailable'
Ifaces.iface[66].attr.insert(2, None)
Ifaces.iface[66].attr[2] = 'sellAvailable'
Ifaces.iface[66].attr.insert(3, None)
Ifaces.iface[66].attr[3] = 'forceViewInTree'
Ifaces.iface[66].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[66].callbackSubscriable = false
Ifaces.iface[66].defaultCallback = ''
Ifaces.iface[66].ifacename = 'IPlaneDynamicDataPack'
Ifaces.iface[66].parent = []
Ifaces.iface[66].parent.insert(0, None)
Ifaces.iface[66].parent[0] = 'IStatus'
Ifaces.iface[66].parent.insert(1, None)
Ifaces.iface[66].parent[1] = 'IClass'
Ifaces.iface[66].parent.insert(2, None)
Ifaces.iface[66].parent[2] = 'IExperience'
Ifaces.iface.insert(67, None)
Ifaces.iface[67] = Dummy()
Ifaces.iface[67].attr = []
Ifaces.iface[67].attr.insert(0, None)
Ifaces.iface[67].attr[0] = 'ids'
Ifaces.iface[67].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[67].callbackSubscriable = false
Ifaces.iface[67].defaultCallback = ''
Ifaces.iface[67].ifacename = 'IListAmmoBelts'
Ifaces.iface[67].parent = []
Ifaces.iface.insert(68, None)
Ifaces.iface[68] = Dummy()
Ifaces.iface[68].attr = []
Ifaces.iface[68].attr.insert(0, None)
Ifaces.iface[68].attr[0] = 'ids'
Ifaces.iface[68].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[68].callbackSubscriable = false
Ifaces.iface[68].defaultCallback = ''
Ifaces.iface[68].ifacename = 'IListBombs'
Ifaces.iface[68].parent = []
Ifaces.iface.insert(69, None)
Ifaces.iface[69] = Dummy()
Ifaces.iface[69].attr = []
Ifaces.iface[69].attr.insert(0, None)
Ifaces.iface[69].attr[0] = 'ids'
Ifaces.iface[69].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[69].callbackSubscriable = false
Ifaces.iface[69].defaultCallback = ''
Ifaces.iface[69].ifacename = 'IListRockets'
Ifaces.iface[69].parent = []
Ifaces.iface.insert(70, None)
Ifaces.iface[70] = Dummy()
Ifaces.iface[70].attr = []
Ifaces.iface[70].attr.insert(0, None)
Ifaces.iface[70].attr[0] = 'ids'
Ifaces.iface[70].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[70].callbackSubscriable = false
Ifaces.iface[70].defaultCallback = ''
Ifaces.iface[70].ifacename = 'IListConsumables'
Ifaces.iface[70].parent = []
Ifaces.iface.insert(71, None)
Ifaces.iface[71] = Dummy()
Ifaces.iface[71].attr = []
Ifaces.iface[71].attr.insert(0, None)
Ifaces.iface[71].attr[0] = 'ids'
Ifaces.iface[71].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[71].callbackSubscriable = false
Ifaces.iface[71].defaultCallback = ''
Ifaces.iface[71].ifacename = 'IListEquipment'
Ifaces.iface[71].parent = []
Ifaces.iface.insert(72, None)
Ifaces.iface[72] = Dummy()
Ifaces.iface[72].attr = []
Ifaces.iface[72].attr.insert(0, None)
Ifaces.iface[72].attr[0] = 'ids'
Ifaces.iface[72].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[72].callbackSubscriable = false
Ifaces.iface[72].defaultCallback = ''
Ifaces.iface[72].ifacename = 'IListUpgrades'
Ifaces.iface[72].parent = []
Ifaces.iface.insert(73, None)
Ifaces.iface[73] = Dummy()
Ifaces.iface[73].attr = []
Ifaces.iface[73].attr.insert(0, None)
Ifaces.iface[73].attr[0] = 'ids'
Ifaces.iface[73].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[73].callbackSubscriable = false
Ifaces.iface[73].defaultCallback = ''
Ifaces.iface[73].ifacename = 'IListBoughtUpgrades'
Ifaces.iface[73].parent = []
Ifaces.iface.insert(74, None)
Ifaces.iface[74] = Dummy()
Ifaces.iface[74].attr = []
Ifaces.iface[74].attr.insert(0, None)
Ifaces.iface[74].attr[0] = 'value'
Ifaces.iface[74].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[74].callbackSubscriable = false
Ifaces.iface[74].defaultCallback = ''
Ifaces.iface[74].ifacename = 'IInstalledCount'
Ifaces.iface[74].parent = []
Ifaces.iface.insert(75, None)
Ifaces.iface[75] = Dummy()
Ifaces.iface[75].attr = []
Ifaces.iface[75].attr.insert(0, None)
Ifaces.iface[75].attr[0] = 'value'
Ifaces.iface[75].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[75].callbackSubscriable = false
Ifaces.iface[75].defaultCallback = ''
Ifaces.iface[75].ifacename = 'IDepotCount'
Ifaces.iface[75].parent = []
Ifaces.iface.insert(76, None)
Ifaces.iface[76] = Dummy()
Ifaces.iface[76].attr = []
Ifaces.iface[76].attr.insert(0, None)
Ifaces.iface[76].attr[0] = 'slots'
Ifaces.iface[76].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[76].callbackSubscriable = false
Ifaces.iface[76].defaultCallback = ''
Ifaces.iface[76].ifacename = 'ISlotsCount'
Ifaces.iface[76].parent = []
Ifaces.iface.insert(77, None)
Ifaces.iface[77] = Dummy()
Ifaces.iface[77].attr = []
Ifaces.iface[77].attr.insert(0, None)
Ifaces.iface[77].attr[0] = 'pilots'
Ifaces.iface[77].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[77].callbackSubscriable = false
Ifaces.iface[77].defaultCallback = ''
Ifaces.iface[77].ifacename = 'IBarrack'
Ifaces.iface[77].parent = []
Ifaces.iface.insert(78, None)
Ifaces.iface[78] = Dummy()
Ifaces.iface[78].attr = []
Ifaces.iface[78].attr.insert(0, None)
Ifaces.iface[78].attr[0] = 'total'
Ifaces.iface[78].attr.insert(1, None)
Ifaces.iface[78].attr[1] = 'free'
Ifaces.iface[78].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[78].callbackSubscriable = false
Ifaces.iface[78].defaultCallback = ''
Ifaces.iface[78].ifacename = 'IBarrackSlots'
Ifaces.iface[78].parent = []
Ifaces.iface.insert(79, None)
Ifaces.iface[79] = Dummy()
Ifaces.iface[79].attr = []
Ifaces.iface[79].attr.insert(0, None)
Ifaces.iface[79].attr[0] = 'extend'
Ifaces.iface[79].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[79].callbackSubscriable = false
Ifaces.iface[79].defaultCallback = ''
Ifaces.iface[79].ifacename = 'IBarrackPrice'
Ifaces.iface[79].parent = []
Ifaces.iface.insert(80, None)
Ifaces.iface[80] = Dummy()
Ifaces.iface[80].attr = []
Ifaces.iface[80].attr.insert(0, None)
Ifaces.iface[80].attr[0] = 'penaltyPrc'
Ifaces.iface[80].attr.insert(1, None)
Ifaces.iface[80].attr[1] = 'descriptions'
Ifaces.iface[80].attr.insert(2, None)
Ifaces.iface[80].attr[2] = 'skills'
Ifaces.iface[80].attr.insert(3, None)
Ifaces.iface[80].attr[3] = 'mainSpecLevel'
Ifaces.iface[80].attr.insert(4, None)
Ifaces.iface[80].attr[4] = 'mainSkillLock'
Ifaces.iface[80].attr.insert(5, None)
Ifaces.iface[80].attr[5] = 'SPLock'
Ifaces.iface[80].cacheType = CACHE_TYPE.NONE
Ifaces.iface[80].callbackSubscriable = false
Ifaces.iface[80].defaultCallback = ''
Ifaces.iface[80].ifacename = 'ISkillPenalty'
Ifaces.iface[80].parent = []
Ifaces.iface.insert(81, None)
Ifaces.iface[81] = Dummy()
Ifaces.iface[81].attr = []
Ifaces.iface[81].attr.insert(0, None)
Ifaces.iface[81].attr[0] = 'prices'
Ifaces.iface[81].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[81].callbackSubscriable = false
Ifaces.iface[81].defaultCallback = ''
Ifaces.iface[81].ifacename = 'ICrewSpecializationRetrainCost'
Ifaces.iface[81].parent = []
Ifaces.iface.insert(82, None)
Ifaces.iface[82] = Dummy()
Ifaces.iface[82].attr = []
Ifaces.iface[82].attr.insert(0, None)
Ifaces.iface[82].attr[0] = 'percents'
Ifaces.iface[82].cacheType = CACHE_TYPE.NONE
Ifaces.iface[82].callbackSubscriable = false
Ifaces.iface[82].defaultCallback = ''
Ifaces.iface[82].ifacename = 'ICrewSpecializationRetrainPrc'
Ifaces.iface[82].parent = []
Ifaces.iface.insert(83, None)
Ifaces.iface[83] = Dummy()
Ifaces.iface[83].attr = []
Ifaces.iface[83].attr.insert(0, None)
Ifaces.iface[83].attr[0] = 'AccountDBID'
Ifaces.iface[83].attr.insert(1, None)
Ifaces.iface[83].attr[1] = 'stats'
Ifaces.iface[83].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[83].callbackSubscriable = false
Ifaces.iface[83].defaultCallback = ''
Ifaces.iface[83].ifacename = 'IPlaneStats'
Ifaces.iface[83].parent = []
Ifaces.iface.insert(84, None)
Ifaces.iface[84] = Dummy()
Ifaces.iface[84].attr = []
Ifaces.iface[84].attr.insert(0, None)
Ifaces.iface[84].attr[0] = 'AccountDBID'
Ifaces.iface[84].attr.insert(1, None)
Ifaces.iface[84].attr[1] = 'stats'
Ifaces.iface[84].attr.insert(2, None)
Ifaces.iface[84].attr[2] = 'lastGameTime'
Ifaces.iface[84].attr.insert(3, None)
Ifaces.iface[84].attr[3] = 'gamesPlayed'
Ifaces.iface[84].attr.insert(4, None)
Ifaces.iface[84].attr[4] = 'createdAt'
Ifaces.iface[84].attr.insert(5, None)
Ifaces.iface[84].attr[5] = 'name'
Ifaces.iface[84].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[84].callbackSubscriable = false
Ifaces.iface[84].defaultCallback = ''
Ifaces.iface[84].ifacename = 'ISummaryStats'
Ifaces.iface[84].parent = []
Ifaces.iface.insert(85, None)
Ifaces.iface[85] = Dummy()
Ifaces.iface[85].attr = []
Ifaces.iface[85].attr.insert(0, None)
Ifaces.iface[85].attr[0] = 'planeName'
Ifaces.iface[85].attr.insert(1, None)
Ifaces.iface[85].attr[1] = 'level'
Ifaces.iface[85].attr.insert(2, None)
Ifaces.iface[85].attr[2] = 'icoPath'
Ifaces.iface[85].attr.insert(3, None)
Ifaces.iface[85].attr[3] = 'flagPath'
Ifaces.iface[85].attr.insert(4, None)
Ifaces.iface[85].attr[4] = 'nationID'
Ifaces.iface[85].attr.insert(5, None)
Ifaces.iface[85].attr[5] = 'planeID'
Ifaces.iface[85].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[85].callbackSubscriable = false
Ifaces.iface[85].defaultCallback = ''
Ifaces.iface[85].ifacename = 'IShortPlaneDescription'
Ifaces.iface[85].parent = []
Ifaces.iface.insert(86, None)
Ifaces.iface[86] = Dummy()
Ifaces.iface[86].attr = []
Ifaces.iface[86].attr.insert(0, None)
Ifaces.iface[86].attr[0] = 'AccountDBID'
Ifaces.iface[86].attr.insert(1, None)
Ifaces.iface[86].attr[1] = 'played'
Ifaces.iface[86].attr.insert(2, None)
Ifaces.iface[86].attr[2] = 'winsPercent'
Ifaces.iface[86].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[86].callbackSubscriable = false
Ifaces.iface[86].defaultCallback = ''
Ifaces.iface[86].ifacename = 'IShortPlaneStats'
Ifaces.iface[86].parent = []
Ifaces.iface[86].parent.insert(0, None)
Ifaces.iface[86].parent[0] = 'IShortPlaneDescription'
Ifaces.iface.insert(87, None)
Ifaces.iface[87] = Dummy()
Ifaces.iface[87].attr = []
Ifaces.iface[87].attr.insert(0, None)
Ifaces.iface[87].attr[0] = 'AccountDBID'
Ifaces.iface[87].attr.insert(1, None)
Ifaces.iface[87].attr[1] = 'planes'
Ifaces.iface[87].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[87].callbackSubscriable = false
Ifaces.iface[87].defaultCallback = ''
Ifaces.iface[87].ifacename = 'IStatsPlanesList'
Ifaces.iface[87].parent = []
Ifaces.iface.insert(88, None)
Ifaces.iface[88] = Dummy()
Ifaces.iface[88].attr = []
Ifaces.iface[88].attr.insert(0, None)
Ifaces.iface[88].attr[0] = 'lang'
Ifaces.iface[88].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[88].callbackSubscriable = false
Ifaces.iface[88].defaultCallback = ''
Ifaces.iface[88].ifacename = 'ILocalizationLanguage'
Ifaces.iface[88].parent = []
Ifaces.iface.insert(89, None)
Ifaces.iface[89] = Dummy()
Ifaces.iface[89].attr = []
Ifaces.iface[89].attr.insert(0, None)
Ifaces.iface[89].attr[0] = 'camouflages'
Ifaces.iface[89].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[89].callbackSubscriable = false
Ifaces.iface[89].defaultCallback = ''
Ifaces.iface[89].ifacename = 'ICamouflages'
Ifaces.iface[89].parent = []
Ifaces.iface.insert(90, None)
Ifaces.iface[90] = Dummy()
Ifaces.iface[90].attr = []
Ifaces.iface[90].attr.insert(0, None)
Ifaces.iface[90].attr[0] = 'planeID'
Ifaces.iface[90].attr.insert(1, None)
Ifaces.iface[90].attr[1] = 'camouflageID'
Ifaces.iface[90].attr.insert(2, None)
Ifaces.iface[90].attr[2] = 'camouflageType'
Ifaces.iface[90].attr.insert(3, None)
Ifaces.iface[90].attr[3] = 'camouflageClass'
Ifaces.iface[90].attr.insert(4, None)
Ifaces.iface[90].attr[4] = 'arenaType'
Ifaces.iface[90].attr.insert(5, None)
Ifaces.iface[90].attr[5] = 'priceScheme'
Ifaces.iface[90].attr.insert(6, None)
Ifaces.iface[90].attr[6] = 'bonusScheme'
Ifaces.iface[90].attr.insert(7, None)
Ifaces.iface[90].attr[7] = 'icoPath'
Ifaces.iface[90].attr.insert(8, None)
Ifaces.iface[90].attr[8] = 'isUnique'
Ifaces.iface[90].attr.insert(9, None)
Ifaces.iface[90].attr[9] = 'isNew'
Ifaces.iface[90].attr.insert(10, None)
Ifaces.iface[90].attr[10] = 'awardTag'
Ifaces.iface[90].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[90].callbackSubscriable = false
Ifaces.iface[90].defaultCallback = ''
Ifaces.iface[90].ifacename = 'ICamouflageDescription'
Ifaces.iface[90].parent = []
Ifaces.iface.insert(91, None)
Ifaces.iface[91] = Dummy()
Ifaces.iface[91].attr = []
Ifaces.iface[91].attr.insert(0, None)
Ifaces.iface[91].attr[0] = 'locked'
Ifaces.iface[91].attr.insert(1, None)
Ifaces.iface[91].attr[1] = 'expiryTime'
Ifaces.iface[91].attr.insert(2, None)
Ifaces.iface[91].attr[2] = 'buyTime'
Ifaces.iface[91].attr.insert(3, None)
Ifaces.iface[91].attr[3] = 'installed'
Ifaces.iface[91].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[91].callbackSubscriable = false
Ifaces.iface[91].defaultCallback = ''
Ifaces.iface[91].ifacename = 'ICamouflageStatus'
Ifaces.iface[91].parent = []
Ifaces.iface.insert(92, None)
Ifaces.iface[92] = Dummy()
Ifaces.iface[92].attr = []
Ifaces.iface[92].attr.insert(0, None)
Ifaces.iface[92].attr[0] = 'priceSchemes'
Ifaces.iface[92].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[92].callbackSubscriable = false
Ifaces.iface[92].defaultCallback = ''
Ifaces.iface[92].ifacename = 'IPriceSchemes'
Ifaces.iface[92].parent = []
Ifaces.iface.insert(93, None)
Ifaces.iface[93] = Dummy()
Ifaces.iface[93].attr = []
Ifaces.iface[93].attr.insert(0, None)
Ifaces.iface[93].attr[0] = 'bonusSchemes'
Ifaces.iface[93].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[93].callbackSubscriable = false
Ifaces.iface[93].defaultCallback = ''
Ifaces.iface[93].ifacename = 'IBonusSchemes'
Ifaces.iface[93].parent = []
Ifaces.iface.insert(94, None)
Ifaces.iface[94] = Dummy()
Ifaces.iface[94].attr = []
Ifaces.iface[94].attr.insert(0, None)
Ifaces.iface[94].attr[0] = 'delta'
Ifaces.iface[94].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[94].callbackSubscriable = false
Ifaces.iface[94].defaultCallback = ''
Ifaces.iface[94].ifacename = 'ITimeDelta'
Ifaces.iface[94].parent = []
Ifaces.iface.insert(95, None)
Ifaces.iface[95] = Dummy()
Ifaces.iface[95].attr = []
Ifaces.iface[95].attr.insert(0, None)
Ifaces.iface[95].attr[0] = 'value'
Ifaces.iface[95].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[95].callbackSubscriable = false
Ifaces.iface[95].defaultCallback = ''
Ifaces.iface[95].ifacename = 'IPlaneSalesLeft'
Ifaces.iface[95].parent = []
Ifaces.iface.insert(96, None)
Ifaces.iface[96] = Dummy()
Ifaces.iface[96].attr = []
Ifaces.iface[96].attr.insert(0, None)
Ifaces.iface[96].attr[0] = 'ids'
Ifaces.iface[96].attr.insert(1, None)
Ifaces.iface[96].attr[1] = 'gids'
Ifaces.iface[96].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[96].callbackSubscriable = false
Ifaces.iface[96].defaultCallback = ''
Ifaces.iface[96].ifacename = 'IInstalledCamouflage'
Ifaces.iface[96].parent = []
Ifaces.iface.insert(97, None)
Ifaces.iface[97] = Dummy()
Ifaces.iface[97].attr = []
Ifaces.iface[97].attr.insert(0, None)
Ifaces.iface[97].attr[0] = 'stats'
Ifaces.iface[97].attr.insert(1, None)
Ifaces.iface[97].attr[1] = 'gamesPlayed'
Ifaces.iface[97].attr.insert(2, None)
Ifaces.iface[97].attr[2] = 'lastGameTime'
Ifaces.iface[97].attr.insert(3, None)
Ifaces.iface[97].attr[3] = 'planes'
Ifaces.iface[97].attr.insert(4, None)
Ifaces.iface[97].attr[4] = 'createdAt'
Ifaces.iface[97].attr.insert(5, None)
Ifaces.iface[97].attr[5] = 'achievements'
Ifaces.iface[97].attr.insert(6, None)
Ifaces.iface[97].attr[6] = 'medals'
Ifaces.iface[97].attr.insert(7, None)
Ifaces.iface[97].attr[7] = 'ribbons'
Ifaces.iface[97].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[97].callbackSubscriable = false
Ifaces.iface[97].defaultCallback = ''
Ifaces.iface[97].ifacename = 'IPlayerSummaryStats'
Ifaces.iface[97].parent = []
Ifaces.iface.insert(98, None)
Ifaces.iface[98] = Dummy()
Ifaces.iface[98].attr = []
Ifaces.iface[98].attr.insert(0, None)
Ifaces.iface[98].attr[0] = 'planeName'
Ifaces.iface[98].attr.insert(1, None)
Ifaces.iface[98].attr[1] = 'level'
Ifaces.iface[98].attr.insert(2, None)
Ifaces.iface[98].attr[2] = 'icoPath'
Ifaces.iface[98].attr.insert(3, None)
Ifaces.iface[98].attr[3] = 'flagPath'
Ifaces.iface[98].attr.insert(4, None)
Ifaces.iface[98].attr[4] = 'nationID'
Ifaces.iface[98].attr.insert(5, None)
Ifaces.iface[98].attr[5] = 'planeID'
Ifaces.iface[98].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[98].callbackSubscriable = false
Ifaces.iface[98].defaultCallback = ''
Ifaces.iface[98].ifacename = 'IPlayerShortPlaneDescription'
Ifaces.iface[98].parent = []
Ifaces.iface.insert(99, None)
Ifaces.iface[99] = Dummy()
Ifaces.iface[99].attr = []
Ifaces.iface[99].attr.insert(0, None)
Ifaces.iface[99].attr[0] = 'played'
Ifaces.iface[99].attr.insert(1, None)
Ifaces.iface[99].attr[1] = 'winsPercent'
Ifaces.iface[99].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[99].callbackSubscriable = false
Ifaces.iface[99].defaultCallback = ''
Ifaces.iface[99].ifacename = 'IPlayerShortPlaneStats'
Ifaces.iface[99].parent = []
Ifaces.iface[99].parent.insert(0, None)
Ifaces.iface[99].parent[0] = 'IPlayerShortPlaneDescription'
Ifaces.iface.insert(100, None)
Ifaces.iface[100] = Dummy()
Ifaces.iface[100].attr = []
Ifaces.iface[100].attr.insert(0, None)
Ifaces.iface[100].attr[0] = 'stats'
Ifaces.iface[100].attr.insert(1, None)
Ifaces.iface[100].attr[1] = 'achievements'
Ifaces.iface[100].attr.insert(2, None)
Ifaces.iface[100].attr[2] = 'medals'
Ifaces.iface[100].attr.insert(3, None)
Ifaces.iface[100].attr[3] = 'ribbons'
Ifaces.iface[100].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[100].callbackSubscriable = false
Ifaces.iface[100].defaultCallback = ''
Ifaces.iface[100].ifacename = 'IPlayerPlaneStats'
Ifaces.iface[100].parent = []
Ifaces.iface.insert(101, None)
Ifaces.iface[101] = Dummy()
Ifaces.iface[101].attr = []
Ifaces.iface[101].attr.insert(0, None)
Ifaces.iface[101].attr[0] = 'paymentType'
Ifaces.iface[101].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[101].callbackSubscriable = false
Ifaces.iface[101].defaultCallback = ''
Ifaces.iface[101].ifacename = 'IPaymentType'
Ifaces.iface[101].parent = []
Ifaces.iface.insert(102, None)
Ifaces.iface[102] = Dummy()
Ifaces.iface[102].attr = []
Ifaces.iface[102].attr.insert(0, None)
Ifaces.iface[102].attr[0] = 'walletStatus'
Ifaces.iface[102].attr.insert(1, None)
Ifaces.iface[102].attr[1] = 'useGold'
Ifaces.iface[102].attr.insert(2, None)
Ifaces.iface[102].attr[2] = 'useFreeXP'
Ifaces.iface[102].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[102].callbackSubscriable = false
Ifaces.iface[102].defaultCallback = ''
Ifaces.iface[102].ifacename = 'IWalletSettings'
Ifaces.iface[102].parent = []
Ifaces.iface.insert(103, None)
Ifaces.iface[103] = Dummy()
Ifaces.iface[103].attr = []
Ifaces.iface[103].attr.insert(0, None)
Ifaces.iface[103].attr[0] = 'achievements'
Ifaces.iface[103].attr.insert(1, None)
Ifaces.iface[103].attr[1] = 'medals'
Ifaces.iface[103].attr.insert(2, None)
Ifaces.iface[103].attr[2] = 'ribbons'
Ifaces.iface[103].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[103].callbackSubscriable = false
Ifaces.iface[103].defaultCallback = ''
Ifaces.iface[103].ifacename = 'IAwardsList'
Ifaces.iface[103].parent = []
Ifaces.iface.insert(104, None)
Ifaces.iface[104] = Dummy()
Ifaces.iface[104].attr = []
Ifaces.iface[104].attr.insert(0, None)
Ifaces.iface[104].attr[0] = 'rid'
Ifaces.iface[104].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[104].callbackSubscriable = false
Ifaces.iface[104].defaultCallback = ''
Ifaces.iface[104].ifacename = 'ILastProcessedResponse'
Ifaces.iface[104].parent = []
Ifaces.iface.insert(105, None)
Ifaces.iface[105] = Dummy()
Ifaces.iface[105].attr = []
Ifaces.iface[105].attr.insert(0, None)
Ifaces.iface[105].attr[0] = 'data'
Ifaces.iface[105].attr.insert(1, None)
Ifaces.iface[105].attr[1] = 'callback'
Ifaces.iface[105].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[105].callbackSubscriable = false
Ifaces.iface[105].defaultCallback = ''
Ifaces.iface[105].ifacename = 'IResponse'
Ifaces.iface[105].parent = []
Ifaces.iface.insert(106, None)
Ifaces.iface[106] = Dummy()
Ifaces.iface[106].attr = []
Ifaces.iface[106].attr.insert(0, None)
Ifaces.iface[106].attr[0] = 'teams'
Ifaces.iface[106].attr.insert(1, None)
Ifaces.iface[106].attr[1] = 'healthsTO'
Ifaces.iface[106].attr.insert(2, None)
Ifaces.iface[106].attr[2] = 'myID'
Ifaces.iface[106].attr.insert(3, None)
Ifaces.iface[106].attr[3] = 'myData'
Ifaces.iface[106].attr.insert(4, None)
Ifaces.iface[106].attr[4] = 'quests'
Ifaces.iface[106].attr.insert(5, None)
Ifaces.iface[106].attr[5] = 'warAction'
Ifaces.iface[106].attr.insert(6, None)
Ifaces.iface[106].attr[6] = 'events'
Ifaces.iface[106].attr.insert(7, None)
Ifaces.iface[106].attr[7] = 'wasPlayerPractices'
Ifaces.iface[106].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[106].callbackSubscriable = false
Ifaces.iface[106].defaultCallback = ''
Ifaces.iface[106].ifacename = 'IBattleResult'
Ifaces.iface[106].parent = []
Ifaces.iface.insert(107, None)
Ifaces.iface[107] = Dummy()
Ifaces.iface[107].attr = []
Ifaces.iface[107].attr.insert(0, None)
Ifaces.iface[107].attr[0] = 'ids'
Ifaces.iface[107].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[107].callbackSubscriable = false
Ifaces.iface[107].defaultCallback = ''
Ifaces.iface[107].ifacename = 'IQuestList'
Ifaces.iface[107].parent = []
Ifaces.iface.insert(108, None)
Ifaces.iface[108] = Dummy()
Ifaces.iface[108].attr = []
Ifaces.iface[108].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[108].callbackSubscriable = false
Ifaces.iface[108].defaultCallback = ''
Ifaces.iface[108].ifacename = 'IQuest'
Ifaces.iface[108].parent = []
Ifaces.iface[108].parent.insert(0, None)
Ifaces.iface[108].parent[0] = 'IQuestDescription'
Ifaces.iface[108].parent.insert(1, None)
Ifaces.iface[108].parent[1] = 'IQuestAvaiblePlanes'
Ifaces.iface[108].parent.insert(2, None)
Ifaces.iface[108].parent[2] = 'IQuestResults'
Ifaces.iface.insert(109, None)
Ifaces.iface[109] = Dummy()
Ifaces.iface[109].attr = []
Ifaces.iface[109].attr.insert(0, None)
Ifaces.iface[109].attr[0] = 'name'
Ifaces.iface[109].attr.insert(1, None)
Ifaces.iface[109].attr[1] = 'start'
Ifaces.iface[109].attr.insert(2, None)
Ifaces.iface[109].attr[2] = 'end'
Ifaces.iface[109].attr.insert(3, None)
Ifaces.iface[109].attr[3] = 'type'
Ifaces.iface[109].attr.insert(4, None)
Ifaces.iface[109].attr[4] = 'maxCount'
Ifaces.iface[109].attr.insert(5, None)
Ifaces.iface[109].attr[5] = 'maps'
Ifaces.iface[109].attr.insert(6, None)
Ifaces.iface[109].attr[6] = 'forPremAccount'
Ifaces.iface[109].attr.insert(7, None)
Ifaces.iface[109].attr[7] = 'forClanAccount'
Ifaces.iface[109].attr.insert(8, None)
Ifaces.iface[109].attr[8] = 'group'
Ifaces.iface[109].attr.insert(9, None)
Ifaces.iface[109].attr[9] = 'isDaily'
Ifaces.iface[109].attr.insert(10, None)
Ifaces.iface[109].attr[10] = 'parentId'
Ifaces.iface[109].attr.insert(11, None)
Ifaces.iface[109].attr[11] = 'typeIsClan'
Ifaces.iface[109].attr.insert(12, None)
Ifaces.iface[109].attr[12] = 'typeIsIGR'
Ifaces.iface[109].attr.insert(13, None)
Ifaces.iface[109].attr[13] = 'typeIsHangar'
Ifaces.iface[109].attr.insert(14, None)
Ifaces.iface[109].attr[14] = 'typeIsPVP'
Ifaces.iface[109].attr.insert(15, None)
Ifaces.iface[109].attr[15] = 'typeIsPVE'
Ifaces.iface[109].attr.insert(16, None)
Ifaces.iface[109].attr[16] = 'typeIsRecruit'
Ifaces.iface[109].attr.insert(17, None)
Ifaces.iface[109].attr[17] = 'typeIsRecruiter'
Ifaces.iface[109].attr.insert(18, None)
Ifaces.iface[109].attr[18] = 'typeIsTokenQuest'
Ifaces.iface[109].attr.insert(19, None)
Ifaces.iface[109].attr[19] = 'isPooled'
Ifaces.iface[109].attr.insert(20, None)
Ifaces.iface[109].attr[20] = 'consistMain'
Ifaces.iface[109].attr.insert(21, None)
Ifaces.iface[109].attr[21] = 'consistChildes'
Ifaces.iface[109].attr.insert(22, None)
Ifaces.iface[109].attr[22] = 'unlockBy'
Ifaces.iface[109].attr.insert(23, None)
Ifaces.iface[109].attr[23] = 'unlockNext'
Ifaces.iface[109].attr.insert(24, None)
Ifaces.iface[109].attr[24] = 'planeBirthday'
Ifaces.iface[109].attr.insert(25, None)
Ifaces.iface[109].attr[25] = 'priceQuestChips'
Ifaces.iface[109].attr.insert(26, None)
Ifaces.iface[109].attr[26] = 'priceCredits'
Ifaces.iface[109].attr.insert(27, None)
Ifaces.iface[109].attr[27] = 'priceGold'
Ifaces.iface[109].attr.insert(28, None)
Ifaces.iface[109].attr[28] = 'priceTickets'
Ifaces.iface[109].attr.insert(29, None)
Ifaces.iface[109].attr[29] = 'availableBuyQuest'
Ifaces.iface[109].attr.insert(30, None)
Ifaces.iface[109].attr[30] = 'tirs'
Ifaces.iface[109].attr.insert(31, None)
Ifaces.iface[109].attr[31] = 'warStates'
Ifaces.iface[109].attr.insert(32, None)
Ifaces.iface[109].attr[32] = 'canAddTime'
Ifaces.iface[109].attr.insert(33, None)
Ifaces.iface[109].attr[33] = 'addTimeSec'
Ifaces.iface[109].attr.insert(34, None)
Ifaces.iface[109].attr[34] = 'priceAddTickets'
Ifaces.iface[109].attr.insert(35, None)
Ifaces.iface[109].attr[35] = 'priceAddGold'
Ifaces.iface[109].attr.insert(36, None)
Ifaces.iface[109].attr[36] = 'priceAddCredits'
Ifaces.iface[109].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[109].callbackSubscriable = false
Ifaces.iface[109].defaultCallback = ''
Ifaces.iface[109].ifacename = 'IQuestDescription'
Ifaces.iface[109].parent = []
Ifaces.iface[109].parent.insert(0, None)
Ifaces.iface[109].parent[0] = 'IQuestRead'
Ifaces.iface[109].parent.insert(1, None)
Ifaces.iface[109].parent[1] = 'IQuestHidden'
Ifaces.iface[109].parent.insert(2, None)
Ifaces.iface[109].parent[2] = 'IQuestDynDescription'
Ifaces.iface.insert(110, None)
Ifaces.iface[110] = Dummy()
Ifaces.iface[110].attr = []
Ifaces.iface[110].attr.insert(0, None)
Ifaces.iface[110].attr[0] = 'isRead'
Ifaces.iface[110].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[110].callbackSubscriable = false
Ifaces.iface[110].defaultCallback = ''
Ifaces.iface[110].ifacename = 'IQuestRead'
Ifaces.iface[110].parent = []
Ifaces.iface.insert(111, None)
Ifaces.iface[111] = Dummy()
Ifaces.iface[111].attr = []
Ifaces.iface[111].attr.insert(0, None)
Ifaces.iface[111].attr[0] = 'questID'
Ifaces.iface[111].cacheType = CACHE_TYPE.NONE
Ifaces.iface[111].callbackSubscriable = false
Ifaces.iface[111].defaultCallback = ''
Ifaces.iface[111].ifacename = 'IQuestBuy'
Ifaces.iface[111].parent = []
Ifaces.iface.insert(112, None)
Ifaces.iface[112] = Dummy()
Ifaces.iface[112].attr = []
Ifaces.iface[112].attr.insert(0, None)
Ifaces.iface[112].attr[0] = 'questID'
Ifaces.iface[112].cacheType = CACHE_TYPE.NONE
Ifaces.iface[112].callbackSubscriable = false
Ifaces.iface[112].defaultCallback = ''
Ifaces.iface[112].ifacename = 'IQuestProlong'
Ifaces.iface[112].parent = []
Ifaces.iface.insert(113, None)
Ifaces.iface[113] = Dummy()
Ifaces.iface[113].attr = []
Ifaces.iface[113].attr.insert(0, None)
Ifaces.iface[113].attr[0] = 'questID'
Ifaces.iface[113].cacheType = CACHE_TYPE.NONE
Ifaces.iface[113].callbackSubscriable = false
Ifaces.iface[113].defaultCallback = ''
Ifaces.iface[113].ifacename = 'IQuestChangeGroup'
Ifaces.iface[113].parent = []
Ifaces.iface.insert(114, None)
Ifaces.iface[114] = Dummy()
Ifaces.iface[114].attr = []
Ifaces.iface[114].attr.insert(0, None)
Ifaces.iface[114].attr[0] = 'questIDs'
Ifaces.iface[114].attr.insert(1, None)
Ifaces.iface[114].attr[1] = 'progress'
Ifaces.iface[114].attr.insert(2, None)
Ifaces.iface[114].attr[2] = 'planeLevel'
Ifaces.iface[114].cacheType = CACHE_TYPE.NONE
Ifaces.iface[114].callbackSubscriable = false
Ifaces.iface[114].defaultCallback = ''
Ifaces.iface[114].ifacename = 'IQuestDebugProcess'
Ifaces.iface[114].parent = []
Ifaces.iface.insert(115, None)
Ifaces.iface[115] = Dummy()
Ifaces.iface[115].attr = []
Ifaces.iface[115].attr.insert(0, None)
Ifaces.iface[115].attr[0] = 'hidden'
Ifaces.iface[115].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[115].callbackSubscriable = false
Ifaces.iface[115].defaultCallback = ''
Ifaces.iface[115].ifacename = 'IQuestHidden'
Ifaces.iface[115].parent = []
Ifaces.iface.insert(116, None)
Ifaces.iface[116] = Dummy()
Ifaces.iface[116].attr = []
Ifaces.iface[116].attr.insert(0, None)
Ifaces.iface[116].attr[0] = 'description'
Ifaces.iface[116].attr.insert(1, None)
Ifaces.iface[116].attr[1] = 'awards'
Ifaces.iface[116].attr.insert(2, None)
Ifaces.iface[116].attr[2] = 'maxProgress'
Ifaces.iface[116].attr.insert(3, None)
Ifaces.iface[116].attr[3] = 'hangar'
Ifaces.iface[116].attr.insert(4, None)
Ifaces.iface[116].attr[4] = 'isLocked'
Ifaces.iface[116].attr.insert(5, None)
Ifaces.iface[116].attr[5] = 'canBuyQuest'
Ifaces.iface[116].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[116].callbackSubscriable = false
Ifaces.iface[116].defaultCallback = ''
Ifaces.iface[116].ifacename = 'IQuestDynDescription'
Ifaces.iface[116].parent = []
Ifaces.iface.insert(117, None)
Ifaces.iface[117] = Dummy()
Ifaces.iface[117].attr = []
Ifaces.iface[117].attr.insert(0, None)
Ifaces.iface[117].attr[0] = 'planeIDs'
Ifaces.iface[117].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[117].callbackSubscriable = false
Ifaces.iface[117].defaultCallback = ''
Ifaces.iface[117].ifacename = 'IQuestAvaiblePlanes'
Ifaces.iface[117].parent = []
Ifaces.iface.insert(118, None)
Ifaces.iface[118] = Dummy()
Ifaces.iface[118].attr = []
Ifaces.iface[118].attr.insert(0, None)
Ifaces.iface[118].attr[0] = 'progress'
Ifaces.iface[118].attr.insert(1, None)
Ifaces.iface[118].attr[1] = 'completePool'
Ifaces.iface[118].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[118].callbackSubscriable = false
Ifaces.iface[118].defaultCallback = ''
Ifaces.iface[118].ifacename = 'IQuestResults'
Ifaces.iface[118].parent = []
Ifaces.iface.insert(119, None)
Ifaces.iface[119] = Dummy()
Ifaces.iface[119].attr = []
Ifaces.iface[119].attr.insert(0, None)
Ifaces.iface[119].attr[0] = 'questID'
Ifaces.iface[119].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[119].callbackSubscriable = false
Ifaces.iface[119].defaultCallback = ''
Ifaces.iface[119].ifacename = 'IQuestSelectConsist'
Ifaces.iface[119].parent = []
Ifaces.iface.insert(120, None)
Ifaces.iface[120] = Dummy()
Ifaces.iface[120].attr = []
Ifaces.iface[120].attr.insert(0, None)
Ifaces.iface[120].attr[0] = 'questIDs'
Ifaces.iface[120].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[120].callbackSubscriable = false
Ifaces.iface[120].defaultCallback = ''
Ifaces.iface[120].ifacename = 'IQuestListAvailableConsist'
Ifaces.iface[120].parent = []
Ifaces.iface.insert(121, None)
Ifaces.iface[121] = Dummy()
Ifaces.iface[121].attr = []
Ifaces.iface[121].attr.insert(0, None)
Ifaces.iface[121].attr[0] = 'endAction'
Ifaces.iface[121].attr.insert(1, None)
Ifaces.iface[121].attr[1] = 'isActive'
Ifaces.iface[121].attr.insert(2, None)
Ifaces.iface[121].attr[2] = 'enable'
Ifaces.iface[121].attr.insert(3, None)
Ifaces.iface[121].attr[3] = 'canBuyQuest'
Ifaces.iface[121].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[121].callbackSubscriable = false
Ifaces.iface[121].defaultCallback = ''
Ifaces.iface[121].ifacename = 'IQuestConsistEndAction'
Ifaces.iface[121].parent = []
Ifaces.iface.insert(122, None)
Ifaces.iface[122] = Dummy()
Ifaces.iface[122].attr = []
Ifaces.iface[122].attr.insert(0, None)
Ifaces.iface[122].attr[0] = 'globalCanCancel'
Ifaces.iface[122].attr.insert(1, None)
Ifaces.iface[122].attr[1] = 'coolDownFinish'
Ifaces.iface[122].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[122].callbackSubscriable = false
Ifaces.iface[122].defaultCallback = ''
Ifaces.iface[122].ifacename = 'IQuestPool'
Ifaces.iface[122].parent = []
Ifaces.iface.insert(123, None)
Ifaces.iface[123] = Dummy()
Ifaces.iface[123].attr = []
Ifaces.iface[123].attr.insert(0, None)
Ifaces.iface[123].attr[0] = 'ids'
Ifaces.iface[123].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[123].callbackSubscriable = false
Ifaces.iface[123].defaultCallback = ''
Ifaces.iface[123].ifacename = 'ISessionBattleResults'
Ifaces.iface[123].parent = []
Ifaces.iface.insert(124, None)
Ifaces.iface[124] = Dummy()
Ifaces.iface[124].attr = []
Ifaces.iface[124].attr.insert(0, None)
Ifaces.iface[124].attr[0] = 'arenaName'
Ifaces.iface[124].attr.insert(1, None)
Ifaces.iface[124].attr[1] = 'loadTime'
Ifaces.iface[124].attr.insert(2, None)
Ifaces.iface[124].attr[2] = 'planeID'
Ifaces.iface[124].attr.insert(3, None)
Ifaces.iface[124].attr[3] = 'killed'
Ifaces.iface[124].attr.insert(4, None)
Ifaces.iface[124].attr[4] = 'turretsDestroyed'
Ifaces.iface[124].attr.insert(5, None)
Ifaces.iface[124].attr[5] = 'objectsDestroyed'
Ifaces.iface[124].attr.insert(6, None)
Ifaces.iface[124].attr[6] = 'winState'
Ifaces.iface[124].attr.insert(7, None)
Ifaces.iface[124].attr[7] = 'teamIndex'
Ifaces.iface[124].attr.insert(8, None)
Ifaces.iface[124].attr[8] = 'credits'
Ifaces.iface[124].attr.insert(9, None)
Ifaces.iface[124].attr[9] = 'xp'
Ifaces.iface[124].attr.insert(10, None)
Ifaces.iface[124].attr[10] = 'xp_free'
Ifaces.iface[124].attr.insert(11, None)
Ifaces.iface[124].attr[11] = 'ribbons'
Ifaces.iface[124].attr.insert(12, None)
Ifaces.iface[124].attr[12] = 'achievements'
Ifaces.iface[124].attr.insert(13, None)
Ifaces.iface[124].attr[13] = 'medals'
Ifaces.iface[124].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[124].callbackSubscriable = false
Ifaces.iface[124].defaultCallback = ''
Ifaces.iface[124].ifacename = 'IBattleResultShort'
Ifaces.iface[124].parent = []
Ifaces.iface.insert(125, None)
Ifaces.iface[125] = Dummy()
Ifaces.iface[125].attr = []
Ifaces.iface[125].attr.insert(0, None)
Ifaces.iface[125].attr[0] = 'rentScheme'
Ifaces.iface[125].attr.insert(1, None)
Ifaces.iface[125].attr[1] = 'rentAvailable'
Ifaces.iface[125].attr.insert(2, None)
Ifaces.iface[125].attr[2] = 'buyAvailable'
Ifaces.iface[125].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[125].callbackSubscriable = false
Ifaces.iface[125].defaultCallback = ''
Ifaces.iface[125].ifacename = 'IRentConf'
Ifaces.iface[125].parent = []
Ifaces.iface.insert(126, None)
Ifaces.iface[126] = Dummy()
Ifaces.iface[126].attr = []
Ifaces.iface[126].attr.insert(0, None)
Ifaces.iface[126].attr[0] = 'expiryTime'
Ifaces.iface[126].attr.insert(1, None)
Ifaces.iface[126].attr[1] = 'refundPrice'
Ifaces.iface[126].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[126].callbackSubscriable = false
Ifaces.iface[126].defaultCallback = ''
Ifaces.iface[126].ifacename = 'IRent'
Ifaces.iface[126].parent = []
Ifaces.iface.insert(127, None)
Ifaces.iface[127] = Dummy()
Ifaces.iface[127].attr = []
Ifaces.iface[127].attr.insert(0, None)
Ifaces.iface[127].attr[0] = 'start'
Ifaces.iface[127].attr.insert(1, None)
Ifaces.iface[127].attr[1] = 'end'
Ifaces.iface[127].attr.insert(2, None)
Ifaces.iface[127].attr[2] = 'showTime'
Ifaces.iface[127].attr.insert(3, None)
Ifaces.iface[127].attr[3] = 'name'
Ifaces.iface[127].attr.insert(4, None)
Ifaces.iface[127].attr[4] = 'description'
Ifaces.iface[127].attr.insert(5, None)
Ifaces.iface[127].attr[5] = 'changes'
Ifaces.iface[127].attr.insert(6, None)
Ifaces.iface[127].attr[6] = 'isRead'
Ifaces.iface[127].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[127].callbackSubscriable = false
Ifaces.iface[127].defaultCallback = ''
Ifaces.iface[127].ifacename = 'IActionUI'
Ifaces.iface[127].parent = []
Ifaces.iface.insert(128, None)
Ifaces.iface[128] = Dummy()
Ifaces.iface[128].attr = []
Ifaces.iface[128].attr.insert(0, None)
Ifaces.iface[128].attr[0] = 'ids'
Ifaces.iface[128].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[128].callbackSubscriable = false
Ifaces.iface[128].defaultCallback = ''
Ifaces.iface[128].ifacename = 'IActionUIList'
Ifaces.iface[128].parent = []
Ifaces.iface.insert(129, None)
Ifaces.iface[129] = Dummy()
Ifaces.iface[129].attr = []
Ifaces.iface[129].attr.insert(0, None)
Ifaces.iface[129].attr[0] = 'measurementSystem'
Ifaces.iface[129].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[129].callbackSubscriable = false
Ifaces.iface[129].defaultCallback = ''
Ifaces.iface[129].ifacename = 'IMeasurementSystem'
Ifaces.iface[129].parent = []
Ifaces.iface.insert(130, None)
Ifaces.iface[130] = Dummy()
Ifaces.iface[130].attr = []
Ifaces.iface[130].attr.insert(0, None)
Ifaces.iface[130].attr[0] = 'distancePost'
Ifaces.iface[130].attr.insert(1, None)
Ifaces.iface[130].attr[1] = 'speedPost'
Ifaces.iface[130].attr.insert(2, None)
Ifaces.iface[130].attr[2] = 'massPost'
Ifaces.iface[130].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[130].callbackSubscriable = false
Ifaces.iface[130].defaultCallback = ''
Ifaces.iface[130].ifacename = 'IMeasurementSystemInfo'
Ifaces.iface[130].parent = []
Ifaces.iface.insert(131, None)
Ifaces.iface[131] = Dummy()
Ifaces.iface[131].attr = []
Ifaces.iface[131].attr.insert(0, None)
Ifaces.iface[131].attr[0] = 'measurementSystems'
Ifaces.iface[131].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[131].callbackSubscriable = false
Ifaces.iface[131].defaultCallback = ''
Ifaces.iface[131].ifacename = 'IMeasurementSystemsList'
Ifaces.iface[131].parent = []
Ifaces.iface.insert(132, None)
Ifaces.iface[132] = Dummy()
Ifaces.iface[132].attr = []
Ifaces.iface[132].attr.insert(0, None)
Ifaces.iface[132].attr[0] = 'operations'
Ifaces.iface[132].attr.insert(1, None)
Ifaces.iface[132].attr[1] = 'res'
Ifaces.iface[132].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[132].callbackSubscriable = false
Ifaces.iface[132].defaultCallback = ''
Ifaces.iface[132].ifacename = 'ITransaction'
Ifaces.iface[132].parent = []
Ifaces.iface.insert(133, None)
Ifaces.iface[133] = Dummy()
Ifaces.iface[133].attr = []
Ifaces.iface[133].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[133].callbackSubscriable = false
Ifaces.iface[133].defaultCallback = ''
Ifaces.iface[133].ifacename = 'IRequestsLocker'
Ifaces.iface[133].parent = []
Ifaces.iface.insert(134, None)
Ifaces.iface[134] = Dummy()
Ifaces.iface[134].attr = []
Ifaces.iface[134].attr.insert(0, None)
Ifaces.iface[134].attr[0] = 'pvpUnlocked'
Ifaces.iface[134].attr.insert(1, None)
Ifaces.iface[134].attr[1] = 'pveEnabled'
Ifaces.iface[134].attr.insert(2, None)
Ifaces.iface[134].attr[2] = 'curMode'
Ifaces.iface[134].attr.insert(3, None)
Ifaces.iface[134].attr[3] = 'defaultMode'
Ifaces.iface[134].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[134].callbackSubscriable = false
Ifaces.iface[134].defaultCallback = ''
Ifaces.iface[134].ifacename = 'IGameModesParams'
Ifaces.iface[134].parent = []
Ifaces.iface.insert(135, None)
Ifaces.iface[135] = Dummy()
Ifaces.iface[135].attr = []
Ifaces.iface[135].attr.insert(0, None)
Ifaces.iface[135].attr[0] = 'ids'
Ifaces.iface[135].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[135].callbackSubscriable = false
Ifaces.iface[135].defaultCallback = ''
Ifaces.iface[135].ifacename = 'IPvEPlanes'
Ifaces.iface[135].parent = []
Ifaces.iface.insert(136, None)
Ifaces.iface[136] = Dummy()
Ifaces.iface[136].attr = []
Ifaces.iface[136].attr.insert(0, None)
Ifaces.iface[136].attr[0] = 'utc'
Ifaces.iface[136].attr.insert(1, None)
Ifaces.iface[136].attr[1] = 'time_shift'
Ifaces.iface[136].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[136].callbackSubscriable = false
Ifaces.iface[136].defaultCallback = ''
Ifaces.iface[136].ifacename = 'IRestartTime'
Ifaces.iface[136].parent = []
Ifaces.iface.insert(137, None)
Ifaces.iface[137] = Dummy()
Ifaces.iface[137].attr = []
Ifaces.iface[137].attr.insert(0, None)
Ifaces.iface[137].attr[0] = 'roomID'
Ifaces.iface[137].attr.insert(1, None)
Ifaces.iface[137].attr[1] = 'type'
Ifaces.iface[137].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[137].callbackSubscriable = false
Ifaces.iface[137].defaultCallback = ''
Ifaces.iface[137].ifacename = 'IIGR'
Ifaces.iface[137].parent = []
Ifaces.iface.insert(138, None)
Ifaces.iface[138] = Dummy()
Ifaces.iface[138].attr = []
Ifaces.iface[138].attr.insert(0, None)
Ifaces.iface[138].attr[0] = 'isAvailable'
Ifaces.iface[138].cacheType = CACHE_TYPE.NONE
Ifaces.iface[138].callbackSubscriable = false
Ifaces.iface[138].defaultCallback = ''
Ifaces.iface[138].ifacename = 'IPvEAvailable'
Ifaces.iface[138].parent = []
Ifaces.iface.insert(139, None)
Ifaces.iface[139] = Dummy()
Ifaces.iface[139].attr = []
Ifaces.iface[139].attr.insert(0, None)
Ifaces.iface[139].attr[0] = 'clanDBID'
Ifaces.iface[139].attr.insert(1, None)
Ifaces.iface[139].attr[1] = 'clanName'
Ifaces.iface[139].attr.insert(2, None)
Ifaces.iface[139].attr[2] = 'clanAbbrev'
Ifaces.iface[139].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[139].callbackSubscriable = false
Ifaces.iface[139].defaultCallback = ''
Ifaces.iface[139].ifacename = 'IClanInfoShort'
Ifaces.iface[139].parent = []
Ifaces.iface.insert(140, None)
Ifaces.iface[140] = Dummy()
Ifaces.iface[140].attr = []
Ifaces.iface[140].attr.insert(0, None)
Ifaces.iface[140].attr[0] = 'clanMotto'
Ifaces.iface[140].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[140].callbackSubscriable = false
Ifaces.iface[140].defaultCallback = ''
Ifaces.iface[140].ifacename = 'IClanMotto'
Ifaces.iface[140].parent = []
Ifaces.iface.insert(141, None)
Ifaces.iface[141] = Dummy()
Ifaces.iface[141].attr = []
Ifaces.iface[141].attr.insert(0, None)
Ifaces.iface[141].attr[0] = 'clanDescr'
Ifaces.iface[141].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[141].callbackSubscriable = false
Ifaces.iface[141].defaultCallback = ''
Ifaces.iface[141].ifacename = 'IClanInfo'
Ifaces.iface[141].parent = []
Ifaces.iface[141].parent.insert(0, None)
Ifaces.iface[141].parent[0] = 'IClanInfoShort'
Ifaces.iface[141].parent.insert(1, None)
Ifaces.iface[141].parent[1] = 'IClanMotto'
Ifaces.iface.insert(142, None)
Ifaces.iface[142] = Dummy()
Ifaces.iface[142].attr = []
Ifaces.iface[142].attr.insert(0, None)
Ifaces.iface[142].attr[0] = 'clanDBID'
Ifaces.iface[142].attr.insert(1, None)
Ifaces.iface[142].attr[1] = 'role'
Ifaces.iface[142].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[142].callbackSubscriable = false
Ifaces.iface[142].defaultCallback = ''
Ifaces.iface[142].ifacename = 'IAccountClanData'
Ifaces.iface[142].parent = []
Ifaces.iface.insert(143, None)
Ifaces.iface[143] = Dummy()
Ifaces.iface[143].attr = []
Ifaces.iface[143].attr.insert(0, None)
Ifaces.iface[143].attr[0] = 'memberIDs'
Ifaces.iface[143].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[143].callbackSubscriable = false
Ifaces.iface[143].defaultCallback = ''
Ifaces.iface[143].ifacename = 'IClanMembers'
Ifaces.iface[143].parent = []
Ifaces.iface.insert(144, None)
Ifaces.iface[144] = Dummy()
Ifaces.iface[144].attr = []
Ifaces.iface[144].attr.insert(0, None)
Ifaces.iface[144].attr[0] = 'nickname'
Ifaces.iface[144].attr.insert(1, None)
Ifaces.iface[144].attr[1] = 'role'
Ifaces.iface[144].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[144].callbackSubscriable = false
Ifaces.iface[144].defaultCallback = ''
Ifaces.iface[144].ifacename = 'IClanMember'
Ifaces.iface[144].parent = []
Ifaces.iface.insert(145, None)
Ifaces.iface[145] = Dummy()
Ifaces.iface[145].attr = []
Ifaces.iface[145].attr.insert(0, None)
Ifaces.iface[145].attr[0] = 'rate'
Ifaces.iface[145].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[145].callbackSubscriable = false
Ifaces.iface[145].defaultCallback = ''
Ifaces.iface[145].ifacename = 'IExchangeXPRate'
Ifaces.iface[145].parent = []
Ifaces.iface.insert(146, None)
Ifaces.iface[146] = Dummy()
Ifaces.iface[146].attr = []
Ifaces.iface[146].attr.insert(0, None)
Ifaces.iface[146].attr[0] = 'groups'
Ifaces.iface[146].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[146].callbackSubscriable = false
Ifaces.iface[146].defaultCallback = ''
Ifaces.iface[146].ifacename = 'IAchieveGroups'
Ifaces.iface[146].parent = []
Ifaces.iface.insert(147, None)
Ifaces.iface[147] = Dummy()
Ifaces.iface[147].attr = []
Ifaces.iface[147].attr.insert(0, None)
Ifaces.iface[147].attr[0] = 'spaces'
Ifaces.iface[147].attr.insert(1, None)
Ifaces.iface[147].attr[1] = 'spaceTypes'
Ifaces.iface[147].attr.insert(2, None)
Ifaces.iface[147].attr[2] = 'spaceImages'
Ifaces.iface[147].attr.insert(3, None)
Ifaces.iface[147].attr[3] = 'showWindow'
Ifaces.iface[147].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[147].callbackSubscriable = false
Ifaces.iface[147].defaultCallback = 'iface.listener'
Ifaces.iface[147].ifacename = 'IHangarSpaces'
Ifaces.iface[147].parent = []
Ifaces.iface.insert(148, None)
Ifaces.iface[148] = Dummy()
Ifaces.iface[148].attr = []
Ifaces.iface[148].attr.insert(0, None)
Ifaces.iface[148].attr[0] = 'hash'
Ifaces.iface[148].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[148].callbackSubscriable = false
Ifaces.iface[148].defaultCallback = ''
Ifaces.iface[148].ifacename = 'IHangarSpacesHash'
Ifaces.iface[148].parent = []
Ifaces.iface.insert(149, None)
Ifaces.iface[149] = Dummy()
Ifaces.iface[149].attr = []
Ifaces.iface[149].attr.insert(0, None)
Ifaces.iface[149].attr[0] = 'spaceID'
Ifaces.iface[149].attr.insert(1, None)
Ifaces.iface[149].attr[1] = 'isModal'
Ifaces.iface[149].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[149].callbackSubscriable = false
Ifaces.iface[149].defaultCallback = ''
Ifaces.iface[149].ifacename = 'ICurrentHangarSpace'
Ifaces.iface[149].parent = []
Ifaces.iface.insert(150, None)
Ifaces.iface[150] = Dummy()
Ifaces.iface[150].attr = []
Ifaces.iface[150].attr.insert(0, None)
Ifaces.iface[150].attr[0] = 'idTypeList'
Ifaces.iface[150].attr.insert(1, None)
Ifaces.iface[150].attr[1] = 'code'
Ifaces.iface[150].attr.insert(2, None)
Ifaces.iface[150].attr[2] = 'description'
Ifaces.iface[150].attr.insert(3, None)
Ifaces.iface[150].attr[3] = 'kwargs'
Ifaces.iface[150].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[150].callbackSubscriable = false
Ifaces.iface[150].defaultCallback = 'iface.listener'
Ifaces.iface[150].ifacename = 'IError'
Ifaces.iface[150].parent = []
Ifaces.iface.insert(151, None)
Ifaces.iface[151] = Dummy()
Ifaces.iface[151].attr = []
Ifaces.iface[151].attr.insert(0, None)
Ifaces.iface[151].attr[0] = 'activeEvents'
Ifaces.iface[151].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[151].callbackSubscriable = false
Ifaces.iface[151].defaultCallback = ''
Ifaces.iface[151].ifacename = 'IActiveEvents'
Ifaces.iface[151].parent = []
Ifaces.iface.insert(152, None)
Ifaces.iface[152] = Dummy()
Ifaces.iface[152].attr = []
Ifaces.iface[152].attr.insert(0, None)
Ifaces.iface[152].attr[0] = 'state'
Ifaces.iface[152].attr.insert(1, None)
Ifaces.iface[152].attr[1] = 'findMask'
Ifaces.iface[152].attr.insert(2, None)
Ifaces.iface[152].attr[2] = 'autoFindTime'
Ifaces.iface[152].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[152].callbackSubscriable = false
Ifaces.iface[152].defaultCallback = ''
Ifaces.iface[152].ifacename = 'IAutoFindSquad'
Ifaces.iface[152].parent = []
Ifaces.iface.insert(153, None)
Ifaces.iface[153] = Dummy()
Ifaces.iface[153].attr = []
Ifaces.iface[153].attr.insert(0, None)
Ifaces.iface[153].attr[0] = 'refresh'
Ifaces.iface[153].attr.insert(1, None)
Ifaces.iface[153].attr[1] = 'finders'
Ifaces.iface[153].attr.insert(2, None)
Ifaces.iface[153].attr[2] = 'players'
Ifaces.iface[153].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[153].callbackSubscriable = false
Ifaces.iface[153].defaultCallback = ''
Ifaces.iface[153].ifacename = 'IAutoFindSquadList'
Ifaces.iface[153].parent = []
Ifaces.iface.insert(154, None)
Ifaces.iface[154] = Dummy()
Ifaces.iface[154].attr = []
Ifaces.iface[154].attr.insert(0, None)
Ifaces.iface[154].attr[0] = 'prevBirthday'
Ifaces.iface[154].attr.insert(1, None)
Ifaces.iface[154].attr[1] = 'nextBirthday'
Ifaces.iface[154].attr.insert(2, None)
Ifaces.iface[154].attr[2] = 'duration'
Ifaces.iface[154].attr.insert(3, None)
Ifaces.iface[154].attr[3] = 'daysTillBirthday'
Ifaces.iface[154].attr.insert(4, None)
Ifaces.iface[154].attr[4] = 'birthdayTime'
Ifaces.iface[154].attr.insert(5, None)
Ifaces.iface[154].attr[5] = 'birthdayTimeStr'
Ifaces.iface[154].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[154].callbackSubscriable = false
Ifaces.iface[154].defaultCallback = ''
Ifaces.iface[154].ifacename = 'IPlaneBirthday'
Ifaces.iface[154].parent = []
Ifaces.iface.insert(155, None)
Ifaces.iface[155] = Dummy()
Ifaces.iface[155].attr = []
Ifaces.iface[155].attr.insert(0, None)
Ifaces.iface[155].attr[0] = 'bonus'
Ifaces.iface[155].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[155].callbackSubscriable = false
Ifaces.iface[155].defaultCallback = ''
Ifaces.iface[155].ifacename = 'IPlaneBirthdayBonus'
Ifaces.iface[155].parent = []
Ifaces.iface.insert(156, None)
Ifaces.iface[156] = Dummy()
Ifaces.iface[156].attr = []
Ifaces.iface[156].attr.insert(0, None)
Ifaces.iface[156].attr[0] = 'current'
Ifaces.iface[156].attr.insert(1, None)
Ifaces.iface[156].attr[1] = 'maximum'
Ifaces.iface[156].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[156].callbackSubscriable = false
Ifaces.iface[156].defaultCallback = ''
Ifaces.iface[156].ifacename = 'IPlaneBirthdayProgress'
Ifaces.iface[156].parent = []
Ifaces.iface.insert(157, None)
Ifaces.iface[157] = Dummy()
Ifaces.iface[157].attr = []
Ifaces.iface[157].attr.insert(0, None)
Ifaces.iface[157].attr[0] = 'title'
Ifaces.iface[157].attr.insert(1, None)
Ifaces.iface[157].attr[1] = 'description'
Ifaces.iface[157].attr.insert(2, None)
Ifaces.iface[157].attr[2] = 'isEnabled'
Ifaces.iface[157].attr.insert(3, None)
Ifaces.iface[157].attr[3] = 'isCompleted'
Ifaces.iface[157].attr.insert(4, None)
Ifaces.iface[157].attr[4] = 'answer'
Ifaces.iface[157].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[157].callbackSubscriable = false
Ifaces.iface[157].defaultCallback = ''
Ifaces.iface[157].ifacename = 'IInterview'
Ifaces.iface[157].parent = []
Ifaces.iface.insert(158, None)
Ifaces.iface[158] = Dummy()
Ifaces.iface[158].attr = []
Ifaces.iface[158].attr.insert(0, None)
Ifaces.iface[158].attr[0] = 'endAction'
Ifaces.iface[158].attr.insert(1, None)
Ifaces.iface[158].attr[1] = 'endDiscount'
Ifaces.iface[158].attr.insert(2, None)
Ifaces.iface[158].attr[2] = 'isActive'
Ifaces.iface[158].attr.insert(3, None)
Ifaces.iface[158].attr[3] = 'enable'
Ifaces.iface[158].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[158].callbackSubscriable = false
Ifaces.iface[158].defaultCallback = ''
Ifaces.iface[158].ifacename = 'ISkinnerBoxEndAction'
Ifaces.iface[158].parent = []
Ifaces.iface.insert(159, None)
Ifaces.iface[159] = Dummy()
Ifaces.iface[159].attr = []
Ifaces.iface[159].attr.insert(0, None)
Ifaces.iface[159].attr[0] = 'ticketPrice'
Ifaces.iface[159].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[159].callbackSubscriable = false
Ifaces.iface[159].defaultCallback = ''
Ifaces.iface[159].ifacename = 'ITicketPrice'
Ifaces.iface[159].parent = []
Ifaces.iface.insert(160, None)
Ifaces.iface[160] = Dummy()
Ifaces.iface[160].attr = []
Ifaces.iface[160].attr.insert(0, None)
Ifaces.iface[160].attr[0] = 'discount'
Ifaces.iface[160].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[160].callbackSubscriable = false
Ifaces.iface[160].defaultCallback = ''
Ifaces.iface[160].ifacename = 'IGoldDiscount'
Ifaces.iface[160].parent = []
Ifaces.iface.insert(161, None)
Ifaces.iface[161] = Dummy()
Ifaces.iface[161].attr = []
Ifaces.iface[161].attr.insert(0, None)
Ifaces.iface[161].attr[0] = 'ticketPrice'
Ifaces.iface[161].attr.insert(1, None)
Ifaces.iface[161].attr[1] = 'ticketPriceCredits'
Ifaces.iface[161].attr.insert(2, None)
Ifaces.iface[161].attr[2] = 'ticketSellCredits'
Ifaces.iface[161].attr.insert(3, None)
Ifaces.iface[161].attr[3] = 'canBuyByGold'
Ifaces.iface[161].attr.insert(4, None)
Ifaces.iface[161].attr[4] = 'canBuyByCredits'
Ifaces.iface[161].attr.insert(5, None)
Ifaces.iface[161].attr[5] = 'canSellByCredits'
Ifaces.iface[161].attr.insert(6, None)
Ifaces.iface[161].attr[6] = 'canQuestAwardTicket'
Ifaces.iface[161].attr.insert(7, None)
Ifaces.iface[161].attr[7] = 'canBuyByGoldEnd'
Ifaces.iface[161].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[161].callbackSubscriable = false
Ifaces.iface[161].defaultCallback = ''
Ifaces.iface[161].ifacename = 'IExchangeTicketPrice'
Ifaces.iface[161].parent = []
Ifaces.iface.insert(162, None)
Ifaces.iface[162] = Dummy()
Ifaces.iface[162].attr = []
Ifaces.iface[162].attr.insert(0, None)
Ifaces.iface[162].attr[0] = 'countTickets'
Ifaces.iface[162].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[162].callbackSubscriable = false
Ifaces.iface[162].defaultCallback = ''
Ifaces.iface[162].ifacename = 'IExchangeGoldTicket'
Ifaces.iface[162].parent = []
Ifaces.iface.insert(163, None)
Ifaces.iface[163] = Dummy()
Ifaces.iface[163].attr = []
Ifaces.iface[163].attr.insert(0, None)
Ifaces.iface[163].attr[0] = 'ids'
Ifaces.iface[163].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[163].callbackSubscriable = false
Ifaces.iface[163].defaultCallback = ''
Ifaces.iface[163].ifacename = 'ITicketPlanes'
Ifaces.iface[163].parent = []
Ifaces.iface.insert(164, None)
Ifaces.iface[164] = Dummy()
Ifaces.iface[164].attr = []
Ifaces.iface[164].attr.insert(0, None)
Ifaces.iface[164].attr[0] = 'isEnabled'
Ifaces.iface[164].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[164].callbackSubscriable = false
Ifaces.iface[164].defaultCallback = ''
Ifaces.iface[164].ifacename = 'IPlaneBirthdayEnabled'
Ifaces.iface[164].parent = []
Ifaces.iface.insert(165, None)
Ifaces.iface[165] = Dummy()
Ifaces.iface[165].attr = []
Ifaces.iface[165].attr.insert(0, None)
Ifaces.iface[165].attr[0] = 'requiredExperience'
Ifaces.iface[165].cacheType = CACHE_TYPE.NONE
Ifaces.iface[165].callbackSubscriable = false
Ifaces.iface[165].defaultCallback = ''
Ifaces.iface[165].ifacename = 'IRequiredExperience'
Ifaces.iface[165].parent = []
Ifaces.iface.insert(166, None)
Ifaces.iface[166] = Dummy()
Ifaces.iface[166].attr = []
Ifaces.iface[166].attr.insert(0, None)
Ifaces.iface[166].attr[0] = 'weaponSlots'
Ifaces.iface[166].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[166].callbackSubscriable = false
Ifaces.iface[166].defaultCallback = ''
Ifaces.iface[166].ifacename = 'IPlaneWeapons'
Ifaces.iface[166].parent = []
Ifaces.iface.insert(167, None)
Ifaces.iface[167] = Dummy()
Ifaces.iface[167].attr = []
Ifaces.iface[167].attr.insert(0, None)
Ifaces.iface[167].attr[0] = 'weaponCount'
Ifaces.iface[167].attr.insert(1, None)
Ifaces.iface[167].attr[1] = 'weaponType'
Ifaces.iface[167].attr.insert(2, None)
Ifaces.iface[167].attr[2] = 'weaponId'
Ifaces.iface[167].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[167].callbackSubscriable = false
Ifaces.iface[167].defaultCallback = ''
Ifaces.iface[167].ifacename = 'IWeaponInfo'
Ifaces.iface[167].parent = []
Ifaces.iface.insert(168, None)
Ifaces.iface[168] = Dummy()
Ifaces.iface[168].attr = []
Ifaces.iface[168].attr.insert(0, None)
Ifaces.iface[168].attr[0] = 'optionList'
Ifaces.iface[168].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[168].callbackSubscriable = false
Ifaces.iface[168].defaultCallback = ''
Ifaces.iface[168].ifacename = 'IPremiumCost'
Ifaces.iface[168].parent = []
Ifaces.iface.insert(169, None)
Ifaces.iface[169] = Dummy()
Ifaces.iface[169].attr = []
Ifaces.iface[169].attr.insert(0, None)
Ifaces.iface[169].attr[0] = 'isVisible'
Ifaces.iface[169].cacheType = CACHE_TYPE.NONE
Ifaces.iface[169].callbackSubscriable = false
Ifaces.iface[169].defaultCallback = ''
Ifaces.iface[169].ifacename = 'IWaitingScreen'
Ifaces.iface[169].parent = []
Ifaces.iface.insert(170, None)
Ifaces.iface[170] = Dummy()
Ifaces.iface[170].attr = []
Ifaces.iface[170].attr.insert(0, None)
Ifaces.iface[170].attr[0] = 'averageTime'
Ifaces.iface[170].attr.insert(1, None)
Ifaces.iface[170].attr[1] = 'tipTime'
Ifaces.iface[170].attr.insert(2, None)
Ifaces.iface[170].attr[2] = 'maxTime'
Ifaces.iface[170].attr.insert(3, None)
Ifaces.iface[170].attr[3] = 'recommendedLevel'
Ifaces.iface[170].cacheType = CACHE_TYPE.NONE
Ifaces.iface[170].callbackSubscriable = false
Ifaces.iface[170].defaultCallback = ''
Ifaces.iface[170].ifacename = 'IAvaregeTime'
Ifaces.iface[170].parent = []
Ifaces.iface.insert(171, None)
Ifaces.iface[171] = Dummy()
Ifaces.iface[171].attr = []
Ifaces.iface[171].attr.insert(0, None)
Ifaces.iface[171].attr[0] = 'enable'
Ifaces.iface[171].attr.insert(1, None)
Ifaces.iface[171].attr[1] = 'canRegisterNewRecruit'
Ifaces.iface[171].attr.insert(2, None)
Ifaces.iface[171].attr[2] = 'viewSideReferralPanel'
Ifaces.iface[171].attr.insert(3, None)
Ifaces.iface[171].attr[3] = 'canHaveRecruits'
Ifaces.iface[171].attr.insert(4, None)
Ifaces.iface[171].attr[4] = 'invitesLeft'
Ifaces.iface[171].attr.insert(5, None)
Ifaces.iface[171].attr[5] = 'startRecruiterTime'
Ifaces.iface[171].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[171].callbackSubscriable = false
Ifaces.iface[171].defaultCallback = ''
Ifaces.iface[171].ifacename = 'IReferralStatus'
Ifaces.iface[171].parent = []
Ifaces.iface.insert(172, None)
Ifaces.iface[172] = Dummy()
Ifaces.iface[172].attr = []
Ifaces.iface[172].attr.insert(0, None)
Ifaces.iface[172].attr[0] = 'dayLengthActions'
Ifaces.iface[172].attr.insert(1, None)
Ifaces.iface[172].attr[1] = 'goldNeedBuyRecruit'
Ifaces.iface[172].attr.insert(2, None)
Ifaces.iface[172].attr[2] = 'premiumNeedBuyRecruitLow'
Ifaces.iface[172].attr.insert(3, None)
Ifaces.iface[172].attr[3] = 'premiumNeedBuyRecruitHigh'
Ifaces.iface[172].attr.insert(4, None)
Ifaces.iface[172].attr[4] = 'countCheckPoint'
Ifaces.iface[172].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[172].callbackSubscriable = false
Ifaces.iface[172].defaultCallback = ''
Ifaces.iface[172].ifacename = 'IReferralDescription'
Ifaces.iface[172].parent = []
Ifaces.iface.insert(173, None)
Ifaces.iface[173] = Dummy()
Ifaces.iface[173].attr = []
Ifaces.iface[173].attr.insert(0, None)
Ifaces.iface[173].attr[0] = 'urlLink'
Ifaces.iface[173].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[173].callbackSubscriable = false
Ifaces.iface[173].defaultCallback = ''
Ifaces.iface[173].ifacename = 'IReferralInviteLink'
Ifaces.iface[173].parent = []
Ifaces.iface.insert(174, None)
Ifaces.iface[174] = Dummy()
Ifaces.iface[174].attr = []
Ifaces.iface[174].attr.insert(0, None)
Ifaces.iface[174].attr[0] = 'recruiterID'
Ifaces.iface[174].attr.insert(1, None)
Ifaces.iface[174].attr[1] = 'recruiterName'
Ifaces.iface[174].attr.insert(2, None)
Ifaces.iface[174].attr[2] = 'recruits'
Ifaces.iface[174].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[174].callbackSubscriable = false
Ifaces.iface[174].defaultCallback = ''
Ifaces.iface[174].ifacename = 'IReferralLinks'
Ifaces.iface[174].parent = []
Ifaces.iface.insert(175, None)
Ifaces.iface[175] = Dummy()
Ifaces.iface[175].attr = []
Ifaces.iface[175].attr.insert(0, None)
Ifaces.iface[175].attr[0] = 'startReferralLinkTime'
Ifaces.iface[175].attr.insert(1, None)
Ifaces.iface[175].attr[1] = 'winsInSquad'
Ifaces.iface[175].attr.insert(2, None)
Ifaces.iface[175].attr[2] = 'buyPremium'
Ifaces.iface[175].attr.insert(3, None)
Ifaces.iface[175].attr[3] = 'buyGold'
Ifaces.iface[175].attr.insert(4, None)
Ifaces.iface[175].attr[4] = 'active'
Ifaces.iface[175].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[175].callbackSubscriable = false
Ifaces.iface[175].defaultCallback = ''
Ifaces.iface[175].ifacename = 'IReferralRecruitStatus'
Ifaces.iface[175].parent = []
Ifaces.iface.insert(176, None)
Ifaces.iface[176] = Dummy()
Ifaces.iface[176].attr = []
Ifaces.iface[176].attr.insert(0, None)
Ifaces.iface[176].attr[0] = 'archived'
Ifaces.iface[176].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[176].callbackSubscriable = false
Ifaces.iface[176].defaultCallback = ''
Ifaces.iface[176].ifacename = 'IReferralRecruitArchiveStatus'
Ifaces.iface[176].parent = []
Ifaces.iface.insert(177, None)
Ifaces.iface[177] = Dummy()
Ifaces.iface[177].attr = []
Ifaces.iface[177].attr.insert(0, None)
Ifaces.iface[177].attr[0] = 'online'
Ifaces.iface[177].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[177].callbackSubscriable = false
Ifaces.iface[177].defaultCallback = ''
Ifaces.iface[177].ifacename = 'IReferralRecruitOnlineStatus'
Ifaces.iface[177].parent = []
Ifaces.iface.insert(178, None)
Ifaces.iface[178] = Dummy()
Ifaces.iface[178].attr = []
Ifaces.iface[178].attr.insert(0, None)
Ifaces.iface[178].attr[0] = 'checkPointComplete'
Ifaces.iface[178].attr.insert(1, None)
Ifaces.iface[178].attr[1] = 'checkPointAwardReady'
Ifaces.iface[178].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[178].callbackSubscriable = false
Ifaces.iface[178].defaultCallback = ''
Ifaces.iface[178].ifacename = 'IReferralRecruitTasks'
Ifaces.iface[178].parent = []
Ifaces.iface.insert(179, None)
Ifaces.iface[179] = Dummy()
Ifaces.iface[179].attr = []
Ifaces.iface[179].attr.insert(0, None)
Ifaces.iface[179].attr[0] = 'awards'
Ifaces.iface[179].attr.insert(1, None)
Ifaces.iface[179].attr[1] = 'description'
Ifaces.iface[179].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[179].callbackSubscriable = false
Ifaces.iface[179].defaultCallback = ''
Ifaces.iface[179].ifacename = 'IReferralCheckpointBonus'
Ifaces.iface[179].parent = []
Ifaces.iface.insert(180, None)
Ifaces.iface[180] = Dummy()
Ifaces.iface[180].attr = []
Ifaces.iface[180].attr.insert(0, None)
Ifaces.iface[180].attr[0] = 'accountID'
Ifaces.iface[180].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[180].callbackSubscriable = false
Ifaces.iface[180].defaultCallback = ''
Ifaces.iface[180].ifacename = 'IReferralCheckpointGetBonus'
Ifaces.iface[180].parent = []
Ifaces.iface.insert(181, None)
Ifaces.iface[181] = Dummy()
Ifaces.iface[181].attr = []
Ifaces.iface[181].attr.insert(0, None)
Ifaces.iface[181].attr[0] = 'allQuests'
Ifaces.iface[181].attr.insert(1, None)
Ifaces.iface[181].attr[1] = 'activeQuests'
Ifaces.iface[181].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[181].callbackSubscriable = false
Ifaces.iface[181].defaultCallback = ''
Ifaces.iface[181].ifacename = 'IReferralRecruiterQuests'
Ifaces.iface[181].parent = []
Ifaces.iface.insert(182, None)
Ifaces.iface[182] = Dummy()
Ifaces.iface[182].attr = []
Ifaces.iface[182].attr.insert(0, None)
Ifaces.iface[182].attr[0] = 'localeDescription'
Ifaces.iface[182].attr.insert(1, None)
Ifaces.iface[182].attr[1] = 'nextStageQuest'
Ifaces.iface[182].attr.insert(2, None)
Ifaces.iface[182].attr[2] = 'prevStageQuest'
Ifaces.iface[182].attr.insert(3, None)
Ifaces.iface[182].attr[3] = 'awards'
Ifaces.iface[182].attr.insert(4, None)
Ifaces.iface[182].attr[4] = 'maxProgress'
Ifaces.iface[182].attr.insert(5, None)
Ifaces.iface[182].attr[5] = 'taskType'
Ifaces.iface[182].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[182].callbackSubscriable = false
Ifaces.iface[182].defaultCallback = ''
Ifaces.iface[182].ifacename = 'IReferralQuestDescription'
Ifaces.iface[182].parent = []
Ifaces.iface.insert(183, None)
Ifaces.iface[183] = Dummy()
Ifaces.iface[183].attr = []
Ifaces.iface[183].attr.insert(0, None)
Ifaces.iface[183].attr[0] = 'progress'
Ifaces.iface[183].attr.insert(1, None)
Ifaces.iface[183].attr[1] = 'complete'
Ifaces.iface[183].attr.insert(2, None)
Ifaces.iface[183].attr[2] = 'waitGetAward'
Ifaces.iface[183].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[183].callbackSubscriable = false
Ifaces.iface[183].defaultCallback = ''
Ifaces.iface[183].ifacename = 'IReferralQuestStatus'
Ifaces.iface[183].parent = []
Ifaces.iface.insert(184, None)
Ifaces.iface[184] = Dummy()
Ifaces.iface[184].attr = []
Ifaces.iface[184].attr.insert(0, None)
Ifaces.iface[184].attr[0] = 'questID'
Ifaces.iface[184].cacheType = CACHE_TYPE.NONE
Ifaces.iface[184].callbackSubscriable = false
Ifaces.iface[184].defaultCallback = ''
Ifaces.iface[184].ifacename = 'IReferralQuestGetBonus'
Ifaces.iface[184].parent = []
Ifaces.iface.insert(185, None)
Ifaces.iface[185] = Dummy()
Ifaces.iface[185].attr = []
Ifaces.iface[185].attr.insert(0, None)
Ifaces.iface[185].attr[0] = 'progress'
Ifaces.iface[185].attr.insert(1, None)
Ifaces.iface[185].attr[1] = 'complete'
Ifaces.iface[185].attr.insert(2, None)
Ifaces.iface[185].attr[2] = 'waitGetAward'
Ifaces.iface[185].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[185].callbackSubscriable = false
Ifaces.iface[185].defaultCallback = ''
Ifaces.iface[185].ifacename = 'IReferralQuestStatus'
Ifaces.iface[185].parent = []
Ifaces.iface.insert(186, None)
Ifaces.iface[186] = Dummy()
Ifaces.iface[186].attr = []
Ifaces.iface[186].attr.insert(0, None)
Ifaces.iface[186].attr[0] = 'requestBody'
Ifaces.iface[186].attr.insert(1, None)
Ifaces.iface[186].attr[1] = 'window'
Ifaces.iface[186].attr.insert(2, None)
Ifaces.iface[186].attr[2] = 'callback'
Ifaces.iface[186].cacheType = CACHE_TYPE.NONE
Ifaces.iface[186].callbackSubscriable = false
Ifaces.iface[186].defaultCallback = ''
Ifaces.iface[186].ifacename = 'IClientPrediction'
Ifaces.iface[186].parent = []
Ifaces.iface.insert(187, None)
Ifaces.iface[187] = Dummy()
Ifaces.iface[187].attr = []
Ifaces.iface[187].attr.insert(0, None)
Ifaces.iface[187].attr[0] = 'email'
Ifaces.iface[187].attr.insert(1, None)
Ifaces.iface[187].attr[1] = 'message'
Ifaces.iface[187].cacheType = CACHE_TYPE.NONE
Ifaces.iface[187].callbackSubscriable = false
Ifaces.iface[187].defaultCallback = ''
Ifaces.iface[187].ifacename = 'IReferralSendInvite'
Ifaces.iface[187].parent = []
Ifaces.iface.insert(188, None)
Ifaces.iface[188] = Dummy()
Ifaces.iface[188].attr = []
Ifaces.iface[188].attr.insert(0, None)
Ifaces.iface[188].attr[0] = 'target'
Ifaces.iface[188].cacheType = CACHE_TYPE.NONE
Ifaces.iface[188].callbackSubscriable = false
Ifaces.iface[188].defaultCallback = ''
Ifaces.iface[188].ifacename = 'IReferralPublicInvite'
Ifaces.iface[188].parent = []
Ifaces.iface.insert(189, None)
Ifaces.iface[189] = Dummy()
Ifaces.iface[189].attr = []
Ifaces.iface[189].attr.insert(0, None)
Ifaces.iface[189].attr[0] = 'currentState'
Ifaces.iface[189].attr.insert(1, None)
Ifaces.iface[189].attr[1] = 'nextState'
Ifaces.iface[189].attr.insert(2, None)
Ifaces.iface[189].attr[2] = 'changeStateTime'
Ifaces.iface[189].attr.insert(3, None)
Ifaces.iface[189].attr[3] = 'warStartTime'
Ifaces.iface[189].attr.insert(4, None)
Ifaces.iface[189].attr[4] = 'peaceExtendTime'
Ifaces.iface[189].attr.insert(5, None)
Ifaces.iface[189].attr[5] = 'isFirst'
Ifaces.iface[189].attr.insert(6, None)
Ifaces.iface[189].attr[6] = 'warID'
Ifaces.iface[189].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[189].callbackSubscriable = false
Ifaces.iface[189].defaultCallback = ''
Ifaces.iface[189].ifacename = 'IWarActionState'
Ifaces.iface[189].parent = []
Ifaces.iface.insert(190, None)
Ifaces.iface[190] = Dummy()
Ifaces.iface[190].attr = []
Ifaces.iface[190].attr.insert(0, None)
Ifaces.iface[190].attr[0] = 'fraction'
Ifaces.iface[190].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[190].callbackSubscriable = false
Ifaces.iface[190].defaultCallback = ''
Ifaces.iface[190].ifacename = 'IWarActionFraction'
Ifaces.iface[190].parent = []
Ifaces.iface.insert(191, None)
Ifaces.iface[191] = Dummy()
Ifaces.iface[191].attr = []
Ifaces.iface[191].attr.insert(0, None)
Ifaces.iface[191].attr[0] = 'current'
Ifaces.iface[191].attr.insert(1, None)
Ifaces.iface[191].attr[1] = 'max'
Ifaces.iface[191].attr.insert(2, None)
Ifaces.iface[191].attr[2] = 'boostedFraction'
Ifaces.iface[191].cacheType = CACHE_TYPE.NONE
Ifaces.iface[191].callbackSubscriable = false
Ifaces.iface[191].defaultCallback = ''
Ifaces.iface[191].ifacename = 'IWarActionForce'
Ifaces.iface[191].parent = []
Ifaces.iface.insert(192, None)
Ifaces.iface[192] = Dummy()
Ifaces.iface[192].attr = []
Ifaces.iface[192].attr.insert(0, None)
Ifaces.iface[192].attr[0] = 'endAction'
Ifaces.iface[192].attr.insert(1, None)
Ifaces.iface[192].attr[1] = 'changeFractionPrice'
Ifaces.iface[192].attr.insert(2, None)
Ifaces.iface[192].attr[2] = 'planeLevels'
Ifaces.iface[192].attr.insert(3, None)
Ifaces.iface[192].attr[3] = 'nations'
Ifaces.iface[192].attr.insert(4, None)
Ifaces.iface[192].attr[4] = 'excludedPlanes'
Ifaces.iface[192].attr.insert(5, None)
Ifaces.iface[192].attr[5] = 'planesFromQuests'
Ifaces.iface[192].attr.insert(6, None)
Ifaces.iface[192].attr[6] = 'trophiesMultiplyForWin'
Ifaces.iface[192].attr.insert(7, None)
Ifaces.iface[192].attr[7] = 'warCashEnabledStates'
Ifaces.iface[192].attr.insert(8, None)
Ifaces.iface[192].attr[8] = 'warCashSlidePrizes'
Ifaces.iface[192].attr.insert(9, None)
Ifaces.iface[192].attr[9] = 'actionPlanes'
Ifaces.iface[192].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[192].callbackSubscriable = false
Ifaces.iface[192].defaultCallback = ''
Ifaces.iface[192].ifacename = 'IWarActionInfo'
Ifaces.iface[192].parent = []
Ifaces.iface.insert(193, None)
Ifaces.iface[193] = Dummy()
Ifaces.iface[193].attr = []
Ifaces.iface[193].attr.insert(0, None)
Ifaces.iface[193].attr[0] = 'fraction'
Ifaces.iface[193].attr.insert(1, None)
Ifaces.iface[193].attr[1] = 'battlesCount'
Ifaces.iface[193].attr.insert(2, None)
Ifaces.iface[193].attr[2] = 'wins'
Ifaces.iface[193].attr.insert(3, None)
Ifaces.iface[193].attr[3] = 'score'
Ifaces.iface[193].attr.insert(4, None)
Ifaces.iface[193].attr[4] = 'medalsHero'
Ifaces.iface[193].attr.insert(5, None)
Ifaces.iface[193].attr[5] = 'medalsEpic'
Ifaces.iface[193].attr.insert(6, None)
Ifaces.iface[193].attr[6] = 'winnerFraction'
Ifaces.iface[193].attr.insert(7, None)
Ifaces.iface[193].attr[7] = 'totalScore'
Ifaces.iface[193].attr.insert(8, None)
Ifaces.iface[193].attr[8] = 'trophies'
Ifaces.iface[193].attr.insert(9, None)
Ifaces.iface[193].attr[9] = 'isPlayedInAnyWar'
Ifaces.iface[193].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[193].callbackSubscriable = false
Ifaces.iface[193].defaultCallback = ''
Ifaces.iface[193].ifacename = 'IWarActionBattleStats'
Ifaces.iface[193].parent = []
Ifaces.iface.insert(194, None)
Ifaces.iface[194] = Dummy()
Ifaces.iface[194].attr = []
Ifaces.iface[194].attr.insert(0, None)
Ifaces.iface[194].attr[0] = 'battlesCount'
Ifaces.iface[194].attr.insert(1, None)
Ifaces.iface[194].attr[1] = 'wins'
Ifaces.iface[194].attr.insert(2, None)
Ifaces.iface[194].attr[2] = 'score'
Ifaces.iface[194].attr.insert(3, None)
Ifaces.iface[194].attr[3] = 'totalScore'
Ifaces.iface[194].attr.insert(4, None)
Ifaces.iface[194].attr[4] = 'medalsHero'
Ifaces.iface[194].attr.insert(5, None)
Ifaces.iface[194].attr[5] = 'medalsEpic'
Ifaces.iface[194].attr.insert(6, None)
Ifaces.iface[194].attr[6] = 'trophies'
Ifaces.iface[194].attr.insert(7, None)
Ifaces.iface[194].attr[7] = 'awards'
Ifaces.iface[194].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[194].callbackSubscriable = false
Ifaces.iface[194].defaultCallback = ''
Ifaces.iface[194].ifacename = 'IWarActionAgregatedBattleStats'
Ifaces.iface[194].parent = []
Ifaces.iface.insert(195, None)
Ifaces.iface[195] = Dummy()
Ifaces.iface[195].attr = []
Ifaces.iface[195].attr.insert(0, None)
Ifaces.iface[195].attr[0] = 'progress'
Ifaces.iface[195].attr.insert(1, None)
Ifaces.iface[195].attr[1] = 'maxProgress'
Ifaces.iface[195].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[195].callbackSubscriable = false
Ifaces.iface[195].defaultCallback = ''
Ifaces.iface[195].ifacename = 'IWarActionTrophiesStatus'
Ifaces.iface[195].parent = []
Ifaces.iface.insert(196, None)
Ifaces.iface[196] = Dummy()
Ifaces.iface[196].attr = []
Ifaces.iface[196].attr.insert(0, None)
Ifaces.iface[196].attr[0] = 'status'
Ifaces.iface[196].attr.insert(1, None)
Ifaces.iface[196].attr[1] = 'quests'
Ifaces.iface[196].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[196].callbackSubscriable = false
Ifaces.iface[196].defaultCallback = ''
Ifaces.iface[196].ifacename = 'IWarActionPlaneQuestStatus'
Ifaces.iface[196].parent = []
Ifaces.iface.insert(197, None)
Ifaces.iface[197] = Dummy()
Ifaces.iface[197].attr = []
Ifaces.iface[197].attr.insert(0, None)
Ifaces.iface[197].attr[0] = 'result'
Ifaces.iface[197].attr.insert(1, None)
Ifaces.iface[197].attr[1] = 'pricePerClick'
Ifaces.iface[197].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[197].callbackSubscriable = false
Ifaces.iface[197].defaultCallback = ''
Ifaces.iface[197].ifacename = 'IWarCash'
Ifaces.iface[197].parent = []
Ifaces.iface.insert(198, None)
Ifaces.iface[198] = Dummy()
Ifaces.iface[198].attr = []
Ifaces.iface[198].attr.insert(0, None)
Ifaces.iface[198].attr[0] = 'planeIDs'
Ifaces.iface[198].attr.insert(1, None)
Ifaces.iface[198].attr[1] = 'endTime'
Ifaces.iface[198].attr.insert(2, None)
Ifaces.iface[198].attr[2] = 'priceGold'
Ifaces.iface[198].attr.insert(3, None)
Ifaces.iface[198].attr[3] = 'priceCredits'
Ifaces.iface[198].attr.insert(4, None)
Ifaces.iface[198].attr[4] = 'priceTickets'
Ifaces.iface[198].attr.insert(5, None)
Ifaces.iface[198].attr[5] = 'packIDs'
Ifaces.iface[198].attr.insert(6, None)
Ifaces.iface[198].attr[6] = 'activePackID'
Ifaces.iface[198].attr.insert(7, None)
Ifaces.iface[198].attr[7] = 'enableActivePack'
Ifaces.iface[198].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[198].callbackSubscriable = false
Ifaces.iface[198].defaultCallback = ''
Ifaces.iface[198].ifacename = 'ILTOStatus'
Ifaces.iface[198].parent = []
Ifaces.iface.insert(199, None)
Ifaces.iface[199] = Dummy()
Ifaces.iface[199].attr = []
Ifaces.iface[199].attr.insert(0, None)
Ifaces.iface[199].attr[0] = 'lessons'
Ifaces.iface[199].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[199].callbackSubscriable = false
Ifaces.iface[199].defaultCallback = ''
Ifaces.iface[199].ifacename = 'ITutorialLessonList'
Ifaces.iface[199].parent = []
Ifaces.iface.insert(200, None)
Ifaces.iface[200] = Dummy()
Ifaces.iface[200].attr = []
Ifaces.iface[200].attr.insert(0, None)
Ifaces.iface[200].attr[0] = 'status'
Ifaces.iface[200].attr.insert(1, None)
Ifaces.iface[200].attr[1] = 'time'
Ifaces.iface[200].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[200].callbackSubscriable = false
Ifaces.iface[200].defaultCallback = ''
Ifaces.iface[200].ifacename = 'ITutorialLessonServer'
Ifaces.iface[200].parent = []
Ifaces.iface.insert(201, None)
Ifaces.iface[201] = Dummy()
Ifaces.iface[201].attr = []
Ifaces.iface[201].attr.insert(0, None)
Ifaces.iface[201].attr[0] = 'lessonNumber'
Ifaces.iface[201].attr.insert(1, None)
Ifaces.iface[201].attr[1] = 'lessonName'
Ifaces.iface[201].attr.insert(2, None)
Ifaces.iface[201].attr[2] = 'disabledTitle'
Ifaces.iface[201].attr.insert(3, None)
Ifaces.iface[201].attr[3] = 'rewardExp'
Ifaces.iface[201].attr.insert(4, None)
Ifaces.iface[201].attr[4] = 'rewardCreds'
Ifaces.iface[201].attr.insert(5, None)
Ifaces.iface[201].attr[5] = 'rewardGold'
Ifaces.iface[201].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[201].callbackSubscriable = false
Ifaces.iface[201].defaultCallback = ''
Ifaces.iface[201].ifacename = 'ITutorialLessonClient'
Ifaces.iface[201].parent = []
Ifaces.iface.insert(202, None)
Ifaces.iface[202] = Dummy()
Ifaces.iface[202].attr = []
Ifaces.iface[202].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[202].callbackSubscriable = false
Ifaces.iface[202].defaultCallback = ''
Ifaces.iface[202].ifacename = 'ITutorialLesson'
Ifaces.iface[202].parent = []
Ifaces.iface[202].parent.insert(0, None)
Ifaces.iface[202].parent[0] = 'ITutorialLessonServer'
Ifaces.iface[202].parent.insert(1, None)
Ifaces.iface[202].parent[1] = 'ITutorialLessonClient'
Ifaces.iface.insert(203, None)
Ifaces.iface[203] = Dummy()
Ifaces.iface[203].attr = []
Ifaces.iface[203].attr.insert(0, None)
Ifaces.iface[203].attr[0] = 'isBonus'
Ifaces.iface[203].attr.insert(1, None)
Ifaces.iface[203].attr[1] = 'nameReward'
Ifaces.iface[203].attr.insert(2, None)
Ifaces.iface[203].attr[2] = 'countCredits'
Ifaces.iface[203].attr.insert(3, None)
Ifaces.iface[203].attr[3] = 'nameCredits'
Ifaces.iface[203].attr.insert(4, None)
Ifaces.iface[203].attr[4] = 'countExperience'
Ifaces.iface[203].attr.insert(5, None)
Ifaces.iface[203].attr[5] = 'nameExperience'
Ifaces.iface[203].attr.insert(6, None)
Ifaces.iface[203].attr[6] = 'countGolds'
Ifaces.iface[203].attr.insert(7, None)
Ifaces.iface[203].attr[7] = 'nameGolds'
Ifaces.iface[203].attr.insert(8, None)
Ifaces.iface[203].attr[8] = 'title'
Ifaces.iface[203].attr.insert(9, None)
Ifaces.iface[203].attr[9] = 'titleCompleted'
Ifaces.iface[203].attr.insert(10, None)
Ifaces.iface[203].attr[10] = 'description1'
Ifaces.iface[203].attr.insert(11, None)
Ifaces.iface[203].attr[11] = 'description2'
Ifaces.iface[203].attr.insert(12, None)
Ifaces.iface[203].attr[12] = 'type'
Ifaces.iface[203].attr.insert(13, None)
Ifaces.iface[203].attr[13] = 'lessonIndex'
Ifaces.iface[203].attr.insert(14, None)
Ifaces.iface[203].attr[14] = 'isLastLesson'
Ifaces.iface[203].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[203].callbackSubscriable = false
Ifaces.iface[203].defaultCallback = ''
Ifaces.iface[203].ifacename = 'ITutorialPromptParams'
Ifaces.iface[203].parent = []
Ifaces.iface.insert(204, None)
Ifaces.iface[204] = Dummy()
Ifaces.iface[204].attr = []
Ifaces.iface[204].attr.insert(0, None)
Ifaces.iface[204].attr[0] = 'lessonID'
Ifaces.iface[204].cacheType = CACHE_TYPE.MEM_CACHE
Ifaces.iface[204].callbackSubscriable = false
Ifaces.iface[204].defaultCallback = ''
Ifaces.iface[204].ifacename = 'ITutorialLessonWindow'
Ifaces.iface[204].parent = []
Ifaces.iface.insert(205, None)
Ifaces.iface[205] = Dummy()
Ifaces.iface[205].attr = []
Ifaces.iface[205].attr.insert(0, None)
Ifaces.iface[205].attr[0] = 'attrs'
Ifaces.iface[205].attr.insert(1, None)
Ifaces.iface[205].attr[1] = 'command'
Ifaces.iface[205].attr.insert(2, None)
Ifaces.iface[205].attr[2] = 'result'
Ifaces.iface[205].cacheType = CACHE_TYPE.NONE
Ifaces.iface[205].callbackSubscriable = false
Ifaces.iface[205].defaultCallback = ''
Ifaces.iface[205].ifacename = 'IDebugCommand'
Ifaces.iface[205].parent = []
Ifaces.iface.insert(206, None)
Ifaces.iface[206] = Dummy()
Ifaces.iface[206].attr = []
Ifaces.iface[206].attr.insert(0, None)
Ifaces.iface[206].attr[0] = 'packItemsList'
Ifaces.iface[206].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[206].callbackSubscriable = false
Ifaces.iface[206].defaultCallback = ''
Ifaces.iface[206].ifacename = 'IPack'
Ifaces.iface[206].parent = []
Ifaces.iface[206].parent.insert(0, None)
Ifaces.iface[206].parent[0] = 'IStatus'
Ifaces.iface[206].parent.insert(1, None)
Ifaces.iface[206].parent[1] = 'IPrice'
Ifaces.iface.insert(207, None)
Ifaces.iface[207] = Dummy()
Ifaces.iface[207].attr = []
Ifaces.iface[207].attr.insert(0, None)
Ifaces.iface[207].attr[0] = 'packList'
Ifaces.iface[207].attr.insert(1, None)
Ifaces.iface[207].attr[1] = 'isAwarded'
Ifaces.iface[207].attr.insert(2, None)
Ifaces.iface[207].attr[2] = 'endDate'
Ifaces.iface[207].cacheType = CACHE_TYPE.FULL_CACHE
Ifaces.iface[207].callbackSubscriable = false
Ifaces.iface[207].defaultCallback = ''
Ifaces.iface[207].ifacename = 'IFemalePilotPackList'
Ifaces.iface[207].parent = []