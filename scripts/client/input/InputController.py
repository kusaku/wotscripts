# Embedded file name: scripts/client/input/InputController.py
import GameEnvironment
from GameServiceBase import GameServiceBase
import InputMapping
import GUI
import BigWorld
from CameraStates import CameraState
import Keys
from EntityHelpers import EntityStates
import VOIP
from debug_utils import LOG_DEBUG, LOG_WARNING, LOG_TRACE
from consts import SHELL_INDEX
import consts
from Helpers.i18n import convert
import Settings
from Event import Event, EventManager
from InputCommandProcessor import InputCommandProcessor
import functools
from clientConsts import CLASTERS, SWITCH_STYLES_BUTTONS, NOT_CONTROLLED_MOD
from input.InputAxisProvider import InputAxisProvider

class UserKeyEvent:

    def __init__(self, key = -1, deviceId = 0):
        self.key = key
        self.deviceId = deviceId

    def isRepeatedEvent(self):
        return False

    def isKeyDown(self):
        if self.key != 0:
            return BigWorld.isKeyDown(self.key, self.deviceId)
        return False

    def isCtrlDown(self):
        return BigWorld.isKeyDown(Keys.KEY_LCONTROL, 0) or BigWorld.isKeyDown(Keys.KEY_RCONTROL, 0)

    def isKeyUp(self):
        return False

    def isMouseButton(self):
        return self.key in [Keys.KEY_LEFTMOUSE, Keys.KEY_RIGHTMOUSE, Keys.KEY_MIDDLEMOUSE]


