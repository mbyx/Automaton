from dataclasses import dataclass
from .key import Key
import evdev

@dataclass
class Mouse:
    """Internally used to provide mouse manipulation and queries"""
    ui: evdev.UInput

    def press(self, key: Key):
        """Presses the specified key as long as its a mouse button. Syncs immediately."""
        if self._is_mouse_button(key):
            self.ui.write(evdev.ecodes.EV_KEY, key, 1)
            self.ui.syn()

    def release(self, key: Key):
        """Releases the specified key as long as its a mouse button. Syncs immediately."""
        if self._is_mouse_button(key):
            self.ui.write(evdev.ecodes.EV_KEY, key, 0)
            self.ui.syn()

    def tap(self, key: Key):
        """Presses and releases the specified key."""
        self.press(key)
        self.release(key)

    def is_pressed(self, key: Key) -> bool:
        """Determines whether a key is pressed or not."""
        return key in self.ui.device.active_keys()

    def move_rel(self, x: int, y: int):
        """Moves the mouse in relative coordinates to x, y. Syncs immediately."""
        self.ui.write(evdev.ecodes.EV_REL, evdev.ecodes.REL_X, x)
        self.ui.write(evdev.ecodes.EV_REL, evdev.ecodes.REL_Y, y)
        self.ui.syn()

    def _is_mouse_button(self, key: Key) -> bool:
        """Determines if the key is a mouse button. This includes Left, Middle, Right Buttons as well
        as XButton and SideButton."""
        if key in [Key.LeftButton, Key.RightButton, Key.MiddleButton, Key.XButton, Key.SideButton]:
            return True
        return False
