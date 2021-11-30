from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional

from .. import core
from .action import Action
from .context import Context


class HotStringOptions(Enum):
    """Configurable options for a hotstring."""

    CaseSensitive = 0
    TriggerImmediately = 1
    TriggerInsideWord = 2
    PreventAutoBackspace = 3


@dataclass
class HotString(Action):
    """Represents the state and logic a single hotstring requires to function and be stored."""

    txt: str
    action: Callable[[], Optional[str]]
    context: Callable[[], bool]
    triggers: List[core.Input]
    options: List[HotStringOptions]
    from_device: Optional[str]

    def emit(self, device: core.Peripheral, context: Context) -> None:
        context.word = ""
        if HotStringOptions.PreventAutoBackspace not in self.options:
            for _ in range(len(self.txt)):
                device.tap(core.Key.Backspace)
        if (txt := self.action()) is not None:
            device.type(txt)

    def should_emit(self, context: Context) -> core.EmissionState:
        if self.context() is False:
            return core.EmissionState.DontEmit
        if context.device_path != self.from_device and self.from_device is not None:
            return core.EmissionState.DontEmit
        # Check if the event triggers a hotstring.
        condition = False
        if HotStringOptions.CaseSensitive in self.options:
            word, txt = context.word.strip(), self.txt.strip()
        else:
            word, txt = context.word.lower().strip(), self.txt.lower().strip()

        if HotStringOptions.TriggerImmediately in self.options:
            is_trigger_pressed = True
        else:
            is_trigger_pressed = context.event.code in self.triggers

        if HotStringOptions.TriggerInsideWord in self.options:
            comparision_method: Callable[[str, str], bool] = lambda x, y: y in x
        else:
            comparision_method: Callable[[str, str], bool] = lambda x, y: (x == y)

        condition = is_trigger_pressed and comparision_method(word, txt)

        return core.EmissionState.Emit if condition else core.EmissionState.DontEmit
