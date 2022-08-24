from enum import IntFlag
from . import squareset as ss
from dataclasses import dataclass, field
from typing import Optional, List


class Color():
    WHITE = True
    BLACK = False

PIECE_NAMES = ['PAWN','KNIGHT','BISHOP','ROOK','QUEEN','KING']
PIECE_MATERIAL_POINTS = {
    'PAWN':1,
    'KNIGHT':3,
    'BISHOP':3,
    'ROOK':5,
    'QUEEN':9,
    'KING':0
}
PROMOTION_PIECES = ['KNIGHT','BISHOP','ROOK','QUEEN']

PIECE_CODES = {}
PIECE_CODES[Color.WHITE] = {
    'PAWN':'P',
    'KNIGHT':'N',
    'BISHOP':'B',
    'ROOK':'R',
    'QUEEN':'Q',
    'KING':'K'
}
PIECE_CODES[Color.BLACK] = { k:v.lower() for k,v in PIECE_CODES[Color.WHITE].items()}

CODE_TO_PIECE = { v:k for k,v in PIECE_CODES[Color.WHITE].items() }

PIECE_UNICODE = {}
PIECE_UNICODE[Color.WHITE] = {
    'PAWN':'♟',
    'KNIGHT':'♞',
    'BISHOP':'♝',
    'ROOK':'♜',
    'QUEEN':'♛',
    'KING':'♚'
}
PIECE_UNICODE[Color.BLACK] = {
    'PAWN':'♙',
    'KNIGHT':'♘',
    'BISHOP':'♗',
    'ROOK':'♖',
    'QUEEN':'♕',
    'KING':'♔'
}

def index2algebraic(x):
    '''return algebraic board location from squareset index'''
    if not(isinstance(x,int)):
        raise TypeError('x must be integer')
    if x > 63 or x < 0:
        raise InvalidIndexError
    rank = x // 8 + 1
    file = chr(x % 8 + 97)
    return f'{file}{rank}'

INDEX_TO_ALGEBRAIC = {}
for i in range(0,64):
    INDEX_TO_ALGEBRAIC[i] = index2algebraic(i)

ALGEBRAIC_TO_INDEX = { v:k for k,v in INDEX_TO_ALGEBRAIC.items() }

class Status(IntFlag):
    valid = 0
    checkmate = 1
    stalemate = 2
    threefold_repetition = 4
    fifty_move = 8

    def count(self):
        return bin(self.value).count('1')

@dataclass
class Piece():
    color = bool
    piece_type = int

    def get_piece_name(self):
        return PIECE_NAMES[self.piece_type]

    def get_piece_code(self):
        if self.color:
            return PIECE_CODES[self.piece_type]
        else:
            return PIECE_CODES[self.piece_type].lower()
