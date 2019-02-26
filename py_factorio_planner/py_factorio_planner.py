from window import Window, dt, gl

wnd = Window()

from factorio_entities import * 

# entity instances
x = 0

entities = {}
for name in entity_classes:
	entities[name] = entity_classes[name]((x,0))
	x += 64*5

@wnd.draw
def draw():
	gl.glClearColor(50/255, 50/255, 50/255, 1)
	wnd.clear()

	#for e in entities.values():
	#	e.update(dt)
	#	e.push_entity()
	
	e = entities["assembling-machine-1"]
	e.update(dt)
	e.push_entity()

wnd.run()
