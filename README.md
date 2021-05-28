# Automaton - A Linux Automation Library

### Note
Automaton supports only Linux, more specifically Linux distributions that use [GTK](https://www.gtk.org/), for example Ubuntu 20.04.
Automaton uses uinput in order to work. Therefore, install Automaton and run its apps via:
```shell
sudo pip3.9 install automaton
sudo python3.9 main.py # main.py contains the Automaton app
```
### What is it
Automaton is a collection of libraries and custom modules designed to provide the easiest
interface to use when automating things in Linux. It has support for:
- Dialogs
- ContextMenus
- Window manipulation and queries
- HotKeys, HotStrings, and Remaps

### Usage
A simple Automaton script looks like:
```python3
from automaton import Automaton

app = Automaton()

@app.hotstring("btw")
def btw():
    return "by the way"
    
app.listen()
```
More info in the docs (coming soon!). Until I have the docs fixed, take a look at some [examples](https://github.com/Abdul-Muiz-Iqbal/Automaton/tree/main/examples)!

### Requirements
- [Python](https://python.org/download) >= 3.9
- Tkinter
```
$ sudo apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install libglib2.0-0 libgirepository-1.0-1
```
- Libraries in [requirements.txt](https://github.com/Abdul-Muiz-Iqbal/Automaton/blob/main/requirements.txt) (duh!)
