# Embedded file name: scripts/service/HTTPReplayService.py
import BackgroundTask
from service_utils import ServiceConfig, ServiceConfigOption, ServiceConfigFileOption, ServiceConfigPortsOption
from TwistedWeb import TwistedWeb
from twisted.internet import abstract, defer, interfaces, reactor, task
from twisted.python.failure import Failure
from twisted.web.resource import Resource, NoResource
from twisted.web.server import NOT_DONE_YET
from twisted.web.static import File
from twisted.web.util import redirectTo
from zope.interface import implements
import BigWorld
import ResMgr
import importlib
import json
import logging
from math import floor
import os
import threading
import time
log = logging.getLogger(__name__)
_childNotFound = NoResource('File not found.')

def fileProducerFactory(f):
    """
    Decorator for nominating a file producer factory function.
    """
    Config.FILE_PRODUCER_FACTORY = staticmethod(f)
    return f


class MetaDataDelayProvider(object):
    """
    This class is a delay value provider using a specific key's value present
    in meta-data.
    """

    def __init__(self, metaDataKey):
        """
        Constructor.
        
        @param metaDataKey              The meta-data key to use for getting the delay
                                                        provider.
        """
        self._metaDataKey = metaDataKey

    def __call__(self, fileProducer, metaData):
        """
        This method provides the delay based on the meta-data key.
        """
        try:
            return float(metaData.get(self._metaDataKey, Config.DEFAULT_FILE_PRODUCER_FACTORY_READ_DELAY))
        except:
            return Config.DEFAULT_FILE_PRODUCER_FACTORY_READ_DELAY


defaultDelayProvider = MetaDataDelayProvider('delay')

def defaultFileProducerFactory(request, fileReader, offset):
    """
    Default file producer factory function.
    
    To nominate a different function in code, use the @fileProducerFactory
    decorator. It can also be changed at run-time by setting the
    Config.FILE_PRODUCER_FACTORY option to a qualified function name.
    
    @param request          The Twisted web request object.
    @param fileReader       The file reader object for this request.
    @param offset           The requested file offset to start from.
    """
    return FileProducer(request, fileReader, offset, defaultDelayProvider)


def fileProducerFactoryOptionConverter(qualifiedFunctionName):
    """
    This method converts watcher input and interprets it as a qualified name of
    a function. e.g. some.module.function would be interpreted by importing
    some.module and using function inside the module as the factory function.
    """
    if '.' not in qualifiedFunctionName:
        raise ValueError('Invalid module name')
    moduleName, factoryName = qualifiedFunctionName.rsplit('.', 1)
    factoryModule = importlib.import_module(moduleName)
    return staticmethod(getattr(factoryModule, factoryName))


class Config(ServiceConfig):
    """
    Configuration class for HTTPReplayService.
    """

    class Meta:
        SERVICE_NAME = 'HTTPReplayService'
        READ_ONLY_OPTIONS = ['CONFIG_PATH',
         'NETMASK',
         'PORTS',
         'CHUNK_SIZE',
         'SEND_BUFFER_SIZE',
         'CHUNK_EXPIRE_TIME',
         'FILE_EXPIRE_TIME',
         'REOPEN_WAIT_TIME',
         'TICK_RATE',
         'WAIT_READ_TIMEOUT',
         'IDLE_TICK_LIMIT']

    CONFIG_PATH = ServiceConfigFileOption('server/config/services/http_replay.xml')
    NETMASK = ServiceConfigOption('', optionName='interface')
    PORTS = ServiceConfigPortsOption([0])
    DOCUMENT_ROOT = ''
    CHUNK_SIZE = abstract.FileDescriptor.bufferSize
    SEND_BUFFER_SIZE = abstract.FileDescriptor.bufferSize
    CHUNK_EXPIRE_TIME = 3
    FILE_EXPIRE_TIME = 4
    REOPEN_WAIT_TIME = 8.0
    TICK_RATE = 0.25
    WAIT_READ_TIMEOUT = 30.0
    IDLE_TICK_LIMIT = FILE_EXPIRE_TIME * TICK_RATE + 1
    FILE_PRODUCER_FACTORY = ServiceConfigOption(staticmethod(defaultFileProducerFactory), converter=fileProducerFactoryOptionConverter)
    DEFAULT_FILE_PRODUCER_FACTORY_READ_DELAY = 0.0
    REPLAY_FILE_CACHE_READ_BLOCK_SIZE = 1024
    REPLAY_FILE_CACHE_REFRESH_MIN_TIME = 5.0
    SHOULD_MATCH_FILENAMES_AT_TOP_LEVEL = False


