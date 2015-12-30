from gi.repository import GObject, Gtk, Gio, GLib
from gettext import gettext as _

from usage.log import log


class Window(Gtk.ApplicationWindow):

    @log
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title=_("Usage"))
        self.settings = Gio.Settings.new('org.gnome.Usage')
        self.set_icon_name('usage')

        self._restore_saved_size()
        self._setup_ui()

    def _setup_ui(self):
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gnome/Usage/ui/window.ui')
        self._stack_switcher = builder.get_object('stack_switcher')
        self._pages_stack = builder.get_object('pages_stack')

        header_bar = Gtk.HeaderBar.new()
        header_bar.set_show_close_button(True)
        header_bar.set_custom_title(self._stack_switcher)
        self.set_titlebar(header_bar)

        self.show_all()

    def _restore_saved_size(self):
        # Restore window size from gsettings
        size_setting = self.settings.get_value('window-size')
        if isinstance(size_setting[0], int) and isinstance(size_setting[1], int):
            self.resize(size_setting[0], size_setting[1])

        position_setting = self.settings.get_value('window-position')
        if len(position_setting) == 2 \
           and isinstance(position_setting[0], int) \
           and isinstance(position_setting[1], int):
            self.move(position_setting[0], position_setting[1])

        if self.settings.get_value('window-maximized'):
            self.maximize()

        # Save changes to window size
        self.connect("window-state-event", self._on_window_state_event)
        self.configure_event_handler = self.connect("configure-event", self._on_configure_event)

    def _on_window_state_event(self, widget, event):
        self.settings.set_boolean('window-maximized',
                                  'GDK_WINDOW_STATE_MAXIMIZED' in event.new_window_state.value_names)

    def _on_configure_event(self, widget, event):
        with self.handler_block(self.configure_event_handler):
            GLib.idle_add(self._store_window_size_and_position, widget, priority=GLib.PRIORITY_LOW)

    def _store_window_size_and_position(self, widget):
        size = widget.get_size()
        self.settings.set_value('window-size', GLib.Variant('ai', [size[0], size[1]]))

        position = widget.get_position()
        self.settings.set_value('window-position', GLib.Variant('ai', [position[0], position[1]]))

