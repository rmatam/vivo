import code
from gi.repository import GObject, Pango, Clutter

class Timeline():
	
	def __init__(self):
		self.tl = Clutter.Timeline()

	def __getattr__(self, name):
		return getattr(self.tl, name)

class Animation():
	
	def __init__(self,animation):
		self.ani = animation

	def __getattr__(self, name):
		return getattr(self.ani, name)

class Color():
	"""
	Wrapper class for Clutter.Color.

	This class is a workaround for some subclassing problems.
	"""
	def __init__(self,r=0,g=0,b=0,a=255):
		self._color = Clutter.Color()
		self.red, self.green, self.blue, self.alpha = r, g, b, a
	
	@classmethod
	def from_str(self, color):
		c = Color()
		c.color.from_string(color)
		return c
	
	@property
	def color(self):
		return self._color
	
	@property
	def red(self):
		return self.color.red

	@red.setter
	def red(self, red):
		self.color.red = red

	@property
	def green(self):
		return self.color.green

	@green.setter
	def green(self, green):
		self.color.green = green

	@property
	def blue(self):
		return self.color.blue

	@blue.setter
	def blue(self, blue):
		self.color.blue = blue

	@property
	def alpha(self):
		return self.color.alpha

	@alpha.setter
	def alpha(self, alpha):
		self.color.alpha = alpha

class Actor():
	def __init__(self, actor):
		self._actor = actor
		self._actor.set_reactive(True)
		
		self._actor_class = type(self._actor)

		self.connect = self._actor.connect
	
	def reset_signals(self): pass
	#	signals = list(GObject.signal_list_ids(type=type(self)))
	#	
	#	for sid in signals:
	#		if self._actor.handler_is_connected(sid):
	#			print("disconnecting -- " + str(GObject.signal_name(sid)))
	#			self._actor.disconnect(sid)

	#def connect(self, event, handler, *args):

	#	if len(args):
	#		self._actor.connect(event, handler, *args)
	#	else:
	#		self._actor.connect(event, handler)

	def animate(self, mode, duration, properties={}):

		return Animation(self._actor.animatev(mode, duration,list(properties.keys()), list(properties.values())))

	@property
	def actor(self):
		return self._actor

	@property
	def x(self):
		return self.actor.get_x()

	@x.setter
	def x(self, x):
		self.actor.set_x(x)

	@property
	def y(self):
		return self.actor.get_y()

	@y.setter
	def y(self, y):
		return self.actor.set_y(y)

	@property
	def width(self):
		return self.actor.get_width()

	@width.setter
	def width(self, width):
		return self.actor.set_width(width)

	@property
	def height(self):
		return self.actor.get_height()

	@height.setter
	def height(self, height):
		return self.actor.set_height(height)

	
class Colored():
	@property
	def color(self):
		return self.actor.get_color()

	@color.setter
	def color(self, color):
		self.actor.set_color(color.color)

class Rectangle(Actor,Colored):
	def __init__(self, w=10, h=10):
		super().__init__(Clutter.Rectangle())

		self.width, self.height = w, h

class Text(Actor,Colored):
	def __init__(self, text, font="sans 16"):
		super().__init__(Clutter.Text())

		self._font = Pango.FontDescription.from_string(font)

		self.actor.set_font_description(self._font)
		self.actor.set_text(text)

	@property
	def font(self):
		return self._font.to_string()

	@font.setter
	def font(self, font):
		self._font = Pango.FontDescription.from_string(font)
		self.actor.set_font_description(self._font)

	@property
	def text(self):
		return self.actor.get_text()

	@text.setter
	def text(self, text):
		self.actor.set_text(text)


class Screen(Actor):
	def __init__(self, stage):
		super().__init__(stage)

		stage.set_accept_focus(True)
		stage.set_motion_events_enabled(True)
		
		self.timeline = Timeline()

	def __del__(self):
		self.reset_signals()
		self.actor.remove_all()


	def put(self, actor):
		self.actor.add_actor(actor.actor)

