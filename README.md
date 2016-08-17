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

Borrowing from Wikipedia's concise definition, the [minimax algorithm](https://en.wikipedia.org/wiki/Minimax) is "a decision rule used ... for minimizing the possible loss for a worst case (maximum loss) scenario." With respect to chess, the player to act is the maximizer, whose move would be met with an adversarial response from the opponent (minimizer). The minimax algorithm assumes that the opponent is competent and would respond by minimizing the value (determined by some heuristic) of the maximizer.

![Minimax Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Minimax.svg/701px-Minimax.svg.png "Minimax Diagram")

This simplified tree represents a game where each depth represents a player's turn. Starting at the bottom of the tree (the deeper into the tree, the further into the game), the leaf nodes' values are passed back up to determine the maximizer's current best move. In an actual chess game, the each depth would have many more branches with each branch representing a possible move by a chess piece.

## Alpha-Beta Pruning

Because of the number of board states possible in chess (estimated to be [10^120](https://en.wikipedia.org/wiki/Shannon_number)), minimax can be improved with a layer of [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). By keeping track of alpha (the highest value guaranteed to the maximizer) and beta (the lowest value guaranteed to the minimizer), it is possible to avoid calculating the heuristics of certain board states that cannot improve the situation for the current player.

![Alpha-Beta Pruning Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/AB_pruning.svg/1212px-AB_pruning.svg.png "Alpha-Beta Pruning Diagram")

The grayed-out leaf node with a heuristic of 5 is never explored because the maximizer, at that point, is guaranteed a 5 by going left and can do no better than 4 by going right. That is, if the value of the grayed-out leaf node is greater than 4, the minimizer would choose the 4. If it were less than 4, the minimizer would choose it instead. From the maximizer's perspective, there is no reason to investigate that leaf node.

For more information on the history of chess, minimax, and alpha-beta pruning, check out Patrick Winston's [lecture](https://www.youtube.com/watch?v=STjW3eH0Cik).

## Heuristics

There are s

## Authors

* **Ian Jabour** - [l4nk332](https://github.com/l4nk332)
* **James Lim** - [jameslim1021](https://github.com/jameslim1021)
* **Dai Nguyen** - [dnguyen87](https://github.com/dnguyen87)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* cgearheart's [Chessnut](https://github.com/cgearhart/Chessnut)
* Aleks Kamko's [Alpha-Beta Pruning Practice](http://inst.eecs.berkeley.edu/~cs61b/fa14/ta-materials/apps/ab_tree_practice/)
