#!/usr/bin/python

from cmath import isclose
from collections import namedtuple
from copy import copy
from itertools import accumulate

SECS_PER_MIN = 60
TOLERANCE = 80


def deltas_tss(deltas):
    yield from accumulate(deltas)


def bpm_bps(bpm):
    return bpm / SECS_PER_MIN


def secs_millis(t):
    return t * 1000


def pattern_deltas(pattern, bpm):
    (beats, beat_unit), notes = pattern
    note_duration = int(secs_millis(beat_unit / beats) / bpm_bps(bpm))
    acc = 0
    deltas = []
    for note in notes:
        if note:
            deltas.append(acc)	
            acc = note_duration
        else:
            acc += note_duration
    return deltas


def pattern_tss(pattern, bpm):
    return deltas_tss(pattern_deltas(pattern, bpm))


def good_match(ts, tss):
    return next(
        (x for x in tss if isclose(ts, x, abs_tol=TOLERANCE)), None)


def analysis(tss_ref, tss_in):
    deltas = []
    missing = []
    tss_in_remaining = copy(tss_in)
    for ts_ref in tss_ref:
        ts_in = good_match(ts_ref, tss_in_remaining)
        if ts_in is None:
            missing.append(ts_ref)
        else:
            deltas.append((ts_ref, (ts_in - ts_ref)))
            tss_in_remaining.remove(ts_in)
    return dict(deltas=deltas, misses=missing, extras=tss_in_remaining)


def trial(tss_ref, tss_in):
    return (len(tss_ref) == len(tss_in) and
        not any(map(lambda x: abs(x) > TOLERANCE,
                [ts_ref - ts_in for ts_ref, ts_in in zip(tss_ref, tss_in)])))


##########################################


def easier(pattern, patterns):
    def cmp(x, y):
        return x[0]*x[1] - y[0]*y[1]
    low = 0
    hi = len(patterns) - 1
    while low < hi:
        mid = (low+hi) >> 1
        delta = cmp(pattern, patterns[mid])
        if delta == 0:
            return patterns[mid >> 1]
        elif delta < 0:
            hi = mid
        else:
            low = mid+1


def p_t(pattern):
    (beats, beat_unit), bpm, notes = pattern
    for i, note in enumerate(notes):
        subdivs = len(note)
        period = beat_unit*1000*SECS_PER_MIN / (bpm*beats)
        note_duration = int(secs_millis(beat_unit / beats) / bpm_bps(bpm))
        assert  period == note_duration
        ts = i * secs_millis((beats / bpm_bps(bpm)) / beat_unit)
        for sub in range(subdivs):
            if note[sub]: yield int(ts)
            ts += note_duration / subdivs

def p_d(pattern):
    (beats, beat_unit), bpm, notes = pattern
    acc = 0
    for note_group in notes:
        subdivs = len(note_group)
        note_duration = secs_millis(SECS_PER_MIN / bpm) / subdivs
        for sub in range(subdivs):
            if note_group[sub]:
                yield acc
                acc = note_duration
                continue
            acc += note_duration


if __name__ == '__main__':
    Pattern = namedtuple('Pattern', ('sig', 'bpm', 'notes'))
    pattern = Pattern((4, 4), 60, [[1, 1], [1], [1], [1]])
    print(list(p_t(pattern)))
    assert((list(p_t(pattern))) == [0, 500, 1000, 2000, 3000])
    pattern = Pattern((4, 4), 60, [[1, 1, 1], [1], [1], [1]])
    print(list(p_t(pattern)))
    assert((list(p_t(pattern))) == [0, 333, 666, 1000, 2000, 3000])
    pattern = Pattern((4, 4), 60, [[1, 1], [1, 1, 1], [1, 1], [1, 1, 1]])
    print(list(p_t(pattern)))
    assert((list(p_t(pattern))) ==
           [0, 500, 1000, 1333, 1666, 2000, 2500, 3000, 3333, 3666])
