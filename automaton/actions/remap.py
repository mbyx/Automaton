from ..core import EmissionState, Input, KeyState, Callable, Peripheral
from automaton.core.context import Context 
from dataclasses import dataclass
from enum import Enum

class RemapOptions(Enum):
    """Configurable options of a remap."""
    FireOnRelease = False
    SuppressKeys = False


@dataclass
class Remap:
    """Represents the state and logic a single remap requires to function and be stored."""
    src: Input
    dest: Input
    context: Callable[[], bool]
    options: list[RemapOptions]
    state: KeyState

    def emit(self, device: Peripheral, context: Context):
        if self.state is KeyState.Press or self.state is KeyState.Hold:
            device.press(self.dest)
        else:
            device.release(self.dest)

    def should_emit(self, context: Context) -> EmissionState:
        # Check if the event can be remapped.
        if self.src.value == context.event.code:  # If a remap was found
            if context.event.value >= 1:
                self.state = KeyState.Press
            else:
                self.state = KeyState.Release
            return EmissionState.Emit
        return EmissionState.DontEmit
