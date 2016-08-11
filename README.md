# Chess-AI

### Galvanize Immersive Web-Dev Quarter 3 Project

**Team Members:**
*   Ian Jabour
*   James Lim
*   Dai Nguyen

This project focuses on Computer Science concepts such as data structures and algorithms. Chessnut is the chess engine we are using for all the moves and Chess logic. We are utilizing a tree to generate the possible Chess boards 3 levels deep and Breadth First Search, Minimax, and Alpha-Beta Pruning to find the best move based on the following heuristics:

*   Material (total piece count for each player)
*   Number of possible legal moves with emphasis on center squares
*   Check/Checkmate status
*   Pawn structure

Currently trying to implement multiprocessing as our recursive function uses a lot of computing power so calculating heuristics on board states more than 4 levels deep takes a lot of time. With a depth of 3 levels, our AI makes pretty good moves but also makes a lot of ill-advised ones as well. The AI's Chess intelligence is estimated to be at a level 3 out of 9.
