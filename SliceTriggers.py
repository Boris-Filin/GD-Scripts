import math


from gd.api import (
	Editor,
	Object,
)
from Strip import Strip


class SliceTriggers():
	def __init__(self, screen):
		self.screen = screen

	def get_objects(self, i, offset):
		group = self.screen.min_group + self.screen.groups_per_slice * i

		colliders = []
		for j in range(self.screen.iterations):
			collider_id = self.screen.min_ray_collider + self.screen.n * j + i
			colliders.append(collider_id)

		self.objects = self.get_triggers(i, group, colliders)
		self.objects += self.get_slice_color_triggers(i, colliders)

		for obj in self.objects:
			obj.is_active_trigger = True
			obj.spawn_triggered = True

		# objects.append(self.get_WHI(group))

		for obj in self.objects:
			obj.x += offset[0]
			obj.y += offset[1]

		return self.objects

	def get_triggers(self, i, group, colliders):
		segment_min_group = group + self.screen.iterations
		pulse_min_group = self.screen.min_group + self.screen.groups_per_slice * self.screen.n + i * len(self.screen.color_variations)
		triggers = [
			# WHI / Corner pulse
			Object(id=1006, x=0, y=300, groups={segment_min_group+3}, multi_trigger=True, target_group_id=segment_min_group,
				hold_time=self.screen.iteration_period+0.01, pulse_mode=1, pulse_type=1, copied_color_id=21),

			# Wall segments follow
			Object(id=1347, x=0, y=1020, groups={1}, multi_trigger=True,
				target_group_id=segment_min_group+1, follow_target_pos_center_id=segment_min_group+3, duration=999, x_mod=0, y_mod=-1),
			Object(id=1347, x=0, y=990, groups={1}, multi_trigger=True,
				target_group_id=segment_min_group+2, follow_target_pos_center_id=segment_min_group+3, duration=999, x_mod=0, y_mod=0.5),
			Object(id=1347, x=0, y=945, groups={1}, multi_trigger=True,
				target_group_id=segment_min_group, follow_target_pos_center_id=segment_min_group+3, duration=999, x_mod=0, y_mod=0.25),

			# Line follow
			Object(id=1347, x=30*self.screen.n+150, y=1020, groups={1}, multi_trigger=True,
				target_group_id=pulse_min_group+1, follow_target_pos_center_id=segment_min_group+3, duration=999, x_mod=0, y_mod=0.075),
			Object(id=1347, x=30*self.screen.n+150, y=990, groups={1}, multi_trigger=True,
				target_group_id=pulse_min_group, follow_target_pos_center_id=segment_min_group+3, duration=999, x_mod=0, y_mod=-0.075)
		]

		if len(self.screen.color_variations) < 2:
			print("huh")
			triggers = triggers[:4]

		for j in range(self.screen.iterations):
			triggers += self.get_slice_iteration(i, j, group, colliders)

		return triggers

	def get_slice_iteration(self, i, j, group, colliders):
		fac = -1 + 2 / (self.screen.n - 1) * i
		fac *= self.screen.fov_tan

		collider_id = colliders[j]
		depth_collider_id = self.screen.depth_colliders[j]
		cycle_group = self.screen.cycle_groups[j]
		cycle_delayed_group = self.screen.cycle_delayed_groups[j]
		cycle_end_group = self.screen.cycle_end_groups[j]
		x_pos = j * (self.screen.n * 30 + 5 * 30)
		forward_group = self.screen.forward_groups[j]
		right_group = self.screen.right_groups[j]

		segment_min_group = group + self.screen.iterations
		min_group = segment_min_group + 4 + j * self.screen.groups_per_iteration - min(j, 2)

		cast_group = min_group
		indicator_group = min_group
		if j == 0:
			cast_group = segment_min_group + 1
		elif j == 1:
			cast_group = segment_min_group + 2
		else:
			indicator_group = min_group + 1

		triggers = [
			# Depth fail colliders
			Object(id=1815, x=x_pos, y=870, groups={1},
				target_group_id=segment_min_group, activate_group=True, item_id=1, block_b_id=collider_id),
			Object(id=1815, x=x_pos, y=840, groups={cycle_group, cast_group}, multi_trigger=True,
				target_group_id=segment_min_group, item_id=depth_collider_id, block_b_id=collider_id),

			# Corner color collider
			Object(id=1815, x=x_pos+10, y=815, groups={1},
				target_group_id=segment_min_group+3, activate_group=True, item_id=5, block_b_id=collider_id),

			# Cycle start move
			Object(id=901, x=x_pos, y=660, groups={cycle_group}, multi_trigger=True, target_group_id=group+j, duration=0,
				follow_target_pos_center_id=self.screen.camera_group, use_target_enabled=True),
			Object(id=901, x=x_pos, y=630, groups={cycle_group}, multi_trigger=True, target_group_id=indicator_group, duration=0,
				follow_target_pos_center_id=self.screen.ground_group, use_target_enabled=True, target_pos_coordinates=2),

			# Ray follow
			Object(id=1347, x=x_pos, y=570, groups={cast_group, cycle_group}, multi_trigger=True, target_group_id=group+j,
				follow_target_pos_center_id=forward_group, duration=self.screen.cycle_duration - 0.05, x_mod=1, y_mod=1),
			Object(id=1347, x=x_pos, y=540, groups={cast_group, cycle_group}, multi_trigger=True, target_group_id=group+j,
				follow_target_pos_center_id=right_group, duration=self.screen.cycle_duration - 0.05, x_mod=fac, y_mod=fac),

			# Indicator move
			Object(id=901, x=x_pos, y=510, groups={cast_group, cycle_delayed_group}, multi_trigger=True,
				target_group_id=indicator_group, move_x=0, move_y=150, duration=self.screen.cycle_duration - 0.1),

			# On ray hit collision
			Object(id=1815, x=x_pos, y=465, groups={1},
				target_group_id=indicator_group, activate_group=True, item_id=1, block_b_id=collider_id),

			# Move WHI to indicator
			Object(id=901, x=x_pos, y=420, groups={cycle_end_group}, multi_trigger=True,
				target_group_id=segment_min_group+3, duration=0,
				follow_target_pos_center_id=indicator_group, use_target_enabled=True, target_pos_coordinates=2),

			# Ray stop triggers / indicators
			Object(id=1616, x=x_pos, y=300, editor_layer_1=1, groups={indicator_group}, multi_trigger=True, target_group_id=cast_group),
		]

		return triggers

	def get_slice_color_triggers(self, i, colliders):
		base_palette = self.screen.base_palette
		color_variations = self.screen.color_variations

		group = self.screen.min_group + self.screen.groups_per_slice * self.screen.n + i * len(color_variations)
		color = self.screen.min_slice_color + Strip.colors_per_strip * i
		y_pos = 300 - 5 * 30
		triggers = []

		for j in range(4):
			triggers.append(Object(
					id=1006, x=0, y=y_pos, groups={123}, multi_trigger=True,
					target_group_id=color+j, hold_time=9999, pulse_mode=1, copied_color_id=base_palette[j]))
			y_pos -= 30

		y_pos -= 30 * 2

		for (j, palette) in enumerate(color_variations):
			collider_id = self.screen.min_texture_collider + j
			for k in range(self.screen.iterations):
				triggers.append(Object(id=1815, x=0, y=y_pos, groups={1},
					target_group_id=group+j, activate_group=True, item_id=collider_id, block_b_id=colliders[k]))
				y_pos -= 30
			y_pos -= 30
			for k in range(4):
				triggers.append(Object(
						id=1006, x=0, y=y_pos, groups={group+j}, multi_trigger=True,
						target_group_id=color+k, hold_time=self.screen.iteration_period+0.01,
						pulse_mode=1, copied_color_id=palette[k]))
				y_pos -= 30
			y_pos -= 30 * 2

		return triggers



	def get_WHI(self, group):
		return Object(id=1764, x=0, y=0, groups={self.screen.invisible_group, group+2})



