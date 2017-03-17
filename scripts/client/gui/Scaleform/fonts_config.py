# Embedded file name: scripts/client/gui/Scaleform/fonts_config.py
from gui.Scaleform import SCALEFORM_FONT_CONFIG_PATH, SCALEFORM_FONT_LIB_PATH, SCALEFORM_DEFAULT_CONFIG_NAME
import ResMgr
import _Scaleform

class FONT_CONFIG_LOAD_RESULT(object):
    loaded, alreadyLoaded, notFound = range(3)


class FontConfig(object):

    def __init__(self, configName, fontlib, aliases):
        self.__configName = configName
        self.__fontlib = fontlib
        self.__aliases = aliases
        self.__loaded = False

    def load(self):
        if self.__loaded:
            return FONT_CONFIG_LOAD_RESULT.alreadyLoaded
        for embedded, fondDesc in self.__aliases.items():
            runtime = fondDesc[0]
            fontType = fondDesc[1]
            _Scaleform.mapFont(embedded, runtime, fontType)

        movieDef = _Scaleform.MovieDef(SCALEFORM_FONT_LIB_PATH + '/' + self.__fontlib)
        movieDef.setAsFontMovie()
        movieDef.addToFontLibrary()
        self.__loaded = True
        return FONT_CONFIG_LOAD_RESULT.loaded

    def configName(self):
        return self.__configName

    def isLoaded(self):
        return self.__loaded


class FontConfigMap(object):

    def __init__(self):
        self.__configs = dict()
        self.__readXml()

    def __readXml(self):
        dataSection = ResMgr.openSection(SCALEFORM_FONT_CONFIG_PATH)
        if dataSection is None:
            raise IOError, 'can not open <%s>.' % SCALEFORM_FONT_CONFIG_PATH
        for tag, fontconfig in dataSection.items():
            if tag == 'config':
                aliases = dict()
                if fontconfig.has_key('name'):
                    configName = fontconfig.readString('name')
                else:
                    raise Exception, 'You must specify the name of the configuration'
                if fontconfig.has_key('fontlib'):
                    fontlib = fontconfig.readString('fontlib')
                else:
                    raise Exception, 'You must specify the font library file'
                if fontconfig.has_key('map'):
                    map = fontconfig['map']
                    for tag, alias in map.items():
                        if tag == 'alias':
                            embedded = alias.readString('embedded')
                            runtime = alias.readString('runtime')
                            fontType = alias.readString('type')
                            aliases[embedded] = (runtime, fontType)

                self.__configs[configName] = FontConfig(configName, fontlib, aliases)

        return

    def loadFonts(self, configName):
        result = FONT_CONFIG_LOAD_RESULT.notFound
        fontConfig = self.__configs.get(configName)
        if fontConfig:
            result = fontConfig.load()
        return result

    def load(self):
        return self.loadFonts(SCALEFORM_DEFAULT_CONFIG_NAME)


g_fontConfigMap = FontConfigMap()