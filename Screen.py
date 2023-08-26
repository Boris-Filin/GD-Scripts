import math

from gd.api import (
	Editor,
	Object,
)

import Defaults
from Strip import Strip
from SliceTriggers import SliceTriggers
from EnemyCast import EnemyCast


class Screen():
	def __init__(self, editor, **kwargs):
		self.__add_properties(Defaults.SCREEN_VALUES)
		self.__add_properties(kwargs)
		self.editor = editor
		self.group_count = self.min_group
		self.strip_groups = []
		self.fov_tan = math.tan(math.radians(self.fov / 2))
		self.camera_world_pos = get_world_coords(self.camera_x, self.camera_y)

		self.iteration_period = self.cycle_duration / self.iterations
		# 4 - WHI and 3 groups per slice, 3 groups per iteration, 2 groups max can be optimized
		self.groups_per_slice = 4 + (self.groups_per_iteration + 1) * self.iterations - min(self.iterations, 2)
	
	def __add_properties(self, properties):
		self.__dict__ = {**self.__dict__, **properties}


	def get_rays(self):
		objects = []
		x_pos, y_pos = get_world_coords(self.camera_x, self.camera_y)
		for i in range(self.n):
			group = self.min_group + self.groups_per_slice * i
			for j in range(self.iterations):
				collider_id = self.min_ray_collider + self.n * j + i
				collider = Object(id=1816, x=x_pos, y=y_pos, item_id=collider_id, groups={2, group+j},
					dynamic_block=False, editor_layer_1=9, scale=0.1, is_active_trigger=True)
				objects.append(collider)

			# collider_1 = Object(id=1816, x=x_pos, y=y_pos, item_id=self.min_ray_collider+i, groups={2, group},
			# 	dynamic_block=False, editor_layer_1=1, scale=0.1, is_active_trigger=True)
			# collider_2 = Object(id=1816, x=x_pos, y=y_pos, item_id=self.min_ray_collider+self.n+i, groups={2, group+1},
			# 	dynamic_block=False, editor_layer_1=1, scale=0.1, is_active_trigger=True)
			# objects.append(collider_1)
			# objects.append(collider_2)
		self.group_count += self.iterations * self.n

		return objects

	def get_strips(self):
		objects = []
		self.strip_groups = []
		for i in range(self.n):
			x, y = get_world_coords(self.x, self.y)
			x += Strip.width * i
			y += Strip.height / 2
			# group = self.min_group + self.groups_per_slice * (i + 1) - Strip.groups_per_strip
			group = self.min_group + self.groups_per_slice * i + self.iterations
			line_group = self.min_group + self.groups_per_slice * self.n + i * len(self.color_variations)
			self.strip_groups.append(group)
			# color = self.min_slice_color
			color = self.min_slice_color + Strip.colors_per_strip * i

			new_strip = Strip((x, y), {self.follow_player_group}, group, line_group, color)
			objects += new_strip.get_objects()
		for obj_ in objects:
			obj_.groups.add(172)
		return objects

	def get_slice_triggers(self):
		objects = []
		for i in range(self.n):
			x, y = get_world_coords(self.trigger_x, self.trigger_y)
			x += 30 * i
			triggers = SliceTriggers(self)
			objects += triggers.get_objects(i, (x, y))
		return objects

	def get_enemy_system(self):
		cast = EnemyCast(self)
		return cast.get_objects()

	def get_objects(self):
		objects = []
		objects += self.get_rays()
		objects += self.get_strips()
		objects += self.get_slice_triggers()
		return objects


def get_world_coords(x, y):
	return 15 + x * 30, 15 + y * 30