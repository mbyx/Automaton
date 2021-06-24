from ..core import Peripheral, Context
from dataclasses import dataclass 
import evdev

@dataclass
class Redirect:
    """The default action that is emitted. It simply redirects the event from one device to another."""
    event: evdev.InputEvent

    def emit(self, device: Peripheral, context: Context):
        device.ui.write(self.event.type, self.event.code, self.event.value)
        device.ui.syn()
