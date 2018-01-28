#!/usr/bin/python

from cmath import isclose
import operator
from statistics import variance

SECS_PER_MIN = 60
TOLERANCE = 80


def bpm_bps(bpm):
    return bpm / SECS_PER_MIN


def secs_millis(t):
    return t * 1000


def good_match(ts, tss):
    return next(
        (x for x in tss if isclose(ts, x, abs_tol=TOLERANCE)), None)


def analysis(ref_tssref, in_tss):
    deltas = []
    missing = []
    remaining_in_tss = list(in_tss)
    for ref_rs in ref_tss:
        ts_in = good_match(ref_ts, remaining_in_tss)
        if in_ts is None:
            missing.append(ref_ts)
        else:
            deltas.append((ref_ts, (in_ts - ref_ts)))
            remaining_in_tss.remove(in_ts)

    return dict(
        deltas=deltas,
        misses=missing,
        extras=remaining_in_tss,
        result=not extras and not missing,
        )

def analysis2(ref_tss, in_tss):
    def to_deltas(tss):
        return [(t1 - t0) for t0, t1 in zip(tss, tss[1:])]

    def deltas_diff(dts1, dts2):
        return [(x - y) for x, y in zip(dts1, dts2)]

    ref_deltas = to_deltas(ref_tss)
    in_deltas = to_deltas(in_tss)
    return deltas_diff(ref_deltas, in_deltas)


x = analysis2([100,200,300,400,500],[100,206,306, 406, 506])
print(x)


def trial(ref_tss, in_tss):
    if len(ref_tss) != len(in_tss):
        return False

    def in_tolerance(x):
        return abs(x) <= TOLERANCE

    deltas = map(operator.sub, ref_tss, in_tss)
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
        sub_divs = len(note)
        period = beat_unit*1000*SECS_PER_MIN / (bpm*beats)
        note_duration = int(secs_millis(beat_unit / beats) / bpm_bps(bpm))
        assert  period == note_duration
        ts = i * secs_millis((beats / bpm_bps(bpm)) / beat_unit)
        for sub in range(sub_divs):
            if note[sub]: yield int(ts)
            ts += note_duration / sub_divs


def p_dts(pattern, bpm):
    (beats, beat_unit), notes = pattern
    acc = 0
    for note_group in notes:
        sub_divs = len(note_group)
        note_duration = secs_millis(SECS_PER_MIN / bpm) / sub_divs
        for sub in range(sub_divs):
            if note_group[sub]:
                yield acc
                acc = note_duration
                continue
            acc += note_duration


def err_sum(deltas):
    dts = [dt for _, dt in deltas]
    return (sum(map(abs, dts)), variance(dts))
