# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/AwardWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class AwardWindowMeta(AbstractWindowView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends AbstractWindowView
    """

    def onOKClick(self):
        self._printOverrideError('onOKClick')

    def onTakeNextClick(self):
        self._printOverrideError('onTakeNextClick')

    def onCloseClick(self):
        self._printOverrideError('onCloseClick')

    def onCheckBoxSelect(self, isSelected):
        self._printOverrideError('onCheckBoxSelect')

    def onWarningHyperlinkClick(self):
        self._printOverrideError('onWarningHyperlinkClick')

    def onAnimationStart(self):
        self._printOverrideError('onAnimationStart')

    def as_setDataS(self, data):
        """
        :param data: Represented by AwardWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setTakeNextBtnS(self, texts):
        """
        :param texts: Represented by AwardWindowTakeNextBtnVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTakeNextBtn(texts)

    def as_startAnimationS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_startAnimation()

    def as_endAnimationS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_endAnimation()