# WHI
# Object(id=1766, x=-29, y=0, editor_layer_1=2, groups={44}, group_parent=True)

# Ground
# Object(id=1764, x=60, y=0, groups={48})





# 





	# def get_triggers(self, i, group, collider_1, collider_2):
	# 	fac = -1 + 2 / (self.screen.n - 1) * i
	# 	return [
	# 		# Wall segments follow
	# 		Object(id=1347, x=0, y=1020, groups={1}, multi_trigger=True,
	# 			target_group_id=group+6, follow_target_pos_center_id=group+2, duration=999, x_mod=0, y_mod=-1),
	# 		Object(id=1347, x=0, y=990, groups={1}, multi_trigger=True,
	# 			target_group_id=group+7, follow_target_pos_center_id=group+2, duration=999, x_mod=0, y_mod=0.5),
	# 		Object(id=1347, x=0, y=945, groups={1}, multi_trigger=True,
	# 			target_group_id=group+5, follow_target_pos_center_id=group+2, duration=999, x_mod=0, y_mod=0.25),

	# 		# Depth fail colliders
	# 		Object(id=1815, x=0, y=870, groups={1},
	# 			target_group_id=group+5, activate_group=True, item_id=1, block_b_id=collider_1),
	# 		Object(id=1815, x=0, y=840, groups={self.screen.cycle1_group, group+6}, multi_trigger=True,
	# 			target_group_id=group+5, item_id=7, block_b_id=collider_1),
	# 		# ^1 | 2v
	# 		Object(id=1815, x=0, y=780, groups={1},
	# 			target_group_id=group+5, activate_group=True, item_id=1, block_b_id=collider_2),
	# 		Object(id=1815, x=0, y=750, groups={self.screen.cycle2_group, group+7}, multi_trigger=True,
	# 			target_group_id=group+5, item_id=7, block_b_id=collider_2),

	# 		# Corner color colliders
	# 		Object(id=1815, x=10, y=815, groups={1},
	# 			target_group_id=group+2, activate_group=True, item_id=5, block_b_id=collider_1),
	# 		# ^1 | 2v
	# 		Object(id=1815, x=10, y=725, groups={1},
	# 			target_group_id=group+2, activate_group=True, item_id=5, block_b_id=collider_2),

	# 		# Cycle start move
	# 		Object(id=901, x=0, y=660, groups={self.screen.cycle1_group}, multi_trigger=True, target_group_id=group, duration=0,
	# 			follow_target_pos_center_id=self.screen.camera_group, use_target_enabled=True),
	# 		Object(id=901, x=0, y=630, groups={self.screen.cycle1_group}, multi_trigger=True, target_group_id=group+3, duration=0,
	# 			follow_target_pos_center_id=self.screen.ground_group, use_target_enabled=True, target_pos_coordinates=2),
	# 		# ^1 | 2v
	# 		Object(id=901, x=0, y=330, groups={self.screen.cycle2_group}, multi_trigger=True, target_group_id=group+1, duration=0,
	# 			follow_target_pos_center_id=self.screen.camera_group, use_target_enabled=True),
	# 		Object(id=901, x=0, y=300, groups={self.screen.cycle2_group}, multi_trigger=True, target_group_id=group+4, duration=0,
	# 			follow_target_pos_center_id=self.screen.ground_group, use_target_enabled=True, target_pos_coordinates=2),

	# 		# Ray follow
	# 		Object(id=1347, x=0, y=570, groups={group+6, self.screen.cycle1_group}, multi_trigger=True,
	# 			target_group_id=group, follow_target_pos_center_id=self.screen.forward_group_1, duration=0.25, x_mod=1, y_mod=1),
	# 		Object(id=1347, x=0, y=540, groups={group+6, self.screen.cycle1_group}, multi_trigger=True,
	# 			target_group_id=group, follow_target_pos_center_id=self.screen.right_group_1, duration=0.25, x_mod=fac, y_mod=fac),
	# 		# ^1 | 2v
	# 		Object(id=1347, x=0, y=240, groups={group+7, self.screen.cycle2_group}, multi_trigger=True,
	# 			target_group_id=group+1, follow_target_pos_center_id=self.screen.forward_group_2, duration=0.25, x_mod=1, y_mod=1),
	# 		Object(id=1347, x=0, y=210, groups={group+7, self.screen.cycle2_group}, multi_trigger=True,
	# 			target_group_id=group+1, follow_target_pos_center_id=self.screen.right_group_2, duration=0.25, x_mod=fac, y_mod=fac),

	# 		# Indicator move
	# 		Object(id=901, x=0, y=510, groups={group+6, self.screen.cycle1_delayed_group}, multi_trigger=True,
	# 			target_group_id=group+3, move_x=0, move_y=150, duration=0.2, easing=14),
	# 		# ^1 | 2v
	# 		Object(id=901, x=0, y=180, groups={group+7, self.screen.cycle2_delayed_group}, multi_trigger=True,
	# 			target_group_id=group+4, move_x=0, move_y=150, duration=0.2, easing=14),

	# 		# On ray hit collision
	# 		Object(id=1815, x=0, y=465, groups={1},
	# 			target_group_id=group+3, activate_group=True, item_id=1, block_b_id=collider_1),
	# 		# ^1 | 2v
	# 		Object(id=1815, x=0, y=135, groups={1},
	# 			target_group_id=group+4, activate_group=True, item_id=1, block_b_id=collider_2),

	# 		# Move WHI to indicator
	# 		Object(id=901, x=0, y=420, groups={self.screen.cycle1_end_group}, multi_trigger=True,
	# 			target_group_id=group+2, duration=0.1,
	# 			follow_target_pos_center_id=group+3, use_target_enabled=True, target_pos_coordinates=2),
	# 		# ^1 | 2v
	# 		Object(id=901, x=0, y=90, groups={self.screen.cycle2_end_group}, multi_trigger=True,
	# 			target_group_id=group+2, duration=0.1,
	# 			follow_target_pos_center_id=group+4, use_target_enabled=True, target_pos_coordinates=2),

	# 		# Ray stop triggers / indicators
	# 		Object(id=1616, x=-7.5, y=0, groups={group+3}, scale=0.5, multi_trigger=True,
	# 			target_group_id=group+6),
	# 		# ^1 | 2v
	# 		Object(id=1616, x=7.5, y=0, groups={group+4}, scale=0.5, multi_trigger=True,
	# 			target_group_id=group+7),

	# 		# WHI / Corner pulse
	# 		Object(id=1006, x=0, y=0, groups={group+2}, multi_trigger=True, target_group_id=group+5,
	# 			hold_time=0.15, pulse_mode=1, pulse_type=1, copied_color_id=21)
	# 	]