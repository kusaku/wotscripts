# Embedded file name: scripts/client/Helpers/PyGUI/__init__.py
from PyGUIBase import PyGUIBase
from PyGUIEvent import PyGUIEvent
from Button import Button, ButtonVisualState
from CheckBox import CheckBox
from RadioButton import RadioButton
from ScrollableText import ScrollableText
from EditField import EditField
from Grid import Grid
from Slider import Slider, SliderThumb, SliderVisualState
from ScrollingList import ScrollingList
from ScrollWindow import ScrollWindow
from SmoothMover import SmoothMover
from TextField import TextField
from ToolTip import ToolTip
from ToolTip import ToolTipInfo
from ToolTip import ToolTipManager
from Window import Window
from Window import DraggableWindow
from Window import EscapableWindow
from Console import Console
from LanguageIndicator import LanguageIndicator
from FocusManager import getFocusedComponent, setFocusedComponent, isFocusedComponent
import EditUtils
import Test
import TextStyles
import Utils
import VisualStateComponent
import IME
from Listeners import *
from Helpers.ProgressBar import IProgressBar
from Helpers.ProgressBar import ProgressBar
from Helpers.ProgressBar import ChunkLoadingProgressBar
from Helpers.ProgressBar import TeleportProgressBar

def handleKeyEvent(event):
    import DraggableComponent
    return DraggableComponent.dragManager.handleKeyEvent(event)


def handleMouseEvent(event):
    if ToolTipManager.instance is not None:
        ToolTipManager.instance.handleMouseEvent(event)
    import DraggableComponent
    return DraggableComponent.dragManager.handleMouseEvent(event)


def handleIMEEvent(event):
    import GUI
    handled = False
    import LanguageIndicator
    LanguageIndicator.handleIMEEvent(event)
    focused = getFocusedComponent()
    if focused is not None and hasattr(focused.script, 'handleIMEEvent'):
        handled = focused.script.handleIMEEvent(event)
    import BigWorld
    if not BigWorld.ime.enabled or BigWorld.ime.state == 'OFF':
        IME.hideAll()
    return handled