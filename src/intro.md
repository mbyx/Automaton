# Introduction

### What is Automaton?
Automaton is a library that allows you to execute certain operations when certain inputs are given (via input devices connected to your computer). It can be used for almost all keyboard and mouse-related projects, be it manipulating said devices or for capturing their inputs. 

As of yet, it provides a number of built-in methods for listening and capturing the input from your keyboards, allowing you to create hotkeys, hotstrings, and whatnot.

### How does it work?
It is meant to be a replacement for [AutoHotkey](https://www.autohotkey.com/), which does not work on Linux. It makes use of the Linux [evdev](https://en.wikipedia.org/wiki/Evdev) interface and, as such, requires root privileges. Automaton is focused on being the perfect tool for the creation of macros and other keyboard-related gimmicks for Linux.

### The Automaton Project
Automaton is divided into two parts: the library itself, which is written in [Python](https://www.python.org), and the `autumn` language, which makes use of the library to allow simple tasks to be done with relative ease (currently not implemented). The latter is similar to the AutoHotkey language, although syntactically distinct. 

The library itself can be used without the `autumn` language (a feature that AutoHotKey lacks).

### Why should I use it?
The unavailability of AutoHotKey on Linux was indubitably the impetus for this project. Sure, there many other libraries/applications in Linux that provide similar features (notable examples include [keyboard](https://github.com/boppreh/keyboard/) and [mouse](https://github.com/boppreh/mouse), [pynput](https://github.com/moses-palmer/pynput), and [AutoKey](https://github.com/autokey/autokey)), however Automaton, unlike these libraries, offers the most feature parity with AutoHotKey on Linux, being directly based on its design and structure after years of use on Windows. With Automaton, you'll be able to do everything you could with Linux in roughly the same amount of code, though their syntaxes differ.

Here's a neat table that summarizes the pros and cons of Automaton, because tables _never_ lie:
| Pros | Cons |
| --- | --- |
| It can be used on *all* Linux distros. | It does not work on Windows. |
| It offers (almost) complete feature-parity with AHK. | |
| It supports unicode (such as 䔄) unlike [some libraries I could mention](https://pypi.org/project/keyboard/). |
| It supports key compression. | |
