import code
import inspect
from gi.repository import GObject

class Sandbox(GObject.GObject, code.InteractiveInterpreter):
	__gsignals__ = {
		'reseted':  (GObject.SIGNAL_RUN_FIRST, None, tuple()),
		'started': (GObject.SIGNAL_RUN_FIRST, None, tuple()),
		'stopped': (GObject.SIGNAL_RUN_FIRST, None, tuple())
	}

	def __init__(self):
		super().__init__()
	
		self.locals={}
		self.globals={
			'__name__': '__vivo__',
			'__doc__': None,
			'globalvar': self.globalvar,
		}

	def setup(self, locals={}):
		self.locals.update(self.globals)
		self.locals.update(locals)

	def reset(self):
		self.locals.clear()

		self.emit('reseted')



	def exec(self, source, filename='<live>'):
		source.replace("\r\n", "\n")

		try:
			codeobj = compile(source, filename, 'exec')
			if codeobj:
				self.emit('started')
				super().runcode(codeobj)
				self.emit('stopped')

		except Exception as e:
			#print(e)
			pass
	
	def globalvar(self, name, value=None):
		if name not in self.globals:
			self.globals[name] = value
			self.locals.update(self.globals)

	@property
	def classes(self):
		return [c for c in self.locals.values() if inspect.isclass(c)]

	@property
	def functions(self):
		return [f for f in self.locals.values() if inspect.isfunction(f)]

	def put(self, name, value):
		self.locals[name] = value
	
	def get(self, name):
		return self.locals[name]

	def exists(self, name):
		return name in self.locals
	
	def runcode(self, codeobj): pass
	def runsource(self, source, filename='<string>',symbol='single'): pass


