from ..core import EmissionState, Input, KeyState, Callable, Peripheral, Context
from .action import Action 
from dataclasses import dataclass
from enum import Enum
from typing import List

class RemapOptions(Enum):
    """Configurable options of a remap."""
    DontSuppressKeys = 0


@dataclass
class Remap(Action):
    """Represents the state and logic a single remap requires to function and be stored."""
    src: Input
    dest: Input
    context: Callable[[], bool]
    options: List[RemapOptions]
    state: KeyState

    def emit(self, device: Peripheral, context: Context):
        if self.state is KeyState.Press or self.state is KeyState.Hold:
            device.press(self.dest)
        else:
            device.release(self.dest)

    def should_emit(self, context: Context) -> EmissionState:
        if self.context() is False:
            return EmissionState.DontEmit

        # Check if the event can be remapped.
        elif self.src.value == context.event.code:  # If a remap was found
            if context.event.value >= 1:
                self.state = KeyState.Press
            else:
                self.state = KeyState.Release
            if RemapOptions.DontSuppressKeys in self.options:
                return EmissionState.EmitButDontSuppress
            else:
                return EmissionState.Emit
        return EmissionState.DontEmit
