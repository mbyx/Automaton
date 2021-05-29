# Fix to make gi work.
from threading import Thread
from typing import Optional
import pgi
pgi.install_as_gi()
import gi
gi.require_version('Wnck', '3.0')

from dataclasses import dataclass
from .keyboard import Keyboard
from threading import Thread
from select import select
from .mouse import Mouse
import evdev, atexit
from .key import Key
from .consts import (
    SCANCODES,
    SHIFT_CODES,
    PRESS, RELEASE,
    HOTSTRING_TRIGGERS,
    CHAR_CODES
)


@dataclass
class Automaton:
    """The dummy device to which all events are redirected. To access keyboard and mouse, use
    Automaton.kb and Automaton.ms. A failsafe can be set to exit out of the app when pressed.
    By default it is Ctrl+Esc. Automaton works by creating a dummy device that receives the events
    of all other devices, while the actual devices are suppress. Once Automaton is active. All output
    is done by this device, and its inputs are other devices connected the computer.
    parameters:
    keyboard: The device path for the keyboard. Usually something like /dev/input/eventX where X is any integer
    mouse: The device path for the mouse. Usually something like /dev/input/eventX where X is any integer"""
    HOTSTRINGS, HOTKEYS, REMAPS = {}, {}, {}

    keyboard: str = '/dev/input/event6'
    mouse: str = '/dev/input/event5'

    DEVICES = (evdev.InputDevice(keyboard), evdev.InputDevice(mouse))
    
    # Create a dummy device for event redirection. It has the capabilities of all connected devices.
    ui = evdev.UInput.from_device(*DEVICES, name = 'Automaton')
    
    # Create instances of Keyboard and Mouse for usage.
    kb, ms = Keyboard(ui), Mouse(ui)

    # When the failsafe is pressed, Automaton immediately exits after ungrabbing devices.
    failsafe = (Key.Esc, Key.LCtrl)

    # For use with a context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.close()
        except:
            pass


    def close(self):
        """Closes the dummy devices, ungrabs and closes all slave devices."""

        for device in self.DEVICES: # Ungrab all devices, and close them. Ignore errors.
            try:
                device.ungrab()
            except IOError:
                raise
            device.close()
        self.ui.close() # Close the dummy device.

    def listen(self):
        """Starts the process of redirection of events from other devices to the dummy device."""

        try:
            for device in self.DEVICES: # Suppress other devices.
                device.grab()

            word: str = '' # Current word that is being typed.
            devices = {dev.fd: dev for dev in self.DEVICES} # Maps the file descriptor to the device.

            while True:
                reader, writer, x = select(devices, [], [])
                for fd in reader:
                    for event in devices[fd].read(): # Redirect events to this device.
                        code = event.code # The scancode of the event.
                        release_ev = False # Whether this event was a release event or not.

                        if event.type == evdev.ecodes.EV_KEY:
                            keys = tuple(self.ui.device.active_keys())

                            if keys == self.failsafe:
                                raise KeyboardInterrupt
                            
                            # Check for hotstrings
                            if code in HOTSTRING_TRIGGERS: # If a trigger key was pressed
                                # Check if it is a text replacement
                                fn = self.HOTSTRINGS.get(word)
                                txt =  fn() if fn is not None else None
                                if txt is not None:
                                    # Overwrite trigger word
                                    for _ in range(len(word)):
                                        self.kb.tap(Key.Backspace)
                                    # Replace with return value
                                    self.kb.type(txt)
                                word = '' # Reset the word.
                            
                            # Check for remappings
                            elif event.code in self.REMAPS:
                                c, register_if, fire_on = self.REMAPS[event.code] # Get the data from the remap.
                                if register_if(): # Fire the remap only if register_if() returns True.
                                    if fire_on == RELEASE and event.value == 0: # Activate remap on release rather than on press.
                                        code = c; release_ev = True
                                    elif fire_on == PRESS and event.value == 1:
                                        code = c
                                    elif fire_on == PRESS and event.value == 0:
                                        code = c
                                    else:
                                        code = 0

                            # Check for hotkeys
                            elif keys in self.HOTKEYS: # If the currently pressed keys are a hotkey combo.
                                self.HOTKEYS[keys]()

                            # Update word and dummy device
                            # Key is Shift, or CapsLock is on and a aphabet in pressed
                            if Key.LShift in keys or Key.RShift in keys or (self.kb.is_toggled(Key.CapsLock) and event.code in CHAR_CODES):
                                word += (SHIFT_CODES.get(code) or '') if event.value >= 1 else ''
                            else:
                                word += (SCANCODES.get(code) or '') if event.value >= 1 else ''

                            if release_ev: # If fired on release, has to immediately be released.
                                self.ui.write(evdev.ecodes.EV_KEY, code, 1)
                                self.ui.write(evdev.ecodes.EV_KEY, code, 0)
                            else:
                                self.ui.write(evdev.ecodes.EV_KEY, code, event.value)
                        else:
                            self.ui.write(event.type, event.code, event.value)
                        self.ui.syn()
        finally:
            self.close()




    def hotkey(self, *keys, register_if= lambda: True):
        """Decorator that wraps a function into a hotkey. It takes a list of keys and
        a callback that determines whether to activate the hotkey. Similar to context
        sensitive hotkeys."""
        def wrapper(f):
            def fn():
                if register_if(): f()
            self.HOTKEYS[tuple(sorted(keys))] = fn
        return wrapper


    def hotstring(self, s: str, register_if = lambda: True):
        """Decorator that wraps a function into a hotstring. It takes a string to replace
        and a callback which determines whether to replace or not.
        The decorated function may return None or str. If str is returned. It is typed."""
        def wrapper(f):
            def fn():
                if register_if():
                    return f()
            self.HOTSTRINGS[s] = fn
        return wrapper


    def remap(self, src: Key, dest: Key, register_if = lambda: True, fire_on = PRESS):
        """Remaps the src key to the dest key, while being context sensitive. Can fire
        on RELEASE or PRESS of the key."""
        self.REMAPS[src] = (dest, register_if, fire_on)
