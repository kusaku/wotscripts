# Embedded file name: scripts/client/gui/GUIHelper.py
import Math
import GUI

def createTextLabel(pos = Math.Vector3(0, 0, 1), text = '', color = (255, 255, 255, 255), font = 'default_small.font', hPosMode = 'CLIP', vPosMode = 'CLIP', hAnchor = 'LEFT', parent = None):
    elem = GUI.Text(text)
    elem.horizontalPositionMode = hPosMode
    elem.verticalPositionMode = vPosMode
    elem.horizontalAnchor = hAnchor
    elem.position = pos
    elem.font = font
    elem.colour = color
    elem.colourFormatting = True
    if parent == None:
        GUI.addRoot(elem)
    else:
        parent.addChild(elem)
    return elem


def createImage(imagePath, position = Math.Vector3(0, 0, 1), size = (0, 0), color = (255, 255, 255, 255), flip = False, hPosMode = 'CLIP', vPosMode = 'CLIP', hAnchor = 'CENTER', vAnchor = 'TOP', sizeMode = 'PIXEL'):
    image = GUI.Simple(imagePath)
    image.horizontalPositionMode = hPosMode
    image.verticalPositionMode = vPosMode
    image.horizontalAnchor = hAnchor
    image.verticalAnchor = vAnchor
    image.flip = flip
    image.materialFX = 'BLEND'
    image.widthMode = sizeMode
    image.heightMode = sizeMode
    image.pixelSnap = True
    image.size = size
    image.colour = color
    image.position = position
    return image