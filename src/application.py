import gi
gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Gdk, Notify
from gettext import gettext as _
from usage.log import *
from usage.window import Window


class Application(Gtk.Application):

    def __repr__(self):
        return '<Application>'

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id='org.gnome.Usage',
                                 flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        GLib.set_application_name(_("Usage"))
        GLib.set_prgname('usage')

        self._add_command_line_options()

        self._window = None

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if(options.contains("debug")):
            logging.basicConfig(level=logging.DEBUG,
                                format="%(asctime)s %(levelname)s\t%(message)s",
                                datefmt="%H:%M:%S")
        else:
            logging.basicConfig(level=logging.WARN,
                                format="%(asctime)s %(levelname)s\t%(message)s",
                                datefmt="%H:%M:%S")

        self.do_activate()

        return -1

    def build_app_menu(self):
        actionEntries = [
            ('about', self.about),
            ('help', self.help),
            ('quit', self.quit),
        ]

        for action, callback in actionEntries:
            simpleAction = Gio.SimpleAction.new(action, None)
            simpleAction.connect('activate', callback)
            self.add_action(simpleAction)

    def _add_command_line_options(self):
        self.add_main_option("debug", b'd', GLib.OptionFlags.NONE, GLib.OptionArg.NONE,
                             _("Show debug output"), None)

    def help(self, action, param):
        Gtk.show_uri(None, "help:usage", Gdk.CURRENT_TIME)

    def about(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gnome/Usage/ui/about-dialog.ui')
        about = builder.get_object('about_dialog')
        about.set_transient_for(self._window)
        about.connect("response", self.about_response)
        about.show()

    def about_response(self, dialog, response):
        dialog.destroy()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.build_app_menu()

    @log
    def quit(self, action=None, param=None):
        self._window.destroy()

    def do_activate(self):
        if not self._window:
            self._window = Window(self)
        self._window.present()

