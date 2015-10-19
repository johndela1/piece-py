from flask import Flask, jsonify, request

import db
from analyze import analysis, pattern_deltas, reshape, pattern_tss, result

app = Flask(__name__)

@app.route('/pattern')
@app.route('/pattern/<pattern_name>/<int:bpm>')
def get_deltas(pattern_name=None, bpm=None):
	if not pattern_name:
		return jsonify({"patterns": db.get_patterns()})
	pattern = db.get_pattern(pattern_name)
	ret = {"deltas": pattern_deltas(pattern, bpm)}
	return jsonify(ret)
	

@app.route('/attempt', methods=['POST'])
def set_attempt():
	pattern_name = request.json['pattern_name']
	bpm = request.json['bpm']
	in_tss = request.json['tss']
	player = request.json['player']

	pattern = db.get_pattern(pattern_name)
	ref_tss = pattern_tss(pattern, bpm)
	res = result(ref_tss, in_tss)
	db.write(res, pattern_name, player, bpm)
	return jsonify(res)

if __name__ == '__main__':
	app.run(debug=True)
