# Embedded file name: scripts/common/_gunsProfiles.py
import Math
import math
import consts
true = True
false = False

class Dummy:
    pass


isServerDatabase = False
from consts import GUN_TYPE
from Curve import Curve
GUN_NORMAL = GUN_TYPE.NORMAL
GUN_AA = GUN_TYPE.AA
GUN_AA_NORMAL = GUN_TYPE.AA_NORMAL

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


GunsProfiles = Dummy()
GunsProfiles.ammo = []
GunsProfiles.ammo.insert(0, None)
GunsProfiles.ammo[0] = Dummy()
GunsProfiles.ammo[0].bulletColour = 4294927365L
GunsProfiles.ammo[0].name = 'Amachinegun_small_low_base'.lower()
GunsProfiles.ammo[0].smokeColour = 1694498815
GunsProfiles.ammo.insert(1, None)
GunsProfiles.ammo[1] = Dummy()
GunsProfiles.ammo[1].bulletColour = 4294927365L
GunsProfiles.ammo[1].name = 'Amachinegun_small_low_silver'.lower()
GunsProfiles.ammo[1].smokeColour = 1694498815
GunsProfiles.ammo.insert(2, None)
GunsProfiles.ammo[2] = Dummy()
GunsProfiles.ammo[2].bulletColour = 4294927365L
GunsProfiles.ammo[2].name = 'Amachinegun_small_low_crit'.lower()
GunsProfiles.ammo[2].smokeColour = 1694498815
GunsProfiles.ammo.insert(3, None)
GunsProfiles.ammo[3] = Dummy()
GunsProfiles.ammo[3].bulletColour = 4294927365L
GunsProfiles.ammo[3].name = 'Amachinegun_small_low_fire'.lower()
GunsProfiles.ammo[3].smokeColour = 1694498815
GunsProfiles.ammo.insert(4, None)
GunsProfiles.ammo[4] = Dummy()
GunsProfiles.ammo[4].bulletColour = 4294927365L
GunsProfiles.ammo[4].name = 'Amachinegun_small_low_ground'.lower()
GunsProfiles.ammo[4].smokeColour = 1694498815
GunsProfiles.ammo.insert(5, None)
GunsProfiles.ammo[5] = Dummy()
GunsProfiles.ammo[5].bulletColour = 4294927365L
GunsProfiles.ammo[5].name = 'Amachinegun_small_default_base'.lower()
GunsProfiles.ammo[5].smokeColour = 352321535
GunsProfiles.ammo.insert(6, None)
GunsProfiles.ammo[6] = Dummy()
GunsProfiles.ammo[6].bulletColour = 4294927365L
GunsProfiles.ammo[6].name = 'Amachinegun_small_default_silver'.lower()
GunsProfiles.ammo[6].smokeColour = 352321535
GunsProfiles.ammo.insert(7, None)
GunsProfiles.ammo[7] = Dummy()
GunsProfiles.ammo[7].bulletColour = 4294927365L
GunsProfiles.ammo[7].name = 'Amachinegun_small_default_crit'.lower()
GunsProfiles.ammo[7].smokeColour = 352321535
GunsProfiles.ammo.insert(8, None)
GunsProfiles.ammo[8] = Dummy()
GunsProfiles.ammo[8].bulletColour = 4294927365L
GunsProfiles.ammo[8].name = 'Amachinegun_small_default_fire'.lower()
GunsProfiles.ammo[8].smokeColour = 352321535
GunsProfiles.ammo.insert(9, None)
GunsProfiles.ammo[9] = Dummy()
GunsProfiles.ammo[9].bulletColour = 4294927365L
GunsProfiles.ammo[9].name = 'Amachinegun_small_default_ground'.lower()
GunsProfiles.ammo[9].smokeColour = 352321535
GunsProfiles.ammo.insert(10, None)
GunsProfiles.ammo[10] = Dummy()
GunsProfiles.ammo[10].bulletColour = 4294904325L
GunsProfiles.ammo[10].name = 'Amachinegun_heavy_default_base'.lower()
GunsProfiles.ammo[10].smokeColour = 352321535
GunsProfiles.ammo.insert(11, None)
GunsProfiles.ammo[11] = Dummy()
GunsProfiles.ammo[11].bulletColour = 4294904325L
GunsProfiles.ammo[11].name = 'Amachinegun_heavy_default_silver'.lower()
GunsProfiles.ammo[11].smokeColour = 352321535
GunsProfiles.ammo.insert(12, None)
GunsProfiles.ammo[12] = Dummy()
GunsProfiles.ammo[12].bulletColour = 4294904325L
GunsProfiles.ammo[12].name = 'Amachinegun_heavy_default_crit'.lower()
GunsProfiles.ammo[12].smokeColour = 352321535
GunsProfiles.ammo.insert(13, None)
GunsProfiles.ammo[13] = Dummy()
GunsProfiles.ammo[13].bulletColour = 4294904325L
GunsProfiles.ammo[13].name = 'Amachinegun_heavy_default_fire'.lower()
GunsProfiles.ammo[13].smokeColour = 352321535
GunsProfiles.ammo.insert(14, None)
GunsProfiles.ammo[14] = Dummy()
GunsProfiles.ammo[14].bulletColour = 4294904325L
GunsProfiles.ammo[14].name = 'Amachinegun_heavy_default_ground'.lower()
GunsProfiles.ammo[14].smokeColour = 352321535
GunsProfiles.ammo.insert(15, None)
GunsProfiles.ammo[15] = Dummy()
GunsProfiles.ammo[15].bulletColour = 4294940170L
GunsProfiles.ammo[15].name = 'Acannon_main_default_base'.lower()
GunsProfiles.ammo[15].smokeColour = 855638015
GunsProfiles.ammo.insert(16, None)
GunsProfiles.ammo[16] = Dummy()
GunsProfiles.ammo[16].bulletColour = 4294940170L
GunsProfiles.ammo[16].name = 'Acannon_main_default_silver'.lower()
GunsProfiles.ammo[16].smokeColour = 855638015
GunsProfiles.ammo.insert(17, None)
GunsProfiles.ammo[17] = Dummy()
GunsProfiles.ammo[17].bulletColour = 4294940170L
GunsProfiles.ammo[17].name = 'Acannon_main_default_crit'.lower()
GunsProfiles.ammo[17].smokeColour = 855638015
GunsProfiles.ammo.insert(18, None)
GunsProfiles.ammo[18] = Dummy()
GunsProfiles.ammo[18].bulletColour = 4294940170L
GunsProfiles.ammo[18].name = 'Acannon_main_default_fire'.lower()
GunsProfiles.ammo[18].smokeColour = 855638015
GunsProfiles.ammo.insert(19, None)
GunsProfiles.ammo[19] = Dummy()
GunsProfiles.ammo[19].bulletColour = 4294940170L
GunsProfiles.ammo[19].name = 'Acannon_main_default_ground'.lower()
GunsProfiles.ammo[19].smokeColour = 855638015
GunsProfiles.ammo.insert(20, None)
GunsProfiles.ammo[20] = Dummy()
GunsProfiles.ammo[20].bulletColour = 4294904325L
GunsProfiles.ammo[20].name = 'Acannon_high_default_base'.lower()
GunsProfiles.ammo[20].smokeColour = 855638015
GunsProfiles.ammo.insert(21, None)
GunsProfiles.ammo[21] = Dummy()
GunsProfiles.ammo[21].bulletColour = 4294904325L
GunsProfiles.ammo[21].name = 'Acannon_high_default_silver'.lower()
GunsProfiles.ammo[21].smokeColour = 855638015
GunsProfiles.ammo.insert(22, None)
GunsProfiles.ammo[22] = Dummy()
GunsProfiles.ammo[22].bulletColour = 4294904325L
GunsProfiles.ammo[22].name = 'Acannon_high_default_crit'.lower()
GunsProfiles.ammo[22].smokeColour = 855638015
GunsProfiles.ammo.insert(23, None)
GunsProfiles.ammo[23] = Dummy()
GunsProfiles.ammo[23].bulletColour = 4294904325L
GunsProfiles.ammo[23].name = 'Acannon_high_default_fire'.lower()
GunsProfiles.ammo[23].smokeColour = 855638015
GunsProfiles.ammo.insert(24, None)
GunsProfiles.ammo[24] = Dummy()
GunsProfiles.ammo[24].bulletColour = 4294904325L
GunsProfiles.ammo[24].name = 'Acannon_high_default_ground'.lower()
GunsProfiles.ammo[24].smokeColour = 855638015
GunsProfiles.ammo.insert(25, None)
GunsProfiles.ammo[25] = Dummy()
GunsProfiles.ammo[25].bulletColour = 4278910730L
GunsProfiles.ammo[25].name = 'Aheavycannon_alpha_default_base'.lower()
GunsProfiles.ammo[25].smokeColour = 3869944490L
GunsProfiles.ammo.insert(26, None)
GunsProfiles.ammo[26] = Dummy()
GunsProfiles.ammo[26].bulletColour = 4278910730L
GunsProfiles.ammo[26].name = 'Aheavycannon_alpha_default_silver'.lower()
GunsProfiles.ammo[26].smokeColour = 3869944490L
GunsProfiles.ammo.insert(27, None)
GunsProfiles.ammo[27] = Dummy()
GunsProfiles.ammo[27].bulletColour = 4278910730L
GunsProfiles.ammo[27].name = 'Aheavycannon_alpha_default_crit'.lower()
GunsProfiles.ammo[27].smokeColour = 3869944490L
GunsProfiles.ammo.insert(28, None)
GunsProfiles.ammo[28] = Dummy()
GunsProfiles.ammo[28].bulletColour = 4278910730L
GunsProfiles.ammo[28].name = 'Aheavycannon_alpha_default_fire'.lower()
GunsProfiles.ammo[28].smokeColour = 3869944490L
GunsProfiles.ammo.insert(29, None)
GunsProfiles.ammo[29] = Dummy()
GunsProfiles.ammo[29].bulletColour = 4278910730L
GunsProfiles.ammo[29].name = 'Aheavycannon_alpha_default_ground'.lower()
GunsProfiles.ammo[29].smokeColour = 3869944490L
GunsProfiles.ammo.insert(30, None)
GunsProfiles.ammo[30] = Dummy()
GunsProfiles.ammo[30].bulletColour = 4288059000L
GunsProfiles.ammo[30].name = 'Aheavycannon_granade_default_base'.lower()
GunsProfiles.ammo[30].smokeColour = 2527767210L
GunsProfiles.ammo.insert(31, None)
GunsProfiles.ammo[31] = Dummy()
GunsProfiles.ammo[31].bulletColour = 4288059000L
GunsProfiles.ammo[31].name = 'Aheavycannon_granade_default_silver'.lower()
GunsProfiles.ammo[31].smokeColour = 2527767210L
GunsProfiles.ammo.insert(32, None)
GunsProfiles.ammo[32] = Dummy()
GunsProfiles.ammo[32].bulletColour = 4288059000L
GunsProfiles.ammo[32].name = 'Aheavycannon_granade_default_crit'.lower()
GunsProfiles.ammo[32].smokeColour = 2527767210L
GunsProfiles.ammo.insert(33, None)
GunsProfiles.ammo[33] = Dummy()
GunsProfiles.ammo[33].bulletColour = 4288059000L
GunsProfiles.ammo[33].name = 'Aheavycannon_granade_default_fire'.lower()
GunsProfiles.ammo[33].smokeColour = 2527767210L
GunsProfiles.ammo.insert(34, None)
GunsProfiles.ammo[34] = Dummy()
GunsProfiles.ammo[34].bulletColour = 4288059000L
GunsProfiles.ammo[34].name = 'Aheavycannon_granade_default_ground'.lower()
GunsProfiles.ammo[34].smokeColour = 2527767210L
GunsProfiles.ammo.insert(35, None)
GunsProfiles.ammo[35] = Dummy()
GunsProfiles.ammo[35].bulletColour = 4294904325L
GunsProfiles.ammo[35].name = 'Aheavycannon_granade_high_default_base'.lower()
GunsProfiles.ammo[35].smokeColour = 1688906410
GunsProfiles.ammo.insert(36, None)
GunsProfiles.ammo[36] = Dummy()
GunsProfiles.ammo[36].bulletColour = 4294904325L
GunsProfiles.ammo[36].name = 'Aheavycannon_granade_high_default_silver'.lower()
GunsProfiles.ammo[36].smokeColour = 1688906410
GunsProfiles.ammo.insert(37, None)
GunsProfiles.ammo[37] = Dummy()
GunsProfiles.ammo[37].bulletColour = 4294904325L
GunsProfiles.ammo[37].name = 'Aheavycannon_granade_high_default_crit'.lower()
GunsProfiles.ammo[37].smokeColour = 1688906410
GunsProfiles.ammo.insert(38, None)
GunsProfiles.ammo[38] = Dummy()
GunsProfiles.ammo[38].bulletColour = 4294904325L
GunsProfiles.ammo[38].name = 'Aheavycannon_granade_high_default_fire'.lower()
GunsProfiles.ammo[38].smokeColour = 1688906410
GunsProfiles.ammo.insert(39, None)
GunsProfiles.ammo[39] = Dummy()
GunsProfiles.ammo[39].bulletColour = 4294904325L
GunsProfiles.ammo[39].name = 'Aheavycannon_granade_high_default_ground'.lower()
GunsProfiles.ammo[39].smokeColour = 1688906410
GunsProfiles.ammo.insert(40, None)
GunsProfiles.ammo[40] = Dummy()
GunsProfiles.ammo[40].bulletColour = 4294967295L
GunsProfiles.ammo[40].name = 'G0mm_ap'.lower()
GunsProfiles.ammo[40].smokeColour = 16777215
GunsProfiles.ammo.insert(41, None)
GunsProfiles.ammo[41] = Dummy()
GunsProfiles.ammo[41].bulletColour = 4294909440L
GunsProfiles.ammo[41].name = 'turret_7mm'.lower()
GunsProfiles.ammo[41].smokeColour = 184549375
GunsProfiles.ammo.insert(42, None)
GunsProfiles.ammo[42] = Dummy()
GunsProfiles.ammo[42].bulletColour = 4294909442L
GunsProfiles.ammo[42].name = 'turret_AA1'.lower()
GunsProfiles.ammo[42].smokeColour = 4294967295L
GunsProfiles.ammo.insert(43, None)
GunsProfiles.ammo[43] = Dummy()
GunsProfiles.ammo[43].bulletColour = 4294909442L
GunsProfiles.ammo[43].name = 'turret_air_7mm'.lower()
GunsProfiles.ammo[43].smokeColour = 687865855
GunsProfiles.ammo.insert(44, None)
GunsProfiles.ammo[44] = Dummy()
GunsProfiles.ammo[44].bulletColour = 4294909442L
GunsProfiles.ammo[44].name = 'turret_air_12mm'.lower()
GunsProfiles.ammo[44].smokeColour = 687865855
GunsProfiles.ammo.insert(45, None)
GunsProfiles.ammo[45] = Dummy()
GunsProfiles.ammo[45].bulletColour = 4294909442L
GunsProfiles.ammo[45].name = 'turret_air_13mm'.lower()
GunsProfiles.ammo[45].smokeColour = 687865855
GunsProfiles.ammo.insert(46, None)
GunsProfiles.ammo[46] = Dummy()
GunsProfiles.ammo[46].bulletColour = 4294909442L
GunsProfiles.ammo[46].name = 'turret_air_20mm'.lower()
GunsProfiles.ammo[46].smokeColour = 687865855
GunsProfiles.ammo.insert(47, None)
GunsProfiles.ammo[47] = Dummy()
GunsProfiles.ammo[47].bulletColour = 4294909442L
GunsProfiles.ammo[47].name = 'turret_air_23mm'.lower()
GunsProfiles.ammo[47].smokeColour = 687865855
GunsProfiles.ammo.insert(48, None)
GunsProfiles.ammo[48] = Dummy()
GunsProfiles.ammo[48].bulletColour = 4294909442L
GunsProfiles.ammo[48].name = 'turret_holiday'.lower()
GunsProfiles.ammo[48].smokeColour = 1023410175
GunsProfiles.gunProfile = []
GunsProfiles.gunProfile.insert(0, None)
GunsProfiles.gunProfile[0] = Dummy()
GunsProfiles.gunProfile[0].asyncDelay = 0.2
GunsProfiles.gunProfile[0].bulletLen = 0.4
GunsProfiles.gunProfile[0].bulletLenExpand = 5.0
GunsProfiles.gunProfile[0].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[0].bulletShot = []
GunsProfiles.gunProfile[0].bulletShot.insert(0, None)
GunsProfiles.gunProfile[0].bulletShot[0] = 'particles/weapons/gun_flash_mg.xml'
GunsProfiles.gunProfile[0].bulletShot.insert(1, None)
GunsProfiles.gunProfile[0].bulletShot[1] = 'particles/weapons/gun_flash_mg_add.xml'
GunsProfiles.gunProfile[0].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[0].bulletThinkness = 0.03
GunsProfiles.gunProfile[0].clientSkipBulletCount = 1
GunsProfiles.gunProfile[0].explosionParticles = Dummy()
GunsProfiles.gunProfile[0].explosionParticles.aircraft = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[0].explosionParticles.baseobject = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[0].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[0].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[0].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[0].explosionParticles.turret = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[0].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[0].hudIcoPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[0].iconEmptyPath = 'icons/weapons/iconWeapGunRunOut.tga'
GunsProfiles.gunProfile[0].name = 'machinegun_small_low'.lower()
GunsProfiles.gunProfile[0].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[0].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[0].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[0].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[0].shellOutInterval = 0.0
GunsProfiles.gunProfile[0].smokeRadiusScale = 0.5
GunsProfiles.gunProfile[0].smokeSizeX = 2.0
GunsProfiles.gunProfile[0].smokeSizeY = 0.035
GunsProfiles.gunProfile[0].smokeTillingLength = 0.35
GunsProfiles.gunProfile[0].sounds = Dummy()
GunsProfiles.gunProfile[0].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[0].sounds.weaponSoundID = 'weapon_machinegun_low'
GunsProfiles.gunProfile[0].textureIndex = 1
GunsProfiles.gunProfile[0].ttxIcoPath = 'icons/characteristics/iconCharMachineGun.png'
GunsProfiles.gunProfile.insert(1, None)
GunsProfiles.gunProfile[1] = Dummy()
GunsProfiles.gunProfile[1].asyncDelay = 0.2
GunsProfiles.gunProfile[1].bulletLen = 0.4
GunsProfiles.gunProfile[1].bulletLenExpand = 4.0
GunsProfiles.gunProfile[1].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[1].bulletShot = []
GunsProfiles.gunProfile[1].bulletShot.insert(0, None)
GunsProfiles.gunProfile[1].bulletShot[0] = 'particles/weapons/gun_flash_mg.xml'
GunsProfiles.gunProfile[1].bulletShot.insert(1, None)
GunsProfiles.gunProfile[1].bulletShot[1] = 'particles/weapons/gun_flash_mg_add.xml'
GunsProfiles.gunProfile[1].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[1].bulletThinkness = 0.03
GunsProfiles.gunProfile[1].clientSkipBulletCount = 1
GunsProfiles.gunProfile[1].explosionParticles = Dummy()
GunsProfiles.gunProfile[1].explosionParticles.aircraft = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[1].explosionParticles.baseobject = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[1].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[1].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[1].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[1].explosionParticles.turret = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[1].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[1].hudIcoPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[1].iconEmptyPath = 'icons/weapons/iconWeapGunRunOut.tga'
GunsProfiles.gunProfile[1].name = 'machinegun_small'.lower()
GunsProfiles.gunProfile[1].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[1].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[1].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[1].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[1].shellOutInterval = 0.0
GunsProfiles.gunProfile[1].smokeRadiusScale = 0.5
GunsProfiles.gunProfile[1].smokeSizeX = 2.0
GunsProfiles.gunProfile[1].smokeSizeY = 0.035
GunsProfiles.gunProfile[1].smokeTillingLength = 0.35
GunsProfiles.gunProfile[1].sounds = Dummy()
GunsProfiles.gunProfile[1].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[1].sounds.weaponSoundID = 'weapon_machinegun_small'
GunsProfiles.gunProfile[1].textureIndex = 1
GunsProfiles.gunProfile[1].ttxIcoPath = 'icons/characteristics/iconCharMachineGun.png'
GunsProfiles.gunProfile.insert(2, None)
GunsProfiles.gunProfile[2] = Dummy()
GunsProfiles.gunProfile[2].asyncDelay = 0.2
GunsProfiles.gunProfile[2].bulletLen = 0.4
GunsProfiles.gunProfile[2].bulletLenExpand = 4.0
GunsProfiles.gunProfile[2].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[2].bulletShot = []
GunsProfiles.gunProfile[2].bulletShot.insert(0, None)
GunsProfiles.gunProfile[2].bulletShot[0] = 'particles/weapons/gun_flash_mg.xml'
GunsProfiles.gunProfile[2].bulletShot.insert(1, None)
GunsProfiles.gunProfile[2].bulletShot[1] = 'particles/weapons/gun_flash_mg_add.xml'
GunsProfiles.gunProfile[2].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[2].bulletThinkness = 0.03
GunsProfiles.gunProfile[2].clientSkipBulletCount = 3
GunsProfiles.gunProfile[2].explosionParticles = Dummy()
GunsProfiles.gunProfile[2].explosionParticles.aircraft = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[2].explosionParticles.baseobject = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[2].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[2].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[2].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[2].explosionParticles.turret = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[2].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[2].hudIcoPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[2].iconEmptyPath = 'icons/weapons/iconWeapGunRunOut.tga'
GunsProfiles.gunProfile[2].name = 'machinegun_small_spec'.lower()
GunsProfiles.gunProfile[2].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[2].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[2].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[2].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[2].shellOutInterval = 0.0
GunsProfiles.gunProfile[2].smokeRadiusScale = 0.5
GunsProfiles.gunProfile[2].smokeSizeX = 2.0
GunsProfiles.gunProfile[2].smokeSizeY = 0.035
GunsProfiles.gunProfile[2].smokeTillingLength = 0.35
GunsProfiles.gunProfile[2].sounds = Dummy()
GunsProfiles.gunProfile[2].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[2].sounds.weaponSoundID = 'weapon_machinegun_small'
GunsProfiles.gunProfile[2].textureIndex = 1
GunsProfiles.gunProfile[2].ttxIcoPath = 'icons/characteristics/iconCharMachineGun.png'
GunsProfiles.gunProfile.insert(3, None)
GunsProfiles.gunProfile[3] = Dummy()
GunsProfiles.gunProfile[3].asyncDelay = 0.2
GunsProfiles.gunProfile[3].bulletLen = 0.7
GunsProfiles.gunProfile[3].bulletLenExpand = 5.0
GunsProfiles.gunProfile[3].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[3].bulletShot = []
GunsProfiles.gunProfile[3].bulletShot.insert(0, None)
GunsProfiles.gunProfile[3].bulletShot[0] = 'particles/weapons/gun_flash_mg_heavy.xml'
GunsProfiles.gunProfile[3].bulletShot.insert(1, None)
GunsProfiles.gunProfile[3].bulletShot[1] = 'particles/weapons/gun_flash_mg_heavy_add.xml'
GunsProfiles.gunProfile[3].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[3].bulletThinkness = 0.05
GunsProfiles.gunProfile[3].clientSkipBulletCount = 1
GunsProfiles.gunProfile[3].explosionParticles = Dummy()
GunsProfiles.gunProfile[3].explosionParticles.aircraft = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[3].explosionParticles.baseobject = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[3].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[3].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[3].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[3].explosionParticles.turret = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[3].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[3].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[3].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[3].name = 'machinegun_heavy'.lower()
GunsProfiles.gunProfile[3].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[3].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[3].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[3].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[3].shellOutInterval = 0.0
GunsProfiles.gunProfile[3].smokeRadiusScale = 0.5
GunsProfiles.gunProfile[3].smokeSizeX = 2.0
GunsProfiles.gunProfile[3].smokeSizeY = 0.035
GunsProfiles.gunProfile[3].smokeTillingLength = 0.35
GunsProfiles.gunProfile[3].sounds = Dummy()
GunsProfiles.gunProfile[3].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[3].sounds.weaponSoundID = 'weapon_machinegun_heavy'
GunsProfiles.gunProfile[3].textureIndex = 1
GunsProfiles.gunProfile[3].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(4, None)
GunsProfiles.gunProfile[4] = Dummy()
GunsProfiles.gunProfile[4].asyncDelay = 0.2
GunsProfiles.gunProfile[4].bulletLen = 0.7
GunsProfiles.gunProfile[4].bulletLenExpand = 5.0
GunsProfiles.gunProfile[4].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[4].bulletShot = []
GunsProfiles.gunProfile[4].bulletShot.insert(0, None)
GunsProfiles.gunProfile[4].bulletShot[0] = 'particles/weapons/gun_flash_mg_heavy.xml'
GunsProfiles.gunProfile[4].bulletShot.insert(1, None)
GunsProfiles.gunProfile[4].bulletShot[1] = 'particles/weapons/gun_flash_mg_heavy_add.xml'
GunsProfiles.gunProfile[4].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[4].bulletThinkness = 0.05
GunsProfiles.gunProfile[4].clientSkipBulletCount = 3
GunsProfiles.gunProfile[4].explosionParticles = Dummy()
GunsProfiles.gunProfile[4].explosionParticles.aircraft = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[4].explosionParticles.baseobject = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[4].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[4].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[4].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[4].explosionParticles.turret = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[4].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[4].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[4].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[4].name = 'machinegun_heavy_spec'.lower()
GunsProfiles.gunProfile[4].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[4].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[4].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[4].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[4].shellOutInterval = 0.0
GunsProfiles.gunProfile[4].smokeRadiusScale = 0.5
GunsProfiles.gunProfile[4].smokeSizeX = 2.0
GunsProfiles.gunProfile[4].smokeSizeY = 0.035
GunsProfiles.gunProfile[4].smokeTillingLength = 0.35
GunsProfiles.gunProfile[4].sounds = Dummy()
GunsProfiles.gunProfile[4].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[4].sounds.weaponSoundID = 'weapon_machinegun_heavy'
GunsProfiles.gunProfile[4].textureIndex = 1
GunsProfiles.gunProfile[4].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(5, None)
GunsProfiles.gunProfile[5] = Dummy()
GunsProfiles.gunProfile[5].asyncDelay = 0.2
GunsProfiles.gunProfile[5].bulletLen = 1.0
GunsProfiles.gunProfile[5].bulletLenExpand = 10.0
GunsProfiles.gunProfile[5].bulletShell = 'particles/weapons/ammo_cartridge_15-23.xml'
GunsProfiles.gunProfile[5].bulletShot = []
GunsProfiles.gunProfile[5].bulletShot.insert(0, None)
GunsProfiles.gunProfile[5].bulletShot[0] = 'particles/weapons/gun_flash_cannon.xml'
GunsProfiles.gunProfile[5].bulletShot.insert(1, None)
GunsProfiles.gunProfile[5].bulletShot[1] = 'particles/weapons/gun_flash_cannon_add.xml'
GunsProfiles.gunProfile[5].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[5].bulletThinkness = 0.07
GunsProfiles.gunProfile[5].clientSkipBulletCount = 1
GunsProfiles.gunProfile[5].explosionParticles = Dummy()
GunsProfiles.gunProfile[5].explosionParticles.aircraft = 'EFFECT_BULLET_20MM_30MM_HIT'
GunsProfiles.gunProfile[5].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[5].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[5].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[5].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[5].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[5].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[5].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[5].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[5].name = 'cannon_main'.lower()
GunsProfiles.gunProfile[5].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[5].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[5].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[5].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[5].shellOutInterval = 0.0
GunsProfiles.gunProfile[5].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[5].smokeSizeX = 2.0
GunsProfiles.gunProfile[5].smokeSizeY = 0.06
GunsProfiles.gunProfile[5].smokeTillingLength = 0.6
GunsProfiles.gunProfile[5].sounds = Dummy()
GunsProfiles.gunProfile[5].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[5].sounds.weaponSoundID = 'weapon_cannon_main'
GunsProfiles.gunProfile[5].textureIndex = 0
GunsProfiles.gunProfile[5].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(6, None)
GunsProfiles.gunProfile[6] = Dummy()
GunsProfiles.gunProfile[6].asyncDelay = 0.2
GunsProfiles.gunProfile[6].bulletLen = 1.0
GunsProfiles.gunProfile[6].bulletLenExpand = 10.0
GunsProfiles.gunProfile[6].bulletShell = 'particles/weapons/ammo_cartridge_15-23.xml'
GunsProfiles.gunProfile[6].bulletShot = []
GunsProfiles.gunProfile[6].bulletShot.insert(0, None)
GunsProfiles.gunProfile[6].bulletShot[0] = 'particles/weapons/gun_flash_cannon_spec.xml'
GunsProfiles.gunProfile[6].bulletShot.insert(1, None)
GunsProfiles.gunProfile[6].bulletShot[1] = 'particles/weaponsgun_flash_cannon_spec_add.xml'
GunsProfiles.gunProfile[6].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[6].bulletThinkness = 0.07
GunsProfiles.gunProfile[6].clientSkipBulletCount = 1
GunsProfiles.gunProfile[6].explosionParticles = Dummy()
GunsProfiles.gunProfile[6].explosionParticles.aircraft = 'EFFECT_BULLET_20MM_30MM_HIT'
GunsProfiles.gunProfile[6].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[6].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[6].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[6].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[6].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[6].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[6].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[6].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[6].name = 'cannon_main_spec'.lower()
GunsProfiles.gunProfile[6].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[6].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[6].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[6].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[6].shellOutInterval = 0.0
GunsProfiles.gunProfile[6].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[6].smokeSizeX = 2.0
GunsProfiles.gunProfile[6].smokeSizeY = 0.06
GunsProfiles.gunProfile[6].smokeTillingLength = 0.6
GunsProfiles.gunProfile[6].sounds = Dummy()
GunsProfiles.gunProfile[6].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[6].sounds.weaponSoundID = 'weapon_cannon_main'
GunsProfiles.gunProfile[6].textureIndex = 0
GunsProfiles.gunProfile[6].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(7, None)
GunsProfiles.gunProfile[7] = Dummy()
GunsProfiles.gunProfile[7].asyncDelay = 0.2
GunsProfiles.gunProfile[7].bulletLen = 1.0
GunsProfiles.gunProfile[7].bulletLenExpand = 10.0
GunsProfiles.gunProfile[7].bulletShell = 'particles/weapons/ammo_cartridge_15-23.xml'
GunsProfiles.gunProfile[7].bulletShot = []
GunsProfiles.gunProfile[7].bulletShot.insert(0, None)
GunsProfiles.gunProfile[7].bulletShot[0] = 'particles/weapons/gun_flash_cannon_high.xml'
GunsProfiles.gunProfile[7].bulletShot.insert(1, None)
GunsProfiles.gunProfile[7].bulletShot[1] = 'particles/weapons/gun_flash_cannon_high_add.xml'
GunsProfiles.gunProfile[7].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[7].bulletThinkness = 0.07
GunsProfiles.gunProfile[7].clientSkipBulletCount = 1
GunsProfiles.gunProfile[7].explosionParticles = Dummy()
GunsProfiles.gunProfile[7].explosionParticles.aircraft = 'EFFECT_BULLET_20MM_30MM_HIT'
GunsProfiles.gunProfile[7].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[7].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[7].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[7].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[7].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[7].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[7].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[7].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[7].name = 'cannon_high'.lower()
GunsProfiles.gunProfile[7].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[7].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[7].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[7].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[7].shellOutInterval = 0.0
GunsProfiles.gunProfile[7].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[7].smokeSizeX = 2.0
GunsProfiles.gunProfile[7].smokeSizeY = 0.06
GunsProfiles.gunProfile[7].smokeTillingLength = 0.6
GunsProfiles.gunProfile[7].sounds = Dummy()
GunsProfiles.gunProfile[7].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[7].sounds.weaponSoundID = 'weapon_cannon_high'
GunsProfiles.gunProfile[7].textureIndex = 0
GunsProfiles.gunProfile[7].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(8, None)
GunsProfiles.gunProfile[8] = Dummy()
GunsProfiles.gunProfile[8].asyncDelay = 0.2
GunsProfiles.gunProfile[8].bulletLen = 1.0
GunsProfiles.gunProfile[8].bulletLenExpand = 10.0
GunsProfiles.gunProfile[8].bulletShell = 'particles/weapons/ammo_cartridge_15-23.xml'
GunsProfiles.gunProfile[8].bulletShot = []
GunsProfiles.gunProfile[8].bulletShot.insert(0, None)
GunsProfiles.gunProfile[8].bulletShot[0] = 'particles/weapons/gun_flash_cannon_high_spec.xml'
GunsProfiles.gunProfile[8].bulletShot.insert(1, None)
GunsProfiles.gunProfile[8].bulletShot[1] = 'particles/weapons/gun_flash_cannon_high_spec_add.xml'
GunsProfiles.gunProfile[8].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[8].bulletThinkness = 0.07
GunsProfiles.gunProfile[8].clientSkipBulletCount = 1
GunsProfiles.gunProfile[8].explosionParticles = Dummy()
GunsProfiles.gunProfile[8].explosionParticles.aircraft = 'EFFECT_BULLET_20MM_30MM_HIT'
GunsProfiles.gunProfile[8].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[8].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[8].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[8].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[8].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[8].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[8].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[8].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[8].name = 'cannon_high_spec'.lower()
GunsProfiles.gunProfile[8].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[8].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[8].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[8].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[8].shellOutInterval = 0.0
GunsProfiles.gunProfile[8].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[8].smokeSizeX = 2.0
GunsProfiles.gunProfile[8].smokeSizeY = 0.06
GunsProfiles.gunProfile[8].smokeTillingLength = 0.6
GunsProfiles.gunProfile[8].sounds = Dummy()
GunsProfiles.gunProfile[8].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[8].sounds.weaponSoundID = 'weapon_cannon_high'
GunsProfiles.gunProfile[8].textureIndex = 0
GunsProfiles.gunProfile[8].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(9, None)
GunsProfiles.gunProfile[9] = Dummy()
GunsProfiles.gunProfile[9].asyncDelay = 0.2
GunsProfiles.gunProfile[9].bulletLen = 1.0
GunsProfiles.gunProfile[9].bulletLenExpand = 10.0
GunsProfiles.gunProfile[9].bulletShell = 'particles/weapons/ammo_cartridge_15-23.xml'
GunsProfiles.gunProfile[9].bulletShot = []
GunsProfiles.gunProfile[9].bulletShot.insert(0, None)
GunsProfiles.gunProfile[9].bulletShot[0] = 'particles/weapons/gun_flash_cannon_high.xml'
GunsProfiles.gunProfile[9].bulletShot.insert(1, None)
GunsProfiles.gunProfile[9].bulletShot[1] = 'particles/weapons/gun_flash_cannon_high_add.xml'
GunsProfiles.gunProfile[9].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[9].bulletThinkness = 0.07
GunsProfiles.gunProfile[9].clientSkipBulletCount = 1
GunsProfiles.gunProfile[9].explosionParticles = Dummy()
GunsProfiles.gunProfile[9].explosionParticles.aircraft = 'EFFECT_BULLET_20MM_30MM_HIT'
GunsProfiles.gunProfile[9].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[9].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[9].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[9].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[9].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[9].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[9].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[9].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[9].name = 'cannon_high_vulcan'.lower()
GunsProfiles.gunProfile[9].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[9].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[9].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[9].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[9].shellOutInterval = 0.0
GunsProfiles.gunProfile[9].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[9].smokeSizeX = 2.0
GunsProfiles.gunProfile[9].smokeSizeY = 0.06
GunsProfiles.gunProfile[9].smokeTillingLength = 0.6
GunsProfiles.gunProfile[9].sounds = Dummy()
GunsProfiles.gunProfile[9].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[9].sounds.weaponSoundID = 'weapon_vulcan'
GunsProfiles.gunProfile[9].textureIndex = 0
GunsProfiles.gunProfile[9].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(10, None)
GunsProfiles.gunProfile[10] = Dummy()
GunsProfiles.gunProfile[10].asyncDelay = 0.1
GunsProfiles.gunProfile[10].bulletLen = 2.0
GunsProfiles.gunProfile[10].bulletLenExpand = 17.0
GunsProfiles.gunProfile[10].bulletShell = 'particles/spaces_fx/empty_particle.xml'
GunsProfiles.gunProfile[10].bulletShot = []
GunsProfiles.gunProfile[10].bulletShot.insert(0, None)
GunsProfiles.gunProfile[10].bulletShot[0] = 'particles/weapons/gun_flash_heavycannon.xml'
GunsProfiles.gunProfile[10].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[10].bulletThinkness = 0.1
GunsProfiles.gunProfile[10].clientSkipBulletCount = 1
GunsProfiles.gunProfile[10].explosionParticles = Dummy()
GunsProfiles.gunProfile[10].explosionParticles.aircraft = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[10].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[10].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[10].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH_27-37'
GunsProfiles.gunProfile[10].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[10].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[10].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER_27-37'
GunsProfiles.gunProfile[10].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[10].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[10].name = 'heavycannon_alpha'.lower()
GunsProfiles.gunProfile[10].receive_damage_other_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[10].receive_damage_other_2 = 'EFFECT_BULLET_37MM_50MM_HIT '
GunsProfiles.gunProfile[10].receive_damage_own_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[10].receive_damage_own_2 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[10].shellOutInterval = 0.0
GunsProfiles.gunProfile[10].smokeRadiusScale = 1.8
GunsProfiles.gunProfile[10].smokeSizeX = 2.0
GunsProfiles.gunProfile[10].smokeSizeY = 0.07
GunsProfiles.gunProfile[10].smokeTillingLength = 0.6
GunsProfiles.gunProfile[10].sounds = Dummy()
GunsProfiles.gunProfile[10].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[10].sounds.weaponSoundID = 'weapon_heavycanon_alpha'
GunsProfiles.gunProfile[10].textureIndex = 0
GunsProfiles.gunProfile[10].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(11, None)
GunsProfiles.gunProfile[11] = Dummy()
GunsProfiles.gunProfile[11].asyncDelay = 0.1
GunsProfiles.gunProfile[11].bulletLen = 2.0
GunsProfiles.gunProfile[11].bulletLenExpand = 17.0
GunsProfiles.gunProfile[11].bulletShell = 'particles/spaces_fx/empty_particle.xml'
GunsProfiles.gunProfile[11].bulletShot = []
GunsProfiles.gunProfile[11].bulletShot.insert(0, None)
GunsProfiles.gunProfile[11].bulletShot[0] = 'particles/weapons/gun_flash_granade.xml'
GunsProfiles.gunProfile[11].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[11].bulletThinkness = 0.1
GunsProfiles.gunProfile[11].clientSkipBulletCount = 1
GunsProfiles.gunProfile[11].explosionParticles = Dummy()
GunsProfiles.gunProfile[11].explosionParticles.aircraft = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[11].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[11].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[11].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH_27-37'
GunsProfiles.gunProfile[11].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[11].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[11].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER_27-37'
GunsProfiles.gunProfile[11].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[11].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[11].name = 'heavycannon_granade'.lower()
GunsProfiles.gunProfile[11].receive_damage_other_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[11].receive_damage_other_2 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[11].receive_damage_own_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[11].receive_damage_own_2 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[11].shellOutInterval = 0.0
GunsProfiles.gunProfile[11].smokeRadiusScale = 1.8
GunsProfiles.gunProfile[11].smokeSizeX = 2.0
GunsProfiles.gunProfile[11].smokeSizeY = 0.07
GunsProfiles.gunProfile[11].smokeTillingLength = 0.6
GunsProfiles.gunProfile[11].sounds = Dummy()
GunsProfiles.gunProfile[11].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[11].sounds.weaponSoundID = 'weapon_heavycanon_granade'
GunsProfiles.gunProfile[11].textureIndex = 0
GunsProfiles.gunProfile[11].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(12, None)
GunsProfiles.gunProfile[12] = Dummy()
GunsProfiles.gunProfile[12].asyncDelay = 0.1
GunsProfiles.gunProfile[12].bulletLen = 2.0
GunsProfiles.gunProfile[12].bulletLenExpand = 17.0
GunsProfiles.gunProfile[12].bulletShell = 'particles/spaces_fx/empty_particle.xml'
GunsProfiles.gunProfile[12].bulletShot = []
GunsProfiles.gunProfile[12].bulletShot.insert(0, None)
GunsProfiles.gunProfile[12].bulletShot[0] = 'particles/weapons/gun_flash_granade_spec.xml'
GunsProfiles.gunProfile[12].bulletShot.insert(1, None)
GunsProfiles.gunProfile[12].bulletShot[1] = 'particles/weapons/gun_flash_granade_spec_add.xml'
GunsProfiles.gunProfile[12].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[12].bulletThinkness = 0.1
GunsProfiles.gunProfile[12].clientSkipBulletCount = 1
GunsProfiles.gunProfile[12].explosionParticles = Dummy()
GunsProfiles.gunProfile[12].explosionParticles.aircraft = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[12].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[12].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[12].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH_27-37'
GunsProfiles.gunProfile[12].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[12].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[12].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER_27-37'
GunsProfiles.gunProfile[12].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[12].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[12].name = 'heavycannon_granade_spec'.lower()
GunsProfiles.gunProfile[12].receive_damage_other_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[12].receive_damage_other_2 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[12].receive_damage_own_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[12].receive_damage_own_2 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[12].shellOutInterval = 0.0
GunsProfiles.gunProfile[12].smokeRadiusScale = 1.8
GunsProfiles.gunProfile[12].smokeSizeX = 2.0
GunsProfiles.gunProfile[12].smokeSizeY = 0.07
GunsProfiles.gunProfile[12].smokeTillingLength = 0.6
GunsProfiles.gunProfile[12].sounds = Dummy()
GunsProfiles.gunProfile[12].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[12].sounds.weaponSoundID = 'weapon_heavycanon_granade'
GunsProfiles.gunProfile[12].textureIndex = 0
GunsProfiles.gunProfile[12].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(13, None)
GunsProfiles.gunProfile[13] = Dummy()
GunsProfiles.gunProfile[13].asyncDelay = 0.1
GunsProfiles.gunProfile[13].bulletLen = 2.0
GunsProfiles.gunProfile[13].bulletLenExpand = 17.0
GunsProfiles.gunProfile[13].bulletShell = 'particles/spaces_fx/empty_particle.xml'
GunsProfiles.gunProfile[13].bulletShot = []
GunsProfiles.gunProfile[13].bulletShot.insert(0, None)
GunsProfiles.gunProfile[13].bulletShot[0] = 'particles/weapons/gun_flash_granade_high.xml'
GunsProfiles.gunProfile[13].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[13].bulletThinkness = 0.1
GunsProfiles.gunProfile[13].clientSkipBulletCount = 1
GunsProfiles.gunProfile[13].explosionParticles = Dummy()
GunsProfiles.gunProfile[13].explosionParticles.aircraft = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[13].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[13].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[13].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH_27-37'
GunsProfiles.gunProfile[13].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[13].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[13].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER_27-37'
GunsProfiles.gunProfile[13].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[13].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[13].name = 'heavycannon_granade_high'.lower()
GunsProfiles.gunProfile[13].receive_damage_other_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[13].receive_damage_other_2 = 'EFFECT_BULLET_37MM_50MM_HIT  '
GunsProfiles.gunProfile[13].receive_damage_own_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[13].receive_damage_own_2 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[13].shellOutInterval = 0.0
GunsProfiles.gunProfile[13].smokeRadiusScale = 1.8
GunsProfiles.gunProfile[13].smokeSizeX = 2.0
GunsProfiles.gunProfile[13].smokeSizeY = 0.07
GunsProfiles.gunProfile[13].smokeTillingLength = 0.6
GunsProfiles.gunProfile[13].sounds = Dummy()
GunsProfiles.gunProfile[13].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[13].sounds.weaponSoundID = 'weapon_heavycanon_granade_high'
GunsProfiles.gunProfile[13].textureIndex = 0
GunsProfiles.gunProfile[13].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(14, None)
GunsProfiles.gunProfile[14] = Dummy()
GunsProfiles.gunProfile[14].asyncDelay = 0.1
GunsProfiles.gunProfile[14].bulletLen = 2.0
GunsProfiles.gunProfile[14].bulletLenExpand = 17.0
GunsProfiles.gunProfile[14].bulletShell = 'particles/spaces_fx/empty_particle.xml'
GunsProfiles.gunProfile[14].bulletShot = []
GunsProfiles.gunProfile[14].bulletShot.insert(0, None)
GunsProfiles.gunProfile[14].bulletShot[0] = 'particles/weapons/gun_flash_granade_high_spec.xml'
GunsProfiles.gunProfile[14].bulletShot.insert(1, None)
GunsProfiles.gunProfile[14].bulletShot[1] = 'particles/weapons/gun_flash_granade_high_spec_add.xml'
GunsProfiles.gunProfile[14].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[14].bulletThinkness = 0.1
GunsProfiles.gunProfile[14].clientSkipBulletCount = 1
GunsProfiles.gunProfile[14].explosionParticles = Dummy()
GunsProfiles.gunProfile[14].explosionParticles.aircraft = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[14].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[14].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[14].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH_27-37'
GunsProfiles.gunProfile[14].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[14].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT_27-37'
GunsProfiles.gunProfile[14].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER_27-37'
GunsProfiles.gunProfile[14].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[14].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[14].name = 'heavycannon_granade_high_spec'.lower()
GunsProfiles.gunProfile[14].receive_damage_other_1 = 'EFFECT_BULLET_37MM_50MM_HIT  '
GunsProfiles.gunProfile[14].receive_damage_other_2 = 'EFFECT_BULLET_37MM_50MM_HIT  '
GunsProfiles.gunProfile[14].receive_damage_own_1 = 'EFFECT_BULLET_37MM_50MM_HIT'
GunsProfiles.gunProfile[14].receive_damage_own_2 = 'EFFECT_BULLET_37MM_50MM_HIT  '
GunsProfiles.gunProfile[14].shellOutInterval = 0.0
GunsProfiles.gunProfile[14].smokeRadiusScale = 1.8
GunsProfiles.gunProfile[14].smokeSizeX = 2.0
GunsProfiles.gunProfile[14].smokeSizeY = 0.07
GunsProfiles.gunProfile[14].smokeTillingLength = 0.6
GunsProfiles.gunProfile[14].sounds = Dummy()
GunsProfiles.gunProfile[14].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[14].sounds.weaponSoundID = 'weapon_heavycanon_granade_high'
GunsProfiles.gunProfile[14].textureIndex = 0
GunsProfiles.gunProfile[14].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(15, None)
GunsProfiles.gunProfile[15] = Dummy()
GunsProfiles.gunProfile[15].asyncDelay = 0.2
GunsProfiles.gunProfile[15].bulletLen = 2.0
GunsProfiles.gunProfile[15].bulletLenExpand = 2.0
GunsProfiles.gunProfile[15].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[15].bulletShot = []
GunsProfiles.gunProfile[15].bulletShot.insert(0, None)
GunsProfiles.gunProfile[15].bulletShot[0] = 'particles/weapons/gun_flash_aa.xml'
GunsProfiles.gunProfile[15].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[15].bulletThinkness = 0.08
GunsProfiles.gunProfile[15].clientSkipBulletCount = 1
GunsProfiles.gunProfile[15].explosionParticles = Dummy()
GunsProfiles.gunProfile[15].explosionParticles.air = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[15].explosionParticles.baseobject = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[15].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[15].explosionParticles.ground = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[15].explosionParticles.tree = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[15].explosionParticles.turret = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[15].explosionParticles.water = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[15].hudIcoPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[15].iconEmptyPath = 'icons/weapons/iconWeapGunRunOut.tga'
GunsProfiles.gunProfile[15].name = 'gun_AA'.lower()
GunsProfiles.gunProfile[15].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[15].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[15].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[15].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[15].shellOutInterval = 0.0
GunsProfiles.gunProfile[15].smokeRadiusScale = 0.4
GunsProfiles.gunProfile[15].smokeSizeX = 2.0
GunsProfiles.gunProfile[15].smokeSizeY = 0.04
GunsProfiles.gunProfile[15].smokeTillingLength = 0.3
GunsProfiles.gunProfile[15].sounds = Dummy()
GunsProfiles.gunProfile[15].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[15].sounds.weaponSoundID = 'weapon_7_AA'
GunsProfiles.gunProfile[15].textureIndex = 0
GunsProfiles.gunProfile[15].ttxIcoPath = 'icons/characteristics/iconCharMachineGun.png'
GunsProfiles.gunProfile.insert(16, None)
GunsProfiles.gunProfile[16] = Dummy()
GunsProfiles.gunProfile[16].asyncDelay = 0.2
GunsProfiles.gunProfile[16].bulletLen = 2.0
GunsProfiles.gunProfile[16].bulletLenExpand = 3.0
GunsProfiles.gunProfile[16].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[16].bulletShot = []
GunsProfiles.gunProfile[16].bulletShot.insert(0, None)
GunsProfiles.gunProfile[16].bulletShot[0] = 'particles/weapons/gun_flash_aa.xml'
GunsProfiles.gunProfile[16].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[16].bulletThinkness = 0.12
GunsProfiles.gunProfile[16].clientSkipBulletCount = 1
GunsProfiles.gunProfile[16].explosionParticles = Dummy()
GunsProfiles.gunProfile[16].explosionParticles.air = 'EFFECT_AA_EXPLOSION'
GunsProfiles.gunProfile[16].explosionParticles.baseobject = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[16].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[16].explosionParticles.ground = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[16].explosionParticles.tree = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[16].explosionParticles.turret = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[16].explosionParticles.water = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[16].hudIcoPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[16].iconEmptyPath = 'icons/weapons/iconWeapGunRunOut.tga'
GunsProfiles.gunProfile[16].name = 'cannon_AA'.lower()
GunsProfiles.gunProfile[16].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[16].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[16].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[16].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[16].shellOutInterval = 0.0
GunsProfiles.gunProfile[16].smokeRadiusScale = 1.8
GunsProfiles.gunProfile[16].smokeSizeX = 2.0
GunsProfiles.gunProfile[16].smokeSizeY = 0.07
GunsProfiles.gunProfile[16].smokeTillingLength = 0.6
GunsProfiles.gunProfile[16].sounds = Dummy()
GunsProfiles.gunProfile[16].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[16].sounds.weaponSoundID = 'weapon_12_AA'
GunsProfiles.gunProfile[16].textureIndex = 0
GunsProfiles.gunProfile[16].ttxIcoPath = 'icons/characteristics/iconCharMachineGun.png'
GunsProfiles.gunProfile.insert(17, None)
GunsProfiles.gunProfile[17] = Dummy()
GunsProfiles.gunProfile[17].asyncDelay = 0.2
GunsProfiles.gunProfile[17].bulletLen = 1.5
GunsProfiles.gunProfile[17].bulletLenExpand = 1.5
GunsProfiles.gunProfile[17].bulletShell = 'particles/weapons/ammo_cartridge_25-32.xml'
GunsProfiles.gunProfile[17].bulletShot = []
GunsProfiles.gunProfile[17].bulletShot.insert(0, None)
GunsProfiles.gunProfile[17].bulletShot[0] = 'particles/weapons/gun_flash_30.xml'
GunsProfiles.gunProfile[17].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[17].bulletThinkness = 0.1
GunsProfiles.gunProfile[17].clientSkipBulletCount = 1
GunsProfiles.gunProfile[17].explosionParticles = Dummy()
GunsProfiles.gunProfile[17].explosionParticles.air = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[17].explosionParticles.baseobject = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[17].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[17].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[17].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[17].explosionParticles.turret = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[17].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[17].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[17].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[17].name = 'turret_gun'.lower()
GunsProfiles.gunProfile[17].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[17].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[17].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[17].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[17].shellOutInterval = 0.0
GunsProfiles.gunProfile[17].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[17].smokeSizeX = 2.0
GunsProfiles.gunProfile[17].smokeSizeY = 0.06
GunsProfiles.gunProfile[17].smokeTillingLength = 0.6
GunsProfiles.gunProfile[17].sounds = Dummy()
GunsProfiles.gunProfile[17].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[17].sounds.weaponSoundID = 'weapon_machinegun_small_TL'
GunsProfiles.gunProfile[17].textureIndex = 0
GunsProfiles.gunProfile[17].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(18, None)
GunsProfiles.gunProfile[18] = Dummy()
GunsProfiles.gunProfile[18].asyncDelay = 0.2
GunsProfiles.gunProfile[18].bulletLen = 0.4
GunsProfiles.gunProfile[18].bulletLenExpand = 4.0
GunsProfiles.gunProfile[18].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[18].bulletShot = []
GunsProfiles.gunProfile[18].bulletShot.insert(0, None)
GunsProfiles.gunProfile[18].bulletShot[0] = 'particles/weapons/gun_flash_rear_mg_long.xml'
GunsProfiles.gunProfile[18].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[18].bulletThinkness = 0.03
GunsProfiles.gunProfile[18].clientSkipBulletCount = 1
GunsProfiles.gunProfile[18].explosionParticles = Dummy()
GunsProfiles.gunProfile[18].explosionParticles.aircraft = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[18].explosionParticles.baseobject = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[18].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[18].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[18].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[18].explosionParticles.turret = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[18].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[18].hudIcoPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[18].iconEmptyPath = 'icons/weapons/iconWeapGunRunOut.tga'
GunsProfiles.gunProfile[18].name = 'turret_machinegun_long'.lower()
GunsProfiles.gunProfile[18].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[18].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[18].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[18].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[18].shellOutInterval = 0.0
GunsProfiles.gunProfile[18].smokeRadiusScale = 0.5
GunsProfiles.gunProfile[18].smokeSizeX = 2.0
GunsProfiles.gunProfile[18].smokeSizeY = 0.035
GunsProfiles.gunProfile[18].smokeTillingLength = 0.35
GunsProfiles.gunProfile[18].sounds = Dummy()
GunsProfiles.gunProfile[18].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[18].sounds.weaponSoundID = 'weapon_machinegun_small_TL'
GunsProfiles.gunProfile[18].textureIndex = 1
GunsProfiles.gunProfile[18].ttxIcoPath = 'icons/characteristics/iconCharMachineGun.png'
GunsProfiles.gunProfile.insert(19, None)
GunsProfiles.gunProfile[19] = Dummy()
GunsProfiles.gunProfile[19].asyncDelay = 0.2
GunsProfiles.gunProfile[19].bulletLen = 1.0
GunsProfiles.gunProfile[19].bulletLenExpand = 10.0
GunsProfiles.gunProfile[19].bulletShell = 'particles/weapons/ammo_cartridge_15-23.xml'
GunsProfiles.gunProfile[19].bulletShot = []
GunsProfiles.gunProfile[19].bulletShot.insert(0, None)
GunsProfiles.gunProfile[19].bulletShot[0] = 'particles/weapons/gun_flash_rear_cannon_long.xml'
GunsProfiles.gunProfile[19].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[19].bulletThinkness = 0.07
GunsProfiles.gunProfile[19].clientSkipBulletCount = 1
GunsProfiles.gunProfile[19].explosionParticles = Dummy()
GunsProfiles.gunProfile[19].explosionParticles.aircraft = 'EFFECT_BULLET_20MM_30MM_HIT'
GunsProfiles.gunProfile[19].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[19].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[19].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[19].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[19].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[19].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[19].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[19].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[19].name = 'turret_cannon_long'.lower()
GunsProfiles.gunProfile[19].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[19].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[19].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[19].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[19].shellOutInterval = 0.0
GunsProfiles.gunProfile[19].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[19].smokeSizeX = 2.0
GunsProfiles.gunProfile[19].smokeSizeY = 0.06
GunsProfiles.gunProfile[19].smokeTillingLength = 0.6
GunsProfiles.gunProfile[19].sounds = Dummy()
GunsProfiles.gunProfile[19].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[19].sounds.weaponSoundID = 'weapon_cannon_high_TL'
GunsProfiles.gunProfile[19].textureIndex = 0
GunsProfiles.gunProfile[19].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(20, None)
GunsProfiles.gunProfile[20] = Dummy()
GunsProfiles.gunProfile[20].asyncDelay = 0.2
GunsProfiles.gunProfile[20].bulletLen = 0.4
GunsProfiles.gunProfile[20].bulletLenExpand = 4.0
GunsProfiles.gunProfile[20].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[20].bulletShot = []
GunsProfiles.gunProfile[20].bulletShot.insert(0, None)
GunsProfiles.gunProfile[20].bulletShot[0] = 'particles/weapons/gun_flash_mg.xml'
GunsProfiles.gunProfile[20].bulletShot.insert(1, None)
GunsProfiles.gunProfile[20].bulletShot[1] = 'particles/weapons/gun_flash_mg_add.xml'
GunsProfiles.gunProfile[20].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[20].bulletThinkness = 0.03
GunsProfiles.gunProfile[20].clientSkipBulletCount = 1
GunsProfiles.gunProfile[20].explosionParticles = Dummy()
GunsProfiles.gunProfile[20].explosionParticles.aircraft = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[20].explosionParticles.baseobject = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[20].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[20].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[20].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[20].explosionParticles.turret = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[20].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[20].hudIcoPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[20].iconEmptyPath = 'icons/weapons/iconWeapGunRunOut.tga'
GunsProfiles.gunProfile[20].name = 'turret_machinegun_small'.lower()
GunsProfiles.gunProfile[20].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[20].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[20].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[20].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[20].shellOutInterval = 0.0
GunsProfiles.gunProfile[20].smokeRadiusScale = 0.5
GunsProfiles.gunProfile[20].smokeSizeX = 2.0
GunsProfiles.gunProfile[20].smokeSizeY = 0.035
GunsProfiles.gunProfile[20].smokeTillingLength = 0.35
GunsProfiles.gunProfile[20].sounds = Dummy()
GunsProfiles.gunProfile[20].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[20].sounds.weaponSoundID = 'weapon_machinegun_small_TL'
GunsProfiles.gunProfile[20].textureIndex = 1
GunsProfiles.gunProfile[20].ttxIcoPath = 'icons/characteristics/iconCharMachineGun.png'
GunsProfiles.gunProfile.insert(21, None)
GunsProfiles.gunProfile[21] = Dummy()
GunsProfiles.gunProfile[21].asyncDelay = 0.2
GunsProfiles.gunProfile[21].bulletLen = 0.7
GunsProfiles.gunProfile[21].bulletLenExpand = 5.0
GunsProfiles.gunProfile[21].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[21].bulletShot = []
GunsProfiles.gunProfile[21].bulletShot.insert(0, None)
GunsProfiles.gunProfile[21].bulletShot[0] = 'particles/weapons/gun_flash_mg_heavy.xml'
GunsProfiles.gunProfile[21].bulletShot.insert(1, None)
GunsProfiles.gunProfile[21].bulletShot[1] = 'particles/weapons/gun_flash_mg_heavy_add.xml'
GunsProfiles.gunProfile[21].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[21].bulletThinkness = 0.05
GunsProfiles.gunProfile[21].clientSkipBulletCount = 3
GunsProfiles.gunProfile[21].explosionParticles = Dummy()
GunsProfiles.gunProfile[21].explosionParticles.aircraft = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[21].explosionParticles.baseobject = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[21].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[21].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[21].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[21].explosionParticles.turret = 'EFFECT_BULLET_HIT_OBJECT'
GunsProfiles.gunProfile[21].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[21].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[21].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[21].name = 'turret_machinegun_heavy'.lower()
GunsProfiles.gunProfile[21].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[21].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[21].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[21].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[21].shellOutInterval = 0.0
GunsProfiles.gunProfile[21].smokeRadiusScale = 0.5
GunsProfiles.gunProfile[21].smokeSizeX = 2.0
GunsProfiles.gunProfile[21].smokeSizeY = 0.035
GunsProfiles.gunProfile[21].smokeTillingLength = 0.35
GunsProfiles.gunProfile[21].sounds = Dummy()
GunsProfiles.gunProfile[21].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[21].sounds.weaponSoundID = 'weapon_machinegun_heavy_TL'
GunsProfiles.gunProfile[21].textureIndex = 1
GunsProfiles.gunProfile[21].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(22, None)
GunsProfiles.gunProfile[22] = Dummy()
GunsProfiles.gunProfile[22].asyncDelay = 0.2
GunsProfiles.gunProfile[22].bulletLen = 1.0
GunsProfiles.gunProfile[22].bulletLenExpand = 10.0
GunsProfiles.gunProfile[22].bulletShell = 'particles/weapons/ammo_cartridge_15-23.xml'
GunsProfiles.gunProfile[22].bulletShot = []
GunsProfiles.gunProfile[22].bulletShot.insert(0, None)
GunsProfiles.gunProfile[22].bulletShot[0] = 'particles/weapons/gun_flash_cannon.xml'
GunsProfiles.gunProfile[22].bulletShot.insert(1, None)
GunsProfiles.gunProfile[22].bulletShot[1] = 'particles/weapons/gun_flash_cannon_add.xml'
GunsProfiles.gunProfile[22].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[22].bulletThinkness = 0.07
GunsProfiles.gunProfile[22].clientSkipBulletCount = 1
GunsProfiles.gunProfile[22].explosionParticles = Dummy()
GunsProfiles.gunProfile[22].explosionParticles.aircraft = 'EFFECT_BULLET_20MM_30MM_HIT'
GunsProfiles.gunProfile[22].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[22].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[22].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[22].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[22].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[22].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[22].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[22].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[22].name = 'turret_cannon_main'.lower()
GunsProfiles.gunProfile[22].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[22].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[22].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[22].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[22].shellOutInterval = 0.0
GunsProfiles.gunProfile[22].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[22].smokeSizeX = 2.0
GunsProfiles.gunProfile[22].smokeSizeY = 0.06
GunsProfiles.gunProfile[22].smokeTillingLength = 0.6
GunsProfiles.gunProfile[22].sounds = Dummy()
GunsProfiles.gunProfile[22].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[22].sounds.weaponSoundID = 'weapon_cannon_main_TL'
GunsProfiles.gunProfile[22].textureIndex = 0
GunsProfiles.gunProfile[22].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(23, None)
GunsProfiles.gunProfile[23] = Dummy()
GunsProfiles.gunProfile[23].asyncDelay = 0.2
GunsProfiles.gunProfile[23].bulletLen = 1.0
GunsProfiles.gunProfile[23].bulletLenExpand = 10.0
GunsProfiles.gunProfile[23].bulletShell = 'particles/weapons/ammo_cartridge_15-23.xml'
GunsProfiles.gunProfile[23].bulletShot = []
GunsProfiles.gunProfile[23].bulletShot.insert(0, None)
GunsProfiles.gunProfile[23].bulletShot[0] = 'particles/weapons/gun_flash_cannon_high.xml'
GunsProfiles.gunProfile[23].bulletShot.insert(1, None)
GunsProfiles.gunProfile[23].bulletShot[1] = 'particles/weapons/gun_flash_cannon_high_add.xml'
GunsProfiles.gunProfile[23].bulletThicknessExpand = 0.02
GunsProfiles.gunProfile[23].bulletThinkness = 0.07
GunsProfiles.gunProfile[23].clientSkipBulletCount = 1
GunsProfiles.gunProfile[23].explosionParticles = Dummy()
GunsProfiles.gunProfile[23].explosionParticles.aircraft = 'EFFECT_BULLET_20MM_30MM_HIT'
GunsProfiles.gunProfile[23].explosionParticles.baseobject = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[23].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[23].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[23].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[23].explosionParticles.turret = 'EFFECT_SHELL_HIT_OBJECT'
GunsProfiles.gunProfile[23].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[23].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[23].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[23].name = 'turret_cannon_high'.lower()
GunsProfiles.gunProfile[23].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[23].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[23].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[23].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[23].shellOutInterval = 0.0
GunsProfiles.gunProfile[23].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[23].smokeSizeX = 2.0
GunsProfiles.gunProfile[23].smokeSizeY = 0.06
GunsProfiles.gunProfile[23].smokeTillingLength = 0.6
GunsProfiles.gunProfile[23].sounds = Dummy()
GunsProfiles.gunProfile[23].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[23].sounds.weaponSoundID = 'weapon_cannon_high_TL'
GunsProfiles.gunProfile[23].textureIndex = 0
GunsProfiles.gunProfile[23].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(24, None)
GunsProfiles.gunProfile[24] = Dummy()
GunsProfiles.gunProfile[24].asyncDelay = 0.2
GunsProfiles.gunProfile[24].bulletLen = 1.5
GunsProfiles.gunProfile[24].bulletLenExpand = 1.5
GunsProfiles.gunProfile[24].bulletShell = 'particles/weapons/ammo_cartridge_25-32.xml'
GunsProfiles.gunProfile[24].bulletShot = []
GunsProfiles.gunProfile[24].bulletShot.insert(0, None)
GunsProfiles.gunProfile[24].bulletShot[0] = 'particles/weapons/gun_flash_30.xml'
GunsProfiles.gunProfile[24].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[24].bulletThinkness = 0.1
GunsProfiles.gunProfile[24].clientSkipBulletCount = 1
GunsProfiles.gunProfile[24].explosionParticles = Dummy()
GunsProfiles.gunProfile[24].explosionParticles.air = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[24].explosionParticles.baseobject = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[24].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[24].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[24].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[24].explosionParticles.turret = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[24].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[24].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[24].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[24].name = 'turret_gun'.lower()
GunsProfiles.gunProfile[24].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[24].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[24].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[24].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[24].shellOutInterval = 0.0
GunsProfiles.gunProfile[24].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[24].smokeSizeX = 2.0
GunsProfiles.gunProfile[24].smokeSizeY = 0.06
GunsProfiles.gunProfile[24].smokeTillingLength = 0.6
GunsProfiles.gunProfile[24].sounds = Dummy()
GunsProfiles.gunProfile[24].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[24].sounds.weaponSoundID = 'weapon_machinegun_small_TL'
GunsProfiles.gunProfile[24].textureIndex = 0
GunsProfiles.gunProfile[24].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(25, None)
GunsProfiles.gunProfile[25] = Dummy()
GunsProfiles.gunProfile[25].asyncDelay = 0.2
GunsProfiles.gunProfile[25].bulletLen = 2.0
GunsProfiles.gunProfile[25].bulletLenExpand = 3.0
GunsProfiles.gunProfile[25].bulletShell = 'particles/weapons/ammo_cartridge_25-32.xml'
GunsProfiles.gunProfile[25].bulletShot = []
GunsProfiles.gunProfile[25].bulletShot.insert(0, None)
GunsProfiles.gunProfile[25].bulletShot[0] = 'particles/weapons/gun_flash_30.xml'
GunsProfiles.gunProfile[25].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[25].bulletThinkness = 0.2
GunsProfiles.gunProfile[25].clientSkipBulletCount = 1
GunsProfiles.gunProfile[25].explosionParticles = Dummy()
GunsProfiles.gunProfile[25].explosionParticles.air = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[25].explosionParticles.baseobject = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[25].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[25].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[25].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[25].explosionParticles.turret = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[25].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[25].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[25].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[25].name = 'turret_cannon'.lower()
GunsProfiles.gunProfile[25].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[25].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[25].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[25].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[25].shellOutInterval = 0.0
GunsProfiles.gunProfile[25].smokeRadiusScale = 0.9
GunsProfiles.gunProfile[25].smokeSizeX = 2.0
GunsProfiles.gunProfile[25].smokeSizeY = 0.06
GunsProfiles.gunProfile[25].smokeTillingLength = 0.6
GunsProfiles.gunProfile[25].sounds = Dummy()
GunsProfiles.gunProfile[25].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar_Big_Caliber'
GunsProfiles.gunProfile[25].sounds.weaponSoundID = 'weapon_cannon_main_TL'
GunsProfiles.gunProfile[25].textureIndex = 0
GunsProfiles.gunProfile[25].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(26, None)
GunsProfiles.gunProfile[26] = Dummy()
GunsProfiles.gunProfile[26].asyncDelay = 0.2
GunsProfiles.gunProfile[26].bulletLen = 2.0
GunsProfiles.gunProfile[26].bulletLenExpand = 3.0
GunsProfiles.gunProfile[26].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[26].bulletShot = []
GunsProfiles.gunProfile[26].bulletShot.insert(0, None)
GunsProfiles.gunProfile[26].bulletShot[0] = 'particles/weapons/gun_flash_aa.xml'
GunsProfiles.gunProfile[26].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[26].bulletThinkness = 0.2
GunsProfiles.gunProfile[26].clientSkipBulletCount = 1
GunsProfiles.gunProfile[26].explosionParticles = Dummy()
GunsProfiles.gunProfile[26].explosionParticles.air = 'EFFECT_FIREWORKS_AA'
GunsProfiles.gunProfile[26].explosionParticles.baseobject = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[26].explosionParticles.default = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[26].explosionParticles.ground = 'EFFECT_SHELL_EXPLOSION_EARTH'
GunsProfiles.gunProfile[26].explosionParticles.tree = 'EFFECT_SHELL_EXPLOSION_TREE'
GunsProfiles.gunProfile[26].explosionParticles.turret = 'EFFECT_SHELL_HIT'
GunsProfiles.gunProfile[26].explosionParticles.water = 'EFFECT_SHELL_EXPLOSION_WATER'
GunsProfiles.gunProfile[26].hudIcoPath = 'icons/weapons/iconWeapCannon.tga'
GunsProfiles.gunProfile[26].iconEmptyPath = 'icons/weapons/iconWeapCannonRunOut.tga'
GunsProfiles.gunProfile[26].name = 'turret_holiday'.lower()
GunsProfiles.gunProfile[26].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[26].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[26].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[26].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[26].shellOutInterval = 0.0
GunsProfiles.gunProfile[26].smokeRadiusScale = 0.4
GunsProfiles.gunProfile[26].smokeSizeX = 2.0
GunsProfiles.gunProfile[26].smokeSizeY = 0.04
GunsProfiles.gunProfile[26].smokeTillingLength = 0.3
GunsProfiles.gunProfile[26].sounds = Dummy()
GunsProfiles.gunProfile[26].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[26].sounds.weaponSoundID = 'weapon_machinegun_small_TL'
GunsProfiles.gunProfile[26].textureIndex = 0
GunsProfiles.gunProfile[26].ttxIcoPath = 'icons/characteristics/iconCharCannon.png'
GunsProfiles.gunProfile.insert(27, None)
GunsProfiles.gunProfile[27] = Dummy()
GunsProfiles.gunProfile[27].asyncDelay = 0.0
GunsProfiles.gunProfile[27].bulletLen = 2.0
GunsProfiles.gunProfile[27].bulletLenExpand = 2.0
GunsProfiles.gunProfile[27].bulletShell = 'particles/weapons/ammo_cartridge_7-13.xml'
GunsProfiles.gunProfile[27].bulletShot = []
GunsProfiles.gunProfile[27].bulletShot.insert(0, None)
GunsProfiles.gunProfile[27].bulletShot[0] = 'particles/weapons/riechslaser_fire.xml'
GunsProfiles.gunProfile[27].bulletThicknessExpand = 0.01
GunsProfiles.gunProfile[27].bulletThinkness = 0.2
GunsProfiles.gunProfile[27].clientSkipBulletCount = 1
GunsProfiles.gunProfile[27].explosionParticles = Dummy()
GunsProfiles.gunProfile[27].explosionParticles.air = 'EFFECT_BULLET_7MM_17MM_HIT'
GunsProfiles.gunProfile[27].explosionParticles.baseobject = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[27].explosionParticles.default = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[27].explosionParticles.ground = 'EFFECT_BULLET_EXPLOSION_EARTH'
GunsProfiles.gunProfile[27].explosionParticles.tree = 'EFFECT_BULLET_EXPLOSION_TREE'
GunsProfiles.gunProfile[27].explosionParticles.turret = 'EFFECT_BULLET_HIT'
GunsProfiles.gunProfile[27].explosionParticles.water = 'EFFECT_BULLET_EXPLOSION_WATER'
GunsProfiles.gunProfile[27].hudIcoPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[27].iconEmptyPath = 'icons/weapons/iconWeapGun.tga'
GunsProfiles.gunProfile[27].name = 'gun_laser'.lower()
GunsProfiles.gunProfile[27].receive_damage_other_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[27].receive_damage_other_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[27].receive_damage_own_1 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[27].receive_damage_own_2 = 'EFFECT_empty_particle'
GunsProfiles.gunProfile[27].shellOutInterval = 0.0
GunsProfiles.gunProfile[27].smokeRadiusScale = 0.4
GunsProfiles.gunProfile[27].smokeSizeX = 2.0
GunsProfiles.gunProfile[27].smokeSizeY = 0.1
GunsProfiles.gunProfile[27].smokeTillingLength = 0.2
GunsProfiles.gunProfile[27].sounds = Dummy()
GunsProfiles.gunProfile[27].sounds.playerAvatarGotHitEvent = 'Play_hit_LOGIC_Avatar'
GunsProfiles.gunProfile[27].sounds.weaponSoundID = 'weapon_machinegun_small_TL'
GunsProfiles.gunProfile[27].textureIndex = 1
GunsProfiles.gunProfile[27].ttxIcoPath = 'icons/characteristics/iconCharMachineGun.png'