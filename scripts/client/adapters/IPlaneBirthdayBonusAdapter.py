# Embedded file name: scripts/client/adapters/IPlaneBirthdayBonusAdapter.py
import _economics
from adapters.DefaultAdapter import DefaultAdapter
import db.DBLogic
from exchangeapi.CommonUtils import splitIDTypeList
from exchangeapi.ErrorCodes import OBJECT_NOT_FOUND, SUCCESS, WRONG_DATA_FORMAT

def getBirthdayBonus(account, index, planeID):
    """
    get bonuses for 'index' birthday for planeID
    @type planeID: int
    @type index: int
    @param index: number of birthday
    @param planeID: plane ID
    @return: bonus in format: {'battles': 7, 'xpFactor': 2.0}
    @rtype: dict
    """
    planeLevel = db.DBLogic.g_instance.getPlaneLevelByID(planeID)
    return _economics.PlaneBirthday.get(index, {}).get(planeLevel, {})


class IPlaneBirthdayBonusAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        idList, typeList = splitIDTypeList(kw['idTypeList'])
        if 'plane' in typeList and 'birthday' in typeList:
            try:
                planeID, index = idList
                if index >= 0 and db.DBLogic.g_instance.isAircraftInDB(planeID):
                    return {'bonus': getBirthdayBonus(account, index, planeID)}
            except:
                pass

        return None