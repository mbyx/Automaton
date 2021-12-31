# Automaton

```

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

    def close(self) -> None:
        """Closes the dummy device"""

    def _get_event(self) -> Iterator[Tuple[evdev.InputEvent, str]]:
        """Wrapper around InputStream.read(). Necessary as read cannot be called more than
        once, yet is required in two separate areas."""

    def run(self) -> None:
        """Starts the automaton main loop. This has to be called in order for automaton to function.
        It functions by redirection and suppression of events from slave devices into the master device.
        The middleman performs all the logic."""

    def record_until(self, condition: Callable[[], bool]) -> Macro:
        """Records a series of events into a Macro until a specific condition becomes
        false."""

    def on(
        self,
        trigger: Union[List[Input], str],
        when: Callable[[], bool] = lambda: True,
        options: List[Union[HotKeyOptions, HotStringOptions]] = [],
        triggers: List[Input] = HOTSTRING_TRIGGERS,
        from_device: Optional[str] = None,
    ) -> Callable[[Any], Any]:
        """Takes in either a List of keys, or a string. If a string is given, a hotstring is
        registered, otherwise a hotkey is registered. Options and context-sensitivity can be
        applied."""

    def remap(
        self,
        src: Input,
        dest: Input,
        when: Callable[[], bool] = lambda: True,
        options: List[RemapOptions] = [],
        from_device: Optional[str] = None,
    ) -> None:
        """Remaps the src to the dest. Other options and context-sensitivity can be applied."""

    def enable_scroll_lock(self) -> None:
        """Hack that allows the usage of ScrollLock. Must always be called if you
        want to use ScrollLock. Note: This requires xmodmap to be installed."""
```