# Embedded file name: scripts/client/gui/Scaleform/HUD/LeaderManager.py
__author__ = 's_karchavets'
import GameEnvironment
import BigWorld
from consts import MESSAGE_TYPE
from Helpers.i18n import localizeHUD
from gui.Scaleform.UIHelper import SQUAD_TYPES, getPlayerNameWithClan
from debug_utils import LOG_ERROR

class LEADER_TYPES:
    AVATAR = 1
    TEAM_OBJECT = 2
    LOST = 3


class LEADERS_TYPES_CHAT_FLASH_EMUN:
    PLANE_ALLY = 1
    PLANE_ENEMY = 2
    PLANE_SQUAD = 3
    TEAM_OBJECT_ALLY = 4
    TEAM_OBJECT_ENEMY = 5
    TEAM_OBJECT_SQUAD = 6


LEADERS_TYPES_CHAT = {LEADER_TYPES.AVATAR: [LEADERS_TYPES_CHAT_FLASH_EMUN.PLANE_SQUAD, LEADERS_TYPES_CHAT_FLASH_EMUN.PLANE_ALLY, LEADERS_TYPES_CHAT_FLASH_EMUN.PLANE_ENEMY],
 LEADER_TYPES.TEAM_OBJECT: [LEADERS_TYPES_CHAT_FLASH_EMUN.TEAM_OBJECT_SQUAD, LEADERS_TYPES_CHAT_FLASH_EMUN.TEAM_OBJECT_ALLY, LEADERS_TYPES_CHAT_FLASH_EMUN.TEAM_OBJECT_ENEMY]}
KEYS_STATS = {LEADER_TYPES.AVATAR: 'frags',
 LEADER_TYPES.TEAM_OBJECT: 'fragsTeamObjects'}
CHAT_MSG = {LEADER_TYPES.AVATAR: ('HUD_MESSAGE_FRAG_LEAD_TEAM', 'HUD_MESSAGE_FRAG_LEAD_TEAM_EXTRA', 'HUD_MESSAGE_LEADER_KILL_PLANES', 'HUD_MESSAGE_FRAG_LEAD_UPDATED'),
 LEADER_TYPES.TEAM_OBJECT: ('HUD_MESSAGE_OBJECT_LEAD_TEAM', 'HUD_MESSAGE_OBJECT_LEAD_TEAM_EXTRA', 'HUD_MESSAGE_LEADER_KILL_OBJECTS', 'HUD_MESSAGE_OBJECT_LEAD_UPDATED')}
MAIN_MSG = {LEADER_TYPES.AVATAR: ('HUD_MESSAGE_FRAG_LEAD_TAKEN', 'HUD_MESSAGE_FRAG_LEAD_LOST'),
 LEADER_TYPES.TEAM_OBJECT: ('HUD_MESSAGE_OBJECT_LEAD_TAKEN', 'HUD_MESSAGE_OBJECT_LEAD_LOST')}

