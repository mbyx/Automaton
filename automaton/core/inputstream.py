from dataclasses import dataclass
import evdev, select, contextlib
from .device import Device
from typing import List

@dataclass
class InputStream:
    """A Stream that reads events from a set of devices and yields them as a generator."""
    DEVICES: List[str]

    def read(self) -> evdev.InputEvent:
        """A Generator that returns an InputEvent from stored devices. Also manages the
        safety of each device and makes sure it is closed."""
        with contextlib.ExitStack() as stack:
            # Create Devices that allow cleanup on exiting.
            devices = [stack.enter_context(
                Device(evdev.InputDevice(dev))) for dev in self.DEVICES]

            self.grab_devices(devices, stack)  # Grab devices.

            # Maps the file descriptor to the device.
            devices = {dev.device.fd: dev.device for dev in devices}

            # Enter event loop
            while True:
                reader, _, _ = select.select(devices, [], [])
                for fd in reader:
                    for event in devices[fd].read():
                        yield event

    def grab_devices(self, devices: List[Device], stack: contextlib.ExitStack):
        """Grabs all devices; prevents keypresses from being registered."""
        # Do not grab until all keys are released. Prevents weirdness.
        while any([key
                   for device in devices
                   for name, key in device.device.active_keys(verbose=True)
                   if name != '?'
                   ]):
            continue

        # Start grabbing.
        for device in devices:
            stack.enter_context(device.device.grab_context())
