import pyglet
from factorio_data import factorio_base_dir

def load_image (filename):
	try:
		return pyglet.image.load(filename.replace("__base__", factorio_base_dir))

	except Exception:
		return None # not loaded

def load_sprite (filename):
	try:
		return pyglet.sprite.Sprite(load_image())

	except Exception:
		return None # not loaded

class Icon:
    def __repr__ (self): return self.name

    def load (filename):
        i = Icon()

        i.filename = filename
        i.sprite = load_sprite(filename)

        return i

class Sprite_Sheet:
	def __repr__ (self): return self.name

	def load (d):
		if "hr_version" in d:
			d = d["hr_version"]

		i = Sprite_Sheet()

		i.filename			= d["filename"]

		i.width				= d["width"]
		i.height			= d["height"]

		i.frame_count		= d.get("frame_count", 1)
		i.line_length		= d.get("line_length", 1)

		i.scale				= d.get("scale", 1)
		i.shift				= d.get("shift", (0,0))

		i.draw_as_shadow	= d.get("draw_as_shadow", False)
		i.blend_mode		= d.get("blend_mode", "normal")

		img = load_image(i.filename)
		img_seq = pyglet.image.ImageGrid(img, i.line_length, i.frame_count // i.line_length, i.width, i.height)
		anim = pyglet.image.Animation.from_image_sequence(img_seq, 0.1, True)

		i.sprite			= pyglet.sprite.Sprite(anim)

		return i
	
	def draw (self, pos, anim_t):

		fy, fx = divmod(int(anim_t * self.frame_count), self.line_length)

		pos = (pos[0] - self.width/2, pos[1] - self.height/2) # sprites are places using their center

		pos = (	pos[0] + self.shift[0] * 32 / self.scale,
				pos[1] + self.shift[1] * 32 / self.scale )

		pos = (pos[0] + 64*3/2, pos[1] + 64*5) # offset for now
		

		flags = 0

		if (self.blend_mode == "additive"):
			#flags |= pg.BLEND_ADD
			pass

		#self.sprite, pos, pg.Rect(fx*self.width, fy*self.height,  self.width,self.height), flags)

		#self.sprite._animate(0.1)
		self.sprite.draw()

def load_icon (name):
	return load_image(icons_dir + name + ".png");

def load_entity_sprite_sheet (name, anim_frames):
	return load_image(entity_dir + name + ".png");