class LeaderManagerBase:

    def __init__(self, type, uiOwner, chat):
        self._currentLeaderID = 0
        self._currentLeaderFrags = 0
        self._chatOwner = chat
        self._uiOwner = uiOwner
        self._type = type

    def checkDead(self, victimID):
        if self._currentLeaderID == victimID:
            self._chatOwner.showTextMessage(BigWorld.player().id, MESSAGE_TYPE.BATTLE_NEUTRAL, 0, 0, localizeHUD(CHAT_MSG[self._type][2]), False)

    def _getLeaderType(self, ID, teamIndex):
        squadType = SQUAD_TYPES().getSquadType(SQUAD_TYPES().getSquadIDbyAvatarID(ID), ID)
        if squadType == SQUAD_TYPES.OWN:
            leaderType = LEADERS_TYPES_CHAT[self._type][0]
        elif teamIndex == BigWorld.player().teamIndex:
            leaderType = LEADERS_TYPES_CHAT[self._type][1]
        else:
            leaderType = LEADERS_TYPES_CHAT[self._type][2]
        return leaderType

    def check(self):
        ID, leaderFrags, playerName, clanAbbrev, teamIndex = self._getNewLeaderID()
        if ID:
            if not self._currentLeaderID:
                if ID == BigWorld.player().id:
                    self._uiOwner.call_1('hud.updateLeaderInfo', self._type, localizeHUD(MAIN_MSG[self._type][0]))
                else:
                    self._chatOwner.showTextMessage(ID, MESSAGE_TYPE.BATTLE_NEUTRAL, 0, 0, localizeHUD(CHAT_MSG[self._type][0]).format(value=leaderFrags), False, self._getLeaderType(ID, teamIndex))
                self._uiOwner.call_1('hud.playerListUpdateLeader', ID, self._type)
                self._currentLeaderFrags = leaderFrags
                self._currentLeaderID = ID
            elif self._currentLeaderID == ID:
                if leaderFrags > self._currentLeaderFrags:
                    if ID == BigWorld.player().id:
                        text = localizeHUD(CHAT_MSG[self._type][3]).format(value=leaderFrags)
                    else:
                        text = localizeHUD(CHAT_MSG[self._type][1]).format(value=leaderFrags)
                    self._chatOwner.showTextMessage(ID, MESSAGE_TYPE.BATTLE_NEUTRAL, 0, 0, text, False, self._getLeaderType(ID, teamIndex))
                    self._currentLeaderFrags = leaderFrags
            elif leaderFrags > self._currentLeaderFrags:
                if ID == BigWorld.player().id:
                    self._uiOwner.call_1('hud.updateLeaderInfo', self._type, localizeHUD(MAIN_MSG[self._type][0]))
                elif self._currentLeaderID == BigWorld.player().id:
                    self._uiOwner.call_1('hud.updateLeaderInfo', LEADER_TYPES.LOST, localizeHUD(MAIN_MSG[self._type][1]).format(player_name=getPlayerNameWithClan(playerName, clanAbbrev)))
                self._uiOwner.call_1('hud.playerListUpdateLeader', ID, self._type)
                self._currentLeaderFrags = leaderFrags
                self._currentLeaderID = ID

    def _getNewLeaderID(self):
        leaderID = 0
        leaderFrags = 0
        playerName = ''
        clanAbbrev = ''
        teamIndex = -1
        for avatarID, avatarInfo in GameEnvironment.getClientArena().avatarInfos.iteritems():
            frags = avatarInfo['stats'][KEYS_STATS.get(self._type)]
            if frags > leaderFrags:
                leaderFrags = frags
                leaderID = avatarID
                playerName = avatarInfo['playerName']
                clanAbbrev = avatarInfo['clanAbbrev']
                teamIndex = avatarInfo['teamIndex']

        return (leaderID,
         leaderFrags,
         playerName,
         clanAbbrev,
         teamIndex)

    def destroy(self):
        self._chatOwner = None
        self._uiOwner = None
        return


class LeaderManager:

    def __init__(self):
        self.__leaders = dict()

    def initialized(self, uiOwner, chat):
        self.__leaders = {LEADER_TYPES.AVATAR: _LeaderEntityManager(LEADER_TYPES.AVATAR, uiOwner, chat),
         LEADER_TYPES.TEAM_OBJECT: _LeaderEntityManager(LEADER_TYPES.TEAM_OBJECT, uiOwner, chat)}

    def destroy(self):
        for leader in self.__leaders.itervalues():
            leader.destroy()

        self.__leaders.clear()

    def check(self):
        for leader in self.__leaders.itervalues():
            leader.check()

    def checkDead(self, victimID):
        for leader in self.__leaders.itervalues():
            leader.checkDead(victimID)


class _LeaderEntityManager(LeaderManagerBase):

    def __init__(self, type, uiOwner, chat):
        LeaderManagerBase.__init__(self, type, uiOwner, chat)