class ReplayFileReadingTask(BackgroundTask.BackgroundTask):
    """
    This task is responsible for periodically running file reading operations
    in the background.
    """

    def __init__(self, replaySender):
        """
        Constructor.
        
        @param replaySender     The replay sender instance.
        """
        self._loopingTask = task.LoopingCall(self.tick)
        self._replaySender = replaySender
        self._isPending = False

    def doBackgroundTask(self, mgr, threadData):
        """
        Override from BackgroundTask.
        """
        self._replaySender.backgroundTick()
        mgr.addMainThreadTask(self)

    def doMainThreadTask(self, mgr):
        """
        Override from BackgroundTask.
        """
        self._replaySender.tick()
        self._isPending = False

    def tick(self):
        """
        This is called in the main thread periodically via the LoopingCall.
        """
        if not self._replaySender.bgTaskMgr:
            self._loopingTask.stop()
            return
        if self._isPending:
            return
        self._replaySender.bgTaskMgr.addBackgroundTask(self)
        self._isPending = True

    def start(self, tickRate):
        """
        This method starts the timer for periodic file operations.
        """
        self._loopingTask.start(tickRate)

    def stop(self):
        """
        This method stops the timer for periodic file operations.
        """
        self._loopingTask.stop()


class ReplaySender(object):
    """
    This class is responsible for broadcasting file data to clients.
    """

    def __init__(self):
        """Constructor."""
        self.activeFiles = {}
        self.clients = []
        self.task = None
        self.isTaskRunning = False
        self.idleTicks = 0
        self.bgTaskMgr = None
        return

    def setup(self, bgTaskMgr):
        """
        This method initiates the broadcasting.
        """
        self.bgTaskMgr = bgTaskMgr
        self.task = ReplayFileReadingTask(self)

    def tearDown(self):
        """
        This method cleans up after the service is shut down.
        """
        self.bgTaskMgr = None
        self.task.stop()
        self.task = None
        return

    def backgroundTick(self):
        """
        This method is called periodically to read file data in the background.
        """
        for fileReader in self.activeFiles.values():
            fileReader.backgroundTick()

    def tick(self):
        """
        This method is called periodically to broadcast the data to clients in
        chunks.
        """
        expireTime = time.time() - Config.FILE_EXPIRE_TIME
        for filename, fileReader in list(self.activeFiles.items()):
            if fileReader.lastUsed < expireTime:
                del self.activeFiles[filename]
            else:
                fileReader.tick()

        if self.clients:
            self.idleTicks = 0
        else:
            self.idleTicks += 1
        if self.idleTicks > Config.IDLE_TICK_LIMIT and self.isTaskRunning and not self.clients and not self.activeFiles:
            self.isTaskRunning = False
            self.task.stop()
            return
        for producer in self.clients:
            producer.write()

    def removeClient(self, client):
        """
        This method removes a client, given the client's producer.
        
        @param client   The file producer.
        """
        try:
            self.clients.remove(client)
        except ValueError:
            pass

    def addClient(self, client):
        """
        This method adds a client, given its producer.
        
        @param client   The file producer.
        """
        self.clients.append(client)
        if not self.isTaskRunning:
            self.isTaskRunning = True
            self.task.start(Config.TICK_RATE)

    def openPath(self, path):
        """
        This method returns the file reader for the given path. If none exists,
        a new FileReader is created. File readers expire after not being used
        for a time, see Config.FILE_EXPIRE_TIME.
        
        @param path     The file reader.
        """
        if path in self.activeFiles:
            return self.activeFiles[path]
        fileReader = FileReader(path)
        self.activeFiles[path] = fileReader
        return fileReader


_replaySender = ReplaySender()

