import logging
import gd
import asyncio
import pathlib
import math
import random

from gd.api import (
	ColorCollection,
	ColorChannel,
	Editor,
	Object,
	HSV
)

from gd import memory
from gd.enums import ZLayer
from gd.enums import TargetPosCoordinates

from Strips import Strips
from Ground import Ground
from Rays import Rays
from Triggers import Triggers
from Toggles import Toggles
from ImageTest import ImageLoader
from Entity_System import Entity_System
from Secondary_Rays import Secondary_Rays
from Wall_Texture_Triggers import Wall_Texture_Triggers
from Entity import Entity
from UI_Panel import UI_Panel
from Flashlight import Flashlight

from Texts import Texts

client = gd.Client()


def load_editor(erase_prev=True, erase_all=False):
	path1 = "/Users/feelin/Library/ApplicationSupport/GeometryDash/CCGameManager.dat"
	path2 = "/Users/feelin/Library/ApplicationSupport/GeometryDash/CCLocalLevels.dat"

	db = gd.api.save.load(path1, path2)

	local_levels = db.load_created_levels()

	i = 5
	while (len(local_levels) == 0 and i > 0):
		db = gd.api.save.load(path1, path2)

		local_levels = db.load_created_levels()

		i -= 1
	print("\n[NemO's Script]: {} created levels found.".format(len(local_levels)))
	chosen_level = local_levels[0]

	if erase_all:
		editor = Editor()
	elif erase_prev:
		editor = chosen_level.open_editor()
		remaining_objects = []
		for obj in editor.get_objects():
			if obj.groups != None:
				if not 1111 in obj.groups:
					remaining_objects.append(obj)
			else:
				remaining_objects.append(obj)
		editor.set_objects(remaining_objects)
	else:
		editor = chosen_level.open_editor()

	print("\n[NemO's Script]: Editor opened")

	return editor, db

def add_objects(editor, objects, mark_as_scripted=True):
	for obj in objects:
		if mark_as_scripted:
			if obj.groups == None:
				obj.groups = {1111}
			elif not 1111 in obj.groups:
				obj.groups.add(1111)
		editor.add_objects(obj)
	print("\n[NemO's Script]: {} objects added.".format(len(objects)))

def save_changes(editor, db):
	local_levels = db.load_created_levels()
	chosen_level = local_levels[0]
	chosen_level.set_data(editor.dump())
	
	db.set_created_levels(local_levels)
	db.dump()
	print("\n[NemO's Script]: Changes saved.")

def read_blocks(editor):
	print("\n[NemO's Script]: Objects in the editor: ")
	for obj in editor.get_objects():
		print("   >", obj)

def write():
	group_offset = 100
	editor, db = load_editor()
	strips = Strips(30, 16, 9)
	group_offset += strips.groups_number
	ground = Ground(30, 16, 9)
	rays = Rays(30, 16)
	triggers = Triggers(30, 16)
	toggles = Toggles(30, 16)
	# secondary_rays = Secondary_Rays(30, 16)
	entity_system = Entity_System(30, 9, group_offset)
	monster1 = Entity(["Monster", "Blast", "Blood"], 30, 16, 9, 0, entity_system.groups)
	actual_offset = 30 * 16 + monster1.groups_number
	monster2 = Entity(["Monster2", "Blood"], 30, 16, 9, 1, entity_system.groups, actual_offset)
	actual_offset += monster2.groups_number
	portal = Entity(["Portal"], 30, 16, 9, 2, entity_system.groups, actual_offset)
	actual_offset += portal.groups_number
	new_offset = 1000 - 100 - 2 * len(entity_system.groups)
	bottle = Entity(["Bottle"], 30, 16, 9, 3, entity_system.groups, new_offset)
	actual_offset += bottle.groups_number
	key = Entity(["Key"], 30, 16, 9, 4, entity_system.groups, new_offset + bottle.groups_number)
	actual_offset += key.groups_number
	flashlight = Flashlight(30, 9)

	ui_panel = UI_Panel(120, 8)


	add_objects(editor, strips.get())
	add_objects(editor, ground.get())
	add_objects(editor, rays.get())
	add_objects(editor, triggers.get())
	add_objects(editor, toggles.get())
	# add_objects(editor, secondary_rays.get())
	add_objects(editor, entity_system.get())
	add_objects(editor, monster1.get())
	add_objects(editor, monster2.get())
	# add_objects(editor, portal.get())
	add_objects(editor, bottle.get())
	add_objects(editor, key.get())
	add_objects(editor, ui_panel.get())
	add_objects(editor, flashlight.get())

	channels = []
	# white = ColorChannel(red=255, green=255, blue=255, id=1)
	# black = ColorChannel(red=0, green=0, blue=0, id=2)
	# red = ColorChannel(red=255, green=0, blue=0, id=3)

	# walls1 = ColorChannel(red=255, green=0, blue=0, id=11)
	# walls2 = ColorChannel(red=0, green=50, blue=100, id=8)
	# ground1 = ColorChannel(red=255, green=0, blue=0, id=9)
	# ground2 = ColorChannel(red=0, green=50, blue=100, id=7)

	channels.append(ColorChannel(red=255, green=255, blue=255, id=1))
	channels.append(ColorChannel(red=0, green=0, blue=0, id=2))
	channels.append(ColorChannel(red=255, green=0, blue=0, id=3))
	channels.append(ColorChannel(red=100, green=0, blue=0, id=4))

	channels.append(ColorChannel(red=255, green=0, blue=0, id=11))
	channels.append(ColorChannel(red=0, green=50, blue=100, id=8))
	channels.append(ColorChannel(red=255, green=0, blue=0, id=9))
	channels.append(ColorChannel(red=0, green=50, blue=100, id=7))


	opacity_channels = []
	for i in range(11):
		opacity_channels.append(ColorChannel(red=255, green=0, blue=0, opacity=0.1 * i, id=12 + i))

	channels.extend(opacity_channels)

	# editor.add_colors(white)
	# editor.add_colors(black)
	# editor.add_colors(red)
	# editor.add_colors(walls1)
	# editor.add_colors(walls2)
	# editor.add_colors(ground1)
	# editor.add_colors(ground2)

	for channel in channels:
		editor.add_colors(channel)

	save_changes(editor, db)

	return editor, db

