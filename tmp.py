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

	new_objects = []

	for obj_ in editor.get_objects():
		if obj_.groups != None and 999 in obj_.groups or obj_.x > 30000:
			new_objects.append(obj_)

	print(len(new_objects))

	editor.objects = new_objects
	# chosen_level2 = local_levels[1]
	# editor2 = chosen_level.open_editor()

	# editor2 

	save_changes(editor, db, local_levels)
