from factorio_data import lua_data
from graphics import * 

class Assembling_Machine:
    
	def __init__ (self):
		self.work_t = 0 # [0,1) work anim

	def draw_entity (self, wnd, pos):
		for l in [l for l in self.sprite_layers if l.draw_as_shadow]:
			l.draw(wnd, pos, self.work_t)

		for l in [l for l in self.sprite_layers if not l.draw_as_shadow]:
			l.draw(wnd, pos, self.work_t)

	def update (self, dt):
		self.work_t += dt * self.crafting_speed
		self.work_t %= 1

def assembling_machine_class (m): # creating classes via functions to adhere to DRY
	cls = type(m["name"].replace("-", "_"), (Assembling_Machine,), {})

	cls.name = m["name"]
	cls.crafting_speed = m["crafting_speed"]

	cls.icon = Icon.load(m["icon"])
	
	if ("north" in m["animation"]):
		cls.sprite_layers = [ Sprite_Sheet.load(l) for l in m["animation"]["north"]["layers"] ] # north only for now
	else: # same sprite for all oris
		cls.sprite_layers = [ Sprite_Sheet.load(l) for l in m["animation"]["layers"] ]
	
	return cls

entity_classes = {}

for m in lua_data["assembling-machine"].values():
	entity_classes[m["name"]] = assembling_machine_class(m)