class Chunk(object):
    """
    This class is represents a cached fixed-size block of a file. The Chunk
    object loads as much data is available from the file at construction.
    
    @attribute index        The chunk index assigned to this chunk.
    @attribute data         The chunk data. Use getData() to retrieve the data
                                            instead of accessing data directly.
    @attribute lastUsed The time this object was last accessed for reading.
    
    @see Config.CHUNK_SIZE
    """

    def __init__(self, fileOffset):
        """
        Constructor.
        
        Loads a chunk from the given file. The file is divided into
        Config.CHUNK_SIZE-sized chunks, each chunk is addressed by a chunk
        index.
        
        @param index    The file offset of the start of the chunk.
        @param f                The file to read from.
        """
        self.fileOffset = fileOffset
        self.data = ''
        self.lastUsed = time.time()
        self.lastRead = time.time()

    def loadMore(self, f):
        """
        This method loads more data from the file, up to Config.CHUNK_SIZE
        bytes.
        
        @param f        The file to read from.
        
        @return         The amount of new data read.
        """
        if len(self.data) >= Config.CHUNK_SIZE:
            return
        f.seek(self.fileOffset + len(self.data), 0)
        chunk = f.read(Config.CHUNK_SIZE - len(self.data))
        if chunk:
            self.lastRead = time.time()
            self.data += chunk
        return len(chunk)

    def scrub(self, offset):
        """
        This method is used to scrub known bad data from a chunk in the cache,
        forcing it to be re-read in the next background tick.
        
        This is useful when we have unreliable network filesystems that decide
        to supply zeroes near the end-of-file rather than reporting a short
        count for read operations.
        """
        self.data = self.data[offset:]

    def getData(self, start, length):
        """
        This method returns the data read from the file, using the given chunk
        offset and length.
        
        @param start    The start of the data to retrieve, as a byte offset
                                        from the start of this chunk.
        @param length   The length of the data to request for retrieval.
        
        @return                 The available data within the given range, or None if
                                        no data in the given range is available. The returned
                                        data may be shorter than the requested length,
                                        depending on proximity to the chunk boundary.
        """
        self.lastUsed = time.time()
        if start >= len(self.data):
            return None
        else:
            return self.data[start:start + length]

    @property
    def isComplete(self):
        """
        This property returns whether the data read for this chunk is complete.
        """
        return len(self.data) == Config.CHUNK_SIZE


class FileReader(object):
    """
    This class reads data from a file, caching the read data into fixed-size
    chunks.
    """

    def __init__(self, path):
        """
        Constructor.
        
        @param path     The path to the file to open.
        """
        self.path = path
        self.cache = {}
        self.lastUsed = time.time()
        self.f = None
        self.stat = None
        return

    def openFile(self):
        """
        This method opens (or re-opens) the file for reading.
        """
        if self.f:
            self.f.close()
        self.f = open(self.path, 'rb')

    def name(self):
        """
        Accessor for the file path.
        """
        return self.f.name

    def read(self, offset, length):
        """
        This method reads data from the given file offset with the given
        length. The returned data may be shorter than the requested length.
        
        @param offset   The file offset to read from.
        @param length   The requested length of the data.
        
        @return                 The data from the file. This data will be cached for
                                        a time (see Config.CHUNK_EXPIRE_TIME) before being
                                        released from memory.
        """
        self.lastUsed = time.time()
        chunkIndex = offset // Config.CHUNK_SIZE
        chunkOffset = offset % Config.CHUNK_SIZE
        chunk = None
        if chunkIndex in self.cache:
            chunk = self.cache[chunkIndex]
        else:
            chunk = self.cache[chunkIndex] = Chunk(chunkIndex * Config.CHUNK_SIZE)
        return chunk.getData(chunkOffset, length)

    def scrub(self, offset):
        """
        This method scrubs the data from immediate chunk around the given
        offset.
        
        @param offset   The offset to scrub from, until the next chunk
                                        boundary.
        """
        chunkIndex = offset // Config.CHUNK_SIZE
        chunkOffset = offset % Config.CHUNK_SIZE
        try:
            chunk = self.cache[chunkIndex]
        except KeyError:
            return

        chunk.scrub(chunkOffset)

    def backgroundTick(self):
        """
        This method processes file reading tasks in the background thread.
        """
        if self.f is None:
            self.openFile()
        self.stat = os.fstat(self.f.fileno())
        lastChunkIndex = None
        lastChunk = None
        lastChunkRead = 0
        for index, chunk in self.cache.items():
            amountRead = chunk.loadMore(self.f)
            if lastChunkIndex is None or index > lastChunkIndex:
                lastChunkIndex = index
                lastChunk = chunk
                lastChunkRead = amountRead
            if not amountRead and time.time() - lastChunk.lastRead > Config.REOPEN_WAIT_TIME:
                log.info('FileReader.tick: Re-opening file path: %r', self.path)
                lastChunk.lastRead = time.time()
                self.openFile()

        return

    def tick(self):
        """
        This method processes file readers and producers to clients.
        """
        if not self.cache:
            return
        else:
            lastChunkIndex = None
            lastChunk = None
            expireTime = time.time() - Config.CHUNK_EXPIRE_TIME
            for index, chunk in list(self.cache.items()):
                if chunk.lastUsed < expireTime:
                    del self.cache[index]
                elif lastChunkIndex is None or index > lastChunkIndex:
                    lastChunkIndex = index
                    lastChunk = chunk

            if lastChunk is not None and lastChunk.isComplete:
                self.cache[lastChunkIndex + 1] = Chunk((lastChunkIndex + 1) * Config.CHUNK_SIZE)
            return


