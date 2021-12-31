import datetime

from automaton import Automaton, Button, Key

# Create an instance of Automaton.
# WARNING: Automaton works by taking control over your keyboard and mouse devices,
# and then redirecting their events to a dummy device called Automaton. This may
# result in some unexpected consequences, which is why it has a failsafe. By default,
# it is Ctrl+Esc, but you can change it with the failsafe keyword arg.
# Paths such as  /dev/input/event* are paths to input devices. You can use the following to find the
# keyboard and mouse:
# import evdev
# for device in map(evdev.InputDevice, evdev.list_devices()):
#     print(device.name, '::', device.path)
# Replace with your own device paths. These correspond to my keyboard and mouse.
app = Automaton.new(
    devices=["/dev/input/event6", "/dev/input/event5"]
)  # Pass in the path to the keyboard and mouse.

# Hotstrings are registered by decorating a function.
# The trigger string allows unicode. The string returned (if any) is typed. Unicode is also supported for the typed string.
@app.on(":date")
def get_date():
    return f"{datetime.date.today()}"


# Hotkeys are also registered by decorating a function.
# The triggers can be numerous, but are sorted by their scancode. Meaning Shift+A and A+Shift are both allowed.
@app.on([Key.LShift, Key.A])
def shift_a():
    print("Who pressed me?")


# There are different modifiers for each action. You can get these from automaton.actions:
from automaton.actions import HotKeyOptions, HotStringOptions, RemapOptions


# `HotStringOptions.TriggerInsideWord` Allows hotstring to be triggered even if the trigger text is inside the currently typed word
# Eg:
@app.on("btw", options=[HotStringOptions.TriggerInsideWord])
def btw():  # Typing 'shlbtw' will expand to 'shl by the way'
    return "by the way"


# `HotStringOptions.TriggerImmediately` When applied, does not require a trigger key to activate
# `HotStringOptions.PreventAutoBackspace` When a hotstring is triggered and is a text replacement, do not auto backspace.

# `RemapOptions.DontSuppressKeys` When applied, both the src and dest keys are pressed/released
# `HotKeyOptions.DontSuppressKeys` When applied, the hotkey such as LShift+A will not suppress 'A'

# Remaps are registered by calling remap and passing in `src` and `dest` keys.
# The `src` key is suppressed and replaced by the `dest` key. Here, Numpad4 is remapped to the left button of the mouse.
app.remap(Key.Numpad4, Button.LeftButton)

# Hotstrings, Hotkeys and remaps have a keyword arg called `when`. These actions
# are activated if `when()` returns True. Otherwise, the action never happens.
# when should have the type: `Callable[[], bool]`
# Remaps K to A only IF 1 == 2. So never.
app.remap(Key.K, Key.A, when=lambda: 1 == 2)

# You can also emit callbacks when any key is pressed or released:
app.device.on_press(lambda event: print(f"{event.code} Pressed!"))
app.device.on_release(lambda event: print(f"{event.code} Released!"))

# Multiple callbacks are allowed.
app.device.on_press(lambda event: print(event.value))

app.run()  # Start listening and redirecting events. Monitoring won't work without this.
