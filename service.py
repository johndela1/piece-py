from analyze import analysis
from db2 import *


def write(a):
    attempt = Attempt(
            deltas=[Delta(ts=ts, val=val) for ts, val in a['deltas']],
            extras=[Extra(ts=ts) for ts in a['extras']],
            misses=[Miss(ts=ts) for ts in a['misses']],
            )
    session.add(attempt)
    session.flush()


if __name__ == '__main__':
    tss_ref=[0,500,1000,2500,10000]
    tss_in=[10,470,1000,2700, 2800, 240]
    write(analysis(tss_ref, tss_in))
    session.commit()

    import pdb;pdb.set_trace()
