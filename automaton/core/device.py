from dataclasses import dataclass
import evdev

@dataclass
class Device:
    """Wrapper around evdev.InputDevice provided context management via with statements."""
    device: evdev.InputDevice

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Do not close until all keys are released. Prevents weirdness.
        while any([key
                   for name, key in self.device.active_keys(verbose=True)
                   if name != '?'
                   ]):
            continue
        self.device.close()
