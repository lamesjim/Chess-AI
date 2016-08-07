from test_helpers import heuristic_gen, get_successors
from node import Node

class AI():
    def __init__(self, max_depth=4, branches=2, leaf_nodes=[]):
        self.branches = branches
        self.max_depth = max_depth
        self.leaf_nodes = heuristic_gen(leaf_nodes)

    def get_moves(self):
        return get_successors(self.branches)

    def get_heuristic(self, board_state):
        return next(self.leaf_nodes)

    def minimax(self, node, current_depth=0):
        current_depth += 1
        if current_depth == self.max_depth:
            # get heuristic of each node
            node.value = self.get_heuristic(node.board_state)
            return node.value
        if current_depth % 2 == 0:
            # min player's turn
            return min([self.minimax(child_node, current_depth) for child_node in self.get_moves()])
        else:
            # max player's turn
            return max([self.minimax(child_node, current_depth) for child_node in self.get_moves()])

if __name__ == "__main__":
    import unittest
    class Test_minimax(unittest.TestCase):
        def test_minimax(self):
            data_set_1 = [8, 12, -13, 4, 1, 1, 20, 17, -5,
                          -1, -15, -12, -11, -1, 1, 17, -3, 12,
                          -7, 14, 9, 18, 4, -15, 8, 0, -6]
            first_test_AI = AI(4, 3, data_set_1)
            self.assertEqual(first_test_AI.minimax(Node()), 8, "Should return correct minimax when given b = 3 and d = 3")
            data_set_2 = [-4, -17, 6, 10, -6, -1, 16, 12,
                          -12, 16, -18, -18, -20, -15, -18, -8,
                          8, 0, 11, -14, 11, -20, 8, -2,
                          -17, -18, -11, 10, -8, -14, 7, -17]
            second_test_AI = AI(6, 2, data_set_2)
            self.assertEqual(second_test_AI.minimax(Node()), -8, "Should return correct minimax when given b = 2 and d = 5")
            data_set_3 = [-7, 14, -11, -16, -3, -19, 17, 0, 15,
                          5, -12, 18, -12, 17, 11, 12, 5, -4,
                          13, -12, 9, 0, 12, 12, -10, 1, -19,
                          20, 6, 13, 9, 14, 7, -3, 4, 11,
                          -14, -10, -13, -18, 17, -6, 0, -8, -1,
                          3, 14, 6, -1, -7, 3, 8, 2, 10,
                          6, -19, 15, -4, -10, -1, -19, -2, 6,
                          -4, 14, -3, -9, -20, 11, -18, 15, -1,
                          -9, -10, 15, 0, 8, -4, -12, 4, -17]
            third_test_AI = AI(5, 3, data_set_3)
            self.assertEqual(third_test_AI.minimax(Node()), -4, "Should return correct minimax when given b = 3 and d = 4")
    unittest.main()
