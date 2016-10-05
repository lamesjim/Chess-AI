# Chess AI

This project focuses on computer science concepts such as data structures and algorithms. Chessnut is the chess engine we are using for all the moves and chess logic. We are utilizing a tree to generate the possible chessboards 3 levels deep and depth first search, minimax, and alpha-beta pruning to find the best move based on the following heuristics:

* material (total piece count for each player)
* number of possible legal moves with emphasis on center squares
* check/checkmate status
* pawn structure

Currently trying to implement multiprocessing as our recursive function uses a lot of computing power so calculating heuristics on board states more than 4 levels deep takes a lot of time. With a depth of 3 leves, our AI makes pretty good moves but also makes a lot of ill-advised ones as well. The AI's chess intelligence is estimated to be at a level 3 out of 9.

![Chess AI Terminal Screenshot](https://github.com/jameslim1021/Chess-AI/blob/master/screenshots/chessai.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisities

1. [Python 2](https://www.python.org/downloads/)
2. [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
3. [PyPy](http://pypy.org/download.html) (Python2.7 compatible)

### Installing

After installing the prerequisites and cloning this repo, go into the repo and create a virtual env:

```
virtualenv env
```

Activate the env:

```
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Run the game with:

```
python chess_ai.py
```

It is HIGHLY recommended that you run ```chess_ai.py``` with PyPy to greatly reduce computation time.

## Minimax Algorithm

Borrowing from Wikipedia's concise definition, the [minimax algorithm](https://en.wikipedia.org/wiki/Minimax) is "a decision rule used ... for minimizing the possible loss for a worst case (maximum loss) scenario." With respect to chess, the player to act is the maximizer, whose move would be met with an adversarial response from the opponent (minimizer). The minimax algorithm assumes that the opponent is competent and would respond by minimizing the value (determined by some heuristic) of the maximizer.

![Minimax Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Minimax.svg/701px-Minimax.svg.png "Minimax Diagram")

This simplified tree represents a game where each depth represents a player's turn. Starting at the bottom of the tree (the deeper into the tree, the further into the game), the leaf nodes' values are passed back up to determine the maximizer's current best move. In an actual chess game, the each depth would have many more branches with each branch representing a possible move by a chess piece.

## Alpha-Beta Pruning

Because of the number of board states possible in chess (estimated to be [10^120](https://en.wikipedia.org/wiki/Shannon_number)), minimax can be improved with a layer of [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). By keeping track of alpha (the highest value guaranteed to the maximizer) and beta (the lowest value guaranteed to the minimizer), it is possible to avoid calculating the heuristics of certain board states that cannot improve the situation for the current player.

![Alpha-Beta Pruning Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/AB_pruning.svg/1212px-AB_pruning.svg.png "Alpha-Beta Pruning Diagram")

The grayed-out leaf node with a heuristic of 5 is never explored because the maximizer, at that point, is guaranteed a 5 by going left and can do no better than 4 by going right. That is, if the value of the grayed-out leaf node is greater than 4, the minimizer would choose the 4. If it were less than 4, the minimizer would choose it instead. From the maximizer's perspective, there is no reason to investigate that leaf node.

For more information on the history of chess, minimax, and alpha-beta pruning, check out Patrick Winston's [lecture](https://www.youtube.com/watch?v=STjW3eH0Cik).

## Heuristics

There are many factors when calculating the heuristics of a chessboard. As we developed our heuristic formula to consider more factors, the computations required to calculate the best move increased exponentially. At the moment, the AI considers the following 4 aspects of a board in its heuristic function.

### Material
The material heuristic compares the value of one's pieces with the opponent's pieces. It encourages the AI to capture pieces and make favorable trades. We used the standard values for each piece:
* Pawn: 1
* Bishop/Knight: 3
* Rook: 5
* Queen: 9

### Number of Moves
This heuristic calculates the number of legal moves a player can make. It encourages the AI to develop its pieces to exert more control over the board. It prioritizes controlling the center where pieces will have more options to influence the game. For example, a queen near the center of the board can move in 8 directions and thus control more squares, whereas a queen on a corner square can only move in 3 directions.

### Pawn Structure
The pawn structure heuristic gives a score based on the number of pawns supported by other pawns. It encourages the AI to develop its pawns in a way that allows pawns moving forward to be defended by other pawns from behind.

### Check Status
This heuristic checks if a player is in check or checkmate status. It encourages the AI to make moves that would put the opponent in check while avoiding moves that would put itself in check. It also detects if a move would put opponent in checkmate, which would be prioritized over all other heuristics.

### Other Heuristics
The heuristics we used don't come close to representing all the depth involved in chess. Creating a heuristic that would encourage the AI to employ more complex strategies and tactics is not only conceptually difficult. It is also computationally demanding. As we optimize our engine, we would like to tweak our heuristics to better match the complexities of chess.

For more ideas about chess heuristics, check out this [article](https://www.quora.com/What-are-some-heuristics-for-quickly-evaluating-chess-positions).

## Authors

* **Ian Jabour** - [l4nk332](https://github.com/l4nk332)
* **James Lim** - [lamesjim](https://github.com/lamesjim)
* **Dai Nguyen** - [dnguyen87](https://github.com/dnguyen87)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* cgearheart's [Chessnut](https://github.com/cgearhart/Chessnut)
* Aleks Kamko's [Alpha-Beta Pruning Practice](http://inst.eecs.berkeley.edu/~cs61b/fa14/ta-materials/apps/ab_tree_practice/)
