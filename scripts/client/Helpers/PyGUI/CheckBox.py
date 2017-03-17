# Embedded file name: scripts/client/Helpers/PyGUI/CheckBox.py
import BigWorld, GUI
from Button import Button

class CheckBox(Button):
    factoryString = 'PyGUI.CheckBox'

    def __init__(self, component):
        Button.__init__(self, component)
        self.buttonStyle = Button.CHECKBOX_STYLE

    def onBound(self):
        self._updateVisualState()

    @property
    def buttonIcon(self):
        return self.component.box

    @property
    def buttonLabel(self):
        return self.component.label

    @staticmethod
    def createInternal(texture, text = '', **kwargs):
        c = GUI.Window('')
        c.materialFX = 'BLEND'
        c.widthMode = 'CLIP'
        c.heightMode = 'CLIP'
        c.horizontalPositionMode = 'CLIP'
        c.verticalPositionMode = 'CLIP'
        box = GUI.Simple(texture)
        box.size = (0, 0)
        box.horizontalPositionMode = 'CLIP'
        box.verticalPositionMode = 'CLIP'
        box.horizontalAnchor = 'LEFT'
        box.position.x = -1
        box.materialFX = 'BLEND'
        box.widthMode = 'PIXEL'
        box.heightMode = 'PIXEL'
        box.width = 20
        box.height = 20
        c.addChild(box, 'box')
        label = GUI.Text(text)
        label.horizontalPositionMode = 'CLIP'
        label.verticalPositionMode = 'CLIP'
        label.horizontalAnchor = 'RIGHT'
        label.position.x = 1
        label.colour = (128, 128, 128, 255)
        c.addChild(label, 'label')
        return c

    @staticmethod
    def create(texture, text = '', **kwargs):
        c = CheckBox.createInternal(texture, text, **kwargs)
        b = CheckBox(c, **kwargs)
        b.onBound()
        return c