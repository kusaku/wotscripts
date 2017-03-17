# Embedded file name: scripts/client/audio/SoundObjects/Voiceover.py
from WwiseGameObject import WwiseGameObject, GS
import BigWorld
import db.DBLogic
from audio.SoundBanksManager import SoundBanksManager
from consts import GAME_MODE, DAMAGE_REASON
import Settings
from clientConsts import CLASTERS
from EntityHelpers import EntityStates
from EntityHelpers import extractGameMode
from audio.AKConsts import PartState, PART_STATE_SPEECH
from debug_utils import LOG_TRACE
from audio.AKConsts import SOUND_CASES

class Voiceover(WwiseGameObject):
    PRIORITY_DISCARD = 0
    PRIORITY_ENQUEUE = 1

    def __init__(self):
        self.__started = {}
        self.__state = 'None'
        self.__gameMsgs = False
        self.__enablePartSpeech = True
        self.__prevPartState = {}
        self.__deferredPlay = []
        self.__cb = None
        self.__soundBanksManager = SoundBanksManager.instance()
        BigWorld.player().eArenaLoaded += self.__onRespawn
        BigWorld.player().eRespawn += self.__onRespawn
        BigWorld.player().eEnterWorldEvent += self.__onEnterWorld
        BigWorld.player().eLeaveWorldEvent += self.__onLeaveWorld
        BigWorld.player().eUpdateSpectator += self.__onUpdateSpectator
        BigWorld.player().onStateChanged += self.__onStateChanged
        GS().eOnBattleStart += self.__onBattleStart
        GS().eOnBattleEnd += self.__onBattleEnd
        WwiseGameObject.__init__(self, 'Voiceover')
        return

    def load(self):
        import BWPersonality
        gamesPlayed = BWPersonality.g_gamesPlayed
        self.__detailed = gamesPlayed < db.DBLogic.g_instance.getVO().battles
        name = 'voiceovers_{0}.bnk'.format('long' if self.__detailed else 'short')
        self.__soundBanksManager.loadBank(name)
        self.__soundBanksManager.attachWwiseObjectToCase(name, SOUND_CASES.VOICEOVER)
        self.__gameMsgs = True
        gm = extractGameMode(BigWorld.player().gameMode)
        if gm is not GAME_MODE.GM_TUTORIAL:
            return
        self.__soundBanksManager.loadBank('voiceovers_tutorials.bnk')
        self.__soundBanksManager.attachWwiseObjectToCase('voiceovers_tutorials.bnk', SOUND_CASES.VOICEOVER)
        self.__gameMsgs = False

    def enableGameMsgs(self, enable):
        self.__gameMsgs = enable

    def play(self, name, delay = 0.0):
        playInTutorialMsgs = ['voice_engine_overheated',
         'voice_gun_overheated',
         'voice_nosedive_danger',
         'voice_stalling_danger']
        if not self.__gameMsgs and name not in playInTutorialMsgs:
            return
        elif name == 'voice_plane_destroyed' and CLASTERS.CN == Settings.g_instance.clusterID:
            return
        elif GS().isReplayMute:
            LOG_TRACE('[Audio].VO: skipped {0} in replay'.format(name))
            return
        elif self.__state == 'Phase_05_Battle_Ended':
            return
        else:
            VO = db.DBLogic.g_instance.getVO()
            voice = VO.gameplay(name)
            if not voice:
                LOG_TRACE('[Audio].VO: skipped {0}'.format(name))
                return
            if name in self.__started:
                if BigWorld.time() < self.__started[name]:
                    return
                self.__started.pop(name)
            prio = voice.get('VOPriority', None)
            gpMsg = prio != None
            if gpMsg and prio == Voiceover.PRIORITY_DISCARD and self.playing:
                return
            ev = voice['VODialogueEvent']
            self.dialogue(ev, VO.soundOn, VO.soundOff, VO.noise, VO.spawnDelay + delay, self.__state if gpMsg else '', 'Long' if self.__detailed else 'Short', prio if gpMsg else Voiceover.PRIORITY_ENQUEUE)
            self.__started[name] = BigWorld.time() + voice['VOCooldown'] if gpMsg else 0
            return

    def playTutorial(self, name):
        if self.__gameMsgs:
            return self.play(name)
        VO = db.DBLogic.g_instance.getVO()
        voice = VO.tutorial(name)
        if not voice:
            return
        ev = voice['VODialogueEvent']
        self.dialogue(ev, VO.soundOn, VO.soundOff, VO.noise, 0, '', '', 1)

    def stopTutorial(self):
        if self.__gameMsgs:
            return
        self.stopDynSeq()

    def playPartStateSpeech(self, partName, stateID, damageReason):
        dmgReasons = [DAMAGE_REASON.DESTRUCTION, DAMAGE_REASON.ROCKET_EXPLOSION, DAMAGE_REASON.BOMB_EXPLOSION]
        if damageReason in dmgReasons:
            return
        elif self.__state == 'Phase_03_Avatar_Is_Dead':
            return
        elif self.__state == 'Phase_05_Battle_Ended':
            return
        else:
            if partName not in self.__prevPartState:
                self.__prevPartState[partName] = PartState.Normal
            prevPartState = self.__prevPartState[partName]
            if stateID > prevPartState:
                partStateInfo = PART_STATE_SPEECH.get(partName, None)
                if partStateInfo and stateID in partStateInfo:
                    self.__deferredPlay.append(partStateInfo[stateID])
                    if not self.__cb:
                        self.__cb = BigWorld.callback(0.5, self.__playDeferred)
            if stateID == PartState.Repaired:
                self.__prevPartState[partName] = PartState.Normal
            else:
                self.__prevPartState[partName] = stateID
            return

    def __playDeferred(self):
        for i in self.__deferredPlay:
            self.play(i)

        self.__deferredPlay = []
        self.__cb = None
        return

    def __clearDeferred(self):
        if self.__cb:
            BigWorld.cancelCallback(self.__cb)
            self.__cb = None
        self.__deferredPlay = []
        return

    def __onEnterWorld(self):
        self.__clearDeferred()
        self.__state = 'Phase_01_Battle_Loading'

    def __onStateChanged(self, oldState, state):
        if state & EntityStates.DEAD and self.__state != 'Phase_03_Avatar_Is_Dead':
            self.__state = 'Phase_03_Avatar_Is_Dead'
            self.clearDynSeq()
            self.play('voice_plane_destroyed')

    def __onUpdateSpectator(self, target):
        self.__state = 'Phase_04_Player_Spectates'

    def __onRespawn(self):
        self.__state = 'Phase_01_Battle_Loading'
        self.__prevPartState = {}
        self.__clearDeferred()

    def __onLeaveWorld(self):
        self.stopDynSeq()
        self.__state = 'None'
        self.__soundBanksManager.unloadSoundCase(SOUND_CASES.VOICEOVER)
        self.__clearDeferred()

    def __onBattleStart(self):
        self.__state = 'Phase_02_Battle_Started'
        self.play('voice_battle_start')

    def __onBattleEnd(self):
        if GS().isWinner:
            self.clearDynSeq()
            self.play('voice_battle_win')
        self.__state = 'Phase_05_Battle_Ended'