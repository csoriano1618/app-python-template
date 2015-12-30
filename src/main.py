import sys
import signal
import os
import locale
import gettext

# Make sure we'll find the pygobject module in any prefix
sys.path.insert(1, "@pyexecdir@")
# Make sure we'll find the app module in any prefix
sys.path.insert(1, "@pythondir@")

try:
    import gi
except ImportError:
    sys.exit("Missing pygobject")
try:
    gi.require_version('GLib', '2.0')
    gi.require_version('Gio', '2.0')
    gi.require_version('GObject', '2.0')
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
except ValueError as e:
    sys.exit("Missing dependency: {}".format(e))


from gi.repository import Gio
from gi.repository import Gtk
from usage.application import Application

def install_excepthook():
    """ Make sure we exit when an unhandled exception occurs. """
    old_hook = sys.excepthook

    def new_hook(etype, evalue, etb):
        old_hook(etype, evalue, etb)
        while Gtk.main_level():
            Gtk.main_quit()
        sys.exit()
    sys.excepthook = new_hook

if __name__ == "__main__":
    install_excepthook()

    locale.bindtextdomain("usage", "@localedir@")
    locale.textdomain("usage")
    gettext.bindtextdomain("usage", "@localedir@")
    gettext.textdomain("usage")

    resource = Gio.resource_load(os.path.join("@pkgdatadir@", "usage.gresource"))
    Gio.Resource._register(resource)

    app = Application()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)

