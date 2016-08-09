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

def piece_moves(player_points, weight, game_state):
    # if game_state == None:
    #     game_state = str(self.game)
    piece_values = {'p': 1, 'b': 4, 'n': 4, 'r': 3, 'q': 3, 'k': 0, 'P': 1, 'B': 4, 'N': 4, 'R': 3, 'Q': 3, 'K': 0}
    white_points = 0
    black_points = 0
    game_clone = Game(game_state)
    for move in game_clone.get_moves():
        current_piece = game_clone.board.get_piece(game_clone.xy2i(move[:2]))
        if current_piece.isupper():
            white_points += piece_values[current_piece]
        elif current_piece.islower():
            black_points += piece_values[current_piece]
    player_points['w'] += white_points * weight
    player_points['b'] += black_points * weight
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
            game_state_1 = str(new_game)
            self.assertEqual(piece_moves(player_points_1, 0.50, game_state_1)['w'], 16, "Should return white player's sum of total weighted legal moves")
            player_points_2 = {'w': 0, 'b': 0}
            new_game.apply_move("d2d3")
            new_game.apply_move("e7e6")
            game_state_2 = str(new_game)
            self.assertEqual(piece_moves(player_points_2, 0.50, game_state_2)['w'], 29, "Should return white player's sum of total weighted legal moves after pawn moves d2d3")
    unittest.main()
