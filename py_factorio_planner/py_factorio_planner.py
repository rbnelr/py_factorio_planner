import pygame as pg
pg.init()

from timer import Timer
from factorio_entities import * 

# entity instances
x = 0

entities = {}
for name in entity_classes:
	entities[name] = entity_classes[name]((x,0))
	x += 64*5

#
timer = Timer.begin()
dt = 0


wnd = pg.display.set_mode((2000,720), pg.RESIZABLE|pg.DOUBLEBUF|( pg.OPENGL if False else 0 ))

pg.display.set_caption("Py Factorio Planner");

run = True;

while run:

	for e in pg.event.get():
		if e.type == pg.QUIT:
			run = False

	wnd.fill((50,50,50))

	for e in entities.values():
		e.update(dt)
		e.push_entity(wnd)

	pg.display.flip()

	dt = timer.step()

pg.quit()
