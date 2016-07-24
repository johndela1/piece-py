from itertools import chain

from analyze import  Pattern, p_tss, p_dts
import analyze
from db2 import Delta, Extra, Miss, session


def write(a):
    attempt = Attempt(
            deltas=[Delta(ts=ts, val=val) for ts, val in a['deltas']],
            extras=[Extra(ts=ts) for ts in a['extras']],
            misses=[Miss(ts=ts) for ts in a['misses']],
            )
    session.add(attempt)
    session.flush()


def get_pattern(name, bpm):
    return Pattern((4, 4), bpm, [[1], [1], [1], [1]])


def deltas_with_note_count(name, bpm):
    pattern = get_pattern(name, bpm)
    return p_dts(pattern), len(list(chain(*pattern.notes)))


def submit(name, bpm, tss_in):
    pattern = get_pattern(name, bpm)
    tss_ref = p_tss(pattern)
    return analyze.analysis(tss_ref, tss_in)


if __name__ == '__main__':
    import pdb;pdb.set_trace()
