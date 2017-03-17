# Embedded file name: scripts/client/messenger/filters.py
import BigWorld
from debug_utils import LOG_WARNING, LOG_DEBUG, LOG_CURRENT_EXCEPTION
from external_strings_utils import normalized_unicode_trim
from Helpers import html
from messenger import g_olDictionary, g_dnDictionary, MESSAGE_MAX_LENGTH, MESSAGE_MAX_LENGTH_IN_BATTLE, MESSAGE_FLOOD_COOLDOWN, COLORING_FOR_BAD_WORD_FORMAT
import weakref
import time

class IncomingFilter(object):

    def filter(self, message, userId, msgTime):
        pass


class ObsceneLanguageFilter(IncomingFilter):

    def __init__(self):
        super(ObsceneLanguageFilter, self).__init__()
        self.applyReplacementFunction()

    @staticmethod
    def applyReplacementFunction():
        g_olDictionary.resetReplacementFunction()

    def filter(self, text, userId, msgTime):
        return g_olDictionary.searchAndReplace(text)


class ColoringObsceneLanguageFilter(IncomingFilter):

    def __init__(self):
        super(ColoringObsceneLanguageFilter, self).__init__()
        self.applyReplacementFunction()

    @staticmethod
    def applyReplacementFunction():
        g_olDictionary.overrideReplacementFunction(lambda word: COLORING_FOR_BAD_WORD_FORMAT % word)

    def filter(self, text, userId, msgTime):
        return g_olDictionary.searchAndReplace(text)


class SpamFilter(IncomingFilter):

    def __init__(self):
        super(SpamFilter, self).__init__()
        try:
            self._filter = BigWorld.WGSpamFilter()
            self._filter.removeSpam('')
        except AttributeError:
            LOG_CURRENT_EXCEPTION()

            class Dummy(object):

                def removeSpam(self, text):
                    return text

            self._filter = Dummy()

    def filter(self, text, userId, msgTime):
        return self._filter.removeSpam(text)


class FloodFilter(IncomingFilter):

    def __init__(self):
        super(FloodFilter, self).__init__()
        self.__history = {}

    def filter(self, text, userId, msgTime = time.time()):
        if not userId or msgTime == 0:
            return text
        else:
            userHistory = self.__history.get(userId)
            if userHistory is None:
                userHistory = self.__history[userId] = []
            recentCount = len(userHistory) + 1
            if recentCount > 1 and userHistory[-1][0] > msgTime:
                userHistory = self.__history[userId] = []
            for hTime, hText in userHistory:
                if msgTime - hTime > MESSAGE_FLOOD_COOLDOWN:
                    recentCount -= 1
                elif text == hText:
                    text = ''
                    break

            userHistory.append((msgTime, text))
            if recentCount < len(userHistory):
                self.__history[userId] = userHistory[-recentCount:]
            return text


class DomainNameFilter(IncomingFilter):

    def __init__(self):
        super(DomainNameFilter, self).__init__()
        g_dnDictionary.resetReplacementFunction()

    def filter(self, text, userId, msgTime):
        return g_dnDictionary.searchAndReplace(text)


class HtmlEscapeFilter(IncomingFilter):

    def filter(self, text, userId, msgTime):
        return html.escape(text)


class OutgoingFilter(object):

    def filter(self, message, isBattle):
        pass


class NormalizeMessageFilter(OutgoingFilter):

    def filter(self, message, isBattle):
        truncated = normalized_unicode_trim(message.strip(), MESSAGE_MAX_LENGTH_IN_BATTLE if isBattle else MESSAGE_MAX_LENGTH)
        return ' '.join(truncated.split())


