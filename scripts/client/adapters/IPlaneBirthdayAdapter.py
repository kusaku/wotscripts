# Embedded file name: scripts/client/adapters/IPlaneBirthdayAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from Helpers.i18n import getFormattedTime
import Settings

class IPlaneBirthdayAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob['birthdayTimeStr'] = getFormattedTime(ob['birthdayTime'], Settings.g_instance.scriptConfig.timeFormated['dmY'])
        return ob