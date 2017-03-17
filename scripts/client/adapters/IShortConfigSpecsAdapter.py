# Embedded file name: scripts/client/adapters/IShortConfigSpecsAdapter.py
from adapters.DefaultAdapter import DefaultAdapter
from Helpers.PerformanceSpecsHelper import getPerformanceSpecsTable, getAirplaneDescriptionPair, SpecsDescriptionList
from consts import SPECS_KEY_MAP
import db

class IShortConfigSpecsAdapter(DefaultAdapter):

    def __call__(self, account, obList, **kw):
        globalID = kw['idTypeList'][0][0]
        ob = obList
        retOb = {}
        if ob is not None:
            import BWPersonality
            lch = BWPersonality.g_lobbyCarouselHelper
            planeID = db.DBLogic.g_instance.getPlaneIDByGlobalID(globalID)
            carouselAirplane = lch.getCarouselAirplaneSelected()
            modify = False
            projectiles = None
            equipment = lch.inventory.getEquipment(planeID)
            crewList = lch.inventory.getCrewList(planeID)
            if carouselAirplane is not None:
                currentPlaneID = carouselAirplane.planeID
                installedGlobalID = lch.inventory.getInstalledUpgradesGlobalID(currentPlaneID) if lch.inventory.isAircraftBought(currentPlaneID) else 0
                if installedGlobalID == globalID:
                    projectiles = carouselAirplane.weapons.getInstalledProjectiles()
                    modify = True
            specs = getPerformanceSpecsTable(globalID, modify, projectiles, equipment, crewList)
            if specs is not None:
                for param in SpecsDescriptionList:
                    _, value, _, _, _, _ = getAirplaneDescriptionPair(specs, param)
                    retOb[SPECS_KEY_MAP[param['tag']]] = value

        return super(IShortConfigSpecsAdapter, self).__call__(account, retOb, **kw)

    def edit(self, account, requestID, idTypeList, data, ob = None, **kw):
        return super(IShortConfigSpecsAdapter, self).view(account, requestID, idTypeList, ob, **kw)