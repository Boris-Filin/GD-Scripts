from MagnumOpus import *
from math import *
from TunnelObjects import get_line
import sys
import copy

# Various default variables
GROUP_OFFSET = 200
COLLIDER_OFFSET = 100
COLOR_OFFSET = 30
WALL_COLLIDER = 1

# This defines the de-facto resolution of the screen
WIDTH = 60
DEPTH = 32

# Some important constants derived from depth 
DEPTH_LOG = math.ceil(math.log(DEPTH, 2))
DEPTH_LOG_POW = 2 ** DEPTH_LOG
GROUPS_PER_STRIP = DEPTH_LOG * 2 - 1
# The two will be different in the future
BINARY_GROUPS_COUNT = DEPTH_LOG * 2 - 1 

# Stuff necessary to define the rendering behaviour
HFoV = 90
VFoV = 60
NEAR_CLIPPING_PLANE = 0.1
DEPTH_DISTANCE = 15

# Visual line variables
LINE_WIDTH = 0.25
LINE_HEIGHT = 9
MIN_V = 0.5

# Separations are necessary to bypass the 1k collider IDs limit
SEPARATIONS = 6
WALL_COLLIDERS = [1, 51, 53, 55, 57, 59]
DEPTH_FAIL_COLLIDERS = [50, 52, 54, 56, 58, 60]
ROTATION_CENTERS = [20, 102, 104, 106, 108, 110]
COLLIDER_SEPARATIONS = [100, 101, 103, 105, 107, 109]
SEPARATION_OFFSET = (0, 1800)

# Variables that determine the texturing
TARGET_COLORS = []
COLOR_COLLIDERS = [[]]

# Various position variables
SCREEN_POS = (300, 150)
CAMERA_POS = (2325, 1125)
TRIGGER_POS = (315, 8265)
TEXTURE_TRIGGER_POS = (315, 5265)


# Duplicate the map for the separation colliders
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


# Get all the individual lines for a specific strip
def get_lines(pos, k, min_group):
	pos = SCREEN_POS
	x_offset = (- WIDTH / 2 + k) * LINE_WIDTH * 30 + LINE_WIDTH / 2
	y_offset = 0

	depths = get_depths()

	objects = []
	# Iterating from farthest to closest
	for i in range(DEPTH):
		groups = get_groups(i, min_group)

		dist_to_camera = DEPTH - i - 1

		height = min(1, 1 / (tan(radians(VFoV / 2)) * depths[i])) * LINE_HEIGHT * 30
		(x, y) = (pos[0] + x_offset, pos[1] + y_offset)
		line = get_line((x, y - height/2), (x, y + height/2), LINE_WIDTH * 30)
		# line = get_line((x, y - height/2), (x, y - height/2 + LINE_WIDTH * 30), LINE_WIDTH * 30)
		for obj in line:
			obj.color_1 = 4
			obj.color_1_hsv_enabled = True
			obj.color_1_hsv_values = HSV(h=0, s=1, v=(1 - (dist_to_camera / (DEPTH - 1)) * (1 - MIN_V)))
			obj.z_order = i

			obj.groups = set(groups)
			obj.groups.add(1)
		objects += line

	return objects


# Get all of the colliders in the right order
def get_colliders(pos, k):
	max_width = 2 * DEPTH_DISTANCE * tan(radians(HFoV) / 2)
	angle = atan((max_width * (k / (WIDTH - 1) - .5)) / DEPTH_DISTANCE)

	depths = get_depths()

	objects = []
	for i in range(DEPTH):
		x_i = depths[i]

		min_scale = 8
		if i < DEPTH - 1:
			min_scale = min(min_scale, x_i - depths[i+1])
		if i > 0:
			min_scale = min(min_scale, depths[i-1] - x_i)

		horiz_width = max_width * x_i / DEPTH_DISTANCE
		min_scale = min(horiz_width / (WIDTH - 1), min_scale)


		min_scale *= 0.7
		min_scale = floor(min_scale * 100) / 100
		min_scale = max(min_scale, 0.01)

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
			is_active_trigger=True, dynamic_block=True, groups={2, 14, 17, rotation_group}))

		# Depth fail colliders
		if i == 0:
			fail_collider_id = DEPTH_FAIL_COLLIDERS[separation_id]
			objects.append(Object(id=1816, x=x, y=y, item_id=fail_collider_id, scale=min_scale,
				is_active_trigger=True, groups={2, 14, 17, rotation_group}))

	# quit()
	return objects


# Get the triggers (logic) that govern the rendering of the 3D scene
def get_triggers(min_group, k):
	pos = (TRIGGER_POS[0] + k * (WIDTH / SEPARATIONS + 5) * 30, TRIGGER_POS[1])
	min_collider = COLLIDER_OFFSET + (k // SEPARATIONS) * DEPTH
	wall_id = WALL_COLLIDERS[k % SEPARATIONS]

	objects = []

	# Depth fail logic
	fail_collider_id = DEPTH_FAIL_COLLIDERS[k % SEPARATIONS]

	for j in range(BINARY_GROUPS_COUNT):
		group = min_group + j
		(x, y) = (pos[0] - 30 * 2 , pos[1] - j * 30)

		# trigger = Object(id=1, x=x, y=y, groups={3}, scale=0.75, color_1 = 3)

		trigger = Object(id=1815, x=x%1000, y=y, groups={3},
			target_group_id=group, item_id=fail_collider_id, block_b_id=min_collider, activate_group=False,
			spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=0)
		objects.append(trigger)

	# Normal rendering
	for i in range(DEPTH):
		groups_on = get_groups(i, min_group)
		collider_id = min_collider + i
	
		for j in range(BINARY_GROUPS_COUNT):
			group = min_group + j
			is_on = group in groups_on
			(x, y) = (pos[0] + 30 * i , pos[1] - j * 30)
			# trigger = Object(id=1, x=x, y=y, groups={3}, scale=0)
			trigger = Object(id=1815, x=x%1000, y=y, groups={3},
				target_group_id=group, item_id=wall_id, block_b_id=collider_id, activate_group=is_on,
				spawn_triggered=True, multi_trigger=True, is_active_trigger=True, scale=0)
			if not is_on:
				trigger.color_1 = 3
				# obj.color_1_hsv_enabled = True
				# obj.color_1_hsv_values = HSV(h=0, s=1, v=(1 - (i / (DEPTH - 1)) * (1 - MIN_V)))
			objects.append(trigger)

	return objects


# Get all of the objects for a specific strip on the screen
def get_strip(pos, k):
	objects = []
	min_group = GROUP_OFFSET + k * GROUPS_PER_STRIP
	objects += get_lines(pos, k, min_group)
	objects += get_colliders(CAMERA_POS, k)
	objects += get_triggers(min_group, k)
	return objects


# Get all of the rendering objects (visual, physical, logic)
def get_screen():
	# Some strip setup stuff
	objects = []
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
		if i == bin_length - 1 and digit == 0:
			continue
		group = min_group + 2 * i + (1 - digit)
		groups.append(group)

	return groups



if __name__ == "__main__":
	arguments = sys.argv

	editor, db, local_levels = load_editor()

	
	if len(arguments) < 2 or arguments[1] != 'void':
		add_objects(editor, cerate_separation_maps(editor.get_objects()))
		add_objects(editor, get_screen())

	save_changes(editor, db, local_levels)

# Object(id=1006, x=165, y=165, groups={3}, spawn_triggered=True, multi_trigger=True,
# is_active_trigger=True, target_group_id=10, hold_time=1, pulse_mode=<PulseMode.HSV:1>,
# exclusive=True, copied_color_id=2)