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

import Utils

client = gd.Client()

def get_intervals(s):
	if not s:
		return None
	l = list(s)
	prev = l[0]
	borders = [prev]
	for e in l[1:]:
		if e != prev + 1:
			borders.append(prev)
			borders.append(e)
		prev = e
	borders.append(l[-1])
	res = [(borders[2 * i], borders[2 * i + 1]) for i in range(len(borders) // 2)]
	return res

def print_used(groups):
	for pair in groups:
		a = pair[0]
		b = pair[1]
		if a == b:
			print("  {}".format(a))
		else:
			print("  {} - {}".format(pair[0], pair[1]))

def load_editor(erase_prev=True, erase_all=False):

	path1 = "C:/Users/user/AppData/Local/GeometryDash/CCGameManager.dat"
	path2 = "C:/Users/user/AppData/Local/GeometryDash/CCLocalLevels.dat"

	db = gd.api.save.load(path1, path2)

	local_levels = db.load_my_levels()

	i = 5
	while (len(local_levels) == 0 and i > 0):
		db = gd.api.save.load(path1, path2)

		local_levels = db.load_my_levels()

		i -= 1
	print("\n[NemO's Script]: {} created levels found.".format(len(local_levels)))
	chosen_level = local_levels[0]
	editor = chosen_level.open_editor()

	if erase_all:
		editor.objects = []
	elif erase_prev:
		remaining_objects = []
		for obj in editor.get_objects():
			if obj.groups != None:
				if not 999 in obj.groups:
					remaining_objects.append(obj)
			else:
				remaining_objects.append(obj)
		editor.objects = remaining_objects
	else:
		editor = chosen_level.open_editor()

	print("\n[NemO's Script]: Editor opened")

	return editor, db, local_levels

def add_objects(editor, objects, mark_as_scripted=True):
	for obj in objects:
		if mark_as_scripted:
			if obj.groups == None:
				obj.groups = {999}
			elif not 999 in obj.groups:
				obj.groups.add(999)
		editor.add_objects(obj)
	print("\n[NemO's Script]: {} objects added.".format(len(objects)))

def save_changes(editor, db, local_levels):
	gd.api.editor.dump_editor(editor)
	db.dump_my_levels(local_levels)
	db.dump()

	print("\n[NemO's Script]: Groups used:")
	print_used(get_intervals(editor.get_groups()))
	print("\n[NemO's Script]: Changes saved.")


async def tmp(editor, db, local_levels):
	level = await client.get_level(91940372)
	editor1 = level.open_editor()

	data = level.data

	editor.objects = editor1.get_objects()
	editor.add_colors(editor1.get_colors())

	# save_changes(editor1, db, local_levels.insert(0, gd.level.Level.from_data(data, level.creator, level.song, client)))
	save_changes(editor, db, local_levels)

	# print(level.name)

if __name__ == "__main__":
	from Screen import Screen

	editor, db, local_levels = load_editor()

	import asyncio
	asyncio.run(tmp(editor, db, local_levels))
	



