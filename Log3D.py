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
BINARY_ZERO_GROUPS_COUNT = 2
TOTAL_BINARY_COUNT = BINARY_GROUPS_COUNT + BINARY_ZERO_GROUPS_COUNT


# Stuff necessary to define the rendering behaviour
HFoV = 90
VFoV = 135
NEAR_CLIPPING_PLANE = 0.01
DEPTH_DISTANCE = 20
WALL_HEIGHT = 6
ANGLE_OFFSET = -0.15

# Visual line variables
LINE_WIDTH = 0.15
LINE_HEIGHT = 9
MIN_V = 0.3

# Separations are necessary to bypass the 1k collider IDs limit
SEPARATIONS = 3
WALL_COLLIDERS = [51, 53, 55, 57, 59]
DEPTH_FAIL_COLLIDERS = [50, 52, 54, 56, 58, 60]
ROTATION_CENTERS = [121, 123, 125, 127]
COLLIDER_SEPARATIONS = [120, 122, 124, 126]
SEPARATION_OFFSET = (1800, 0)

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
DEPTH_LAYERS = 10
DEPTH_LAYER_GROUPS = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]

# Various position variables
SCREEN_POS = (300, 150)
CAMERA_POS = (2325, 1125)
TRIGGER_POS = (315, 2265)
TEXTURE_TRIGGER_POS = (315, 5265)

GROUPS_PER_STRIP = BINARY_GROUPS_COUNT + BINARY_ZERO_GROUPS_COUNT + COLOR_COUNT + 1


# Duplicate the map for the separation colliders
def cerate_separation_maps(objects):
	duplicates = []
	for obj in objects:
		if obj.id == 1816:
			if obj.item_id == 1:
				for s in range(SEPARATIONS):
					new_col = copy.deepcopy(obj)
					new_col.x += SEPARATION_OFFSET[0] * (s + 1)
					new_col.y += SEPARATION_OFFSET[1] * (s + 1)
					new_col.item_id = WALL_COLLIDERS[s]
					duplicates.append(new_col)
			continue
		if obj.id == 1764:
			if obj.groups == None:
				continue
			if not 18 in obj.groups:
				continue
			for s in range(SEPARATIONS):
				new_dot = copy.deepcopy(obj)
				new_dot.x += SEPARATION_OFFSET[0] * (s + 1)
				new_dot.y += SEPARATION_OFFSET[1] * (s + 1)
				new_dot.groups.remove(18)
				new_dot.groups.add(ROTATION_CENTERS[s])
				new_dot.groups.add(20)
				duplicates.append(new_dot)
			color_dot = copy.deepcopy(obj)
			color_dot.x += SEPARATION_OFFSET[0] * (-1)
			color_dot.y += SEPARATION_OFFSET[1] * (-1)
			color_dot.groups.remove(18)
			color_dot.groups.add(ROTATION_CENTERS[SEPARATIONS])
			color_dot.groups.add(20)
			duplicates.append(color_dot)
	return duplicates


