from MagnumOpus import *
from math import *
from TunnelObjects import get_line
import copy

GROUP_OFFSET = 100
COLLIDER_OFFSET = 100
WALL_COLLIDER = 1

DEPTH = 32
DEPTH_LOG = math.ceil(math.log(DEPTH, 2))
DEPTH_LOG_POW = 2 ** DEPTH_LOG
GROUPS_PER_STRIP = DEPTH_LOG * 2 - 1

WIDTH = 20
# SCREEN_WIDTH = 50 * 0.25

HFoV = 90
VFoV = 90
WALL_HEIGHT = 1
NEAR_CLIPPING_PLANE = 1
DEPTH_DISTANCE = 10

LINE_WIDTH = 0.25
LINE_HEIGHT = 9

SEPARATIONS = 1
WALL_COLLIDERS = [1, 4]
ROTATION_CENTERS = [20, 32]
COLLIDER_SEPARATIONS = [30, 31]
SEPARATION_OFFSET = (900, 0)

SCREEN_POS = (300, 150)
CAMERA_POS = (2325, 525)
TRIGGER_POS = (315, 2265)

MIN_V = 0.5

def cerate_separation_maps(objects):
	duplicates = []
	for obj in objects:
		if obj.id == 1816:
			if obj.item_id != 1:
				continue

			for s in range(1, SEPARATIONS):
				new_col = copy.deepcopy(obj)
				new_col.x += SEPARATION_OFFSET[0] * s
				new_col.y += SEPARATION_OFFSET[1] * s
				new_col.item_id = WALL_COLLIDERS[s]
				duplicates.append(new_col)
			continue
		if obj.id == 1764:
			if obj.groups == None:
				continue
			if not ROTATION_CENTERS[0] in obj.groups:
				continue
			for s in range(1, SEPARATIONS):
				new_dot = copy.deepcopy(obj)
				new_dot.x += SEPARATION_OFFSET[0] * s
				new_dot.y += SEPARATION_OFFSET[1] * s
				new_dot.groups.remove(ROTATION_CENTERS[0])
				new_dot.groups.add(ROTATION_CENTERS[s])
				new_dot.groups.add(17)
				duplicates.append(new_dot)
	return duplicates


def get_lines(pos, k, min_group):
	pos = SCREEN_POS
	x_offset = (- WIDTH / 2 + k) * LINE_WIDTH * 30 + LINE_WIDTH / 2
	y_offset = 0

	depths = get_depths()

	objects = []
	for i in range(DEPTH):
		groups = get_groups(i, min_group)
		if i < DEPTH_LOG_POW / 2:
			groups = groups[:-1]

		height = min(1, 1 / (tan(radians(VFoV / 2)) * depths[i])) * LINE_HEIGHT * 30
		# (x, y) = (pos[0], pos[1] - 30 * i)
		(x, y) = (pos[0] + x_offset, pos[1] + y_offset)
		# line = get_line((x, y - height/2), (x, y + height/2), LINE_WIDTH * 30)
		line = get_line((x, y - height/2), (x, y - height/2 + LINE_WIDTH * 30), LINE_WIDTH * 30)
		for obj in line:
			obj.color_1 = 4
			obj.color_1_hsv_enabled = True
			obj.color_1_hsv_values = HSV(h=0, s=1, v=(1 - (i / (DEPTH - 1)) * (1 - MIN_V)))

			obj.groups = set(groups)
			obj.groups.add(1)
			# print(obj)
		objects += line
	# quit()
	return objects

