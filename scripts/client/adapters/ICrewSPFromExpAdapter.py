# Embedded file name: scripts/client/adapters/ICrewSPFromExpAdapter.py
from DefaultAdapter import DefaultAdapter
import _economics

class ICrewSPFromExpAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        import SkillsHelper
        aob = super(ICrewSPFromExpAdapter, self).__call__(account, ob, **kw)
        aob['items'] = SkillsHelper.SP_COUNT_FROM_EXP
        aob['changeRate'] = _economics.Economics.freeXPToCrewXPRate
        return aob