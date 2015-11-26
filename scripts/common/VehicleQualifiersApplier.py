# Embedded file name: scripts/common/VehicleQualifiersApplier.py
from items import vehicles
from items import qualifiers as Qualifiers
from items.qualifiers import QUALIFIER_TYPE, QUALIFIER_TYPE_NAMES

def makeQualifiersChainApplier(conditions, qualifiers):

    def makeApplier(v):
        for qualifier in qualifiers:
            if qualifier.conditionParams <= set(conditions.keys()):
                v = qualifier(v, **conditions)

        return v

    return makeApplier


class _SubApplier(object):

    def __init__(self, conditions, qualifierType, qualifiersByType):
        qualifiersBySubType = {}
        for qualifier in qualifiersByType:
            if qualifierType == QUALIFIER_TYPE.MAIN_SKILL:
                subType = qualifier.crewRole
            else:
                raise 'SubApplier %s not implemented' % QUALIFIER_TYPE_NAMES[qualifierType]
            qualifiersBySubType.setdefault(subType, []).append(qualifier)

        self.__qualifiersSubApplier = qualifiersSubApplier = {}
        for qualifierSubType, qualifiers in qualifiersBySubType.iteritems():
            qualifiersSubApplier[qualifierSubType] = makeQualifiersChainApplier(conditions, qualifiers)

    def __getitem__(self, subType):
        return self.__qualifiersSubApplier.setdefault(subType, lambda v: v)


class VehicleQualifiersApplier(object):

    def __init__(self, conditions, vehDescr, arenaCamouflageKind = None):
        self.__requiredParams = requiredParams = set()
        self.__qualifiersApplier = qualifiersApplier = {}
        qualifiersByType = {}
        activatedQualifierIDs = self.__activatedQualifierIDs(vehDescr, arenaCamouflageKind)
        for qualifierID in activatedQualifierIDs:
            qualifier = Qualifiers.g_cache[qualifierID]
            if qualifier:
                qualifiersByType.setdefault(qualifier.qualifierType, []).append(qualifier)
                cndParams = qualifier.conditionParams
                if cndParams:
                    requiredParams.update(cndParams)

        for qualifierType, qualifiers in qualifiersByType.iteritems():
            qualifiersApplier[qualifierType] = self.__createApplier(qualifierType, qualifiers, conditions)

    requiredParams = property(lambda self: self.__requiredParams)

    def __activatedQualifierIDs(self, vehDescr, arenaCamouflageKind):
        v_cache = vehicles.g_cache
        g_customization = v_cache.customization
        activatedQualifierIDs = []
        selectors = (('playerInscriptions', range(0, 4)), ('playerEmblems', range(0, 4)))
        for propName, positions in selectors:
            propValue = getattr(vehDescr, propName, None)
            if not propValue:
                continue
            for pos in positions:
                if pos is None:
                    continue
                itemID = propValue[pos][0]
                if itemID is None:
                    continue
                nationID = vehDescr.type.customizationNationID
                customization = None
                if propName == 'playerInscriptions':
                    customization = g_customization(nationID)['inscriptions']
                elif propName == 'playerEmblems':
                    customization = v_cache.playerEmblems()[1]
                qualifierID = customization[itemID][-1]
                if qualifierID is not None:
                    activatedQualifierIDs.append(qualifierID)

        return activatedQualifierIDs

    def __createApplier(self, qualifierType, qualifiers = [], conditions = {}):
        if qualifierType == QUALIFIER_TYPE.MAIN_SKILL:
            return _SubApplier(conditions, qualifierType, qualifiers)
        else:
            return makeQualifiersChainApplier(conditions, qualifiers)

    def __getitem__(self, qualifierType):
        return self.__qualifiersApplier.setdefault(qualifierType, self.__createApplier(qualifierType))