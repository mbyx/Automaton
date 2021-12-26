import contextlib
import select
from dataclasses import dataclass
from typing import Any, ContextManager, Iterator, List, Tuple, cast

import evdev

from .device import Device


@dataclass
class InputStream:
    """A Stream that reads events from a set
    of devices and yields them as a generator."""

    devices: List[Device]
    stack: contextlib.ExitStack

    @staticmethod
    def new(devices: List[str]) -> "InputStream":
        stack = contextlib.ExitStack()
        # Create Devices that allow cleanup on exiting.
        devs: List[Device] = [
            stack.enter_context(
                cast(ContextManager[Any], Device(evdev.InputDevice(dev)))
            )
            for dev in devices
        ]
        return InputStream(devs, stack)

    def read(self) -> Iterator[Tuple[evdev.InputEvent, str]]:
        """A Generator that returns an InputEvent from stored devices. Also manages the
        safety of each device and makes sure it is closed."""

        # Maps the file descriptor to the device.
        devices = {dev.device.fd: dev.device for dev in self.devices}

        # Enter event loop
        while True:
            # Get the amount of time we waited for a new event.
            reader, _, _ = select.select(devices, [], [])
            for fd in reader:
                for event in devices[fd].read():
                    yield event, devices[fd].path

    def grab_devices(self) -> None:
        """Grabs all devices; prevents keypresses from being registered."""
        # Do not grab until all keys are released. Prevents weirdness.
        while any(
            [
                key
                for device in self.devices
                for name, key in device.device.active_keys(verbose=True)
                if name != "?"
            ]
        ):
            continue

        # Start grabbing.
        for device in self.devices:
            self.stack.enter_context(device.device.grab_context())
