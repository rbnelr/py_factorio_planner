import pyglet
from window import Window, gl

wnd = Window()

from factorio_entities import * 

# entity instances
x = 0

entities = {}
for name in entity_classes:
	entities[name] = entity_classes[name]((x,0))
	x += 64*5


def in_rect(pos, rect_pos, rect_sz):
	return	pos[0] > rect_pos[0] - rect_sz[0]/2 and pos[1] > rect_pos[1] - rect_sz[1]/2 and pos[0] < rect_pos[0] + rect_sz[0]/2 and pos[1] < rect_pos[1] + rect_sz[1]/2

toolbar_selected = None

def draw_toolbar(inp):
	global toolbar_selected
	
	pad = 3
	sz = (55,55)
	col_normal = (0.6,0.6,0.6)
	col_hovered = (0.9,0.9,0.9)
	col_selected = (0.6,1.0,0.6)
	col_selected_hover = (0.3,0.9,0.3)

	count = len(entity_classes)
	width = (sz[1] +pad*2) * count

	shortcuts = [inp.button["_%d" % num] for num in (1,2,3,4,5,6,7,8,9,0)]

	for i, (name, ec) in enumerate(entity_classes.items()):

		x = wnd.width/2 - width/2 + (sz[1] +pad*2) * i
		
		pos = (x, sz[1]/2 +pad)

		selected = toolbar_selected == name
		hovered = in_rect(inp.mouse_pos_px, rect_pos=pos, rect_sz=sz)

		if (hovered and inp.lmb.went_down) or (i<10 and shortcuts[i].went_down):
			selected = not selected
			toolbar_selected = name if selected else None

		col = col_normal

		if hovered:
			col = col_hovered
		if selected:
			col = col_selected_hover if hovered else col_selected

		Button.draw(pos, sz, col)

		ec.icon.draw(pos, (sz[0] -pad*2, sz[1] -pad*2))

@wnd.draw
def draw(inp,dt):
	gl.glClearColor(50/255, 50/255, 50/255, 1)
	wnd.clear()

	draw_toolbar(inp)


	for e in entities.values():
		e.update(dt)
		e.draw_entity()

wnd.run()
