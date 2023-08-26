from MagnumOpus import *
import re

excluded_properties = [
'glow_disabled',
'do_not_fade',
'do_not_enter'
]

def read_blocks(editor, groups=[], excluded_groups=[]):
	print("\n[NemO's Script]: Objects in the editor: ")
	print("Included groups:", *groups)
	print("Excluded groups:", *excluded_groups)
	# objects = editor.get_objects().copy()
	# objects.sort(key=lambda obj: obj.y, reverse=True)
	# for obj in objects:
	i = 0
	for obj in editor.get_objects():
		if validate_object(obj, groups, excluded_groups):
			i += 1
			print(get_description(str(obj)))
	print("{} objects found".format(i))

def validate_object(obj, groups=[], excluded_groups=[]):
	if excluded_groups:
		if not obj.groups:
			return False
		skip = False
		for g in excluded_groups:
			if g in obj.groups:
				skip = True
				break
		if skip:
			return False
	if not groups:
		return True
	if not obj.groups:
		return False
	for g in groups:
		if not g in obj.groups:
			return False
	return True

def get_description(desc):
	if desc[0] == "<":
		desc = desc[1:]
	if desc[-1] == ">":
		desc = desc[:-1]
	if desc[0:6] == "Object":
		desc = desc[7:]
	desc = re.sub(", ", ",", desc)
	desc = re.sub(": ", ":", desc)
	properties_list = desc.split(" ")
	names = [p.split("=")[0] for p in properties_list]
	values = [p.split("=")[1] for p in properties_list]
	z = zip(names, values)
	final_items = []
	for item in z:
		if not item[0] in excluded_properties:
			final_items.append(item)
	desc = "Object("
	for i, e in enumerate(final_items):
		desc += re.sub(",", ", ", e[0] + "=" + e[1])
		desc += ")" if i == len(final_items) - 1 else ", "
	return desc

if __name__ == "__main__":
	print("Input the groups you are looking for:")
	inp = input()
	if inp.lower() in ["info", "i"]:
		editor, db, local_levels = load_editor(False)
		groups = set()
		colliders = set()
		for obj_ in editor.get_objects():
			if obj_.groups != None:
				for group in obj_.groups:
					groups.add(group)
			if obj_.item_id != None:	
				colliders.add(obj_.item_id)

		print("\n[NemO's Script]: Groups used:")
		print_used(get_intervals(groups))
		print("\n[NemO's Script]: Colliders used:")
		print_used(get_intervals(colliders))
	else:
		groups = list(map(int, inp.split()))
		excluded_groups = list(filter(lambda x: x < 0, groups))
		groups = list(filter(lambda x: x > 0, groups))
		excluded_groups = list(map(lambda x: abs(x), excluded_groups))

		editor, db, local_levels = load_editor(False)

		read_blocks(editor, groups, excluded_groups)