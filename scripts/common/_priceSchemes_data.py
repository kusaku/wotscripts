# Embedded file name: scripts/common/_priceSchemes_data.py
import Math
import math
import consts
true = True
false = False

class Dummy:
    pass


isServerDatabase = True

class AMMO_TYPE:
    BALL = 0
    AP = 1
    APC = 2
    I = 3
    APHC = 4
    API = 5
    HEI = 6
    APHE = 7
    ALL_TYPES = (BALL,
     AP,
     APC,
     I,
     APHC,
     API,
     HEI,
     APHE)


PriceShemes = Dummy()
PriceShemes.priceScheme = []
PriceShemes.priceScheme.insert(0, None)
PriceShemes.priceScheme[0] = Dummy()
PriceShemes.priceScheme[0].name = 'BASE'
PriceShemes.priceScheme[0].price = []
PriceShemes.priceScheme[0].price.insert(0, None)
PriceShemes.priceScheme[0].price[0] = Dummy()
PriceShemes.priceScheme[0].price[0].credits = 700
PriceShemes.priceScheme[0].price[0].daycount = 7
PriceShemes.priceScheme[0].price[0].gold = 0
PriceShemes.priceScheme[0].price.insert(1, None)
PriceShemes.priceScheme[0].price[1] = Dummy()
PriceShemes.priceScheme[0].price[1].credits = 3000
PriceShemes.priceScheme[0].price[1].daycount = 30
PriceShemes.priceScheme[0].price[1].gold = 0
PriceShemes.priceScheme[0].price.insert(2, None)
PriceShemes.priceScheme[0].price[2] = Dummy()
PriceShemes.priceScheme[0].price[2].credits = 0
PriceShemes.priceScheme[0].price[2].daycount = -1
PriceShemes.priceScheme[0].price[2].gold = 850
PriceShemes.priceScheme.insert(1, None)
PriceShemes.priceScheme[1] = Dummy()
PriceShemes.priceScheme[1].name = 'FULL_PRICE'
PriceShemes.priceScheme[1].price = []
PriceShemes.priceScheme[1].price.insert(0, None)
PriceShemes.priceScheme[1].price[0] = Dummy()
PriceShemes.priceScheme[1].price[0].credits = 1000
PriceShemes.priceScheme[1].price[0].daycount = 7
PriceShemes.priceScheme[1].price[0].gold = 0
PriceShemes.priceScheme[1].price.insert(1, None)
PriceShemes.priceScheme[1].price[1] = Dummy()
PriceShemes.priceScheme[1].price[1].credits = 4000
PriceShemes.priceScheme[1].price[1].daycount = 30
PriceShemes.priceScheme[1].price[1].gold = 0
PriceShemes.priceScheme[1].price.insert(2, None)
PriceShemes.priceScheme[1].price[2] = Dummy()
PriceShemes.priceScheme[1].price[2].credits = 0
PriceShemes.priceScheme[1].price[2].daycount = -1
PriceShemes.priceScheme[1].price[2].gold = 1000
PriceShemes.priceScheme.insert(2, None)
PriceShemes.priceScheme[2] = Dummy()
PriceShemes.priceScheme[2].name = '1'
PriceShemes.priceScheme[2].price = []
PriceShemes.priceScheme[2].price.insert(0, None)
PriceShemes.priceScheme[2].price[0] = Dummy()
PriceShemes.priceScheme[2].price[0].credits = 2000
PriceShemes.priceScheme[2].price[0].daycount = 7
PriceShemes.priceScheme[2].price[0].gold = 0
PriceShemes.priceScheme[2].price.insert(1, None)
PriceShemes.priceScheme[2].price[1] = Dummy()
PriceShemes.priceScheme[2].price[1].credits = 8000
PriceShemes.priceScheme[2].price[1].daycount = 30
PriceShemes.priceScheme[2].price[1].gold = 0
PriceShemes.priceScheme[2].price.insert(2, None)
PriceShemes.priceScheme[2].price[2] = Dummy()
PriceShemes.priceScheme[2].price[2].credits = 0
PriceShemes.priceScheme[2].price[2].daycount = -1
PriceShemes.priceScheme[2].price[2].gold = 20
PriceShemes.priceScheme.insert(3, None)
PriceShemes.priceScheme[3] = Dummy()
PriceShemes.priceScheme[3].name = '2'
PriceShemes.priceScheme[3].price = []
PriceShemes.priceScheme[3].price.insert(0, None)
PriceShemes.priceScheme[3].price[0] = Dummy()
PriceShemes.priceScheme[3].price[0].credits = 3500
PriceShemes.priceScheme[3].price[0].daycount = 7
PriceShemes.priceScheme[3].price[0].gold = 0
PriceShemes.priceScheme[3].price.insert(1, None)
PriceShemes.priceScheme[3].price[1] = Dummy()
PriceShemes.priceScheme[3].price[1].credits = 14000
PriceShemes.priceScheme[3].price[1].daycount = 30
PriceShemes.priceScheme[3].price[1].gold = 0
PriceShemes.priceScheme[3].price.insert(2, None)
PriceShemes.priceScheme[3].price[2] = Dummy()
PriceShemes.priceScheme[3].price[2].credits = 0
PriceShemes.priceScheme[3].price[2].daycount = -1
PriceShemes.priceScheme[3].price[2].gold = 35
PriceShemes.priceScheme.insert(4, None)
PriceShemes.priceScheme[4] = Dummy()
PriceShemes.priceScheme[4].name = '3'
PriceShemes.priceScheme[4].price = []
PriceShemes.priceScheme[4].price.insert(0, None)
PriceShemes.priceScheme[4].price[0] = Dummy()
PriceShemes.priceScheme[4].price[0].credits = 5500
PriceShemes.priceScheme[4].price[0].daycount = 7
PriceShemes.priceScheme[4].price[0].gold = 0
PriceShemes.priceScheme[4].price.insert(1, None)
PriceShemes.priceScheme[4].price[1] = Dummy()
PriceShemes.priceScheme[4].price[1].credits = 22000
PriceShemes.priceScheme[4].price[1].daycount = 30
PriceShemes.priceScheme[4].price[1].gold = 0
PriceShemes.priceScheme[4].price.insert(2, None)
PriceShemes.priceScheme[4].price[2] = Dummy()
PriceShemes.priceScheme[4].price[2].credits = 0
PriceShemes.priceScheme[4].price[2].daycount = -1
PriceShemes.priceScheme[4].price[2].gold = 55
PriceShemes.priceScheme.insert(5, None)
PriceShemes.priceScheme[5] = Dummy()
PriceShemes.priceScheme[5].name = '4'
PriceShemes.priceScheme[5].price = []
PriceShemes.priceScheme[5].price.insert(0, None)
PriceShemes.priceScheme[5].price[0] = Dummy()
PriceShemes.priceScheme[5].price[0].credits = 7500
PriceShemes.priceScheme[5].price[0].daycount = 7
PriceShemes.priceScheme[5].price[0].gold = 0
PriceShemes.priceScheme[5].price.insert(1, None)
PriceShemes.priceScheme[5].price[1] = Dummy()
PriceShemes.priceScheme[5].price[1].credits = 30000
PriceShemes.priceScheme[5].price[1].daycount = 30
PriceShemes.priceScheme[5].price[1].gold = 0
PriceShemes.priceScheme[5].price.insert(2, None)
PriceShemes.priceScheme[5].price[2] = Dummy()
PriceShemes.priceScheme[5].price[2].credits = 0
PriceShemes.priceScheme[5].price[2].daycount = -1
PriceShemes.priceScheme[5].price[2].gold = 75
PriceShemes.priceScheme.insert(6, None)
PriceShemes.priceScheme[6] = Dummy()
PriceShemes.priceScheme[6].name = '5'
PriceShemes.priceScheme[6].price = []
PriceShemes.priceScheme[6].price.insert(0, None)
PriceShemes.priceScheme[6].price[0] = Dummy()
PriceShemes.priceScheme[6].price[0].credits = 9000
PriceShemes.priceScheme[6].price[0].daycount = 7
PriceShemes.priceScheme[6].price[0].gold = 0
PriceShemes.priceScheme[6].price.insert(1, None)
PriceShemes.priceScheme[6].price[1] = Dummy()
PriceShemes.priceScheme[6].price[1].credits = 36000
PriceShemes.priceScheme[6].price[1].daycount = 30
PriceShemes.priceScheme[6].price[1].gold = 0
PriceShemes.priceScheme[6].price.insert(2, None)
PriceShemes.priceScheme[6].price[2] = Dummy()
PriceShemes.priceScheme[6].price[2].credits = 0
PriceShemes.priceScheme[6].price[2].daycount = -1
PriceShemes.priceScheme[6].price[2].gold = 90
PriceShemes.priceScheme.insert(7, None)
PriceShemes.priceScheme[7] = Dummy()
PriceShemes.priceScheme[7].name = '6'
PriceShemes.priceScheme[7].price = []
PriceShemes.priceScheme[7].price.insert(0, None)
PriceShemes.priceScheme[7].price[0] = Dummy()
PriceShemes.priceScheme[7].price[0].credits = 11000
PriceShemes.priceScheme[7].price[0].daycount = 7
PriceShemes.priceScheme[7].price[0].gold = 0
PriceShemes.priceScheme[7].price.insert(1, None)
PriceShemes.priceScheme[7].price[1] = Dummy()
PriceShemes.priceScheme[7].price[1].credits = 44000
PriceShemes.priceScheme[7].price[1].daycount = 30
PriceShemes.priceScheme[7].price[1].gold = 0
PriceShemes.priceScheme[7].price.insert(2, None)
PriceShemes.priceScheme[7].price[2] = Dummy()
PriceShemes.priceScheme[7].price[2].credits = 0
PriceShemes.priceScheme[7].price[2].daycount = -1
PriceShemes.priceScheme[7].price[2].gold = 110
PriceShemes.priceScheme.insert(8, None)
PriceShemes.priceScheme[8] = Dummy()
PriceShemes.priceScheme[8].name = '7'
PriceShemes.priceScheme[8].price = []
PriceShemes.priceScheme[8].price.insert(0, None)
PriceShemes.priceScheme[8].price[0] = Dummy()
PriceShemes.priceScheme[8].price[0].credits = 13000
PriceShemes.priceScheme[8].price[0].daycount = 7
PriceShemes.priceScheme[8].price[0].gold = 0
PriceShemes.priceScheme[8].price.insert(1, None)
PriceShemes.priceScheme[8].price[1] = Dummy()
PriceShemes.priceScheme[8].price[1].credits = 52000
PriceShemes.priceScheme[8].price[1].daycount = 30
PriceShemes.priceScheme[8].price[1].gold = 0
PriceShemes.priceScheme[8].price.insert(2, None)
PriceShemes.priceScheme[8].price[2] = Dummy()
PriceShemes.priceScheme[8].price[2].credits = 0
PriceShemes.priceScheme[8].price[2].daycount = -1
PriceShemes.priceScheme[8].price[2].gold = 130
PriceShemes.priceScheme.insert(9, None)
PriceShemes.priceScheme[9] = Dummy()
PriceShemes.priceScheme[9].name = '8'
PriceShemes.priceScheme[9].price = []
PriceShemes.priceScheme[9].price.insert(0, None)
PriceShemes.priceScheme[9].price[0] = Dummy()
PriceShemes.priceScheme[9].price[0].credits = 15000
PriceShemes.priceScheme[9].price[0].daycount = 7
PriceShemes.priceScheme[9].price[0].gold = 0
PriceShemes.priceScheme[9].price.insert(1, None)
PriceShemes.priceScheme[9].price[1] = Dummy()
PriceShemes.priceScheme[9].price[1].credits = 60000
PriceShemes.priceScheme[9].price[1].daycount = 30
PriceShemes.priceScheme[9].price[1].gold = 0
PriceShemes.priceScheme[9].price.insert(2, None)
PriceShemes.priceScheme[9].price[2] = Dummy()
PriceShemes.priceScheme[9].price[2].credits = 0
PriceShemes.priceScheme[9].price[2].daycount = -1
PriceShemes.priceScheme[9].price[2].gold = 150
PriceShemes.priceScheme.insert(10, None)
PriceShemes.priceScheme[10] = Dummy()
PriceShemes.priceScheme[10].name = '9'
PriceShemes.priceScheme[10].price = []
PriceShemes.priceScheme[10].price.insert(0, None)
PriceShemes.priceScheme[10].price[0] = Dummy()
PriceShemes.priceScheme[10].price[0].credits = 16500
PriceShemes.priceScheme[10].price[0].daycount = 7
PriceShemes.priceScheme[10].price[0].gold = 0
PriceShemes.priceScheme[10].price.insert(1, None)
PriceShemes.priceScheme[10].price[1] = Dummy()
PriceShemes.priceScheme[10].price[1].credits = 66000
PriceShemes.priceScheme[10].price[1].daycount = 30
PriceShemes.priceScheme[10].price[1].gold = 0
PriceShemes.priceScheme[10].price.insert(2, None)
PriceShemes.priceScheme[10].price[2] = Dummy()
PriceShemes.priceScheme[10].price[2].credits = 0
PriceShemes.priceScheme[10].price[2].daycount = -1
PriceShemes.priceScheme[10].price[2].gold = 165
PriceShemes.priceScheme.insert(11, None)
PriceShemes.priceScheme[11] = Dummy()
PriceShemes.priceScheme[11].name = '10'
PriceShemes.priceScheme[11].price = []
PriceShemes.priceScheme[11].price.insert(0, None)
PriceShemes.priceScheme[11].price[0] = Dummy()
PriceShemes.priceScheme[11].price[0].credits = 18000
PriceShemes.priceScheme[11].price[0].daycount = 7
PriceShemes.priceScheme[11].price[0].gold = 0
PriceShemes.priceScheme[11].price.insert(1, None)
PriceShemes.priceScheme[11].price[1] = Dummy()
PriceShemes.priceScheme[11].price[1].credits = 72000
PriceShemes.priceScheme[11].price[1].daycount = 30
PriceShemes.priceScheme[11].price[1].gold = 0
PriceShemes.priceScheme[11].price.insert(2, None)
PriceShemes.priceScheme[11].price[2] = Dummy()
PriceShemes.priceScheme[11].price[2].credits = 0
PriceShemes.priceScheme[11].price[2].daycount = -1
PriceShemes.priceScheme[11].price[2].gold = 180
PriceShemes.priceScheme.insert(12, None)
PriceShemes.priceScheme[12] = Dummy()
PriceShemes.priceScheme[12].name = '1_decor'
PriceShemes.priceScheme[12].price = []
PriceShemes.priceScheme[12].price.insert(0, None)
PriceShemes.priceScheme[12].price[0] = Dummy()
PriceShemes.priceScheme[12].price[0].credits = 1500
PriceShemes.priceScheme[12].price[0].daycount = 7
PriceShemes.priceScheme[12].price[0].gold = 0
PriceShemes.priceScheme[12].price.insert(1, None)
PriceShemes.priceScheme[12].price[1] = Dummy()
PriceShemes.priceScheme[12].price[1].credits = 6000
PriceShemes.priceScheme[12].price[1].daycount = 30
PriceShemes.priceScheme[12].price[1].gold = 0
PriceShemes.priceScheme[12].price.insert(2, None)
PriceShemes.priceScheme[12].price[2] = Dummy()
PriceShemes.priceScheme[12].price[2].credits = 0
PriceShemes.priceScheme[12].price[2].daycount = -1
PriceShemes.priceScheme[12].price[2].gold = 15
PriceShemes.priceScheme.insert(13, None)
PriceShemes.priceScheme[13] = Dummy()
PriceShemes.priceScheme[13].name = '2_decor'
PriceShemes.priceScheme[13].price = []
PriceShemes.priceScheme[13].price.insert(0, None)
PriceShemes.priceScheme[13].price[0] = Dummy()
PriceShemes.priceScheme[13].price[0].credits = 3000
PriceShemes.priceScheme[13].price[0].daycount = 7
PriceShemes.priceScheme[13].price[0].gold = 0
PriceShemes.priceScheme[13].price.insert(1, None)
PriceShemes.priceScheme[13].price[1] = Dummy()
PriceShemes.priceScheme[13].price[1].credits = 12000
PriceShemes.priceScheme[13].price[1].daycount = 30
PriceShemes.priceScheme[13].price[1].gold = 0
PriceShemes.priceScheme[13].price.insert(2, None)
PriceShemes.priceScheme[13].price[2] = Dummy()
PriceShemes.priceScheme[13].price[2].credits = 0
PriceShemes.priceScheme[13].price[2].daycount = -1
PriceShemes.priceScheme[13].price[2].gold = 30
PriceShemes.priceScheme.insert(14, None)
PriceShemes.priceScheme[14] = Dummy()
PriceShemes.priceScheme[14].name = '3_decor'
PriceShemes.priceScheme[14].price = []
PriceShemes.priceScheme[14].price.insert(0, None)
PriceShemes.priceScheme[14].price[0] = Dummy()
PriceShemes.priceScheme[14].price[0].credits = 4500
PriceShemes.priceScheme[14].price[0].daycount = 7
PriceShemes.priceScheme[14].price[0].gold = 0
PriceShemes.priceScheme[14].price.insert(1, None)
PriceShemes.priceScheme[14].price[1] = Dummy()
PriceShemes.priceScheme[14].price[1].credits = 18000
PriceShemes.priceScheme[14].price[1].daycount = 30
PriceShemes.priceScheme[14].price[1].gold = 0
PriceShemes.priceScheme[14].price.insert(2, None)
PriceShemes.priceScheme[14].price[2] = Dummy()
PriceShemes.priceScheme[14].price[2].credits = 0
PriceShemes.priceScheme[14].price[2].daycount = -1
PriceShemes.priceScheme[14].price[2].gold = 45
PriceShemes.priceScheme.insert(15, None)
PriceShemes.priceScheme[15] = Dummy()
PriceShemes.priceScheme[15].name = '4_decor'
PriceShemes.priceScheme[15].price = []
PriceShemes.priceScheme[15].price.insert(0, None)
PriceShemes.priceScheme[15].price[0] = Dummy()
PriceShemes.priceScheme[15].price[0].credits = 6000
PriceShemes.priceScheme[15].price[0].daycount = 7
PriceShemes.priceScheme[15].price[0].gold = 0
PriceShemes.priceScheme[15].price.insert(1, None)
PriceShemes.priceScheme[15].price[1] = Dummy()
PriceShemes.priceScheme[15].price[1].credits = 24000
PriceShemes.priceScheme[15].price[1].daycount = 30
PriceShemes.priceScheme[15].price[1].gold = 0
PriceShemes.priceScheme[15].price.insert(2, None)
PriceShemes.priceScheme[15].price[2] = Dummy()
PriceShemes.priceScheme[15].price[2].credits = 0
PriceShemes.priceScheme[15].price[2].daycount = -1
PriceShemes.priceScheme[15].price[2].gold = 60
PriceShemes.priceScheme.insert(16, None)
PriceShemes.priceScheme[16] = Dummy()
PriceShemes.priceScheme[16].name = '5_decor'
PriceShemes.priceScheme[16].price = []
PriceShemes.priceScheme[16].price.insert(0, None)
PriceShemes.priceScheme[16].price[0] = Dummy()
PriceShemes.priceScheme[16].price[0].credits = 7500
PriceShemes.priceScheme[16].price[0].daycount = 7
PriceShemes.priceScheme[16].price[0].gold = 0
PriceShemes.priceScheme[16].price.insert(1, None)
PriceShemes.priceScheme[16].price[1] = Dummy()
PriceShemes.priceScheme[16].price[1].credits = 30000
PriceShemes.priceScheme[16].price[1].daycount = 30
PriceShemes.priceScheme[16].price[1].gold = 0
PriceShemes.priceScheme[16].price.insert(2, None)
PriceShemes.priceScheme[16].price[2] = Dummy()
PriceShemes.priceScheme[16].price[2].credits = 0
PriceShemes.priceScheme[16].price[2].daycount = -1
PriceShemes.priceScheme[16].price[2].gold = 75
PriceShemes.priceScheme.insert(17, None)
PriceShemes.priceScheme[17] = Dummy()
PriceShemes.priceScheme[17].name = '6_decor'
PriceShemes.priceScheme[17].price = []
PriceShemes.priceScheme[17].price.insert(0, None)
PriceShemes.priceScheme[17].price[0] = Dummy()
PriceShemes.priceScheme[17].price[0].credits = 9000
PriceShemes.priceScheme[17].price[0].daycount = 7
PriceShemes.priceScheme[17].price[0].gold = 0
PriceShemes.priceScheme[17].price.insert(1, None)
PriceShemes.priceScheme[17].price[1] = Dummy()
PriceShemes.priceScheme[17].price[1].credits = 36000
PriceShemes.priceScheme[17].price[1].daycount = 30
PriceShemes.priceScheme[17].price[1].gold = 0
PriceShemes.priceScheme[17].price.insert(2, None)
PriceShemes.priceScheme[17].price[2] = Dummy()
PriceShemes.priceScheme[17].price[2].credits = 0
PriceShemes.priceScheme[17].price[2].daycount = -1
PriceShemes.priceScheme[17].price[2].gold = 90
PriceShemes.priceScheme.insert(18, None)
PriceShemes.priceScheme[18] = Dummy()
PriceShemes.priceScheme[18].name = '7_decor'
PriceShemes.priceScheme[18].price = []
PriceShemes.priceScheme[18].price.insert(0, None)
PriceShemes.priceScheme[18].price[0] = Dummy()
PriceShemes.priceScheme[18].price[0].credits = 10500
PriceShemes.priceScheme[18].price[0].daycount = 7
PriceShemes.priceScheme[18].price[0].gold = 0
PriceShemes.priceScheme[18].price.insert(1, None)
PriceShemes.priceScheme[18].price[1] = Dummy()
PriceShemes.priceScheme[18].price[1].credits = 42000
PriceShemes.priceScheme[18].price[1].daycount = 30
PriceShemes.priceScheme[18].price[1].gold = 0
PriceShemes.priceScheme[18].price.insert(2, None)
PriceShemes.priceScheme[18].price[2] = Dummy()
PriceShemes.priceScheme[18].price[2].credits = 0
PriceShemes.priceScheme[18].price[2].daycount = -1
PriceShemes.priceScheme[18].price[2].gold = 105
PriceShemes.priceScheme.insert(19, None)
PriceShemes.priceScheme[19] = Dummy()
PriceShemes.priceScheme[19].name = '8_decor'
PriceShemes.priceScheme[19].price = []
PriceShemes.priceScheme[19].price.insert(0, None)
PriceShemes.priceScheme[19].price[0] = Dummy()
PriceShemes.priceScheme[19].price[0].credits = 12000
PriceShemes.priceScheme[19].price[0].daycount = 7
PriceShemes.priceScheme[19].price[0].gold = 0
PriceShemes.priceScheme[19].price.insert(1, None)
PriceShemes.priceScheme[19].price[1] = Dummy()
PriceShemes.priceScheme[19].price[1].credits = 48000
PriceShemes.priceScheme[19].price[1].daycount = 30
PriceShemes.priceScheme[19].price[1].gold = 0
PriceShemes.priceScheme[19].price.insert(2, None)
PriceShemes.priceScheme[19].price[2] = Dummy()
PriceShemes.priceScheme[19].price[2].credits = 0
PriceShemes.priceScheme[19].price[2].daycount = -1
PriceShemes.priceScheme[19].price[2].gold = 120
PriceShemes.priceScheme.insert(20, None)
PriceShemes.priceScheme[20] = Dummy()
PriceShemes.priceScheme[20].name = '9_decor'
PriceShemes.priceScheme[20].price = []
PriceShemes.priceScheme[20].price.insert(0, None)
PriceShemes.priceScheme[20].price[0] = Dummy()
PriceShemes.priceScheme[20].price[0].credits = 13500
PriceShemes.priceScheme[20].price[0].daycount = 7
PriceShemes.priceScheme[20].price[0].gold = 0
PriceShemes.priceScheme[20].price.insert(1, None)
PriceShemes.priceScheme[20].price[1] = Dummy()
PriceShemes.priceScheme[20].price[1].credits = 54000
PriceShemes.priceScheme[20].price[1].daycount = 30
PriceShemes.priceScheme[20].price[1].gold = 0
PriceShemes.priceScheme[20].price.insert(2, None)
PriceShemes.priceScheme[20].price[2] = Dummy()
PriceShemes.priceScheme[20].price[2].credits = 0
PriceShemes.priceScheme[20].price[2].daycount = -1
PriceShemes.priceScheme[20].price[2].gold = 135
PriceShemes.priceScheme.insert(21, None)
PriceShemes.priceScheme[21] = Dummy()
PriceShemes.priceScheme[21].name = '10_decor'
PriceShemes.priceScheme[21].price = []
PriceShemes.priceScheme[21].price.insert(0, None)
PriceShemes.priceScheme[21].price[0] = Dummy()
PriceShemes.priceScheme[21].price[0].credits = 15000
PriceShemes.priceScheme[21].price[0].daycount = 7
PriceShemes.priceScheme[21].price[0].gold = 0
PriceShemes.priceScheme[21].price.insert(1, None)
PriceShemes.priceScheme[21].price[1] = Dummy()
PriceShemes.priceScheme[21].price[1].credits = 60000
PriceShemes.priceScheme[21].price[1].daycount = 30
PriceShemes.priceScheme[21].price[1].gold = 0
PriceShemes.priceScheme[21].price.insert(2, None)
PriceShemes.priceScheme[21].price[2] = Dummy()
PriceShemes.priceScheme[21].price[2].credits = 0
PriceShemes.priceScheme[21].price[2].daycount = -1
PriceShemes.priceScheme[21].price[2].gold = 150
PriceShemes.priceScheme.insert(22, None)
PriceShemes.priceScheme[22] = Dummy()
PriceShemes.priceScheme[22].name = 'newyear_ufo_1'
PriceShemes.priceScheme[22].price = []
PriceShemes.priceScheme[22].price.insert(0, None)
PriceShemes.priceScheme[22].price[0] = Dummy()
PriceShemes.priceScheme[22].price[0].credits = -1
PriceShemes.priceScheme[22].price[0].daycount = -1
PriceShemes.priceScheme[22].price[0].gold = -1
PriceShemes.priceScheme.insert(23, None)
PriceShemes.priceScheme[23] = Dummy()
PriceShemes.priceScheme[23].name = 'newyear_ufo_2'
PriceShemes.priceScheme[23].price = []
PriceShemes.priceScheme[23].price.insert(0, None)
PriceShemes.priceScheme[23].price[0] = Dummy()
PriceShemes.priceScheme[23].price[0].credits = -1
PriceShemes.priceScheme[23].price[0].daycount = -1
PriceShemes.priceScheme[23].price[0].gold = -1
PriceShemes.priceScheme.insert(24, None)
PriceShemes.priceScheme[24] = Dummy()
PriceShemes.priceScheme[24].name = 'newyear_ufo_3'
PriceShemes.priceScheme[24].price = []
PriceShemes.priceScheme[24].price.insert(0, None)
PriceShemes.priceScheme[24].price[0] = Dummy()
PriceShemes.priceScheme[24].price[0].credits = -1
PriceShemes.priceScheme[24].price[0].daycount = -1
PriceShemes.priceScheme[24].price[0].gold = -1
PriceShemes.priceScheme.insert(25, None)
PriceShemes.priceScheme[25] = Dummy()
PriceShemes.priceScheme[25].name = 'newyear_ufo_4'
PriceShemes.priceScheme[25].price = []
PriceShemes.priceScheme[25].price.insert(0, None)
PriceShemes.priceScheme[25].price[0] = Dummy()
PriceShemes.priceScheme[25].price[0].credits = -1
PriceShemes.priceScheme[25].price[0].daycount = -1
PriceShemes.priceScheme[25].price[0].gold = -1
PriceShemes.priceScheme.insert(26, None)
PriceShemes.priceScheme[26] = Dummy()
PriceShemes.priceScheme[26].name = 'newyear_ufo_5'
PriceShemes.priceScheme[26].price = []
PriceShemes.priceScheme[26].price.insert(0, None)
PriceShemes.priceScheme[26].price[0] = Dummy()
PriceShemes.priceScheme[26].price[0].credits = -1
PriceShemes.priceScheme[26].price[0].daycount = -1
PriceShemes.priceScheme[26].price[0].gold = -1
PriceShemes.priceScheme.insert(27, None)
PriceShemes.priceScheme[27] = Dummy()
PriceShemes.priceScheme[27].name = 'newyear_ufo_6'
PriceShemes.priceScheme[27].price = []
PriceShemes.priceScheme[27].price.insert(0, None)
PriceShemes.priceScheme[27].price[0] = Dummy()
PriceShemes.priceScheme[27].price[0].credits = -1
PriceShemes.priceScheme[27].price[0].daycount = -1
PriceShemes.priceScheme[27].price[0].gold = -1
PriceShemes.priceScheme.insert(28, None)
PriceShemes.priceScheme[28] = Dummy()
PriceShemes.priceScheme[28].name = 'newyear_ufo_7'
PriceShemes.priceScheme[28].price = []
PriceShemes.priceScheme[28].price.insert(0, None)
PriceShemes.priceScheme[28].price[0] = Dummy()
PriceShemes.priceScheme[28].price[0].credits = -1
PriceShemes.priceScheme[28].price[0].daycount = -1
PriceShemes.priceScheme[28].price[0].gold = -1
PriceShemes.priceScheme.insert(29, None)
PriceShemes.priceScheme[29] = Dummy()
PriceShemes.priceScheme[29].name = 'newyear_ufo_8'
PriceShemes.priceScheme[29].price = []
PriceShemes.priceScheme[29].price.insert(0, None)
PriceShemes.priceScheme[29].price[0] = Dummy()
PriceShemes.priceScheme[29].price[0].credits = -1
PriceShemes.priceScheme[29].price[0].daycount = -1
PriceShemes.priceScheme[29].price[0].gold = -1
PriceShemes.priceScheme.insert(30, None)
PriceShemes.priceScheme[30] = Dummy()
PriceShemes.priceScheme[30].name = 'newyear_ufo_9'
PriceShemes.priceScheme[30].price = []
PriceShemes.priceScheme[30].price.insert(0, None)
PriceShemes.priceScheme[30].price[0] = Dummy()
PriceShemes.priceScheme[30].price[0].credits = -1
PriceShemes.priceScheme[30].price[0].daycount = -1
PriceShemes.priceScheme[30].price[0].gold = -1
PriceShemes.priceScheme.insert(31, None)
PriceShemes.priceScheme[31] = Dummy()
PriceShemes.priceScheme[31].name = 'newyear_ufo_10'
PriceShemes.priceScheme[31].price = []
PriceShemes.priceScheme[31].price.insert(0, None)
PriceShemes.priceScheme[31].price[0] = Dummy()
PriceShemes.priceScheme[31].price[0].credits = -1
PriceShemes.priceScheme[31].price[0].daycount = -1
PriceShemes.priceScheme[31].price[0].gold = -1
PriceShemes.priceScheme.insert(32, None)
PriceShemes.priceScheme[32] = Dummy()
PriceShemes.priceScheme[32].name = '1_april_price_1'
PriceShemes.priceScheme[32].price = []
PriceShemes.priceScheme[32].price.insert(0, None)
PriceShemes.priceScheme[32].price[0] = Dummy()
PriceShemes.priceScheme[32].price[0].credits = -1
PriceShemes.priceScheme[32].price[0].daycount = -1
PriceShemes.priceScheme[32].price[0].gold = -1
PriceShemes.priceScheme.insert(33, None)
PriceShemes.priceScheme[33] = Dummy()
PriceShemes.priceScheme[33].name = '1_april_price_2'
PriceShemes.priceScheme[33].price = []
PriceShemes.priceScheme[33].price.insert(0, None)
PriceShemes.priceScheme[33].price[0] = Dummy()
PriceShemes.priceScheme[33].price[0].credits = -1
PriceShemes.priceScheme[33].price[0].daycount = -1
PriceShemes.priceScheme[33].price[0].gold = -1
PriceShemes.priceScheme.insert(34, None)
PriceShemes.priceScheme[34] = Dummy()
PriceShemes.priceScheme[34].name = '1_april_price_3'
PriceShemes.priceScheme[34].price = []
PriceShemes.priceScheme[34].price.insert(0, None)
PriceShemes.priceScheme[34].price[0] = Dummy()
PriceShemes.priceScheme[34].price[0].credits = -1
PriceShemes.priceScheme[34].price[0].daycount = -1
PriceShemes.priceScheme[34].price[0].gold = -1
PriceShemes.priceScheme.insert(35, None)
PriceShemes.priceScheme[35] = Dummy()
PriceShemes.priceScheme[35].name = '1_april_price_4'
PriceShemes.priceScheme[35].price = []
PriceShemes.priceScheme[35].price.insert(0, None)
PriceShemes.priceScheme[35].price[0] = Dummy()
PriceShemes.priceScheme[35].price[0].credits = -1
PriceShemes.priceScheme[35].price[0].daycount = -1
PriceShemes.priceScheme[35].price[0].gold = -1
PriceShemes.priceScheme.insert(36, None)
PriceShemes.priceScheme[36] = Dummy()
PriceShemes.priceScheme[36].name = '1_april_price_5'
PriceShemes.priceScheme[36].price = []
PriceShemes.priceScheme[36].price.insert(0, None)
PriceShemes.priceScheme[36].price[0] = Dummy()
PriceShemes.priceScheme[36].price[0].credits = -1
PriceShemes.priceScheme[36].price[0].daycount = -1
PriceShemes.priceScheme[36].price[0].gold = -1
PriceShemes.priceScheme.insert(37, None)
PriceShemes.priceScheme[37] = Dummy()
PriceShemes.priceScheme[37].name = '1_april_price_6'
PriceShemes.priceScheme[37].price = []
PriceShemes.priceScheme[37].price.insert(0, None)
PriceShemes.priceScheme[37].price[0] = Dummy()
PriceShemes.priceScheme[37].price[0].credits = -1
PriceShemes.priceScheme[37].price[0].daycount = -1
PriceShemes.priceScheme[37].price[0].gold = -1
PriceShemes.priceScheme.insert(38, None)
PriceShemes.priceScheme[38] = Dummy()
PriceShemes.priceScheme[38].name = '1_april_price_7'
PriceShemes.priceScheme[38].price = []
PriceShemes.priceScheme[38].price.insert(0, None)
PriceShemes.priceScheme[38].price[0] = Dummy()
PriceShemes.priceScheme[38].price[0].credits = -1
PriceShemes.priceScheme[38].price[0].daycount = -1
PriceShemes.priceScheme[38].price[0].gold = -1
PriceShemes.priceScheme.insert(39, None)
PriceShemes.priceScheme[39] = Dummy()
PriceShemes.priceScheme[39].name = '1_april_price_8'
PriceShemes.priceScheme[39].price = []
PriceShemes.priceScheme[39].price.insert(0, None)
PriceShemes.priceScheme[39].price[0] = Dummy()
PriceShemes.priceScheme[39].price[0].credits = -1
PriceShemes.priceScheme[39].price[0].daycount = -1
PriceShemes.priceScheme[39].price[0].gold = -1
PriceShemes.priceScheme.insert(40, None)
PriceShemes.priceScheme[40] = Dummy()
PriceShemes.priceScheme[40].name = '1_april_price_9'
PriceShemes.priceScheme[40].price = []
PriceShemes.priceScheme[40].price.insert(0, None)
PriceShemes.priceScheme[40].price[0] = Dummy()
PriceShemes.priceScheme[40].price[0].credits = -1
PriceShemes.priceScheme[40].price[0].daycount = -1
PriceShemes.priceScheme[40].price[0].gold = -1
PriceShemes.priceScheme.insert(41, None)
PriceShemes.priceScheme[41] = Dummy()
PriceShemes.priceScheme[41].name = '1_april_price_10'
PriceShemes.priceScheme[41].price = []
PriceShemes.priceScheme[41].price.insert(0, None)
PriceShemes.priceScheme[41].price[0] = Dummy()
PriceShemes.priceScheme[41].price[0].credits = -1
PriceShemes.priceScheme[41].price[0].daycount = -1
PriceShemes.priceScheme[41].price[0].gold = -1
PriceSchemesDB = None

def initDB():
    global PriceSchemesDB
    if PriceSchemesDB is None:
        PriceSchemesDB = dict()
        for priceScheme in PriceShemes.priceScheme:
            PriceSchemesDB[priceScheme.name] = priceScheme

    return


initDB()