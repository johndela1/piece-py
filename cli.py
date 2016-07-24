from time import sleep
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


def play(deltas):
    for dt in deltas:
        sleep(dt/1000)
        print("X")


if __name__ == '__main__':
    name = 'easy-4'
    bpm = 120
    deltas, note_count = service.deltas_with_note_count(name=name, bpm=bpm)

    play(deltas)

    tss_raw = list(get_input(note_count))
    tss_in = [int(1000 * (ts - tss_raw[0])) for ts in tss_raw]

    print(service.submit(name, bpm, tss_in))
