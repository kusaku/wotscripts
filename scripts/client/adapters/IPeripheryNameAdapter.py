# Embedded file name: scripts/client/adapters/IPeripheryNameAdapter.py
import Settings
from adapters.DefaultAdapter import DefaultAdapter
from debug_utils import LOG_ERROR, LOG_DEBUG

class IPeripheryNameAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(IPeripheryNameAdapter, self).__call__(account, ob, **kw)
        currPeripheryID = kw['idTypeList'][0][0]
        adaptedOB['name'] = 'periphery_%d' % currPeripheryID
        dataSection = Settings.g_instance.scriptConfig.scriptData['login']
        if dataSection:
            for name, host in dataSection.items():
                if host.has_key('periphery_id'):
                    peripheryID = host.readString('periphery_id')
                    if not peripheryID.isdigit():
                        LOG_ERROR('Wrong periphery_id format in scripts_config.xml')
                        continue
                    if currPeripheryID == int(peripheryID):
                        adaptedOB['name'] = host.readString('name')
                        break

        return adaptedOB