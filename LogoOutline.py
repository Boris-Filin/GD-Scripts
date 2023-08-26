from MagnumOpus import *
from gd.api import (
	ColorCollection,
	ColorChannel,
	Editor,
	Object,
	HSV
)
if __name__ == "__main__":

	editor, db, local_levels = load_editor(False)

	fac1 = 1.533333
	fac2 = 2.066667

	new_objects = []

	for obj_ in editor.get_objects():
		if obj_.groups == None or not 172 in obj_.groups:
			continue
		if obj_.scale == None:
			obj_.scale = 1
		copy1 = obj_.copy()
		copy1.scale *= fac1
		copy1.color_1_hsv_enabled = True
		copy1.color_1_hsv_values = HSV(h=0, s=1, v=0, s_checked=False, v_checked=False)
		copy1.editor_layer_1 = 29
		copy1.z_order -= 1
	
		copy2 = obj_.copy()
		copy2.scale *= fac2
		copy2.color_1_hsv_enabled = True
		copy2.color_1_hsv_values = HSV(h=0, s=0, v=2, s_checked=False, v_checked=False)
		copy2.editor_layer_1 = 30
		copy2.z_order = 1

		new_objects.append(copy1)
		new_objects.append(copy2)

	print(new_objects)

	add_objects(editor, new_objects)

	save_changes(editor, db, local_levels)
