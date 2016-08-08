from test_helpers import heuristic_gen, get_successors
from node import Node

class AI():
    def __init__(self, max_depth=4, branches=2, leaf_nodes=[]):
        self.branches = branches
        self.max_depth = max_depth
        self.leaf_nodes = heuristic_gen(leaf_nodes)

    def get_moves(self, board_state, is_turn):
        self.is_turn = is_turn
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
            self.is_turn = False
            return min([self.minimax(child_node, current_depth) for child_node in self.get_moves(node.board_state, self.is_turn)])
        else:
            # max player's turn
            self.is_turn = True
            return max([self.minimax(child_node, current_depth) for child_node in self.get_moves(node.board_state, self.is_turn)])

    def make_move(self, node):
        self.is_turn = True
        possible_moves = self.get_moves(node.board_state, self.is_turn)
        for move in possible_moves:
            move.value = self.minimax(move, 1)
        best_move = possible_moves[0]
        for move in possible_moves:
            if move.value > best_move.value:
                best_move = move
        # best_move at this point stores the move with the highest heuristic
        return best_move

    def ab_make_move(self, node):
        self.is_turn = True
        possible_moves = self.get_moves(node.board_state, self.is_turn)
        alpha = float("-inf")
        beta = float("inf")
        best_move = possible_moves[0]
        for move in possible_moves:
            board_value = self.ab_minimax(move, alpha, beta, 1)
            if alpha < board_value:
                alpha = board_value
                best_move = move
                best_move.value = alpha
        # best_move at this point stores the move with the highest heuristic
        return best_move

    def ab_minimax(self, node, alpha, beta, current_depth=0):
        current_depth += 1
        if current_depth == self.max_depth:
            board_value = self.get_heuristic(node.board_state)
            if current_depth % 2 == 0:
                # pick largest number
                if (alpha < board_value):
                    alpha = board_value
                return alpha
            else:
                # pick smallest number
                if (beta > board_value):
                    beta = board_value
                return beta
        if current_depth % 2 == 0:
            # min player's turn
            self.is_turn = False
            for child_node in self.get_moves(node.board_state, self.is_turn):
                if alpha < beta:
                    board_value = self.ab_minimax(child_node,alpha, beta, current_depth)
                    if beta > board_value:
                        beta = board_value
            return beta
        else:
            # max player's turn
            self.is_turn = True
            for child_node in self.get_moves(node.board_state, self.is_turn):
                if alpha < beta:
                    board_value = self.ab_minimax(child_node,alpha, beta, current_depth)
                    if alpha < board_value:
                        alpha = board_value
            return alpha

if __name__ == "__main__":
    import unittest
    class Test_AI(unittest.TestCase):
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

        def test_make_move(self):
            data_set_1 = [-4, -17, 6, 10, -6, -1, 16, 12,
                          -12, 16, -18, -18, -20, -15, -18, -8,
                          8, 0, 11, -14, 11, -20, 8, -2,
                          -17, -18, -11, 10, -8, -14, 7, -17]
            first_test_AI = AI(6, 2, data_set_1)
            self.assertEqual(first_test_AI.make_move(Node()).value, -8, "Should return best move given node w/ current board state")
            data_set_2 = [-7, 14, -11, -16, -3, -19, 17, 0, 15,
                          5, -12, 18, -12, 17, 11, 12, 5, -4,
                          13, -12, 9, 0, 12, 12, -10, 1, -19,
                          20, 6, 13, 9, 14, 7, -3, 4, 11,
                          -14, -10, -13, -18, 17, -6, 0, -8, -1,
                          3, 14, 6, -1, -7, 3, 8, 2, 10,
                          6, -19, 15, -4, -10, -1, -19, -2, 6,
                          -4, 14, -3, -9, -20, 11, -18, 15, -1,
                          -9, -10, 15, 0, 8, -4, -12, 4, -17]
            second_test_AI = AI(5, 3, data_set_2)
            self.assertEqual(second_test_AI.make_move(Node()).value, -4, "Should return best move when many moves are possible")

        def test_ab(self):
            data_set_1_prune = [8, 12, -13, 4, 1, 1, 20,
                          -1, -15, -12,
                          -7, 14, 9, 18, 8, 0, -6]
            data_set_1_unprune = [-4, -17, 6, 10, -6, -1, 16, 12,
                          -12, 16, -18, -18, -20, -15, -18, -8,
                          8, 0, 11, -14, 11, -20, 8, -2,
                          -17, -18, -11, 10, -8, -14, 7, -17]
            first_prune_test_ab_AI = AI(4, 3, data_set_1_prune)
            first_unprune_test_ab_AI = AI(4, 3, data_set_1_unprune)
            self.assertEqual(first_prune_test_ab_AI.ab_make_move(Node()).value, 8, "Should return correct number with pruning when given b = 3 and d = 3")
            self.assertEqual(first_unprune_test_ab_AI.ab_make_move(Node()).value == 8, False, "Should fail for unpruned dataset")

        # def test_ab_make_move(self):


    unittest.main()
