import logging
logging.basicConfig(level=logging.INFO)

_db = {
    'easy-4': (4, (1,1,1,1)),
	'easy-8': (8, (1,1,1,1,1,1,1,1)),
	'12123': (12, (1,0,0,1,0,0,1,0,1,0,1,0))
}


def get_pattern(name):
	return _db[name]
	#return {'name': row[0], 'contents': ('beat_div': row[1], 'notes': row[2])}

def get_patterns():
    return ['stub mode']

def write(result, pattern_name, player_name, bpm):
    logging.info("insert into attempt (pattern_name, player_name, bpm, ts) " +
          "values ('{}','{}',{}, now()) returning id".format(
                pattern_name, player_name, bpm))

    attempt_id='stub_id'
    for ts, diff in result['delta']:
        logging.info("insert into delta (attempt_id, ts, diff) values ({}, {}, {})".format(
            attempt_id, ts, diff))
    for ts in result['miss']:
        logging.info("insert into miss (attempt_id, ts) values ({}, {})".format(
            attempt_id, ts))
    for ts in result['extra']:
        logging.info("insert into extra (attempt_id, ts) values ({}, {})".format(
            attempt_id, ts))

