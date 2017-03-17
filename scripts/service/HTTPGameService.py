# Embedded file name: scripts/service/HTTPGameService.py
import ResMgr
import BigWorld
from TwistedWeb import TwistedWeb
from TWResources.json_util import JSONResource
from TWResources.DBResource import DBResource
from TWResources.GlobalEntitiesResource import GlobalEntitiesResource
from TWResources.EntitiesResource import EntitiesByNameResource, EntitiesByIDResource
from service_utils import ServiceConfig, ServiceConfigOption, ServiceConfigFileOption

class Config(ServiceConfig):
    """
    Configuration class for HTTPGameService.
    """

    class Meta:
        SERVICE_NAME = 'HTTPGameService'

    CONFIG_PATH = ServiceConfigFileOption('server/config/services/http_game.xml')
    NETMASK = ServiceConfigOption('', optionName='interface')


class HTTPGameService(TwistedWeb):
    """
    Performs remote execution of entity methods over HTTP.
    """

    def __init__(self):
        TwistedWeb.__init__(self, netmask=Config.NETMASK)

    def createResources(self):
        """ Implements superclass method TwistedWeb.createResources """
        root = JSONResource()
        root.putChild('entities_by_name', EntitiesByNameResource())
        root.putChild('entities_by_id', EntitiesByIDResource())
        root.putChild('global_entities', GlobalEntitiesResource())
        root.putChild('db', DBResource())
        return root