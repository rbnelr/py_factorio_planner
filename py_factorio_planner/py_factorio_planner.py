from window import Window, gl

wnd = Window()

from factorio_entities import * 

# entity instances
x = 0

entities = {}
for name in entity_classes:
	entities[name] = entity_classes[name]((x,0))
	x += 64*5

@wnd.draw
def draw(dt):
	gl.glClearColor(50/255, 50/255, 50/255, 1)
	wnd.clear()

	for e in entities.values():
		e.update(dt)
		e.draw_entity()

wnd.run()
