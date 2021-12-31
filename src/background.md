# Background

Before you can start using automaton, you'll need a bit of a lesson. Linux uses an interface for communicating between the keyboard and the kernel, known as evdev. In linux, pretty much everything is a file, and devices are no exception to this.

In the directory `/dev/input/*`, there are a number of files starting with eventN where N is any number which represent all of the devices that are connected to the computer. This includes the keyboard and the mouse.
```bash
$ ls /dev/input/
by-id/    event0  event10  event12  event2  event4  event6  event8  mice    mouse1  mouse3
by-path/  event1  event11  event13  event3  event5  event7  event9  mouse0  mouse2
```

Automaton uses these files in order to do what it does, but you as the user must specify what device you want to capture inputs from. For example, my keyboard and mouse correspond to `/dev/input/event5` and `/dev/input/event4`.

Keep in mind that these paths may change everytime the device is disconnected and reconnected (such as when powering off). To figure out which of these files represent your chosen devices, refer to the next page.