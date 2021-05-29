from automaton.menu import ContextMenu, ignore

# Create a context menu from a dictionary
ContextMenu({
    "Utils": { # Nested Dictionaries create a cascading menu
        "Copy": lambda: print("Copy!"),
        "Paste": lambda: print("Paste!")
    },  # The string --- is special here; it creates a separator line.
    "---": ignore, # This function ignore does nothing. ignore it.
    "Exit": lambda: print("Exiting...")
}).at(200, 250) # You can show to context menu at some pos by calling at(x, y).
