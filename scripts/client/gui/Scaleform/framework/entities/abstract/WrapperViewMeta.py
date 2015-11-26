# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/WrapperViewMeta.py
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class WrapperViewMeta(DAAPIModule):

    def onWindowClose(self):
        self._printOverrideError('onWindowClose')