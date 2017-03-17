# Embedded file name: scripts/client/gui/LocalizationHolder.py
from Helpers import i18n
from Singleton import singleton
from gui.Scaleform import main_interfaces
from debug_utils import LOG_INFO
LOC_DICT = {main_interfaces.GUI_SCREEN_LOGIN: ['menu', 'lobby', 'messages'],
 main_interfaces.GUI_SCREEN_LOBBY: ['lobby',
                                    'hud',
                                    'tooltips',
                                    'options',
                                    'messages',
                                    'chat',
                                    'achievements',
                                    'skills',
                                    'tutorial',
                                    'airplanes',
                                    'components',
                                    'battle_results'],
 main_interfaces.GUI_SCREEN_OPTIONS: ['options', 'tooltips'],
 main_interfaces.GUI_SCREEN_UI: ['hud',
                                 'options',
                                 'lobby',
                                 'tutorial',
                                 'battle_results',
                                 'messages',
                                 'keys',
                                 'tooltips',
                                 'skills'],
 main_interfaces.GUI_SCREEN_BEFORESTART: [],
 main_interfaces.GUI_SCREEN_BATTLERESULT: ['lobby', 'achievements'],
 main_interfaces.GUI_SCREEN_PREBATTLE: ['lobby',
                                        'hud',
                                        'tooltips',
                                        'options',
                                        'messages',
                                        'chat'],
 main_interfaces.GUI_SCREEN_BATTLELOADING: ['lobby',
                                            'maps',
                                            'hud',
                                            'tutorial'],
 main_interfaces.GUI_SCREEN_INTERVIEW: ['lobby']}

@singleton

class LocalizationHolder(object):

    def __init__(self):
        self.language = ''

    def fillLocalization(self, language, domain):
        LOG_INFO('___fillLocalization', language, domain)
        self.language = language
        d = i18n.getTranslationTable(domain, language)
        for key, value in d.items():
            self.localization.append(key)
            self.localization.append(value)

    def getLocalization(self, language, screenName):
        self.localization = []
        if screenName in LOC_DICT:
            domains = LOC_DICT[screenName]
            for domain in domains:
                self.fillLocalization(language, domain)

        return self.localization