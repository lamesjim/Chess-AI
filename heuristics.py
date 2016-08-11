from game import Game

def material(board_state, weight):
    black_points = 0
    board_state = board_state.split()[0]
    piece_values = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 0}
    for piece in board_state:
        if piece.islower():
            black_points += piece_values[piece]
        elif piece.isupper():
            black_points -= piece_values[piece.lower()]
    return black_points * weight

def piece_moves(game, weight):
    black_points = 0
    turn = str(game).split()[1]
    square_values = {"e4": 1, "e5": 1, "d4": 1, "d5": 1, "c6": 0.5, "d6": 0.5, "e6": 0.5, "f6": 0.5,
                    "c3": 0.5, "d3": 0.5, "e3": 0.5, "f3": 0.5, "c4": 0.5, "c5": 0.5, "f4": 0.5, "f5": 0.5}
    possible_moves = game.get_moves()
    for move in possible_moves:
        if turn == "b":
            if move[2:4] in square_values:
                black_points += square_values[move[2:4]]
        else:
            if move[2:4] in square_values:
                black_points -= square_values[move[2:4]]
    # piece_values = {'p': 1, 'b': 4, 'n': 4, 'r': 3, 'q': 3, 'k': 0}
    # for move in game.get_moves():
    #     current_piece = game.board.get_piece(game.xy2i(move[:2]))
    #     if current_piece.islower():
    #         black_points += piece_values[current_piece]
    return black_points

def pawn_structure(board_state, weight):
    black_points = 0
    board_state, current_player = [segment for segment in board_state.split()[:2]]
    board_state = board_state.split("/")

    # convert fen into matrix:
    board_state_arr = []
    for row in board_state:
    	row_arr = []
    	for char in row:
    		if char.isdigit():
    			for i in range(int(char)):
    				row_arr.append(" ")
    		else:
    			row_arr.append(char)
    	board_state_arr.append(row_arr)

    # determine pawn to search for based on whose turn it is
    for i, row in enumerate(board_state_arr):
        for j in range(len(row)):
            if board_state_arr[i][j] == "p":
                tl = i-1, j-1
                tr = i-1, j+1
                if tl[0] >= 0 and tl[0] <= 7 and tl[1] >= 0 and tl[1] <= 7:
                    if board_state_arr[tl[0]][tl[1]] == "p":
                        black_points += 1
                if tr[0] >= 0 and tr[0] <= 7 and tr[1] >= 0 and tr[1] <= 7:
                    if board_state_arr[tr[0]][tr[1]] == "p":
                        black_points += 1
    return black_points * weight

def in_check(game, weight):
    black_points = 0
    current_status = game.status
    # Turn should be 'w' or 'b'
    turn = str(game).split(" ")[1]
    # Check or Checkmate situations
    if turn == "w":
        if current_status == 1:
            black_points += 1 * weight
        elif current_status == 2:
            black_points += float("inf")
    else:
        if current_status == 1:
            black_points -= 1 * weight
        elif current_status == 2:
            black_points += float("-inf")
    return black_points

# def center_squares(game, weight):
#     black_points = 0
#     # inner center squares - e4, e5, d4, d5
#     inner = [game.board.get_piece(game.xy2i("e4")),
#             game.board.get_piece(game.xy2i("e5")),
#             game.board.get_piece(game.xy2i("d4")),
#             game.board.get_piece(game.xy2i("d5"))]
#     for square in inner:
#         if square.islower():
#             black_points += 3
#     # outer center squares - c3, d3, e3, f3, c6, d6, e6, f6, f4, f5, c4, c5
#     outer = [game.board.get_piece(game.xy2i("c3")),
#             game.board.get_piece(game.xy2i("d3")),
#             game.board.get_piece(game.xy2i("e3")),
#             game.board.get_piece(game.xy2i("f3")),
#             game.board.get_piece(game.xy2i("c6")),
#             game.board.get_piece(game.xy2i("d6")),
#             game.board.get_piece(game.xy2i("e6")),
#             game.board.get_piece(game.xy2i("f6")),
#             game.board.get_piece(game.xy2i("f4")),
#             game.board.get_piece(game.xy2i("f5")),
#             game.board.get_piece(game.xy2i("c4")),
#             game.board.get_piece(game.xy2i("c5"))]
#     for square in outer:
#         if square.islower():
#             black_points += 1
#     return black_points * weight

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

        def test_pawn_structure_heuristic(self):
            player_points_1 = {'w': 0, 'b': 0}
            situation_1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
            self.assertEqual(pawn_structure(situation_1, player_points_1, 1)['w'], 0, "Should return value of white's pawn structure")
            player_points_2 = {'w': 0, 'b': 0}
            situation_2 = "rnbqkbnr/8/p1p1p1p1/1p1p1p1p/1P1P1P1P/P1P1P1P1/8/RNBQKBNR w KQkq - 0 9"
            self.assertEqual(pawn_structure(situation_2, player_points_2, 1)['w'], 7, "Should return value of white's pawn structure")
            player_points_3 = {'w': 0, 'b': 0}
            situation_3 = "rnbqkbnr/pppp4/4pp2/P3P1pp/1P1P4/2P5/5PPP/RNBQKBNR b KQkq - 0 7"
            pawn_structure(situation_3, player_points_3, 1)
            self.assertEqual(player_points_3['w'], 4, "Should return value of white's pawn structure")
            self.assertEqual(player_points_3['b'], 2, "Should return value of black's pawn structure")
    unittest.main()
