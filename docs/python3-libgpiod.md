https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/

`sudo apt install python3-libgpiod`

Usage `sudo python3 test.py`

`python3 -c 'import gpiod; help(gpiod)' >> help.txt`

---

```
inputs = chip.get_lines([d0, d1, door, aux])

print('offset: {} timestamp: [{}.{}]'.format(
    event.source.offset(),
    event.sec, event.nsec
), end='')

def print_values(lines):
    vals = lines.get_values()

    for val in vals:
        print(val, end=' ')
    print()
```

LineBulk was messing up get/set value and directed everything to the first line so removed
although get_values all together seemed fine
but possibly that relates to the way you could not read interrupt pins values?

---

check if a module exists from command line

`python3 -c 'import state'`

---

can do *args but that's a tuple
**kwargs means the args should be like key=val
the actual names don't matter

---

# does this take care of Ctrl+Z?
# i would rather manually kill the pid
import signal
import os

def handler(signum, frame):
    print('Ctrl+Z pressed, but ignored')
    os.system(f'kill -STOP {os.getpid()}')

signal.signal(signal.SIGTSTP, handler)
