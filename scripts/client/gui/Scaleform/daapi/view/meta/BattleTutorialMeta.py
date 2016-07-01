# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BattleTutorialMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BattleTutorialMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def as_populateProgressBarS(self, currentChapter, totalChapters):
        """
        :param currentChapter:
        :param totalChapters:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_populateProgressBar(currentChapter, totalChapters)

    def as_setTrainingProgressBarS(self, mask):
        """
        :param mask:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTrainingProgressBar(mask)

    def as_setChapterProgressBarS(self, totalSteps, mask):
        """
        :param totalSteps:
        :param mask:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setChapterProgressBar(totalSteps, mask)

    def as_showGreetingS(self, targetID, title, description):
        """
        :param targetID:
        :param title:
        :param description:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showGreeting(targetID, title, description)

    def as_setChapterInfoS(self, description):
        """
        :param description:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setChapterInfo(description)

    def as_showNextTaskS(self, taskID, text, prevDone):
        """
        :param taskID:
        :param text:
        :param prevDone:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showNextTask(taskID, text, prevDone)

    def as_showHintS(self, hintID, text, imagePath, imageAltPath):
        """
        :param hintID:
        :param text:
        :param imagePath:
        :param imageAltPath:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showHint(hintID, text, imagePath, imageAltPath)

    def as_hideGreetingS(self, targetID):
        """
        :param targetID:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_hideGreeting(targetID)