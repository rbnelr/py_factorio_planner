import pyglet
import pyglet.gl as gl
import pyglet.window.key as key
import collections

from timer import Timer

class Button_State:
	def __init__(self):
		self.went_down = False
		self.went_up = False
		self.is_down = False
		
	def clear(self):
		self.went_down = False
		self.went_up = False

	def update(self, state):
		if state == True:
			self.went_down = True
		else:
			self.went_up = True
		
		self.is_down = state

class Input:
	def __init__(self):
		self.mouse_pos_px = (-1,-1)

		self.lmb = Button_State()
		self.mmb = Button_State()
		self.rmb = Button_State()

		self.button = {name: Button_State() for name in key._key_names.values()}

	def clear(self):
		self.lmb.clear()
		self.mmb.clear()
		self.rmb.clear()

		for b in self.button.values():
			b.clear()

class Window(pyglet.window.Window):
	def __init__(self):
		super(Window, self).__init__(1280,720, resizable=True, caption="Py Factorio Planner", vsync=True)

		self.user_draw = None

		self.quit = False
		self.is_fullscreen = False # fullscreen already in pyglet window?

		
		self.counter = 0

		self.timer = Timer.begin()
		self.fps_limit = 160.0

		self.dt = 0.0

		self.dt_history = collections.deque(maxlen = 60)
		

		self.dbg_counter = pyglet.text.Label(font_name="Consolas", font_size=17)

		self.inp = Input()

	def draw(self, f):
		self.user_draw = f

	def _draw(self, flip=True):
		if self.user_draw:
			self.user_draw(self.inp, self.dt)
		
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
			Timer.accurate_sleep_until(self.timer.prev_ts + int(Timer.freq / self.fps_limit))

		self.dt = min(self.timer.step(), 1 / 20) # max dt

		self.dt_history.append(self.dt)

	def on_close(self):
		self.quit = True

	def button_change(self, symbol, state):
		self.inp.button[key._key_names[symbol]].update(state)

	def on_key_press(self, symbol, modifiers): # override to not close on ESC
		if (symbol == key.F11):
			self.is_fullscreen = not self.is_fullscreen
			self.set_fullscreen(self.is_fullscreen)

		self.button_change(symbol, True)

	def on_key_release(self, symbol, modifiers):
		self.button_change(symbol, False)

	def on_mouse_motion(self, x, y, dx, dy):
		#print("on_mouse_motion(%d, %d, %d, %d)" % (x, y, dx, dy))
		self.inp.mouse_pos_px = (x,y)
	
	def mouse_button_change(self, button_indx, state):
		#print("MB%d went %s" % (button_indx, ("down","up")[0 if state else 1]))
		if button_indx >= 1 and button_indx <= 3:
			(self.inp.lmb, self.inp.mmb, self.inp.rmb)[button_indx -1].update(state)

	def on_mouse_press(self, x, y, button, modifiers):
		self.mouse_button_change(button, True)
	def on_mouse_release(self, x, y, button, modifiers):
		self.mouse_button_change(button, False)

	def run(self):
		while not self.quit:
			self.inp.clear()

			event = self.dispatch_events()
			if event:
				print(event)

			self._draw()
			
	def on_draw(self):
		self._draw(False)
