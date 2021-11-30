from dataclasses import dataclass

import evdev

from .. import core
from .action import Action
from .context import Context


@dataclass
class Redirect(Action):
    """The default action that is emitted. It simply redirects the event from one device to another."""

    event: evdev.InputEvent

    def emit(self, device: core.Peripheral, context: Context) -> None:
        device.ui.write(self.event.type, self.event.code, self.event.value)
        device.ui.syn()
