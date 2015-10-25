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
def post_attempt():
	pattern_name = request.values['pattern_name']
	bpm = int(request.values['bpm'])
	in_tss = [int(x) for x in request.values['tss'].split(',')]
	player = request.values['player']

	pattern = db.get_pattern(pattern_name)
	ref_tss = pattern_tss(pattern, bpm)
	res = result(ref_tss, in_tss)
	db.write(res, pattern_name, player, bpm)
	return str(res)+'<br><a href=http://127.0.0.1:5000/static/client.html>back</a>'

if __name__ == '__main__':
	app.run(debug=True)
