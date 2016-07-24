from itertools import chain

from evdev import InputDevice, ecodes

import service

def get_input(n):
    dev = InputDevice('/dev/input/event8')
    x = 1
    for e in dev.read_loop():
        if x > n:
            return
        if e.type == ecodes.EV_KEY and e.value == 1:
            x += 1
            yield e.timestamp()

pattern = service.pattern(name='easy-4', bpm=80)
print(pattern)

tss_raw = list(get_input(len(list(chain(*pattern.notes)))))
tss_in = [int(1000 * (ts - tss_raw[0])) for ts in tss_raw]

print(service.analysis(pattern, tss_in))
