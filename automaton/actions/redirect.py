from ..peripheral import Peripheral
from dataclasses import dataclass
from ..core import Context
import evdev

@dataclass
class Redirect:
    """The default action that is emitted. It simply redirects the event from one device to another."""
    event: evdev.InputEvent

    def emit(self, device: Peripheral, context: Context):
        device.ui.write(self.event.type, self.event.code, self.event.value)
        device.ui.syn()
