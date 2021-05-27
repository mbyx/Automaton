from dataclasses import dataclass
from typing import Any
import tkinter as tk

ROOT = tk.Tk()
ROOT.withdraw()
ROOT.grab_set()

ignore = lambda *_: None

OPTIONS = {
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
        self.build(ROOT)
        try:
            self.menu.tk_popup(x, y)
            self.menu.focus_force()
        except:
            self.menu.grab_release()

    def build(self, root):
        """Builds a tk.Menu from the nested dictionary. Mainly an internal function."""
        self.menu = tk.Menu(root, tearoff=0, **OPTIONS)
        for name, value in self.tree.items():
            if isinstance(value, dict):
                m2 = ContextMenu(value).build(self.menu)
                self.menu.add_cascade(label=name, menu=m2)
            elif name == '---':
                self.menu.add_separator()
            elif name.startswith('^'):
                self.menu.add_checkbutton(
                    label=name, command=value, underline=0)
            elif name.startswith('*'):
                self.menu.add_radiobutton(
                    label=name, command=value, underline=0)
            else:
                self.menu.add_command(label=name, command=value, underline=0)
        return self.menu
