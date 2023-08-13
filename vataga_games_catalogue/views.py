import flask
from flask import request

from vataga_games_catalogue import app, logger
from vataga_games_catalogue.models import Game


@app.route("/")
def main():
    """Страница удаления зависшего чека."""

    collection = {"hello": 1, "world": 2, "!": [1, 2, 3, 4, 5]}

    return flask.jsonify(collection)


@app.route('/get_games')
def get_games():
    """Эндпоинт, который возвращает весь список игр"""

    games = Game.get_games()

    return flask.jsonify(games)


@app.route("/add_games", methods=['POST'])
def add_games():
    """Эндпоинт для добавления игр, получает json тело"""

    if games := request.json:
        games_added_count = Game.add_games(games)
        return f'{games_added_count} games were added', 200

    return "No body provided", 400

