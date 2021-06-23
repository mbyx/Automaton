from .actions import HotKey, HotString, Remap, ActionEmitter, RemapOptions
from .core import InputStream
from typing import Callable, NoReturn, Optional, Union
from .consts import HOTSTRING_TRIGGERS, KeyState, Input
from .peripheral import Peripheral
from dataclasses import dataclass
from .input import Key
import evdev


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
    failsafe: list[Input]

    def new(
        devices: Optional[list[str]] = None,
        failsafe: Optional[list[Input]] = [Key.LCtrl, Key.Esc]
    ) -> 'Automaton':
        """Creates a new instance of Automaton. Takes in a list of devices to act as slaves,
        and a list of keys to be pressed. These act as a special hotkey that can close Automaton."""
        if devices is None:
            devices = evdev.list_devices()
        ui = evdev.UInput.from_device(*devices, name='Automaton')
        
        return Automaton(
            ActionEmitter.new(),
            InputStream(devices),
            Peripheral(ui),
            failsafe
        )

    def close(self):
        """Closes the dummy device"""
        self.device.ui.close()

    def run(self) -> NoReturn:
        """Starts the automaton main loop. This has to be called in order for automaton to function.
        It functions by redirection and suppression of events from slave devices into the master device.
        The middleman performs all the logic."""
        try:
            for event in self.stream.read():
                action = self.emitter.handle(event, self.device)
                self.device.update(event)
                if list(map(int, self.failsafe)) in [self.emitter.context.active_keys]:
                    raise KeyboardInterrupt
                action.emit(self.device, self.emitter.context)
        finally:
            self.close()

    def on(
        self, trigger: Union[list[Input], str],
        context: Callable[[], bool] = lambda: True,
        options: list[RemapOptions] = [],
        triggers: list[Input] = HOTSTRING_TRIGGERS
    ):
        """Takes in either a list of keys, or a string. If a string is given, a hotstring is
        registered, otherwise a hotkey is registered. Options and context-sensitivity can be
        applied."""
        def wrapper(action):
            if isinstance(trigger, str):
                hotstring = HotString(trigger, action, context, triggers, options)
                self.emitter.HOTSTRINGS.append(hotstring)
            elif isinstance(trigger, list):
                hotkey = HotKey(trigger, action, lambda: True, [], [])
                self.emitter.HOTKEYS.append(hotkey)
            return action
        return wrapper

    def remap(
        self, src: Input, dest: Input,
        context: Callable[[], bool] = lambda: True,
        options: list[RemapOptions] = []
    ):
        """Remaps the src to the dest. Other options and context-sensitivity can be applied."""
        remap = Remap(src, dest, context, options, KeyState.Press)
        self.emitter.REMAPS.append(remap)