class FileProducer(object):
    """
    This class produces file data for a web request.
    """
    implements(interfaces.IPushProducer)

    def __init__(self, request, fileReader, offset, readDelayProvider = defaultDelayProvider):
        """
        Constructor.
        
        @param request                          The request to serve file data for.
        @param fileReader                       The file reader to read data from.
        @param offset                           The initial file offset to read from.
        @param readDelayProvider        The read delay provider to use. This is an
                                                                object that is callable with this object
                                                                and the meta-data dictionary as arguments,
                                                                called when meta-data is read.
        """
        self.request = request
        self.fileReader = fileReader
        self.offset = offset
        self.readDelay = None
        self.readDelayProvider = readDelayProvider
        self.failReadCount = 0
        self.isPaused = True
        self.replayFileReader = BigWorld.ReplayDataFileReader('', False)
        self.replayFileReader.listener = self
        self.lastReadTime = time.time()
        self.lastGoodReadTime = time.time()
        log.info('FileProducer.__init__: Started streaming %s to %s:%d', fileReader.path, self.request.client.host, self.request.client.port)
        return

    def onReplayDataFileReaderMetaData(self, reader, metaData):
        """
        Callback from the replay file reader when meta-data has been read.
        """
        self.readDelay = self.readDelayProvider(self, metaData)

    def start(self):
        """
        This method starts the producer, beginning writing out of file data.
        """
        self.request.registerProducer(self, True)
        self.isPaused = False

    def write(self):
        """
        This method writes an amount of data to the client.
        """
        if self.isPaused:
            return
        elif not self.request:
            return
        else:
            data = self.fileReader.read(self.offset, Config.SEND_BUFFER_SIZE)
            now = time.time()
            MODE_WRITE_BITS = 146
            if data is None:
                if self.offset == self.fileReader.stat.st_size and self.fileReader.stat.st_mode & MODE_WRITE_BITS == 0:
                    log.info('FileProducer.write( %s ): Finished sending to client %s:%d', self.fileReader.path, self.request.client.host, self.request.client.port)
                    self.disconnect()
                elif now - self.lastReadTime >= Config.WAIT_READ_TIMEOUT:
                    log.error('FileProducer.write( %s ): Disconnecting client %s:%d due to no new data read after %.01fs (but still read-writeable)', self.fileReader.path, self.request.client.host, self.request.client.port, now - self.lastReadTime)
                    self.disconnect()
                return
            self.lastReadTime = now
            dataToAdd = data
            if self.replayFileReader.numBytesAdded > self.offset:
                dataToAdd = data[self.replayFileReader.numBytesAdded - self.offset:]
            try:
                self.replayFileReader.addData(dataToAdd)
                self.lastGoodReadTime = now
            except Exception as e:
                self.fileReader.scrub(self.offset)
                if now - self.lastGoodReadTime >= Config.WAIT_READ_TIMEOUT:
                    log.error('FileProducer.write( %s ): Disconnecting client %s:%d due to persistent bad data reading after %.01fs', self.fileReader.path, self.request.client.host, self.request.client.port, now - self.lastGoodReadTime)
                    self.disconnect()
                else:
                    self.replayFileReader.clearError()
                return

            if self.replayFileReader.header is None:
                return
            now = time.time()
            numSecondsRead = self.replayFileReader.numTicksRead / float(self.replayFileReader.header.gameUpdateFrequency)
            if self.readDelay is None or self.replayFileReader.header.timestamp + numSecondsRead + self.readDelay > now:
                return
            self.request.write(data)
            self.offset += len(data)
            self.failReadCount = 0
            HTTPReplayService.bytesSent += len(data)
            return

    def disconnect(self):
        """
        This method is called to finish sending data to the client.
        """
        self.request.unregisterProducer()
        self.request.finish()
        self.stopProducing()

    def pauseProducing(self):
        """
        Override from IPushProducer.
        """
        _replaySender.removeClient(self)
        self.isPaused = True

    def resumeProducing(self):
        """
        Override from IPushProducer.
        """
        _replaySender.addClient(self)
        self.isPaused = False
        self.write()

    def stopProducing(self):
        """
        Override from IPushProducer.
        """
        _replaySender.removeClient(self)
        self.request = None
        return


