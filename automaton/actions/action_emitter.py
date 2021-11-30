from dataclasses import dataclass
from typing import List

import evdev
from multiprocess import Queue

from .. import core
from ..actions import Action, Context, HotKey, HotString, Redirect, Remap


@dataclass
class ActionEmitter:
    """Container class that stores all the hotkeys, hotstrings, and remaps.
    It also determines, given an event, which action to emit. It also updates
    its builtin state (context)"""

    hotkeys: List[HotKey]
    hotstrings: List[HotString]
    remaps: List[Remap]
    context: Context

    @staticmethod
    def new() -> "ActionEmitter":
        """Returns a default and empty version of the ActionEmitter."""
        return ActionEmitter([], [], [], Context.new())

    def handle(self, event: evdev.InputEvent, device_path: str, queue: Queue) -> Action:
        """Given a device and an event, determine which kind of action to perform."""
        if event.type == evdev.ecodes.ecodes["EV_KEY"]:
            self.context.update(event, device_path)

            actions: List[Action] = [
                *self.hotkeys,
                *self.hotstrings,
                *self.remaps,
            ]
            for action in actions:
                should_emit = action.should_emit(self.context)
                if should_emit is core.EmissionState.Emit:
                    return action
                elif should_emit is core.EmissionState.EmitButDontSuppress:
                    queue.put_nowait((event, device_path))
                    break
            if self.context.event.code in list(
                map(lambda key: int(key), core.HOTSTRING_TRIGGERS)
            ):
                self.context.word = ""
        return Redirect(event)
