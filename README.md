# Automaton - A Linux Automation Library

### Note
Automaton supports only linux, with distributions that use gtk. For example, Ubuntu 20.04
Automaton uses uinput in order to work. Therefore, install automaton and run its apps via
```shell
sudo pip3.9 install automaton
sudo python3.9 main.py # Where main.py is an automaton app
```
### What is it
Automaton is a collection of libraries and custom modules designed to provide the easiest
interface to use when automating things in linux. It has support for:
- Dialogs
- ContextMenus
- Window manipulation and queries
- keyboard and mouse manipulation and queries
- Hotkeys
- Hotstrings
- Remaps

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
More info in the (non-existant) docs. Till the docs are fixed, take a look at the examples!

### Requirements
- Python 3.9+
- Tkinter
```
$ sudo apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install libglib2.0-0 libgirepository-1.0-1
```
- Whatever is in requirements.txt (duh!)
