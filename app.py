import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from chess_ai import Game_Engine

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/board', methods=['POST'])
def send_board():
    game_engine = Game_Engine(request.form['fen'])
    game = game_engine.game
    ai = game_engine.computer
    if game.status < 2:
        ai_algebraic_move = ai.ab_make_move(str(game))
        game.apply_move(ai_algebraic_move)
        return jsonify(move = ai_algebraic_move, fen = str(game))
    return "Game over"


if __name__ == "__main__":
    port = int(os.environ.get('PORT')) or 5000
    app.run(port)
