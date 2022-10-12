# Quickstart

A simple Automaton app might look like this:
```
from automaton import *

app = Automaton.new(devices = [
    '/dev/input/event5',
    '/dev/input/event6'
])

app.remap(Key.A, Key.K)

app.run()
```

On line 1, we import everything that we need from Automaton, which is usually everything and the kitchen sink.  

On line 3, we instantiate a new Automaton object. We pass to it a keyword argument, `devices`. This is a list of paths to the devices that we want to monitor or control. Keep in mind, Automaton can only monitor events that the devices are capable of executing.  

On line 8, we call the remap method, which takes two arguments, `src` and `dest`. All it does is remap the `src` key to the `dest` key. If you were to press the `A` key while this script is running, you would find that instead of `a` being typed, a nice fat `k` is typed instead. 

Finally, on line 10, we call the `run` method, which is a blocking call. Only after this method has been called, will the monitoring (and thus the remapping)start. Conversely, controlling a device can be done at any time after the Automaton object has been instantiated.  

While this script is running, if you were to in a separate repl do `Automaton.find_devices()`, you will find a new device, named `Automaton`. This is a UInput device that is created by Automaton. You don't need to care about this much, and the details of how it works are explained in the Internals chapter.

With that simple app out of the way, here are some more examples of automaton apps:

#### Do something when a hotkey is pressed
```
@app.on([Key.LCtrl, Key.LShift, Key.M])
def type_hello():
    app.type("Hello, John!")
```

#### Text replacement
```
from datetime import datetime

@app.on(":date")
def insert_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M")
```

As you can see, the `on()` method is overloaded to either take a list of keys, or a string. This is parsed into a hotkey and hotstring, respectively. 

Another important point is that we are returning a string from the function. This is the replacement text that will be written instead of the hotstring.  

**Note**: You _can_ return a string in a hotkey invocation as well, and it does exactly what you'd expect (it is also written). Therefore, in the hotkey example, we could have just returned the string `"Hello, John!"`

#### Do something when a hotstring is typed
```
import os

@app.on(":shutdown")
def shutdown():
    os.system("shutdown -P")
```

#### Remapping a key to a mouse button
```
app.remap(Key.Numpad4, Button.LeftButton)
```

#### Actions that only works if certain condition are true:
```
# Only work on Fridays the 13th

from datetime import datetime as dt
ominous = lambda: dt.now().weekday() == 4 and dt.now().day == 13

app.remap(Key.A, Key.K, when=ominous)
```

Both `app.on` and `app.remap` have a keyword argument called `when`. It takes a callable that should return a Boolean value. The action will run only when the returned value is true. In this example, all As will be replaced with Ks only on Fridays the 13th.

#### Actions that only works if the requirements are met by a specific device
Say you have two keyboards connected, one being your daily driver, and the other your dedicated macro keyboard. You want your second keyboard and only your second keyboard to do something different when the A key is pressed. What do you do? This!
```
# Assume /dev/input/event5 is your main keyboard...
# and /dev/input/event6 is your macro keyboard.

app = Automaton.new(devices = [
    '/dev/input/event5',
    '/dev/input/event6',
    # We don't care about the mouse here.
])

app.on([Key.A], from_device = '/dev/input/event6')
def macro_keyboard_only():
    print("Only available on MacroKeyboard!")
```

#### Configuring the behaviour of certain actions
If you've ever used AutoHotkey, you'll probably know that you can specify if a hotstring replaces the trigger text or not. There are many other options like that too, and Automaton has them all!
```
app.on(":date", options = [
    # Just one of many. See Api/Actions/HotString
    HotStringOptions.PreventAutoBackspace
])
def date():
    return "No Replacement :)"
```
Pretty much all actions besides `Redirect` have options.

Another thing you can configure in AutoHotkey would be which keys can actually trigger the hotstring after the trigger text has been typed. Guess who can do that as well:
```
app.on(":date", triggers = [Key.Space, Key.K])
def date():
    return "15 March 2022"
```
By default, the triggers keys are the constant `HOTSTRING_TRIGGERS` (see Api/Internals/Constants)

#### Recording a macro, then playing it.
```
macro: Macro = app.record_until(lambda: app.device.is_pressed(Key.Esc))

speed = 1.5 # Speed at which to perform the actions.
macro.play(speed)
```

Note that macros are currently experimental.