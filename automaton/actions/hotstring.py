from automaton.core.context import Context
from typing import Callable, Optional, List
from ..core import Peripheral, Key, EmissionState, HOTSTRING_TRIGGERS, Input
from dataclasses import dataclass
from enum import Enum 

class HotStringOptions(Enum):
    """Configurable options for a hotstring."""
    CaseSensitive = True
    RequiresTrigger = True
    TriggerInsideWord = False
    PreventAutoBackspace = False


@dataclass
class HotString:
    """Represents the state and logic a single hotstring requires to function and be stored."""
    txt: str
    action: Callable[[], Optional[str]]
    context: Callable[[], bool]
    triggers: List[Input]
    options: List[HotStringOptions]

    def emit(self, device: Peripheral, context: Context):
        if (txt := self.action()) is not None:
            for _ in range(len(context.word)):
                device.tap(Key.Backspace)
            device.type(txt)

    def should_emit(self, context: Context) -> EmissionState:
        # Check if the event triggers a hotstring.
        condition = False
        if HotStringOptions.RequiresTrigger in self.options:
            if HotStringOptions.CaseSensitive in self.options:
                condition = (context.event.code in self.triggers) and (
                    context.word == self.txt)
            else:
                condition = (context.event.code in self.triggers) and (
                    context.word.lower() == self.txt.lower())

        if HotStringOptions.TriggerInsideWord in self.options:
            if HotStringOptions.CaseSensitive in self.options:
                condition = (context.event.code in self.triggers) and (
                    context.word in self.txt)
            else:
                condition = (context.event.code in self.triggers) and (
                    context.word.lower() in self.txt.lower())

        if condition or context.event.code in map(lambda key: key.value, HOTSTRING_TRIGGERS):
            context.word = ''
        
        return EmissionState.Emit if condition else EmissionState.DontEmit
