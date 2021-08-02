from ..core import Context, Peripheral, EmissionState, HOTSTRING_TRIGGERS
from ..actions import HotKey, HotString, Remap, Redirect, Action
from dataclasses import dataclass
from typing import List
import evdev

@dataclass
class ActionEmitter:
    """Container class that stores all the hotkeys, hotstrings, and remaps. It also determines,
    given an event, which action to emit. It also updates its builtin state (context)"""
    HOTKEYS: List[HotKey]
    HOTSTRINGS: List[HotString]
    REMAPS: List[Remap]
    context: Context

    @staticmethod
    def new() -> 'ActionEmitter':
        """Returns a default and empty version of the ActionEmitter."""
        return ActionEmitter([], [], [], Context.new())

    def handle(self, event: evdev.InputEvent, device_path: str, device: Peripheral) -> Action:
        """Given a device and an event, determine which kind of action to perform."""
        if event.type == evdev.ecodes.EV_KEY:
            self.context.update(event, device_path)
            
            for action in self.HOTKEYS + self.HOTSTRINGS + self.REMAPS:
                should_emit = action.should_emit(self.context)
                if should_emit is EmissionState.Emit:
                    return action
                elif should_emit is EmissionState.EmitButDontSuppress:
                    action.emit(device, self.context)
                    break
            if self.context.event.code in list(map(lambda key: int(key), HOTSTRING_TRIGGERS)):
                self.context.word = ''
        return Redirect(event)
