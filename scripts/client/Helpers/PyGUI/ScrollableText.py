# Embedded file name: scripts/client/Helpers/PyGUI/ScrollableText.py
import BigWorld
import GUI
import re
from PyGUIBase import PyGUIBase
from Helpers.PyGUI.Utils import getHPixelScalar, WHITESPACE
from Helpers.PyGUI.Listeners import registerDeviceListener
import Utils
import StringIO
import string
from debug_utils import LOG_DEBUG
_colourTagLen = len('\\cAABBCCDD;')
_colourTagRE = re.compile('(?<!\\\\)\\\\[cC][0-9a-fA-F]{8};')

def _packColourTag(colour):
    return '\\c%.2x%.2x%.2x%.2x;' % (int(colour[0]),
     int(colour[1]),
     int(colour[2]),
     int(colour[3]))


def _findStartOfWord(s, offset):
    i = offset
    while i >= 0:
        if i >= _colourTagLen and _colourTagRE.match(s, i - _colourTagLen) != None:
            i -= _colourTagLen + 1
            continue
        if s[i] in WHITESPACE:
            return i + 1
        i -= 1

    return -1


def _wrapLine(s, desiredWidth, textComponent):
    """
            Wraps the given string into a list of lines. If there is no
            wrapping performed, a list of length 1 is returned.
    """
    ret = []
    i = 0
    while i < len(s):
        while _colourTagRE.match(s, i) != None and i < len(s):
            i += _colourTagLen

        if i >= len(s):
            break
        subStr = s[:i]
        subStrWidth = textComponent.stringWidth(subStr)
        if subStrWidth > desiredWidth:
            wordStart = _findStartOfWord(s, i)
            if wordStart >= 0:
                subStr = s[:wordStart]
            else:
                while subStrWidth > desiredWidth and i > 0:
                    i -= 1
                    subStr = s[:i]
                    subStrWidth = textComponent.stringWidth(subStr)

                if i == 0:
                    i = 1
                subStr = s[:i]
            ret.append(subStr)
            s = s[len(subStr):]
            i = 0
        else:
            i += 1

    if len(s):
        ret.append(s)
    return ret


