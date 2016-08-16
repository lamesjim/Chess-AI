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

## Authors

* **Ian Jabour** - [l4nk332](https://github.com/l4nk332)
* **James Lim** - [jameslim1021](https://github.com/jameslim1021)
* **Dai Nguyen** - [dnguyen87](https://github.com/dnguyen87)

See also the list of [contributors](https://github.com/jameslim1021/Chess-AI/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* cgearheart's [Chessnut](https://github.com/cgearhart/Chessnut)
* Aleks Kamko's [Alpha-Beta Pruning Practice](http://inst.eecs.berkeley.edu/~cs61b/fa14/ta-materials/apps/ab_tree_practice/)