class ReplayFileDescriptor(object):
    """
    This class represents a descriptor for a replay file.
    """

    def __init__(self, path, stat, header, metaData):
        """
        Constructor.
        
        @param path     The file resource path.
        @param stat     The stat() of the file.
        @param header   The replay header.
        @param metaData The replay meta-data.
        """
        self._path = path
        self._stat = stat
        self._header = header
        self._metaData = metaData

    @property
    def path(self):
        """
        This attribute is the resource path of the replay file.
        """
        return self._path

    @property
    def stat(self):
        """
        This attribute is the results of stat() on the replay file.
        """
        return self._stat

    @property
    def header(self):
        """
        This attribute is the header of the replay file, as a dict.
        """
        return self._header

    @property
    def metaData(self):
        """
        This attribute is the meta-data of the replay file.
        """
        return self._metaData

    def __str__(self):
        return '<ReplayFileDescriptor: %s>' % self._path


class ReplayFileInfoDescriptorEncoder(json.JSONEncoder):
    """
    This class extends JSONEncoder to encode ReplayFileDescriptor.
    """

    def __init__(self, documentRoot, *args, **kwargs):
        """
        Constructor.
        
        @param documentRoot     The top-level recordings directory.
        """
        json.JSONEncoder.__init__(self, *args, **kwargs)
        self._documentRoot = documentRoot

    def default(self, obj):
        """
        Override from JSONEncoder.
        """
        if isinstance(obj, ReplayFileDescriptor):
            path = obj.path
            if path.startswith(self._documentRoot):
                path = obj.path[len(self._documentRoot):]
                if path.startswith('/'):
                    path = path[1:]
            return dict(path=path, size=obj.stat.st_size, mtime=obj.stat.st_mtime, header=obj.header, metaData=obj.metaData)
        return json.JSONEncoder.default(self, obj)


class ReplayHeaderReader(object):
    """
    This class reads a replay file until the header and meta-data have been
    read.
    """

    def __init__(self, path):
        """
        Constructor.
        
        @param path     The replay file resource path.
        """
        self._path = path
        self._stat = None
        self._header = None
        self._metaData = None
        return

    def getDescriptor(self, previousDescriptor = None):
        """
        This method returns the descriptor for this file by reading the header
        and meta-data.
        
        @param  previousDescriptor      A copy of the previous descriptor. If the
                                                                modification time is the same, this is
                                                                returned straight-away.
        
        @return a descriptor for the replay file.
        """
        reader = BigWorld.ReplayDataFileReader()
        reader.listener = self
        absPath = ResMgr.resolveToAbsolutePath(self._path)
        self._stat = os.stat(absPath)
        if previousDescriptor and self._stat.st_mtime == previousDescriptor.stat.st_mtime:
            return previousDescriptor
        else:
            with open(self._path, 'rb') as f:
                isDone = False
                while not isDone:
                    block = f.read(Config.REPLAY_FILE_CACHE_READ_BLOCK_SIZE)
                    if not block:
                        isDone = True
                    else:
                        reader.addData(block)
                        if self._header is not None and self._metaData is not None:
                            isDone = True

                if self._header is None or self._metaData is None:
                    raise ValueError('Invalid replay file')
                return ReplayFileDescriptor(self._path, self._stat, self._header, self._metaData)
            return

    def onReplayDataFileReaderHeader(self, reader, header):
        """
        This method is callback from the replay file reader when the header has
        been read.
        
        @param reader   The reader instance.
        @param header   The header.
        """
        self._header = dict(version=header.version, digest=header.digest, numTicks=header.numTicks, timestamp=header.timestamp)

    def onReplayDataFileReaderMetaData(self, reader, metaData):
        """
        This method is a callback from the replay file reader when the
        meta-data block has been read.
        
        @param reader   The reader instance.
        @param metaData The meta-data as a dictionary of key-value pairs.
        """
        self._metaData = metaData


