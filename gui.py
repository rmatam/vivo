from gi.repository import GObject, Gtk, Gdk, GtkClutter, GtkSource

class Editor(Gtk.ScrolledWindow):
	__gsignals__ = {
		"changed": (GObject.SIGNAL_RUN_FIRST, None, (object, )),
	}

	def __init__(self):
		super().__init__(None, None)

		langmngr = GtkSource.LanguageManager.get_default()

		self.buffer = GtkSource.Buffer.new_with_language(langmngr.get_language("python"))
		self.view = GtkSource.View.new_with_buffer(self.buffer)

		self.buffer.set_highlight_syntax(True)

		self.view.set_auto_indent(True)
		self.view.set_tab_width(4)
		self.view.set_smart_home_end(GtkSource.SmartHomeEndType.ALWAYS)
		self.view.set_show_line_numbers(True)

		self.add(self.view)
		
		self.buffer.connect('changed', self.on_buffer_changed)

	def on_buffer_changed(self, buff, data=None):
		self.emit("changed", self)

#class View(Gtk.EventBox):
class View(GtkClutter.Embed):
	def __init__(self):
		super().__init__()

		#self.view  = GtkClutter.Embed()
		self.view  = self
		self.stage = self.view.get_stage()

		self.set_can_focus(True)
		self.connect('button-release-event', self.on_button_release)

		#self.add(self.view)
		#self.set_events(Gdk.EventMask.ALL_EVENTS_MASK)

	def on_button_release(self, widget, event, data=None):
		self.grab_focus()

	def reset(self):
		signals = list(GObject.signal_list_ids(type=Gtk.Widget))
		signals = filter(lambda s: self.handler_is_connected(s), signals)

		for s in signals:
			self.disconnect(s)


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


