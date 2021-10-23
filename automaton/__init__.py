import os
from dataclasses import dataclass
from typing import Callable, Iterator, List, Optional, Tuple, Union, cast

import evdev
from multiprocess import Process, Queue

from .actions import (
    Action,
    ActionEmitter,
    Context,
    HotKey,
    HotKeyOptions,
    HotString,
    HotStringOptions,
    Macro,
    Redirect,
    Remap,
    RemapOptions,
)
from .core import (
    CHAR_CODES,
    HOTSTRING_TRIGGERS,
    SCANCODES,
    SHIFT_CODES,
    ActionString,
    Button,
    Callback,
    Device,
    EmissionState,
    Input,
    InputStream,
    Key,
    KeyState,
    LockState,
    Peripheral,
)


@dataclass
class Automaton:
    """The dummy device to which all events are redirected. To access keyboard and mouse, use
    Automaton.device. A failsafe can be set to exit out of the app when pressed.
    By default it is Ctrl+Esc. Automaton works by creating a dummy device that receives the events
    of all other devices, while the actual devices are suppressed. Once Automaton is active. All output
    is done by this device, and its inputs are other devices connected the computer."""

    emitter: ActionEmitter
    stream: InputStream
    device: Peripheral
    failsafe: List[Input]

    @staticmethod
    def new(  # All capapbilities by default
        devices: List[str] = None,
        failsafe: List[Input] = [Key.LCtrl, Key.Esc],
    ) -> "Automaton":
        """Creates a new instance of Automaton. Takes in a List of devices to act as slaves,
        and a List of keys to be pressed. These act as a special hotkey that can close Automaton."""
        if devices is None:
            devices = evdev.list_devices()
        ui = evdev.UInput.from_device(*devices, name="Automaton")

        return Automaton(
            ActionEmitter.new(),
            InputStream.new(devices),
            Peripheral(ui),
            failsafe,
        )

    def close(self):
        """Closes the dummy device"""
        self.device.ui.close()
        self.stream.stack.close()

    def _get_event(self) -> Iterator[Tuple[evdev.InputEvent, str]]:
        """Wrapper around InputStream.read(). Necessary as read cannot be called more than
        once, yet is required in two separate areas."""
        for event, device_path in self.stream.read():
            yield event, device_path

    def run(self) -> None:
        """Starts the automaton main loop. This has to be called in order for automaton to function.
        It functions by redirection and suppression of events from slave devices into the master device.
        The middleman performs all the logic."""
        try:
            queue = Queue()

            def process_events(queue: Queue) -> None:
                while True:
                    action = queue.get()
                    action.emit(self.device, self.emitter.context)

            proc = Process(target=process_events, args=(queue,))
            proc.start()

            self.stream.grab_devices()
            for event, device_path in self._get_event():
                action = self.emitter.handle(event, device_path, queue)
                self.device.update(event)
                if list(map(int, self.failsafe)) in [
                    self.emitter.context.active_keys
                ]:
                    raise KeyboardInterrupt

                if not isinstance(action, Remap) and not isinstance(
                    action, Redirect
                ):
                    queue.put_nowait(action)
                else:
                    action.emit(self.device, self.emitter.context)

            proc.join()
        finally:
            self.close()

    def record_until(self, condition: Callable[[], bool]) -> Macro:
        """Records a series of events into a Macro until a specific condition becomes
        false."""
        events: List[evdev.InputEvent] = []
        for event, _ in self._get_event():
            if condition():
                break
            events.append(event)
        return Macro(events, self.emitter, self.device)

    def on(
        self,
        trigger: Union[List[Input], str],
        when: Callable[[], bool] = lambda: True,
        options: List[Union[HotKeyOptions, HotStringOptions]] = [],
        triggers: List[Input] = HOTSTRING_TRIGGERS,
        from_device: Optional[str] = None,
    ):
        """Takes in either a List of keys, or a string. If a string is given, a hotstring is
        registered, otherwise a hotkey is registered. Options and context-sensitivity can be
        applied."""

        def wrapper(action):
            if isinstance(trigger, str):
                hotstring = HotString(
                    trigger,
                    action,
                    when,
                    triggers,
                    cast(List[HotStringOptions], options),
                    from_device,
                )
                self.emitter.hotstrings.append(hotstring)
            elif isinstance(trigger, list):
                hotkey = HotKey(
                    trigger,
                    action,
                    when,
                    cast(List[HotKeyOptions], options),
                    from_device,
                )
                self.emitter.hotkeys.append(hotkey)
            return action

        return wrapper

    def remap(
        self,
        src: Input,
        dest: Input,
        when: Callable[[], bool] = lambda: True,
        options: List[RemapOptions] = [],
        from_device: Optional[str] = None,
    ):
        """Remaps the src to the dest. Other options and context-sensitivity can be applied."""
        remap = Remap(src, dest, when, options, KeyState.Press, from_device)
        self.emitter.remaps.append(remap)

    def enable_scroll_lock(self):
        """Hack that allows the usage of ScrollLock. Must always be called if you
        want to use ScrollLock. Note: This requires xmodmap to be installed."""
        os.system("xmodmap -e 'add mod3 = Scroll_Lock'")


__all__ = [
    "Automaton",
    "Action",
    "ActionEmitter",
    "Context",
    "HotKey",
    "HotKeyOptions",
    "HotString",
    "HotStringOptions",
    "Macro",
    "Redirect",
    "Remap",
    "RemapOptions",
    "CHAR_CODES",
    "HOTSTRING_TRIGGERS",
    "SCANCODES",
    "SHIFT_CODES",
    "ActionString",
    "Button",
    "Callable",
    "Callback",
    "Device",
    "EmissionState",
    "Input",
    "InputStream",
    "Key",
    "KeyState",
    "LockState",
    "Peripheral",
]
