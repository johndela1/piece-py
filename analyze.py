from cmath import isclose
from time import time
from collections import namedtuple

BEAT = 4
SECS_MIN = 60
TOLERANCE = 80

import sys
import select

def deltas_tss(deltas, acc_time=0):
	if not deltas:
		return []
	ts = acc_time + deltas[0]
	return list([ts] + (deltas_tss(deltas[1:], ts)))

def i_deltas_tss(deltas):
	ret = []
	acc = 0
	for delta in deltas:
		ret.append(delta + acc)
		acc += delta
	return ret

def bpm_bps(bpm):
	return bpm / SECS_MIN

def secs_millis(t):
	return t * 1000

def pattern_deltas(pattern, bpm):
	# used when sending pattern to client
	# pattern -> bpm => deltas
	beat_div, notes = pattern
	note_duration = int(secs_millis(BEAT / beat_div) / bpm_bps(bpm))
	acc = 0
	ret = []
	for note in notes:
		if note:
			ret.append(acc)	
			acc = note_duration
		else:
			acc += note_duration
			continue
	return ret

def pattern_tss(pattern, bpm):
	return deltas_tss(pattern_deltas(pattern, bpm))

def result(tss_ref, tss_in):
	return reshape(analysis(tss_ref, tss_in))

def find_match(t, tss):
	if not tss:
		return None
	if isclose(t, tss[0], abs_tol=TOLERANCE):
		return tss[0]
	else:
		find_match(t, tss[1:])

def analysis(tss_ref, tss_in):
	if not tss_ref:
		return list(tss_in)

	sample, samples = tss_ref[0], tss_ref[1:]
	match = find_match(sample, tss_in)

	if match is not None:
		return ([(sample, match - sample)] +
			analysis(samples,
				 [i for i in tss_in if i != match]))
	else:
		return [(sample, None)] + analysis(samples, tss_in)

def trial(tss_ref, tss_in):
    return (len(tss_ref) == len(tss_in) and
        not any(map(lambda x: abs(x) > TOLERANCE,
                [ts_ref - ts_in for ts_ref, ts_in in zip(tss_ref, tss_in)])))

def reshape(analysis):
	ret = {}
	ret['delta'] = []
	ret['miss'] = []
	ret['extra'] = []
	Delta = namedtuple('Delta', ('ts', 'diff'))
	for i in analysis:
		if type(i) == tuple:
			if i[1] is None:
				ret['miss'].append(i[0])
				continue
			ret['delta'].append(Delta(i[0], i[1]))
		else:
			ret['extra'].append(i)
	return ret

##########################################

assert (deltas_tss([0, 500, 500]) == i_deltas_tss([0, 500, 500]) ==
	[0, 500, 1000])
assert pattern_deltas((4, [1, 1, 1, 1]), 60) == [0, 1000, 1000, 1000]
analysis([0,100,200], [0, 101, 300])

def cmp(x, y):
    return x[0]*x[1] - y[0]*y[1]

def easier(pattern, patterns):
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

if __name__ == '__main__':
	#print(reshape(analysis([0,100,200], [0, 101, 300])))
    tss_ref=[0,500,1000]
    tss_in=[10,450,1300]
    print(trial(tss_ref, tss_in))
    tss_in=[0,500,1080]
    print(trial(tss_ref, tss_in))


    patterns = [(div, bpm, int(div/4)) for div in (4,8) for bpm in range(60,121,10)]
    print (str(dict(patterns = patterns)))
    tss_in=(4,100,1)
    print('input:', tss_in)
    print(easier((4,100,1), patterns))
