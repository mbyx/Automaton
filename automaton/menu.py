from dataclasses import dataclass
from typing import Any
import tkinter as tk

# Create a global window that is reused for every context menu.
ROOT: tk.Tk = tk.Tk()
ROOT.withdraw() # Hide the window.
ROOT.grab_set()

ignore = lambda *_: None

# Default options for how the menus look. This creates a dark themed menu
OPTIONS: dict[str, str] = {
    'background': '#272C34',
    'foreground': '#FFF',
    'activeborderwidth': '0.3',
    'activebackground': '#2c3747',
    'activeforeground': '#fff',
    'borderwidth': '0.4',
    'relief': 'groove',
    'font': 'Consolas'
}

@dataclass
class ContextMenu:
    """A Context Menu created from tkinter. It uses nested dictionaries in order to
    specify callbacks and menu items. Separators can be added with the special ---
    string. A function ignore is given to improve this process."""
    tree: dict[str, Any]
    menu = None

    def at(self, x: int, y: int):
        """Display the context menu at the specified position. All events will be directed
        to the menu while in focus."""
        self.build(ROOT) # Create a tk.Menu object from `tree`
        try:
            self.menu.tk_popup(x, y)
            self.menu.focus_force() # Allows the keyboard to navigation across the menu.
        finally:
            self.menu.grab_release()

    def build(self, root):
        """Builds a tk.Menu from the nested dictionary. Mainly an internal function."""
        self.menu = tk.Menu(root, tearoff=0, **OPTIONS)
        for name, value in self.tree.items():
            if isinstance(value, dict): # Recursively build the Menu and submenus
                m2 = ContextMenu(value).build(self.menu)
                self.menu.add_cascade(label=name, menu=m2)
            elif name == '---': # Special string --- adds a separator
                self.menu.add_separator()
            else:
                self.menu.add_command(label=name, command=value, underline=0)
        return self.menu
