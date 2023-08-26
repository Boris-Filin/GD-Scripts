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

def read_blocks(editor):
	print("\n[NemO's Script]: Objects in the editor: ")
	for obj in editor.get_objects():
		print("   >", obj)
