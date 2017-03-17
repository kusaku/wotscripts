# Embedded file name: scripts/client/PvEManager.py
from AvatarControllerBase import AvatarControllerBase
import BigWorld
from EntityHelpers import EntityStates
import GameEnvironment
from Helpers.i18n import localizeHUD
from OperationCodes import OPERATION_CODE
from _pve_data import PvEData
from debug_utils import LOG_DEBUG
from gui.MapBase import MarkerType
import gui.hud
from gui.WindowsManager import g_windowsManager

class PvEManager(AvatarControllerBase):

    def __init__(self, avatar, opReceiver):
        AvatarControllerBase.__init__(self, avatar)
        self.__handlers = {OPERATION_CODE.PVE_SCENE_TYPE: self.__handleSceneName,
         OPERATION_CODE.PVE_BOTS_SPAWN_MESSAGE: self.__handleBotsSpawn,
         OPERATION_CODE.PVE_LOOSE: self.__handleLoose,
         OPERATION_CODE.PVE_WIN: self.__handleWin,
         OPERATION_CODE.PVE_MESSAGE: self.__handleMessage}
        self.__opReceiver = opReceiver
        self.__opReceiver.onReceiveOperation += self.__onReceiveOperation
        self.__currentSceneData = None
        self._owner.onStateChanged += self.__onAvatarStateChanged
        return

    def update(self, dt):
        pass

    def destroy(self):
        self.__opReceiver.onReceiveOperation -= self.__onReceiveOperation
        self.__opReceiver = None
        self.__currentSceneData = None
        self._owner.onStateChanged -= self.__onAvatarStateChanged
        AvatarControllerBase.destroy(self)
        return

    def __onReceiveOperation(self, operation):
        """
        Receives operation
        @param operation: received operation
        @type operation: ReceivedOperation
        """
        self.__handlers[operation.operationCode](operation)

    def __onAvatarStateChanged(self, oldState, newState):
        if EntityStates.inState(self._owner, EntityStates.GAME):
            g_windowsManager.getBattleUI().showHeaderMessage(localizeHUD(self.__currentSceneData.briefingMsg.title), localizeHUD(self.__currentSceneData.briefingMsg.text), self.__currentSceneData.briefingMsg.duration)

    def __handleBotsSpawn(self, operation):
        """
        @type operation: ReceivedOperation
        """
        for pos in operation.args[0]:
            GameEnvironment.getHUD().minimap.setMarker(pos.x, pos.z, MarkerType.DEFAULT)

        g_windowsManager.getBattleUI().uiCallTextLabel(self.__currentSceneData.botsSpawnMsg.type, localizeHUD(self.__currentSceneData.botsSpawnMsg.text))
        operation.destroy()

    def __handleLoose(self, operation):
        g_windowsManager.getBattleUI().showHeaderMessage(localizeHUD(PvEData.looseMsg.title), localizeHUD(PvEData.looseMsg.text))
        operation.destroy()

    def __handleWin(self, operation):
        g_windowsManager.getBattleUI().showHeaderMessage(localizeHUD(PvEData.winMsg.title), localizeHUD(PvEData.winMsg.text))
        operation.destroy()

    def __handleMessage(self, operation):
        msg = self.__currentSceneData.messages.message[operation.args[0]]
        if len(operation.args) == 2:
            g_windowsManager.getBattleUI().uiCallTextLabel(msg.type, localizeHUD(msg.text).format(*operation.args[1]))
        else:
            g_windowsManager.getBattleUI().uiCallTextLabel(msg.type, localizeHUD(msg.text))
        operation.destroy()

    def __handleSceneName(self, operation):
        self.__currentSceneData = getattr(PvEData, operation.args[0])
        operation.destroy()