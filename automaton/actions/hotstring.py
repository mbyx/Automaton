from .action import Action
from typing import Callable, Optional, List
from ..core import Peripheral, Key, EmissionState, HOTSTRING_TRIGGERS, Input, Context
from dataclasses import dataclass
from enum import Enum 

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
    triggers: List[Input]
    options: List[HotStringOptions]
    from_device: Optional[str]

    def emit(self, device: Peripheral, context: Context):
        context.word = ''
        if (txt := self.action()) is not None:
            if HotStringOptions.PreventAutoBackspace not in self.options:
                for _ in range(len(self.txt)):
                    device.tap(Key.Backspace)
            device.type(txt)

    def should_emit(self, context: Context) -> EmissionState:
        if self.context() is False:
            return EmissionState.DontEmit
        if context.device_path != self.from_device and self.from_device is not None:
            return EmissionState.DontEmit
        # Check if the event triggers a hotstring.
        condition = False
        if HotStringOptions.TriggerImmediately in self.options:
            is_trigger_pressed = True
        else:
            is_trigger_pressed = (context.event.code in self.triggers)

        if HotStringOptions.TriggerInsideWord in self.options:
            comparision_method = lambda x, y: x in y
        else:
            comparision_method = lambda x, y: x == y

        if HotStringOptions.CaseSensitive in self.options:
            word, txt = context.word.strip(), self.txt.strip()
        else:
            word, txt = context.word.lower().strip(), self.txt.lower().strip()
        condition = is_trigger_pressed and comparision_method(word, txt)

        return EmissionState.Emit if condition else EmissionState.DontEmit
