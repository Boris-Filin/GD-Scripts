from math import (
	cos, sin, tan,
	radians, degrees, pi,
	sqrt, floor, ceil, atan
)

from gd.api import (
	ColorCollection,
	ColorChannel,
	Editor,
	Object,
	HSV
)

import copy





# All perfect rectangles in the game
# Presented in the form
# ID: (width, height)
# Ordered from highest to lowest aspect ratio
rectangles = {
	1753: (30, 1),  # line
	1757: (15, 1),  # 1/2 line
	579: (30, 10),  # 3D slab
	1767: (8, 3),  # Dash
	580: (15, 10),  # 3D 1/2 slab
	211: (30, 30)  # Block
}


def get_corner(angle, width):
	objects = []
	id_ = 584 if angle <= 90 else 580

	horiz = Object(id=id_, x=7.5, y=5)
	x = sin(radians(angle)) * 5 + cos(radians(angle)) * 7.5
	y = -cos(radians(angle)) * 5 + sin(radians(angle)) * 7.5
	vert = Object(id=id_, x=x, y=y, v_flipped=True, rotation=(-angle))
	objects = [horiz, vert]

	scale = width / 10
	for obj in objects:
		obj.x *= scale
		obj.y *= scale
		obj.scale = scale
	
	return objects

# This thing is insane
def get_line_origin(point, line_width, leeway=(0, 0)):
	for id_ in rectangles.keys():
		objects = attempt_line_origin(id_, point, line_width, leeway)
		if objects != None:
			return objects
	for id_ in list(rectangles.keys())[::-1]:
		objects = attempt_line_origin(id_, point, line_width, leeway, True)
		if objects != None:
			return objects


	raise Exception("line aspect ration LT 1, I was too lazy to implement it")


def attempt_line_origin(id_, point, line_width, leeway, flipped=False):
	objects = []

	dim = rectangles[id_]
	if flipped:
		dim = dim[::-1]
	scale = (line_width / dim[1])
	scaled_width = scale * dim[0]

	length = sqrt(point[0] ** 2 + point[1] ** 2)
	max_length = leeway[0] + length + leeway[1]

	if scaled_width > max_length:
		return None

	if point[0] == 0:
		angle = radians(90) if point[1] > 0 else radians(-90)
	else:
		angle = atan(point[1] / point[0])

	# direction = (cos(angle), sin(angle))
	direction = (point[0] / length, point[1] / length)

	# num_segments = floor(max_length / scaled_width)
	num_segments = ceil(length / scaled_width)
	res_length = scaled_width * num_segments
	end_segment = False
	start_offset = 0
	if res_length > max_length:
		num_segments -= 1
		end_segment = True
	# if res_length < length:
		# end_segment = True
	# 	start_offset = 0
	elif res_length >= length + leeway[0]:
		start_offset = -leeway[0]
	else:
		start_offset = length - res_length

	offset_fac = scaled_width / 2 + start_offset
	offset = (direction[0] * offset_fac, direction[1] * offset_fac)

	flipped_rot = 90 if flipped else 0

	for i in range(num_segments):
		x = offset[0] + direction[0] * scaled_width * i
		y = offset[1] + direction[1] * scaled_width * i

		obj_ = Object(id=id_, x=x, y=y, scale=scale, rotation=(-degrees(angle) + flipped_rot))
		objects.append(obj_)
		if start_offset + scaled_width * i > length:
			break

	if end_segment:
		x = point[0] - direction[0] * scaled_width / 2
		y = point[1] - direction[1] * scaled_width / 2

		obj_ = Object(id=id_, x=x, y=y, scale=scale, rotation=(-degrees(angle) + flipped_rot))
		objects.append(obj_)

	return objects

def get_line(a, b, width, leeway=(0,0)):
	line = get_line_origin(sub(b, a), width, leeway)
	move(line, a)
	return line

