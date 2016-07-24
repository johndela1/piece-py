from analyze import  Pattern, p_tss
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

def pattern(name, bpm):
    return Pattern((4, 4), bpm, [[1], [1], [1], [1]])


def analysis(pattern, tss_in):
    return analyze.analysis(p_tss(pattern), tss_in)
if __name__ == '__main__':
    import pdb;pdb.set_trace()
