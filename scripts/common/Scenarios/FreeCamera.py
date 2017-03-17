# Embedded file name: scripts/common/Scenarios/FreeCamera.py
import os, sys
import ComponentModel.SysComponent
import ComponentModel.CameraController
import ComponentModel.ComponentCore
import VisualScript
import ComponentModel.ContextComponents
import ComponentModel.TypeSystem
import ComponentModel.ScriptUtil
import ComponentModel.ClientComponents
import Math
import ComponentModel.Component

def getParentModule():
    return ''


def createControllers(aspect, entity):
    controllers = []
    controllers.append(ComponentModel.CameraController.CameraController(entity))
    return controllers


def requiredControllers():
    controllers = []
    controllers.append(ComponentModel.CameraController.CameraController)
    return controllers


def getControllerCount():
    return 1


def fillPlan1(plan, aspect):
    ComponentModel.ScriptUtil.fillPlanFromParent(getParentModule(), plan, aspect)


def fillPlan2(plan, aspect):
    ComponentModel.ScriptUtil.fillPlanFromParent(getParentModule(), plan, aspect)
    ContextSet3 = VisualScript.ContextSet(getattr(plan, 'camera'), ComponentModel.TypeSystem.Vector3T, 'POSITION')
    plan.append(ContextSet3)
    ContextSet3.meta_ID = 'ContextSet3'
    ContextSet3.meta_posY = int(546)
    ContextSet3.meta_posX = int(-240)
    FrameEvent2 = ComponentModel.Component.FrameEvent()
    plan.append(FrameEvent2)
    FrameEvent2.meta_ID = 'FrameEvent2'
    FrameEvent2.meta_isCompactForm = bool(True)
    FrameEvent2.meta_posX = int(-1306)
    FrameEvent2.meta_posY = int(116)
    Macro1 = ComponentModel.SysComponent.Macro('TranslateByKey', plan)
    plan.append(Macro1)
    Macro1.meta_ID = 'Macro1'
    Macro1.leftKey.setAccessor(ComponentModel.ComponentCore.ConstValue(int(30)))
    Macro1.RightKey.setAccessor(ComponentModel.ComponentCore.ConstValue(int(32)))
    Macro1.ForwardKey.setAccessor(ComponentModel.ComponentCore.ConstValue(int(17)))
    Macro1.BackKey.setAccessor(ComponentModel.ComponentCore.ConstValue(int(31)))
    Macro1.UpKey.setAccessor(ComponentModel.ComponentCore.ConstValue(int(16)))
    Macro1.DownKey.setAccessor(ComponentModel.ComponentCore.ConstValue(int(44)))
    Macro1.Scale.setAccessor(ComponentModel.ComponentCore.ConstValue(float(0.1)))
    Macro1.meta_posY = int(585)
    Macro1.meta_posX = int(-1239)
    ContextGet3 = VisualScript.ContextGet(getattr(plan, 'camera'), ComponentModel.TypeSystem.FloatT, 'FOV')
    plan.append(ContextGet3)
    ContextGet3.meta_ID = 'ContextGet3'
    ContextGet3.meta_posX = int(-814)
    ContextGet3.meta_posY = int(955)
    Multiply2 = VisualScript.Multiply(int(2))
    plan.append(Multiply2)
    Multiply2.meta_ID = 'Multiply2'
    Multiply2.i2.setAccessor(ComponentModel.ComponentCore.ConstValue(float(0.01)))
    Multiply2.meta_posY = int(866)
    Multiply2.meta_posX = int(-1026)
    ContextSet4 = VisualScript.ContextSet(getattr(plan, 'camera'), ComponentModel.TypeSystem.FloatT, 'FOV')
    plan.append(ContextSet4)
    ContextSet4.meta_ID = 'ContextSet4'
    ContextSet4.meta_posY = int(831)
    ContextSet4.meta_posX = int(-443)
    Add1 = VisualScript.Add(int(2))
    plan.append(Add1)
    Add1.meta_ID = 'Add1'
    Add1.meta_posY = int(865)
    Add1.meta_posX = int(-620)
    MouseEvent1 = ComponentModel.ClientComponents.MouseEvent()
    plan.append(MouseEvent1)
    MouseEvent1.meta_ID = 'MouseEvent1'
    MouseEvent1.meta_posY = int(836)
    MouseEvent1.meta_posX = int(-1215)
    Multiply1 = VisualScript.Multiply(int(2))
    plan.append(Multiply1)
    Multiply1.meta_ID = 'Multiply1'
    Multiply1.i2.setAccessor(ComponentModel.ComponentCore.ConstValue(float(-0.1)))
    Multiply1.meta_posY = int(866)
    Multiply1.meta_posX = int(-820)
    MultiplyV3Float1 = ComponentModel.Component.MultiplyV3Float()
    plan.append(MultiplyV3Float1)
    MultiplyV3Float1.meta_ID = 'MultiplyV3Float1'
    MultiplyV3Float1.f.setAccessor(ComponentModel.ComponentCore.ConstValue(float(1.0)))
    MultiplyV3Float1.meta_posY = int(553)
    MultiplyV3Float1.meta_posX = int(-1026)
    MouseEvent2 = ComponentModel.ClientComponents.MouseEvent()
    plan.append(MouseEvent2)
    MouseEvent2.meta_ID = 'MouseEvent2'
    MouseEvent2.meta_posY = int(-169)
    MouseEvent2.meta_posX = int(-1371)
    CreateV31 = ComponentModel.Component.CreateV3()
    plan.append(CreateV31)
    CreateV31.meta_ID = 'CreateV31'
    CreateV31.meta_posY = int(-77)
    CreateV31.meta_posX = int(-1012)
    CreateMatrix1 = ComponentModel.Component.CreateMatrix()
    plan.append(CreateMatrix1)
    CreateMatrix1.meta_ID = 'CreateMatrix1'
    CreateMatrix1.pos.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((0, 0, 0))))
    CreateMatrix1.scale.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((1, 1, 1))))
    CreateMatrix1.meta_posY = int(201)
    CreateMatrix1.meta_posX = int(-1265)
    TransformV31 = ComponentModel.Component.TransformV3()
    plan.append(TransformV31)
    TransformV31.meta_ID = 'TransformV31'
    TransformV31.v.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((10, 0, 0))))
    TransformV31.meta_posY = int(188)
    TransformV31.meta_posX = int(-946)
    ContextSet7 = VisualScript.ContextSet(getattr(plan, 'camera'), ComponentModel.TypeSystem.Vector3T, 'DIRECTION')
    plan.append(ContextSet7)
    ContextSet7.meta_ID = 'ContextSet7'
    ContextSet7.meta_posY = int(137)
    ContextSet7.meta_posX = int(-654)
    TransformV32 = ComponentModel.Component.TransformV3()
    plan.append(TransformV32)
    TransformV32.meta_ID = 'TransformV32'
    TransformV32.v.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((0, 1, 0))))
    TransformV32.meta_posY = int(281)
    TransformV32.meta_posX = int(-939)
    ContextSet8 = VisualScript.ContextSet(getattr(plan, 'camera'), ComponentModel.TypeSystem.Vector3T, 'UP')
    plan.append(ContextSet8)
    ContextSet8.meta_ID = 'ContextSet8'
    ContextSet8.meta_posY = int(281)
    ContextSet8.meta_posX = int(-671)
    TransformV33 = ComponentModel.Component.TransformV3()
    plan.append(TransformV33)
    TransformV33.meta_ID = 'TransformV33'
    TransformV33.meta_posY = int(555)
    TransformV33.meta_posX = int(-833)
    Macro2 = ComponentModel.SysComponent.Macro('Inertial', plan)
    plan.append(Macro2)
    Macro2.meta_ID = 'Macro2'
    Macro2.HalfLife.setAccessor(ComponentModel.ComponentCore.ConstValue(float(0.95)))
    Macro2.StartPos.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((50, 10, 50))))
    Macro2.meta_posY = int(563)
    Macro2.meta_posX = int(-561)
    Macro3 = ComponentModel.SysComponent.Macro('Inertial', plan)
    plan.append(Macro3)
    Macro3.meta_ID = 'Macro3'
    Macro3.HalfLife.setAccessor(ComponentModel.ComponentCore.ConstValue(float(0.95)))
    Macro3.StartPos.setAccessor(ComponentModel.ComponentCore.ConstValue(Math.Vector3((0, 0, 0))))
    Macro3.meta_posY = int(-231)
    Macro3.meta_posX = int(-576)
    MultiplyV3Float2 = ComponentModel.Component.MultiplyV3Float()
    plan.append(MultiplyV3Float2)
    MultiplyV3Float2.meta_ID = 'MultiplyV3Float2'
    MultiplyV3Float2.f.setAccessor(ComponentModel.ComponentCore.ConstValue(float(0.01)))
    MultiplyV3Float2.meta_posY = int(-88)
    MultiplyV3Float2.meta_posX = int(-837)
    Multiply3 = VisualScript.Multiply(int(2))
    plan.append(Multiply3)
    Multiply3.meta_ID = 'Multiply3'
    Multiply3.i2.setAccessor(ComponentModel.ComponentCore.ConstValue(float(0.1)))
    Multiply3.meta_posY = int(-111)
    Multiply3.meta_posX = int(-1188)
    Multiply4 = VisualScript.Multiply(int(2))
    plan.append(Multiply4)
    Multiply4.meta_ID = 'Multiply4'
    Multiply4.i2.setAccessor(ComponentModel.ComponentCore.ConstValue(float(-0.1)))
    Multiply4.meta_posY = int(-29)
    Multiply4.meta_posX = int(-1192)
    FrameEvent2.out += ContextSet7.input
    Macro1.pos += MultiplyV3Float1.v
    ContextGet3.value += Add1.i2
    Multiply2.result += Multiply1.i1
    Add1.result += ContextSet4.value
    MouseEvent1.out += ContextSet4.input
    MouseEvent1.dz += Multiply2.i1
    Multiply1.result += Add1.i1
    MultiplyV3Float1.result += TransformV33.v
    MouseEvent2.out += Macro3.AddForce
    MouseEvent2.dx += Multiply3.i1
    MouseEvent2.dy += Multiply4.i1
    CreateV31.result += MultiplyV3Float2.v
    CreateMatrix1.result += TransformV31.m
    CreateMatrix1.result += TransformV32.m
    CreateMatrix1.result += TransformV33.m
    TransformV31.result += ContextSet7.value
    ContextSet7.out += ContextSet8.input
    TransformV32.result += ContextSet8.value
    TransformV33.result += Macro2.Force
    Macro2.Position += ContextSet3.value
    Macro2.OnChange += ContextSet3.input
    Macro3.Position += CreateMatrix1.rotation
    MultiplyV3Float2.result += Macro3.AdditionForce
    Multiply3.result += CreateV31.x
    Multiply4.result += CreateV31.z
    group1 = ComponentModel.ComponentCore.ComponentGroup()
    plan.groups.append(group1)
    group1.meta_ID = 'group1'
    group1.meta_posX = -794
    group1.meta_posY = 873
    group1.meta_width = 1023
    group1.meta_height = 281
    group1.meta_title = 'Zoom'
    group1.components = [Multiply2,
     ContextSet4,
     MouseEvent1,
     ContextGet3,
     Add1,
     Multiply1]
    group2 = ComponentModel.ComponentCore.ComponentGroup()
    plan.groups.append(group2)
    group2.meta_ID = 'group2'
    group2.meta_posX = -737
    group2.meta_posY = 566
    group2.meta_width = 1246
    group2.meta_height = 274
    group2.meta_title = 'Move'
    group2.components = [MultiplyV3Float1,
     TransformV33,
     ContextSet3,
     Macro1,
     Macro2]
    group4 = ComponentModel.ComponentCore.ComponentGroup()
    plan.groups.append(group4)
    group4.meta_ID = 'group4'
    group4.meta_posX = -935
    group4.meta_posY = 201
    group4.meta_width = 979
    group4.meta_height = 299
    group4.meta_title = 'Rotation'
    group4.components = [TransformV32,
     FrameEvent2,
     TransformV31,
     ContextSet7,
     CreateMatrix1,
     ContextSet8]
    group3 = ComponentModel.ComponentCore.ComponentGroup()
    plan.groups.append(group3)
    group3.meta_ID = 'group3'
    group3.meta_posX = -931
    group3.meta_posY = -185
    group3.meta_width = 1038
    group3.meta_height = 332
    group3.meta_title = 'Mouse'
    group3.components = [Macro3,
     Multiply3,
     CreateV31,
     MultiplyV3Float2,
     MouseEvent2]


def createPlan(aspect, entity, controllers):
    funcName = 'fillPlan{0}'.format(str(aspect))
    if funcName in globals():
        planFunc = globals()[funcName]
        if controllers is None:
            controllers = createControllers(aspect, entity)
        plan = ComponentModel.ComponentCore.Plan(controllers, ComponentModel.ContextCore.UserVarController())
        planFunc(plan, aspect)
        return plan
    else:
        return


def getSupportedAspects():
    return 7


def getScriptCategory():
    return ''