class ScrollableText(PyGUIBase):
    factoryString = 'PyGUI.ScrollableText'

    @staticmethod
    def create():
        component = GUI.Window(db.DBLogic.g_instance.getGUITexture('TX_MAP_MASK'))
        component.colour = (128, 128, 128, 255)
        component.widthMode = 'CLIP'
        component.heightMode = 'CLIP'
        component.addChild(GUI.Text(''), 'text')
        component.text.horizontalAnchor = 'LEFT'
        component.text.horizontalPositionMode = 'CLIP'
        component.text.verticalAnchor = 'BOTTOM'
        component.text.verticalPositionMode = 'CLIP'
        component.text.position = (-1.0, -1.0, 0.5)
        component.text.multiline = True
        component.text.richFormatting = True
        component.text.colour = (255, 255, 255, 255)
        component.script = ScrollableText(component)
        component.script.onBound()
        return component

    def __init__(self, component = None):
        PyGUIBase.__init__(self, component)
        self.maxLines = 255
        self.wordWrap = True
        self.minVisibleLines = 4
        self.autoSelectionFonts = ['default_medium.font']
        self.idealCharactersPerLine = 80
        self.lines = []
        self.wrappedLines = []
        self.scrollIndex = 0
        self._displayedLineCount = 0
        registerDeviceListener(self)

    def clear(self):
        self.lines = []
        self.scrollIndex = 0
        self._recalcWrapping()

    def getMaxLines(self):
        return self.maxLines

    def setMaxLines(self, maxLines):
        self.maxLines = maxLines
        self.scrollIndex = min(self.scrollIndex, self.maxLines)
        self.scrollIndex = min(self.scrollIndex, self._displayedLineCount - self.minVisibleLines)
        self._updateScroll()

    def scrollUp(self, amt = 4):
        self.scrollIndex = min(self.scrollIndex + amt, self.maxLines)
        self.scrollIndex = min(self.scrollIndex, self._displayedLineCount - self.minVisibleLines)
        self._updateScroll()

    def scrollDown(self, amt = 4):
        self.scrollIndex = max(self.scrollIndex - amt, 0)
        self._updateScroll()

    def setScrollIndex(self, idx):
        self.scrollIndex = min(idx, self.maxLines)
        self.scrollIndex = max(self.scrollIndex, 0)
        self.scrollIndex = min(self.scrollIndex, self._displayedLineCount - self.minVisibleLines)
        self._updateScroll()

    def onBound(self):
        if len(self.autoSelectionFonts) == 0:
            self.autoSelectionFonts = [self.component.text.font]
        self._recalcFontMetrics()
        self._selectFontBestMatch()

    def onSave(self, dataSection):
        PyGUIBase.onSave(self, dataSection)
        dataSection.writeInt('maxLines', self.maxLines)
        dataSection.writeBool('wordWrap', self.wordWrap)
        dataSection.writeInt('idealCharactersPerLine', self.idealCharactersPerLine)
        if len(self.autoSelectionFonts) > 0:
            dataSection.writeStrings('autoFont', self.autoSelectionFonts)

    def onLoad(self, dataSection):
        PyGUIBase.onLoad(self, dataSection)
        self.maxLines = dataSection.readInt('maxLines', self.maxLines)
        self.wordWrap = dataSection.readBool('wordWrap', self.wordWrap)
        self.idealCharactersPerLine = dataSection.readInt('idealCharactersPerLine', self.idealCharactersPerLine)
        fonts = dataSection.readStrings('autoFont')
        if len(fonts) > 0:
            self.autoSelectionFonts = fonts

    def appendLine(self, str, colour = (255, 255, 255, 255)):
        io = StringIO.StringIO(_packColourTag(colour) + unicode(str))
        newLines = [ unicode(x).rstrip() for x in io.readlines() ]
        if len(newLines) + len(self.lines) >= self.maxLines:
            diff = self.maxLines - len(self.lines)
            self.lines = self.lines[diff:]
        self.lines.extend(newLines)
        widthInPixels = self._widthInPixels()
        for line in newLines:
            wrapped = _wrapLine(line, widthInPixels, self.component.text)
            self.wrappedLines.extend(wrapped)

        self._refillBuffer()
        if self.scrollIndex > 0:
            self.setScrollIndex(self.scrollIndex + len(newLines))

    def onRecreateDevice(self):
        self._selectFontBestMatch()

    def _recalcWrapping(self):
        widthInPixels = self._widthInPixels()
        self.wrappedLines = []
        for x in self.lines:
            self.wrappedLines.extend(_wrapLine(x, widthInPixels, self.component.text))

        self._refillBuffer()

    def _refillBuffer(self):
        buffer = '\n' + '\n'.join(self.wrappedLines)
        self.component.text.text = buffer
        self._displayedLineCount = len(self.wrappedLines)
        self._recalcMaxScroll()
        self._updateScroll()

    def _recalcMaxScroll(self):
        totalPixelHeight = self._lineHeight * self._displayedLineCount
        self.component.minScroll.y = -totalPixelHeight / (BigWorld.screenHeight() * 0.5)

    def _recalcFontMetrics(self):
        _, self._lineHeight = self.component.text.stringDimensions('W')

    def _widthInPixels(self):
        widthMode = self.component.widthMode
        self.component.widthMode = 'PIXEL'
        w = self.component.width
        self.component.widthMode = widthMode
        return w / getHPixelScalar()

    def _updateScroll(self):
        self.component.scroll.y = -self.scrollIndex * (self._lineHeight / (BigWorld.screenHeight() * 0.5))

    def _selectFontBestMatch(self):
        selectedFont = Utils.autoSelectFont(self.autoSelectionFonts, self.idealCharactersPerLine, self._widthInPixels(), self.component.text)
        self.component.text.font = selectedFont
        self._recalcFontMetrics()
        self._recalcMaxScroll()
        self._recalcWrapping()

    @staticmethod
    def test():
        global testUI
        for x in GUI.roots():
            GUI.delRoot(x)

        testUI = ScrollableText().component
        GUI.addRoot(testUI)
        testUI.script.appendLine('AAAA\nBBBB\\CCCC\nDDDD')
        testUI.script.appendLine('XYZ')
        testUI.script.appendLine('ABCD')
        testUI.script.appendLine('EFG')
        testUI.script.appendLine('HIJKL')
        testUI.script.appendLine('VRRRRFRF')
        testUI.script.appendLine('\\cFF0000FF;test one two three four')
        testUI.script.appendLine('\\c00FF00FF;the fat cat sat on the MAT')
        testUI.script.appendLine('\\c0000FFFF;The quick brown fox jumped over the lazy dog')