# Embedded file name: scripts/client/adapters/IPlanePresetAdapter.py
from debug_utils import LOG_DEBUG
import db
from adapters.DefaultAdapter import DefaultAdapter
from consts import CUSTOM_PRESET_NAME
from Helpers.i18n import localizeComponents, localizePresets

class IPlanePresetAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(IPlanePresetAdapter, self).__call__(account, ob, **kw)
        if ob is not None:
            globalID = ob['globalID']
            dbInstance = db.DBLogic.g_instance
            name = dbInstance.getPresetNameByGlobalID(globalID)
            weapons = dbInstance.getUpgradesNamesByGlobalID(globalID)
            weapons = [ x for x in weapons if x not in ob['preset'].modules ]
            adaptedOb['name'] = localizeComponents('PRESET_NAME_%s' % name) if name == CUSTOM_PRESET_NAME else localizePresets('PRESET_NAME_%s' % name)
            adaptedOb['modulesList'] = [ dbInstance.getUpgradeByName(module).id for module in ob['preset'].modules ]
            adaptedOb['weaponSlotsList'] = ob['preset'].weaponSlots
            adaptedOb['weaponsList'] = [ dbInstance.getUpgradeByName(weapon).id for weapon in weapons ]
        return adaptedOb