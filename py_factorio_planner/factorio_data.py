r"""
Get real data and graphics from factorio

tries to get data from actual factorio installation (can only get data from lua with mod currently)
else loads from 'factorio_lua_data.json' next to python script

---------- How to get data from real factorio installation
download
https://www.reddit.com/r/factorio/comments/4x24t3/factorio_data_in_json/
https://drive.google.com/file/d/0B7P6GeSO30hxTEJUd2JCZnFmSk0/view

install into C:\Users\<user>\AppData\Roaming\Factorio\mods
-> had to change  "factorio_version": "0.16",  and  "dependencies": ["base >= 0.16.0" in  info.json to get the mod to work

start factorio
-> C:\Users\<user>\AppData\Roaming\Factorio\factorio-current.log contains json string with all lua data of factorio
"""

import os.path
import re
import json
import sys

steam_dir = r"D:\steam"
factorio_dir = fr"{steam_dir}\steamapps\common\factorio"

factorio_appdata = os.path.expandvars(r"%APPDATA%\Factorio")

#
factorio_log = fr"{factorio_appdata}\factorio-current.log"

factorio_base_dir   = fr"{factorio_dir}\data\base"

def get_factorio_lua_data():
	
	print(f"try to get factorio lua data from '{factorio_log}'...")

	def extract_factorio_data_json_from_log():
		try:
			with open(factorio_log) as f:
				for line in f:
					m = re.search(r"^\s*[\d\.]+\s+Script @__json-extractor.*__/data.lua:3:\s*(.*)$", line)
					if m:
						return m.group(1) # success

			return None # mod not installed and factorio run?
		except Exception:
			return None # file not found, factorio not installed?

	json_str = extract_factorio_data_json_from_log()

	path = fr"{sys.path[0]}\factorio_lua_data.json" if sys.path[0] else "factorio_lua_data.json"
	
	if (json_str): # json string found in factorio_log, we are on a machine that has factorio and the extraction mod installed
		
		print(f"parse factorio lua data from json...")
		
		lua_data = json.loads(json_str)
		
		print(f"save factorio lua data to '{path}'...")

		try:
			indent = 4 if True else None # indented pretty dumps is VERY slow, while no indent is fast enough 
			json_str = json.dumps(lua_data, indent=None)

			with open(path, "w") as f:
				f.write(json_str) # save as json file so i can run this on a machine without factorio installed
		except Exception:
			pass # writing file failed
		
	else: # we are on a machine that does not have factorio and the extraction mod installed
		
		print(f"parse factorio lua data from '{path}'...")

		with open(path) as f:
			lua_data = json.load(f)
	
	print(f"got factorio lua data.")

	return lua_data

lua_data = get_factorio_lua_data()
