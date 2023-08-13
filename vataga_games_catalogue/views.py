import flask

from vataga_games_catalogue import app, logger


@app.route("/")
def main():
    """Страница удаления зависшего чека."""

    collection = {"hello": 1, "world": 2, "!": [1,2,3,4,5]}

    return flask.jsonify(collection)
