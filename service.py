from itertools import chain

from analyze import p_tss, p_dts
import analyze
from db2 import Delta, Extra, Miss, session, Pattern


def write(a):
    attempt = Attempt(
            deltas=[Delta(ts=ts, val=val) for ts, val in a['deltas']],
            extras=[Extra(ts=ts) for ts in a['extras']],
            misses=[Miss(ts=ts) for ts in a['misses']],
            )
    session.add(attempt)
    session.flush()


def deltas_with_note_count(name, bpm):
    pattern = session.query(Pattern).filter_by(name=name).one()
    return (p_dts(((pattern.beats, pattern.beat_unit), eval(pattern.notes)), bpm),
            len(list(chain(*(eval(pattern.notes))))))


def submit(name, bpm, tss_in):
    pattern = session.query(Pattern).filter_by(name=name).one()
    tss_ref = p_tss(((pattern.beats, pattern.beat_unit), eval(pattern.notes)), bpm)
    return analyze.analysis(tss_ref, tss_in)


#session.add(Pattern(name='easy-4', beats=4, beat_unit=4, notes='[[1], [1], [1], [1]]'))
#session.add(Pattern(name='2-3', beats=4, beat_unit=4, notes='[[1,1], [1,1,1]]'))
#session.commit()
if __name__ == '__main__':
    import pdb;pdb.set_trace()
