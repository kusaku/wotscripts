# Embedded file name: scripts/client/adapters/IMeasurementSystemAdapter.py
from DefaultAdapter import DefaultAdapter
import Settings
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem

class IMeasurementSystemAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ob = {'measurementSystem': Settings.g_instance.gameUI['measurementSystem']}
        return super(IMeasurementSystemAdapter, self).__call__(account, ob, **kw)


class IMeasurementSystemInfoAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        ms = MeasurementSystem(kw['idTypeList'][0][0])
        adaptedOb = super(IMeasurementSystemInfoAdapter, self).__call__(account, {}, **kw)
        adaptedOb['distancePost'] = ms.localizeMarket('MARKET_AIRPLANE_TURN_RADIUS')
        adaptedOb['speedPost'] = ms.localizeMarket('MARKET_AIRPLANE_GROUND_MAX_SPEED')
        adaptedOb['massPost'] = ms.localizeMarket('MARKET_AIRPLANE_MASS')
        return adaptedOb


class IMeasurementSystemsListAdapter(DefaultAdapter):

    def __call__(self, account, ob, **kw):
        adaptedOb = super(IMeasurementSystemsListAdapter, self).__call__(account, {}, **kw)
        adaptedOb['measurementSystems'] = range(len(Settings.g_instance.gameUI['measurementSystems'].split(',')))
        return adaptedOb