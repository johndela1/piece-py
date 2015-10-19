from flask import Flask, jsonify, request

import db
from analyze import analysis, pattern_deltas, deltas_tss, reshape

app = Flask(__name__)

@app.route('/pattern')
@app.route('/pattern/<name>/<int:bpm>')
def get_pattern(name=None, bpm=None):
	if not name:
		return jsonify({"patterns": db.get_patterns()})
	pattern = db.get_pattern(name)
	ret = {"deltas": pattern_deltas(pattern, bpm)}
	return jsonify(ret)
	

@app.route('/attempt', methods=['POST'])
def set_attempt():
	pattern_name = request.json['pattern_name']
	in_tss = request.json['tss']
	bpm = request.json['bpm']
	player = request.json['player']

	pattern = db.get_pattern(pattern_name)
	ref_tss = deltas_tss(pattern_deltas(pattern, bpm))
	result = reshape(analysis(ref_tss, in_tss))
	db.write(result, pattern_name, player, bpm)
	return jsonify(result)

if __name__ == '__main__':
	app.run(debug=True)
