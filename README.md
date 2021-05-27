# Automaton - A Linux Automation Library

### Note
Automaton supports only linux, with distributions that use gtk. For example, Ubuntu

### What is it
Automaton is a collection of libraries and custom modules designed to provide the easiest
interface to use when automating things in linux. It has support for Dialogs, ContextMenus,
Window manipulation and queries, keyboard and mouse manipulation and queries, hotkeys, hotstrings, and remaps.
### Usage
A simple Automaton script looks like this:
```python3
from automaton import Automaton

app = Automaton()

@app.hotstring("btw")
def btw():
    return "by the way!"

app.listen()
```
More info in the (non-existant) docs.

### Requirements
- Python 3.9+
- Wnck
- Whatever is in requirements.txt (duh!)