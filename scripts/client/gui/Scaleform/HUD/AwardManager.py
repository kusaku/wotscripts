# Embedded file name: scripts/client/gui/Scaleform/HUD/AwardManager.py
__author__ = 's_karchavets'
from gui.HudElements.IngameChat import COLORS
from Helpers.i18n import localizeAchievements, localizeHUD, localizeLobby
from _awards_data import ACHIEVE_GROUP_TYPE as ACHIEVE_GROUPS, QUEST_TYPE
import _awards_data
import BigWorld
from consts import MESSAGE_TYPE, IS_CLIENT, IS_EDITOR
import GameEnvironment
from Helpers.i18n import LOG_DEBUG, LOG_WARNING
from gui.Scaleform.UIHelper import SQUAD_TYPES
import Settings
from audio import GameSound
_AWARD_UPDATE_TIME = 5.0
_AWARD_WAIT_TIME = 5.0
_AWARD_ADD_TIME = 2.0
_AWARD_LOCALIZE_ID = ('UI_MESSAGE_YOU_GET_ACHIEVEMENT', 'UI_MESSAGE_PLAYER_GETS_ACHIEVEMENT')

class _AwardVO:

    def __init__(self, text, icoPath, type = QUEST_TYPE.NONE):
        self.text = text
        self.icoPath = icoPath
        self.type = type


class AwardManager:

    def __init__(self):
        self.__queue = list()
        self.__uiOwner = None
        self.__chatOwner = None
        self.__enabled = False
        self.__updateCallback = None
        self.__isFired = False
        return

    def initialized(self, uiOwner, chat):
        self.__uiOwner = uiOwner
        self.__chatOwner = chat

    def setEnabled(self, isEnable):
        self.__enabled = isEnable
        if self.__updateCallback is None:
            self.__updateCallback = BigWorld.callback(_AWARD_WAIT_TIME, self.__update)
        return

    def destroy(self):
        self.__uiOwner = None
        self.__chatOwner = None
        self.__clearCallback()
        return

    def add(self, awardInfo):
        self.__queue.insert(0, awardInfo)
        if self.__updateCallback is None:
            self.__updateCallback = BigWorld.callback(_AWARD_ADD_TIME, self.__update)
        return

    def __clearCallback(self):
        if self.__updateCallback is not None:
            BigWorld.cancelCallback(self.__updateCallback)
            self.__updateCallback = None
        return

    def __popAwardByPriority(self):
        priorAward = None
        for awardInfo in self.__queue:
            avatarID, isRibbon, award_id, MaxProgress = awardInfo
            awardData = _awards_data.AwardsDB[award_id]
            award_type = awardData.options.quest
            if award_type == QUEST_TYPE.MAIN_QUEST:
                priorAward = awardInfo
                break
            elif award_type == QUEST_TYPE.CHILD_QUEST:
                priorAward = awardInfo

        if priorAward:
            self.__queue.remove(priorAward)
            return priorAward
        else:
            return self.__queue.pop()

    def __update(self):
        if self.__enabled:
            if self.__queue:
                if not self.__isFired:
                    awardInfo = self.__popAwardByPriority()
                    self.__checkSameAwards(awardInfo)
                    self.__fire(awardInfo)
                    self.__isFired = True
                    self.__updateCallback = BigWorld.callback(_AWARD_UPDATE_TIME, self.__stopFired)
            else:
                self.__clearCallback()
        else:
            self.__clearCallback()

    def __stopFired(self):
        self.__isFired = False
        if self.__queue:
            self.__update()
        else:
            self.__clearCallback()

    def __checkSameAwards(self, _awardInfo):
        _avatarID, _isRibbon, _award_id, _MaxProgress = _awardInfo
        if _avatarID != BigWorld.player().id:
            return
        groups = list()
        for i, awardInfo in enumerate(self.__queue):
            avatarID, isRibbon, award_id, MaxProgress = awardInfo
            if avatarID == _avatarID and isRibbon == _isRibbon and award_id == _award_id and not (isRibbon and not MaxProgress):
                groups.append(i)

        self.__queue = [ awardInfo for i, awardInfo in enumerate(self.__queue) if i not in groups ]

    def __fire(self, awardInfo):
        player = BigWorld.player()
        LOG_DEBUG('__fire - try to show award:', player.id, awardInfo)
        avatarID, isRibbon, award_id, MaxProgress = awardInfo
        if isRibbon and not MaxProgress:
            LOG_DEBUG('__fire - ribbons has no progress:', isRibbon, MaxProgress)
            return
        else:
            awardData = _awards_data.AwardsDB[award_id]
            award_tag = awardData.ui.localizeTag
            award_group = awardData.ui.group
            award_icoPath = awardData.ui.icoPath
            award_type = awardData.options.quest
            award_str = localizeAchievements('MEDAL_NAME_{0}'.format(award_tag))
            isComplexQuest = award_type in (QUEST_TYPE.MAIN_QUEST, QUEST_TYPE.CHILD_QUEST)
            if isComplexQuest:
                import BWPersonality
                questSelected = BWPersonality.g_questSelected
                if questSelected:
                    for qId, qData in questSelected.quests.iteritems():
                        if qData.isMain:
                            if qData.name.isupper():
                                award_str = localizeLobby(qData.name)
                            else:
                                award_str = qData.name
                            break

            msg = None
            msgLocID = _AWARD_LOCALIZE_ID
            color = 0
            if msgLocID is not None:
                if player.id == avatarID:
                    if not isComplexQuest:
                        msg = localizeHUD(msgLocID[0]).format(achievement_name=award_str, msg_color1=str('%x' % COLORS.WHITE))
                    LOG_DEBUG('hud.showAward', award_str, award_icoPath, award_type)
                    self.__uiOwner.call_1('hud.showAward', _AwardVO(award_str, award_icoPath, award_type))
                    GameSound().ui.play('UISoundAchievement')
                elif award_group in (ACHIEVE_GROUPS.EPIC, ACHIEVE_GROUPS.HERO, ACHIEVE_GROUPS.GROUP) and not isComplexQuest:
                    avatarInfo = GameEnvironment.getClientArena().getAvatarInfo(avatarID)
                    if avatarInfo is not None:
                        if avatarInfo['teamIndex'] != player.teamIndex:
                            color = str('%x' % COLORS.PURPLE) if Settings.g_instance.getGameUI()['alternativeColorMode'] else str('%x' % COLORS.RED)
                        else:
                            squadType = SQUAD_TYPES.getSquadType(SQUAD_TYPES.getSquadIDbyAvatarID(avatarID), avatarID)
                            color = str('%x' % COLORS.YELLOW) if squadType == SQUAD_TYPES.OWN else str('%x' % COLORS.GREEN)
                        msg = localizeHUD(msgLocID[1]).format(achievement_name=award_str, user_name=avatarInfo['playerName'], msg_color1=color, msg_color2=str('%x' % COLORS.WHITE))
                    else:
                        LOG_WARNING('__fire - avatarInfo is None', award_group)
                else:
                    LOG_DEBUG('__fire - award disabled for show', award_group)
            if msg is not None:
                self.__chatOwner.showTextMessage(avatarID, MESSAGE_TYPE.BATTLE_NEUTRAL_UNIVERSAL, 0, 0, msg, False, -1, True)
            return