class InputController(GameServiceBase):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.MAPPING_CAMERA_STATE = {}
        self.__intermissionFireAllowed = True
        self.__intermissionMenuMode = False
        self.__intermissionZoomWasReset = False
        self.__eventManager = EventManager()
        em = self.__eventManager
        self.eAddProcessorListeners = Event(em)
        self.eSideViewPressed = Event(em)
        self.eSideViewReleased = Event(em)
        self.ePlayerListChangeState = Event(em)
        self.eVisibilityTeams = Event(em)
        self.eVisibilityChat = Event(em)
        self.eInputProfileChange = Event(em)
        self.eBattleModeChange = Event(em)
        self.__globalCommandsPredicates = {InputMapping.CMD_SHOW_CURSOR: {'isUp': True},
         InputMapping.CMD_SNIPER_CAMERA: {'isUp': True},
         InputMapping.CMD_BACK_VIEW: {'isUp': True},
         InputMapping.CMD_CHAT: {'isUp': False},
         InputMapping.CMD_INTERMISSION_MENU: {'isUp': False}}

    def init(self, gameEnvr):
        super(self.__class__, self).init(gameEnvr)
        self.__commandProcessor = InputCommandProcessor()
        self.__commandProcessor.recreateCommandMap()
        InputMapping.g_instance.onSaveControls += self.__commandProcessor.recreateCommandMap
        self.__inputAxis = InputAxisProvider()

    def destroy(self):
        self.__eventManager.clear()
        del self.__inputAxis
        super(self.__class__, self).destroy()

    def afterLinking(self):
        super(self.__class__, self).afterLinking()
        self.__setPredicates()
        self.__linkEvents()
        self.__inputAxis.init(self.__commandProcessor)

    def __onPlayerListKey(self, fired):
        if fired and (BigWorld.isKeyDown(Keys.KEY_LCONTROL, 0) or BigWorld.isKeyDown(Keys.KEY_RCONTROL, 0)):
            self.ePlayerListChangeState()
        else:
            self.eVisibilityTeams(fired)

    def __onFireButtonPress(self, fired):
        owner = BigWorld.player()
        shootingFlag = 0
        if self.__intermissionFireAllowed:
            if self.isFired(InputMapping.CMD_PRIMARY_FIRE):
                shootingFlag = 255
            else:
                if self.isFired(InputMapping.CMD_FIRE_GROUP_1):
                    shootingFlag |= 1
                if self.isFired(InputMapping.CMD_FIRE_GROUP_2):
                    shootingFlag |= 2
                if self.isFired(InputMapping.CMD_FIRE_GROUP_3):
                    shootingFlag |= 4
        owner.onFireChange(shootingFlag)

    def __onSideViewPress(self, stateData, key, isKeyFired):
        flag = Settings.g_instance.isCameraFreezEnabled and key != InputMapping.CMD_BACK_VIEW
        if isKeyFired:
            self.eSideViewPressed(stateData, flag)
        else:
            self.eSideViewReleased(stateData, flag)

    def __setPredicates(self):
        """
        Set up predicate for command event. Command can has many predicates, and run only if all predicates are TRUE 
        Add new predicate: processor.addPredicate( COMMAND ID, predicate function )
        """
        processor = self.__commandProcessor
        import BattleReplay
        inGame = lambda : EntityStates.inState(BigWorld.player(), EntityStates.GAME) and not BigWorld.player().isArenaFreezed and not BattleReplay.isPlaying()
        inNotDestroyFallAndReplay = lambda : BattleReplay.isPlaying() or not (EntityStates.inState(BigWorld.player(), EntityStates.DESTROYED_FALL) and BigWorld.player().curVehicleID == 0)
        processor.addPredicate(InputMapping.CMD_SHOW_TEAMS, inNotDestroyFallAndReplay)
        processor.addPredicate(InputMapping.CMD_SHOW_TEAMS, lambda : not (hud.isBattleLoadingVisible() or inOutro()))
        processor.addPredicate(InputMapping.CMD_SHOW_TEAMS, lambda : not EntityStates.inState(BigWorld.player(), EntityStates.DESTROYED))
        inGameAndStart = lambda : EntityStates.inState(BigWorld.player(), EntityStates.GAME | EntityStates.WAIT_START | EntityStates.PRE_START_INTRO) and not BigWorld.player().isArenaFreezed and not BattleReplay.isPlaying()
        inGameAndStartAndReplay = lambda : EntityStates.inState(BigWorld.player(), EntityStates.GAME | EntityStates.WAIT_START | EntityStates.PRE_START_INTRO) and not BigWorld.player().isArenaFreezed
        notInGame = lambda : not EntityStates.inState(BigWorld.player(), EntityStates.GAME | EntityStates.WAIT_START | EntityStates.PRE_START_INTRO)
        hidenMouseCursor = lambda : not GUI.mcursor().visible
        ctrlBtn = lambda : BigWorld.isKeyDown(Keys.KEY_LCONTROL, 0) or BigWorld.isKeyDown(Keys.KEY_RCONTROL, 0)
        hud = GameEnvironment.getHUD()
        inGameAndStartAndBattleLoadingDispossessed = lambda : hud.isBattleLoadingDispossessed() and not BattleReplay.isPlaying()
        inOutro = lambda : EntityStates.inState(BigWorld.player(), EntityStates.OUTRO)
        processor.addPredicate(InputMapping.CMD_TARGET_CAMERA, hud.isEntityesLockEnabled)
        processor.addPredicate(InputMapping.CMD_TARGET_CAMERA, hud.isBattleLoadingDispossessed)
        processor.addPredicate(InputMapping.CMD_TARGET_CAMERA, --- This code section failed: ---

0	LOAD_DEREF        'inGameAndStartAndReplay'
3	CALL_FUNCTION_0   None
6	JUMP_IF_FALSE_OR_POP '35'
9	LOAD_DEREF        'BattleReplay'
12	LOAD_ATTR         'isPlaying'
15	CALL_FUNCTION_0   None
18	POP_JUMP_IF_FALSE '32'
21	LOAD_DEREF        'BattleReplay'
24	LOAD_ATTR         'g_replay'
27	LOAD_ATTR         'isControllingCamera'
30	UNARY_NOT         None
31	RETURN_END_IF     None
32	LOAD_GLOBAL       'True'
35_0	COME_FROM         '6'
35	RETURN_VALUE      None
-1	LAMBDA_MARKER     None

Syntax error at or near `RETURN_END_IF' token at offset 31
)
        inGameAndStartCommands = [InputMapping.CMD_CURSOR_CAMERA,
         InputMapping.CMD_SNIPER_CAMERA,
         InputMapping.CMD_EXTRA_INPUT_MODE,
         InputMapping.CMD_LOCK_TARGET,
         InputMapping.CMD_NEXT_TARGET,
         InputMapping.CMD_NEXT_TARGET_TEAM_OBJECT,
         InputMapping.CMD_MINIMAP_ZOOM_OUT,
         InputMapping.CMD_MINIMAP_ZOOM_IN]
        inGameAndStartCommands.extend(self.MAPPING_CAMERA_STATE.keys())
        for commandID in inGameAndStartCommands:
            processor.addPredicate(commandID, lambda : inGameAndStartAndBattleLoadingDispossessed() and not inOutro())

        processor.addPredicate(InputMapping.CMD_SHOW_MAP, lambda : not hud.isBattleLoadingVisible() and not inOutro())
        processor.addPredicate(InputMapping.CMD_BACK_VIEW, lambda : inGameAndStartAndBattleLoadingDispossessed() and EntityStates.inState(BigWorld.player(), EntityStates.WAIT_START | EntityStates.GAME))
        processor.addPredicate(InputMapping.CMD_HELP, lambda : True)
        for commandID in [InputMapping.CMD_MINIMAP_SIZE_INC, InputMapping.CMD_MINIMAP_SIZE_DEC]:
            processor.addPredicate(commandID, lambda : hud.isBattleLoadingDispossessed())

        for commandID in [InputMapping.CMD_TURN_LEFT,
         InputMapping.CMD_TURN_RIGHT,
         InputMapping.CMD_PITCH_DOWN,
         InputMapping.CMD_PITCH_UP,
         InputMapping.CMD_ROLL_LEFT,
         InputMapping.CMD_ROLL_RIGHT,
         InputMapping.CMD_INCREASE_FORCE,
         InputMapping.CMD_DECREASE_FORCE,
         InputMapping.CMD_ENGINE_OFF,
         InputMapping.CMD_F5_CHAT_COMMAND,
         InputMapping.CMD_F7_CHAT_COMMAND]:
            processor.addPredicate(commandID, lambda : not EntityStates.inState(BigWorld.player(), EntityStates.PRE_START_INTRO))

        processor.addPredicate(InputMapping.CMD_SNIPER_CAMERA, inGame)
        processor.addPredicate(InputMapping.CMD_AUTOPILOT, inGame)
        processor.addPredicate(InputMapping.CMD_LAUNCH_ROCKET, inGame)
        processor.addPredicate(InputMapping.CMD_LAUNCH_BOMB, inGame)
        processor.addPredicate(InputMapping.CMD_BOMBING_SIGHT, inGame)
        processor.addPredicate(InputMapping.CMD_PRIMARY_FIRE, inGame)
        processor.addPredicate(InputMapping.CMD_FIRE_GROUP_1, inGame)
        processor.addPredicate(InputMapping.CMD_FIRE_GROUP_2, inGame)
        processor.addPredicate(InputMapping.CMD_FIRE_GROUP_3, inGame)
        processor.addPredicate(InputMapping.CMD_TURN_LEFT, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_TURN_RIGHT, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_PITCH_DOWN, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_PITCH_UP, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_ROLL_LEFT, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_ROLL_RIGHT, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_INCREASE_FORCE, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_DECREASE_FORCE, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_FLAPS_UP, inGame)
        processor.addPredicate(InputMapping.CMD_ENGINE_OFF, inGameAndStart)
        processor.addPredicate(InputMapping.CMD_INC_TARGET_FORCE, inGame)
        processor.addPredicate(InputMapping.CMD_DEC_TARGET_FORCE, inGame)
        processor.addPredicate(InputMapping.CMD_BATTLE_MODE, inGame)
        processor.addPredicate(InputMapping.CMD_NEXT_VEHICLE_WHEN_DEAD, notInGame)
        processor.addPredicate(InputMapping.CMD_PREV_VEHICLE_WHEN_DEAD, notInGame)
        processor.addPredicate(InputMapping.CMD_NEXT_VEHICLE_WHEN_DEAD, hidenMouseCursor)
        processor.addPredicate(InputMapping.CMD_PREV_VEHICLE_WHEN_DEAD, hidenMouseCursor)
        processor.addPredicate(InputMapping.CMD_SHOW_CURSOR, lambda : not BattleReplay.isPlaying())
        processor.addPredicate(InputMapping.CMD_REPLAY_SHOW_CURSOR, lambda : BattleReplay.isPlaying())
        for command in [InputMapping.CMD_F9_CHAT_COMMAND]:
            processor.addPredicate(command, inGame)

        for command in [InputMapping.CMD_F2_CHAT_COMMAND,
         InputMapping.CMD_F3_CHAT_COMMAND,
         InputMapping.CMD_F4_CHAT_COMMAND,
         InputMapping.CMD_F5_CHAT_COMMAND,
         InputMapping.CMD_F6_CHAT_COMMAND,
         InputMapping.CMD_F7_CHAT_COMMAND,
         InputMapping.CMD_F8_CHAT_COMMAND]:
            processor.addPredicate(command, inGameAndStart)

        for command in InputMapping.EQUIPMENT_COMMANDS:
            processor.addPredicate(command, inGame)

    def __linkEvents(self):
        """
        Link all commands event to all game subsystems
        For add new event listeners for command: processor.addListeners( COMMAND ID, onKeyDownEvent() function,onKeyUpEvent() function, onChangeEvent(isFired) function)
        """
        owner = BigWorld.player()
        cmdMap = InputMapping.g_instance
        processor = self.__commandProcessor
        processor.addListeners(InputMapping.CMD_SHOW_TEAMS, None, None, self.__onPlayerListKey)
        processor.addListeners(InputMapping.CMD_CHAT, self.eVisibilityChat)
        processor.addPredicate(InputMapping.CMD_CHAT, lambda : not BigWorld.isKeyDown(Keys.KEY_LALT, 0) and not BigWorld.isKeyDown(Keys.KEY_RALT, 0))
        processor.addListeners(InputMapping.CMD_LAUNCH_ROCKET, lambda : owner.launchShell(SHELL_INDEX.TYPE1))
        processor.addListeners(InputMapping.CMD_LAUNCH_BOMB, lambda : owner.launchShell(SHELL_INDEX.TYPE2))
        processor.addListeners(InputMapping.CMD_PRIMARY_FIRE, None, None, self.__onFireButtonPress)
        processor.addListeners(InputMapping.CMD_FIRE_GROUP_1, None, None, self.__onFireButtonPress)
        processor.addListeners(InputMapping.CMD_FIRE_GROUP_2, None, None, self.__onFireButtonPress)
        processor.addListeners(InputMapping.CMD_FIRE_GROUP_3, None, None, self.__onFireButtonPress)
        if InputMapping.g_instance.getSwitchingStyle(InputMapping.CMD_PUSH_TO_TALK_SQUAD) == SWITCH_STYLES_BUTTONS.HOLD:
            self.__voipPushToTalk(consts.VOIP.CHANNEL_TYPES.ARENA, InputMapping.CMD_PUSH_TO_TALK, None)
            self.__voipPushToTalk(consts.VOIP.CHANNEL_TYPES.SQUAD, InputMapping.CMD_PUSH_TO_TALK_SQUAD, None)
        processor.addListeners(InputMapping.CMD_PUSH_TO_TALK, None, None, lambda fired: self.__voipPushToTalk(consts.VOIP.CHANNEL_TYPES.ARENA, InputMapping.CMD_PUSH_TO_TALK, fired))
        processor.addListeners(InputMapping.CMD_TOGGLE_ARENA_VOICE_CHANNEL, lambda : self.__voipToggleArenaChannel())
        for commandID in self.MAPPING_CAMERA_STATE:
            processor.addListeners(commandID, None, None, functools.partial(self.__onSideViewPress, self.MAPPING_CAMERA_STATE[commandID], commandID))

        processor.addListeners(InputMapping.CMD_INVERT_Y, cmdMap.invertY)
        self.eAddProcessorListeners(processor)
        return

    def __voipPushToTalk(self, channel, cmd, fired):
        """
        @param channel: one of constants from consts.VOIP.CHANNEL_TYPES
        @param cmd:     one of commands from InputMapping
        @param fired:   new command-key state (True/False or None to auto-detect initial state)
        """
        if fired is None:
            fired = self.isFired(cmd)
            init = True
        else:
            init = False
        switchingStyle = InputMapping.g_instance.getSwitchingStyle(cmd)
        LOG_TRACE('InputController.__voipPushToTalk: channel %s, switching style %d, fired %s' % (consts.VOIP.CHANNEL_TYPES.getConstNameByValue(channel), switchingStyle, fired))
        if not init and switchingStyle == SWITCH_STYLES_BUTTONS.SWITCH:
            VOIP.api().togglePushToTalk(channel, False)
        else:
            VOIP.api().setPushToTalk(channel, fired, True)
        return

    def __voipToggleArenaChannel(self):
        VOIP.api().toggleArenaChannelStatus()

    def __commandGlobalPredicate(self, event):
        commandIDlist = self.__commandProcessor.getCommandIDlist(event.key, event.deviceId)
        if commandIDlist is not None:
            for commandID in commandIDlist:
                globalCommandPredicate = self.__globalCommandsPredicates.get(commandID, None)
                if globalCommandPredicate is not None:
                    if globalCommandPredicate['isUp']:
                        return event.isKeyUp()
                    return True

        return False

    def __keyboardGlobalPredicate(self, event):
        owner = BigWorld.player()
        res = (owner.isFlyKeyBoardInputAllowed() or owner.isFlyMouseInputAllowed() and (event.isMouseButton() or event.deviceId != 0) or self.__commandGlobalPredicate(event)) and not (event.isMouseButton() and GUI.mcursor().visible and event.isKeyDown()) and not event.isRepeatedEvent()
        return res

    def __mouseGlobalPredicate(self, event):
        owner = BigWorld.player()
        camera = GameEnvironment.getCamera()
        return (EntityStates.inState(owner, EntityStates.GAME) or EntityStates.inState(owner, EntityStates.WAIT_START | EntityStates.PRE_START_INTRO)) and owner.isFlyMouseInputAllowed() and not camera.isMouseHandled()

    def __joystickGlobalPredicate(self, event):
        owner = BigWorld.player()
        return owner.isArenaFreezed != True

    def handleKeyEvent(self, event):
        if self.__keyboardGlobalPredicate(event):
            self.__commandProcessor.onKeyEvent(event)

    def processMouseEvent(self, event):
        if self.__mouseGlobalPredicate(event):
            self.__inputAxis.processMouseEvent(event)

    def processJoystickEvent(self, event):
        if self.__joystickGlobalPredicate(event):
            self.__commandProcessor.onAxisEvent(event)
            self.__inputAxis.processJoystickEvent(event)

    def doLeaveWorld(self):
        super(self.__class__, self).doLeaveWorld()
        self.dispose()

    def dispose(self):
        InputMapping.g_instance.onSaveControls -= self.__commandProcessor.recreateCommandMap
        self.__inputAxis.dispose()
        import BWPersonality
        BWPersonality.g_commandsFiredCounter.update(self.__commandProcessor.getCommandsFiredCount())
        self.__commandProcessor.destroy()
        self.__commandProcessor = None
        return

    def setIntermissionMenuMode(self, value = True, resetToZoomMin = False):
        if self.__intermissionMenuMode == value:
            return
        self.__intermissionMenuMode = value
        owner = BigWorld.player()
        if not value:
            self.__inputAxis.notControlledByUser(False, NOT_CONTROLLED_MOD.PLAYER_MENU)
            self.forceRefreshButtons(InputMapping.COMMANDS_TO_REFRESH)
            self.refreshButtons(InputMapping.COMMANDS_TO_NOT_REFRESH)
            self.__onFireButtonPress(False)
            if not self.__changeCommandProcessorFiredFlag(InputMapping.CMD_PRIMARY_FIRE):
                for cmd in [InputMapping.CMD_FIRE_GROUP_1, InputMapping.CMD_FIRE_GROUP_2, InputMapping.CMD_FIRE_GROUP_3]:
                    self.__changeCommandProcessorFiredFlag(cmd)

            if EntityStates.inState(owner, EntityStates.GAME) and self.__intermissionZoomWasReset:
                GameEnvironment.getCamera().resetToBackZoom()
                self.__intermissionZoomWasReset = False
            self.__intermissionFireAllowed = True
        else:
            self.__inputAxis.notControlledByUser(resetToZoomMin, NOT_CONTROLLED_MOD.PLAYER_MENU)
            import BattleReplay
            isPlayingReplay = BattleReplay.g_replay.isPlayingReplay()
            if EntityStates.inState(owner, EntityStates.GAME) and not isPlayingReplay and resetToZoomMin:
                GameEnvironment.getCamera().resetToZoomMin()
                self.__intermissionZoomWasReset = True
                self.__intermissionFireAllowed = False
                owner.onFireChange(0)
            self.refreshButtons(InputMapping.COMMANDS_TO_NOT_REFRESH)

    def __changeCommandProcessorFiredFlag(self, cmdID):
        """
        @param cmdID: int Ex.: InputMapping.CMD_PRIMARY_FIRE
        @return: bool
        """
        isFired = self.isFired(cmdID)
        if isFired != self.__commandProcessor.getCommand(cmdID).isFired:
            self.__commandProcessor.getCommand(cmdID).isFired = isFired
        return isFired

    def onSetFocus(self, state):
        self.__inputAxis.notControlledByUser(not state, NOT_CONTROLLED_MOD.LOST_WINDOW_FOCUS)
        self.refreshButtons([])

    def refreshButtons(self, ignoreCommandIDsList):
        userKeyEvents = InputMapping.g_instance.getAllCommandsButtonsList(ignoreCommandIDsList)
        for userKeyEvent in userKeyEvents:
            if userKeyEvent.isKeyDown():
                self.handleKeyEvent(userKeyEvent)

    def forceRefreshButtons(self, commandIDsList):
        userKeyEvents = InputMapping.g_instance.getCommandsButtonsList(commandIDsList)
        for userKeyEvent in userKeyEvents:
            self.handleKeyEvent(userKeyEvent)

    @property
    def inputAxis(self):
        return self.__inputAxis

    @property
    def commandProcessor(self):
        return self.__commandProcessor

    def onHideModalScreen(self):
        self.setIntermissionMenuMode(False)

    def onFlyKeyBoardInputAllowed(self, flag, playerAvatar):
        NEED_REFRESH = [InputMapping.CMD_INCREASE_FORCE,
         InputMapping.CMD_ENGINE_OFF,
         InputMapping.CMD_FLAPS_UP,
         InputMapping.CMD_SIDE_VIEW_UP_LEFT,
         InputMapping.CMD_BATTLE_MODE,
         InputMapping.CMD_BOMBING_SIGHT,
         InputMapping.CMD_ROLL_LEFT,
         InputMapping.CMD_ROLL_RIGHT,
         InputMapping.CMD_PITCH_DOWN,
         InputMapping.CMD_PITCH_UP,
         InputMapping.CMD_TURN_LEFT,
         InputMapping.CMD_TURN_RIGHT,
         InputMapping.CMD_PRIMARY_FIRE,
         InputMapping.CMD_HELP]
        NEED_REFRESH.extend(self.MAPPING_CAMERA_STATE.keys())
        if flag:
            ignoreList = [InputMapping.CMD_SHOW_TEAMS,
             InputMapping.CMD_VISIBILITY_HUD,
             InputMapping.CMD_SHOW_CURSOR,
             InputMapping.CMD_SHOW_MAP]
            ignoreList.extend(NEED_REFRESH)
            self.refreshButtons(ignoreList)
        self.forceRefreshButtons(NEED_REFRESH)

    def isFired(self, commandId):
        import BWPersonality
        if commandId in BWPersonality.qaCommands:
            return True
        return self.__commandProcessor.isFired(commandId)

    def onPlayerAvatarStateChanged(self, oldState, state):
        if state & EntityStates.GAME:
            self.__commandProcessor.startCollectClientStats()
        else:
            self.__commandProcessor.stopCollectClientStats()

    def resetCommandStats(self):
        self.__commandProcessor.reset()

    def getCommandStats(self):
        return self.__commandProcessor.gatherCommandStats()

    @property
    def isCollectingClientStats(self):
        return self.__commandProcessor.isCollectingClientStats

    def startCollectClientStats(self):
        self.__commandProcessor.startCollectClientStats()

    def stopCollectClientStats(self):
        self.__commandProcessor.stopCollectClientStats()

    def inputIsBlocked(self, val):
        map = self.isFired(InputMapping.CMD_SHOW_MAP)
        tab = self.isFired(InputMapping.CMD_SHOW_TEAMS)
        cursor = self.isFired(InputMapping.CMD_SHOW_CURSOR)
        if not map and not tab and not cursor:
            self.__inputAxis.notControlledByUser(not val, NOT_CONTROLLED_MOD.MOUSE_INPUT_BLOCKED)