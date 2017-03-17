# Embedded file name: scripts/client/audio/InteractiveMix/GamePhases.py
import db.DBLogic
import WWISE_
import BigWorld
from EntityHelpers import EntityStates
import GameEnvironment
import GlobalEvents
import audio.debug

class SOUND_PHASES:
    HANGAR = 'Hangar'
    SCREEN = 'Screen'
    SCENE = 'Scene'
    PILOTING = 'Piloting'
    DOGFIGHT = 'Dogfight'
    BOMBING = 'Bombing'
    NOSEDIVING = 'Nosediving'
    SPECTATOR = 'Spectator'
    RESULT_SCREEN = 'ResultScreen'


class FLAG:
    NONE = 0
    RESPAWN = 1
    LEAVE_WORLD = 2


class GamePhases:
    LOCAL_STATES = 'LocalStatesContainer'
    GLOBAL_STATE = 'GP_GlobalPhase'

    def __init__(self):
        self.__gamePhasesDB = db.DBLogic.g_instance.getInteractiveMixParameters().gamePhases
        self.__currentGlobalState = None
        self.__currentLocalContainer = None
        self.__currentLocalState = None
        self.__currentSoundPhase = None
        self.__registerGlobalEvents()
        return

    def __registerGlobalEvents(self):
        GlobalEvents.onMovieLoaded += self.__onMovieLoaded

    def __registerBattleEvents(self):
        player = BigWorld.player()
        player.onStateChanged += self.__onPlayerStateChanged
        player.onAvatarEnterWorldEvent += self.__onAvatarEnterWorld
        player.onAvatarLeaveWorldEvent += self.__onAvatarLeaveWorld
        player.eUpdateSpectator += self.__onSpectator
        player.onHUDBattleLoadingClosedEvent += self.__onHUDBattleLoadingClosed
        player.eRespawn += self.__onPlayerRespawn

    def __onMovieLoaded(self, movieName, movieInstance):
        if movieName == 'ui':
            self.__setGamePhase(SOUND_PHASES.SCREEN)
            self.__registerBattleEvents()
        elif movieName == 'lobby':
            self.__setGamePhase(SOUND_PHASES.HANGAR)

    def __onPlayerStateChanged(self, oldState, state):
        if state == EntityStates.GAME:
            self.__setGamePhase(self.__getFightPhase())
        elif state == EntityStates.DESTROYED_FALL or state == EntityStates.DESTROYED:
            self.__setGamePhase(SOUND_PHASES.NOSEDIVING)
        elif state == EntityStates.OUTRO:
            self.__setGamePhase(SOUND_PHASES.RESULT_SCREEN)

    def __onAvatarEnterWorld(self, avatarID):
        BigWorld.entities.get(avatarID).eOnAvatarStateChanged += self.__onAvatarStateChanged
        self.__setGamePhase(self.__getFightPhase())

    def __onAvatarStateChanged(self, avatarID, oldState, state):
        if (state == EntityStates.DESTROYED_FALL or state == EntityStates.DESTROYED) and oldState != state:
            self.__setGamePhase(self.__getFightPhase(FLAG.LEAVE_WORLD))

    def __onAvatarLeaveWorld(self, player, avatarID):
        self.__setGamePhase(self.__getFightPhase(FLAG.LEAVE_WORLD))

    def __onSpectator(self, avatarID):
        self.__setGamePhase(SOUND_PHASES.SPECTATOR)

    def __onHUDBattleLoadingClosed(self):
        self.__setGamePhase(SOUND_PHASES.SCENE)

    def __onPlayerRespawn(self):
        if BigWorld.player().state != EntityStates.WAIT_START:
            self.__setGamePhase(self.__getFightPhase(FLAG.RESPAWN))

    def __getFightPhase(self, flag = FLAG.NONE):
        if self.__currentSoundPhase == SOUND_PHASES.SPECTATOR or self.__currentSoundPhase == SOUND_PHASES.RESULT_SCREEN or self.__currentSoundPhase == SOUND_PHASES.NOSEDIVING and not flag == FLAG.RESPAWN:
            return
        phase = SOUND_PHASES.PILOTING
        player = BigWorld.player()
        visibleAvatars = player.visibleAvatars.values()
        if flag == FLAG.LEAVE_WORLD:
            enemiesCounter = 0
        for avatar in visibleAvatars:
            arena = GameEnvironment.getClientArena()
            isTeamate = arena.avatarInfos.get(player.id).get('teamIndex', -1) == arena.avatarInfos.get(avatar.id).get('teamIndex', -1)
            if not isTeamate and not EntityStates.inState(avatar, EntityStates.DESTROYED):
                if not flag == FLAG.LEAVE_WORLD or enemiesCounter:
                    phase = SOUND_PHASES.DOGFIGHT
                    break
                else:
                    enemiesCounter += 1

        return phase

    def __setGamePhase(self, localID):
        if not localID:
            return
        globalState, localContainer, localState = self.__getStates(localID)
        if globalState and globalState != self.__currentGlobalState:
            WWISE_.setState(GamePhases.GLOBAL_STATE, globalState)
        if localContainer != self.__currentLocalContainer and self.__currentLocalContainer:
            WWISE_.setState(self.__currentLocalContainer, '')
        if localContainer and localState and localState != self.__currentLocalState:
            WWISE_.setState(localContainer, localState)
        audio.debug.LOG_AUDIO('%s %s' % ('SoundPhase: ', localID))
        self.__currentGlobalState = globalState
        self.__currentLocalContainer = localContainer
        self.__currentLocalState = localState
        self.__currentSoundPhase = localID
        if audio.debug.IS_AUDIO_DEBUG:
            audio.debug.SHOW_DEBUG_OBJ('Global', str(globalState), group='GamePhases')
            audio.debug.SHOW_DEBUG_OBJ('Container', str(localContainer), group='GamePhases')
            audio.debug.SHOW_DEBUG_OBJ('Local', str(localState), group='GamePhases')

    def __getStates(self, localID):
        localState = None
        globalContainer = None
        globalState = None
        for globalKey in self.__gamePhasesDB.keys():
            locals = self.__gamePhasesDB[globalKey]
            for localKey in locals.keys():
                if localID == localKey:
                    globalContainer = locals[GamePhases.LOCAL_STATES]
                    globalState = globalKey
                    localState = locals[localID]

        return (globalState, globalContainer, localState)