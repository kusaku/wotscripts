# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/ImageManagerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIModule import BaseDAAPIModule

class ImageManagerMeta(BaseDAAPIModule):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIModule
    null
    """

    def as_setImageCacheSettingsS(self, maxSize, minSize):
        """
        :param maxSize:
        :param minSize:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setImageCacheSettings(maxSize, minSize)

    def as_loadImagesS(self, sourceData):
        """
        :param sourceData:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_loadImages(sourceData)

    def as_unloadImagesS(self, sourceData):
        """
        :param sourceData:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_unloadImages(sourceData)