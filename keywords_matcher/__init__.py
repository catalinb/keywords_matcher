from keywords_matcher.keywords_matcher import create_app
from flask import jsonify, request, current_app, abort

# Create app and load phrases into memory
app = create_app()
if 'PHRASES_PATH' in app.config:
    app.load_phrases(app.config['PHRASES_PATH'])


@app.route('/parse_slow', methods=['GET'])
def parse_slow_text():
    """ Reference lookup endpoint in n^2 steps """
    text = request.args.get('text')
    if text is None:
        return abort(400)

    return jsonify({
        'phrases': [phrase for phrase in current_app.phrases if phrase in text]
    });


@app.route('/parse', methods=['GET'])
def parse_text():
    """ Fast lookup endpoint using ahocorasick """

    text = request.args.get('text')
    if text is None:
        return abort(400)

    return jsonify({
        'phrases': [phrase for id, phrase in current_app.automaton.iter(text)]
    })


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"message": "Bad request!"}), 400
