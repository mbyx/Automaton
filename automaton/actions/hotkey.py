from automaton.actions.action import Action
from automaton.core.context import Context
from typing import Callable, Optional, List
from ..core import Peripheral, EmissionState, Input
from dataclasses import dataclass, field
from enum import Enum

class HotKeyOptions(Enum):
    """Configurable options of a hotkey."""
    FireOnRelease = False
    DontSuppressKeys = False


@dataclass
class HotKey(Action):
    """Represents the state and logic a single hotkey requires to function and be stored."""
    keys: List[Input]
    action: Callable[[], Optional[str]]
    context: Callable[[], bool]
    options: List[HotKeyOptions]
    active_keys: List[int] = field(default_factory = List)

    def emit(self, device: Peripheral, context: Context):
        if (txt := self.action()) is not None:
            device.type(txt)

    def should_emit(self, context: Context) -> EmissionState:
        if list(map(lambda key: key.value, self.keys)) == context.active_keys:
            return EmissionState.Emit
        return EmissionState.DontEmit
