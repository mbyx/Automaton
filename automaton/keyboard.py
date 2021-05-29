from .consts import SHIFT_CODES, SCANCODES
from dataclasses import dataclass
from .key import Key
import evdev

# The inverse of SCANCODES and SHIFT_CODES
sc = {v: k for k, v in SCANCODES.items()}
shc = {v: k for k, v in SHIFT_CODES.items()}

@dataclass
class Keyboard:
    """Internally used to provide keyboard input and query it."""
    ui: evdev.UInput

    def press(self, key: Key):
        """Presses the specified key. Syncs immediately."""
        self.ui.write(evdev.ecodes.EV_KEY, key, 1)
        self.ui.syn()

    def release(self, key: Key):
        """Releases the specified key. Syncs immediately."""
        self.ui.write(evdev.ecodes.EV_KEY, key, 0)
        self.ui.syn()

    def tap(self, key: Key):
        """Presses and releases a key."""
        self.press(key)
        self.release(key)

    def type(self, txt: str):
        """Types a string of characters. String must be ASCII. UTF-8 is not supported... yet."""
        for chr in txt:
            if chr in shc:
                self.press(Key.LShift)  # Press shift to change to Shifted Keys
                self.tap(shc[chr])
                self.release(Key.LShift)
            else:
                self.tap(sc[chr])

    def is_pressed(self, key: Key) -> bool:
        """Determines if the key is pressed. NOTE: This only works after redirection has started."""
        return key in self.ui.device.active_keys()

    def set_state(self, key: Key, state: bool):
        """Sets the state of a lock key to ON or OFF, True or False"""
        if self._is_lock_key(key):
            if self.is_toggled(key) and state == False:
                self.tap(key)
            elif not self.is_toggled(key) and state == True:
                self.tap(key)

    def is_toggled(self, key: Key) -> bool:
        """Determines if a key (a lock key) is toggled or not."""
        leds = self.ui.device.leds()
        if key == Key.NumLock:
            return 0 in leds
        elif key == Key.CapsLock:
            return 1 in leds
        elif key == Key.ScrollLock:
            return 2 in leds
        else:
            return False

    def _is_lock_key(self, key: Key) -> bool:
        """Determines whether a key is CapsLock, NumLock or ScrollLock."""
        return key in [Key.NumLock, Key.CapsLock, Key.ScrollLock]