def get_trapezium_outline(point, base, top, width):
	a = (0, 0)
	b = point
	c = (b[0] + top, b[1])
	d = (base, 0)

	angleA = degrees(atan(b[1] / b[0]))
	angleB = 180 - angleA
	angleD = degrees(atan(c[1] / (d[0] - c[0])))
	angleC = 180 - angleD

	cornerA = get_corner(angleA, width)

	cornerB = get_corner(angleB, width)
	flip(cornerB, True)
	move(cornerB, b)

	cornerC = get_corner(angleC, width)
	flip(cornerC)
	flip(cornerC, True)
	move(cornerC, c)

	cornerD = get_corner(angleD, width)
	flip(cornerD)
	move(cornerD, d)

	corners = cornerA + cornerB + cornerC + cornerD


	cornerScale = width / 10
	leeway = (5 * cornerScale, 5 * cornerScale)

	abStart = mul(rotateVector((5, 15), 90 - angleA), cornerScale)
	abEnd = add(b, mul(rotateVector((-5, 15), 90 + angleB), cornerScale))
	lineAB = get_line(abStart, abEnd, width, leeway)

	bcStart = add(b, mul(rotateVector((5, 15), 90), cornerScale))
	bcEnd = add(c, mul(rotateVector((-5, 15), -90), cornerScale))
	lineBC = get_line(bcStart, bcEnd, width, leeway)

	adStart = mul(rotateVector((-5, 15), 90), cornerScale)
	adEnd = add(d, mul(rotateVector((5, 15), -90), cornerScale))
	lineAD = get_line(adStart, adEnd, width, leeway)

	cdStart = add(c, mul(rotateVector((5, 15), 270 - angleC), cornerScale))
	cdEnd = add(d, mul(rotateVector((-5, 15), angleD - 90), cornerScale))
	lineCD = get_line(cdStart, cdEnd, width, leeway)

	lines = lineAB + lineBC + lineAD + lineCD


	objects = corners + lines

	return objects

def get_filling_corner(point):
	defaultLength = 2 * 30

	angle = degrees(atan(point[0] / point[1]))
	resAngle = 90 + angle
	scale = sqrt(point[0] ** 2 + point[1] ** 2) / defaultLength
	(x, y) = add(point, mul(rotateVector((15, -30), angle), scale))
	slope = Object(id=694, x=x, y=y, scale=scale, h_flipped=True, rotation=resAngle)


	scale_under = point[0] / 30 * 1.05
	if angle >= degrees(atan(1/2)):
		(x_under, y_under) = mul((15, 15), scale_under)
		under_slope = Object(id=693, x=x_under, y=y_under, scale=scale_under)
	else:
		(x_under, y_under) = mul((15, 30), scale_under)
		under_slope = Object(id=694, x=x_under, y=y_under, scale=scale_under, h_flipped=True, rotation=-90)

	objects = [slope, under_slope]
	return objects


def get_trapezium_filling(point, base, top):
	rectangle = get_line((point[0], point[1] / 2), (point[0] + top, point[1] / 2), point[1])
	left_corner = get_filling_corner(point)

	right_corner = get_filling_corner((base - point[0] - top, point[1]))
	flip(right_corner)
	move(right_corner, (base, 0))

	objects = {
		"center": rectangle,
		"left": left_corner,
		"right": right_corner
	}
	return objects


def get_tile(a, b, base, line_width):
	top = base - 2 * (b[0] - a[0])
	side = sub(b, a)
	# # outline = get_trapezium_outline(side, base, top, line_width)
	# # move(outline, a)
	# outline = get_trapezium_filling(side, base, top)
	# move(outline, a)



	angle = atan(side[1] / side[0])
	filling_inset_y = line_width / 2
	# filling_inset_y = line_width
	filling_inset_x1 = filling_inset_y / tan(angle / 2)
	filling_inset_x2 = filling_inset_y / tan((pi - angle) / 2)
	a_inset = (filling_inset_x1, filling_inset_y)
	b_inset = add(side, (filling_inset_x2, - filling_inset_y))
	base_inset = base - 2 * filling_inset_x1
	top_inset = top - 2 * filling_inset_x2

	a_outset = (-filling_inset_x1, -filling_inset_y)
	b_outset = add(side, (- filling_inset_x2, filling_inset_y))
	base_outset = base + 2 * filling_inset_x1
	top_outset = top + 2 * filling_inset_x2

	outline = get_trapezium_filling(sub(b_outset, a_outset), base_outset, top_outset)
	move(outline["center"], add(a, a_outset))
	move(outline["right"], add(a, a_outset))
	move(outline["left"], add(a, a_outset))
	
	filling = get_trapezium_filling(sub(b_inset, a_inset), base_inset, top_inset)
	move(filling["center"], add(a, a_inset))
	move(filling["right"], add(a, a_inset))
	move(filling["left"], add(a, a_inset))

	for obj_ in flatten(outline.values()):
		obj_.color_1 = 2
		obj_.z_layer = 1
		obj_.editor_layer_1 = 2

	for obj_ in flatten(filling.values()):
		obj_.color_1 = 1
		obj_.z_layer = 3
		obj_.editor_layer_1 = 3

	objects = {
		"center": filling["center"] + outline["center"],
		"left": filling["left"] + outline["left"],
		"right": filling["right"] + outline["right"]
	}
	return objects

