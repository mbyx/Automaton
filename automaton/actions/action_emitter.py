from dataclasses import dataclass
from typing import List

import evdev
from multiprocess import Queue

from .. import core
from ..actions import Action, Context, HotKey, HotString, Redirect, Remap


@dataclass
class ActionEmitter:
    """Stores all emittable `Action`s and determines when to emit them.

        An `Action` can be one of the following: `HotKey`, `HotString`, and `Remap`. Each
    action is stored separately in its own list. A `Context` is also stored, which
    contains useful information such as the current keys being pressed, which are
    used to determine whether to emit some action or not.
        All that a user has to do to use it is register some actions into the list (typically done
    at the top level by the `Automaton` object itself). To determine if some `Action` should be emitted,
    the `handle(event, device_path, queue)` function is called which will update it's `Context` using the first
    two arguments. If an action is to be emitted immediately, it will be pushed into the given queue for processing.

    ### Attributes:
        `hotkeys`: The list of all `HotKey`s currently registered.
        `hotstrings`: The list of all `HotString`s currently registered.
        `remaps`: The list of all `Remap`s currently registered.
        `context`: The state which helps determine which action to emit."""

    hotkeys: List[HotKey]
    hotstrings: List[HotString]
    remaps: List[Remap]
    context: Context

    @staticmethod
    def new() -> "ActionEmitter":
        """Returns a default and empty version of the ActionEmitter.

        This `ActionEmitter` object will not have any registered actions, and
        it's `Context` will also be empty."""
        return ActionEmitter([], [], [], Context.new())

    def handle(self, event: evdev.InputEvent, device_path: str, queue: Queue) -> Action:
        """Given a device and an event, determine which kind of action to perform.

        ### Args:
            `event`: A low level device event that can be a keypress or mouse input.
            `device_path`: The path to the device that emitted the event.
            `queue`: The queue to which an action will be pushed if it is to be immediately processed.

        ### Returns:
            The `Action` that it determines should be emitted. Can be one of the following:\n
                `HotKey`: A sequence of keys when pressed triggers some action.\n
                `HotString`: A sequence of letters when typed triggers some action.\n
                `Remap`: Simply put, when one key is pressed, another is pressed instead.\n
                `Redirect`: Redirect miscellaneous input as is."""

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
