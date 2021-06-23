from typing import Callable, Optional, Union
from .input import Key, Button
from enum import Enum

Callback = Callable[[], Optional[str]]
Input = Union[Key, Button]

# Maps scancodes to their lowercase variants
SCANCODES: dict[int, str] = {
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0', 12: '-', 13: '=',
    16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y', 22: 'u', 23: 'i', 24: 'o', 25: 'p', 26: '[', 27: ']', 43: '\\',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h', 36: 'j', 37: 'k', 38: 'l', 39: ';', 40: '"', 41: '`',
    44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b', 49: 'n', 50: 'm', 51: ',', 52: '.', 53: '/'
}

# Maps scancodes to their uppercase variants
SHIFT_CODES: dict[int, str] = {
    2: '!', 3: '@', 4: '#', 5: '$', 6: '%', 7: '^', 8: '&', 9: '*', 10: '(', 11: ')', 12: '_', 13: '+',
    16: 'Q', 17: 'W', 18: 'E', 19: 'R', 20: 'T', 21: 'Y', 22: 'U', 23: 'I', 24: 'O', 25: 'P', 26: '{', 27: '}',
    30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J', 37: 'K', 38: 'L', 39: ':', 40: '\'', 41: '~', 43: '|',
    44: 'Z', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N', 50: 'M', 51: '<', 52: '>', 53: '?'
}

# All the scancodes that are characters.
CHAR_CODES: list[int] = [
    16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32,
    33, 34, 35, 36, 37, 38, 44, 45, 46, 47, 48, 49, 50
]

# The default keys that have to be pressed in order for a hotstring to activate. Can be changed.
HOTSTRING_TRIGGERS: set[Key] = {
    Key.Space, Key.Backspace, Key.Enter, Key.Tab
}


class LockState(Enum):
    """States of a Lock key."""
    On  = True
    Off = False

class KeyState(Enum):
    """The states of a normal key."""
    Press = "PRESS"
    Release = "RELEASE"
    Hold = "HOLD"

class EmissionState(Enum):
    """The ways an action can be emitted, or not emitted."""
    Emit = True
    DontEmit = False
    EmitButDontSuppress = None

