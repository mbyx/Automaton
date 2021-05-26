# Fix to make gi work.
import pgi
pgi.install_as_gi()
import gi
gi.require_version('Wnck', '3.0')

from dataclasses import dataclass
from select import select
import atexit, evdev
from key import Key

# Add Dialogues
import zenipy as Dialog

SCANCODES: dict[int, str] = {
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0', 12: '-', 13: '=',
    16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y', 22: 'u', 23: 'i', 24: 'o', 25: 'p', 26: '[', 27: ']', 43: '\\',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h', 36: 'j', 37: 'k', 38: 'l', 39: ';', 40: '"', 41: '`',
    44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b', 49: 'n', 50: 'm', 51: ',', 52: '.', 53: '/', 57: ' '
}

sc = {v: k for k, v in SCANCODES.items()}

HOTSTRING_TRIGGERS: set[Key] = {
    Key.Space, Key.Backspace, Key.Enter, Key.Tab
}

# Prepare device for redirection
KEYBD = evdev.InputDevice('/dev/input/event6')
MOUSE = evdev.InputDevice('/dev/input/event5')

DEVICES = (KEYBD, MOUSE)

@dataclass
class Keyboard:
    
    def press(key: Key):
        KEYBD.write(evdev.ecodes.EV_KEY, key, 1)

    def release(key: Key):
        KEYBD.write(evdev.ecodes.EV_KEY, key, 0)

    @classmethod
    def tap(cls, key: Key):
        cls.press(key)
        cls.release(key)

    @classmethod
    def type(cls, txt: str):
        for chr in txt:
            cls.tap(sc[chr])

    def is_pressed(key: Key) -> bool:
        return key in KEYBD.active_keys()

    def is_toggled(key: Key) -> bool:
        leds = KEYBD.leds()
        if key == Key.NumLock:
            return 0 in leds
        elif key == Key.CapsLock:
            return 1 in leds
        elif key == Key.ScrollLock:
            return 2 in leds
        else:
            return False

@dataclass
class Mouse:
    
    @classmethod
    def press(cls, key: Key):
        if cls._is_mouse_button(key):
            MOUSE.write(evdev.ecodes.EV_KEY, key, 1)

    @classmethod
    def release(cls, key: Key):
        if cls._is_mouse_button(key):
            MOUSE.write(evdev.ecodes.EV_KEY, key, 0)

    @classmethod
    def tap(cls, key: Key):
        cls.press(key)
        cls.release(key)

    @classmethod
    def is_pressed(cls, key: Key) -> bool:
        return key in MOUSE.active_keys()

    def move_abs(x: int, y: int):
        MOUSE.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_X, x)
        MOUSE.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_Y, y)

    def move_rel(x: int, y: int):
        MOUSE.write(evdev.ecodes.EV_REL, evdev.ecodes.REL_X, x)
        MOUSE.write(evdev.ecodes.EV_REL, evdev.ecodes.REL_Y, y)

    def _is_mouse_button(key: Key) -> bool:
        if key in [Key.LeftButton, Key.RightButton, Key.MiddleButton, Key.XButton, Key.SideButton]:
            return True
        return False


@dataclass
class Automaton:
    HOTSTRINGS = {}
    HOTKEYS = {}
    REMAPS = {}

    def listen(self):
        atexit.register(KEYBD.ungrab)
        atexit.register(MOUSE.ungrab)
        KEYBD.grab()
        MOUSE.grab()
        word: str = ''

        with evdev.UInput.from_device(KEYBD, MOUSE, name = 'Automaton') as ui:
            devices = {dev.fd: dev for dev in DEVICES}
            while True:
                reader, writer, x = select(devices, [], [])
                for fd in reader:
                    for event in devices[fd].read():
                        code = event.code
                        # print(event)

                        if event.type == evdev.ecodes.EV_KEY:
                            (keys := tuple(ui.device.active_keys()))
                            
                            # Check for hotstrings
                            if code in HOTSTRING_TRIGGERS:
                                # Check if it is text replacement
                                fn = self.HOTSTRINGS.get(word)
                                txt =  fn() if fn is not None else None
                                if txt is not None:
                                    # Overwrite trigger word
                                    for _ in range(len(word)):
                                        Keyboard.tap(Key.Backspace)
                                    # Replace with return value
                                    Keyboard.type(txt)
                                word = ''
                            
                            # Check for remappings
                            elif event.code in self.REMAPS:
                                c, register_if = self.REMAPS[event.code]
                                if register_if():
                                    code = c

                            # Check for hotkeys
                            elif keys in self.HOTKEYS:
                                self.HOTKEYS[keys]()

                            # Update word and dummy device
                            word += (SCANCODES.get(code) or '') if event.value >= 1 else ''
                            ui.write(evdev.ecodes.EV_KEY, code, event.value)
                        else:
                            ui.write(event.type, event.code, event.value)


    def hotkey(self, *keys):
        def wrapper(f, register_if = lambda: True):
            def fn():
                if register_if(): f()
            self.HOTKEYS[tuple(sorted(keys))] = fn
        return wrapper


    def hotstring(self, s: str, register_if = lambda: True):
        def wrapper(f):
            def fn():
                if register_if(): f()
            self.HOTSTRINGS[s] = fn
        return wrapper


    def remap(self, src: Key, dest: Key, register_if = lambda: True):
        self.REMAPS[src] = (dest, register_if)