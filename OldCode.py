
editor, db, local_levels = load_editor()

camera = editor.get_objects()[0]
for obj in editor.get_objects():
	if not obj.groups:
		continue
	if 14 in obj.groups:
		camera = obj
		break

import Rays
rays = Rays.get_rays(20, 20, 90)
add_objects(editor, rays)

triggers1 = Rays.get_ray_triggers(50, 50, camera)
add_objects(editor, triggers1)

import Slices
slices = Slices.get_slices(3, 1)
add_objects(editor, slices)

save_changes(editor, db, local_levels)

# Utils.read_blocks(editor)

print()