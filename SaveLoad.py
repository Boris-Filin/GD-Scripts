from MagnumOpus import *
import re
import os.path
from gd.api import (
	Editor,
	Object,
)
import json

def read_blocks(editor, groups=[], excluded_groups=[], ):
	print("\n[NemO's Script]: Objects in the editor: ")
	print("Included groups:", *groups)
	print("Excluded groups:", *excluded_groups)
	# objects = editor.get_objects().copy()
	# objects.sort(key=lambda obj: obj.y, reverse=True)
	# for obj in objects:
	objects = []
	for obj in editor.get_objects():
		if validate_object(obj, groups, excluded_groups):
			objects.append(obj)
			# print(get_description(str(obj)))
	return objects

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
	try:
		values = [p.split("=")[1] for p in properties_list]
	except:
		print(desc)
		print(properties_list)

	z = zip(names, values)
	final_items = []
	for item in z:
		final_items.append(item)
	desc = "Object("
	for i, e in enumerate(final_items):
		desc += re.sub(",", ", ", e[0] + "=" + e[1])
		desc += ")" if i == len(final_items) - 1 else ", "
	return desc

def save():
	print("Input the groups you are looking for:")

	inp = input(" > ")
	groups = list(map(int, inp.split()))
	excluded_groups = list(filter(lambda x: x < 0, groups))
	groups = list(filter(lambda x: x > 0, groups))
	excluded_groups = list(map(lambda x: abs(x), excluded_groups))

	editor, db, local_levels = load_editor(False)

	objects = read_blocks(editor, groups, excluded_groups)

	print("{} objects loaded".format(len(objects)))
	print("Enter the file name:")
	name = input(" > ")
	with open("Structures/" + name + ".txt", 'w') as f:
		f.writelines([str(obj_.to_map()) + '\n' for obj_ in objects])
	print("Saved successfully!")

def load():
	print("Enter the file name:")
	name = input(" > ")
	fname = "Structures/" + name + ".txt"
	if not os.path.isfile(fname):
		print("No such file found!")
		return
	str_objects = []
	with open(fname, 'r') as f:
		str_objects = f.readlines()

	print("Enter group offset:")
	group_offset = int(input(" > "))
	print("Enter position XY offset:")
	x_offset, y_offset = list(map(float, input().split()))[:2]

	objects = []
	for s in str_objects:
		s = s.strip()
		j = json.loads(str.replace(s, "\'", "\""))
		obj_ = Object.from_mapping(j)
		obj_.x += x_offset
		obj_.y += y_offset
		groups = set()
		for g in obj_.groups.split('.'):
			groups.add(int(g) + group_offset)
		obj_.groups = groups
		objects.append(obj_)

	editor, db, local_levels = load_editor(False)

	add_objects(editor, objects)

	save_changes(editor, db, local_levels)

	print("Structure loaded successfully!")


if __name__ == "__main__":
	print("Save or load?")
	inp = input(" > ")
	if inp.lower() in ["s", "save"]:
		save()
	elif inp.lower() in ["l", "load"]:
		load()
