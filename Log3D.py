from MagnumOpus import *
from TunnelObjects import get_line

from math import *
import sys
import copy
from itertools import chain

# Various default variables
GROUP_OFFSET = 130
COLLIDER_OFFSET = 100
COLOR_OFFSET = 30
WALL_COLLIDER = 1

# This defines the de-facto resolution of the screen
WIDTH = 78
DEPTH = 32

# Some important constants derived from depth 
DEPTH_LOG = math.ceil(math.log(DEPTH, 2))
DEPTH_LOG_POW = 2 ** DEPTH_LOG
BINARY_GROUPS_COUNT = DEPTH_LOG
# BINARY_ZERO_GROUPS_COUNT = 2
# TOTAL_BINARY_COUNT = BINARY_GROUPS_COUNT + BINARY_ZERO_GROUPS_COUNT


# Stuff necessary to define the rendering behaviour
HFoV = 90
VFoV = 135
NEAR_CLIPPING_PLANE = 0.01
MIN_DEPTH_DISTANCE = 20
# WALL_HEIGHT = 6
# ANGLE_OFFSET = -0.15

# Visual line variables
LINE_WIDTH = 1/5
LINE_HEIGHT = 9
MIN_V = 0.3

# Separations are necessary to bypass the 1k collider IDs limit
SPLIT_COUNT = 3
WALL_COLLIDERS = [51, 53, 55, 57, 59]
DEPTH_FAIL_COLLIDERS = [50, 52, 54, 56, 58, 60]
ROTATION_CENTERS = [121, 123, 125, 127]
SPLIT_COLLIDERS = [120, 122, 124, 126]
SPLIT_OFFSET = (1800, 0)

# Values for the texturing of the walls
COLOR_COUNT = 3
MIN_STRIP_COLOR = 30
TARGET_COLORS = [21, 22, 23]

COLOR_COLLIDERS = [30, 31, 32, 33, 34, 35]

COLORS_PER_STRIP = 6

MIN_STRIP_Z = -99
Z_LAYERS_PER_STRIP = 2

# Depth layering to prevent excessive lag
# NOTE: technically it is no longer tied to depth,
#  but fixing all of the references takes too much time.
SUBFRAME_COUNT = 10
SUBFRAME_GROUPS = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]

# Various position variables
SCREEN_POS = (300, 150)
CAMERA_POS = (2325, 1125)
COLLISION_TRIGGER_POS = (315, 2265)
TEXTURE_TRIGGER_POS = (315, 5265)

GROUPS_PER_STRIP = BINARY_GROUPS_COUNT
# GROUPS_PER_STRIP = BINARY_GROUPS_COUNT + BINARY_ZERO_GROUPS_COUNT + COLOR_COUNT + 1


# Duplicate the map for the separation colliders
def cerate_separation_maps(objects):
	duplicates = []
	for obj in objects:
		if obj.id == 1816:
			if obj.item_id == 1:
				for s in range(SPLIT_COUNT):
					new_col = copy.deepcopy(obj)
					new_col.x += SPLIT_OFFSET[0] * (s + 1)
					new_col.y += SPLIT_OFFSET[1] * (s + 1)
					new_col.item_id = WALL_COLLIDERS[s]
					duplicates.append(new_col)
			continue
		if obj.id == 1764:
			if obj.groups == None:
				continue
			if not 18 in obj.groups:
				continue
			for s in range(SPLIT_COUNT):
				new_dot = copy.deepcopy(obj)
				new_dot.x += SPLIT_OFFSET[0] * (s + 1)
				new_dot.y += SPLIT_OFFSET[1] * (s + 1)
				new_dot.groups.remove(18)
				new_dot.groups.add(ROTATION_CENTERS[s])
				new_dot.groups.add(20)
				duplicates.append(new_dot)
			color_dot = copy.deepcopy(obj)
			color_dot.x += SPLIT_OFFSET[0] * (-1)
			color_dot.y += SPLIT_OFFSET[1] * (-1)
			color_dot.groups.remove(18)
			color_dot.groups.add(ROTATION_CENTERS[SPLIT_COUNT])
			color_dot.groups.add(20)
			duplicates.append(color_dot)
	return duplicates