def resmgrwalk(path, *args, **kwargs):
    """
    Wrapper for os.walk() to use resource paths.
    """
    absolutePath = ResMgr.resolveToAbsolutePath(path)
    absolutePathLocation = absolutePath[:-len(path)]
    for path, dirList, fileList in os.walk(absolutePath, *args, **kwargs):
        path = path[len(absolutePathLocation):]
        yield (path, dirList, fileList)


class IsFileCheckTask(BackgroundTask.BackgroundTask):
    """
    This class checks for a file's existence in the background,
    calling back on a deferred in the main thread.
    """

    def __init__(self, path, deferred):
        self._path = path
        self._deferred = deferred
        self._result = None
        return

    def doBackgroundTask(self, mgr, threadData):
        self._result = ResMgr.isFile(self._path)
        mgr.addMainThreadTask(self)

    def doMainThreadTask(self, mgr):
        self._deferred.callback(self._result)


class ReplayFileCacheRefreshTask(BackgroundTask.BackgroundTask):
    """
    This class is a task for traversing the recordings directory and reading
    file data in the background.
    """

    def __init__(self, cache, documentRoot, originalDescriptors):
        """
        Constructor.
        
        @param cache                    The replay file cache to refresh.
        @param documentRoot     The top-level recordings directory.
        @param originalDescriptors
                                                        The results from a previous refresh. Files that
                                                        haven't been modified since the previous
                                                        refresh will be assumed to have stayed the
                                                        same.
        """
        self._descriptors = {}
        self._cache = cache
        self._documentRoot = documentRoot
        self._originalDescriptors = originalDescriptors

    def doBackgroundTask(self, mgr, threadData):
        """
        Override from BackgroundTask.
        """
        for path, dirList, fileList in resmgrwalk(self._documentRoot):
            for fileName in fileList:
                filePath = os.path.join(path, fileName)
                reader = ReplayHeaderReader(filePath)
                try:
                    descriptor = reader.getDescriptor(self._originalDescriptors.get(filePath, None))
                    self._descriptors[descriptor.path] = descriptor
                except ValueError as e:
                    continue

        mgr.addMainThreadTask(self)
        return

    def doMainThreadTask(self, mgr):
        """
        Override from BackgroundTask.
        """
        self._cache.onRefreshTaskComplete(self._descriptors)


class ReplayFileCache(object):
    """
    This class holds cached replay file descriptors.
    """

    def __init__(self, taskMgr, documentRoot):
        """
        Constructor.
        
        @param taskMgr                  A background task manager instance.
        @param documentRoot     The top-level recordings directory.
        """
        self._documentRoot = documentRoot
        self._files = {}
        self._taskMgr = taskMgr
        self._task = None
        self._deferred = None
        self._lastRefreshTime = None
        return

    @property
    def files(self):
        """
        This attribute returns an iterator through the cached file descriptors.
        """
        return iter(self._files.values())

    def startRefresh(self):
        """
        Request to refresh the cache. Returns a deferred which can be be used
        to register a callback when complete. 
        
        May not actually refresh the cache if too soon since the last refresh.
        """
        if self._task is None:
            if self._lastRefreshTime is not None and time.time() - self._lastRefreshTime < Config.REPLAY_FILE_CACHE_REFRESH_MIN_TIME:
                return defer.succeed(self._files.values())
            self._deferred = defer.Deferred()
            self._task = ReplayFileCacheRefreshTask(self, self._documentRoot, self._files)
            self._taskMgr.addBackgroundTask(self._task)
        return self._deferred

    def onRefreshTaskComplete(self, descriptors):
        """
        Called when the background refresh task completes.
        
        @param descriptors      The new descriptors.
        """
        if self._deferred is None:
            return
        else:
            self._files = descriptors
            self._task = None
            self._lastRefreshTime = time.time()
            self._deferred.callback(self.files)
            self._deferred = None
            return

    def stop(self):
        """
        Called to cancel a pending task.
        """
        self._task = None
        self._deferred = None
        return