class FilterChain(object):

    def __init__(self):
        super(FilterChain, self).__init__()
        self.__inFilters = [{'name': 'htmlEscape',
          'filter': HtmlEscapeFilter(),
          'order': 0,
          'lock': True}]
        self.__outFilters = [{'name': 'normalizeMessage',
          'filter': NormalizeMessageFilter(),
          'order': 0,
          'lock': True}]
        self.__inFilterNames = {}
        self.__outFilterNames = {}
        self.__prepareInFilters()
        self.__prepareOutFilters()

    def addFilter(self, name, filter, order = -1, removed = None):
        inFilter = isinstance(filter, IncomingFilter)
        outFilter = isinstance(filter, OutgoingFilter)
        if removed is None:
            removed = []
        if not inFilter and not outFilter or inFilter and outFilter:
            LOG_WARNING('Invalid filter (name = {0:>s}, object = {1!r:s}))'.format(name, filter))
            return
        else:
            if inFilter and not self.__inFilterNames.has_key(name):
                if self.__outFilterNames.has_key(name):
                    LOG_WARNING('Invalid filter (name = {0:>s}, object = {1!r:s})).Filter name must be unique.'.format(name, filter))
                    return
                self.__inFilters.append({'name': name,
                 'filter': filter,
                 'order': order if order > 0 else len(self.__inFilters) + 1,
                 'lock': False})
                for removedName in removed:
                    self.__doRemoveInFilter(removedName)

                self.__prepareInFilters()
            elif inFilter:
                LOG_DEBUG('Filter (name = {0:>s}, object = {1!r:s})) is already added to chain of incoming filters'.format(name, filter))
            if outFilter and not self.__outFilterNames.has_key(name):
                if self.__inFilterNames.has_key(name):
                    LOG_WARNING('Invalid filter (name = {0:>s}, object = {1!r:s})).Filter name must be unique.'.format(name, filter))
                    return
                self.__outFilters.append({'name': name,
                 'filter': filter,
                 'order': order if order > 0 else len(self.__outFilters) + 1,
                 'lock': False})
                for removedName in removed:
                    self.__doRemoveOutFilter(removedName)

                self.__prepareOutFilters()
            elif outFilter:
                LOG_DEBUG('Filter (name = {0:>s}, object = {1!r:s})) is already added to chain of outgoing filters'.format(name, filter))
            return

    def removeFilter(self, name):
        if self.__doRemoveInFilter(name):
            self.__prepareInFilters()
        elif self.__doRemoveOutFilter(name):
            self.__prepareOutFilters()

    def hasFilter(self, name):
        return self.__inFilterNames.has_key(name) or self.__outFilterNames.has_key(name)

    def chainIn(self, message, userId, msgTime):
        for filterInfo in self.__inFilters:
            message = filterInfo['filter'].filter(message, userId, msgTime)

        return message

    def chainOut(self, message, isBattle):
        for filterInfo in self.__outFilters:
            message = filterInfo['filter'].filter(message, isBattle)

        return message

    def __doRemoveInFilter(self, name):
        result = False
        if self.__inFilterNames.has_key(name):
            idx = self.__inFilterNames[name]
            if not self.__inFilters[idx]['lock']:
                self.__inFilters.pop(idx)
                result = True
            else:
                LOG_WARNING('Incoming filter (name = {0:>s}) can not remove.It is locked.'.format(name))
        return result

    def __doRemoveOutFilter(self, name):
        result = False
        if self.__outFilterNames.has_key(name):
            idx = self.__outFilterNames[name]
            if not self.__outFilters[idx]['lock']:
                self.__outFilters.pop(idx)
                result = True
            else:
                LOG_WARNING('Outgoing filter (name = {0:>s}) can not remove.It is locked.'.format(name))
        return result

    def __prepareInFilters(self):
        self.__inFilters = sorted(self.__inFilters, cmp=lambda item, other: cmp(item['order'], other['order']))
        self.__inFilterNames = dict(((filter['name'], idx) for idx, filter in enumerate(self.__inFilters)))

    def __prepareOutFilters(self):
        self.__outFilters = sorted(self.__outFilters, cmp=lambda item, other: cmp(item['order'], other['order']))
        self.__outFilterNames = dict(((filter['name'], idx) for idx, filter in enumerate(self.__outFilters)))