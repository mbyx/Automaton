# Automaton - A Linux Automation Library

### Note
Automaton supports only Linux.
Automaton uses uinput in order to work. Therefore, install Automaton and run its apps via:
```shell
sudo pip3.9 install automaton-linux
sudo python3.9 main.py # main.py contains the Automaton app
```

### What is it
Automaton is a library based on uinput designed to be a substitute for autohotkey in linux.
It has support for HotKeys, HotStrings, and Remaps with configurable options, context sensitivity, and device manipulation.

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
More info in the docs (coming soon!). Until I have the docs fixed, take a look at some [examples](https://github.com/Abdul-Muiz-Iqbal/Automaton/tree/main/examples)!

### Requirements
- [Python](https://python.org/download) >= 3.9
- Libraries in [requirements.txt](https://github.com/Abdul-Muiz-Iqbal/Automaton/blob/main/requirements.txt) (duh!)
