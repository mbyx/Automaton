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

    def emit(self, device: Peripheral, context: Context):
        if (txt := self.action()) is not None:
            if HotStringOptions.PreventAutoBackspace not in self.options:
                for _ in range(len(context.word)):
                    device.tap(Key.Backspace)
            device.type(txt)

    def should_emit(self, context: Context) -> EmissionState:
        print(context.word)
        if self.context() is False:
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
            word, txt = context.word, self.txt
        else:
            word, txt = context.word.lower(), self.txt.lower()

        condition = is_trigger_pressed and comparision_method(word, txt)

        if condition or context.event.code in map(lambda key: key.value, HOTSTRING_TRIGGERS):
            context.word = ''
        
        return EmissionState.Emit if condition else EmissionState.DontEmit
