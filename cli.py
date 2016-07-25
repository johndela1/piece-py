from time import sleep
from evdev import InputDevice, ecodes

import service

PRE_SCALER = 1000

def get_tss_in(n):
    dev = InputDevice('/dev/input/event8')
    x = 0
    base = None
    tss = []
    for e in dev.read_loop():
        if x >= n:
            break
        if e.type == ecodes.EV_KEY and e.value == 1:
            if base == None:
                base = e.timestamp()
            x += 1
            tss.append(int((e.timestamp()-base)*PRE_SCALER))
    return tss

def play(deltas):
    for dt in deltas:
        sleep(dt/PRE_SCALER)
        print("X")


if __name__ == '__main__':
    name = 'easy-4'
    name = '2-3'
    bpm = 60
    deltas, note_count = service.deltas_with_note_count(name=name, bpm=bpm)

    play(deltas)
    tss_in = get_tss_in(note_count)

    print(service.submit(name, bpm, tss_in))
