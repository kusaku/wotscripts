# Embedded file name: scripts/client/gui/customization_2_0/bonus_panel.py
from Event import Event
from gui.Scaleform.genConsts.CUSTOMIZATION_BONUS_ANIMATION_TYPES import CUSTOMIZATION_BONUS_ANIMATION_TYPES
from gui.shared.formatters import text_styles
from elements.qualifier import getNameByType as _getBonusNameByType
from elements.qualifier import getIcon42x42ByType as _getBonusIcon42x42ByType
from elements.qualifier import QUALIFIER_TYPE_NAMES
from shared import forEachSlotIn
from data_aggregator import CUSTOMIZATION_TYPE

class BonusPanel(object):

    def __init__(self, aggregatedData):
        self.__initAnimation = False
        self.__aData = aggregatedData
        self.__bonusData = {}
        for qTypeName in QUALIFIER_TYPE_NAMES.iterkeys():
            self.__bonusData[qTypeName] = {'bonusName': text_styles.main(_getBonusNameByType(qTypeName)),
             'bonusIcon': _getBonusIcon42x42ByType(qTypeName),
             'bonusTotalCount': 0,
             'oldBonusTotalCount': 0,
             'bonusAppliedCount': 0,
             'oldBonusAppliedCount': 0}

        self.__initialSlotsData = None
        self.bonusesUpdated = Event()
        return

    def fini(self):
        self.__aData = None
        self.__bonusData = None
        self.__initialSlotsData = None
        return

    @property
    def bonusData(self):
        return self.__bonusData

    def setInitialSlotsData(self, iSlotsData):
        self.__initialSlotsData = iSlotsData
        for qTypeName in QUALIFIER_TYPE_NAMES.iterkeys():
            self.__bonusData[qTypeName]['bonusTotalCount'] = 0
            self.__bonusData[qTypeName]['bonusAppliedCount'] = 0

        def getInitialBonusData(newSlotItem, oldSlotItem, cType, slotIdx):
            if newSlotItem['itemID'] > 0:
                availableItem = self.__aData.available[cType][newSlotItem['itemID']]
                renderingDataObject = self.__bonusData[availableItem.qualifier.getType()]
                if cType == CUSTOMIZATION_TYPE.CAMOUFLAGE and not renderingDataObject['bonusTotalCount'] or cType != CUSTOMIZATION_TYPE.CAMOUFLAGE:
                    renderingDataObject['bonusTotalCount'] += availableItem.qualifier.getValue()

        forEachSlotIn(iSlotsData, iSlotsData, getInitialBonusData)

    def update(self, updatedSlotsData):
        for qTypeName in QUALIFIER_TYPE_NAMES.iterkeys():
            self.__bonusData[qTypeName]['bonusAppliedCount'] = 0

        forEachSlotIn(updatedSlotsData, self.__initialSlotsData, self.__recalculateBonusData)
        self.__setAnimations()
        self.bonusesUpdated(self.__bonusData)

    def __recalculateBonusData(self, newSlotItem, oldSlotItem, cType, slotIdx):
        if newSlotItem['itemID'] != oldSlotItem['itemID']:
            if newSlotItem['itemID'] > 0 and oldSlotItem['itemID'] > 0:
                cNewItem = self.__aData.available[cType][newSlotItem['itemID']]
                cOldItem = self.__aData.available[cType][oldSlotItem['itemID']]
                self.__bonusData[cNewItem.qualifier.getType()]['bonusAppliedCount'] += cNewItem.qualifier.getValue()
                self.__bonusData[cOldItem.qualifier.getType()]['bonusAppliedCount'] -= cOldItem.qualifier.getValue()
            elif newSlotItem['itemID'] > 0 > oldSlotItem['itemID']:
                cNewItem = self.__aData.available[cType][newSlotItem['itemID']]
                self.__bonusData[cNewItem.qualifier.getType()]['bonusAppliedCount'] += cNewItem.qualifier.getValue()

    def __setAnimations(self):
        for qTypeName in QUALIFIER_TYPE_NAMES.iterkeys():
            oldBonusAppliedCount = self.__bonusData[qTypeName]['oldBonusAppliedCount']
            appliedBonusValue = self.__bonusData[qTypeName]['bonusAppliedCount']
            oldBonusTotalCount = self.__bonusData[qTypeName]['oldBonusTotalCount']
            bonusTotalCount = self.__bonusData[qTypeName]['bonusTotalCount']
            formattedString = '+{0}%'
            bonusFormatter = text_styles.bonusAppliedText
            color = CUSTOMIZATION_BONUS_ANIMATION_TYPES.COLOR_GREEN
            additionalValue = ''
            if oldBonusTotalCount != bonusTotalCount and self.__initAnimation:
                animationType = CUSTOMIZATION_BONUS_ANIMATION_TYPES.BUY
                bonusFormatter = text_styles.bonusLocalText
                animationValue = bonusTotalCount
            elif appliedBonusValue == oldBonusAppliedCount:
                animationType = CUSTOMIZATION_BONUS_ANIMATION_TYPES.NONE
                bonusFormatter = text_styles.bonusLocalText
                animationValue = bonusTotalCount
                if appliedBonusValue > 0:
                    additionalValue = text_styles.bonusAppliedText('+{0}%'.format(appliedBonusValue))
                elif appliedBonusValue < 0:
                    additionalValue = text_styles.error('{0}%'.format(appliedBonusValue))
            elif appliedBonusValue == 0:
                if oldBonusAppliedCount < 0:
                    formattedString = '{0}%'
                    bonusFormatter = text_styles.error
                    color = CUSTOMIZATION_BONUS_ANIMATION_TYPES.COLOR_RED
                animationType = CUSTOMIZATION_BONUS_ANIMATION_TYPES.RESET
                animationValue = oldBonusAppliedCount
            else:
                if appliedBonusValue < 0:
                    formattedString = '{0}%'
                    bonusFormatter = text_styles.error
                    color = CUSTOMIZATION_BONUS_ANIMATION_TYPES.COLOR_RED
                animationType = CUSTOMIZATION_BONUS_ANIMATION_TYPES.SET
                animationValue = appliedBonusValue
            self.__bonusData[qTypeName]['oldBonusAppliedCount'] = appliedBonusValue
            self.__bonusData[qTypeName]['oldBonusTotalCount'] = bonusTotalCount
            self.__bonusData[qTypeName]['animationPanel'] = {'animationType': animationType,
             'install': False,
             'color': color,
             'value1': bonusFormatter(formattedString.format(animationValue)),
             'value2': additionalValue}

        self.__initAnimation = True