class ReplayResource(Resource):
    """
    This class implements a resource for streaming a replay file.
    """

    def __init__(self, path, bgTaskMgr):
        """
        Constructor.
        
        @param path             The path to the file to serve.
        """
        Resource.__init__(self)
        self._path = path
        self._bgTaskMgr = bgTaskMgr

    def render_GET(self, request):
        """
        Override from Resource.
        """
        deferred = defer.Deferred()

        def callback(isFileResult):
            if not isFileResult:
                request.render(_childNotFound)
                return
            else:
                request.setHeader('Content-Type', 'application/octet-stream')
                offset = request.getHeader('Range')
                if offset == None:
                    offset = 0
                else:
                    offset = int(offset[0:offset.find('-')])
                request.setHeader('Content-Range', 'bytes */*')
                reader = _replaySender.openPath(self._path)
                producer = Config.FILE_PRODUCER_FACTORY(request, reader, offset)
                producer.start()
                _replaySender.addClient(producer)
                return

        deferred.addCallback(callback)
        task = IsFileCheckTask(self._path, deferred)
        self._bgTaskMgr.addBackgroundTask(task)
        return NOT_DONE_YET


class ReplayJSONListResource(Resource):

    def __init__(self, bgTaskMgr, cache, documentRoot):
        """
        Constructor.
        
        @param cache            The ReplayFileCache.
        @param documentRoot The replay file document root.
        """
        Resource.__init__(self)
        self._bgTaskMgr = bgTaskMgr
        self._cache = cache
        self._documentRoot = documentRoot

    def getChild(self, path, request):
        """
        Override from Resource.
        """
        if not path:
            return self
        filePath = os.path.join(self._documentRoot, path)
        return ReplayResource(filePath, self._bgTaskMgr)

    def render_GET(self, request):
        """
        Override from Resource.
        """
        deferred = self._cache.startRefresh()
        requestedVersion = request.args.get('version', [None])[0]
        requestedDigest = request.args.get('digest', [None])[0]
        requestedAllMetaData = request.args.get('meta_data_match', [])
        requestedAnyMetaData = request.args.get('meta_data_any', [])

        def metaDataMatch(descriptor):
            for match in requestedAllMetaData:
                try:
                    key, value = match.split(':')
                    if descriptor.metaData.get(key) != value:
                        return False
                except:
                    return False

            if requestedAnyMetaData:
                for match in requestedAnyMetaData:
                    try:
                        key, value = match.split(':')
                        if descriptor.metaData.get(key) == value:
                            return True
                    except:
                        return False

                return False
            return True

        def callback(files):
            request.setHeader('Content-Type', 'application/json')
            filteredFiles = [ f for f in files if (requestedVersion is None or f.header['version'] == requestedVersion) and (requestedDigest is None or f.header['digest'] == requestedDigest) and metaDataMatch(f) ]
            encoder = ReplayFileInfoDescriptorEncoder(self._documentRoot, separators=(',', ':'))
            for chunk in encoder.iterencode(filteredFiles):
                request.write(chunk)

            request.finish()
            return

        deferred.addCallback(callback)
        return NOT_DONE_YET


