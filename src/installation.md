# Installation

Automaton is hosted on [github](https://www.github.com/Abdul-Muiz-Iqbal/Automaton) as well as [pypi](https://pypi.org/project/automaton-linux/). The preferred method of installation is via pip. As Automaton requires root previleges in order to function properly, the package must be installed as root as well:  
```
$ sudo pip install automaton-linux
```  
Automaton supports Python3.8+
Automaton has few dependencies, but if an error occurs when building evdev, make sure that you have the python headers installed. On debian, this is as simple as:  
```
$ sudo apt-get install python3-dev
```

To make sure that it is working properly, open a python repl **as root** and type the following:
```python3
from automaton import *

for device in Automaton.find_devices():
    print(device)
```
This should output each device in the following format:
```name :: path```
The paths may change when the devices are disconnected, however the names will remain the same as long as the device is the same.  

Note down the path of your keyboard and mouse, and then go to the next page.