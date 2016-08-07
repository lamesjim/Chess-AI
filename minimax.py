from test_helpers import heuristic_gen, get_successors

def minimax(board_state, heuristic, next_moves, current_depth=0, max_depth=4):
    current_depth += 1
    if current_depth == max_depth:
        # get heuristic of each node
        return next(heuristic)
    if current_depth % 2 == 0:
        # min player's turn
        return min([minimax(node, heuristic, current_depth, max_depth) for node in next_moves()])
    else:
        # max player's turn
        return max([minimax(node, heuristic, current_depth, max_depth) for node in next_moves()])

if __name__ == "__main__":
    import unittest
    class Test_minimax(unittest.TestCase):
        def test_minimax(self):
            heuristics = heuristic_gen([8, 12, -13, 4, 1, 1, 20, 17, -5,
                                        -1, -15, -12, -11, -1, 1, 17, -3, 12,
                                        -7, 14, 9, 18, 4, -15, 8, 0, -6])
            heuristics2 = heuristic_gen([-4, -17, 6, 10, -6, -1, 16, 12, -12,
                                        16, -18, -18, -20, -15, -18, -8, 8, 0,
                                        11, -14, 11, -20, 8, -2, -17, -18,
                                        -11, 10, -8, -14, 7, -17])
            self.assertEqual(minimax(None, heuristics), 8, "Should return 8")
            self.assertEqual(minimax(None, heuristics2, 0, 6), -8, "Should return -8")
    unittest.main()