class ReplayHTMLIndexResource(Resource):
    """
    This class implements a resource for rendering an index view of the replay
    directory.
    """

    def __init__(self, cache, documentRoot):
        """
        Constructor.
        
        @param documentRoot     The directory to serve recordings from.
        """
        self._cache = cache
        self._documentRoot = documentRoot
        Resource.__init__(self)

    def getChild(self, path, request):
        """
        Override from Resource.
        """
        if not path:
            return self
        return _childNotFound

    def render_GET(self, request):
        """
        Override from Resource.
        """
        deferred = self._cache.startRefresh()

        def callback(files):
            request.setHeader('Content-Type', 'text/html')
            request.write('<html><body><h1>Index of %s</h1><ul>' % self._documentRoot)
            for fileDescriptor in files:
                path = fileDescriptor.path
                if path.startswith(self._documentRoot):
                    path = path[len(self._documentRoot):]
                    if path.startswith('/'):
                        path = path[1:]
                hrefPath = '/replays/' + path
                request.write('<li><a href="%s">%s</a> (%s, %d bytes)</li>' % (hrefPath,
                 path,
                 'live' if fileDescriptor.header['numTicks'] == 0 else 'complete',
                 fileDescriptor.stat.st_size))

            request.write('</ul></body></html>')
            request.finish()

        deferred.addCallback(callback)
        return NOT_DONE_YET


class TopLevelResource(Resource):
    """
    The top-level resource.
    """

    def __init__(self, bgTaskMgr, replayFileCache, documentRoot):
        """
        Constructor.
        
        @param replayFileCache  The replay file cache.
        @param documentRoot     The top-level recordings directory.
        """
        Resource.__init__(self)
        self._bgTaskMgr = bgTaskMgr
        self._documentRoot = documentRoot
        self._htmlIndex = ReplayHTMLIndexResource(replayFileCache, documentRoot)
        self._jsonList = ReplayJSONListResource(bgTaskMgr, replayFileCache, documentRoot)

    def getChild(self, path, request):
        """ Override from Resource. """
        if path == 'html':
            return self._htmlIndex
        if path == 'replays':
            return self._jsonList
        if path:
            filePath = os.path.join(self._documentRoot, path)
            if not Config.SHOULD_MATCH_FILENAMES_AT_TOP_LEVEL:
                return _childNotFound
            return ReplayResource(filePath, self._bgTaskMgr)
        return self

    def render_GET(self, request):
        """ Override from Resource. """
        return redirectTo('/html', request)


class HTTPReplayService(TwistedWeb):
    """
    Generic HTTP L{Bigworld.Service} for serving files from the 'res' tree
    subject to simple pattern-based whitelisting.
    
    See also L{ResTreeResource}.
    """
    bytesSent = 0

    def __init__(self):
        """
        Constructor.
        """
        self._bgTaskMgr = BackgroundTask.Manager()
        self._bgTaskMgr.startThreads(1)
        self._replayFileCache = ReplayFileCache(self._bgTaskMgr, Config.DOCUMENT_ROOT)
        self._topLevelResource = TopLevelResource(self._bgTaskMgr, self._replayFileCache, Config.DOCUMENT_ROOT)
        TwistedWeb.__init__(self, portOrPorts=Config.PORTS, netmask=Config.NETMASK)

    def createResources(self):
        """ Implements superclass method TwistedWeb.createResources """
        reactor.callWhenRunning(lambda : _replaySender.setup(self._bgTaskMgr))
        return self._topLevelResource

    def initWatchers(self, interface):
        """ Overrides superclass method TwistedWeb.initWatchers """
        TwistedWeb.initWatchers(self, interface)
        BigWorld.addWatcher('services/HTTPReplayService/bytesSent', lambda : '%d' % HTTPReplayService.bytesSent)
        BigWorld.addWatcher('services/HTTPReplayService/clientsInQueue', lambda : '%d' % len(_replaySender.clients))
        BigWorld.addWatcher('services/HTTPReplayService/activeFiles', lambda : '%d' % len(_replaySender.activeFiles))
        BigWorld.addWatcher('services/HTTPReplayService/isTaskRunning', lambda : ('true' if _replaySender.isTaskRunning else 'false'))

    def finiWatchers(self):
        """ Override from TwistedWeb. """
        BigWorld.delWatcher('services/HTTPReplayService/bytesSent')
        BigWorld.delWatcher('services/HTTPReplayService/clientsInQueue')
        BigWorld.delWatcher('services/HTTPReplayService/activeFiles')
        BigWorld.delWatcher('services/HTTPReplayService/isTaskRunning')
        TwistedWeb.finiWatchers(self)

    def onDestroy(self):
        self._replayFileCache.stop()
        _replaySender.tearDown()
        self._bgTaskMgr.stopAll()