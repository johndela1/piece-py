from cmath import isclose
from time import time
from collections import namedtuple

BEAT = 4
SECS_MIN = 60
TOLRENCE = 80

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

def pattern_deltas(note_div, notes, bpm):
	# used when sending pattern to client
	# pattern -> bpm => deltas
	note_duration = int(secs_millis(BEAT / note_div) / bpm_bps(bpm))
	acc = 0
	ret = []
	for note in notes:
		if note == 0:
			acc += note_duration
			continue
		ret.append(acc)	
		acc = note_duration
	return ret

def find_match(t, tss):
	if not tss:
		return None
	if isclose(t, tss[0], abs_tol=TOLRENCE):
		return tss[0]
	else:
		find_match(t, tss[1:])

def analysis(ref_tss, input_tss):
	if not ref_tss:
		return list(input_tss)

	sample, samples = ref_tss[0], ref_tss[1:]
	match = find_match(sample, input_tss)

	if match is not None:
		return ([(sample, match - sample)] +
			analysis(samples,
				 [i for i in input_tss if i != match]))
	else:
		return [(sample, None)] + analysis(samples, input_tss)

def reshape(analysis):
	ret = {}
	ret['deltas'] = []
	ret['missed'] = []
	ret['extra'] = []
	Delta = namedtuple('Delta', ('ts', 'diff'))
	for i in analysis:
		if type(i) == tuple:
			if i[1] is None:
				ret['missed'].append(i[0])
				continue
			ret['deltas'].append(Delta(i[0], i[1]))
		else:
			ret['extra'].append(i)
	return ret

		
##########################################

assert (deltas_tss([0, 500, 500]) == i_deltas_tss([0, 500, 500]) ==
	[0, 500, 1000])
assert pattern_deltas(4, [1, 1, 1, 1], 60) == [0, 1000, 1000, 1000]

if __name__ == '__main__':
#	rec = record()
#	print("in: ", rec)
#	print(analysis([0,100,200], rec))
	
	print(reshape(analysis([0,100,200], [0, 101, 300])))
	print(analysis([0,100,200], [0, 101, 300]))
