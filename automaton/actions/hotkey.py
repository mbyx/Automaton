from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional

from automaton.actions.action import Action

from .. import core
from .context import Context


class HotKeyOptions(Enum):
    """Configurable options of a hotkey."""

    DontSuppressKeys = 0


@dataclass
class HotKey(Action):
    """Represents the state and logic a single hotkey requires to function and be stored."""

    keys: List[core.Input]
    action: Callable[[], Optional[str]]
    context: Callable[[], bool]
    options: List[HotKeyOptions]
    from_device: Optional[str]

    def emit(self, device: core.Peripheral, context: Context) -> None:
        if (txt := self.action()) is not None:
            device.type_unicode(txt)

    def should_emit(self, context: Context) -> core.EmissionState:
        if self.context() is False:
            return core.EmissionState.DontEmit
        if context.device_path != self.from_device and self.from_device is not None:
            return core.EmissionState.DontEmit

        elif list(map(int, self.keys)) == context.active_keys:
            if HotKeyOptions.DontSuppressKeys in self.options:
                return core.EmissionState.EmitButDontSuppress
            else:
                return core.EmissionState.Emit
        return core.EmissionState.DontEmit
