# -*- coding: utf-8 -*-

from Chessnut import Game
from test_helpers import heuristic_gen, get_successors
from node import Node
import heuristics

class Test_Engine():
    def __init__(self):
        self.game = Game()
        self.computer = AI(self.game, 3)

    def prompt_user(self):
        self.computer.print_board()
        while self.game.status < 2:
            user_move = raw_input("Make a move: ")
            while user_move not in self.game.get_moves():
                user_move = raw_input("Please enter a valid move: ")
            self.game.apply_move(user_move)
            if self.game.status < 2:
                current_state = str(self.game)
                computer_move = self.computer.ab_make_move(current_state)
                self.game.apply_move(computer_move)
            self.computer.print_board()

class AI():
    def __init__(self, game, max_depth=4, leaf_nodes=[]):
        self.max_depth = max_depth
        self.leaf_nodes = heuristic_gen(leaf_nodes)
        self.game = game

    def print_board(self, board_state=None):
        PIECE_SYMBOLS = {'P': '♟', 'B': '♝', 'N': '♞', 'R': '♜', 'Q': '♛', 'K': '♚', 'p': '♙', 'b': '♗', 'n': '♘', 'r': '♖', 'q': '♕', 'k': '♔'}
        if board_state == None:
            board_state = str(self.game)
        board_state = board_state.split()[0].split("/")
        board_state_str = ""
        for i, row in enumerate(board_state):
            board_state_str += str(8-i)
            for char in row:
                if char.isdigit():
                    board_state_str += " –" * int(char)
                else:
                    board_state_str += " " + PIECE_SYMBOLS[char]
            board_state_str += "\n"
        board_state_str += "  A B C D E F G H"

        print(board_state_str)

    def get_moves(self, game_state=None):
        if game_state == None:
            game_state = str(self.game)
        possible_moves = []
        for move in Game(game_state).get_moves():
            clone = Game(game_state)
            clone.apply_move(move)
            node = Node(str(clone))
            node.algebraic_move = move
            possible_moves.append(node)
        return possible_moves

    def get_heuristic(self, board_state):
        player_points = {'w': 0, 'b': 0}
        # total piece count
        heuristics.material(board_state, player_points)

        return player_points

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

    def ab_make_move(self, board_state):
        possible_moves = self.get_moves(board_state)
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
        return best_move.algebraic_move

    def ab_minimax(self, node, alpha, beta, current_depth=0):
        current_depth += 1
        if current_depth == self.max_depth:
            total_value = self.get_heuristic(node.board_state)
            if current_depth % 2 == 0:
                # pick largest number, where root is black and even depth
                board_value = total_value['w'] - total_value['b']
                if (alpha < board_value):
                    alpha = board_value
                return alpha
            else:
                # pick smallest number, where root is black and odd depth
                board_value = total_value['b'] - total_value['w']
                if (beta > board_value):
                    beta = board_value
                return beta
        if current_depth % 2 == 0:
            # min player's turn
            for child_node in self.get_moves(node.board_state):
                if alpha < beta:
                    board_value = self.ab_minimax(child_node,alpha, beta, current_depth)
                    if beta > board_value:
                        beta = board_value
            return beta
        else:
            # max player's turn
            for child_node in self.get_moves(node.board_state):
                if alpha < beta:
                    board_value = self.ab_minimax(child_node,alpha, beta, current_depth)
                    if alpha < board_value:
                        alpha = board_value
            return alpha

