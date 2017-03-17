# Embedded file name: scripts/client/Helpers/PyGUI/Test.py
import BigWorld
import GUI
from Window import DraggableWindow
from PyGUIEvent import PyGUIEvent
import FocusManager
import IME
from random import random
from functools import partial
from debug_utils import LOG_DEBUG

def clear():
    for x in GUI.roots():
        GUI.delRoot(x)


def _deleteComponent(t):
    if t.parent:
        t.parent.delChild(t)
    else:
        GUI.delRoot(t)


class TestWindow(DraggableWindow):
    factoryString = 'PyGUI.Test.TestWindow'

    def __init__(self, component):
        DraggableWindow.__init__(self, component)

    @PyGUIEvent('button1', 'onClick')
    def buttonClicked(self):
        LOG_DEBUG('TestWindow.buttonClicked')
        t = GUI.Text('Button Clicked!')
        t.colour = (255, 0, 0, 255)
        t.position.y = 0.85
        t.verticalAnchor = 'TOP'
        GUI.addRoot(t)
        BigWorld.callback(2.5, partial(_deleteComponent, t))

    @PyGUIEvent('button2', 'onActivate', True)
    @PyGUIEvent('button2', 'onDeactivate', False)
    def buttonToggled(self, newState):
        self.component.statusLabel.text = 'Toggle state: %s' % ('True' if newState else 'False')

    @PyGUIEvent('slider', 'onBeginDrag')
    def sliderBeginDrag(self, value):
        self.component.draggableStatus.text = 'Dragging (value=%d)' % int(value)

    @PyGUIEvent('slider', 'onEndDrag')
    def sliderEndDrag(self, value):
        self.component.draggableStatus.text = ''

    @PyGUIEvent('slider', 'onValueChanged')
    def sliderValueChanged(self, value):
        self.component.draggableStatus.text = 'Dragging (value=%d)' % int(value)
        self.component.draggableStatus.colour = (int(random() * 127),
         int(random() * 127),
         int(random() * 127),
         255)

    @PyGUIEvent('editField', 'onEnter')
    def editFieldOnEnter(self, text):
        t = GUI.Text('Entered Text: %s' % text)
        t.colour = (255, 0, 0, 255)
        t.position.y = 0.9
        t.verticalAnchor = 'TOP'
        GUI.addRoot(t)
        BigWorld.callback(2.5, partial(_deleteComponent, t))
        self.component.editField.script.setText('')

    @PyGUIEvent('editField', 'onEscape')
    def editFieldOnEscape(self):
        FocusManager.setFocusedComponent(None)
        return

    @PyGUIEvent('editField', 'onChangeFocus')
    def editFieldOnChangeFocus(self, state):
        self.component.editField.script.setText('' if state else 'Enter Text Here')
        self.component.editField.languageIndicator.visible = state


def testWindow():
    BigWorld.setCursor(GUI.mcursor())
    GUI.mcursor().visible = True
    clear()
    w = GUI.load('gui/tests/menu.gui')
    w.script.active(True)
    IME.fini()
    IME.init()
    return w