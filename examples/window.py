from automaton import Window

# Print the names of all open windows.
for window in Window.get_all_windows():
    print(window.name)

# Get a window with the word YouTube in its title.
wnd: Window = Window.get('YouTube') # It also takes a keyword arg called strict=False, which forces the title to exactly match the title.
if wnd is not None: # It returns None if no matching window was found.
    window \
        .minimize() \
        .maximize() \
        .close() # You can chain actions to the windows. Minimize, Maximize, Close, etc.

# Get the current active window
wnd: Window = Window.get_active_window()
# Check if this window is the active window, redundant in this case.
if wnd.is_active():
    print("Yay!")