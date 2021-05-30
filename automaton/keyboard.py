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

    def press(self, *keys: Key):
        """Presses the specified key/keys. Syncs immediately."""
        for key in keys:
            self.ui.write(evdev.ecodes.EV_KEY, key, 1)
            self.ui.syn()

    def release(self, *keys: Key):
        """Releases the specified key/keys. Syncs immediately."""
        for key in keys:
            self.ui.write(evdev.ecodes.EV_KEY, key, 0)
            self.ui.syn()

    def tap(self, *keys: Key):
        """Presses and releases a key."""
        self.press(keys)
        self.release(keys)

    def type(self, txt: str):
        """Types a string of unicode characters. This works by using the Ctrl+Shift+U key combo
        in Linux. Some distributions that use Qt may not have this key combo."""
        for chr in txt:
            self.press(Key.LCtrl, Key.LShift)
            self.tap(Key.U)
            self.release(Key.LCtrl, Key.LShift)
            self.type_ascii(hex(ord(chr))[2:])
            self.tap(Key.Enter)

    def type_ascii(self, txt: str):
        """Types a string of characters. String must be ASCII."""
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