def refresh_colours(editor, db):

	channels = []

	channels.append(ColorChannel(red=255, green=255, blue=255, id=1))
	channels.append(ColorChannel(red=0, green=0, blue=0, id=2))
	channels.append(ColorChannel(red=255, green=0, blue=0, id=3))
	channels.append(ColorChannel(red=100, green=0, blue=0, id=4))

	channels.append(ColorChannel(red=255, green=0, blue=0, id=11))
	channels.append(ColorChannel(red=0, green=50, blue=100, id=8))
	channels.append(ColorChannel(red=255, green=0, blue=0, id=9))
	channels.append(ColorChannel(red=0, green=50, blue=100, id=7))


	opacity_channels = []
	for i in range(11):
		opacity_channels.append(ColorChannel(red=255, green=0, blue=0, opacity=0.1 * i, id=12 + i))

	channels.extend(opacity_channels)

	for channel in channels:
		editor.add_colors(channel)

	save_changes(editor, db)

def write_test():
	editor, db = load_editor(True, True)
	objects = exceed_group_limit()
	add_objects(editor, objects)
	save_changes(editor, db)


def read():
	editor, db = load_editor(False)
	read_blocks(editor)

def clear_scripted():
	editor, db = load_editor()

def load_from_string(string_data):
	editor = gd.api.Editor.from_string(string_data)

	return editor

def save(file_name, save_all):
	editor, db = load_editor(not save_all)
	string_data = editor.to_string()
	try:
		with open("Structures/" + file_name, "w") as file:
			file.write(string_data)
			file.close()
	except:
		pass

def load(file_name, editor=None, mark_as_scripted=True):
	try:
		with open("Structures/" + file_name, "r") as file:
			string_data = file.read()
			if editor == None:
				editor = gd.api.Editor.from_string(string_data)
			else:
				editor2 = gd.api.Editor.from_string(string_data)
				# for obj_ in editor2.get_objects():
				add_objects(editor, editor2.get_objects(), mark_as_scripted)
			return editor
	except:
		return None

def restore(file_name):
	editor, db = load_editor(True, True)
	backup = load(file_name)
	save_changes(backup, db)

def image_test():
	white = ColorChannel(red=255, green=255, blue=255, id=1)
	black = ColorChannel(red=0, green=0, blue=0, id=2)
	red = ColorChannel(red=255, green=0, blue=0, id=4)
	colors = ColorCollection()
	editor, db = load_editor()

	# editor.set_colors(colors)
	editor.add_colors(white)
	editor.add_colors(black)
	editor.add_colors(red)

	image = ImageLoader("Gun", 0, 30, 30, True)
	add_objects(editor, image.get())
	# image = ImageLoader("GunFire", 0, 30, 30)
	add_objects(editor, image.get())

	# print(editor.get_colors())
	save_changes(editor, db)

def add(objects, mark_as_scripted=False):
	editor, db = load_editor(False)
	for obj in objects:
		editor.add_objects(obj)
	save_changes(editor, db)
	print("\n[NemO's Script]: {} objects added.".format(len(objects)))

