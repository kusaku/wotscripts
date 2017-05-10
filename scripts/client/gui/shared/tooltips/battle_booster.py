# Embedded file name: scripts/client/gui/shared/tooltips/battle_booster.py
from gui.shared.utils.requesters import REQ_CRITERIA
from gui.Scaleform.genConsts.BLOCKS_TOOLTIP_TYPES import BLOCKS_TOOLTIP_TYPES
from gui.Scaleform.genConsts.SLOT_HIGHLIGHT_TYPES import SLOT_HIGHLIGHT_TYPES
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.Scaleform.locale.ITEM_TYPES import ITEM_TYPES
from gui.shared.formatters import text_styles
from gui.shared.tooltips import formatters, TOOLTIP_TYPE
from gui.shared.tooltips.common import BlocksTooltipData
from gui.shared.tooltips.module import PriceBlockConstructor
from helpers import dependency
from helpers.i18n import makeString as _ms
from skeletons.gui.shared import IItemsCache
_TOOLTIP_MIN_WIDTH = 420
_TOOLTIP_MAX_WIDTH = 480
_AUTOCANNON_SHOT_DISTANCE = 400
_MAX_INSTALLED_LIST_LEN = 10

class BattleBoosterBlockTooltipData(BlocksTooltipData):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self, context):
        super(BattleBoosterBlockTooltipData, self).__init__(context, TOOLTIP_TYPE.MODULE)
        self.item = None
        self._setContentMargin(top=0, left=0, bottom=20, right=20)
        self._setMargins(10, 15)
        self._setWidth(_TOOLTIP_MIN_WIDTH)
        return

    def _packBlocks(self, *args, **kwargs):
        self.item = self.context.buildItem(*args, **kwargs)
        items = super(BattleBoosterBlockTooltipData, self)._packBlocks()
        module = self.item
        statsConfig = self.context.getStatsConfiguration(module)
        statusConfig = self.context.getStatusConfiguration(module)
        leftPadding = 20
        rightPadding = 20
        topPadding = 20
        bottomPadding = -20
        blockTopPadding = -4
        blockPadding = formatters.packPadding(left=leftPadding, right=rightPadding, top=blockTopPadding)
        textGap = -2
        valueWidth = 110
        items.append(formatters.packBuildUpBlockData(HeaderBlockConstructor(module, statsConfig, leftPadding, rightPadding).construct(), padding=formatters.packPadding(left=leftPadding, right=rightPadding, top=topPadding, bottom=bottomPadding)))
        effectsBlock = EffectsBlockConstructor(module, statusConfig, leftPadding, rightPadding).construct()
        if effectsBlock:
            items.append(formatters.packBuildUpBlockData(effectsBlock, padding=blockPadding, linkage=BLOCKS_TOOLTIP_TYPES.TOOLTIP_BUILDUP_BLOCK_WHITE_BG_LINKAGE))
        priceBlock, invalidWidth = BattleBoosterPriceBlockConstructor(module, statsConfig, valueWidth, leftPadding, rightPadding).construct()
        if priceBlock:
            self._setWidth(_TOOLTIP_MAX_WIDTH if invalidWidth else _TOOLTIP_MIN_WIDTH)
            items.append(formatters.packBuildUpBlockData(priceBlock, padding=blockPadding, gap=textGap))
        statusBlock = StatusBlockConstructor(module, statusConfig, leftPadding, rightPadding).construct()
        if statusBlock:
            items.append(formatters.packBuildUpBlockData(statusBlock, padding=blockPadding))
        boosterIsUseless = BoosterHasNoEffectBlockConstructor(module, statusConfig, leftPadding, rightPadding).construct()
        if boosterIsUseless:
            items.append(formatters.packBuildUpBlockData(boosterIsUseless, gap=-4, padding=formatters.packPadding(left=leftPadding, right=rightPadding, top=blockTopPadding, bottom=2), stretchBg=False))
        return items


class BattleBoosterTooltipBlockConstructor(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self, module, configuration, leftPadding = 20, rightPadding = 20):
        self.module = module
        self.configuration = configuration
        self.leftPadding = leftPadding
        self.rightPadding = rightPadding

    def construct(self):
        return None


class HeaderBlockConstructor(BattleBoosterTooltipBlockConstructor):

    def construct(self):
        module = self.module
        block = []
        title = module.userName
        imgPaddingLeft = 7
        imgPaddingTop = 5
        desc = TOOLTIPS.BATTLEBOOSTER_CREW if module.isCrewBooster() else TOOLTIPS.BATTLEBOOSTER_OPTIONALDEVICE
        overlayPath, highlightPath = self.__getOverlayAndHighlight()
        padding = formatters.packPadding(top=SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER_PADDING_TOP, left=SLOT_HIGHLIGHT_TYPES.BATTLE_BOOSTER_PADDING_LEFT)
        block.append(formatters.packItemTitleDescBlockData(title=text_styles.highTitle(title), desc=text_styles.standard(_ms(desc)), img=module.icon, imgPadding=formatters.packPadding(left=imgPaddingLeft, top=imgPaddingTop), txtGap=-3, txtOffset=90 - self.leftPadding, padding=formatters.packPadding(top=-6), overlayPath=overlayPath, overlayPadding=padding, highlightPath=highlightPath, highlightPadding=padding))
        return block

    def __getOverlayAndHighlight(self):
        module = self.module
        if module.isCrewBooster():
            isLearnt = module.isAffectedSkillLearnt(self.configuration.vehicle)
            overlayPath = RES_ICONS.MAPS_ICONS_ARTEFACT_BATTLEBOOSTER_OVERLAY if isLearnt else RES_ICONS.MAPS_ICONS_ARTEFACT_BATTLEBOOSTER_REPLACE_OVERLAY
        else:
            overlayPath = RES_ICONS.MAPS_ICONS_ARTEFACT_BATTLEBOOSTER_OVERLAY
        highlightPath = RES_ICONS.MAPS_ICONS_ARTEFACT_BATTLEBOOSTER_HIGHLIGHT
        return (overlayPath, highlightPath)


