from automaton import Automaton, Key, Button
import datetime

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
app = Automaton.new(devices = ['/dev/input/event6', '/dev/input/event5']) # Pass in the path to the keyboard and mouse.

# Hotstrings are registered by decorating a function.
# The trigger string allows unicode. The string returned (if any) is typed. Unicode is also supported for the typed string.
@app.on(":date")
def get_date():
    return f'{datetime.date.today()}'

# Hotkeys are also registered by decorating a function.
# The triggers can be numerous, but are sorted by their scancode. Meaning Shift+A and A+Shift are both allowed.
@app.on([Key.LShift, Key.A])
def shift_a():
    print("Who pressed me?")

# Remaps are registered by calling remap and passing in src and dest keys.
# The src key is suppressed and replaced by the dest key. Here, Numpad4 is remapped to the left button of the mouse.
app.remap(Key.Numpad4, Button.LeftButton)

# ADVANCED
# Hotstrings, Hotkeys and remaps have a keyword arg called register_if. These actions
# are activated if register_if() returns True. Otherwise, the action never happens.
# Remaps K to A only IF 1 == 2. So never.
app.remap(Key.K, Key.A, context = lambda: 1 == 2)

# You can also emit callbacks when any key is pressed or released:
app.on_press(lambda event: print(event.code))
app.on_release(lambda event: print(event.code))

# Multiple callbacks are allowed.
app.on_press(lambda event: print(event.value))

app.run() # Start listening and redirecting events. Hotkeys and such won't work without this.
