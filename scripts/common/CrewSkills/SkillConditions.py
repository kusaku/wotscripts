# Embedded file name: scripts/common/CrewSkills/SkillConditions.py
from EnumConditions import EnumConditions

class SkillConditions(EnumConditions):

    def PILOT_S_FIREMANUVER_START(self):
        return self.IS_ON_FIRE and self.ROLL_SPEED_NORM > self.MIN_ROLL_SPEED_NORM and self.PITCH_SPEED_NORM > 0.4 and self.SPEED_NORM > 0.2

    def PILOT_S_FIREMANUVER_END(self):
        return not self.IS_ON_FIRE or self.ROLL_SPEED_NORM < self.MIN_ROLL_SPEED_NORM

    def PILOT_S_CRUISEFLIGHT_START(self):
        return self.TIME_GET_NO_DAMAGE > 20 and self.TIME_LAST_INFLICT_DAMAGE > 20

    def PILOT_S_CRUISEFLIGHT_END(self):
        return self.TIME_GET_NO_DAMAGE < 20 or self.TIME_LAST_INFLICT_DAMAGE < 20

    def PILOT_S_DIEHARD_START(self):
        return self.HEALTH_NORM < 0.3

    def PILOT_S_DIEHARD_END(self):
        return self.HEALTH_NORM > 0.3

    def PILOT_S_BLOODLUST_START(self):
        return self.TIME_LAST_KILL_PLANE < 10

    def PILOT_S_BLOODLUST_END(self):
        return self.WORK_TIME >= 10

    def PILOT_S_BOOMZOOM_START(self):
        return self.SPEED_NORM > 0.6 and self.VERTICAL_ANGLE < -45

    def PILOT_S_BOOMZOOM_END(self):
        return self.VERTICAL_ANGLE > -15

    def PILOT_S_EVASIONMANUVER_START(self):
        return self.ROLL_SPEED_NORM > self.MIN_ROLL_SPEED_NORM and self.PITCH_SPEED_NORM > 0.75 and self.SPEED_NORM > 0.2

    def PILOT_S_EVASIONMANUVER_END(self):
        return self.PITCH_SPEED_NORM < 0.4 and self.WORK_TIME > 2.0

    def PILOT_S_CELESTIAL_FURY_START(self):
        return self.IS_FURY_ACTIVE

    def PILOT_S_CELESTIAL_FURY_END(self):
        return not self.IS_FURY_ACTIVE

    def PILOT_HOT_CHICK_START(self):
        return self.IS_HOT_CHICK_ACTIVE

    def PILOT_HOT_CHICK_END(self):
        return not self.IS_HOT_CHICK_ACTIVE

    def GUNNER_PROTECTOR_START(self):
        return self.TIME_LAST_TURRET_FIRE < 2

    def GUNNER_PROTECTOR_END(self):
        return self.TIME_LAST_TURRET_FIRE > 2