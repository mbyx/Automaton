import time
from dataclasses import dataclass
from typing import List

import evdev

from automaton.core.peripheral import Peripheral

from .action_emitter import ActionEmitter


@dataclass
class Macro:
    """Represents a recorded macro. It can be created from Automaton.record_until, or
    by loading it from a file. Macros can be played back as well. If you want to manipulate
    playback (such as by playing in reverse), you have to directly mutate Macro.events before
    calling macro.play()"""

    events: List[evdev.InputEvent]
    emitter: ActionEmitter
    device: Peripheral

    def play(self, speed: int = 0) -> None:
        """Plays the macro that has been recorded or loaded in."""
        prev_time = None
        for event in self.events:
            if speed > 0 and prev_time is not None:
                time.sleep((event.timestamp() - prev_time) / speed)
            prev_time = event.timestamp()
            self.device.ui.write_event(event)

    # TODO: Add ability to save and load macros from binary files.
