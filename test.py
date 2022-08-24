#!/bin/env python3.10

from bitchess.game import Game
from bitchess.core import Status
from datetime import datetime
import pandas as pd
import multiprocessing as mp

g = Game()
g.play(white_move_func=g.move_select_cli,black_move_func=g.move_select_cli)
