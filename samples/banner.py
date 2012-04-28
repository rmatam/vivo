from gi.repository import Clutter,GLib,GObject


text = Text("Vivo Live Programming Environment", "inconsolata 24")
text.color = Color.from_str("black")
text.actor.set_anchor_point(text.width / 2, text.height / 2)
text.x = Screen.width/2
text.y = Screen.height/2

v = Clutter.Vertex()
v.x=text.width/2
v.y=text.width/2
v.z=0

props= {
	"fixed::rotation-center-y": v,
	"rotation-angle-y": 360.0
}
a = text.animate(Clutter.AnimationMode.LINEAR, 3000, props)

a.set_loop(True)
Screen.put(text)
