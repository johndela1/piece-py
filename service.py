from itertools import chain
import json

from analyze import p_tss, p_dts, trial, err_sum
import analyze
from model import Delta, Extra, Miss, session, Pattern, Attempt


def write(analysis, name, bpm):
    session.add(
        Attempt(
            deltas=[Delta(ts=ts, val=val) for ts, val in analysis['deltas']],
            extras=[Extra(ts=ts) for ts in analysis['extras']],
            misses=[Miss(ts=ts) for ts in analysis['misses']],
            result=analysis['result'],
            pattern_id=session.query(Pattern).filter_by(name=name).one().id,
            bpm=bpm,
            )
        )
    session.commit()


def get_pattern(name):
    p = session.query(Pattern).filter_by(name=name).one()
    return ((p.beats, p.beat_unit), eval(p.notes))


def deltas_with_note_count(name, bpm):
    pattern = get_pattern(name)
    note_count = len(list(chain(*pattern[1])))
    deltas = [i for i in p_dts(pattern, bpm)]
    return (deltas, note_count)


def submit(name, bpm, tss_in):
    pattern = get_pattern(name)
    tss_ref = p_tss(pattern, bpm)
    analysis = analyze.analysis(tss_ref, tss_in)
    write(analysis, name, bpm)
    return analysis


if not session.query(Pattern).first():
    session.add(
        Pattern(
            name='easy-4',
            beats=4, beat_unit=4,
            notes='[[1], [1], [1], [1]]',
            )
        )
    session.add(
        Pattern(
            name='2-3',
            beats=4, beat_unit=4,
            notes='[[1,1], [1,1,1]]',
            )
         )
    session.commit()


if __name__ == '__main__':
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8001))
    while True:
        data, addr = sock.recvfrom(1024)
        name = data.decode('utf8').rstrip('\0')
        print("pname", name)
        res = json.dumps(deltas_with_note_count(name, 60))
        print("res", res)
        sock.sendto(res.encode(), addr)
