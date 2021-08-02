from automaton.core.peripheral import Peripheral
from automaton.actions.action_emitter import ActionEmitter
from dataclasses import dataclass
from typing import List, Tuple
import evdev, re, time

@dataclass
class Macro:
    """Represents a recorded macro. It can be created from Automaton.record_until, or
    by loading it from a file. Macros can be played back as well. If you want to manipulate
    playback (such as by playing in reverse), you have to directly mutate Macro.events before
    calling macro.play()"""
    events: List[Tuple[evdev.InputEvent, int]]
    emitter: ActionEmitter
    device: Peripheral

    def play(self):
        """Plays the macro that has been recorded or loaded in."""
        for event, seconds in self.events:
            time.sleep(seconds)
            action = self.emitter.handle(event, '', self.device)
            self.device.update(event)
            action.emit(self.device, self.emitter.context)

    # TODO: Add ability to save and load macros from binary files.
