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

		ss = Sprite_Sheet()

		ss.filename			= d["filename"]

		ss.width			= d["width"]
		ss.height			= d["height"]

		ss.frame_count		= d.get("frame_count", 1)
		ss.line_length		= d.get("line_length", 1)

		ss.scale			= d.get("scale", 1)
		ss.shift			= d.get("shift", (0,0))

		ss.draw_as_shadow	= d.get("draw_as_shadow", False)
		ss.blend_mode		= d.get("blend_mode", "normal")

		sheet_img = load_image(ss.filename)
		#img_seq = pyglet.image.ImageGrid(img, i.line_length, i.frame_count // i.line_length, i.width, i.height)
		#anim = pyglet.image.Animation.from_image_sequence(img_seq, 0.1, True)
		
		blend_src = pyglet.gl.GL_SRC_ALPHA
		blend_dst = pyglet.gl.GL_ONE_MINUS_SRC_ALPHA

		if (ss.blend_mode == "additive"):
			blend_src = pyglet.gl.GL_SRC_ALPHA
			blend_dst = pyglet.gl.GL_ONE

		ss.sprites = []
		for i in range(ss.frame_count):
			fy, fx = divmod(i, ss.line_length) # frame pos in sprite sheet
			
			s = pyglet.sprite.Sprite(sheet_img.get_region(fx * ss.width, sheet_img.height - (fy+1) * ss.height,  ss.width, ss.height), blend_src=blend_src, blend_dest=blend_dst)

			if ss.draw_as_shadow:
				s.opacity = 127

			ss.sprites.append(s)

		return ss
	
	def draw (self, pos, anim_t):

		frame = int(anim_t * self.frame_count)

		pos = (pos[0] - self.width/2, pos[1] - self.height/2) # sprites are places using their center

		pos = (	pos[0] + self.shift[0] * 32 / self.scale,
				pos[1] - self.shift[1] * 32 / self.scale )

		pos = (pos[0] + 64*3/2, pos[1] + 64*5) # offset for now
		

		self.sprites[frame].position = pos
		self.sprites[frame].draw()

def load_icon (name):
	return load_image(icons_dir + name + ".png");

def load_entity_sprite_sheet (name, anim_frames):
	return load_image(entity_dir + name + ".png");

