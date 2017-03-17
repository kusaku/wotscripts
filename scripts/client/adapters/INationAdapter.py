# Embedded file name: scripts/client/adapters/INationAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from exchangeapi.Connectors import getObject
NATION_FLAG_TEMPLATE = 'icons/shop/flag{0}_.dds'

class INationPlaneAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOB = super(INationPlaneAdapter, self).__call__(account, ob, **kw)
        if ob is not None:
            from db.DBLogic import g_instance as db_instance
            adaptedOB['nationID'] = db_instance.getNationIDbyName(ob.country)
            adaptedOB['flagPath'] = NATION_FLAG_TEMPLATE.format(ob.country)
        else:
            adaptedOB['nationID'] = -1
            adaptedOB['flagPath'] = ''
        return adaptedOB


class INationAmmoBeltAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        from db.DBLogic import g_instance as db_instance
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(INationAmmoBeltAdapter, self).__call__(account, ob, **kw)
        adaptedOB['nationID'] = -1
        adaptedOB['flagPath'] = ''
        if ob is not None:
            guns = db_instance.getBeltSuitableGuns(ob.id)
            if guns:
                adaptedOB['nationID'] = db_instance.getNationIDbyName(guns[0].country)
                adaptedOB['flagPath'] = NATION_FLAG_TEMPLATE.format(guns[0].country)
        return adaptedOB


class INationShellAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        from db.DBLogic import g_instance as db_instance
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(INationShellAdapter, self).__call__(account, ob, **kw)
        if ob is not None:
            adaptedOB['nationID'] = db_instance.getNationIDbyName(ob.country)
            adaptedOB['flagPath'] = NATION_FLAG_TEMPLATE.format(ob.country)
        else:
            adaptedOB['nationID'] = -1
            adaptedOB['flagPath'] = ''
        return adaptedOB


class INationUpgradeAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        from db.DBLogic import g_instance as db_instance
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(INationUpgradeAdapter, self).__call__(account, ob, **kw)
        if hasattr(ob, 'variant'):
            planeID = db_instance.getAircraftIDbyName(ob.variant[0].aircraftName)
            data = db_instance.getAircraftData(planeID)
            adaptedOB['nationID'] = db_instance.getNationIDbyName(data.airplane.country)
            adaptedOB['flagPath'] = NATION_FLAG_TEMPLATE.format(data.airplane.country)
        return adaptedOB


class INationListAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        from db.DBLogic import g_instance as db_instance
        ob = ob or getObject(kw['idTypeList'])
        adaptedOB = super(INationListAdapter, self).__call__(account, ob, **kw)
        adaptedOB['nationIDList'] = []
        adaptedOB['flagPathList'] = []
        if ob is not None:
            for x in ob.nations:
                adaptedOB['nationIDList'].append(db_instance.getNationIDbyName(x))
                adaptedOB['flagPathList'].append(NATION_FLAG_TEMPLATE.format(x))

        return adaptedOB