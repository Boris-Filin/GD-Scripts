from gd.api import (
	Editor,
	Object,
	HSV
)

class Strip():
	width = 7.5
	height = 300
	groups_per_strip = 3
	colors_per_strip = 4

	upper_quarter = [
		# Main rectangles
		Object(id=1757, x=5, y=112.5, editor_layer_1=11, z_order=-1, rotation=-90, color_1=2, z_layer=3, scale=5),
		Object(id=1757, x=2.5, y=112.5, editor_layer_1=11, z_order=-1, rotation=-90, color_1=2, z_layer=3, scale=5),
		# Squares
		Object(id=917, x=3.75, y=146.25, editor_layer_1=11, z_order=3, color_1=1, z_layer=3),
		Object(id=917, x=3.75, y=138.75, editor_layer_1=11, z_order=3, color_1=1, z_layer=3),
		# Line effect
		Object(id=580, x=3.75, y=129.375, editor_layer_1=11, groups={2}, z_order=4, rotation=90, color_1=2, z_layer=3, scale=0.75),

		# Shading
		Object(id=1754, x=0.94, y=121.875, editor_layer_1=15,
			z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.88,
			color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
		Object(id=1754, x=2.815, y=121.8755, editor_layer_1=15,
			z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.87,
			color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
		Object(id=1754, x=4.685, y=121.8755, editor_layer_1=15,
			z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.87,
			color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
		Object(id=1754, x=6.56, y=121.875, editor_layer_1=15,
			z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.88,
			color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
	]

	upper_middle_quarter = [
		# Main rectangles
		Object(id=1757, x=2.5, y=37.5, editor_layer_1=12, z_order=1, rotation=-90, color_1=3, z_layer=3, scale=5),
		Object(id=1757, x=5, y=37.5, editor_layer_1=12, z_order=1, rotation=-90, color_1=3, z_layer=3, scale=5),
		# Line effect
		Object(id=580, x=3.75, y=69.375, h_flipped=True, editor_layer_1=12, z_order=2, rotation=90, color_1=2, z_layer=3, scale=0.75),
		Object(id=580, x=3.75, y=63.125, h_flipped=True, editor_layer_1=12, z_order=4, rotation=90, color_1=2, z_layer=3, scale=0.75),
		# Squares
		Object(id=917, x=3.75, y=53.75, editor_layer_1=12, groups={2}, z_order=3, color_1=1, z_layer=3),
		Object(id=917, x=3.75, y=46.25, editor_layer_1=12, groups={2}, z_order=3, color_1=1, z_layer=3),
	]

	lower_middle_quarter = [
		# Main rectangles
		Object(id=1757, x=5, y=-37.5, editor_layer_1=13, z_order=1, rotation=-90, color_1=3, z_layer=3, scale=5),
		Object(id=1757, x=2.5, y=-37.5, editor_layer_1=13, z_order=1, rotation=-90, color_1=3, z_layer=3, scale=5),
		# Line effect
		Object(id=580, x=3.75, y=-63.125, editor_layer_1=13, z_order=4, rotation=90, color_1=4, z_layer=3, scale=0.75),
		Object(id=580, x=3.75, y=-69.375, editor_layer_1=13, z_order=2, rotation=90, color_1=4, z_layer=3, scale=0.75),
		# Square
		Object(id=917, x=3.75, y=-53.75, editor_layer_1=13, groups={1}, z_order=3, color_1=1, z_layer=3),
		Object(id=917, x=3.75, y=-46.25, editor_layer_1=13, groups={1}, z_order=3, color_1=1, z_layer=3),
	]

	lower_quarter = [
		# Main rectangles
		Object(id=1757, x=2.5, y=-112.5, h_flipped=True, editor_layer_1=14, z_order=-1, rotation=-90, color_1=4, z_layer=3, scale=5),
		Object(id=1757, x=5, y=-112.5, h_flipped=True, editor_layer_1=14, z_order=-1, rotation=-90, color_1=4, z_layer=3, scale=5),
		# Squares
		Object(id=917, x=3.75, y=-146.25, v_flipped=True, editor_layer_1=14, z_order=3, color_1=1, z_layer=3),
		Object(id=917, x=3.75, y=-138.75, v_flipped=True, editor_layer_1=14, z_order=3, color_1=1, z_layer=3),
		# Line effect
		Object(id=580, x=3.75, y=-129.375, h_flipped=True, editor_layer_1=14, groups={1},
			z_order=4, rotation=90, color_1=4, z_layer=3, scale=0.75),

		# Shading
		Object(id=1754, x=0.94, y=-121.875, editor_layer_1=15,
			z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.88,
			color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
		Object(id=1754, x=2.815, y=-121.8755, editor_layer_1=15,
			z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.87,
			color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
		Object(id=1754, x=4.685, y=-121.8755, editor_layer_1=15,
			z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.87,
			color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
		Object(id=1754, x=6.56, y=-121.875, editor_layer_1=15,
			z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.88,
			color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0))
	]



	def __init__(self, offset, base_groups, group_offset, line_group_1, color_offset=10, shadow_color=11):
		self.objects = []
		upper_groups = base_groups.union({group_offset, group_offset + 1})
		upper_middle_groups = base_groups.union({group_offset, group_offset + 1, group_offset + 2})
		lower_middle_groups = base_groups.union({group_offset})
		lower_groups = base_groups.union({group_offset, group_offset + 2})
		print(line_group_1)

		self.add_objects_from_quarter(self.upper_quarter, upper_groups, line_group_1)
		self.add_objects_from_quarter(self.upper_middle_quarter, upper_middle_groups, line_group_1)
		self.add_objects_from_quarter(self.lower_middle_quarter, lower_middle_groups, line_group_1)
		self.add_objects_from_quarter(self.lower_quarter, lower_groups, line_group_1)

		# for obj in self.upper_quarter:
		# 	obj.groups = upper_groups
		# 	self.objects.append(obj.copy())


		# for obj in self.upper_middle_quarter:
		# 	obj.groups = upper_middle_groups
		# 	self.objects.append(obj.copy())


		# for obj in self.lower_middle_quarter:
		# 	obj.groups = lower_middle_groups
		# 	self.objects.append(obj.copy())


		# for obj in self.lower_quarter:
		# 	obj.groups = lower_groups
		# 	self.objects.append(obj.copy())


		for obj in self.objects:
			if obj.editor_layer_1 != 15:
				obj.color_1 += color_offset - 1
				# obj.scale = 1.01 if not obj.scale else obj.scale * 1.01
			else:
				obj.color_1 = shadow_color
			obj.x += offset[0]
			obj.y += offset[1]
			obj.do_not_fade = True
			obj.do_not_enter = True

	def add_objects_from_quarter(self, quarter, groups, line_group_1):
		for obj in quarter:
			new_obj = obj.copy()
			line_group_offset = 0
			if new_obj.groups != None and len(new_obj.groups) > 0:
				line_group_offset = list(new_obj.groups)[0]
			new_obj.groups = groups.copy()
			if line_group_offset > 0:
				print(" >", line_group_1 + line_group_offset - 1)
				new_obj.groups.add(line_group_1 + line_group_offset - 1)
			self.objects.append(new_obj)


	def get_objects(self):
		return self.objects




# Object(id=1754, x=15, y=45, color_1=1, color_1_hsv_enabled=True, color_1_hsv_values=<HSV, h=0, s=1, v=0, s_checked=False, v_checked=False>)



	# upper_quarter = [
	# 	# Main rectangles
	# 	Object(id=1757, x=2.5, y=112.5, editor_layer_1=11, z_order=1, rotation=-90, color_1=2, z_layer=3, scale=5),
	# 	Object(id=1757, x=5, y=112.5, editor_layer_1=11, z_order=1, rotation=-90, color_1=2, z_layer=3, scale=5),
	# 	# Square
	# 	Object(id=917, x=3.75, y=146.25, editor_layer_1=11, z_order=4, color_1=1),
	# 	# Shading
	# 	Object(id=1754, x=0.94, y=121.875, editor_layer_1=15,
	# 		z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.88,
	# 		color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
	# 	Object(id=1754, x=2.815, y=121.8755, editor_layer_1=15,
	# 		z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.87,
	# 		color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
	# 	Object(id=1754, x=4.685, y=121.8755, editor_layer_1=15,
	# 		z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.87,
	# 		color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
	# 	Object(id=1754, x=6.56, y=121.875, editor_layer_1=15,
	# 		z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.88,
	# 		color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0))
	# ]

	# upper_middle_quarter = [
	# 	# Main rectangles
	# 	Object(id=1757, x=2.5, y=37.5, editor_layer_1=12, z_order=2, rotation=-90, color_1=3, z_layer=3, scale=5),
	# 	Object(id=1757, x=5, y=37.5, editor_layer_1=12, z_order=2, rotation=-90, color_1=3, z_layer=3, scale=5),
	# 	# 2/3 rectangle
	# 	Object(id=579, x=3.75, y=63.75, editor_layer_1=12, z_order=3, rotation=-90, color_1=2, z_layer=3, scale=0.75),
	# 	# Square
	# 	Object(id=917, x=3.75, y=53.75, editor_layer_1=12, z_order=4, color_1=1)
	# ]

	# lower_middle_quarter = [
	# 	# Main rectangles
	# 	Object(id=1757, x=2.5, y=-37.5, editor_layer_1=13, z_order=2, rotation=-90, color_1=3, z_layer=3, scale=5),
	# 	Object(id=1757, x=5, y=-37.5, editor_layer_1=13, z_order=2, rotation=-90, color_1=3, z_layer=3, scale=5),
	# 	# 2/3 rectangle
	# 	Object(id=579, x=3.75, y=-63.75, editor_layer_1=13, z_order=3, rotation=-90, color_1=4, z_layer=3, scale=0.75),
	# 	# Square
	# 	Object(id=917, x=3.75, y=-53.75, editor_layer_1=13, z_order=4, color_1=1)
	# ]

	# lower_quarter = [
	# 	# Main rectangles
	# 	Object(id=1757, x=2.5, y=-112.5, editor_layer_1=14, z_order=1, rotation=-90, color_1=4, z_layer=3, scale=5),
	# 	Object(id=1757, x=5, y=-112.5, editor_layer_1=14, z_order=1, rotation=-90, color_1=4, z_layer=3, scale=5),
	# 	# Square
	# 	Object(id=917, x=3.75, y=-146.25, editor_layer_1=14, z_order=4, color_1=1),
	# 	# Shading
	# 	Object(id=1754, x=0.94, y=-121.875, editor_layer_1=15,
	# 		z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.88,
	# 		color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
	# 	Object(id=1754, x=2.815, y=-121.8755, editor_layer_1=15,
	# 		z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.87,
	# 		color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
	# 	Object(id=1754, x=4.685, y=-121.8755, editor_layer_1=15,
	# 		z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.87,
	# 		color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0)),
	# 	Object(id=1754, x=6.56, y=-121.875, editor_layer_1=15,
	# 		z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.88,
	# 		color_1_hsv_enabled=True, color_1_hsv_values=HSV(h=0, s=1, v=0))
	# ]



	# upper_quarter_old = [
	# 	# Main rectangles
	# 	Object(id=1191, x=15, y=105, editor_layer_1=11,
	# 		z_order=1, rotation=-90, color_1=2, z_layer=3),
	# 	Object(id=1191, x=15, y=75, editor_layer_1=11,
	# 		z_order=1, rotation=-90, color_1=2, z_layer=3),
	# 	# Square
	# 	Object(id=917, x=3.75, y=116.25, editor_layer_1=11,
	# 		z_order=4, color_1=1, z_layer=3),
	# 	# Shading
	# 	Object(id=1754, x=0.94, y=91.875, editor_layer_1=15,
	# 		z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.88),
	# 	Object(id=1754, x=2.815, y=91.875, editor_layer_1=15,
	# 		z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.87),
	# 	Object(id=1754, x=4.685, y=91.875, editor_layer_1=15,
	# 		z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.87),
	# 	Object(id=1754, x=6.56, y=91.875, editor_layer_1=15,
	# 		z_order=5, rotation=90, color_1=4, z_layer=3, scale=1.88)
	# ]

	# upper_middle_quarter_old = [
	# 	# Main rectangles
	# 	Object(id=1191, x=15, y=15, editor_layer_1=12,
	# 		z_order=2, rotation=-90, color_1=3, z_layer=3),
	# 	Object(id=1191, x=15, y=45, editor_layer_1=12,
	# 		z_order=2, rotation=-90, color_1=3, z_layer=3),
	# 	# 2/3 rectangle
	# 	Object(id=1767, x=3.75, y=50, editor_layer_1=12,
	# 		z_order=3, rotation=-270, color_1=2, z_layer=3, scale=2.5),
	# 	# Square
	# 	Object(id=917, x=3.75, y=41.25, editor_layer_1=12,
	# 		z_order=4, color_1=1, z_layer=3)
	# ]

	# lower_middle_quarter_old = [
	# 	# Main rectangles
	# 	Object(id=1191, x=15, y=-45, editor_layer_1=13,
	# 		z_order=2, rotation=-90, color_1=3, z_layer=3),
	# 	Object(id=1191, x=15, y=-15, editor_layer_1=13,
	# 		z_order=2, rotation=-90, color_1=3, z_layer=3),
	# 	# 2/3 rectangle
	# 	Object(id=1767, x=3.75, y=-50, editor_layer_1=13,
	# 		z_order=3, rotation=-90, color_1=4, z_layer=3, scale=2.5),
	# 	# Square
	# 	Object(id=917, x=3.75, y=-41.25, editor_layer_1=13,
	# 		z_order=4, color_1=1, z_layer=3)
	# ]

	# lower_quarter_old = [
	# 	# Main rectangles
	# 	Object(id=1191, x=15, y=-75, editor_layer_1=14,
	# 		z_order=1, rotation=-90, color_1=4, z_layer=3),
	# 	Object(id=1191, x=15, y=-105, editor_layer_1=14,
	# 		z_order=1, rotation=-90, color_1=4, z_layer=3),
	# 	# Square
	# 	Object(id=917, x=3.75, y=-116.25, editor_layer_1=14,
	# 		z_order=4, color_1=1, z_layer=3),
	# 	# Shading
	# 	Object(id=1754, x=0.94, y=-91.875, editor_layer_1=15,
	# 		z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.88),
	# 	Object(id=1754, x=2.815, y=-91.875, editor_layer_1=15,
	# 		z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.87),
	# 	Object(id=1754, x=4.685, y=-91.875, editor_layer_1=15,
	# 		z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.87),
	# 	Object(id=1754, x=6.56, y=-91.875, editor_layer_1=15,
	# 		z_order=5, rotation=-90, color_1=4, z_layer=3, scale=1.88)
	# ]
