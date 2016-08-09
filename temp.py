from Chessnut import Game

game = Game()

def center_squares():
    # inner center squares - e4, e5, d4, d5
    white_points = 0
    black_points = 0
    player_points = {'w': 0, 'b': 0}
    inner = [game.board.get_piece(game.xy2i("e4")),
            game.board.get_piece(game.xy2i("e5")),
            game.board.get_piece(game.xy2i("d4")),
            game.board.get_piece(game.xy2i("d5"))]
    for square in inner:
        if square.isupper():
            white_points += 3
        elif square.islower():
            black_points += 3
    # outer center squares - c3, d3, e3, f3, c6, d6, e6, f6, f4, f5, c4, c5
    outer = [game.board.get_piece(game.xy2i("c3")),
            game.board.get_piece(game.xy2i("d3")),
            game.board.get_piece(game.xy2i("e3")),
            game.board.get_piece(game.xy2i("f3")),
            game.board.get_piece(game.xy2i("c6")),
            game.board.get_piece(game.xy2i("d6")),
            game.board.get_piece(game.xy2i("e6")),
            game.board.get_piece(game.xy2i("f6")),
            game.board.get_piece(game.xy2i("f4")),
            game.board.get_piece(game.xy2i("f5")),
            game.board.get_piece(game.xy2i("c4")),
            game.board.get_piece(game.xy2i("c5"))]
    for square in outer:
        if square.isupper():
            white_points += 1
        elif square.islower():
            black_points += 1
    player_points['w'] += white_points
    player_points['b'] += black_points
    return player_points

print(center_squares())