def get_colliders(pos, k):
	max_width = 2 * DEPTH_DISTANCE * tan(radians(HFoV) / 2)
	angle = atan((max_width * (k / (WIDTH - 1) - .5)) / DEPTH_DISTANCE)

	depths = get_depths()

	objects = []
	for i in range(DEPTH):
		x_i = depths[i]
		# x_i = i / (DEPTH - 1) * DEPTH_DISTANCE

		min_scale = 8
		if i > 0:
			min_scale = min(min_scale, x_i - depths[i-1])
		if i < DEPTH - 1:
			min_scale = min(min_scale, depths[i+1] - x_i)

		# print( "- ", min_scale)

		horiz_width = max_width * x_i / DEPTH_DISTANCE
		min_scale = min(horiz_width / (WIDTH - 1), min_scale)

		# print(horiz_width)

		min_scale *= 0.7
		min_scale = floor(min_scale * 100) / 100

		# print("fin: ", min_scale)

		x_pos = tan(angle) * x_i * 30
		# x_pos = tan(angle) * max_width * 30
		(x, y) = (pos[0] + x_pos, pos[1] + x_i * 30)

		separation_id = k % SEPARATIONS
		x += SEPARATION_OFFSET[0] * separation_id		
		y += SEPARATION_OFFSET[1] * separation_id		
		rotation_group = COLLIDER_SEPARATIONS[separation_id]
		collider_id = COLLIDER_OFFSET + (k // SEPARATIONS) * DEPTH + i

		objects.append(Object(id=1816, x=x, y=y, item_id=collider_id, scale=min_scale,
			is_active_trigger=True, dynamic_block=True, groups={14, 17, rotation_group}))
	# quit()
	return objects

def get_depths():

	min_depth = WIDTH * 0.055 * .5 / tan(radians(HFoV) / 2)
	min_depth = max(NEAR_CLIPPING_PLANE, min_depth)

	min_depth_step = 0.055

	if DEPTH_DISTANCE - min_depth < min_depth_step * (DEPTH - 1):
		raise Exception("Depth cannot fit the colliders. Increase depth distance or decrease collider count.")

	excess_step = (DEPTH_DISTANCE - min_depth) / (DEPTH - 1) - min_depth_step
	step_increase = excess_step * 2 / (DEPTH - 2)
	step = min_depth_step
	current_depth = min_depth

	# depths = [DEPTH / ((DEPTH - i) / NEAR_CLIPPING_PLANE + 1 / DEPTH_DISTANCE)
	# 	for i in range(DEPTH)]
	depths = []
	for i in range(DEPTH):
		depths.append(current_depth)
		current_depth += step
		step += step_increase

	return depths


def get_triggers(min_group, k):
	pos = (TRIGGER_POS[0] + k * (WIDTH + 5) * 30, TRIGGER_POS[1])

	objects = []
	for i in range(DEPTH):
		groups_on = get_groups(i, min_group)
		groups_off = toggle_groups(groups_on)

		if i < DEPTH_LOG_POW / 2:
			groups_on = groups_on[:-1]
		else:
			groups_off = groups_off[:-1]

		for j in range(len(groups_on)):
			(x, y) = (pos[0] + 30 * i , pos[1] - (len(groups_on) - j - 1) * 30)
			collider_id = COLLIDER_OFFSET + (k // SEPARATIONS) * DEPTH + i
			wall_id = WALL_COLLIDERS[k % SEPARATIONS]

			objects.append(Object(id=1815, x=x, y=y, groups={3},
				target_group_id=groups_on[j], item_id=wall_id, block_b_id=collider_id, activate_group=True,
				spawn_triggered=True, multi_trigger=True, is_active_trigger=True))

		for j in range(len(groups_off)):
			(x, y) = (pos[0] + 30 * i, pos[1] - (2 * len(groups_off) - j) * 30)
			collider_id = COLLIDER_OFFSET + (k // SEPARATIONS) * DEPTH + i

			objects.append(Object(id=1815, x=x, y=y, groups={3},
				target_group_id=groups_off[j], item_id=wall_id, block_b_id=collider_id,
				spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=0.5))

		(x, y) = (pos[0] + 30 * i, pos[1] - (2 * len(groups_off) + 3) * 30)
		objects.append(Object(id=1815, x=x, y=y, groups={3},
			target_group_id=15, item_id=wall_id, block_b_id=collider_id,
				spawn_triggered=True, multi_trigger=True, is_active_trigger=True))

	groups = (groups_on + groups_off)
	groups.sort()
	# for i in range(len(groups)):
	# 	group = groups[i]
	# 	(x, y) = (pos[0] - 60, pos[1] - 30 * (1 + i))
		# This one's unfinished
		# objects.append(Object(id=1815, x=x, y=y, groups={13, 15},
		# 	target_group_id=15, item_id=wall_id, block_b_id=collider_id,
		# 		spawn_triggered=True, multi_trigger=True, is_active_trigger=True))


	return objects

def get_strip(pos, k):
	objects = []
	min_group = GROUP_OFFSET + k * GROUPS_PER_STRIP
	objects += get_lines(pos, k, min_group)
	objects += get_colliders(CAMERA_POS, k)
	objects += get_triggers(min_group, k)
	return objects

def get_screen():
	# Some strip setup stuff
	objects = []
	for k in range(WIDTH):
		objects += get_strip(SCREEN_POS, k)
	return objects


def get_groups(num, min_group):
	# bin_length = math.ceil(math.log(DEPTH, 2))
	bin_length = DEPTH_LOG
	b = format(num, 'b')
	b = '0' * (bin_length - len(b)) + b
	b = list(map(int, b))
	b_flipped = b[::-1]

	groups = []
	for i in range(bin_length):
		digit = b_flipped[i]
		# if i == bin_length - 1 and digit == 0:
		# 	continue
		group = min_group + 2 * i + toggle_digit(digit)
		groups.append(group)

	return groups


# I was too lazy to define proper behaviour
def toggle_digit(digit):
	return (1 if digit == 0 else 0)

def toggle_groups(groups):
	new_groups = []
	for group in groups:
		new_groups.append(group - 1 if group % 2 else group + 1)
	return new_groups

if __name__ == "__main__":
	editor, db, local_levels = load_editor()
	
	add_objects(editor, cerate_separation_maps(editor.get_objects()))
	add_objects(editor, get_screen())

	save_changes(editor, db, local_levels)

