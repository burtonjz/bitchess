import pytest
from bitchess import core, squareset as ss
from bitchess.board import Board
from bitchess.move import Move
from bitchess.game import Game
from bitchess.negamax import Negamax

def test_negamax_tree_generation():
    game = Game()
    n = Negamax(game,4)
    n.tree.show()
    assert False
