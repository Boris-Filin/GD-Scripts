from gd.api import (
	Editor,
	Object,
)


class EnemyCast():
	def __init__(self, screen):
		self.screen = screen

	def get_rays(self):
		s = self.screen
		objects = []
		x_pos, y_pos = s.camera_world_pos
		num = int(s.depth * s.fov_tan * 2)
		min_group = s.min_group + s.groups_per_slice * s.n
		min_collider = s.min_ray_collider + s.iterations * s.n
		for i in range(num):
			group = min_group + i
			collider_id = min_collider + i
			collider = Object(id=1816, x=x_pos, y=y_pos, item_id=collider_id, groups={2, group},
				dynamic_block=False, editor_layer_1=8, scale=0.5, is_active_trigger=True)
			objects.append(collider)

		return objects

	def get_objects(self):
		objects = self.get_rays()
		return objects