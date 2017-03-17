# Embedded file name: scripts/common/db/DBHangar.py
from db.DBHelpers import readValues, findSection, readValue
import Math, math
import consts

class HangarConfig:

    def __init__(self, data):
        params = (('space_name', ''),
         ('v_scale', 0.0),
         ('v_start_angles', Math.Vector3(0, 0, 0)),
         ('v_start_pos', Math.Vector3(0, 0, 0)),
         ('cam_start_dist', 0.0),
         ('cam_start_angles', Math.Vector2(0, 0)),
         ('cam_start_target_pos', Math.Vector3(0, 0, 0)),
         ('cam_dist_constr', Math.Vector3(0, 0, 0)),
         ('cam_pitch_constr', Math.Vector2(0, 0)),
         ('cam_sens_rotation', 0.0),
         ('cam_zooming_steps', 5.0),
         ('cam_fluency_rotation', 0.0),
         ('cam_fluency_zooming', 0.0),
         ('cam_fluency_movement', 0.0),
         ('cam_fov_constr', Math.Vector3(60, 60, 60)),
         ('cam_fov_interpolation_time', 0.05),
         ('cam_ellipticity', 1.0),
         ('cam_lobby_win_screen_shift_x', 0.0),
         ('cam_lobby_win_screen_shift_interval', 0.0),
         ('emblems_alpha_damaged', 0.0),
         ('emblems_alpha_undamaged', 0.0),
         ('static_rotor', False),
         ('preview_cam_start_dist', 0.0),
         ('preview_cam_start_angles', Math.Vector2(0, 0)),
         ('preview_cam_start_target_pos', Math.Vector3(0, 0, 0)))
        readValues(self, data, params)
        cam_views_section = findSection(data, 'cam_views')
        self.cam_views = {}
        if cam_views_section is not None:
            for _, data in cam_views_section.items():
                cam_view = data.readString('id')
                self.cam_views[cam_view] = HangarCamView(data)

        self.v_scale *= consts.AIRCRAFT_MODEL_SCALING
        self.preview_cam_start_dist *= consts.AIRCRAFT_MODEL_SCALING
        for i in range(0, 3):
            self.v_start_angles[i] = math.radians(self.v_start_angles[i])

        self.cam_fov_constr[0] = math.radians(self.cam_fov_constr[0])
        self.cam_fov_constr[1] = math.radians(self.cam_fov_constr[1])
        self.cam_fov_constr[2] = math.radians(self.cam_fov_constr[2])
        return


class HangarCamView:

    def __init__(self, data):
        params = (('cam_offset', Math.Vector3(0, 0, 0)), ('cam_dist', 0.0), ('cam_fov', 0.0))
        readValues(self, data, params)
        if self.cam_fov < 0 or self.cam_fov >= 180:
            self.cam_fov = 60
        if data.has_key('cam_angles'):
            readValue(self, data, 'cam_angles', Math.Vector2(0, 0))