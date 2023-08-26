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
	HSV,
	PulseMode
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

if __name__ == "__main__":
	from Screen import Screen

	editor, db, local_levels = load_editor()

	screen = Screen(editor)
	
	add_objects(editor, screen.get_objects())

	save_changes(editor, db, local_levels)






# [NemO's Script]: Objects in the editor:
#    > <Object id=1007 x=-29 y=135 is_active_trigger=True target_group_id=2 duration=0 opacity=0>
#    > <Object id=1268 x=-29 y=105 is_active_trigger=True target_group_id=3>
#    > <Object id=1268 x=15 y=165 is_active_trigger=True target_group_id=1>
#    > <Object id=1347 x=75 y=255 groups={1} spawn_triggered=True is_active_trigger=True target_group_id=12 follow_target_pos_center_id=9 duration=999 x_mod=0 y_mod=-0.5>
#    > <Object id=1347 x=75 y=225 groups={1} spawn_triggered=True is_active_trigger=True target_group_id=13 follow_target_pos_center_id=9 duration=999 x_mod=0 y_mod=0.5>
#    > <Object id=1268 x=45 y=165 groups={1} spawn_triggered=True is_active_trigger=True target_group_id=11 spawn_duration=0.1>
#    > <Object id=1757 x=122.5 y=127.5 h_flipped=True rotation=-90 color_1=1 z_layer=5 scale=5>
#    > <Object id=1757 x=122.5 y=202.5 h_flipped=True groups={12} rotation=-90 color_1=1 z_layer=5 scale=5>
#    > <Object id=1757 x=122.5 y=52.5 h_flipped=True groups={13} rotation=-90 color_1=1 z_layer=5 scale=5>
#    > <Object id=1754 x=121.25 y=202.5 v_flipped=True linked_group=1 editor_layer_1=1 groups={12} z_order=9 rotation=-270 color_1=4 z_layer=7 scale=2.5 color_1_hsv_enabled=True color_1_hsv_val
# ues=<HSV h=0 s=1 v=0 s_checked=False v_checked=False>>
#    > <Object id=1754 x=123.75 y=202.5 v_flipped=True linked_group=1 editor_layer_1=1 groups={12} z_order=9 rotation=-270 color_1=4 z_layer=7 scale=2.5 color_1_hsv_enabled=True color_1_hsv_val
# ues=<HSV h=0 s=1 v=0 s_checked=False v_checked=False>>
#    > <Object id=1754 x=121.25 y=52.5 h_flipped=True v_flipped=True linked_group=2 editor_layer_1=1 groups={13} z_order=9 rotation=-270 color_1=4 z_layer=7 scale=2.5 color_1_hsv_enabled=True c
# olor_1_hsv_values=<HSV h=0 s=1 v=0 s_checked=False v_checked=False>>
#    > <Object id=1754 x=123.75 y=52.5 h_flipped=True v_flipped=True linked_group=2 editor_layer_1=1 groups={13} z_order=9 rotation=-270 color_1=4 z_layer=7 scale=2.5 color_1_hsv_enabled=True c
# olor_1_hsv_values=<HSV h=0 s=1 v=0 s_checked=False v_checked=False>>
#    > <Object id=901 x=225 y=-15 is_active_trigger=True target_group_id=4 move_x=0 move_y=0 duration=999 easing=<Easing.Default: 0> easing_rate=2 lock_to_player_x=True>
#    > <Object id=901 x=225 y=-45 is_active_trigger=True target_group_id=17 move_x=0 move_y=-90 duration=5 easing=<Easing.Default: 0> easing_rate=2>
#    > <Object id=901 x=285 y=375 groups={8, 9} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=7 move_x=0 move_y=150 duration=0.2 easing=<Easing.Default: 0> easi
# ng_rate=2>
#    > <Object id=1766 x=375 y=375 editor_layer_1=1 groups={5}>
#    > <Object id=901 x=375 y=225 groups={8} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=7 move_x=0 move_y=150 duration=0 easing=<Easing.Default: 0> easing_ra
# te=2 follow_target_pos_center_id=5 use_target_enabled=True target_pos_coordinates=<TargetPosCoordinates.Both: 0>>                                                                              
#    > <Object id=1268 x=315 y=225 groups={8, 1} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=8 spawn_duration=0.2>                                            
#    > <Object id=1816 x=375 y=375 editor_layer_1=2 groups={15} z_order=2 z_layer=5 scale=0.15 is_active_trigger=True item_id=12 dynamic_block=True>                                             
#    > <Object id=1816 x=375 y=375 groups={7} z_order=2 z_layer=5 scale=0.15 is_active_trigger=True item_id=11 dynamic_block=True>                                                               
#    > <Object id=1268 x=315 y=195 groups={11} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=11 spawn_duration=0.2>                                             
#    > <Object id=1767 x=375 y=525 editor_layer_1=1 groups={6}>                                                                                                                                  
#    > <Object id=1816 x=375 y=525 groups={17} is_active_trigger=True item_id=1>                                                                                                                 
#    > <Object id=1815 x=405 y=135 groups={1} spawn_triggered=True is_active_trigger=True target_group_id=16 duration=0.5 activate_group=True item_id=1 block_b_id=12>                           
#    > <Object id=901 x=495 y=225 groups={18, 11} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=15 move_x=0 move_y=150 duration=0.2 easing=<Easing.Default: 0> e
# asing_rate=2>                                                                                                                                                                                  
#    > <Object id=1815 x=405 y=165 groups={1} spawn_triggered=True is_active_trigger=True target_group_id=10 duration=0.5 activate_group=True item_id=1 block_b_id=11>                           
#    > <Object id=1616 x=465 y=135 groups={16} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=18>                                                                
#    > <Object id=901 x=465 y=225 groups={11} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=15 move_x=0 move_y=150 duration=0 easing=<Easing.Default: 0> easing_
# rate=2 follow_target_pos_center_id=5 use_target_enabled=True target_pos_coordinates=<TargetPosCoordinates.Both: 0>>                                                                            
#    > <Object id=1616 x=465 y=165 groups={10} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=9>                                                                 
#    > <Object id=1616 x=495 y=165 groups={10} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=16>                                                                
#    > <Object id=1616 x=495 y=135 groups={16} spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=10>                                                                
#    > <Object id=901 x=525 y=165 groups={10} z_order=2 z_layer=5 spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=9 move_x=0 move_y=150 duration=0.2 easing=<Easin
# g.Default: 0> easing_rate=2 follow_target_pos_center_id=7 use_target_enabled=True target_pos_coordinates=<TargetPosCoordinates.OnlyY: 2>>                                                      
#    > <Object id=901 x=525 y=135 groups={16} z_order=2 z_layer=5 spawn_triggered=True multi_trigger=True is_active_trigger=True target_group_id=9 move_x=0 move_y=150 duration=0.2 easing=<Easin
# g.Default: 0> easing_rate=2 follow_target_pos_center_id=15 use_target_enabled=True target_pos_coordinates=<TargetPosCoordinates.OnlyY: 2>>                                                     
