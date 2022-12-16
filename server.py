import flask

import api.api as api

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def f1():
	return flask.render_template('index.html')
@app.route('/check_guess', methods=['POST'])
def f2():
	json = flask.request.get_json()
	try:
		return {
			'error': 'ok',
			'rating': api.games[json['game']].word_to_place(json['word'])
		}
	except KeyError:
		return {'error': 'not_ok'}
@app.route('/hint', methods=['POST'])
def f3():
	json = flask.request.get_json()
	word = api.games[json['game']].place_to_word(json['number'])
	return {'word': '<error>'} if word is None else {'word': word}

app.run(debug=False, host='0.0.0.0', port='8080')

