import math

from gd.api import (
	Editor,
	Object,
)


def get_rays(x, y, n=90, min_group=101, min_collision=51):
	objects = []
	for i in range(n):
		collider_1 = Object(id=1816, x=15+x*30, y=15+y*30, item_id=min_collision+i, groups={2, min_group+i},
			dynamic_block=False, editor_layer_1=1, scale=0.1, is_active_trigger=True)
		collider_2 = Object(id=1816, x=15+x*30, y=15+y*30, item_id=min_collision+n+i, groups={2, min_group+n+i},
			dynamic_block=False, editor_layer_1=1, scale=0.1, is_active_trigger=True)
		objects.append(collider_1)
		objects.append(collider_2)

	return objects

def get_ray_triggers(x, y, camera, fov=90, depth=4.5, n=90, min_ray1_group=101, camera_group=14):
	objects = []
	groups_per_slice = 4
	min_ray2_group = min_ray1_group + n
	min_group = min_ray2_group + n
	min_ray1_collision = 51
	min_ray2_collision = min_ray1_collision + n

	far_plane = depth * math.tan(math.radians(fov / 2)) * 2

	x0 = 15 + x * 30
	y0 = 15 + y * 30

	for i in range(n):
		min_slice_group = min_group+groups_per_slice*i
		dir_x = far_plane * (-0.5 + i / (n - 1)) * 30
		dir_y = depth * 30
		x_slice = x0+30*i
		y_slice = y0
		move_1_a = Object(id=901, x=x_slice, y=y_slice, scale=0.5, groups={8}, spawn_triggered=True, multi_trigger=True, is_active_trigger=True,
			target_group_id=min_ray1_group+i, follow_target_pos_center_id=camera_group, use_target_enabled=True)
		move_1_b = Object(id=901, x=camera.x+90+5*i, y=camera.y, scale=0.5, groups={8, min_slice_group}, spawn_triggered=True,
			multi_trigger=True, is_active_trigger=True, target_group_id=min_ray1_group+i, move_x=dir_x, move_y=dir_y, duration=0.2)
		objects.append(move_1_a)
		objects.append(move_1_b)

		move_2_a = Object(id=901, x=x_slice+10, y=y_slice, scale=0.5, groups={11}, spawn_triggered=True, multi_trigger=True, is_active_trigger=True,
			target_group_id=min_ray2_group+i, follow_target_pos_center_id=camera_group, use_target_enabled=True)
		move_2_b = Object(id=901, x=x_slice+10, y=y_slice-5, scale=0.5, groups={11, min_slice_group+1}, spawn_triggered=True,
			multi_trigger=True, is_active_trigger=True, target_group_id=min_ray2_group+i, move_x=dir_x, move_y=dir_y, duration=0.2)
		objects.append(move_2_a)
		objects.append(move_2_b)

		collision_1 = Object(id=1815, x=x_slice, y=y_slice-30, scale=0.5, groups={1}, spawn_triggered=True, is_active_trigger=True,
			target_group_id=min_slice_group+2, activate_group=True, item_id=1, block_b_id=min_ray1_collision+i)
		stop_cast_1 = Object(id=1616, x=x_slice, y=y_slice-50, scale=0.5, groups={min_slice_group+2}, spawn_triggered=True,
			multi_trigger=True, is_active_trigger=True, target_group_id=min_slice_group)
		move_to_1 = Object(id=901, x=x_slice, y=y_slice-70, scale=0.5, groups={min_slice_group+2}, spawn_triggered=True,
			multi_trigger=True, is_active_trigger=True, target_group_id=min_slice_group, follow_target_pos_center_id=min_ray1_group+i,
			use_target_enabled=True, duration=0.1)
		stop_other_move_1 = Object(id=1616, x=x_slice, y=y_slice-80, scale=0.5, groups={min_slice_group+2}, spawn_triggered=True,
			multi_trigger=True, is_active_trigger=True, target_group_id=min_slice_group+3)
		objects.append(collision_1)
		objects.append(stop_cast_1)
		objects.append(move_to_1)
		objects.append(stop_other_move_1)

		collision_2 = Object(id=1815, x=x_slice+10, y=y_slice-30, scale=0.5, groups={1}, spawn_triggered=True, is_active_trigger=True,
			target_group_id=min_slice_group+3, activate_group=True, item_id=1, block_b_id=min_ray2_collision+i)
		stop_cast_2 = Object(id=1616, x=x_slice+10, y=y_slice-50, scale=0.5, groups={min_slice_group+3}, spawn_triggered=True, multi_trigger=True,
			is_active_trigger=True, target_group_id=min_slice_group+1)
		move_to_2 = Object(id=901, x=x_slice+10, y=y_slice-70, scale=0.5, groups={min_slice_group+3}, spawn_triggered=True,
			multi_trigger=True, is_active_trigger=True, target_group_id=min_slice_group, follow_target_pos_center_id=min_ray2_group+i,
			use_target_enabled=True, duration=0.1)
		stop_other_move_2 = Object(id=1616, x=x_slice+10, y=y_slice-80, scale=0.5, groups={min_slice_group+3}, spawn_triggered=True,
			multi_trigger=True, is_active_trigger=True, target_group_id=min_slice_group+2)
		objects.append(collision_2)
		objects.append(stop_cast_2)
		objects.append(move_to_2)
		objects.append(stop_other_move_2)

	return objects


