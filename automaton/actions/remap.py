from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .. import core
from .action import Action
from .context import Context


class RemapOptions(Enum):
    """Configurable options of a remap."""

    DontSuppressKeys = 0


@dataclass
class Remap(Action):
    """Represents the state and logic a single remap requires to function and be stored."""

    src: core.Input
    dest: core.Input
    context: core.Callable[[], bool]
    options: List[RemapOptions]
    state: core.KeyState
    from_device: Optional[str]

    def emit(self, device: core.Peripheral, context: Context):
        if (
            self.state is core.KeyState.Press
            or self.state is core.KeyState.Hold
        ):
            device.press(self.dest)
        else:
            device.release(self.dest)

    def should_emit(self, context: Context) -> core.EmissionState:
        if self.context() is False:
            return core.EmissionState.DontEmit
        if (
            context.device_path != self.from_device
            and self.from_device is not None
        ):
            return core.EmissionState.DontEmit

        # Check if the event can be remapped.
        elif int(self.src) == context.event.code:  # If a remap was found
            if context.event.value >= 1:
                self.state = core.KeyState.Press
            else:
                self.state = core.KeyState.Release
            if RemapOptions.DontSuppressKeys in self.options:
                return core.EmissionState.EmitButDontSuppress
            else:
                return core.EmissionState.Emit
        return core.EmissionState.DontEmit
