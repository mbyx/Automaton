from dataclasses import dataclass
import evdev, select, contextlib
from .device import Device
from typing import Iterator, List, Tuple
import datetime

@dataclass
class InputStream:
    """A Stream that reads events from a set of devices and yields them as a generator."""
    devices: List[Device]
    stack: contextlib.ExitStack

    @staticmethod
    def new(devices: List[str]) -> 'InputStream':
        stack = contextlib.ExitStack()
        # Create Devices that allow cleanup on exiting.
        devices = [stack.enter_context(
            Device(evdev.InputDevice(dev))) for dev in devices]
        return InputStream(devices, stack)

    def read(self) -> Iterator[Tuple[evdev.InputEvent, str, int]]:
        """A Generator that returns an InputEvent from stored devices. Also manages the
        safety of each device and makes sure it is closed."""

        # Maps the file descriptor to the device.
        devices = {dev.device.fd: dev.device for dev in self.devices}

        # Enter event loop
        while True:
            # Get the amount of time we waited for a new event.
            start = datetime.datetime.now()
            reader, _, _ = select.select(devices, [], [])
            end = datetime.datetime.now()
            delta = (end - start).total_seconds()
            for fd in reader:
                for event in devices[fd].read():
                    yield event, devices[fd].path, delta

    def grab_devices(self):
        """Grabs all devices; prevents keypresses from being registered."""
        # Do not grab until all keys are released. Prevents weirdness.
        while any([key
                   for device in self.devices
                   for name, key in device.device.active_keys(verbose=True)
                   if name != '?'
                   ]):
            continue

        # Start grabbing.
        for device in self.devices:
            self.stack.enter_context(device.device.grab_context())
