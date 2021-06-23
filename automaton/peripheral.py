from .consts import LockState, SCANCODES, SHIFT_CODES, Input
from typing import Callable, Optional
from dataclasses import dataclass, field
from .input import Key
import evdev

# The inverse of SCANCODES and SHIFT_CODES
sc = {v: k for k, v in SCANCODES.items()}
shc = {v: k for k, v in SHIFT_CODES.items()}

Subscriber = Callable[[evdev.InputEvent], Optional[str]]

@dataclass
class Peripheral:
    """Internally used to provide keyboard input and query it. Note: All query methods
    will only work after Automaton.run() is called. This means they can only be used
    inside of action callbacks, unless you choose to use a separate thread."""
    ui: evdev.UInput
    PRESS_CALLBACKS: list[Subscriber] = field(default_factory = list)
    RELEASE_CALLBACKS: list[Subscriber] = field(default_factory=list)

    def on_press(self, callback: Subscriber):
        """Registers a callback which is called when a key is pressed."""
        self.PRESS_CALLBACKS.append(callback)

    def on_release(self, callback: Subscriber):
        """Registers a callback which is called when a key is released."""
        self.RELEASE_CALLBACKS.append(callback)

    def update(self, event: evdev.InputEvent):
        """Using the given event, it determines which callback to call."""
        callbacks = self.PRESS_CALLBACKS if event.value >= 1 else self.RELEASE_CALLBACKS
        for callback in callbacks:
            if (txt := callback(event)) is not None:
                self.type(txt)

    def press(self, *keys: Input):
        """Presses the specified key/keys. Syncs immediately."""
        for key in keys:
            self.ui.write(evdev.ecodes.EV_KEY, int(key), 1)
            self.ui.syn()

    def release(self, *keys: Input):
        """Releases the specified key/keys. Syncs immediately."""
        for key in keys:
            self.ui.write(evdev.ecodes.EV_KEY, int(key), 0)
            self.ui.syn()

    def tap(self, *keys: Input):
        """Presses and releases a key."""
        self.press(*keys)
        self.release(*keys)

    def type(self, txt: str):
        """Types a string of unicode characters. This works by using the Ctrl+Shift+U key combo
        in Linux. Some distributions that use Qt may not have this key combo."""
        for chr in txt:
            if chr in shc or chr in sc:
                self.type_ascii(chr)
            else:
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

    def is_pressed(self, key: Input) -> bool:
        """Determines if the key is pressed. NOTE: This only works after redirection has started."""
        return key.value in self.ui.device.active_keys()

    def set_state(self, key: Input, state: LockState):
        """Sets the state of a lock key to ON or OFF, True or False"""
        if self._is_lock_key(key):
            if self.is_toggled(key) and state is LockState.Off:
                self.tap(key)
            elif not self.is_toggled(key) and state is LockState.On:
                self.tap(key)

    def is_toggled(self, key: Input) -> bool:
        """Determines if a key (a lock key) is toggled or not."""
        leds = self.ui.device.leds()
        state = False
        if key == Key.NumLock:
            state = 0 in leds
        elif key == Key.CapsLock:
            state = 1 in leds
        elif key == Key.ScrollLock:
            state = 2 in leds
        return LockState.On if state is True else LockState.Off

    def _is_lock_key(self, key: Input) -> bool:
        """Determines whether a key is CapsLock, NumLock or ScrollLock."""
        return key in [Key.NumLock, Key.CapsLock, Key.ScrollLock]

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
