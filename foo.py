/bin/bash: s: command not found
import sys
import code
from gi.repository import Gio, Gtk, Gdk, Clutter, GtkClutter, GtkSource



# GUI
##################################################################################################

class Editor(Gtk.ScrolledWindow):
	def __init__(self):
		super().__init__(None, None)

		langmngr = GtkSource.LanguageManager.get_default()

		self.buffer = GtkSource.Buffer.new_with_language(langmngr.get_language("python"))
		self.view = GtkSource.View.new_with_buffer(self.buffer)

		self.buffer.set_highlight_syntax(True)

		self.add(self.view)

class View(GtkClutter.Embed):
	def __init__(self):
		super().__init__()

		self.stage = self.get_stage()


class MainWindow(Gtk.Window):
	def __init__(self):
		super().__init__(type=Gtk.WindowType.TOPLEVEL)

		self.pane = Gtk.HPaned()
		self.editor = Editor()
		self.view = View()

		self.pane.pack1(self.editor, True, True)
		self.pane.pack2(self.view, True, False)

		self.add(self.pane)
		self.set_title("Vivo")
		
		screen = Gdk.Screen.get_default()
		self.pane.set_position(screen.get_width() * 0.45)

		self.set_default(self.editor)
		self.set_default_size(screen.get_width() * 0.9, screen.get_height() * 0.8)
		self.set_position(Gtk.WindowPosition.CENTER)

def VivoColor(r=0,g=0,b=0,a=255):
	c = Clutter.Color()
	c.red, c.green, c.blue, c.alpha = r, g, b, a
	return c

class Vivo(Gtk.Application):
	def __init__(self):
		super().__init__(application_id="apps.Vivo")
		
		self.connect("activate", self.on_activate)
	#	self.connect("command-line", self.on_command_line)

	def on_activate(self, data=None):
		GtkClutter.init([])


		self.mainwin = MainWindow()
		self.mainwin.show_all()
		self.add_window(self.mainwin)

		self.interpreter = code.InteractiveInterpreter(locals={
			'__name__' : '__livepy__',
			'__doc__' : None,
			'Stage' : self.mainwin.view.stage,
			'Path'  : Clutter.Path,
			'Color' : VivoColor,
			'Text'  : Clutter.Text
			})

		self.mainwin.editor.view.get_buffer().connect('changed', self.on_editor_change)

	def on_editor_change(self, buff, data=None):
		source = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), False)
		source.replace("\r\n","\n")

		try:
			codeobj = compile(source,'<string>','exec')
			if codeobj:
				self.interpreter.runcode(codeobj)

			#self.interpreter.runsource(source)
		except Exception as e:
			#str(e)
			pass

		
	
	def on_command_line(self, app, cmdline, data=None):
		args = cmdline.get_arguments()



if __name__ == "__main__":
	app = Vivo()
	app.run(sys.argv)


