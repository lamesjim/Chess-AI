# Chess AI

This project focuses on computer science concepts such as data structures and algorithms. Chessnut is the chess engine we are using for all the moves and chess logic. We are utilizing a tree to generate the possible chessboards 3 levels deep and depth first search, minimax, and alpha-beta pruning to find the best move based on the following heuristics:

* material (total piece count for each player)
* number of possible legal moves with emphasis on center squares
* check/checkmate status
* pawn structure

Currently trying to implement multiprocessing as our recursive function uses a lot of computing power so calculating heuristics on board states more than 4 levels deep takes a lot of time. With a depth of 3 leves, our AI makes pretty good moves but also makes a lot of ill-advised ones as well. The AI's chess intelligence is estimated to be at a level 3 out of 9.

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

Borrowing from Wikipedia's concise definition, the [minimax algorithm](https://en.wikipedia.org/wiki/Minimax) is "a decision rule used ... for minimizing the possible loss for a worst case (maximum loss) scenario." With respect to chess, each move a player makes is met with a response from the opponent (barring a checkmate or draw). The minimax algorithm assumes that the opponent is competent and that the opponent will respond by minimizing the value (given some heuristic to determine value) of your future moves.

![Minimax Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Minimax.svg/701px-Minimax.svg.png "Minimax Diagram")

This simplified tree represents a game where each depth is a player's turn to act. Starting at the bottom (further into the future), the leaf nodes' values are passed up depending on the current player's turn. For example, at depth 3, the minimizing player would act in a way to give maximizer a 10 instead of infinity.

In an actual chess game, the each depth would have many more branches with each branch representing a possible move by a chess piece.

## Alpha-Beta Pruning

Because of the number of board states possible in chess (estimated to be [10^120](https://en.wikipedia.org/wiki/Shannon_number)), minimax can be improved with a layer of [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). By keeping track of alpha (the highest value guaranteed to the maximizer) and beta (the highest value value guaranteed to the minimizer), it is possible to avoid calculating the heuristics of certain board states that can not change the alpha-beta values.

![Alpha-Beta Pruning Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/AB_pruning.svg/1212px-AB_pruning.svg.png "Alpha-Beta Pruning Diagram")

The grayed-out leaf node with the 5 is never explored because the maximizer, at this point, is guaranteed a 5 by going left and can do no better than 4 by going right. That is, if the value of the leaf node is greater than 4, the minimizer would choose the 4. If it were less than 4, the minimizer would choose it instead. From the maximizer's perspective, there is no reason to investigate that node.

## Heuristics

(not yet added)

## Authors

* **Ian Jabour** - [l4nk332](https://github.com/l4nk332)
* **James Lim** - [jameslim1021](https://github.com/jameslim1021)
* **Dai Nguyen** - [dnguyen87](https://github.com/dnguyen87)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* cgearheart's [Chessnut](https://github.com/cgearhart/Chessnut)
* Aleks Kamko's [Alpha-Beta Pruning Practice](http://inst.eecs.berkeley.edu/~cs61b/fa14/ta-materials/apps/ab_tree_practice/)
