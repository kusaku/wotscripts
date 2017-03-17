# Embedded file name: scripts/client/gui/Scaleform/Flash.py
import BigWorld
import GUI, _Scaleform, weakref
from gui.Scaleform import SCALEFORM_SWF_PATH
from gui.Scaleform.Handler import Handler
from debug_utils import LOG_DEBUG, LOG_CODEPOINT_WARNING
from clientConsts import GUI_COMPONENTS_DEPH

class Flash(Handler):

    def __init__(self, swf, className = 'Flash', args = []):
        movie = BigWorld.PyMovieView(SCALEFORM_SWF_PATH + '/' + swf)
        self.component = getattr(GUI, className)(movie, *args)
        self.component.focus = True
        self.component.moveFocus = True
        self.component.position.z = GUI_COMPONENTS_DEPH.FLASH
        self.flashSize = (2, 2)
        self.isActive = False
        Handler.__init__(self)
        movie = self.component.movie
        movie.setFSCommandHandler(_FuncObj(self, 'handleFsCommandCallback'))
        movie.setExternalInterfaceCallback(_FuncObj(self, 'handleExternalInterfaceCallback'))
        self.__className = None
        return

    def __setClassName(self, className):
        self.__className = className

    def __getClassName(self):
        return self.__className

    className = property(__getClassName, __setClassName)

    def __del__(self):
        LOG_DEBUG('Deleted: %s' % self)

    @property
    def movie(self):
        return self.component.movie

    def active(self, state):
        if self.isActive != state:
            self.isActive = state
            if state:
                GUI.addRoot(self.component)
                self.component.size = self.flashSize
            else:
                GUI.delRoot(self.component)

    def close(self):
        self.component.script = None
        self.active(False)
        self.beforeDelete()
        return


class _FuncObj:

    def __init__(self, obj, funcName):
        self.__weakObj = weakref.ref(obj)
        self.__funcName = funcName

    def __call__(self, command, args):
        if self.__weakObj() is not None:
            return getattr(self.__weakObj(), self.__funcName)(command, args)
        else:
            LOG_CODEPOINT_WARNING('weak object has been already destroyed.')
            return
            return