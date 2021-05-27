# Fix to make gi work.
import pgi
pgi.install_as_gi()
import gi
gi.require_version('Wnck', '3.0')

from dataclasses import dataclass
from select import select
import evdev, atexit
from .key import Key

# Add Dialogues
import zenipy as Dialog

SCANCODES: dict[int, str] = {
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0', 12: '-', 13: '=',
    16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y', 22: 'u', 23: 'i', 24: 'o', 25: 'p', 26: '[', 27: ']', 43: '\\',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h', 36: 'j', 37: 'k', 38: 'l', 39: ';', 40: '"', 41: '`',
    44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b', 49: 'n', 50: 'm', 51: ',', 52: '.', 53: '/', 57: ' '
}

SHIFT_CODES: dict[int, str] = {
    2: '!', 3: '@', 4: '#', 5: '$', 6: '%', 7: '^', 8: '&', 9: '*',
    10: '(', 11: ')', 12: '_', 13: '+', 16: 'Q', 17: 'W', 18: 'E', 19: 'R',
    20: 'T', 21: 'Y', 22: 'U', 23: 'I', 24: 'O', 25: 'P', 26: '{', 27: '}',
    30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J', 37: 'K', 38: 'L', 39: ':',
    40: '\'', 41: '~', 43: '|', 44: 'Z', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N',
    50: 'M', 51: '<', 52: '>', 53: '?'
}

CHAR_CODES = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 44, 45, 46, 47, 48, 49, 50]

sc = {v: k for k, v in SCANCODES.items()}
shc = {v: k for k, v in SHIFT_CODES.items()}

HOTSTRING_TRIGGERS: set[Key] = {
    Key.Space, Key.Backspace, Key.Enter, Key.Tab
}


ON = True
OFF = False

PRESS = "PRESS"
RELEASE = "RELEASE"
HOLD = "HOLD"


@dataclass
class Keyboard:
    """Internally used to provide keyboard input and query it."""
    ui: evdev.UInput
    
    def press(self, key: Key):
        self.ui.write(evdev.ecodes.EV_KEY, key, 1)
        self.ui.syn()

    def release(self, key: Key):
        self.ui.write(evdev.ecodes.EV_KEY, key, 0)
        self.ui.syn()

    def tap(self, key: Key):
        self.press(key)
        self.release(key)

    def type(self, txt: str):
        for chr in txt:
            if chr in shc:
                self.press(Key.LShift)
                self.tap(shc[chr])
                self.release(Key.LShift)
            else:
                self.tap(sc[chr])

    def is_pressed(self, key: Key) -> bool:
        return key in self.ui.device.active_keys()

    def set_state(self, key: Key, state: bool):
        if self._is_lock_key(key):
            if self.is_toggled(key) and state == False:
                self.tap(key)
            elif not self.is_toggled(key) and state == True:
                self.tap(key)

    def is_toggled(self, key: Key) -> bool:
        leds = self.ui.device.leds()
        if key == Key.NumLock:
            return 0 in leds
        elif key == Key.CapsLock:
            return 1 in leds
        elif key == Key.ScrollLock:
            return 2 in leds
        else:
            return False

    def _is_lock_key(key: Key) -> bool:
        return key in [Key.NumLock, Key.CapsLock, Key.ScrollLock]


@dataclass
class Mouse:
    """Internally used to provide mouse manipulation and queries"""
    ui: evdev.UInput
    
    def press(self, key: Key):
        if self._is_mouse_button(key):
            self.ui.write(evdev.ecodes.EV_KEY, key, 1)
            self.ui.syn()

    def release(self, key: Key):
        if self._is_mouse_button(key):
            self.ui.write(evdev.ecodes.EV_KEY, key, 0)
            self.ui.syn()

    def tap(self, key: Key):
        self.press(key)
        self.release(key)

    def is_pressed(self, key: Key) -> bool:
        return key in self.ui.device.active_keys()

    def move_abs(self, x: int, y: int):
        self.ui.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_X, x)
        self.ui.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_Y, y)
        self.ui.syn()

    def move_rel(self, x: int, y: int):
        self.ui.write(evdev.ecodes.EV_REL, evdev.ecodes.REL_X, x)
        self.ui.write(evdev.ecodes.EV_REL, evdev.ecodes.REL_Y, y)
        self.ui.syn()

    def _is_mouse_button(key: Key) -> bool:
        if key in [Key.LeftButton, Key.RightButton, Key.MiddleButton, Key.XButton, Key.SideButton]:
            return True
        return False

