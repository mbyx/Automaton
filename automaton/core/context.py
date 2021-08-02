from .consts import CHAR_CODES, SCANCODES, SHIFT_CODES
from dataclasses import dataclass
from typing import List
from .input import Key
import evdev

@dataclass
class Context:
    """Container that stores the essential state of a device, and actions."""
    word: str
    active_keys: List[int]
    lock_states: List[int]
    event: evdev.InputEvent
    device_path: str

    @staticmethod
    def new() -> 'Context':
        """Create an empty context object."""
        return Context('', [], [], evdev.InputEvent(0, 0, 0, 0, 0), '')

    def update(self, event: evdev.InputEvent, device_path: str):
        """Updates the context with new information gathered from the event."""
        self.update_active_keys(event)
        self.update_lock_states(event)
        self.append_key(event)
        self.event = event
        self.device_path = device_path

    def update_lock_states(self, event: evdev.InputEvent):
        """Updates the information about the lock states using the event."""
        if event.type == evdev.ecodes.EV_KEY:
            if event.value >= 1 and event.code not in self.lock_states:
                self.lock_states.append(event.code)
            elif event.value >= 1 and event.code in self.lock_states:
                self.lock_states.remove(event.code)

    def update_active_keys(self, event: evdev.InputEvent):
        """Updates the information about the active keys using the event."""
        # Update active_keys.
        if event.type == evdev.ecodes.EV_KEY:
            if event.value >= 1 and event.code not in self.active_keys:
                self.active_keys.append(event.code)
            elif event.value <= 0 and event.code in self.active_keys:
                self.active_keys.remove(event.code)

    def append_key(self, event: evdev.InputEvent):
        """Updates the word being currently typed."""
        if event.type == evdev.ecodes.EV_KEY and event.value >= 1:
            conditions = [
                Key.LShift.value in self.active_keys,
                Key.RShift.value in self.active_keys,
                (Key.CapsLock.value in self.lock_states) and (event.code in CHAR_CODES)
            ]
            if any(conditions):
                self.word += SHIFT_CODES.get(event.code) or ''
            else:
                self.word += SCANCODES.get(event.code) or ''
