
import pygame as pg

from timer import Timer

pg.init()

wnd = pg.display.set_mode((1280,720), pg.RESIZABLE|pg.DOUBLEBUF|( pg.OPENGL if False else 0 ))

pg.display.set_caption("Py Factorio Planner");

factorio_dir = "D:/steam/steamapps/common/Factorio/"

icons_dir   = factorio_dir + "data/base/graphics/icons/"
entity_dir  = factorio_dir + "data/base/graphics/entity/"

def load_image (filepath):
    try:
        return pg.image.load(filepath.replace("/", "\\"))

    except Exception:
        return None # not loaded
    
class Icon:
    def __repr__ (self): return self.name

    def load (name):
        i = Icon()

        i.name = name
        i.image = load_image(icons_dir + name + ".png")

        return i

class Sprite_Sheet:
    def __repr__ (self): return self.name

    def load (name, frames):
        i = Sprite_Sheet()

        i.name = name
        i.image = load_image(entity_dir + name + ".png")
        i.frames = frames

        return i
    
    def draw (self, pos, frame):
        sheet_sz = self.image.get_size()
        sprite_w = sheet_sz[0] / self.frames[0]
        sprite_h = sheet_sz[1] / self.frames[1]

        fy, fx = divmod(frame, self.frames[0])

        wnd.blit(self.image, pos, pg.Rect(fx*sprite_w, fy*sprite_h,  sprite_w,sprite_h));

def load_icon (name):
    return load_image(icons_dir + name + ".png");
    
def load_entity_sprite_sheet (name, anim_frames):
    return load_image(entity_dir + name + ".png");

#
class Assembling_Machine:
    
    def __init__ (self):
        self.work_t = 0 # [0,1) work anim

    def draw_entity (self, pos):
        frames = self.sprite.frames
        frames_count = frames[0] * frames[1]

        f = int(self.work_t * frames_count)

        self.sprite.draw(pos, f)

    def update (self):
        self.work_t += dt * self.work_speed
        self.work_t %= 1

def assembling_machine_class (level, work_speed): # creating classes via functions to adhere to DRY
    cls = type(f"Assembling_Machine_{level}", (Assembling_Machine,), {})
    
    cls.name = f"assembling-machine-{level}"
    cls.work_speed = work_speed
    
    cls.icon = Icon.load(cls.name)
    cls.sprite = Sprite_Sheet.load(f"{cls.name}/hr-{cls.name}", (8,4))
    cls.shadow = Sprite_Sheet.load(f"{cls.name}/hr-{cls.name}-shadow", (8,4))
    return cls

Assembling_Machine_1 = assembling_machine_class(1, 0.5)
Assembling_Machine_2 = assembling_machine_class(2, 0.75)
Assembling_Machine_3 = assembling_machine_class(3, 1.21)

# entity instances
am1 = Assembling_Machine_1()
am2 = Assembling_Machine_2()
am3 = Assembling_Machine_3()

#
timer = Timer.begin()
dt = 0

run = True;

while run:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
    
    wnd.fill((50,50,50))
    
    am1.update()
    am2.update()
    am3.update()

    am1.draw_entity((0,0))
    am2.draw_entity((300,0))
    am3.draw_entity((600,0))

    pg.display.flip()

    dt = timer.step()

pg.quit()
