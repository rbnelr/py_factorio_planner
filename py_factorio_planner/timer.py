import ctypes as ctypes

def get_freq():
    i = ctypes.c_ulonglong()
    ctypes.windll.kernel32.QueryPerformanceFrequency(ctypes.byref(i))
    return i.value

QueryPerformanceCounter = ctypes.windll.kernel32.QueryPerformanceCounter

def get_timestamp():
    i = ctypes.c_ulonglong()
    QueryPerformanceCounter(ctypes.byref(i))
    return i.value

class Timer:
	# frequency of Windows QPC Timer ticks
	freq = get_freq()
	
	# *_ts values are raw Windows QPC Timer timestamps

	# use cases:
	# 
	# 1.
	#   measure_time = Timer.begin()
	#   blah()
	#   time_elapsed = measure_time.end()
	#
	# 2. (elapsed_A + elapsed_B + elapsed_C) == elapsed_total
	#   measure_time = Timer.begin()
	#   blah_A()
	#   elapsed_A = measure_time.step()
	#   blah_B()
	#   elapsed_B = measure_time.step()
	#   blah_C()
	#   elapsed_total = measure_time.end()
	#   elapsed_C = measure_time.step_period
	#
	# e.
	#   measure_time = Timer.begin()
	#   dt = 0
	#   
	#   while (run): # game loop
	#       blah()
	#       dt = measure_time.step()
	#

    # begin a timer (this returns a new timer)
	def begin():
		t = Timer()
		t.begin_ts = get_timestamp()
		t.prev_ts = t.begin_ts
		return t
	
    # time since begin(), in seconds
	def end(self):
		self.end_ts = get_timestamp()
		self.step_period = (self.end_ts -self.prev_ts) / Timer.freq
		self.full_period = (self.end_ts -self.begin_ts) / Timer.freq

		return self.full_period

    # time since begin() or prev step(), in seconds
	def step(self):
		step_ts = get_timestamp()
		self.step_period = (step_ts -self.prev_ts) / Timer.freq

		self.prev_ts = step_ts
		return self.step_period

	def get_time_since_step():
		now_ts = get_timestamp()
		return (now_ts -self.step_ts) / Timer.freq
	
    # time since begin() or prev step(), in seconds
	def get_time_since_begin():
		now_ts = get_timestamp()
		return (now_ts -self.begin_ts) / Timer.freq


	def accurate_sleep_until(target_ts):
		diff_sec = (target_ts -get_timestamp()) / Timer.freq

		if int(diff_sec > 0):
			ctypes.windll.kernel32.Sleep(int(diff_sec)) # sleep whole milliseconds

		while get_timestamp() < target_ts:
			pass # busy wait
