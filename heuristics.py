def material(board_state, player_points):
    board_state = board_state.split()[0]
    piece_values = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 0, 'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9, 'K': 0}
    for piece in board_state:
        if piece.isupper():
            player_points['w'] += piece_values[piece]
        elif piece.islower():
            player_points['b'] += piece_values[piece]
    return player_points

if __name__ == "__main__":
    import unittest
    class Test_material_heuristic(unittest.TestCase):
        def test_material_heuristic(self):
            player_points_1 = {'w': 0, 'b': 0}
            self.assertEqual(material('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', player_points_1)['w'], 39, "Should return white player's total sum of piece values")
            player_points_2 = {'w': 0, 'b': 0}
            self.assertEqual(material('1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', player_points_2)['b'], 34, "Should return black player's total sum of piece values minus one rook")
    unittest.main()
