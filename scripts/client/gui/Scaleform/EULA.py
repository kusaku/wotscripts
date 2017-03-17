# Embedded file name: scripts/client/gui/Scaleform/EULA.py
import BigWorld, ResMgr
import Settings
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_CURRENT_EXCEPTION
from gui.Version import Version
from config_consts import IS_DEVELOPMENT
from clientConsts import EULA_FILE_PATH, OBT_INTRO_FILE_PATH, GENERAL_INTRO_FILE_PATH, SINGLE_EXP_INTRO_FILE_PATH, RELEASE_INTRO_FILE_PATH, LEGAL_INFO_FILE_PATH
CURRENT_VERSION_TAG = 'currentVersion'
EULA_TEMPLATES_FILE_PATH = 'gui/EULA_templates.xml'

class IXmlParser(object):

    def __init__(self, filePath):
        self._filePath = filePath
        self._text = []

    def getText(self):
        return self._text

    def _readFile(self):
        res = ResMgr.openSection(self._filePath)
        if res:
            try:
                processor = _LicenseXMLProcessor()
                for child in res.values():
                    result = processor.execute(child, result=[])
                    if len(result) > 0:
                        self._text.extend(result)

            except:
                LOG_CURRENT_EXCEPTION()

            ResMgr.purge(self._filePath, True)
        else:
            LOG_ERROR("_readFile - can't open resource: %s" % self._filePath)


class LegalInfoInterface(IXmlParser):

    def __init__(self):
        IXmlParser.__init__(self, LEGAL_INFO_FILE_PATH)
        self._readFile()


class OBTIntroInterface(IXmlParser):

    def __init__(self):
        IXmlParser.__init__(self, OBT_INTRO_FILE_PATH)
        self._readFile()


class ReleaseIntroInterface(IXmlParser):

    def __init__(self):
        IXmlParser.__init__(self, RELEASE_INTRO_FILE_PATH)
        self._readFile()


class SingleExpIntroInterface(IXmlParser):

    def __init__(self):
        IXmlParser.__init__(self, SINGLE_EXP_INTRO_FILE_PATH)
        self._readFile()


class GeneralTestIntroInterface(IXmlParser):

    def __init__(self):
        IXmlParser.__init__(self, GENERAL_INTRO_FILE_PATH)
        self._readFile()


class EULAInterface(IXmlParser):

    def __init__(self, language = 'ru'):
        IXmlParser.__init__(self, EULA_FILE_PATH)
        self.__showLicense = False
        self.__readVersionFile()
        if self.needShowLicense():
            self._readFile()

    def needShowLicense(self):
        return self.__showLicense

    def onPlayerAgree(self):
        self.__saveVersionFile()

    def __readVersionFile(self):
        res = Settings.g_instance.userPrefs
        if res:
            versionString = Version().getVersion()
            savedVersionString = res.readString(CURRENT_VERSION_TAG, 'unknow')
            self.__showLicense = versionString.strip() != savedVersionString.strip() and not IS_DEVELOPMENT

    def __saveVersionFile(self):
        res = Settings.g_instance.userPrefs
        if res:
            versionString = Version().getVersion()
            res.writeString(CURRENT_VERSION_TAG, versionString)
            BigWorld.savePreferences()


class _TagTemplate(object):

    def __init__(self, template):
        self._template = template

    def execute(self, section, processor, result):
        result.append(self._template)


class _LinkTemplate(_TagTemplate):

    def execute(self, section, processor, result):
        text = section['text']
        url = section['url']
        if text is None and url is not None:
            text = url
        if text is not None and url is not None:
            result.append(self._template % (url.asWideString, text.asWideString))
        return


class _ContentTemplate(_TagTemplate):

    def execute(self, section, processor, result):
        values = section.values()
        if len(values) > 0:
            selfResult = []
            for tSection in values:
                processor.execute(tSection, processor, selfResult)

        else:
            selfResult = [section.asWideString]
        result.append(self._template % u''.join(selfResult))


class _ChapterTemplate(object):

    def __init__(self, titleTemplate, contentTemplate):
        self.__titleTemplate = titleTemplate
        self.__content = _ContentTemplate(contentTemplate)

    def execute(self, section, processor, result):
        tSection = section['title']
        if tSection:
            result.append(self.__titleTemplate % tSection.asWideString)
        cSection = section['content']
        if cSection:
            self.__content.execute(cSection, processor, result)


class _LicenseXMLProcessor(object):

    def __init__(self):
        self.__templates = {}
        self.__loadTemplates()

    def __loadTemplates(self):
        res = ResMgr.openSection(EULA_TEMPLATES_FILE_PATH)
        if res:
            for tagName, child in res.items():
                className = child.readString('class')
                if className:
                    cl = globals().get(className)
                    if cl:
                        args = []
                        argsSection = child['args'] if child.has_key('args') else []
                        for argSection in argsSection.values():
                            arg = argSection.asString
                            if len(arg) > 0:
                                args.append(arg)

                        self.__templates[tagName] = cl(*args)
                    else:
                        LOG_ERROR('_LicenseXMLProcessor::__loadTemplates', 'Class tag not found: %s' % cl)

        else:
            LOG_ERROR('_LicenseXMLProcessor::__loadTemplates()', "Can't open resource: %s" % EULA_TEMPLATES_FILE_PATH)

    def execute(self, section, processor = None, result = []):
        template = self.__templates.get(section.name)
        if template:
            template.execute(section, self, result)
        else:
            result.append(section.asWideString)
        return result