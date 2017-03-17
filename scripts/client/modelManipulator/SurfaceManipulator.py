# Embedded file name: scripts/client/modelManipulator/SurfaceManipulator.py
import consts
import BigWorld
import debug_utils
import Math
import clientConsts
import CompoundBuilder
if not consts.IS_EDITOR:
    from account_helpers import ClanEmblemsCache
if not consts.IS_EDITOR:
    import GameEnvironment

class SurfaceManipulator(object):
    """
    Control material parameters on compound objects
    """
    DELAYED_SURFACE_APPLY = 1.0

    def __init__(self, visualSettings, textureQuality, cidProxy, context):
        self.__visualSettings = visualSettings
        self.__textureQuality = textureQuality
        self.__surfaceTextures = None
        self.__surfaceParameters = (0.0, Math.Vector4(1, 1, 1, 1), Math.Vector4(1, 1, 1, 1))
        self.__compoundIDProxy = cidProxy
        self.__context = context
        self.__clanEmblemFileNameCached = None
        self.__posponedApplySurfacesCb = None
        self.__onCombinedCallback = None
        return

    def getDetailTexture(self):
        """return main detail texture"""
        surfaceSettings = self.__visualSettings.surfaceSettings
        if surfaceSettings:
            return surfaceSettings.detailTexture
        else:
            return None

    def applySurfaces(self, callback = None):
        self.__onCombinedCallback = self.__onCombinedCallback or callback
        if self.__surfaceTextures is not None and self.__compoundIDProxy.handle != CompoundBuilder.INVALID_ID:
            if self.__posponedApplySurfacesCb is not None:
                BigWorld.cancelCallback(self.__posponedApplySurfacesCb)
                self.__posponedApplySurfacesCb = None
            debug_utils.LOG_TRACE('::applySurfaces ', *self.__surfaceTextures)
            BigWorld.combineAndApplyDiffuse(self.__onCombinedAndApplyDiffuse, self.__compoundIDProxy.handle, self.__textureQuality, self.__surfaceParameters[0], self.__surfaceParameters[1], self.__surfaceParameters[2], *self.__surfaceTextures)
        else:
            debug_utils.LOG_TRACE('::applySurfaces - data not ready yet!', self.__surfaceTextures, self.__compoundIDProxy.handle)
            self.__posponedApplySurfacesCb = BigWorld.callback(self.__class__.DELAYED_SURFACE_APPLY, self.applySurfaces)
        return

    def setSurfaceParameters(self, glossinessOffset, bottomColor, reflectionColor):
        """set up material surface parameters. Direct use only in editors"""
        self.__surfaceParameters = (glossinessOffset, bottomColor, reflectionColor)

    def setSurfaceTextures(self, detail, camouflage, selfShadow, decals):
        """set up camouflage. Direct use only in editors"""
        self.__surfaceTextures = (detail,
         camouflage,
         selfShadow,
         decals)
        if consts.IS_EDITOR:
            self.applySurfaces()

    def refreshClanEmblem(self):
        if self.__surfaceTextures is not None:
            if not consts.IS_EDITOR and clientConsts.ENABLE_PLANE_CLAN_EMBLEM:
                import BWPersonality
                env = GameEnvironment.getClientArena()
                allowBGLoading = False if env and env.isLoaded() else True
                if env:
                    avatarInfo = env.getAvatarInfo(self.__context.entityId)
                    clanDBID = avatarInfo.get('clanDBID')
                    if clanDBID and int(clanDBID) > 0:
                        ClanEmblemsCache.g_clanEmblemsCache.get(clanDBID, self.__updateClanEmblemClbk, not allowBGLoading)
                elif int(BWPersonality.g_initPlayerInfo.clanDBID) > 0:
                    ClanEmblemsCache.g_clanEmblemsCache.get(BWPersonality.g_initPlayerInfo.clanDBID, self.__updateClanEmblemClbk, not allowBGLoading)
        return

    def setDecalsByIds(self, camouflageID, decalIDs):
        """init decals and camouflage"""
        surfaceSettings = self.__visualSettings.surfaceSettings
        if surfaceSettings:
            detail = surfaceSettings.detailTexture
            if detail != '':
                decalGroups = surfaceSettings.decalsSettings.decalGroups
                camouflage = decalGroups['camouflage'].getDecalTexNameByID(camouflageID)
                selfShadow = ''
                glossinessOffset = 0.0
                bottomColor = Math.Vector4(1, 1, 1, 1)
                reflectionColor = Math.Vector4(1, 1, 1, 1)
                camuflageSettings = decalGroups['camouflage'].getDecal(camouflageID)
                if camuflageSettings is not None:
                    if hasattr(camuflageSettings, 'glossinessOffset'):
                        glossinessOffset = camuflageSettings.glossinessOffset
                    if hasattr(camuflageSettings, 'bottomColor'):
                        bottomColor = camuflageSettings.bottomColor
                    if hasattr(camuflageSettings, 'reflectionColor'):
                        reflectionColor = camuflageSettings.reflectionColor
                debug_utils.LOG_TRACE('ModelManipulator: setDecalsByIds', decalIDs)
                decals = []
                if len(decalIDs) < clientConsts.DECAL_NUM_MIN:
                    debug_utils.LOG_ERROR("Can't set decals: wrong decal list size!")
                else:
                    if not consts.IS_EDITOR and clientConsts.ENABLE_PLANE_CLAN_EMBLEM:
                        import BWPersonality
                        env = GameEnvironment.getClientArena()
                        allowBGLoading = False if env and env.isLoaded() else True
                        if env:
                            avatarInfo = env.getAvatarInfo(self.__context.entityId)
                            clanDBID = avatarInfo.get('clanDBID')
                            if clanDBID and int(clanDBID) > 0:
                                ClanEmblemsCache.g_clanEmblemsCache.get(clanDBID, self.__updateClanEmblemClbk, not allowBGLoading)
                        elif int(BWPersonality.g_initPlayerInfo.clanDBID) > 0:
                            ClanEmblemsCache.g_clanEmblemsCache.get(BWPersonality.g_initPlayerInfo.clanDBID, self.__updateClanEmblemClbk, not allowBGLoading)
                    specialNationalityDecalId = decalIDs[10] if len(decalIDs) > 10 else -1
                    clanBigId = 0
                    clanSmallId = 0
                    if specialNationalityDecalId == 0:
                        clanBigId = clientConsts.DECAL_DEFAULT_VALUE[0]
                        clanSmallId = clientConsts.DECAL_DEFAULT_VALUE[1]
                    elif specialNationalityDecalId > 0:
                        clanBigId = specialNationalityDecalId
                        clanSmallId = specialNationalityDecalId
                    decals.append(decalGroups['clan_big'].getDecalTexNameByID(clanBigId) if clanBigId > 0 else '')
                    decals.append(decalGroups['clan_small'].getDecalTexNameByID(clanSmallId) if clanSmallId > 0 else '')
                    if self.__clanEmblemFileNameCached:
                        decals.append(self.__clanEmblemFileNameCached)
                    else:
                        decals.append('')
                    decals.append(decalGroups['platoon_number'].getDecalTexNameByID(decalIDs[3]) if decalIDs[3] != clientConsts.DECAL_ISNT_EXIST_VALUE[3] else '')
                    decals.append(decalGroups['member_number'].getDecalTexNameByID(decalIDs[4]) if decalIDs[4] != clientConsts.DECAL_ISNT_EXIST_VALUE[4] else '')
                    decals.append(decalGroups['air_frags'].getDecalTexNameByID(decalIDs[5][0]) if decalIDs[5][0] != clientConsts.DECAL_ISNT_EXIST_VALUE[5] else '')
                    decals.append(decalGroups['ground_frags'].getDecalTexNameByID(decalIDs[5][1]) if decalIDs[5][1] != clientConsts.DECAL_ISNT_EXIST_VALUE[5] else '')
                    decals.append('')
                    decals.append(decalGroups['nose'].getDecalTexNameByID(decalIDs[6]) if decalIDs[6] != clientConsts.DECAL_ISNT_EXIST_VALUE[6] else '')
                    decals.append(decalGroups['decor'].getDecalTexNameByID(decalIDs[7]) if decalIDs[7] != clientConsts.DECAL_ISNT_EXIST_VALUE[7] else '')
                self.setSurfaceParameters(glossinessOffset, bottomColor, reflectionColor)
                self.setSurfaceTextures(detail, camouflage, selfShadow, decals)
            else:
                debug_utils.LOG_WARNING('Wrong detail texture in surfaceSettings.detailTexture')
        else:
            debug_utils.LOG_WARNING('Wrong surfaceSettings')
        return

    def __onCombinedAndApplyDiffuse(self):
        if self.__onCombinedCallback:
            self.__onCombinedCallback()
            self.__onCombinedCallback = None
        return

    def __updateClanEmblem(self, texture):
        detail, camouflage, selfShadow, decals = self.__surfaceTextures
        decals[2] = texture
        self.__surfaceTextures = (detail,
         camouflage,
         selfShadow,
         decals)
        self.applySurfaces()
        self.__clanEmblemFileNameCached = texture

    def __updateClanEmblemClbk(self, emblemId, texture, size):
        if texture is not None:
            self.__updateClanEmblem(texture)
        else:
            debug_utils.LOG_WARNING('Failed to download embled id: %s!' % str(emblemId))
        return