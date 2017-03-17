# Embedded file name: scripts/common/_warAction.py
import Math
import math
import consts
true = True
false = False

class Dummy:
    pass


isServerDatabase = False

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


class CASE_COMPENSATION:
    CREDITS = 0
    GOLD = 1
    TICKETS = 2
    VIRTUAL_CASH = 3
    ALL_TYPES = (CREDITS,
     GOLD,
     TICKETS,
     VIRTUAL_CASH)


WarAction = Dummy()
WarAction.actionID = 1
WarAction.uiConfig = Dummy()
WarAction.uiConfig.achievements = Dummy()
WarAction.uiConfig.achievements.endID = 219
WarAction.uiConfig.achievements.startID = 206
WarAction.uiConfig.actionPlaneID = []
WarAction.uiConfig.actionPlaneID.insert(0, None)
WarAction.uiConfig.actionPlaneID[0] = 4802
WarAction.uiConfig.actionPlaneID.insert(1, None)
WarAction.uiConfig.actionPlaneID[1] = 4202
WarAction.uiConfig.actionPlaneID.insert(2, None)
WarAction.uiConfig.actionPlaneID[2] = 4304
WarAction.uiConfig.actionPlaneID.insert(3, None)
WarAction.uiConfig.actionPlaneID[3] = 4402
WarAction.uiConfig.actionPlaneID.insert(4, None)
WarAction.uiConfig.actionPlaneID[4] = 4503
WarAction.uiConfig.actionPlaneID.insert(5, None)
WarAction.uiConfig.actionPlaneID[5] = 4602
WarAction.uiConfig.actionPlaneID.insert(6, None)
WarAction.uiConfig.actionPlaneID[6] = 4701
WarAction.uiConfig.actionPlaneID.insert(7, None)
WarAction.uiConfig.actionPlaneID[7] = 4902
WarAction.uiConfig.actionPlaneID.insert(8, None)
WarAction.uiConfig.actionPlaneID[8] = 4002
WarAction.uiConfig.hangarPeace = '00_14_Tropical_Island_peace_2016'
WarAction.uiConfig.hangarWar = '00_13_Tropical_Island_war_2016'
WarAction.uiConfig.pathArt = 'gui\\flash\\imageJapaneseThreat'
WarAction.uiConfig.slidePrizes = Dummy()
WarAction.uiConfig.slidePrizes.prizes = '1,2,3'
if isServerDatabase:
    __planeIDsGlobal = set()
    __planeIDsAllyCommand = set()
    __planeIDsAxisCommand = set()
    changeFractionStates = dict(((price.state, price) for price in WarAction.economics.fractionSelect.priceChange))

    def init():
        global __planeIDsAllyCommand
        global __planeIDsAxisCommand
        global __planeIDsGlobal
        import _aircrafts_db

        def getSetPlaneIDs--- This code section failed: ---

0	SETUP_LOOP        '327'
3	LOAD_DEREF        '_aircrafts_db'
6	LOAD_ATTR         'DB'
9	LOAD_ATTR         'aircraft'
12	GET_ITER          None
13	FOR_ITER          '326'
16	STORE_FAST        'plane'

19	LOAD_FAST         'plane'
22	LOAD_ATTR         'options'
25	LOAD_ATTR         'isDev'
28	JUMP_IF_FALSE_OR_POP '40'
31	LOAD_FAST         'plane'
34	LOAD_ATTR         'options'
37	LOAD_ATTR         'isTest'
40_0	COME_FROM         '28'
40	POP_JUMP_IF_TRUE  '13'

43	LOAD_FAST         'plane'
46	LOAD_ATTR         'id'
49	LOAD_FAST         'filters'
52	LOAD_ATTR         'exclude'
55	LOAD_ATTR         'planeID'
58	COMPARE_OP        'in'
61_0	COME_FROM         '40'
61	POP_JUMP_IF_FALSE '70'

64	CONTINUE          '13'
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	LOAD_FAST         'plane'
73	LOAD_ATTR         'country'
76	LOAD_FAST         'filters'
79	LOAD_ATTR         'exclude'
82	LOAD_ATTR         'nation'
85	COMPARE_OP        'in'
88	POP_JUMP_IF_FALSE '97'

91	CONTINUE          '13'
94	JUMP_FORWARD      '97'
97_0	COME_FROM         '94'

