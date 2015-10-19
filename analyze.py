from cmath import isclose
from time import time
from collections import namedtuple

BEAT = 4
SECS_MIN = 60
TOLERENCE = 80

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
	if isclose(t, tss[0], abs_tol=TOLERENCE):
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

if __name__ == '__main__':
	print(reshape(analysis([0,100,200], [0, 101, 300])))
