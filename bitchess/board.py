'''board representation class'''
import re
import colorama
from typing import Optional, List, Tuple
from bitarray import bitarray
from . import core, squareset as ss
from .move import Move
from copy import deepcopy

def _copy_board(board):
    '''
    return a copy of the board object
    '''
    b = Board(fen=None)
    b.squaresets = { k:v.copy() for k,v in board.squaresets.items()}
    b.castling = deepcopy(board.castling)
    b.ep_index = board.ep_index
    return b

class Board():
    '''
    board representation class.
    '''
    def __init__(self,fen:str='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        if fen is not None:
            self.fen = fen
            self._squaresets_from_fen()

    def __eq__(self,other):
        '''
        overload == to test if boards match
        2 boards are equal if all squaresets are equal and castling rights match
        '''
        for k in self.squaresets.keys():
            if self.squaresets[k] != other.squaresets[k]:
                return False
        if self.castling != other.castling:
            return False
        return True

    def _squaresets_from_fen(self):
        '''
        this function will convert a fen to a dictionary of all square sets,
        save castling information, and en passant square if exists.
        '''
        fen_parts = self.fen.split(' ')
        self.squaresets = {}
        self.squaresets['PAWN'] = self._fen_regex_to_squareset(fen_parts[0],'[pP]')
        self.squaresets['BISHOP'] = self._fen_regex_to_squareset(fen_parts[0],'[bB]')
        self.squaresets['KNIGHT'] = self._fen_regex_to_squareset(fen_parts[0],'[nN]')
        self.squaresets['ROOK'] = self._fen_regex_to_squareset(fen_parts[0],'[rR]')
        self.squaresets['QUEEN'] = self._fen_regex_to_squareset(fen_parts[0],'[qQ]')
        self.squaresets['KING'] = self._fen_regex_to_squareset(fen_parts[0],'[kK]')
        self.squaresets[core.Color.WHITE] = self._fen_regex_to_squareset(fen_parts[0],'[A-Z]')
        self.squaresets[core.Color.BLACK] = self._fen_regex_to_squareset(fen_parts[0],'[a-z]')
        self.squaresets['OCCUPIED'] = self._fen_regex_to_squareset(fen_parts[0],'[A-Za-z]')
        self.squaresets['UNOCCUPIED'] = self.squaresets['OCCUPIED'] ^ ss.UNIVERSE

        # en passant
        if fen_parts[3] == '-':
            self.ep_index = None
            self.squaresets['EN_PASSANT'] = ss.EMPTY.copy()
        else:
            self.ep_index = core.ALGEBRAIC_TO_INDEX[fen_parts[3]]
            self.squaresets['EN_PASSANT'] = ss.SQUARES[self.ep_index].copy()
        self.castling = {}
        self.castling[core.Color.WHITE] = { #
            'KINGSIDE':'K' in fen_parts[2],
            'QUEENSIDE':'Q' in fen_parts[2]
        }
        self.castling[core.Color.BLACK] = {
            'KINGSIDE': 'k' in fen_parts[2],
            'QUEENSIDE': 'q' in fen_parts[2]
        }

    @classmethod
    def copy(cls,board):
        '''
        return a copy of the board object
        '''
        b = cls(fen=None)
        b.squaresets = { k:v.copy() for k,v in board.squaresets.items()}
        b.castling = board.castling.copy()
        b.ep_index = board.ep_index
        return b

    def print_all_squaresets(self):
        for k,v in self.squaresets.items():
            print(f'squareset: {k}')
            ss.print_squareset(v)

    def print_boardstate(self):
        outstr = ''
        for i in range(56,-1,-8):
            outstr += colorama.Fore.GREEN + f'{i//8+1} '
            for j in range(0,8):
                # calculate square color
                square_color = colorama.Fore.LIGHTYELLOW_EX
                if (i / 8) % 2 == (j % 2):
                    square_color = colorama.Fore.GREEN
                # select str to place in square
                piece_info = self.get_piece_at_index(i+j)
                if piece_info is None:
                    piece_str = square_color + '■ '
                else:
                    piece_str = colorama.Fore.RESET + \
                        core.PIECE_UNICODE[piece_info[1]][piece_info[0]] + ' '
                outstr += piece_str
            outstr += '\n'
        outstr += colorama.Fore.GREEN + '  A B C D E F G H' + colorama.Fore.RESET
        print(outstr)

    def get_fen_board(self):
        fen = ''
        n = 0
        for i in range(56,-1,-8):
            if n > 0:
                fen += str(n)
                n = 0
            fen += '/'
            for j in range(i,i+8):
                piece = self.get_piece_at_index(j)
                if piece is None:
                    n += 1
                else:
                    if n > 0:
                        fen += str(n)
                        n = 0
                    fen += core.PIECE_CODES[piece[1]][piece[0]]
        if n > 0:
            fen += str(n)
        return fen[1:]

    def _fen_regex_to_squareset(self,board_fen:str,expr:str) -> bitarray:
        '''
        creates squareset using regex from board position portion of FEN.
        Returns squareset in LERF mapping
        '''
        array = ss.EMPTY.copy()
        for i,rank in enumerate(reversed(board_fen.split('/'))):
            j=0
            for x in rank:
                if x.isdigit():
                    j+=int(x)
                else:
                    if re.match(expr,x):
                        array[8*(i)+j] = True
                    j+=1
        return array

    def get_piece_at_index(self,idx:int):
        '''return (piece_name,piece_color) at index, None if unoccupied'''
        piece_name = self.get_piece_name_at_index(idx)
        if piece_name is None:
            return None
        else:
            if (self.squaresets[core.Color.WHITE] & ss.SQUARES[idx]).count() > 0:
                return piece_name,core.Color.WHITE
            else:
                return piece_name,core.Color.BLACK

    def get_piece_name_at_index(self,idx:int):
        '''returns piece type at index, None if unoccupied'''
        if (self.squaresets['OCCUPIED'] & ss.SQUARES[idx]).count() == 0:
            return None
        else:
            for p in core.PIECE_NAMES:
                if (self.squaresets[p] & ss.SQUARES[idx]).count() > 0:
                    return p

    def get_pseudolegal_moves(self,piece_color:bool) -> List[Move]:
        '''get pseudolegal moves for <piece_color>. Pseudolegal moves are those
        that pieces are capable of making, but does not account for king attacks.
        '''
        moves = self._get_pseudolegal_pawn_moves(piece_color)
        moves.extend(self._get_pseudolegal_knight_moves(piece_color))
        moves.extend(self._get_pseudolegal_bishop_moves(piece_color))
        moves.extend(self._get_pseudolegal_rook_moves(piece_color))
        moves.extend(self._get_pseudolegal_queen_moves(piece_color))
        moves.extend(self._get_pseudolegal_king_moves(piece_color))
        return moves

    def _create_moves(
        self,piece_type:str,piece_color:bool,
        from_square:bitarray,targets:bitarray,
        enemy_squares:bitarray
    ) -> List[Move]:
        '''
        create pseudolegal move objects
        '''
        moves = []
        while targets.count() > 0:
            to_index = targets.index(1)
            targets.invert(to_index)
            if (ss.SQUARES[to_index] & enemy_squares).count() > 0:
                move_type = 'attack'
            else:
                move_type = 'quiet'
            if piece_type == 'PAWN' and (ss.SQUARES[to_index] & ss.END_RANKS != ss.EMPTY):
                for p in core.PROMOTION_PIECES:
                    m = Move(piece_type,piece_color,from_square,ss.SQUARES[to_index],move_type,p)
                    moves.append(m)
            else:
                m = Move(piece_type,piece_color,from_square,ss.SQUARES[to_index],move_type)
                moves.append(m)
        return moves

    def _get_pseudolegal_pawn_moves(self,piece_color:bool) -> List[Move]:
        pieces = self.squaresets[piece_color] & self.squaresets['PAWN']
        enemy_squares = self.squaresets[not(piece_color)] | self.squaresets['EN_PASSANT']

        moves = []
        while pieces.count() > 0:
            # get LSB index and clear
            from_index = pieces.index(1)
            pieces.invert(from_index)
            # get targets
            targets = ss.get_pawn_targets(
                ss.SQUARES[from_index],
                enemy_squares,
                self.squaresets['UNOCCUPIED'],
                piece_color
            )
            m = self._create_moves('PAWN',piece_color,ss.SQUARES[from_index],targets,enemy_squares)
            moves.extend(m)
        return moves

    def _get_pseudolegal_knight_moves(self,piece_color:bool) -> List[Move]:
        pieces = self.squaresets[piece_color] & self.squaresets['KNIGHT']
        enemy_squares = self.squaresets[not(piece_color)]

        moves = []
        while pieces.count() > 0:
            # get LSB index and clear
            from_index = pieces.index(1)
            pieces.invert(from_index)
            # get targets
            targets = ss.get_knight_targets(
                ss.SQUARES[from_index],
                enemy_squares,
                self.squaresets['UNOCCUPIED']
            )
            m = self._create_moves('KNIGHT',piece_color,ss.SQUARES[from_index],targets,enemy_squares)
            moves.extend(m)
        return moves

    def _get_pseudolegal_bishop_moves(self,piece_color:bool) -> List[Move]:
        pieces = self.squaresets[piece_color] & self.squaresets['BISHOP']
        enemy_squares = self.squaresets[not(piece_color)]

        moves = []
        while pieces.count() > 0:
            # get LSB index and clear
            from_index = pieces.index(1)
            pieces.invert(from_index)
            # get targets
            targets = ss.get_bishop_targets(
                ss.SQUARES[from_index],
                enemy_squares,
                self.squaresets['UNOCCUPIED']
            )
            m = self._create_moves('BISHOP',piece_color,ss.SQUARES[from_index],targets,enemy_squares)
            moves.extend(m)
        return moves

    def _get_pseudolegal_rook_moves(self,piece_color:bool) -> List[Move]:
        pieces = self.squaresets[piece_color] & self.squaresets['ROOK']
        enemy_squares = self.squaresets[not(piece_color)]

        moves = []
        while pieces.count() > 0:
            # get LSB index and clear
            from_index = pieces.index(1)
            pieces.invert(from_index)
            # get targets
            targets = ss.get_rook_targets(
                ss.SQUARES[from_index],
                enemy_squares,
                self.squaresets['UNOCCUPIED']
            )
            m = self._create_moves('ROOK',piece_color,ss.SQUARES[from_index],targets,enemy_squares)
            moves.extend(m)
        return moves

    def _get_pseudolegal_queen_moves(self,piece_color:bool) -> List[Move]:
        pieces = self.squaresets[piece_color] & self.squaresets['QUEEN']
        enemy_squares = self.squaresets[not(piece_color)]

        moves = []
        while pieces.count() > 0:
            # get LSB index and clear
            from_index = pieces.index(1)
            pieces.invert(from_index)
            # get targets
            targets = ss.get_queen_targets(
                ss.SQUARES[from_index],
                enemy_squares,
                self.squaresets['UNOCCUPIED']
            )
            m = self._create_moves('QUEEN',piece_color,ss.SQUARES[from_index],targets,enemy_squares)
            moves.extend(m)
        return moves

    def _get_pseudolegal_king_moves(self,piece_color:bool) -> List[Move]:
        pieces = self.squaresets[piece_color] & self.squaresets['KING']
        enemy_squares = self.squaresets[not(piece_color)]

        moves = []
        while pieces.count() > 0:
            # get LSB index and clear
            from_index = pieces.index(1)
            pieces.invert(from_index)
            # get targets
            targets = ss.get_king_targets(
                ss.SQUARES[from_index],
                enemy_squares,
                self.squaresets['UNOCCUPIED']
            )
            m = self._create_moves('KING',piece_color,ss.SQUARES[from_index],targets,enemy_squares)
            moves.extend(m)
        return moves

    def get_legal_moves(self,piece_color:bool):
        '''
        returns list of tuples (move,board) containing legal moves
        '''
        moves = self.get_pseudolegal_moves(piece_color)
        out = []
        for move in moves:
            is_legal,board = self._is_legal_move(piece_color,move)
            if is_legal:
                out.append((move,board))
        # add castling
        out.extend(self._get_legal_castling_moves(piece_color))
        return out

    def _get_legal_castling_moves(self,piece_color:bool):
        '''return list of tuple (move, board) for available castling moves'''
        out = []
        king = self.squaresets['KING'] & self.squaresets[piece_color]

        if self.castling[piece_color]['KINGSIDE']:
            rook = self.squaresets['ROOK'] & self.squaresets[piece_color] & ss.FILE[7]
            king_targets = king >> 1  | king >> 2
            king_move = Move('KING',piece_color,king,king >> 2,'castle')
            rook_move = Move('ROOK',piece_color,rook,rook << 2,'castle')
            if king_targets & self.squaresets['OCCUPIED'] == ss.EMPTY:
                self.place_piece_at(king_targets,'KING',piece_color)
                if not(self.is_check(piece_color)):
                    board = _copy_board(self)
                    board.make_move(king_move)
                    board.make_move(rook_move)
                    out.append((king_move,board))
                self.remove_piece_at(king_targets)
        if self.castling[piece_color]['QUEENSIDE']:
            rook = self.squaresets['ROOK'] & self.squaresets[piece_color] & ss.FILE[0]
            king_targets = (king << 1  | king << 2 )
            king_move = Move('KING',piece_color,king,king << 2,'castle')
            rook_move = Move('ROOK',piece_color,rook,rook >> 3,'castle')
            if king_targets & self.squaresets['OCCUPIED'] == ss.EMPTY:
                self.place_piece_at(king_targets,'KING',piece_color)
                if not(self.is_check(piece_color)):
                    board = _copy_board(self)
                    board.make_move(king_move)
                    board.make_move(rook_move)
                    out.append((king_move,board))
                self.remove_piece_at(king_targets)
        return out

    def _is_legal_move(self,piece_color:bool,move:Move):
        '''
        test pseudolegal move for legality. Make the move, evaluate if resulting
        position is check. Does not test castling as that does not have a
        pseudolegal stage
        '''
        # print(move)
        # print(self.castling)
        test_board = _copy_board(self)
        test_board.make_move(move)
        return not(test_board.is_check(piece_color)), test_board

    def place_piece_at(self,mask:bitarray,piece_type:str,piece_color:bool):
        '''
        place piece of type <piece_type> for player <piece_color> at <mask>
        bitarray. This will overwrite any other piece located on the square
        '''
        not_mask = ss.UNIVERSE ^ mask
        self.squaresets['OCCUPIED'] |= mask
        self.squaresets['UNOCCUPIED'] &= not_mask
        self.squaresets[piece_color] |= mask
        self.squaresets[not(piece_color)] &= not_mask
        for p in core.PIECE_NAMES:
            if p == piece_type:
                self.squaresets[p] |= mask
            else:
                self.squaresets[p] &= not_mask

    def remove_piece_at(self,mask:bitarray):
        '''
        remove any pieces at <mask> bitarray
        '''
        not_mask = ss.UNIVERSE ^ mask
        self.squaresets['OCCUPIED'] &= not_mask
        self.squaresets['UNOCCUPIED'] |= mask
        self.squaresets[core.Color.WHITE] &= not_mask
        self.squaresets[core.Color.BLACK] &= not_mask
        for p in core.PIECE_NAMES:
            self.squaresets[p] &= not_mask

    def make_move(self,move:Move):
        '''
        make move, updating all squaresets accordingly
        '''
        self.place_piece_at(move.to_square,move.piece_type,move.piece_color)
        self.remove_piece_at(move.from_square)

        if move.promotion is not None:
            self.place_piece_at(move.to_square,move.promotion,move.piece_color)

        # handle en passant schtuff
        if move.piece_type == 'PAWN':
            if self.squaresets['EN_PASSANT'] == move.to_square:
                if move.piece_color:
                    target = move.to_square << 8
                else:
                    target = move.to_square >> 8
                self.remove_piece_at(target)
                self.squaresets['EN_PASSANT'] = ss.EMPTY.copy()
            elif move.to_square << 16 == move.from_square:
                self.squaresets['EN_PASSANT'] = move.from_square >> 8
            elif move.to_square >> 16 == move.from_square:
                self.squaresets['EN_PASSANT'] = move.from_square << 8
            else:
                self.squaresets['EN_PASSANT'] = ss.EMPTY.copy()
        else:
            self.squaresets['EN_PASSANT'] = ss.EMPTY.copy()

        # update castling
        if move.piece_type == 'KING':
            self.castling[move.piece_color]['KINGSIDE'] = False
            self.castling[move.piece_color]['QUEENSIDE'] = False
        elif move.piece_type == 'ROOK':
            if (self.castling[move.piece_color]['KINGSIDE'] and
                (move.from_square & ss.FILE[7]) != ss.EMPTY):
                self.castling[move.piece_color]['KINGSIDE'] = False
            if (self.castling[move.piece_color]['QUEENSIDE'] and
                (move.from_square & ss.FILE[0]) != ss.EMPTY):
                self.castling[move.piece_color]['QUEENSIDE'] = False

    # STATUS CHECKS
    def is_check(self,piece_color:bool) -> bool:
        '''
        performs a check to see if <piece_color> is checked in the current
        position.
        :param moves: supply moves list if already generated elsewhere
        :param king_targets: in the case of using this function to evaluate
        castling, king targets is a squareset including the castle-through
        squares
        '''
        moves = self.get_pseudolegal_moves(not(piece_color))
        king = self.squaresets[piece_color] & self.squaresets['KING']
        for m in moves:
            if (m.to_square & king).count() > 0 and m.move_type == 'attack':
                return True
        return False

    def is_checkmate(self,piece_color:bool,is_check:bool=None) -> bool:
        '''
        returns True if player <piece_color> is checkmated. it is checkmate
        '''
        if is_check is None:
            is_check = self.is_check(piece_color)
        return is_check and not(self.get_legal_moves(piece_color))

    def is_stalemate(self,piece_color:bool,is_check:bool=None) -> bool:
        '''
        returns True if player <piece_color> is not in check and has no moves
        '''
        if is_check is None:
            is_check = self.is_check(piece_color)
        return not(is_check) and not(self.get_legal_moves(piece_color))

    def count_material(self):
        '''return matieral counts by player'''
        score = {}
        for player in (core.Color.WHITE,core.Color.BLACK):
            score[player] = 0
            for piece in core.PIECE_NAMES:
                score[player] += (
                    (self.squaresets[piece] & self.squaresets[player]).count() *
                    core.PIECE_MATERIAL_POINTS[piece]
                )
        return score
