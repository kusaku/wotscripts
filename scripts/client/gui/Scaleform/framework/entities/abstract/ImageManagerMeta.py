# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/ImageManagerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ImageManagerMeta(BaseDAAPIComponent):

    def as_setImageCacheSettingsS(self, maxSize, minSize):
        if self._isDAAPIInited():
            return self.flashObject.as_setImageCacheSettings(maxSize, minSize)

    def as_loadImagesS(self, sourceData):
        """
        :param sourceData: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_loadImages(sourceData)

    def as_unloadImagesS(self, sourceData):
        """
        :param sourceData: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_unloadImages(sourceData)