# if __name__ == "__main__":
#     import unittest
#     class Test_AI(unittest.TestCase):
#         # def test_minimax(self):
#         #     data_set_1 = [8, 12, -13, 4, 1, 1, 20, 17, -5,
#         #                   -1, -15, -12, -11, -1, 1, 17, -3, 12,
#         #                   -7, 14, 9, 18, 4, -15, 8, 0, -6]
#         #     first_test_AI = AI(4, 3, data_set_1)
#         #     self.assertEqual(first_test_AI.minimax(Node()), 8, "Should return correct minimax when given b = 3 and d = 3")
#         #     data_set_2 = [-4, -17, 6, 10, -6, -1, 16, 12,
#         #                   -12, 16, -18, -18, -20, -15, -18, -8,
#         #                   8, 0, 11, -14, 11, -20, 8, -2,
#         #                   -17, -18, -11, 10, -8, -14, 7, -17]
#         #     second_test_AI = AI(6, 2, data_set_2)
#         #     self.assertEqual(second_test_AI.minimax(Node()), -8, "Should return correct minimax when given b = 2 and d = 5")
#         #     data_set_3 = [-7, 14, -11, -16, -3, -19, 17, 0, 15,
#         #                   5, -12, 18, -12, 17, 11, 12, 5, -4,
#         #                   13, -12, 9, 0, 12, 12, -10, 1, -19,
#         #                   20, 6, 13, 9, 14, 7, -3, 4, 11,
#         #                   -14, -10, -13, -18, 17, -6, 0, -8, -1,
#         #                   3, 14, 6, -1, -7, 3, 8, 2, 10,
#         #                   6, -19, 15, -4, -10, -1, -19, -2, 6,
#         #                   -4, 14, -3, -9, -20, 11, -18, 15, -1,
#         #                   -9, -10, 15, 0, 8, -4, -12, 4, -17]
#         #     third_test_AI = AI(5, 3, data_set_3)
#         #     self.assertEqual(third_test_AI.minimax(Node()), -4, "Should return correct minimax when given b = 3 and d = 4")
#         #
#         # def test_make_move(self):
#         #     data_set_1 = [-4, -17, 6, 10, -6, -1, 16, 12,
#         #                   -12, 16, -18, -18, -20, -15, -18, -8,
#         #                   8, 0, 11, -14, 11, -20, 8, -2,
#         #                   -17, -18, -11, 10, -8, -14, 7, -17]
#         #     first_test_AI = AI(6, 2, data_set_1)
#         #     self.assertEqual(first_test_AI.make_move(Node()).value, -8, "Should return best move given node w/ current board state")
#         #     data_set_2 = [-7, 14, -11, -16, -3, -19, 17, 0, 15,
#         #                   5, -12, 18, -12, 17, 11, 12, 5, -4,
#         #                   13, -12, 9, 0, 12, 12, -10, 1, -19,
#         #                   20, 6, 13, 9, 14, 7, -3, 4, 11,
#         #                   -14, -10, -13, -18, 17, -6, 0, -8, -1,
#         #                   3, 14, 6, -1, -7, 3, 8, 2, 10,
#         #                   6, -19, 15, -4, -10, -1, -19, -2, 6,
#         #                   -4, 14, -3, -9, -20, 11, -18, 15, -1,
#         #                   -9, -10, 15, 0, 8, -4, -12, 4, -17]
#         #     second_test_AI = AI(5, 3, data_set_2)
#         #     self.assertEqual(second_test_AI.make_move(Node()).value, -4, "Should return best move when many moves are possible")
#         #
#         # def test_ab(self):
#         #     data_set_1_prune = [8, 12, -13, 4, 1, 1, 20,
#         #                   -1, -15, -12,
#         #                   -7, 14, 9, 18, 8, 0, -6]
#         #     data_set_1_unprune = [-4, -17, 6, 10, -6, -1, 16, 12,
#         #                   -12, 16, -18, -18, -20, -15, -18, -8,
#         #                   8, 0, 11, -14, 11, -20, 8, -2,
#         #                   -17, -18, -11, 10, -8, -14, 7, -17]
#         #     first_prune_test_ab_AI = AI(4, 3, data_set_1_prune)
#         #     first_unprune_test_ab_AI = AI(4, 3, data_set_1_unprune)
#         #     self.assertEqual(first_prune_test_ab_AI.ab_make_move(Node()).value, 8, "Should return correct number with pruning when given b = 3 and d = 3")
#         #     self.assertEqual(first_unprune_test_ab_AI.ab_make_move(Node()).value == 8, False, "Should fail for unpruned dataset")
#
#         # def test_get_moves(self):
#         #     new_game = Game()
#         #     first_test_AI = AI(new_game, 4, 0)
#         #     # White move
#         #     self.assertEqual(len(first_test_AI.get_moves()), 20, "Should get all initial moves for white")
#         #     current_turn = str(new_game).split(" ")[1]
#         #     self.assertEqual(current_turn, "w", "Should start as white's turn")
#         #     new_game.apply_move("a2a4")
#         #     # Black move
#         #     current_turn = str(new_game).split(" ")[1]
#         #     self.assertEqual(current_turn, "b", "Should switch to black's turn")
#         #     self.assertEqual(len(first_test_AI.get_moves()), 20, "Should get all initial moves for black")
#         #     new_game.apply_move("b8a6")
#         #     # White move
#         #     current_turn = str(new_game).split(" ")[1]
#         #     self.assertEqual(current_turn, "w", "Should start as white's turn")
#         #     self.assertEqual(len(first_test_AI.get_moves()), 21, "Should get all moves for white 3rd turn")
#         def test_make_move(self):
#             new_game = Game()
#             first_test_AI = AI(new_game, 2, 0)
#             first_test_AI.print_board(str(new_game))
#             new_game.apply_move("a2a3")
#             first_test_AI.print_board(str(new_game))
#             new_game.apply_move(first_test_AI.ab_make_move(str(new_game)))
#             first_test_AI.print_board(str(new_game))
#
#     unittest.main()

new_test = Test_Engine()
new_test.prompt_user()
