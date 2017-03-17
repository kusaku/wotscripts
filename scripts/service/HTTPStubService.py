# Embedded file name: scripts/service/HTTPStubService.py
import ResMgr
import BigWorld
from TwistedWeb import TwistedWeb
from TWResources.json_util import JSONResource
from twisted.web.resource import Resource
from TWResources.DBResource import DBResource
from TWResources.GlobalEntitiesResource import GlobalEntitiesResource
from TWResources.EntitiesResource import EntitiesByNameResource, EntitiesByIDResource
from twisted.internet import defer, reactor, protocol
from twisted.web.server import NOT_DONE_YET
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from http_stub import resources
from service_utils import ServiceConfig, ServiceConfigOption, ServiceConfigFileOption, ServiceConfigPortsOption

class Config(ServiceConfig):
    """
    Configuration class for HTTPGameService.
    """

    class Meta:
        SERVICE_NAME = 'HTTPStubService'
        READ_ONLY_OPTIONS = ['PORTS']

    CONFIG_PATH = ServiceConfigFileOption('server/config/services/http_stub.xml')
    PORTS = ServiceConfigPortsOption([0])
    NETMASK = ServiceConfigOption('', optionName='interface')


class HTTPStubService(TwistedWeb):
    """
    Performs remote execution of entity methods over HTTP.
    """

    def __init__(self):
        TwistedWeb.__init__(self, portOrPorts=Config.PORTS, netmask=Config.NETMASK)

    def createResources(self):
        """ Implements superclass method TwistedWeb.createResources """
        return resources.root