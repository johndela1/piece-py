from flask import Flask, jsonify, request

import db
from analyze import analysis, pattern_deltas, deltas_tss, reshape

app = Flask(__name__)

@app.route('/pattern')
@app.route('/pattern/<name>/<int:bpm>')
def get_pattern(name=None, bpm=None):
	if not name:
		return jsonify(db.get_patterns())
	pattern = db.get_pattern(name)
	notes = pattern['notes']
	beat_div = pattern['beat_div']
	ret = {"deltas": pattern_deltas(beat_div, notes, bpm)}
	return jsonify(ret)
	

@app.route('/attempt', methods=['POST'])
def set_pattern():
	name = request.json['name']
	in_tss = request.json['tss']
	bpm = request.json['bpm']
	ref = db.get_pattern(name)  # should be namedtuple or tuple
	beat_div = ref['beat_div']
	notes = ref['notes']
	ref_tss = deltas_tss(pattern_deltas(beat_div, notes, bpm))
	result = {'result': reshape(analysis(ref_tss, in_tss))}
	return jsonify(result)

if __name__ == '__main__':
	app.run(debug=True)