def test_scaling(file_names):
	editor, db = load_editor(True, True)
	z_order = 0
	for file_name in file_names:
		for i in range(16):
			save = load(file_name + "_" + str(i))
			for obj in save.get_objects():
				obj.x += i * 300
				# obj.z_order = z_order
			add_objects(editor, save.get_objects())
		z_order += 1
	# backup = load(file_name)
	white = ColorChannel(red=255, green=255, blue=255, id=1)
	black = ColorChannel(red=0, green=0, blue=0, id=2)
	red = ColorChannel(red=255, green=0, blue=0, id=3)

	editor.add_colors(white)
	editor.add_colors(black)
	editor.add_colors(red)

	save_changes(editor, db)

def add_stuff():
	file_names = [
	# "Head",
	"Gun",
	"GunFire",
	# "Final Controls"
	]

	editor, db = load_editor(False)

	for file_name in file_names:
		load(file_name, editor, False)

	save_changes(editor, db)

def extrastuff():
	editor, db = load_editor(False)
	# for i in range(1100):
	# 	editor.add_objects(Object(id=1764, x=45, y=15, groups={i + 1}))
	# editor.add_objects(Object(id=1816, x=15, y=15, trigger=True, item_or_block_id=10,
	# 				dynamic_block=True, scale=4))
	# editor.add_objects(Object(id=1816, x=15, y=15, trigger=True, item_or_block_id=494,
	# 				dynamic_block=True, scale=6.4))
	# editor.add_objects(Object(id=1816, x=15, y=15, trigger=True, item_or_block_id=10,
	# 			dynamic_block=True, scale=0.3))
	# editor.add_objects(Object(id=1764, x=45, y=15, groups={1009}))
	# editor.add_objects(Object(id=901, x=15, y=-15, trigger=True, target_group_id=1,
	# 	other_id=1009, use_target=True, target_pos_coordinates=TargetPosCoordinates.BOTH))
	# editor.add_objects(Object(id=1764, x=75, y=15, groups={1008}))
	# editor.add_objects(Object(id=901, x=45, y=-15, trigger=True, target_group_id=1,
	# 	other_id=1008, use_target=True, target_pos_coordinates=TargetPosCoordinates.BOTH))
	# editor.add_objects(Object(id=1815, x=15, y=-15, trigger=True,
	# 	target_group_id=1008, duration=0.5, activate_group=True, item_or_block_id=1,
	# 	block_b_id=2))
	# editor.add_objects(Object(id=1049, x=75, y=-15, groups={1008}, spawn_triggered=True, multi_trigger=True,
	# 	trigger=True, target_group_id=1009))
	# editor.add_objects(Object(id=914, x=45.5, y=15.0, text='Chapter', scale=0.25))
	# editor.add_objects(Object(id=914, x=45.5, y=75.0, text='Chapter', scale=0.4))
	# editor.add_objects(Object(id=914, x=45.5, y=45.0, text='Chapter', scale=0.3))

	# editor.add_objects(Object(id=914, x=45.5, y=15.0, text='Monster 1 (71, 72, 73)'))
	# editor.add_objects(Object(id=914, x=45.5, y=45.0, text='Monster 2 (74, 75, 76)'))
	texts = Texts()
	texts.add_tutorial(editor)

	save_changes(editor, db)

# def tweak():
# 	editor, db = load_editor(False)
# 	rays = Rays(30, 16)
# 	add_objects(editor, rays.get())
# 	save_changes(editor, db)

# def fix_issue():
# 	editor, db = load_editor(False)
# 	objects = editor.get_objects()
# 	for obj_ in objects:
# 		if obj_.text = 'fix here':
# 			obj_.text = 'Splendid!'
# 			print('Fix successful!')
# 	editor.

# 	save_changes(editor, db)

# test_scaling(["Monster", "Blood", "Blast"])
# test_scaling("Blast")
# test_scaling("Blood")
# image_test()
# restore("Pre-release 3")

# editor, db = write()
# refresh_colours(editor, db)

# read()
# save("RELEASE", True)

# save("Pre-release 3", True)
# save("Final Controls", True)

# clear_scripted()

# add_stuff()

# tweak()

# Colour scheme:
# 3 - Arts, Entities
# 4 - Underwater entities parts
# 7 - Ground
# 9 - Ceiling
# 8 - Underwater walls
# 11 - Walls
# 5 - Fog
# 6 - Underwater fog


def replace():
	editor, db = load_editor(False)

	local_levels = db.load_created_levels()
	chosen_level = local_levels[1]
	chosen_level.set_data(editor.dump())
	
	db.set_created_levels(local_levels)
	db.dump()
	print("\n[NemO's Script]: Changes saved.")


replace()

# extrastuff()
print()