97	LOAD_FAST         'plane'
100	LOAD_ATTR         'planeType'
103	LOAD_FAST         'filters'
106	LOAD_ATTR         'exclude'
109	LOAD_ATTR         'class_'
112	COMPARE_OP        'in'
115	POP_JUMP_IF_FALSE '124'

118	CONTINUE          '13'
121	JUMP_FORWARD      '124'
124_0	COME_FROM         '121'

124	LOAD_FAST         'plane'
127	LOAD_ATTR         'level'
130	LOAD_FAST         'filters'
133	LOAD_ATTR         'exclude'
136	LOAD_ATTR         'level'
139	COMPARE_OP        'in'
142	POP_JUMP_IF_FALSE '151'

145	CONTINUE          '13'
148	JUMP_FORWARD      '151'
151_0	COME_FROM         '148'

151	LOAD_FAST         'filters'
154	LOAD_ATTR         'include'
157	LOAD_ATTR         'planeID'
160	POP_JUMP_IF_FALSE '195'
163	LOAD_FAST         'plane'
166	LOAD_ATTR         'id'
169	LOAD_FAST         'filters'
172	LOAD_ATTR         'include'
175	LOAD_ATTR         'planeID'
178	COMPARE_OP        'in'
181_0	COME_FROM         '160'
181	POP_JUMP_IF_FALSE '195'

184	LOAD_FAST         'plane'
187	LOAD_ATTR         'id'
190	YIELD_VALUE       None
191	POP_TOP           None
192	JUMP_ABSOLUTE     '323'

195	LOAD_FAST         'filters'
198	LOAD_ATTR         'include'
201	LOAD_ATTR         'nation'
204	POP_JUMP_IF_FALSE '234'
207	LOAD_FAST         'plane'
210	LOAD_ATTR         'country'
213	LOAD_FAST         'filters'
216	LOAD_ATTR         'include'
219	LOAD_ATTR         'nation'
222	COMPARE_OP        'not in'
225_0	COME_FROM         '204'
225	POP_JUMP_IF_FALSE '234'

228	CONTINUE          '13'
231	JUMP_FORWARD      '234'
234_0	COME_FROM         '231'

234	LOAD_FAST         'filters'
237	LOAD_ATTR         'include'
240	LOAD_ATTR         'class_'
243	POP_JUMP_IF_FALSE '273'
246	LOAD_FAST         'plane'
249	LOAD_ATTR         'planeType'
252	LOAD_FAST         'filters'
255	LOAD_ATTR         'include'
258	LOAD_ATTR         'class_'
261	COMPARE_OP        'not in'
264_0	COME_FROM         '243'
264	POP_JUMP_IF_FALSE '273'

267	CONTINUE          '13'
270	JUMP_FORWARD      '273'
273_0	COME_FROM         '270'

273	LOAD_FAST         'filters'
276	LOAD_ATTR         'include'
279	LOAD_ATTR         'level'
282	POP_JUMP_IF_FALSE '312'
285	LOAD_FAST         'plane'
288	LOAD_ATTR         'level'
291	LOAD_FAST         'filters'
294	LOAD_ATTR         'include'
297	LOAD_ATTR         'level'
300	COMPARE_OP        'not in'
303_0	COME_FROM         '282'
303	POP_JUMP_IF_FALSE '312'

306	CONTINUE          '13'
309	JUMP_FORWARD      '312'
312_0	COME_FROM         '309'

312	LOAD_FAST         'plane'
315	LOAD_ATTR         'id'
318	YIELD_VALUE       None
319	POP_TOP           None
320	JUMP_BACK         '13'
323	JUMP_BACK         '13'
326	POP_BLOCK         None
327_0	COME_FROM         '0'

Syntax error at or near `LOAD_FAST' token at offset 195

        __planeIDsGlobal = set(getSetPlaneIDs(WarAction.filters.global_))
        __planeIDsAllyCommand = set(getSetPlaneIDs(WarAction.filters.allyCommand))
        __planeIDsAxisCommand = set(getSetPlaneIDs(WarAction.filters.axisCommand))
        WarAction.uiConfig.slidePrizes.prizeID = [ int(pr.strip()) for pr in WarAction.uiConfig.slidePrizes.prizes.split(',') ]


    init()

    def checkPlaneInGlobalFilter(planeID):
        return planeID in __planeIDsGlobal


    def checkPlaneInAllyCommandFilter(planeID):
        return planeID in __planeIDsAllyCommand


    def checkPlaneInAxisCommandFilter(planeID):
        return planeID in __planeIDsAxisCommand