# Object(id=579, x=0, y=168.75, editor_layer_1=2, groups={21}, z_order=1, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=198.75, editor_layer_1=2, groups={21}, z_order=1, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=917, x=0, y=183.75, editor_layer_1=2, groups={21}, z_order=1, color_1=2)
# Object(id=579, x=0, y=116.25, editor_layer_1=2, groups={21, 22}, z_order=3, rotation=90, color_1=1, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=138.75, editor_layer_1=2, groups={21, 22}, z_order=3, rotation=90, color_1=1, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=63.75, editor_layer_1=2, z_order=5, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=86.25, editor_layer_1=2, z_order=5, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=11.25, editor_layer_1=2, groups={22}, z_order=7, rotation=90, color_1=1, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=33.75, editor_layer_1=2, groups={22}, z_order=7, rotation=90, color_1=1, z_layer=3, scale=0.75)
# Object(id=917, x=0, y=93.75, editor_layer_1=2, z_order=11, color_1=1, z_layer=3)
# Object(id=917, x=0, y=101.25, editor_layer_1=2, z_order=11, color_1=1, z_layer=3)
# Object(id=579, x=0, y=41.25, editor_layer_1=2, groups={22}, z_order=9, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=917, x=0, y=153.75, editor_layer_1=2, groups={21, 22}, z_order=13, color_1=2)
# Object(id=579, x=0, y=-168.75, editor_layer_1=2, groups={22, 23}, z_order=1, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=-116.25, editor_layer_1=2, groups={23}, z_order=3, rotation=90, color_1=1, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=-138.75, editor_layer_1=2, groups={23}, z_order=3, rotation=90, color_1=1, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=-63.75, editor_layer_1=2, groups={21, 22, 23}, z_order=5, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=-86.25, editor_layer_1=2, groups={21, 22, 23}, z_order=5, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=-11.25, editor_layer_1=2, groups={21, , 23}, z_order=7, rotation=90, color_1=1, z_layer=3, scale=0.75)
# Object(id=579, x=0, y=-33.75, editor_layer_1=2, groups={21, , 23}, z_order=7, rotation=90, color_1=1, z_layer=3, scale=0.75)
# Object(id=917, x=0, y=-93.75, editor_layer_1=2, groups={21, 22, 23}, z_order=11, color_1=1, z_layer=3)
# Object(id=917, x=0, y=-101.25, editor_layer_1=2, groups={21, 22, 23}, z_order=11, color_1=1, z_layer=3)
# Object(id=579, x=0, y=-41.25, editor_layer_1=2, groups={21, , 23}, z_order=9, rotation=90, color_1=2, z_layer=3, scale=0.75)
# Object(id=917, x=0, y=-153.75, editor_layer_1=2, groups={23}, z_order=13, color_1=2)
# Object(id=917, x=0, y=-183.75, editor_layer_1=2, groups={22, 23}, z_order=1, color_1=2)
# Object(id=579, x=0, y=-198.75, editor_layer_1=2, groups={22, 23}, z_order=1, rotation=90, color_1=2, z_layer=3, scale=0.75)

# Get all the individual lines for a specific strip
def get_lines(pos, k, min_group):
	pos = SCREEN_POS
	x_offset = (- WIDTH / 2 + k) * LINE_WIDTH * 30 + LINE_WIDTH * 30 / 2
	y_offset = 0

	# Fix this stuff

	return []


'''

	depths = get_depths()


	objects = []
	# Iterating from farthest to closest
	# for i in range(1, DEPTH):
		groups = get_groups(i, min_group)




		# line = [Object(id=211, x=x, y=y, scale=strip_width/30, groups=set(groups), z_order=min_z)]

		for obj in line:
			obj.color_1_hsv_enabled = True
			obj.color_1_hsv_values = HSV(h=0, s=1, v=(1 - (dist_to_camera / (DEPTH - 1)) * (1 - MIN_V)))
			obj.z_layer = 3

			# obj.z_order = min_z
			# obj.z_order = 1

			obj.groups = set(groups)
			obj.groups.add(1)
			obj.groups.add(23)

		objects += line

	return objects
'''
	
