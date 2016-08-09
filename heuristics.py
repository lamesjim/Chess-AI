from Chessnut import Game

def material(board_state, player_points, weight):
    board_state = board_state.split()[0]
    piece_values = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 15, 'k': 0, 'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 15, 'K': 0}
    white_points = 0
    black_points = 0
    for piece in board_state:
        if piece.isupper():
            white_points += piece_values[piece]
        elif piece.islower():
            black_points += piece_values[piece]
    player_points['w'] += white_points * weight
    player_points['b'] += black_points * weight
    return player_points

def piece_moves(game, player_points, weight):
    piece_values = {'p': 1, 'b': 4, 'n': 4, 'r': 3, 'q': 3, 'k': 0, 'P': 1, 'B': 4, 'N': 4, 'R': 3, 'Q': 3, 'K': 0}
    white_points = 0
    black_points = 0
    for move in game.get_moves():
        current_piece = game.board.get_piece(game.xy2i(move[:2]))
        if current_piece.isupper():
            white_points += piece_values[current_piece]
        elif current_piece.islower():
            black_points += piece_values[current_piece]
    player_points['w'] += white_points * weight
    player_points['b'] += black_points * weight
    return player_points

def in_check(game, player_points, weight):
    current_status = game.status
    # Turn should be 'w' or 'b'
    turn = str(game).split(" ")[1]
    opponent = 'b' if turn == 'w' else 'w'
    # Check or Checkmate situations
    if current_status == 1:
        player_points[opponent] += weight
    elif current_status == 2:
        player_points[opponent] += float("inf")
    return player_points

def center_squares(game, player_points, weight):
    # inner center squares - e4, e5, d4, d5
    white_points = 0
    black_points = 0
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

if __name__ == "__main__":
    import unittest
    class Test_material_heuristic(unittest.TestCase):
        def test_material_heuristic(self):
            player_points_1 = {'w': 0, 'b': 0}
            self.assertEqual(material('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', player_points_1, 1)['w'], 45, "Should return white player's total sum of piece values")
            player_points_2 = {'w': 0, 'b': 0}
            self.assertEqual(material('1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', player_points_2, 1)['b'], 40, "Should return black player's total sum of piece values minus one rook")

        def test_piece_moves_heuristics(self):
            player_points_1 = {'w': 0, 'b': 0}
            new_game = Game()
            self.assertEqual(piece_moves(new_game, player_points_1, 0.50)['w'], 16, "Should return white player's sum of total weighted legal moves")
            player_points_2 = {'w': 0, 'b': 0}
            new_game.apply_move("d2d3")
            new_game.apply_move("e7e6")
            self.assertEqual(piece_moves(new_game, player_points_2, 0.50)['w'], 29, "Should return white player's sum of total weighted legal moves after pawn moves d2d3")

        def test_in_check(self):
            player_points = {'w': 0, 'b': 0}
            # Initialized Board
            situation_a = Game()
            in_check(situation_a, player_points, 1)
            self.assertEqual(player_points['b'], 0, "Should not increment player_points when opponent not in check or checkmate")
            self.assertEqual(player_points['w'], 0, "Should not increment player_points when opponent not in check or checkmate")
            # Check situation
            situation_b = Game("rnbqkbnr/ppp2ppp/8/1B1pp3/3PP3/8/PPP2PPP/RNBQK1NR b KQkq - 1 3")
            in_check(situation_b, player_points, 1)
            self.assertEqual(player_points['b'], 0, "Should not increment player_points when opponent not in check or checkmate")
            self.assertEqual(player_points['w'], 1, "Should increment player_points when opponent is in check")

            # Checkmate situation
            situation_c = Game("r1bqkbnr/p1pppB1p/1pn2p2/6p1/8/1QP1P3/PP1P1PPP/RNB1K1NR b KQkq - 1 5")
            in_check(situation_c, player_points, 1)
            self.assertEqual(player_points['b'], 0, "Should not increment player_points when opponent not in check or checkmate")
            self.assertEqual(player_points['w'], float("inf"), "Should set player_points to infinity when opponent in checkmate")

        def test_center_squares(self):
            player_points = {'w': 0, 'b': 0}
            #Initialized board
            situation_a = Game()
            center_squares(situation_a, player_points, 1)
            self.assertEqual(player_points['b'], 0, "Should not have value since no piece is in any of the center squares")
            self.assertEqual(player_points['w'], 0, "Should not have value since no piece is in any of the center squares")
            situation_b = Game("r1bqkb1r/ppp1pppp/2n2n2/3p4/3PP3/2PQ4/PP3PPP/RNB1KBNR b KQkq e3 0 4")
            center_squares(situation_b, player_points, 1)
            self.assertEqual(player_points['b'], 5, "Should have points for 2 pieces in the outer square and 1 in the inner (5)")
            self.assertEqual(player_points['w'], 8, "Should have points for 2 pieces in the outer square and 2 in the inner (8)")

    unittest.main()
