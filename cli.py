from time import sleep
from evdev import InputDevice, ecodes
from pprint import pprint as pp
import service

PRE_SCALER = 1000

def get_tss_in(n):
    dev = InputDevice('/dev/input/event8')
    base = None
    tss_in = []
    x = 0
    for e in dev.read_loop():
        if not(e.type == ecodes.EV_KEY and e.value == 1):
            continue
        if base is None:
            base = e.timestamp()
        tss_in.append(int((e.timestamp()-base)*PRE_SCALER))
        x += 1
        if x >= n:
            break
    return tss_in

def play(deltas):
    for dt in deltas:
        sleep(dt/PRE_SCALER)
        print("X")


if __name__ == '__main__':
    name = 'easy-4'
    # name = '2-3'
    bpm = 120

    deltas, note_count = service.deltas_with_note_count(name=name, bpm=bpm)
    play(deltas)
    tss_in = get_tss_in(note_count)
    analysis = service.submit(name, bpm, tss_in)
    pp(analysis)
