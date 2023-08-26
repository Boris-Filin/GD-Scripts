from gd.api import (
	Editor,
	Object,
)


def get_slices(x, y, n=90, min_group=641, min_trigger_group=281, groups_per_trigger_slice=4):
	objects = []

	follow_player_group = 4
	groups_per_slice = 3

	x0 = x * 30
	y0 = y * 30

	for i in range(n):
		slice_group = min_group + groups_per_slice * i
		trigger_slice_group = min_trigger_group + groups_per_trigger_slice * i
		
		x_slice = x0 + 2.5 + 5 * i
		y_slice = y0 + 32.5

		upper_slice = Object(id=1757, x=x_slice, y=y_slice+75*2, groups={follow_player_group, slice_group, slice_group+1},
			rotation=-90, color_1=5, z_layer=7, z_order=1, scale=5)
		middle_slice = Object(id=1757, x=x_slice, y=y_slice+75, groups={follow_player_group, slice_group},
			rotation=-90, color_1=5, z_layer=7, z_order=1, scale=5)
		lower_slice = Object(id=1757, x=x_slice, y=y_slice, groups={follow_player_group, slice_group, slice_group+2},
			rotation=-90, color_1=5, z_layer=7, z_order=1, scale=5)
		objects.append(upper_slice)
		objects.append(middle_slice)
		objects.append(lower_slice)

		upper_follow = Object(id=1347, x=15+(50+i)*30, y=-15-90, groups={1}, spawn_triggered=True, is_active_trigger=True,
			target_group_id=slice_group+1, follow_target_pos_center_id=trigger_slice_group, duration=999, x_mod=0, y_mod=-0.5)
		lower_follow = Object(id=1347, x=15+(50+i)*30, y=-15-120, groups={1}, spawn_triggered=True, is_active_trigger=True,
			target_group_id=slice_group+2, follow_target_pos_center_id=trigger_slice_group, duration=999, x_mod=0, y_mod=0.5)
		objects.append(upper_follow)
		objects.append(lower_follow)

	return objects




