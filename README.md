<div align="center">
  <h1>Automaton</h1>

  <p>
    <strong>A Linux Automation Library.</strong>
  </p>

  <p>
    <img src="https://img.shields.io/pypi/l/automaton-linux" alt="License: MIT" style="max-width:100%;">
    <a href="https://pypi.org/project/automaton-linux/" rel="nofollow"><img src="https://img.shields.io/pypi/v/automaton-linux" alt="Version" style="max-width:100%;"></a>
    <a href="https://abdul-muiz-iqbal.github.io/Automaton/index.html" rel="nofollow"><img src="https://img.shields.io/badge/Manual-online-brightgreen" alt="Manual" style="max-width:100%;"></a>
  </p>

</div>

Automaton is a library based on uinput designed to be a substitute for [AutoHotkey](https://www.autohotkey.com/) in linux.
It has support for hotkeys, hotstrings, and remaps with configurable options, context sensitivity, and device manipulation.

### Note
Automaton supports only Linux.
Automaton uses uinput in order to work. So your user should either be in the input group, or install Automaton and run scripts as:
```shell
sudo pip install automaton-linux
sudo python3 main.py # main.py contains the Automaton app
```

### Usage
A simple Automaton script looks like:
```python3
from automaton import Automaton

# devices is a list of paths to the devices that you want to manipulate or monitor.
# More information on how to get the path for your device is in the Manual
app = Automaton.new(devices = [
  '/dev/input/event5',
  '/dev/input/event6'
])

# When btw is typed, hit space. It should be replaced with 'by the way'
@app.on("btw")
def btw():
    return "by the way"
    
app.run() # Blocking.
```
More info in the [docs](https://abdul-muiz-iqbal.github.io/Automaton/index.html), or take a look at some [examples](https://github.com/Abdul-Muiz-Iqbal/Automaton/tree/main/examples)!

### Used in
- https://github.com/Abdul-Muiz-Iqbal/MacroPad

### Requirements
- [Python](https://python.org/download) >= 3.8
- Python Headers (`Python.h`)
On Ubuntu, getting them is as simple as `sudo apt-get install python3-dev`
