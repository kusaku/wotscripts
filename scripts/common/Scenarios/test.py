# Embedded file name: scripts/common/Scenarios/test.py
import os, sys
import ComponentModel.TypeSystem
import ComponentModel.ComponentCore
import ComponentModel.ClientComponents
import Math
import ComponentModel.Component
import ComponentModel.SysComponent
import ComponentModel.ScriptUtil
import VisualScript

def getParentModule():
    return ''


def createControllers(aspect, entity):
    controllers = []
    return controllers


def requiredControllers():
    return []


def getControllerCount():
    return 0


def fillPlan1(plan, aspect):
    pass


def fillPlan2(plan, aspect):
    Group22 = ComponentModel.ComponentCore.ComponentGroup()
    plan.groups.append(Group22)
    Group22.meta_ID = 'Group22'
    Group22.meta_posX = 17
    Group22.meta_posY = 248
    Group22.meta_width = 650
    Group22.meta_height = 899
    Group22.meta_title = 'Ships'
    StartEvent1 = VisualScript.StartClientScript()
    plan.append(StartEvent1)
    StartEvent1.meta_ID = 'StartEvent1'
    StartEvent1.meta_posY = int(-142)
    StartEvent1.meta_posX = int(-1095)
    Macro2 = ComponentModel.SysComponent.Macro('BismarkComplete', plan)
    plan.append(Macro2)
    Macro2.meta_ID = 'Macro2'
    Macro2.offset.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((20, 0, 0))))
    Macro2.meta_posX = int(131)
    Macro2.meta_posY = int(-89)
    ConstComponent3 = ComponentModel.Component.ConstComponent(ComponentModel.TypeSystem.SplineIDT)
    plan.append(ConstComponent3)
    ConstComponent3.meta_ID = 'ConstComponent3'
    ConstComponent3.const.setAccessor(ComponentModel.ComponentCore.ConstValue('pacific_scen_0_3'))
    ConstComponent3.meta_posX = int(-932)
    ConstComponent3.meta_posY = int(269)
    Macro4 = ComponentModel.SysComponent.Macro('BismarkComplete', plan)
    plan.append(Macro4)
    Macro4.meta_ID = 'Macro4'
    Macro4.offset.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((60, 0, 0))))
    Macro4.meta_posX = int(122)
    Macro4.meta_posY = int(69)
    Macro5 = ComponentModel.SysComponent.Macro('BismarkComplete', plan)
    plan.append(Macro5)
    Macro5.meta_ID = 'Macro5'
    Macro5.offset.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((-60, 0, 0))))
    Macro5.meta_posX = int(123)
    Macro5.meta_posY = int(388)
    Macro6 = ComponentModel.SysComponent.Macro('BismarkComplete', plan)
    plan.append(Macro6)
    Macro6.meta_ID = 'Macro6'
    Macro6.offset.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((-20, 0, 0))))
    Macro6.meta_posX = int(117)
    Macro6.meta_posY = int(230)
    Macro7 = ComponentModel.SysComponent.Macro('BismarkComplete', plan)
    plan.append(Macro7)
    Macro7.meta_ID = 'Macro7'
    Macro7.offset.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((0, 0, 0))))
    Macro7.meta_posX = int(149)
    Macro7.meta_posY = int(545)
    Sequence8 = ComponentModel.Component.Sequence(int(5))
    plan.append(Sequence8)
    Sequence8.meta_ID = 'Sequence8'
    Sequence8.meta_posY = int(150)
    Sequence8.meta_posX = int(-480)
    Sequence9 = ComponentModel.Component.Sequence(int(2))
    plan.append(Sequence9)
    Sequence9.meta_ID = 'Sequence9'
    Sequence9.meta_posY = int(168)
    Sequence9.meta_posX = int(-866)
    Repeat10 = ComponentModel.Component.Repeat()
    plan.append(Repeat10)
    Repeat10.meta_ID = 'Repeat10'
    Repeat10.meta_posY = int(478)
    Repeat10.meta_posX = int(-714)
    RndFloat11 = VisualScript.RandInRangeFloat()
    plan.append(RndFloat11)
    RndFloat11.meta_ID = 'RndFloat11'
    RndFloat11.a.setAccessor(ComponentModel.ComponentCore.ConstValue(float(1.0)))
    RndFloat11.b.setAccessor(ComponentModel.ComponentCore.ConstValue(float(3.0)))
    RndFloat11.meta_posX = int(-981)
    RndFloat11.meta_posY = int(507)
    WorldEffect12 = ComponentModel.ClientComponents.WorldEffect()
    plan.append(WorldEffect12)
    WorldEffect12.meta_ID = 'WorldEffect12'
    WorldEffect12.effectId.setAccessor(ComponentModel.ComponentCore.ConstValue('EFFECT_BOMB_EXPLOSION_BIG_WATER'))
    WorldEffect12.meta_posY = int(604)
    WorldEffect12.meta_posX = int(-300)
    SplinePoint13 = ComponentModel.Component.SplinePoint()
    plan.append(SplinePoint13)
    SplinePoint13.meta_ID = 'SplinePoint13'
    SplinePoint13.time.setAccessor(ComponentModel.ComponentCore.ConstValue(float(0.0)))
    SplinePoint13.meta_posX = int(-813)
    SplinePoint13.meta_posY = int(601)
    AddV314 = ComponentModel.Component.AddV3()
    plan.append(AddV314)
    AddV314.meta_ID = 'AddV314'
    AddV314.meta_posY = int(641)
    AddV314.meta_posX = int(-616)
    Macro15 = ComponentModel.SysComponent.Macro('RndVector', plan)
    plan.append(Macro15)
    Macro15.meta_ID = 'Macro15'
    Macro15.xRnd.setAccessor(ComponentModel.ComponentCore.ConstValue(float(100.0)))
    Macro15.zRnd.setAccessor(ComponentModel.ComponentCore.ConstValue(float(100.0)))
    Macro15.yRnd.setAccessor(ComponentModel.ComponentCore.ConstValue(float(0.0)))
    Macro15.meta_posX = int(-882)
    Macro15.meta_posY = int(729)
    Sequence16 = ComponentModel.Component.Sequence(int(2))
    plan.append(Sequence16)
    Sequence16.meta_ID = 'Sequence16'
    Sequence16.meta_posY = int(-104)
    Sequence16.meta_posX = int(-923)
    Sequence17 = ComponentModel.Component.Sequence(int(5))
    plan.append(Sequence17)
    Sequence17.meta_ID = 'Sequence17'
    Sequence17.meta_posY = int(-102)
    Sequence17.meta_posX = int(-698)
    Delay18 = VisualScript.Delay()
    plan.append(Delay18)
    Delay18.meta_ID = 'Delay18'
    Delay18.meta_posY = int(-166)
    Delay18.meta_posX = int(-497)
    Delay19 = VisualScript.Delay()
    plan.append(Delay19)
    Delay19.meta_ID = 'Delay19'
    Delay19.meta_posY = int(-96)
    Delay19.meta_posX = int(-474)
    Delay20 = VisualScript.Delay()
    plan.append(Delay20)
    Delay20.meta_ID = 'Delay20'
    Delay20.meta_posY = int(-4)
    Delay20.meta_posX = int(-494)
    RndFloat21 = VisualScript.RandInRangeFloat()
    plan.append(RndFloat21)
    RndFloat21.meta_ID = 'RndFloat21'
    RndFloat21.a.setAccessor(ComponentModel.ComponentCore.ConstValue(float(5.0)))
    RndFloat21.b.setAccessor(ComponentModel.ComponentCore.ConstValue(float(10.0)))
    RndFloat21.meta_posX = int(-740)
    RndFloat21.meta_posY = int(52)
    StartEvent1.out += Sequence16.input
    ConstComponent3.value += Macro2.spline
    ConstComponent3.value += Macro4.spline
    ConstComponent3.value += Macro6.spline
    ConstComponent3.value += Macro5.spline
    ConstComponent3.value += Macro7.spline
    ConstComponent3.value += SplinePoint13.splineId
    Sequence8.o0 += Macro2.start
    Sequence8.o1 += Macro4.start
    Sequence8.o2 += Macro6.start
    Sequence8.o3 += Macro5.start
    Sequence8.o4 += Macro7.start
    Sequence9.o0 += Sequence8.input
    Sequence9.o1 += Repeat10.start
    Repeat10.out += WorldEffect12.input
    RndFloat11.result += Repeat10.time
    SplinePoint13.pos += AddV314.a
    AddV314.result += WorldEffect12.position
    Macro15.out += AddV314.b
    Sequence16.o0 += Sequence17.input
    Sequence16.o1 += Sequence9.input
    Sequence17.o0 += Delay18.start
    Sequence17.o1 += Delay19.start
    Sequence17.o2 += Delay20.start
    Delay18.out += Macro2.damage
    Delay19.out += Macro4.damage
    Delay20.out += Macro6.damage
    RndFloat21.result += Delay20.time
    RndFloat21.result += Delay19.time
    RndFloat21.result += Delay18.time


def createPlan(aspect, entity, controllers):
    funcName = 'fillPlan{0}'.format(str(aspect))
    if funcName in globals():
        planFunc = globals()[funcName]
        if controllers is None:
            controllers = createControllers(aspect, entity)
        plan = ComponentModel.ComponentCore.Plan(controllers, None)
        plan.userVarController = ComponentModel.ContextCore.UserVarController()
        planFunc(plan, aspect)
        return plan
    else:
        return


def getSupportedAspects():
    return 7


def getScriptCategory():
    return ''