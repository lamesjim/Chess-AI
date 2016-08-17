import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from chess_ai import Game_Engine

app = Flask(__name__, static_url_path='/static')

game_engine = Game_Engine()
game = game_engine.game
ai = game_engine.computer

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/board', methods=['GET'])
def get_board():
    fen = str(game)
    return flask.jsonify(fen)

@app.route('/board', methods=['POST'])
def send_board():
    user_algebraic_move = request.get_json()
    game.apply_move(user_algebraic_move)
    if game.status < 2:
        ai_algebraic_move = ai.make_move()
        game.apply_move(ai_algebraic_move)
    fen = str(game)
    return flask.jsonify(fen)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port)
