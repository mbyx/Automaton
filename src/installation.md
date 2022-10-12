# Installation

Automaton is hosted on [GitHub](https://www.github.com/Abdul-Muiz-Iqbal/Automaton) as well as [PyPI](https://pypi.org/project/automaton-linux/). It supports Python >= 3.8. The preferred method of installation is via `pip`. As Automaton requires root privileges in order to function properly, the package must be installed as root as well:  
```
$ sudo pip install automaton-linux
```
Automaton has a few dependencies, but if an error occurs when building `evdev`, make sure that you have the Python headers installed. On Debian, this is as simple as:  
```
$ sudo apt-get install python3-dev
```
To make sure that it is working properly, open a Python repl **as root** and run the following:
```python3
from automaton import *

for device in Automaton.find_devices():
    print(device)
```
This should output each device in the format, ```name :: path```. These paths may change when a device reconnects, however its name will remain the same.

Find the path of your keyboard and mouse, then proceed to the [next page](quickstart.md).