@dataclass
class Automaton:
    """The device to which all events are redirected. To access keyboard and mouse, use
    Automaton.kb and Automaton.ms. A failsafe can be set to exit out of the app when pressed.
    By default it is Ctrl+Esc."""
    HOTSTRINGS = {}
    HOTKEYS = {}
    REMAPS = {}
    keyboard: str = '/dev/input/event6'
    mouse: str = '/dev/input/event5'
    DEVICES = [evdev.InputDevice(keyboard), evdev.InputDevice(mouse)]
    ui = evdev.UInput.from_device(*DEVICES, name = 'Automaton')
    kb, ms = Keyboard(ui), Mouse(ui)
    failsafe = (Key.Esc, Key.LCtrl)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @classmethod
    def close(cls):
        cls.ui.close()
        for device in cls.DEVICES:
            try:
                device.ungrab()
            except IOError:
                pass
            device.close()

    def listen(self):
        for device in self.DEVICES:
            device.grab()
        word: str = ''


        devices = {dev.fd: dev for dev in self.DEVICES}
        while True:
            reader, writer, x = select(devices, [], [])
            for fd in reader:
                for event in devices[fd].read():
                    code = event.code
                    release_ev = False
                    # print(event)

                    if event.type == evdev.ecodes.EV_KEY:
                        (keys := tuple(self.ui.device.active_keys()))

                        if keys == self.failsafe:
                            break
                        
                        # Check for hotstrings
                        if code in HOTSTRING_TRIGGERS:
                            # Check if it is text replacement
                            fn = self.HOTSTRINGS.get(word)

                            txt =  fn() if fn is not None else None
                            if txt is not None:
                                # Overwrite trigger word
                                for _ in range(len(word)):
                                    self.kb.tap(Key.Backspace)
                                # Replace with return value
                                self.kb.type(txt)
                            word = ''
                        
                        # Check for remappings
                        elif event.code in self.REMAPS:
                            c, register_if, fire_on = self.REMAPS[event.code]
                            if register_if():
                                if fire_on == RELEASE and event.value == 0:
                                    code = c; release_ev = True
                                elif fire_on == PRESS and event.value == 1:
                                    code = c
                                else:
                                    code = 0

                        # Check for hotkeys
                        elif keys in self.HOTKEYS:
                            self.HOTKEYS[keys]()

                        # Update word and dummy device
                        # Key is Shift, or CapsLock is on and a aphabet in pressed
                        if Key.LShift in keys or Key.RShift in keys or (self.kb.is_toggled(Key.CapsLock) and event.code in CHAR_CODES):
                            word += (SHIFT_CODES.get(code) or '') if event.value >= 1 else ''
                        else:
                            word += (SCANCODES.get(code) or '') if event.value >= 1 else ''
                        if release_ev:
                            self.ui.write(evdev.ecodes.EV_KEY, code, 1)
                            self.ui.write(evdev.ecodes.EV_KEY, code, 0)
                        else:
                            self.ui.write(evdev.ecodes.EV_KEY, code, event.value)
                    else:
                        self.ui.write(event.type, event.code, event.value)
                    self.ui.syn()
                else:
                    continue
                break
            else:
                continue
            self.close()
            break


    def hotkey(self, *keys):
        def wrapper(f, register_if = lambda: True):
            def fn():
                if register_if(): f()
            self.HOTKEYS[tuple(sorted(keys))] = fn
        return wrapper


    def hotstring(self, s: str, register_if = lambda: True):
        def wrapper(f):
            def fn():
                if register_if():
                    return f()
            self.HOTSTRINGS[s] = fn
        return wrapper


    def remap(self, src: Key, dest: Key, register_if = lambda: True, fire_on = PRESS):
        self.REMAPS[src] = (dest, register_if, fire_on)

atexit.register(Automaton.close)