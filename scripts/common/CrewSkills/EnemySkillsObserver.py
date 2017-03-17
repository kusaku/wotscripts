# Embedded file name: scripts/common/CrewSkills/EnemySkillsObserver.py
from SkillsHelper import getSkillByID, getTargetSkillIDList, calcNotMainSingleMod
from _consumables_data import ModsTypeEnum
from _skills_data import SpecializationEnum as SE
target_modifiers = {SE.PILOT: [ModsTypeEnum.GUNS_INCFLICT_DAMAGE,
            ModsTypeEnum.GUNS_INFLICT_CRIT,
            ModsTypeEnum.GUNS_INFLICT_FIRE,
            ModsTypeEnum.TEAM_OBJ_GUNS_INFLICT_FIRE],
 SE.GUNNER: []}
mask1 = 1
mask2 = 2
mask3 = 3
mask = 0

class SpecStates:
    s50 = 1
    s75 = 2
    s100 = 3


def get_state_by_value(value):
    if value <= 0:
        return SpecStates.s50
    if value <= 0.5:
        return SpecStates.s75
    return SpecStates.s100


def get_base_skill_value_by_state(state):
    if state == SpecStates.s50:
        return 0
    if state == SpecStates.s75:
        return 0.5
    return 1


target_skills_list = {SE.PILOT: getTargetSkillIDList(target_modifiers[SE.PILOT]),
 SE.GUNNER: getTargetSkillIDList(target_modifiers[SE.GUNNER])}
bits_dict = {SE.PILOT: dict(((k, 2 * i) for i, k in enumerate(target_skills_list[SE.PILOT]))),
 SE.GUNNER: dict(((k, 2 * i) for i, k in enumerate(target_skills_list[SE.GUNNER])))}
state_to_mask = {SpecStates.s50: mask1,
 SpecStates.s75: mask2,
 SpecStates.s100: mask3}
mask_to_state = {mask1: SpecStates.s50,
 mask2: SpecStates.s75,
 mask3: SpecStates.s100}

class EnemySkillObserver(object):

    @staticmethod
    def _pack_active_skills(crew_member, skill_dict):
        send_mask = mask
        for key, bits in bits_dict[crew_member].iteritems():
            send_mask |= state_to_mask.get(skill_dict.get(key, -1), 0) << bits

        return send_mask

    @staticmethod
    def _unpack_active_skills(crew_member, send_mask):
        res = {}
        for key, bits in bits_dict[crew_member].iteritems():
            res[key] = mask_to_state.get(send_mask >> bits & mask3, 0)

        return res

    @staticmethod
    def get_target_skill_mods_activity(owner, crew_member):
        active_skills_dict = {}

        def check_skill_activity(skill_id):
            for crewMember in owner.crew:
                if crewMember.isSkillActive(skill_id):
                    return True

            return False

        def get_base_skill_value(skill_id):
            for crewMember in owner.crew:
                value = crewMember.skillValue(skill_id)
                if value is not None:
                    return value

            return 0

        for skillID in target_skills_list[crew_member]:
            skill_obj = getSkillByID(skillID)
            if skill_obj is not None and check_skill_activity(skill_obj.id):
                active_skills_dict[skill_obj.id] = get_state_by_value(get_base_skill_value(skill_obj.id))

        return EnemySkillObserver._pack_active_skills(crew_member, active_skills_dict)

    @staticmethod
    def get_target_skill_mod_value(crew_member, mods_activity):
        res = {}
        active_skills_dict = EnemySkillObserver._unpack_active_skills(crew_member, mods_activity)
        for skillID, state in active_skills_dict.iteritems():
            skill_obj = getSkillByID(skillID)
            if skill_obj is not None and state:
                for mod in skill_obj.mods:
                    if mod.type in target_modifiers[crew_member]:
                        res[mod.type] = res.setdefault(mod.type, 1) * calcNotMainSingleMod(get_base_skill_value_by_state(state), mod.states[0] - 1, 1)

        return res