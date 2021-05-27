# Fix to make gi work.
import pgi
pgi.install_as_gi()
import gi
gi.require_version('Wnck', '3.0')
gi.require_version('Gtk', '3.0')

from typing import Iterator, Optional
from dataclasses import dataclass
from gi.repository import Wnck, Gtk

@dataclass
class Window:
    """A wrapper around Wnck providing methods to manipulate and query windows."""
    window: Wnck.Window
    screen = Wnck.Screen.get_default()

    @property
    def name(self) -> str:
        return self.window.get_name()

    @classmethod
    def get_all_windows(cls) -> Iterator:
        cls.screen.force_update()
        while Gtk.events_pending():
            Gtk.main_iteration()
        return map(Window, cls.screen.get_windows())

    @classmethod
    def get_active_window(cls):
        cls.screen.force_update()
        while Gtk.events_pending():
            Gtk.main_iteration()
        return Window(cls.screen.get_active_window())

    def activate(self):
        self.window.activate(1)
        return self

    def close(self):
        self.window.close(1)
        return self

    def get_size(self) -> tuple[int, int, int, int]:
        return self.window.get_geometry()

    def get_icon(self):
        return self.window.get_icon()  # PixBuf

    def is_active(self) -> bool:
        return self.window.is_active()

    def is_on_top(self):
        return self.window.is_above()

    def is_at_bottom(self):
        return self.window.is_below()

    def is_maximized(self):
        return self.window.is_maximized()

    def is_minimized(self):
        return self.window.is_minimized()

    def is_fullscreen(self):
        return self.window.is_fullscreen()

    def is_maximized_vertically(self):
        return self.window.is_maximized_vertically()

    def is_maximized_horizontally(self):
        return self.window.is_maximized_horizontally()

    def always_on_top(self, toggle: bool):
        self.window.make_above() if toggle else self.window.unmake_above()
        return self

    def always_at_bottom(self, toggle: bool):
        self.window.make_below() if toggle else self.window.unmake_below()
        return self

    def maximize(self):
        self.window.maximize()
        return self

    def minimize(self):
        self.window.minimize()
        return self

    def maximize_horizontally(self):
        self.window.maximize_horizontally()
        return self

    def maximize_vertically(self):
        self.window.maximize_vertically()
        return self

    def unmaximize(self):
        self.window.unmaximize()
        return self

    def unminimize(self):
        self.window.unminimize()
        return self

    def unmaximize_horizontally(self):
        self.window.unmaximize_horizontally()
        return self

    def unmaximize_vertically(self):
        self.window.unmaximize_vertically()
        return self

    def fullscreen(self):
        self.window.set_fullscreen()
        return self

    def set_geometry(self, x, y, w, h):
        self.window.set_geometry(x, y, w, h)
        return self

    @classmethod
    def get(cls, title: str, strict: bool = False) -> Optional['Window']:
        for window in cls.get_all_windows():
            # Strict disabled; Title doesnt have to match exactly
            name = window.window.get_name()
            if strict:
                cond = title == name
            else:
                cond = title in name
            if cond:
                return window
