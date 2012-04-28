import sys
import code


# initialize gtkclutter
if __name__ == "__main__":
	from gi.repository import GtkClutter

	GtkClutter.init(sys.argv)

from gi.repository import Clutter, GLib, Gio, Gtk, Gdk, GtkSource

from gui import *
from sandbox import *
import user


class VivoApp(Gtk.Application):
	def __init__(self):
		super().__init__(
			application_id="apps.Vivo",
			#flags=Gio.ApplicationFlags.HANDLES_OPEN
		)
		
		self.connect("activate", self.on_activate)
	#	self.connect("command-line", self.on_command_line)

	def on_activate(self, data=None):

		self.mainwin = MainWindow()
		self.mainwin.show_all()
		self.add_window(self.mainwin)

		self.mainwin.editor.connect('changed', self.on_editor_change)

		self.mainwin.view.reset()

		self.sandbox = Sandbox()
		self.sandbox.connect('started', self.on_sandbox_started)
		self.sandbox.connect('stopped', self.on_sandbox_stopped)

		self._has_update = False

		#self.env = user.Environment()
		#self.env.connect('reset', self.on_env_reset)
		##self.env.connect('run', self.on_env_run)

		#self.env.default_vars['Screen'] = user.Screen(self.mainwin.view.stage)

		#self.env.run("print('hello world')\n")

	def on_update_timeout(self, data=None):
		if not self._has_update:
			return False

		self.sandbox.get('vivo_update')()


	def on_sandbox_started(self, sandbox):
		sandbox.reset()

		sandbox.setup(locals={
			'Screen'   : user.Screen(self.mainwin.view.stage),
			'Animation' : user.Animation,
			'Timeline' : user.Timeline,
			'Color'    : user.Color,
			'Text'     : user.Text,
			'Rectangle': user.Rectangle,

			# Colors
			'BLACK'    : user.Color(),
			'WHITE'    : user.Color(255,255,255),
			'RED'      : user.Color(r=255),
			'GREEN'    : user.Color(g=255),
			'BLUE'     : user.Color(b=255),

		})

	def on_sandbox_stopped(self, sandbox):
		if sandbox.exists('vivo_main'):
			sandbox.get('vivo_main')()
	

		if not self._has_update and sandbox.exists('vivo_update'):
			self._has_update = True
			GLib.timeout_add(int(1000 / 24), self.on_update_timeout, None)
		pass

	def on_editor_change(self, editor, data=None):
		buff = editor.buffer
	
		source = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), False)
		self.sandbox.exec(source)
		#source.replace("\r\n","\n")


#		try:
#			self.interpreter = code.InteractiveInterpreter(locals={
#				'__name__' : '__livepy__',
#				'__doc__' : None,
#				'Stage' : self.mainwin.view.stage,
#				'View'  : self.mainwin.view,
#				'Path'  : Clutter.Path,
#				'Color' : user.Color,
#				'Text'  : user.Text,
#				'Rectangle'  : user.Rectangle,
#				'GestureAction' : Clutter.GestureAction,
#				'BLACK' : user.Color(),
#				'WHITE' : user.Color(255,255,255),
#				})
#			codeobj = compile(source,'<string>','exec')
#			if codeobj:
#				self.mainwin.view.reset()
#				self.interpreter.runcode(codeobj)
#
#			#self.interpreter.runsource(source)
#		except Exception as e:
#			#str(e)
#			pass

		
	
	def on_command_line(self, app, cmdline, data=None):
		args = cmdline.get_arguments()



if __name__ == "__main__":
	app = VivoApp()
	app.run(sys.argv)