def get_floor(pos):
	depths = get_depths()
	objects = []

	block_width = WIDTH * LINE_WIDTH * 30 / 3
	leeway = 0.1
	x_values = [
		pos[0] - block_width + (leeway / 2) * 30,
		pos[0],
		pos[0] + block_width - (leeway / 2) * 30]

	for i in range(1, DEPTH):
		dist_to_camera = DEPTH - i - 1

		# height = min(1, 1 / (tan(radians(VFoV / 2)) * depths[i])) * WALL_HEIGHT * LINE_HEIGHT * 30
		# y_offset = ANGLE_OFFSET * (height - 300)
		y_offset = - 1 - i * LINE_WIDTH
		# floor_level = pos[1] + y_offset - height / 2

		y = y_offset - .5 * block_width - leeway

		layer = []
		for x in x_values:
			layer.append(Object(id=211, x=x, y=y, scale=block_width / 30 + leeway))
		
		for obj in layer:
			obj.color_1 = 19
			obj.color_1_hsv_enabled = True
			obj.color_1_hsv_values = HSV(h=0, s=1, v=(1 - (dist_to_camera / (DEPTH - 1)) * (1 - MIN_V)))
			obj.z_order = i
			obj.groups = {1}

		objects += layer

	return objects


# Get all of the colliders in the right order
def get_colliders(pos, k):
	max_width = 2 * MIN_DEPTH_DISTANCE * tan(radians(HFoV) / 2)
	angle = atan((max_width * (k / (WIDTH - 1) - .5)) / MIN_DEPTH_DISTANCE)

	depths = get_depths()

	objects = []
	for i in range(DEPTH):
		x_i = depths[i]

		depth_layer_id = floor(k / WIDTH * SUBFRAME_COUNT)
		next_depth_layer_id = floor((k+1) / WIDTH * SUBFRAME_COUNT)
		depth_layer_group = SUBFRAME_GROUPS[depth_layer_id]

		min_scale = 8
		if i < DEPTH - 1:
			min_scale = min(min_scale, x_i - depths[i+1])
		if i > 0:
			min_scale = min(min_scale, depths[i-1] - x_i)

		horiz_width = max_width * x_i / MIN_DEPTH_DISTANCE
		min_scale = min(horiz_width / (WIDTH - 1) - 0.25, min_scale)


		# min_scale *= 0.9
		min_scale = floor(min_scale * 100) / 100
		# min_scale -= 0.01
		if min_scale < 0.2:
			min_scale = 0.01
		min_scale = max(min_scale, 0.01)

		# print("fin: ", min_scale)

		x_pos = tan(angle) * x_i * 30
		# x_pos = tan(angle) * max_width * 30
		(x, y) = (pos[0] + x_pos, pos[1] + x_i * 30)

		separation_id = k % SPLIT_COUNT
		# separation_id = floor(k / WIDTH * SEPARATIONS)
		x += SPLIT_OFFSET[0] * (separation_id + 1)		
		y += SPLIT_OFFSET[1] * (separation_id + 1)
		rotation_group = SPLIT_COLLIDERS[separation_id]
		collider_id = COLLIDER_OFFSET + (k // SPLIT_COUNT) * DEPTH + i
		# first_separation_k = ceil(separation_id * WIDTH / SEPARATIONS)
		# collider_id = COLLIDER_OFFSET + (k - first_separation_k) * DEPTH + i

		objects.append(Object(id=1816, x=x, y=y, item_id=collider_id, scale=min_scale,
			is_active_trigger=True, dynamic_block=True, groups={2, 20, rotation_group, depth_layer_group}))

		# Depth fail colliders
		if i == 0 or (i == DEPTH - 1 and (depth_layer_id != next_depth_layer_id or k == WIDTH)):
			fail_collider_id = DEPTH_FAIL_COLLIDERS[separation_id]
			objects.append(Object(id=1816, x=x, y=y, item_id=fail_collider_id, scale=min_scale,
				is_active_trigger=True, groups={2, 20, rotation_group}))


	return objects


# Get the triggers (logic) that govern the rendering of the 3D scene
def get_triggers(min_group, k):
	pos = (COLLISION_TRIGGER_POS[0] + k * (DEPTH + 3) * 30, COLLISION_TRIGGER_POS[1])
	min_collider = COLLIDER_OFFSET + (k // SPLIT_COUNT) * DEPTH
	split_id = k % SPLIT_COUNT
	wall_id = WALL_COLLIDERS[split_id]

	subframe_id = floor(k / WIDTH * SUBFRAME_COUNT)
	next_subframe_id = floor((k+1) / WIDTH * SUBFRAME_COUNT)

	objects = []

	# Depth fail logic and initial toggle - to be deprecated
	fail_collider_id = DEPTH_FAIL_COLLIDERS[split_id]

	# Normal rendering
	for i in range(DEPTH):
		groups_on = get_groups(DEPTH - i - 1, min_group)
		collider_id = min_collider + i
	
		for j in range(BINARY_GROUPS_COUNT):
			group = min_group + j
			is_on = group in groups_on
			if not is_on: continue

			(x, y) = (pos[0] + 30 * i , pos[1] - j * 30)
			trigger = Object(id=1815, x=x, y=y, groups={3},
				target_group_id=group, item_id=wall_id, block_b_id=collider_id, activate_group=True,
				spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=0.75)
			objects.append(trigger)


		if i == DEPTH - 1 and (subframe_id != next_subframe_id or k == WIDTH):
			trigger = Object(id=1815, x=x, y=y-30, groups={3},
				target_group_id=SUBFRAME_GROUPS[subframe_id],
				item_id=fail_collider_id, block_b_id=collider_id,
				spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=2)
			objects.append(trigger)

# Object(id=1049, x=225, y=195, groups={2},
# spawn_triggered=True, multi_trigger=True, is_active_trigger=True, target_group_id=6)

	# Color logic
	pulse_groups = [min_group + BINARY_GROUPS_COUNT + c for c in range(COLOR_COUNT)]
	prev_depth_layer_id = (subframe_id - 2) % SUBFRAME_COUNT
	prev_depth_layer_group = SUBFRAME_GROUPS[prev_depth_layer_id]

	coloring_group = min_group + BINARY_GROUPS_COUNT + COLOR_COUNT

	toggle_triggers = []

	for color_id in range(COLOR_COUNT):
		(x, y) = (pos[0] - (3 + color_id) * 30, pos[1] - 2 * 30)
		pulse_group = pulse_groups[color_id]
		strip_col = MIN_STRIP_COLOR + k

		pulse = Object(id=1006, x=x, y=y - 30, groups={pulse_group, coloring_group},
			spawn_triggered=True, multi_trigger=True, is_active_trigger=True,
			target_group_id=strip_col, hold_time=0.1, pulse_mode=1,
			copied_color_id=TARGET_COLORS[color_id])

		toggle = Object(id=1049, x=x, y=y, groups={pulse_group},
			target_group_id=coloring_group, spawn_triggered=True, multi_trigger=True, is_active_trigger=True)
		toggle_triggers.append(toggle)


		color_collider = COLOR_COLLIDERS[color_id]
		collider_id = COLLIDER_OFFSET + k

		trigger = Object(id=1815, x=x, y=y + 60, groups={3},
			target_group_id=pulse_group, item_id=color_collider, block_b_id=collider_id, activate_group=True,
			spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=0.5)

		# objects.append(trigger)
		
	# objects += toggle_triggers

	(x, y) = (pos[0] - 60, pos[1] - 4 * 30)
	toggle_on = Object(id=1049, x=x, y=y, groups={prev_depth_layer_group}, activate_group=True,
			target_group_id=coloring_group, spawn_triggered=True, multi_trigger=True, is_active_trigger=True)
	# objects.append(toggle_on)

	# toggle_off = Object(id=1049, x=x - 30, y=y, groups=set(pulse_groups),
	# 		target_group_id=coloring_group, spawn_triggered=True, multi_trigger=True, is_active_trigger=True)
	# objects.append(toggle_off)


	return objects

# Get all of the colliders that are used to render the textures
def get_color_colliders(pos, k):
	max_width = 2 * MIN_DEPTH_DISTANCE * tan(radians(HFoV) / 2)
	angle = atan((max_width * (k / (WIDTH - 1) - .5)) / MIN_DEPTH_DISTANCE)

	depths = get_depths()

	objects = []
	for i in range(DEPTH - 1, -1, -1):
		x_i = depths[i]

		depth_layer_id = (floor(k / WIDTH * SUBFRAME_COUNT)) % SUBFRAME_COUNT
		depth_layer_group = SUBFRAME_GROUPS[depth_layer_id]

		min_scale = 8
		if i < DEPTH - 1:
			min_scale = min(min_scale, x_i - depths[i+1])
		if i > 0:
			min_scale = min(min_scale, depths[i-1] - x_i)

		horiz_width = max_width * x_i / MIN_DEPTH_DISTANCE
		min_scale = min(horiz_width / (WIDTH - 1) - 0.25, min_scale)


		# min_scale *= 0.9
		min_scale = floor(min_scale * 100) / 100
		# min_scale -= 0.01
		if min_scale < 0.2:
			min_scale = 0.01
		min_scale = max(min_scale, 0.01)


		x_pos = tan(angle) * x_i * 30
		(x, y) = (pos[0] + x_pos, pos[1] + x_i * 30)

		separation_id = -1
		x += SPLIT_OFFSET[0] * separation_id		
		y += SPLIT_OFFSET[1] * separation_id
		rotation_group = SPLIT_COLLIDERS[SPLIT_COUNT]
		collider_id = COLLIDER_OFFSET + k

		groups = {2, 20, rotation_group, depth_layer_group}

		objects.append(Object(id=1816, x=x, y=y, item_id=collider_id, scale=min_scale,
			is_active_trigger=True, dynamic_block=True, groups=groups))

	return objects


# Get all of the objects for a specific strip on the screen
def get_strip(pos, k):
	objects = []
	min_group = GROUP_OFFSET + k * GROUPS_PER_STRIP
	objects += get_lines(pos, k, min_group)
	# objects += get_colliders(CAMERA_POS, k)
	objects += get_triggers(min_group, k)
	return objects

# Get all of the rendering objects (visual, physical, logic)
def get_screen():
	# Some strip setup stuff
	objects = []

	objects += get_floor(SCREEN_POS)
	
	for k in range(WIDTH):
		objects += get_color_colliders(CAMERA_POS, k)
	
	for k in range(WIDTH):
		objects += get_colliders(CAMERA_POS, k)

	for k in range(WIDTH):
		objects += get_strip(SCREEN_POS, k)
	
	return objects


# Get the depths list, farthest to lowest (this time deppths are not linear)
def get_depths():
	min_depth = WIDTH * 0.055 * .5 / tan(radians(HFoV) / 2)
	min_depth = max(NEAR_CLIPPING_PLANE, min_depth)

	min_depth_step = 0.055

	if MIN_DEPTH_DISTANCE - min_depth < min_depth_step * (DEPTH - 1):
		raise Exception("Depth cannot fit the colliders. Increase depth distance or decrease collider count.")

	excess_step = (MIN_DEPTH_DISTANCE - min_depth) / (DEPTH - 1) - min_depth_step
	step_increase = excess_step * 2 / (DEPTH - 2)
	step = min_depth_step
	current_depth = min_depth

	depths = []
	for i in range(DEPTH):
		depths.append(current_depth)
		current_depth += step
		step += step_increase

	return depths[::-1]


# Get the binary groups for the object at a given position
def get_groups(num, min_group):
	bin_length = math.ceil(math.log(DEPTH, 2))
	b = format(num, 'b')
	b = '0' * (bin_length - len(b)) + b
	b_int = list(map(int, b))
	b_flipped = b_int[::-1]

	groups = []
	for i in range(bin_length):
		if b_flipped[i] == 1:
			groups.append(min_group + i)


	return groups

def scale(objects, fac, center=(0,0)):
	for obj in objects:
		obj.x -= center[0]
		obj.y -= center[0]
	for obj in objects:
		if obj.scale != None:
			obj.scale *= fac
		obj.x *= scale
		obj.y *= scale
	for obj in objects:
		obj.x -= center[1]
		obj.y -= center[1]

if __name__ == "__main__":
	arguments = sys.argv

	editor, db, local_levels = load_editor()

	
	if len(arguments) < 2 or arguments[1] != 'void':
		# This ensures that there are enough groups specified for the collider splits
		splits_needed = SPLIT_COUNT + 1 - len(ROTATION_CENTERS)
		if splits_needed > 0:
			print("{} more splits needed!".format(splits_needed))
			quit()
		add_objects(editor, cerate_separation_maps(editor.get_objects()))
		add_objects(editor, get_screen())

	save_changes(editor, db, local_levels)
