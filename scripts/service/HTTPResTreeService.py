# Embedded file name: scripts/service/HTTPResTreeService.py
import re
import logging
import ResMgr
import BigWorld
from TwistedWeb import TwistedWeb
from twisted.web.resource import Resource
from TWResources.res_tree_resource import ResTreeResource
from service_utils import ServiceConfig, ServiceConfigOption, ServiceConfigFileOption
log = logging.getLogger(__name__)

class Config(ServiceConfig):
    """
    Configuration class for HTTPResTreeService.
    """

    class Meta:
        SERVICE_NAME = 'HTTPResTreeService'

    CONFIG_PATH = ServiceConfigFileOption('server/config/services/http_res_tree.xml')
    NETMASK = ServiceConfigOption('', optionName='interface')


class HTTPResTreeService(TwistedWeb):
    """
    Generic HTTP L{Bigworld.Service} for serving files from the 'res' tree
    subject to simple pattern-based whitelisting.
    
    See also L{ResTreeResource}.
    """
    SERVICE_ADDRESS = 'services/HTTPResTreeService/address'
    SPACEVIEWER_ADDRESS = 'services/data/space_viewer_http'
    PATTERNS = ('/space_viewer_images/\\w+\\.png$', '/space_viewer/')
    ACCESS_LIST = [ re.compile(p) for p in PATTERNS ]

    def __init__(self):
        TwistedWeb.__init__(self, netmask=Config.NETMASK)

    def createResources(self):
        """ Implements superclass method TwistedWeb.createResources """
        root = Resource()
        root.putChild('res', ResTreeResource(whitelist=self.ACCESS_LIST))
        return root

    def initWatchers(self, interface):
        """ Implements superclass method TwistedWeb.initWatchers """
        TwistedWeb.initWatchers(self, interface)
        BigWorld.addWatcher(self.SPACEVIEWER_ADDRESS, lambda : '%s:%d' % (interface.host, interface.port))

    def finiWatchers(self):
        """ Override from TwistedWeb. """
        BigWorld.delWatcher(self.SPACEVIEWER_ADDRESS)
        TwistedWeb.finiWatchers(self)