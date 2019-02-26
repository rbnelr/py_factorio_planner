import pygame as pg
from factorio_data import factorio_base_dir

def load_image (filename):
    try:
        return pg.image.load(filename.replace("__base__", factorio_base_dir))

    except Exception:
        return None # not loaded

class Icon:
    def __repr__ (self): return self.name

    def load (filename):
        i = Icon()

        i.filename = filename
        i.image = load_image(filename)

        return i

class Sprite_Sheet:
	def __repr__ (self): return self.name

	def load (d):
		if "hr_version" in d:
			d = d["hr_version"]

		i = Sprite_Sheet()

		i.filename			= d["filename"]

		i.image				= load_image(i.filename)
		i.width				= d["width"]
		i.height			= d["height"]

		i.frame_count		= d.get("frame_count", 1)
		i.line_length		= d.get("line_length", 1)

		i.scale				= d.get("scale", 1)
		i.shift				= d.get("shift", (0,0))

		i.draw_as_shadow	= d.get("draw_as_shadow", False)
		i.blend_mode		= d.get("blend_mode", "normal")

		return i
	
	def push (self, pos, anim_t): # for use with pygame.Surface.blits

		fy, fx = divmod(int(anim_t * self.frame_count), self.line_length)

		pos = (pos[0] - self.width/2, pos[1] - self.height/2) # sprites are places using their center

		pos = (	pos[0] + self.shift[0] * 32 / self.scale,
				pos[1] + self.shift[1] * 32 / self.scale )

		pos = (pos[0] + 64*3/2, pos[1] + 64*5) # offset for now
		

		flags = 0

		if (self.blend_mode == "additive"):
			flags |= pg.BLEND_ADD

		return (self.image, pos, pg.Rect(fx*self.width, fy*self.height,  self.width,self.height), flags)

	def draw (self, wnd, *args):
		pg.Surface.blit(wnd, *self.push(*args));

def load_icon (name):
	return load_image(icons_dir + name + ".png");

def load_entity_sprite_sheet (name, anim_frames):
	return load_image(entity_dir + name + ".png");