# Get all the individual lines for a specific strip
def get_lines(pos, k, min_group):
	pos = SCREEN_POS
	x_offset = (- WIDTH / 2 + k) * LINE_WIDTH * 30 + LINE_WIDTH * 30 / 2
	y_offset = 0

	depths = get_depths()


	objects = []
	# Iterating from farthest to closest
	for i in range(1, DEPTH):
		groups = get_groups(i, min_group)

		dist_to_camera = DEPTH - i - 1

		height = min(1, 1 / (tan(radians(VFoV / 2)) * depths[i])) * WALL_HEIGHT * LINE_HEIGHT * 30
		if k == 0:
			print(height / 30)

		y_offset = ANGLE_OFFSET * (height - 300)

		(x, y) = (pos[0] + x_offset, pos[1] + y_offset)
		top = y + height / 2
		bottom = y - height / 2
		strip_width = LINE_WIDTH * 30
		# min_color = MIN_STRIP_COLOR + k * COLORS_PER_STRIP
		min_color = MIN_STRIP_COLOR
		min_z = MIN_STRIP_Z + (i // (2 ** BINARY_ZERO_GROUPS_COUNT)) * Z_LAYERS_PER_STRIP
		# line = get_line((x, y - height/2), (x, y + height/2), LINE_WIDTH * 30)

		divisions = [(x, top - fac * height) for fac in [0, 0.1, 0.26, 0.42, 0.58, 0.74, 0.9, 1]]

		end1 = get_line(divisions[0], divisions[1], strip_width, (0, height * 0.75))
		end2 = get_line(divisions[7], divisions[6], strip_width, (0, height * 0.75))
		for obj in (end1 + end2):
			obj.color_1 = min_color
			obj.z_order = min_z + 0

		middle = get_line(divisions[1], divisions[6], strip_width)
		for obj in middle:
			obj.color_1 = min_color + 1
			obj.z_order = min_z + 1

		tile1 = get_line(divisions[1], divisions[3], strip_width, (0, height * 0.15))
		for obj in tile1:
			obj.color_1 = min_color + 1
			obj.z_order = min_z + 1

		# tile2 = get_line(divisions[2], divisions[3], strip_width, (0, height * 0.15))
		# for obj in tile2:
		# 	obj.color_1 = min_color + 2
		# 	obj.z_order = min_z + 2

		tile3 = get_line(divisions[3], divisions[4], strip_width)
		for obj in tile3:
			obj.color_1 = min_color + 3
			obj.z_order = min_z + 3

		# tile4 = get_line(divisions[5], divisions[4], strip_width, (0, height * 0.15))
		# for obj in tile4:
		# 	obj.color_1 = min_color + 4
		# 	obj.z_order = min_z + 2

		tile5 = get_line(divisions[6], divisions[4], strip_width, (0, height * 0.15))
		for obj in tile5:
			obj.color_1 = min_color + 5
			obj.z_order = min_z + 1

		# line = end1 + tile1 + tile2 + tile3 + tile4 + tile5 + end2
		# line = end1 + tile1 + tile3 + tile5 + end2
		line = end1 + end2 + middle

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

		height = min(1, 1 / (tan(radians(VFoV / 2)) * depths[i])) * WALL_HEIGHT * LINE_HEIGHT * 30
		y_offset = ANGLE_OFFSET * (height - 300)
		floor_level = pos[1] + y_offset - height / 2

		y = floor_level - .5 * block_width - leeway

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
	max_width = 2 * DEPTH_DISTANCE * tan(radians(HFoV) / 2)
	angle = atan((max_width * (k / (WIDTH - 1) - .5)) / DEPTH_DISTANCE)

	depths = get_depths()

	objects = []
	for i in range(DEPTH):
		x_i = depths[i]

		depth_layer_id = floor(k / WIDTH * DEPTH_LAYERS)
		next_depth_layer_id = floor((k+1) / WIDTH * DEPTH_LAYERS)
		depth_layer_group = DEPTH_LAYER_GROUPS[depth_layer_id]

		min_scale = 8
		if i < DEPTH - 1:
			min_scale = min(min_scale, x_i - depths[i+1])
		if i > 0:
			min_scale = min(min_scale, depths[i-1] - x_i)

		horiz_width = max_width * x_i / DEPTH_DISTANCE
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

		separation_id = k % SEPARATIONS
		# separation_id = floor(k / WIDTH * SEPARATIONS)
		x += SEPARATION_OFFSET[0] * (separation_id + 1)		
		y += SEPARATION_OFFSET[1] * (separation_id + 1)
		rotation_group = COLLIDER_SEPARATIONS[separation_id]
		collider_id = COLLIDER_OFFSET + (k // SEPARATIONS) * DEPTH + i
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
	pos = (TRIGGER_POS[0] + k * (DEPTH + COLOR_COUNT + 3) * 30, TRIGGER_POS[1])
	min_collider = COLLIDER_OFFSET + (k // SEPARATIONS) * DEPTH
	separation_id = k % SEPARATIONS
	# separation_id = floor(k / WIDTH * SEPARATIONS)
	# first_separation_k = ceil(separation_id * WIDTH / SEPARATIONS)
	# min_collider = COLLIDER_OFFSET + (k - first_separation_k) * DEPTH
	wall_id = WALL_COLLIDERS[separation_id]

	depth_layer_id = floor(k / WIDTH * DEPTH_LAYERS)
	next_depth_layer_id = floor((k+1) / WIDTH * DEPTH_LAYERS)

	objects = []

	# Depth fail logic and initial toggle
	# fail_collider_id = DEPTH_FAIL_COLLIDERS[k % SEPARATIONS]
	fail_collider_id = DEPTH_FAIL_COLLIDERS[separation_id]

	for j in range(TOTAL_BINARY_COUNT):
		group = min_group + j
		(x, y) = (pos[0] - 60 , pos[1] - j * 30)

		# trigger = Object(id=1, x=x, y=y, groups={3}, scale=0.75, color_1 = 3)

		trigger = Object(id=1815, x=x, y=y, groups={3},
			target_group_id=group, item_id=fail_collider_id, block_b_id=min_collider, activate_group=False,
			spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=0.75)
		objects.append(trigger)

		toggle = Object(id=1049, x=x+30, y=y, groups={3},
			target_group_id=group, spawn_triggered=True, multi_trigger=True, is_active_trigger=True)
		objects.append(toggle)


	# Normal rendering
	for i in range(DEPTH):
		groups_on = get_groups(i, min_group)
		collider_id = min_collider + i
	
		for j in range(TOTAL_BINARY_COUNT):
			group = min_group + j
			is_on = group in groups_on
			(x, y) = (pos[0] + 30 * i , pos[1] - j * 30)
			# trigger = Object(id=1, x=x, y=y, groups={3}, scale=0.75)
			trigger = Object(id=1815, x=x, y=y, groups={3},
				target_group_id=group, item_id=wall_id, block_b_id=collider_id, activate_group=is_on,
				spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=0.75)
			if not is_on:
				trigger.color_1 = 3
			else:
				trigger.color_1 = 3
				trigger.color_1_hsv_enabled = True
				trigger.color_1_hsv_values = HSV(h=120, s=1, v=1)
			objects.append(trigger)

			if i == DEPTH - 1 and (depth_layer_id != next_depth_layer_id or k == WIDTH):
				trigger = Object(id=1815, x=x, y=y-30, groups={3},
					target_group_id=DEPTH_LAYER_GROUPS[depth_layer_id],
					item_id=fail_collider_id, block_b_id=collider_id,
					spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=0.75)
				objects.append(trigger)

# Object(id=1049, x=225, y=195, groups={2},
# spawn_triggered=True, multi_trigger=True, is_active_trigger=True, target_group_id=6)

	# Color logic
	pulse_groups = [min_group + TOTAL_BINARY_COUNT + c for c in range(COLOR_COUNT)]
	prev_depth_layer_id = (depth_layer_id - 2) % DEPTH_LAYERS
	prev_depth_layer_group = DEPTH_LAYER_GROUPS[prev_depth_layer_id]

	coloring_group = min_group + TOTAL_BINARY_COUNT + COLOR_COUNT

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

		objects.append(trigger)
		# objects.append(pulse)

	objects += toggle_triggers

	(x, y) = (pos[0] - 60, pos[1] - 4 * 30)
	toggle_on = Object(id=1049, x=x, y=y, groups={prev_depth_layer_group}, activate_group=True,
			target_group_id=coloring_group, spawn_triggered=True, multi_trigger=True, is_active_trigger=True)
	objects.append(toggle_on)

	# toggle_off = Object(id=1049, x=x - 30, y=y, groups=set(pulse_groups),
	# 		target_group_id=coloring_group, spawn_triggered=True, multi_trigger=True, is_active_trigger=True)
	# objects.append(toggle_off)


	return objects

# Get all of the colliders that are used to render the textures
def get_color_colliders(pos, k):
	max_width = 2 * DEPTH_DISTANCE * tan(radians(HFoV) / 2)
	angle = atan((max_width * (k / (WIDTH - 1) - .5)) / DEPTH_DISTANCE)

	depths = get_depths()

	objects = []
	for i in range(DEPTH - 1, -1, -1):
		x_i = depths[i]

		depth_layer_id = (floor(k / WIDTH * DEPTH_LAYERS)) % DEPTH_LAYERS
		depth_layer_group = DEPTH_LAYER_GROUPS[depth_layer_id]

		min_scale = 8
		if i < DEPTH - 1:
			min_scale = min(min_scale, x_i - depths[i+1])
		if i > 0:
			min_scale = min(min_scale, depths[i-1] - x_i)

		horiz_width = max_width * x_i / DEPTH_DISTANCE
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
		x += SEPARATION_OFFSET[0] * separation_id		
		y += SEPARATION_OFFSET[1] * separation_id
		rotation_group = COLLIDER_SEPARATIONS[SEPARATIONS]
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

	if DEPTH_DISTANCE - min_depth < min_depth_step * (DEPTH - 1):
		raise Exception("Depth cannot fit the colliders. Increase depth distance or decrease collider count.")

	excess_step = (DEPTH_DISTANCE - min_depth) / (DEPTH - 1) - min_depth_step
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
		digit = b_flipped[i]
		if digit == 0 and i < BINARY_ZERO_GROUPS_COUNT:
				groups.append(min_group + BINARY_GROUPS_COUNT + i)
		elif digit == 1:
			groups.append(min_group + i)


	return groups



if __name__ == "__main__":
	arguments = sys.argv

	editor, db, local_levels = load_editor()

	
	if len(arguments) < 2 or arguments[1] != 'void':
		# This ensures that there
		separations_needed = SEPARATIONS + 1 - len(ROTATION_CENTERS)
		if separations_needed > 0:
			print("{} more separations needed!".format(separations_needed))
			quit()
		add_objects(editor, cerate_separation_maps(editor.get_objects()))
		add_objects(editor, get_screen())

	save_changes(editor, db, local_levels)

# Object(id=1006, x=165, y=165, groups={3}, spawn_triggered=True, multi_trigger=True,
# is_active_trigger=True, target_group_id=10, hold_time=1, pulse_mode=<PulseMode.HSV:1>,
# exclusive=True, copied_color_id=2)