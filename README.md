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

Automaton is a library based on uinput designed to be a substitute for autohotkey in linux.
It has support for HotKeys, HotStrings, and Remaps with configurable options, context sensitivity, and device manipulation.

### Note
Automaton supports only Linux.
Automaton uses uinput in order to work. Therefore, install Automaton and run its apps via:
```shell
sudo pip install automaton-linux
sudo python3 main.py # main.py contains the Automaton app
```

### Usage
A simple Automaton script looks like:
```python3
from automaton import Automaton

app = Automaton.new()

@app.on("btw")
def btw():
    return "by the way"
    
app.run()
```
More info in the [docs](https://abdul-muiz-iqbal.github.io/Automaton/index.html), or take a look at some [examples](https://github.com/Abdul-Muiz-Iqbal/Automaton/tree/main/examples)!

### Used in
- https://github.com/Abdul-Muiz-Iqbal/MacroPad

### Requirements
- [Python](https://python.org/download) >= 3.8
- Python Headers (`Python.h`)
On Ubuntu, getting them is as simple as `sudo apt-get install python3-dev`
