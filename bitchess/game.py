from . import core, squareset as ss
from .board import Board
from .move import Move
from typing import Optional, List, Tuple, Callable, TypeAlias
import numpy as np
import time
import os
import secrets

LegalMoves: TypeAlias = List[Tuple[Move,Board]]

class Game():
    def __init__(self,fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.current_board = Board(fen=fen)
        self.board_stack = []
        self.move_stack = []
        self.fen = fen
        fen_parts = self.fen.split()
        if 'w' in fen_parts[1]:
            self._current_player = core.Color.WHITE
        else:
            self._current_player = core.Color.BLACK
        self._half_move_clock = int(fen_parts[4])
        self._full_move_counter = int(fen_parts[5])
        self.status = core.Status.valid
        # run initial status checks. Either player in checkmate, current
        # player in stalemate (any variation)
        if self.current_board.is_checkmate(self._current_player):
            self.status |= core.Status.checkmate
        if self.current_board.is_checkmate(not(self._current_player)):
            self.status |= core.Status.checkmate
        if self.current_board.is_stalemate(self._current_player):
            self.status |= core.Status.stalemate
        if self.is_fifty_move_rule():
            self.status |= core.Status.fifty_move

    def play(
        self,
        white_move_func:Callable[LegalMoves, Tuple[Move,Board]],
        black_move_func:Callable[LegalMoves, Tuple[Move,Board]],
        *args,
        **kwargs
    ) -> None:
        '''
        play a game of chess. <white_move_func> and <black_move_func> are
        callables where the input should be <LegalMove> ([(Move,Board),...])
        and the output should return the selected tuple (Move,Board).
        '''
        while self.status.count() == 0:
            legal_moves = self.current_board.get_legal_moves(self._current_player)
            if self._current_player:
                move,board = white_move_func(legal_moves)
            else:
                move,board = black_move_func(legal_moves)
            self._post_move_update(move,board)
        return self.status

    def play_str_move(self,s:str) -> None:
        '''
        play a single half move for current player from algebraic string
        '''
        legal_moves = self.current_board.get_legal_moves(self._current_player)
        move,board = self._str_to_move(s,legal_moves)
        self._post_move_update(move,board)

    def _post_move_update(self,move:Move,board:Board) -> None:
        '''perform all updates to game stacks/timers/statuses'''
        self.board_stack.append(self.current_board)
        self.current_board = board
        self.move_stack.append(move)

        # update half-move clock
        if (
            move.piece_type == 'PAWN' or
            move.move_type != 'quiet'
        ):
            self._half_move_clock = 0
        else:
            self._half_move_clock += 1

        if self._current_player:
            self._full_move_counter += 1

        self._update_statuses()
        self._current_player = not(self._current_player)

    # MOVE SELECTION FUNCTIONS
    def _str_to_move(self,s:str,legal_moves:LegalMoves) -> Tuple[Move,Board] | None:
        '''Use algebraic string to get (move,board) from <LegalMoves> object.
        Returns None if multiple matches or no match'''
        if s == '0-0':
            m = Move(
                'KING',
                self._current_player,
                ss.SQUARES[-56 * self._current_player + 60],
                ss.SQUARES[-56 * self._current_player + 62],
                'castle'
            )
        elif s == '0-0-0':
            m = Move(
                'KING',
                self._current_player,
                ss.SQUARES[-56 * self._current_player + 60],
                ss.SQUARES[-56 * self._current_player + 58],
                'castle'
            )
        else:
            if s[0] in core.CODE_TO_PIECE.keys():
                piece_type = core.CODE_TO_PIECE[s[0]]
                s = s[1:]
            else:
                piece_type = 'PAWN'
            # last two characters might be promotion
            if s[-2] == '=':
                promotion = core.CODE_TO_PIECE[s[-1]]
                s = s[:-2]
            else:
                promotion = None
            # last two characters always target square
            target = ss.SQUARES[core.ALGEBRAIC_TO_INDEX[s[-2:]]]
            s = s[:-2]
            # x indicates it's an attack
            if len(s) > 0 and s[-1] == 'x':
                move_type = 'attack'
                s = s[:-1]
            else:
                move_type = 'quiet'
            # whatever's left hints at the from square
            from_square = ss.UNIVERSE.copy()
            for x in s:
                uni = ord(x)
                if uni in range(97,105): #it's a file
                    from_square &= ss.FILE[uni-97]
                elif x.isdigit(): #it's rank
                    from_square &= ss.RANK[int(x)-1]
            m = Move(
                piece_type, self._current_player, from_square,
                target, move_type, promotion
            )
        # make sure only one move in legal_moves matches
        out = []
        for move,board in legal_moves:
            if move._from_square_match(m):
                out.append((move,board))
        if len(out) == 1:
            return out[0]
        else:
            return None

    def move_select_cli(self,legal_moves:LegalMoves) -> Tuple[Move,Board]:
        '''interactively select a move at command line'''
        self.current_board.print_boardstate()
        if self._current_player == core.Color.WHITE:
            color = 'White'
        else:
            color = 'Black'
        move = None
        while True:
            move_str = input(f"\n{color}'s move:")
            try:
                move,board = self._str_to_move(move_str,legal_moves)
            except:
                pass
            if move is None:
                print('\x1b[1A' + '\x1b[2K' + 'Invalid Move. Please try again...')
            else:
                break
        return move,board

    def move_select_random(self,legal_moves:LegalMoves) -> Tuple[Move,Board]:
        '''select a random move from LegalMoves'''
        i = secrets.randbelow(len(legal_moves))
        return legal_moves[i]

    # GAME STATUS FUNCTIONS
    def _update_statuses(self):
        '''check the current position for all game-ending statuses'''
        opponent = not(self._current_player)
        is_check = self.current_board.is_check(opponent)
        if self.current_board.is_checkmate(opponent,is_check):
            self.status |= core.Status.checkmate
        if self.current_board.is_stalemate(opponent,is_check):
            self.status |= core.Status.stalemate
        if self.is_fifty_move_rule():
            self.status |= core.Status.fifty_move
        if self.is_threefold_repetition():
            self.status |= core.Status.threefold_repetition

    def is_threefold_repetition(self):
        '''evaluates whether the current position has been reached 3 times'''
        i = 0
        for b in self.board_stack[:-1]:
            i += b == self.current_board
        return i >= 2

    def is_fifty_move_rule(self):
        '''returns True if 50-move rule has been hit. No pawn move or capture
        in 50 full moves.'''
        if self._half_move_clock >= 100:
            return True
        return False

    def get_fen(self):
        '''generates a fen for the current game state'''
        fen = self.current_board.get_fen_board()
        fen += f' {chr(98+21*self._current_player)} ' # add current player
        c = ''
        if self.current_board.castling[core.Color.WHITE]['KINGSIDE']:
            c += 'K'
        if self.current_board.castling[core.Color.WHITE]['QUEENSIDE']:
            c += 'Q'
        if self.current_board.castling[core.Color.BLACK]['KINGSIDE']:
            c += 'k'
        if self.current_board.castling[core.Color.BLACK]['QUEENSIDE']:
            c += 'q'
        if c == '':
            fen += '-'
        else:
            fen += c
        fen += ' '
        try:
            i = self.current_board.squaresets['EN_PASSANT'].index(1)
            fen += core.INDEX_TO_ALGEBRAIC[i]
        except:
            fen += '-'
        fen += f' {self._half_move_clock} {self._full_move_counter}'
        return fen

        n_empty = 0
        for i in range(56,-1,-8):
            for j in range(0,8):
                piece_info = self.current_board.get_piece_at_index(i+j)
                if piece_info is not None:
                    fen.append(core.PIECE_CODES[piece_info[1]][piece_info[0]])
                    n_empty = 0
                else:
                    n_empty += 1
                core.PIECE_CODES

    # GAME EVALUATION FUNCTIONS
    def get_material_advantage(self) -> int:
        '''
        WHITE-BLACK material, +- inf if status is complete
        '''
        scores = self.current_board.count_material()
        if self.status.count() == 0:
            return scores[core.Color.WHITE] - scores[core.Color.BLACK]
        else:
            if self.status == core.Status.checkmate:
                if self._current_player:
                    return np.inf
                else:
                    return -np.inf
            else:
                return 0
