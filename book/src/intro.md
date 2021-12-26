# Introduction

### What is Automaton?
Automaton is a library to perform certain tasks when certain keys are pressed in a specific order. It can be used for all manner of keyboard and mouse related projects, whether for manipulation of said devices or for the capturing of input from those devices. It provides a number of builtin methods of listening for input from the keyboard, such as hotkeys, hotstrings and the like.  

### How does it work?
It is meant to be a replacement for [AutoHotkey](https://www.autohotkey.com/), which does not work on Linux. It makes use of the linux [evdev](https://en.wikipedia.org/wiki/Evdev) interface and as such requires root previleges and will run only on Linux. Automaton is focused on being the perfect tool for the creation of macros and other keyboard shortcuts.  

### What does it refer to?
Automaton is divided into two parts; the library itself, which is written in [Python](https://www.python.org), and the `autumn` language, which makes use of the library to allow simple tasks to be done with relative ease. The latter is similar to the AutoHotkey language, though syntatically different. The library can be used without the language itself, something that is different from AutoHotkey.

### Why should I use it?
When questioned about why should you use this instead of AutoHotkey, the answer is simple. You can't use AutoHotkey on Linux. Nor can you use Automaton on Windows. But there are many more libraries and applications in Linux that help solve this exact same problem. Most notable among them are [keyboard](https://github.com/boppreh/keyboard/) and [mouse](https://github.com/boppreh/mouse), [pynput](https://github.com/moses-palmer/pynput), and [AutoKey](https://github.com/autokey/autokey). 

Automaton was created with a single goal in my mind: a replacement for AutoHotkey on Linux. Automaton therefore has the most feature parity with AutoHotkey than all of these other libraries. For an avid Windows user who's recently switched to Linux, while the syntax for Automaton may be different, you will be able to do most of what AutoHotkey does with the same few lines of code.

With all that said, here's a neat table that summarizes the pros and cons of automaton, because tables _never_ lie.  
#### Pros:  
- Can be used across Linux. Not _just_ x11, or KDE, **all** of Linux.  
- Almost complete feature parity with AutoHotkey.  
- Supports unicode 䔄 (looking at you, keyboard)  
- Supports key suppression.  
#### Cons:  
- Does not work on Windows.