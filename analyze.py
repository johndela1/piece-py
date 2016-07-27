#!/usr/bin/python

from cmath import isclose
import operator

SECS_PER_MIN = 60
TOLERANCE = 80


def bpm_bps(bpm):
    return bpm / SECS_PER_MIN


def secs_millis(t):
    return t * 1000


def good_match(ts, tss):
    return next(
        (x for x in tss if isclose(ts, x, abs_tol=TOLERANCE)), None)


def analysis(tss_ref, tss_in):
    deltas = []
    missing = []
    tss_in_remaining = list(tss_in)
    for ts_ref in tss_ref:
        ts_in = good_match(ts_ref, tss_in_remaining)
        if ts_in is None:
            missing.append(ts_ref)
        else:
            deltas.append((ts_ref, (ts_in - ts_ref)))
            tss_in_remaining.remove(ts_in)

    return dict(
        deltas=deltas,
        misses=missing,
        extras=tss_in_remaining,
        result=not tss_in_remaining and not missing,
        )


def trial(tss_ref, tss_in):
    if len(tss_ref) != len(tss_in):
        return False

    def in_tolerance(x):
        return abs(x) <= TOLERANCE

    deltas = map(operator.sub, tss_ref, tss_in)
    return all(map(in_tolerance, deltas))


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


def p_tss(pattern, bpm):
    (beats, beat_unit), notes = pattern
    for i, note in enumerate(notes):
        subdivs = len(note)
        period = beat_unit*1000*SECS_PER_MIN / (bpm*beats)
        note_duration = int(secs_millis(beat_unit / beats) / bpm_bps(bpm))
        assert  period == note_duration
        ts = i * secs_millis((beats / bpm_bps(bpm)) / beat_unit)
        for sub in range(subdivs):
            if note[sub]: yield int(ts)
            ts += note_duration / subdivs


def p_dts(pattern, bpm):
    (beats, beat_unit), notes = pattern
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
