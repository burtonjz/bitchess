from .game import Game
from .board import Board
from .move import Move
from typing import Optional, List, Tuple, Dict
from dataclasses import dataclass, field
from treelib import Node, Tree
from copy import deepcopy

@dataclass
class GameState:
    game: Game
    '''the current Game instance'''

    evaluation: int
    '''numerical score which evaluates position (e.g., material advantage)'''

class Negamax:
    def __init__(self,game:Game,depth:int):
        self.max_depth = depth
        self.initial_state = GameState(
            deepcopy(game),
            game.get_material_advantage(),

        )
        self.tree = Tree()
        self.root = Node(0,0,data=GameState(game,game.get_material_advantage()))
        self.tree.add_node(self.root)
        self.create_children(self.root,1)

    def create_children(self,node,i):
        if i > self.max_depth:
            return
        legal_moves = node.data.game.current_board.get_legal_moves(node.data.game._current_player)
        for move,board in legal_moves:
            game = deepcopy(node.data.game)
            game._post_move_update(move,board)
            gamestate = GameState(game,game.get_material_advantage())
            n = Node(data=gamestate)
            self.tree.add_node(n,parent=node)
            self.create_children(n,i+1)
