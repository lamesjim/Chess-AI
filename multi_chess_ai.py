# -*- coding: utf-8 -*-
from subprocess import call
from time import sleep
from game import Game
from test_helpers import heuristic_gen, get_successors
from node import Node
import heuristics
import random
import time
from multiprocessing import Pool
import math

cache = {}
found_in_cache = 0

class Test_Engine():
    def __init__(self):
        self.game = Game()
        self.computer = AI(self.game, 4)

    def prompt_user(self):
        self.computer.print_board()
        while self.game.status < 2:
            user_move = raw_input("Make a move: ")
            while user_move not in self.game.get_moves() and user_move != "ff":
                user_move = raw_input("Please enter a valid move: ")
            if user_move == "ff":
                break;
            self.game.apply_move(user_move)
            start_time = time.time()
            self.computer.print_board()
            print("\nCalculating...\n")
            if self.game.status < 2:
                current_state = str(self.game)
                computer_move = self.computer.ab_make_move(current_state)
                PIECE_NAME = {'p': 'Pawn', 'b': 'Bishop', 'n': 'Knight', 'r': 'Rook', 'q': 'Queen', 'k': 'King'}
                print("Computer moved " + PIECE_NAME[self.game.board.get_piece(self.game.xy2i(computer_move[:2]))] + " at " + computer_move[:2] + " to " + computer_move[2:])
                self.game.apply_move(computer_move)
            self.computer.print_board()
            print("Elapsed time in sec: {time}".format(time=time.time() - start_time))
        user_move = raw_input("Game over. Play again? y/n: ")
        if user_move.lower() == "y":
            self.game = Game()
            self.computer.game = self.game
            self.prompt_user()

class AI():
    def __init__(self, game, max_depth=4, node_count=0):
        self.max_depth = max_depth
        self.game = game
        self.node_count = node_count

    def print_board(self, board_state=None):
        global cache
        global found_in_cache
        PIECE_SYMBOLS = {'P': '♟', 'B': '♝', 'N': '♞', 'R': '♜', 'Q': '♛', 'K': '♚', 'p': '♙', 'b': '♗', 'n': '♘', 'r': '♖', 'q': '♕', 'k': '♔'}
        if board_state == None:
            board_state = str(self.game)
        board_state = board_state.split()[0].split("/")
        board_state_str = "\n"
        for i, row in enumerate(board_state):
            board_state_str += str(8-i)
            for char in row:
                if char.isdigit():
                    board_state_str += " ♢" * int(char)
                else:
                    board_state_str += " " + PIECE_SYMBOLS[char]
            board_state_str += "\n"
        board_state_str += "  A B C D E F G H"

        print("Node Count: {}".format(self.node_count))
        print("Cache size: {}".format(len(cache)))
        print("Found in Cache: {}".format(found_in_cache))
        found_in_cache = 0
        self.node_count = 0
        print(board_state_str)

    def get_moves(self, board_state=None):
        if board_state == None:
            board_state = str(self.game)
        possible_moves = []
        for move in Game(board_state).get_moves():
            if (len(move) < 5 or move[4] == "q"):
                clone = Game(board_state)
                clone.apply_move(move)
                node = Node(str(clone))
                node.algebraic_move = move
                possible_moves.append(node)
        return possible_moves

    def get_heuristic(self, board_state=None):
        global cache
        global found_in_cache

        cache_parse = board_state.split(" ")[0] + " " + board_state.split(" ")[1]
        if board_state == None:
            board_state = str(self.game)
        if cache_parse in cache:
            found_in_cache += 1
            return cache[cache_parse]
        clone = Game(board_state)
        total_points = 0
        # total piece count
        total_points += heuristics.material(board_state, 0.6)
        total_points += heuristics.piece_moves(clone, 0.15)
        total_points += heuristics.in_check(clone, 0.1)
        # total_points += heuristics.center_squares(clone, 0.2)
        total_points += heuristics.pawn_structure(board_state, 0.15)
        cache[cache_parse] = total_points
        return total_points

    # def minimax(self, node, current_depth=0):
    #     current_depth += 1
    #     if current_depth == self.max_depth:
    #         # get heuristic of each node
    #         node.value = self.get_heuristic(node.board_state)
    #         return node.value
    #     if current_depth % 2 == 0:
    #         # min player's turn
    #         self.is_turn = False
    #         return min([self.minimax(child_node, current_depth) for child_node in self.get_moves(node.board_state, self.is_turn)])
    #     else:
    #         # max player's turn
    #         self.is_turn = True
    #         return max([self.minimax(child_node, current_depth) for child_node in self.get_moves(node.board_state, self.is_turn)])

    # def make_move(self, node):
    #     self.is_turn = True
    #     possible_moves = self.get_moves(node.board_state, self.is_turn)
    #     for move in possible_moves:
    #         move.value = self.minimax(move, 1)
    #     best_move = possible_moves[0]
    #     for move in possible_moves:
    #         if move.value > best_move.value:
    #             best_move = move
    #     # best_move at this point stores the move with the highest heuristic
    #     return best_move

    def ab_make_move(self, board_state):
        possible_moves = self.get_moves(board_state)
        # print possible_moves
        best_move = None

        p = Pool(4)
        result = p.map(map_partial, possible_moves, )
        for node in result:
            if best_move == None:
                best_move = node
            if best_move.value < node.value:
                best_move = node
        p.close()
        p.join()
        return best_move.algebraic_move

    def ab_minimax(self, node, alpha=float("-inf"), beta=float("inf"), current_depth=1):
        current_depth += 1
        if current_depth == self.max_depth:
            board_value = self.get_heuristic(node.board_state)
            if current_depth % 2 == 0:
                # pick largest number, where root is black and even depth
                if (alpha < board_value):
                    alpha = board_value
                self.node_count += 1
                return alpha
            else:
                # pick smallest number, where root is black and odd depth
                if (beta > board_value):
                    beta = board_value
                self.node_count += 1
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
    #     def test_make_move(self):
    #         new_game = Game()
    #         first_test_AI = AI(new_game, 2, 0)
    #         first_test_AI.print_board(str(new_game))
    #         new_game.apply_move("a2a3")
    #         first_test_AI.print_board(str(new_game))
    #         new_game.apply_move(first_test_AI.ab_make_move(str(new_game)))
    #         first_test_AI.print_board(str(new_game))
    #
    # unittest.main()

new_test = Test_Engine()

def map_partial(move_node, AI=new_test.computer):
    move_node.value = AI.ab_minimax(move_node)
    return move_node

new_test.prompt_user()