class BattleBoosterPriceBlockConstructor(PriceBlockConstructor):

    def _getInventoryBlock(self, count):
        return formatters.packTextParameterBlockData(name=text_styles.main(TOOLTIPS.BATTLEBOOSTER_INVENTORYCOUNT), value=text_styles.stats(count), valueWidth=self._valueWidth, padding=formatters.packPadding(left=-5))


class EffectsBlockConstructor(BattleBoosterTooltipBlockConstructor):

    def construct(self):
        block = []
        module = self.module
        vehicle = self.configuration.vehicle
        if module.isCrewBooster():
            skillLearnt = module.isAffectedSkillLearnt(vehicle)
            skillName = _ms(ITEM_TYPES.tankman_skills(module.getAffectedSkillName()))
            replaceText = module.getCrewBoosterAction(True)
            boostText = module.getCrewBoosterAction(False)
            skillNotLearntText = text_styles.standard(TOOLTIPS.BATTLEBOOSTER_SKILL_NOT_LEARNT)
            skillLearntText = text_styles.standard(TOOLTIPS.BATTLEBOOSTER_SKILL_LEARNT)
            replaceText, boostText = self.__getSkillTexts(skillLearnt, replaceText, boostText)
            block.append(formatters.packImageTextBlockData(title=replaceText, img=RES_ICONS.MAPS_ICONS_BUTTONS_CHECKMARK if not skillLearnt else None, imgPadding=formatters.packPadding(left=2, top=3), txtOffset=20))
            block.append(formatters.packImageTextBlockData(title=skillNotLearntText % skillName, txtOffset=20))
            block.append(formatters.packImageTextBlockData(title=boostText, img=RES_ICONS.MAPS_ICONS_BUTTONS_CHECKMARK if skillLearnt else None, imgPadding=formatters.packPadding(left=2, top=3), txtOffset=20, padding=formatters.packPadding(top=15)))
            block.append(formatters.packImageTextBlockData(title=skillLearntText % skillName, txtOffset=20))
        else:
            desc = text_styles.bonusAppliedText(module.getOptDeviceBoosterDescription(vehicle))
            block.append(formatters.packTitleDescBlock(title='', desc=desc, padding=formatters.packPadding(top=-8)))
        return block

    @staticmethod
    def __getSkillTexts(skillLearnt, replaceText, boostText):
        if skillLearnt:
            return (text_styles.main(replaceText), text_styles.bonusAppliedText(boostText))
        else:
            return (text_styles.bonusAppliedText(replaceText), text_styles.main(boostText))


class StatusBlockConstructor(BattleBoosterTooltipBlockConstructor):

    def construct(self):
        block = list()
        module = self.module
        inventoryVehicles = self.itemsCache.items.getVehicles(REQ_CRITERIA.INVENTORY).itervalues()
        totalInstalledVehicles = map(lambda x: x.shortUserName, module.getInstalledVehicles(inventoryVehicles))
        installedVehicles = totalInstalledVehicles[:_MAX_INSTALLED_LIST_LEN]
        if installedVehicles:
            tooltipText = ', '.join(installedVehicles)
            if len(totalInstalledVehicles) > _MAX_INSTALLED_LIST_LEN:
                hiddenVehicleCount = len(totalInstalledVehicles) - _MAX_INSTALLED_LIST_LEN
                hiddenTxt = '%s %s' % (text_styles.main(TOOLTIPS.SUITABLEVEHICLE_HIDDENVEHICLECOUNT), text_styles.stats(hiddenVehicleCount))
                tooltipText = '%s\n%s' % (tooltipText, hiddenTxt)
            block.append(formatters.packTitleDescBlock(title=text_styles.middleTitle(TOOLTIPS.DEVICEFITS_ALREADY_INSTALLED_HEADER), desc=text_styles.standard(tooltipText)))
        return block


class BoosterHasNoEffectBlockConstructor(BattleBoosterTooltipBlockConstructor):
    """
    Notification if the booster has not effect
    """

    def construct(self):
        block = list()
        module = self.module
        vehicle = self.configuration.vehicle
        if vehicle is not None and not module.isAffectsOnVehicle(vehicle):
            block.append(formatters.packImageTextBlockData(title=text_styles.alert(TOOLTIPS.BATTLEBOOSTER_USELESS_HEADER), img=RES_ICONS.MAPS_ICONS_TOOLTIP_ALERTICON, imgPadding=formatters.packPadding(left=2, top=3), txtOffset=20))
            block.append(formatters.packTextBlockData(text=text_styles.main(TOOLTIPS.BATTLEBOOSTER_USELESS_BODY), padding=formatters.packPadding(top=8)))
        return block