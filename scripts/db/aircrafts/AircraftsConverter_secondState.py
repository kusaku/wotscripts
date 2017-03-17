# Embedded file name: scripts/db/aircrafts/AircraftsConverter_secondState.py
import os
from xml.dom import minidom
pathToFile = 'D://work//source//perforce_WoWP//a_usoltsev_UA1-WW-819_4073//depot//branches//content//balance_stable3//game//hammer//res//scripts//db//aircrafts'
pathToLeafNode = ['root',
 'Airplane',
 'parts',
 'part',
 'upgrade',
 'bBoxes',
 'bbox',
 'absorption']

class XmlParser:

    def __init__(self):
        for root, _, files in os.walk(pathToFile):
            for f in files:
                fullFileName = root + '\\' + f
                if f.lower().endswith('.xml') and os.access(fullFileName, os.W_OK):
                    print ('\nProcessing file:', f)
                    doc = minidom.parse(fullFileName)
                    leafs = []
                    self.getChildNodes(pathToLeafNode, 0, doc, leafs)
                    for leaf in leafs:
                        value = float(leaf.childNodes[0].nodeValue)
                        if value < 10 and value > 0.01:
                            value = 0.8
                        leaf.childNodes[0].nodeValue = str(value)

                    if len(leafs) > 0:
                        f = open(fullFileName, 'w')
                        try:
                            f.write(doc.toxml())
                        finally:
                            f.close()

    def getChildNodes(self, nodePath, nodeLevel, parent, leafs):
        curTagName = nodePath[nodeLevel]
        for child in parent.childNodes:
            if hasattr(child, 'tagName'):
                canProceed = True
                if curTagName == 'part':
                    proceedPath = ['name']
                    proceedLeafs = []
                    self.getChildNodes(proceedPath, 0, child, proceedLeafs)
                    nameStr = proceedLeafs[0].childNodes[0].nodeValue
                    canProceed = nameStr.find('hull') != -1
                if child.tagName == curTagName and canProceed:
                    if nodeLevel < len(nodePath) - 1:
                        self.getChildNodes(nodePath, nodeLevel + 1, child, leafs)
                    else:
                        print ('  Append leaf: ', child.tagName)
                        leafs.append(child)


XmlParser()