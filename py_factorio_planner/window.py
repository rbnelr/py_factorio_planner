import pyglet
import pyglet.gl as gl
import pyglet.window.key as key
import collections

from timer import Timer

timer = Timer.begin()
dt = 0

class Window(pyglet.window.Window):
	def __init__(self):
		super(Window, self).__init__(1280,720, resizable=True, caption="Py Factorio Planner", vsync=True)

		self.user_draw = None

		self.quit = False
		self.is_fullscreen = False # fullscreen already in pyglet window?

		self.dt = 0
		self.fps_limit = 160

		self.dt_history = collections.deque(maxlen = 60)

		self.dbg_counter = pyglet.text.Label(font_name="Consolas", font_size=17)

		self.counter = 0

	def draw(self, f):
		self.user_draw = f

	def _draw(self, flip=True):
		if self.user_draw:
			self.user_draw()
		
		def mean(numbers):
			return float(sum(numbers)) / max(len(numbers), 1)
		
		avg_dt = mean(self.dt_history)
		avg_fps = mean([0 if dt == 0 else 1 / dt for dt in self.dt_history])

		self.dbg_counter.y = self.height -17
		self.dbg_counter.text = "%6d %6.2f ms %6.2f fps" % (self.counter, avg_dt * 1000, avg_fps)
		self.dbg_counter.draw()

		self.counter += 1


		if flip:
			self.flip()
		
		if self.fps_limit:
			Timer.accurate_sleep_until(timer.prev_ts + int(Timer.freq / self.fps_limit))

		self.dt = min(timer.step(), 1 / 20) # max dt

		self.dt_history.append(self.dt)

	def on_close(self):
		self.quit = True

	def on_key_press(self, symbol, modifiers): # override to not close on ESC
		if (symbol == key.F11):
			self.is_fullscreen = not self.is_fullscreen
			self.set_fullscreen(self.is_fullscreen)

	def run(self):
		while not self.quit:
			event = self.dispatch_events()
			if event:
				print(event)

			self._draw()
			
	def on_draw(self):
		self._draw(False)
