# Embedded file name: scripts/client/vehicle_systems/camouflages.py
import BigWorld
import Math
from vehicle_systems.tankStructure import VehiclePartsTuple
from debug_utils import LOG_ERROR
import items
from vehicle_systems.tankStructure import TankPartNames

def prepareFashions(vDesc, isCurrentModelDamaged, camouflageId = None, newPhysic = True):
    if isCurrentModelDamaged:
        fashions = [None,
         None,
         None,
         None]
    else:
        drivenJoints = vDesc.gun.get('drivenJoints', None)
        fashions = [BigWorld.WGVehicleFashion(False, 1.0, newPhysic),
         None,
         None,
         BigWorld.WGGunRecoil('G', drivenJoints)]
    camouflagePresent = False
    texture = ''
    customization = items.vehicles.g_cache.customization(vDesc.type.customizationNationID)
    if camouflageId is not None and customization is not None:
        camouflage = customization['camouflages'].get(camouflageId)
        if camouflage is not None:
            camouflagePresent = True
            texture = camouflage['texture']
    useCamouflage = camouflagePresent and texture
    for fashionIdx, descId in enumerate(TankPartNames.ALL):
        fashion = fashions[fashionIdx]
        forceFashion = fashion is None and (useCamouflage or hasattr(vDesc.type, 'repaintParameters'))
        if forceFashion:
            fashions[fashionIdx] = BigWorld.WGBaseFashion()

    return fashions


def applyCamouflage(vDesc, fashions, isCurrentModelDamaged, camouflageId = None):
    fashions = list(fashions)
    texture = ''
    colors = [0,
     0,
     0,
     0]
    weights = Math.Vector4(1, 0, 0, 0)
    camouflagePresent = False
    customization = items.vehicles.g_cache.customization(vDesc.type.customizationNationID)
    defaultTiling = None
    if camouflageId is not None and customization is not None:
        camouflage = customization['camouflages'].get(camouflageId)
        if camouflage is not None:
            camouflagePresent = True
            texture = camouflage['texture']
            colors = camouflage['colors']
            weights = Math.Vector4(*[ (c >> 24) / 255.0 for c in colors ])
            defaultTiling = camouflage['tiling'].get(vDesc.type.compactDescr)
    if isCurrentModelDamaged:
        weights *= 0.1
    for fashionIdx, descId in enumerate(TankPartNames.ALL):
        exclusionMap = vDesc.type.camouflageExclusionMask
        tiling = defaultTiling
        if tiling is None:
            tiling = vDesc.type.camouflageTiling
        if descId == 'chassis':
            compDesc = vDesc.chassis
        elif descId == 'hull':
            compDesc = vDesc.hull
        elif descId == 'turret':
            compDesc = vDesc.turret
        elif descId == 'gun':
            compDesc = vDesc.gun
        else:
            compDesc = None
        if compDesc is not None:
            coeff = compDesc.get('camouflageTiling')
            if coeff is not None:
                if tiling is not None:
                    tiling = (tiling[0] * coeff[0],
                     tiling[1] * coeff[1],
                     tiling[2] + coeff[2],
                     tiling[3] + coeff[3])
                else:
                    tiling = coeff
            if compDesc.get('camouflageExclusionMask'):
                exclusionMap = compDesc['camouflageExclusionMask']
        useCamouflage = camouflagePresent and texture
        fashion = fashions[fashionIdx]
        if fashion is not None:
            if useCamouflage:
                fashion.setCamouflage(texture, exclusionMap, tiling, colors[0], colors[1], colors[2], colors[3], weights)
            else:
                fashion.removeCamouflage()
        elif useCamouflage:
            LOG_ERROR('Unexpected lack of fashion, but camouflage is being applied. Use prepareFashions function!')

    return VehiclePartsTuple(*fashions)


def _getRepaintParams(vDesc):
    tintGroups = items.vehicles.g_cache.customization(vDesc.type.customizationNationID)['tintGroups']
    for i in tintGroups.keys():
        grp = tintGroups[i]
        repaintReplaceColor = Math.Vector4(grp.x, grp.y, grp.z, 0.0) / 255.0

    refColor = vDesc.type.repaintParameters['refColor'] / 255.0
    repaintReferenceGloss = vDesc.type.repaintParameters['refGloss'] / 255.0
    repaintColorRangeScale = vDesc.type.repaintParameters['refColorMult']
    repaintGlossRangeScale = vDesc.type.repaintParameters['refGlossMult']
    repaintReferenceColor = Math.Vector4(refColor.x, refColor.y, refColor.z, repaintReferenceGloss)
    repaintReplaceColor.w = repaintColorRangeScale
    return (repaintReferenceColor, repaintReplaceColor, repaintGlossRangeScale)


def applyRepaint(vDesc, fashions):
    if not hasattr(vDesc.type, 'repaintParameters'):
        return fashions
    else:
        repaintReferenceColor, repaintReplaceColor, repaintGlossRangeScale = _getRepaintParams(vDesc)
        fashions = list(fashions)
        for fashionIdx, fashion in enumerate(fashions):
            if fashion is not None:
                fashion.setRepaint(repaintReferenceColor, repaintReplaceColor, repaintGlossRangeScale)
            else:
                LOG_ERROR('Unexpected lack of fashion, but repaint is being applied. Use prepareFashions function!')

        return VehiclePartsTuple(*fashions)


def getFootballEventCamouflageKind(team):
    """
    blue team - winter camouflage type, tuple position '0'
    red team - desert camo type, tuple position '2'
    unused - summer camo type, tuple position '1'
    :param team:
    :return:
    """
    if team == 2:
        return 0
    return 2