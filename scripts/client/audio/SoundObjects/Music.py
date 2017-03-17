# Embedded file name: scripts/client/audio/SoundObjects/Music.py
from WwiseGameObject import WwiseGameObject, GS
import BigWorld
import db.DBLogic
from WWISE_ import setState
from audio.SoundBanksManager import SoundBanksManager
from consts import GAME_RESULT
import GameEnvironment
from audio.AKTunes import Common_Banks
from audio.AKConsts import SOUND_CASES
from debug_utils import LOG_DEBUG_DEV
from adapters.IHangarSpacesAdapter import getHangarSpaceByID

class Music(WwiseGameObject):

    def __init__(self):
        WwiseGameObject.__init__(self, 'MusicPlayer')
        self.__arenaSet = None
        self.__hangarSet = None
        self.__winner = None
        self.__hangarStopEvent = None
        self.__hangarMusicStopEvent = None
        self.__enemy = []
        self.__playedThemes = []
        self.__mainThemeWasPlayed = False
        self.__hangarSpace = None
        self.__soundBanksManager = SoundBanksManager.instance()
        for n in Common_Banks:
            self.__soundBanksManager.loadBank(n)

        return

    def playHangar(self, _, space):
        GS().onConnected()
        self.__hangarSet = db.DBLogic.g_instance.getHangarSoundSet()
        self.__hangarSpace = getHangarSpaceByID(space)
        self.start()

    def start(self):
        if self.__hangarSpace is None:
            return
        else:
            spaceName = self.__hangarSpace['spaceID'].lower()
            bank_tag = 'HangarSpaceID_' + spaceName
            if bank_tag in self.__hangarSet:
                bank = self.__hangarSet[bank_tag]
                if bank not in self.__hangar_ld:
                    loadBank(bank)
                    self.__hangar_ld.append(bank)
            isHoliday = spaceName.rfind('ny') >= 0 or spaceName.rfind('23feb') >= 0 or spaceName.rfind('april') >= 0
            if self.__hangarSpace['hangarType'] == 'premium':
                if isHoliday:
                    tag = 'HangarHolidayVIP'
                else:
                    tag = 'HangarVIP'
            elif isHoliday:
                tag = 'HangarHoliday'
            else:
                tag = 'HangarMain'
            ambient = self.__hangarSpace.get('ambient', None)
            if ambient:
                rtpc = ambient.get('rtpc')
                if rtpc:
                    self.setRTPC('RTPC_{0}'.format(rtpc['name']), rtpc['value'])
                event = 'Play_{0}'.format(ambient['name'])
                self.__soundBanksManager.prepareEvent(event, self.__soundBanksManager.PREPARATION_LOAD)
                self.__soundBanksManager.attachWwiseObjectToCase(event, SOUND_CASES.HANGAR)
                self.postEvent(event)
            if tag in self.__hangarSet:
                if ambient:
                    self.__hangarStopEvent = 'Stop_{0}'.format(ambient['name'])
                else:
                    LOG_DEBUG_DEV('play ambient', tag, self.__hangarSet[tag])
                    self.__soundBanksManager.prepareEvent(self.__hangarSet[tag], self.__soundBanksManager.PREPARATION_LOAD)
                    self.__soundBanksManager.attachWwiseObjectToCase(self.__hangarSet[tag], SOUND_CASES.HANGAR)
                    self.postEvent(self.__hangarSet[tag])
                    self.__hangarStopEvent = str(self.__hangarSet[tag]).replace('Play_', 'Stop_')
            if self.__winner == None:
                music = self.__hangarSpace.get('music', None)
                if spaceName.rfind('april') >= 0:
                    tag = 'AprilTheme'
                elif music:
                    tag = music['play']
                    if tag not in self.__playedThemes:
                        self.__playedThemes.append(tag)
                        self.__mainThemeWasPlayed = False
                else:
                    tag = 'HangarMusicMainTheme'
                LOG_DEBUG_DEV('play music', tag, self.__hangarSet[tag], self.__mainThemeWasPlayed)
                if tag in self.__hangarSet and not self.__mainThemeWasPlayed:
                    self.__soundBanksManager.prepareEvent(self.__hangarSet[tag], self.__soundBanksManager.PREPARATION_LOAD)
                    self.__soundBanksManager.attachWwiseObjectToCase(self.__hangarSet[tag], SOUND_CASES.HANGAR)
                    self.postEvent(self.__hangarSet[tag])
                    self.__hangarMusicStopEvent = music['stop'] if music and 'stop' in music else str(self.__hangarSet[tag]).replace('Play_', 'Stop_')
                    self.__mainThemeWasPlayed = True
            elif self.__winner:
                self.__playWinnerTheme()
            return

    def stopHangar(self):
        if GS().isDisconnected:
            self.postEvent(self.__hangarStopEvent + '_loginscreen')
            self.postEvent(self.__hangarMusicStopEvent + '_loginscreen')
        else:
            self.postEvent(self.__hangarStopEvent)
            self.postEvent(self.__hangarMusicStopEvent)

    def playArena(self):
        mapname = db.DBLogic.g_instance.getArenaData(BigWorld.player().arenaType).name
        ambient = db.DBLogic.g_instance.getAmbient(mapname)
        self.__arenaSet = ambient
        self.__enemy = []
        setState('STATE_Music_Map_Theme', 'Map_Music_Overture')
        setState('STATE_Music_Map_Superiority', 'None')
        BigWorld.player().eReportDestruction += self.__playVictimDestroyed
        BigWorld.player().eLeaveWorldEvent += self.stopArena
        GameEnvironment.getClientArena().onGameResultChanged += self.__onGameResultChanged
        for e in ['AmbientEvent', 'MusicEvent']:
            if e in self.__arenaSet:
                self.__soundBanksManager.prepareEvent(self.__arenaSet[e], self.__soundBanksManager.PREPARATION_LOAD)
                self.__soundBanksManager.attachWwiseObjectToCase(self.__arenaSet[e], SOUND_CASES.ARENA)
                self.postEvent(self.__arenaSet[e])

    def stopArena(self):
        if not self.__arenaSet:
            return
        else:
            self.postEvent(str(self.__arenaSet['MusicEvent']).replace('Play_', 'Stop_'), GS().unloadArena)
            self.__arenaSet = None
            self.postEvent('Stop_all_environment')
            return

    def playBattle(self, ownScore, enemyScore):
        musicState = 'Superiority_Neutral'
        if ownScore > enemyScore:
            musicState = 'Superiority_Positive'
        elif ownScore < enemyScore:
            musicState = 'Superiority_Negative'
        setState('STATE_Music_Map_Superiority', musicState)

    def startBattle(self, eid):
        if eid in self.__enemy:
            return
        if len(self.__enemy) == 0:
            setState('STATE_Music_Map_Theme', 'Map_Music_Battle')
        self.__enemy.append(eid)

    def endBattle(self, eid):
        if eid not in self.__enemy:
            return
        self.__enemy.remove(eid)
        if len(self.__enemy) == 0:
            setState('STATE_Music_Map_Theme', 'Map_Music_Overture')

    def playTeamObjectDestroyed(self, killerID, objectTeamIndex):
        player = BigWorld.player()
        if killerID == player.id and player.teamIndex != objectTeamIndex:
            self.trigger('Stinger_Positive')

    def __playVictimDestroyed(self, killingInfo):
        player = BigWorld.player()
        victimID = killingInfo['victimID']
        killerID = killingInfo['killerID']
        stinger = 'Stinger_Negative'
        if victimID != player.id:
            victimData = GameEnvironment.getClientArena().getAvatarInfo(victimID)
            if victimData:
                victimPlayerTeamIndex = victimData['teamIndex']
                if victimPlayerTeamIndex != player.teamIndex and killerID == player.id:
                    stinger = 'Stinger_Positive'
                else:
                    return
        self.trigger(stinger)

    def __playWinnerTheme(self):
        tag = 'HangarMusicWinnerTheme'
        if tag in self.__hangarSet:
            self.__soundBanksManager.prepareEvent(self.__hangarSet[tag], self.__soundBanksManager.PREPARATION_LOAD)
            self.__soundBanksManager.attachWwiseObjectToCase(self.__hangarSet[tag], SOUND_CASES.HANGAR)
            self.postEvent(self.__hangarSet[tag])
            self.__hangarMusicStopEvent = str(self.__hangarSet[tag]).replace('Play_', 'Stop_')
            self.__winner = False

    def __onGameResultChanged(self, gameResult, winState):
        winResults = [GAME_RESULT.SUPERIORITY_SUCCESS, GAME_RESULT.ELIMINATION]
        self.__winner = gameResult in winResults and BigWorld.player().teamIndex == winState
        if not self.__winner:
            self.trigger('Stinger_Negative')
        else:
            self.trigger('Stinger_Positive')