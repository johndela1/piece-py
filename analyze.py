from cmath import isclose
from collections import namedtuple
from itertools import accumulate

SECS_PER_MINUTE = 60
TOLERANCE = 80


def deltas_tss(deltas):
        yield from accumulate(deltas)
        
def bpm_bps(bpm):
	return bpm / SECS_PER_MINUTE

def secs_millis(t):
	return t * 1000

def pattern_deltas(pattern, bpm):
	# used when sending pattern to client
	# pattern -> bpm => deltas
	(beats, beat_unit), notes = pattern
	note_duration = int(secs_millis(beat_unit / beats) / bpm_bps(bpm))
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

assert (list(deltas_tss([0, 500, 500])) == [0, 500, 1000])
assert pattern_deltas(((4, 4), [1, 1, 1, 1]), 60) == [0, 1000, 1000, 1000]
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

def p_t(piece):
    (beats, beat_div), bpm, notes = piece
    for i, note in enumerate(notes):
        subdivs = len(note)
        ts = i * secs_millis((beats / bpm_bps(bpm)) / beat_div)
        for sub in range(subdivs):
            if note[sub]: yield ts
            ts += ts / subdivs

def p_d(piece):
    (beats, beat_div), bpm, notes = piece
    acc = 0
    for note_group in notes:
        subdivs = len(note_group)
        note_duration = secs_millis(SECS_PER_MINUTE / bpm) / subdivs
        for sub in range(subdivs):
            if note_group[sub]:
                yield acc
                acc = note_duration
                continue
            acc += note_duration

if __name__ == '__main__':
	#print(reshape(analysis([0,100,200], [0, 101, 300])))
    tss_ref=[0,500,1000]
    tss_in=[10,450,1300]
 
#    import pdb;pdb.set_trace()
    print('pass')
    # beats/beat_unit
    Pattern = namedtuple('Pattern', ('sig', 'bpm', 'notes'))
    pattern = Pattern((4,4), 60, [[1], [1,1], [1], [1]])
    print ("hey 60:",pattern,"\n", list(p_d(pattern)))

    pattern = Pattern((4,4), 120, [[1], [1,1], [1], [1]])
    print ("hey 120:",pattern,"\n", list(p_d(pattern)))
#[Pattern((4,4), bpm,[[1]*subdiv]*4) for subdiv in [1,2]for bpm in range(60,121,10)]
