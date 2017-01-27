# Embedded file name: scripts/tools/process_replay/replay_processor.py
import os
from datetime import datetime
import json

def _str(o):
    """
    Helper method to convert the object into JSON friendly format.
    """
    try:
        return vars(o)
    except:
        return str(o)


class ReplayProcessor(object):
    totalTicks = 0
    currentTick = 0
    timestamp = 0
    gameUpdateFrequency = 10
    outputFile = None

    def currentTime(self):
        """
        Convert the tick into real client time.
        """
        dt = datetime.utcfromtimestamp(self.timestamp + self.currentTick / self.gameUpdateFrequency)
        ms = self.currentTick % self.gameUpdateFrequency * 1000000 / self.gameUpdateFrequency
        dt = dt.replace(microsecond=ms)
        return dt.strftime('%F %H:%M:%S:%f')

    def __init__(self, outputFileName):
        """
        Constructor.
        
        @param: outputFileName  The output file name to store replay parsing result content.
        """
        try:
            self.outputFile = open(os.path.abspath(outputFileName), 'w')
        except:
            return False

        return True

    def output(self, data):
        """
        Helper method to write data into output file.
        @param: data    the data string to be written.
        """
        self.outputFile.write(data)

    def JSONify(self, var):
        """
        Helper method to convert given Python variable into JSON format string.
        @param: var     The Python object to be converted.
        """
        return json.dumps(var, default=lambda o: _str(o))

    def onTick(self, currentTick, totalTicks):
        """
        Callback method for a new game tick.
        @param: currentTick     The current tick number
        @param: totalTicks      The total ticks in this replay file.
        """
        self.currentTick = currentTick
        self.totalTicks = totalTicks

    def onMetaData(self, metaData):
        """
        Callback method for replay meta data.
        @param: metaData        The meta data dictionary for the replay file.
        """
        self.output('METADATA: %s\n' % self.JSONify(metaData))
        return True

    def onHeader(self, header):
        """
        Callback method for replay header.
        @param: header  The replay header object.
        """
        self.timestamp = header['timestamp']
        self.gameUpdateFrequency = header['gameUpdateFrequency']
        self.output('HEADER: %s\n' % self.JSONify(header))
        return True

    def onCreate(self, entityName, entityID, properties):
        """
        Callback method for entity creation event.
        @param: entityName      The entity name.
        @param: entityID        The entity ID.
        @param: properties      The entity initialization properties.
        """
        self.output('%s TICK: %s\tCREATE\t%s[%s]: %s\n' % (self.currentTime(),
         self.currentTick,
         entityName,
         entityID,
         self.JSONify(properties)))
        return True

    def onDelete(self, entityName, entityID):
        """
        Callback method for entity deletion event.
        @param: entityName The entity name.
        @param: entityID The entity ID.
        """
        self.output('%s TICK: %s\tDELETE\t%s[%s]\n' % (self.currentTime(),
         self.currentTick,
         entityName,
         entityID))
        return True

    def onMethod(self, entityName, entityID, methodName, methodArgs):
        """
        Callback method for entity method call event.
        @param: entityName The entity name.
        @param: entityID The entity ID.
        @param: methodName The method name.
        @param: methodArgs The method arguments.
        """
        self.output('%s TICK: %s\tMETHOD\t%s[%s].%s( %s )\n' % (self.currentTime(),
         self.currentTick,
         entityName,
         entityID,
         methodName,
         self.JSONify(methodArgs)))
        return True

    def onProperty(self, entityName, entityID, propertyName, propertyValue):
        """
        Callback method for entity property update event.
        @param: entityName The entity name.
        @param: entityID The entity ID.
        @param: propertyName The property name.
        @param: propertyValue The property value.
        """
        self.output('%s TICK: %s\tPROPERTY\t%s[%s].%s = %s\n' % (self.currentTime(),
         self.currentTick,
         entityName,
         entityID,
         propertyName,
         self.JSONify(propertyValue)))
        return True

    def onNestedProperty(self, entityName, entityID, changePath, oldValue, newValue):
        """
        Callback method for entity nested property update event.
        @param: entityName The entity name.
        @param: entityID The entity ID.
        @param: changePath The nested property change path.
        @param: oldValue The old value for this nested property.
        @param: newValue The new value for this nested property.
        """
        self.output('%s TICK: %s\tNESTED_PROPERTY\t%s[%s].%s = %s\n' % (self.currentTime(),
         self.currentTick,
         entityName,
         entityID,
         changePath,
         self.JSONify(newValue)))
        return True

    def onClientChanged(self, entityName, entityID):
        """
        Callback method for client entity change event.'
        @param: entityName The entity name.
        @param: entityID The entity ID.
        """
        self.output('%s TICK: %s\tCLIENT_CHANGED\t%s[%s]\n' % (self.currentTime(),
         self.currentTick,
         entityName,
         entityID))
        return True

    def onAoIChanged(self, witnessName, witnessID, entityName, entityID, isEnter):
        """
        Callback method for AoI change event.
        @param: witnessName The AoI witness entity type name.
        @param: witnessID The AoI witness entity ID.
        @param: entityName The entity name.
        @param: entityID The entity ID.
        @param: isEnter True for enter AoI, False otherwise.
        """
        self.output('%s TICK: %s\tAOI_CHANGED\twitness: %s[%s], entity: %s[%s], isEnter: %s\n' % (self.currentTime(),
         self.currentTick,
         witnessName,
         witnessID,
         entityName,
         entityID,
         isEnter))
        return True

    def onGeometryMapping(self, spaceID, spaceName, entryID, matrix):
        """
        Callback method for space geometry mapping creation event.
        @param: spaceID The space ID.
        @param: spaceName The space name.
        @param: entryID The space mapping entry ID.
        @param: matrix The space mapping matrix.
        """
        self.output('%s TICK: %s\tGEOMETRY_MAPPING\tspaceID: %s, spaceName: %s, entryID: %s matrix: %s\n' % (self.currentTime(),
         self.currentTick,
         spaceID,
         spaceName,
         entryID,
         matrix))
        return True

    def onGeometryMappingDeleted(self, spaceID, entryID):
        """
        Callback method for space geometry mapping deletion event.
        @param: spaceID The space ID.
        @param: entryID The space entry ID.
        """
        self.output('%s TICK: %s\tGEOMETRY_MAPPING_DELETED\tspaceID: %s, entryID: %s\n' % (self.currentTime(),
         self.currentTick,
         spaceID,
         entryID))
        return True

    def onFinish(self):
        """
        Callback method for reaching the end of replay file.
        """
        self.outputFile.close()
        return True

    def help(self):
        """
        Usage method for process_replay Python interface.
        """
        return True