def get_follow_triggers(min_custom_group, heights, divisions, segments):
	pos = (1515, 1515)
	follow_group = 11
	angle = pi * 2 / divisions

	offsets = []
	for i in range(segments):
		y = heights[i + 1] - heights[i]
		x = y * tan(angle / 2)
		offsets.append((x, y))

	objects = []
	for i in range(segments):
		target_offset = offsets[i]
		min_group = min_custom_group + i * divisions

		for j in range(divisions):
			offset = rotateVector(target_offset, -degrees(angle * j))
			# offset = mul(offset, 1/30)
			(x, y) = add(pos, (30 * i, -30 * j))
			group = min_group + j

			objects.append(Object(id=901, x=x, y=y, groups={13}, z_order=2, z_layer=5, spawn_triggered=True, multi_trigger=True, is_active_trigger=True,
				target_group_id=group, move_x=offset[0], move_y=offset[1], duration=1))
			objects.append(Object(id=901, x=x + 450, y=y, groups={14}, z_order=2, z_layer=5, spawn_triggered=True, multi_trigger=True, is_active_trigger=True,
				target_group_id=group, move_x=-offset[0], move_y=-offset[1], duration=0))
			# objects.append(Object(id=1347, x=x, y=y, groups={3}, spawn_triggered=True, multi_trigger=True, is_active_trigger=True,
			# 	target_group_id=group, follow_target_pos_center_id=follow_group, duration=9999, x_mod=offset[0], y_mod=offset[1]))
	return objects


def get_tunnel(pos, width=22, divisions=8, segments=10):
	i_offset = 1.5
	angle = pi * 2 / divisions
	radius = width / 2 * 30 * i_offset
	objects = []
	fac = 1.05
	min_custom_group = 200

	heights = [radius / (i_offset + i) for i in range(segments + 1)]

	heights = [radius - (radius - h) * fac for h in heights]

	for i in range(segments):
		far = heights[i]
		near = heights[i + 1]

		min_group = min_custom_group + i * divisions
		prev_segment_group = min_group - divisions

		base = 2 * far * tan(angle / 2)
		top = 2 * near * tan(angle / 2)
		a = (-base / 2, -far)
		b = (-top / 2, -near)

		tile = get_tile(a, b, base, 3)
		# tile = tile["center"] + tile["left"] + tile["right"]

		for j in range(divisions):
			# tile_clone = clone(tile)
			tile_objects = []
			tile_objects += add_group(clone(tile["left"]), min_group + j)
			tile_objects += add_group(clone(tile["center"]), min_group + j)

			tile_objects += add_group(clone(tile["center"]), min_group + (j + 1) % divisions)
			tile_objects += add_group(clone(tile["right"]), min_group + (j + 1) % divisions)

			if i > 0:
				tile_objects += add_group(clone(tile["left"]), prev_segment_group + j)
				tile_objects += add_group(clone(tile["center"]), prev_segment_group + j)

				tile_objects += add_group(clone(tile["center"]), prev_segment_group + (j + 1) % divisions)
				tile_objects += add_group(clone(tile["right"]), prev_segment_group + (j + 1) % divisions)

			for obj_ in tile_objects:
				obj_.editor_layer_1 = 10 + i * divisions + j

			objects += rotate(tile_objects, -degrees(angle * j))
			
	move(objects, pos)

	objects += get_follow_triggers(min_custom_group, heights, divisions, segments)

	return objects


def move(objects, offset):
	for obj in objects:
		obj.x += offset[0]
		obj.y += offset[1]
	return objects

def flip(objects, vert=False):
	for obj in objects:
		if not vert:
			obj.h_flipped = not obj.h_flipped
			obj.x = - obj.x
		else:
			obj.v_flipped = not obj.v_flipped
			obj.y = - obj.y
		if obj.rotation != None:
			obj.rotation = - obj.rotation
	return objects

def rotate(objects, angle):
	for obj in objects:
		if obj.rotation == None:
			obj.rotation = angle
		else:
			obj.rotation += angle
		(obj.x, obj.y) = rotateVector((obj.x, obj.y), angle)
	return objects

def rotateAround(objects, pos, angle):
	for obj in objects:
		obj.x -= pos[0]
		obj.y -= pos[1]
	rotate(objects, angle)
	for obj in objects:
		obj.x += pos[0]
		obj.y += pos[1]
	return objects

def clone(objects):
	return copy.deepcopy(objects)

def add(a, b):
	return (a[0] + b[0], a[1] + b[1])

def sub(a, b):
	return (a[0] - b[0], a[1] - b[1])

def mul(v, k):
	return (v[0] * k, v[1] * k)

# Rotation in degrees clockwise
def rotateVector(v, angle):
	rad = radians(angle)
	x =  cos(rad) * v[0] + sin(rad) * v[1]
	y = -sin(rad) * v[0] + cos(rad) * v[1]
	return (x, y)

def flatten(l):
	res = []
	for el in l:
		res += el
	return res

def add_group(objects, group):
	for obj in objects:
		if(obj.groups == None):
			obj.groups = set()
		obj.groups.add(group)
	return objects