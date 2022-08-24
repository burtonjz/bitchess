from typing import Optional, List
from dataclasses import dataclass, field
from bitarray import bitarray
from copy import deepcopy
from . import core, squareset as ss

@dataclass
class Move():
    piece_type: str
    '''type of piece moving'''

    piece_color: bool
    '''color of piece (True == White)'''

    from_square: bitarray
    '''bitarray of departing square'''

    to_square: bitarray
    '''bitarray of target square'''

    move_type: str
    '''specify type of move (e.g., quiet, attack)'''

    promotion: Optional[str] = field(default=None)
    '''specify promotion piece name (if move results in promotion)'''

    def get_uci(self) -> str:
        '''return long algebraic move string'''
        s = core.INDEX_TO_ALGEBRAIC[self.from_square.index(1)] + \
            core.INDEX_TO_ALGEBRAIC[self.to_square.index(1)]

        if self.promotion is not None:
            return s + core.PIECE_CODES[core.Color.BLACK][self.promotion]
        else:
            return s

    def get_pgn(self) -> str:
        if self.move_type == 'castle':
            if self.to_square > self.from_square:
                s = '0-0'
            else:
                s = '0-0-0'
        else:
            s = core.PIECE_CODES[core.Color.WHITE][self.piece_type].replace('P','')
            s += core.INDEX_TO_ALGEBRAIC[self.from_square.index(1)]
            if self.move_type == 'attack':
                s += 'x'
            s += core.INDEX_TO_ALGEBRAIC[self.to_square.index(1)]
            if self.promotion is not None:
                s += f'={core.PIECE_CODES[core.Color.WHITE][self.promotion]}'
        return s


    def _from_square_match(self,other_move) -> List[str]:
        '''returns True if all data elements match and self.from_square is in
        other_move.from_square'''
        keys = list(self.__dict__.keys())
        keys.remove('from_square')
        for k in keys:
            if self.__dict__[k] != other_move.__dict__[k]:
                return False
        if self.from_square & other_move.from_square == ss.EMPTY:
            return False
        return True

    @classmethod
    def copy(cls,obj):
        '''return a copy of object'''
        d = {}
        for k,v in obj.__dict__.items():
            d[k] = deepcopy(v)
        return cls(**d)
