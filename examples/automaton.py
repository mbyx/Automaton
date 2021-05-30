from automaton.automaton import Automaton, Key, RELEASE
import datetime

# Create an instance of Automaton.
# WARNING: Automaton works by taking control over your keyboard and mouse devices,
# and then redirecting their events to a dummy device called Automaton. This may
# result in some unexpected consequences, which is why it has a failsafe. By default,
# it is Ctrl+Esc, but you can change it with the failsafe keyword arg.
app = Automaton(keyboard = '/dev/input/event6', mouse = '/dev/input/event6') # Pass in the path to the keyboard and mouse.
# If you aren't sure where your device is, you can use this:
# Automaton.active_device() # Returns the device path with the latest event

# Hotstrings are registered by decorating a function.
# The trigger string only allows ascii. The string returned (if any) is typed. Unicode is supported for the typed string.
@app.hotstring(":date")
def get_date():
    return f'{datetime.date.today()}'

# Hotkeys are also registered by decorating a function.
# The triggers can be numerous, but are sorted by their scancode. Meaning Shift+A and A+Shift are both allowed.
@app.hotkey(Key.LShift, Key.A)
def shift_a():
    print("Who pressed me?")

# Remaps are registered by calling remap and passing in src and dest keys.
# The src key is suppressed and replaced by the dest key. Here, Numpad4 is remapped to the left button of the mouse.
app.remap(Key.Numpad4, Key.LeftButton)

# ADVANCED
# Hotstrings, Hotkeys and remaps have a keyword arg called register_if. These actions
# are activated if register_if() returns True. Otherwise, the action never happens.
# Remaps K to A only IF 1 == 2. So never.
app.remap(Key.K, Key.A, register_if = lambda: 1 == 2)

# Remap only feature. You can activate the remap when the key is released instead of when its pressed.
app.remap(Key.B, Key.A, fire_on = RELEASE)

# You can also emit callbacks when any key is pressed or released:
app.on_press(lambda event: print(event.code))
app.on_release(lambda event: print(event.code))

# Multiple callbacks are allowed.
app.on_press(lambda event: print(event.value))

app.listen() # Start listening and redirecting events. Hotkeys and such won't work without this.
