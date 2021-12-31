from automaton import Automaton, Key, Button, LockState

# Remember to change to your device path.
app = Automaton.new(devices=["/dev/input/event6", "/dev/input/event5"])

# Access keyboard/mouse like so
# Press the left shift key, but do not release it.
app.device.press(Key.LShift)
app.device.release(Key.LShift)  # Release the left shift key, if its pressed.

# You can press, release, or tap multiple keys at the same time:
app.device.press(Key.LCtrl, Key.LShift)
app.device.release(Key.LCtrl, Key.LShift)

app.device.tap(Key.LShift)  # Presses and releases the left shift key
app.device.tap(Key.LCtrl, Key.LShift)

app.device.type("Hello, World! 攄")  # Types a string. Can be any utf-8 value.
app.device.type_ascii("Hello, World!")  # Types a string. Can be any utf-8 value.

print(app.device.is_pressed(Key.LShift))  # Returns True if left shift is pressed.
print(app.device.is_toggled(Key.CapsLock))  # Returns True if capslock is toggled on
app.device.set_state(Key.CapsLock, LockState.On)  # Toggles the capslock on.

# NOTE: The following uses Computer Coordinate System, so (0, 0) is the top left.
# (0, 0) ============== (5, 0)
# ============================
# ============================
# ============================
# (0, 5) ============== (5, 5)

app.device.move_rel(100, 100)  # Moves 100px Left and 100px Down.
app.device.drag_rel(10, 100, Button.MiddleButton) # Drag the middle mouse button 10px Left and 100px Down.

app.run()