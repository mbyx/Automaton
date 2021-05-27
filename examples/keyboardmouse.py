from automaton import Automaton, Key, ON

app = Automaton()

# Access keyboard like so
# Press the left shift key, but do not release it.
app.kb.press(Key.LShift)
app.kb.release(Key.LShift) # Release the left shift key, if its pressed.

app.kb.tap(Key.LShift) # Presses and releases the left shift key
app.kb.type("Hello, World!") # Types a string. MUST be ascii

app.kb.is_pressed(Key.LShift) # Returns True if left shift is pressed.
app.kb.is_toggled(Key.CapsLock) # Returns True if capslock is toggled on
app.kb.set_state(Key.CapsLock, ON) # Toggles the capslock on.

# Access mouse like so
# Press the left mouse button. You can technically use kb.press() for this, but not the reverse.
app.ms.press(Key.LeftButton)
app.ms.release(Key.LeftButton) # Release the left mouse button

app.ms.tap(Key.LeftButton) # Press and release the left mouse button

app.ms.is_pressed(Key.RightButton) # Returns True if the right mouse button is pressed
app.ms.move_abs(100, 100) # Moves to 100, 100 on the screen
app.ms.move_rel(100, 100) # Moves 100px Left and 100px Right. 

app.listen()