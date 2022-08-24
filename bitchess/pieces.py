'''chess pieces class'''
from bitarray import bitarray
import bitchess.squareset as ss
from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self,player,i):
        '''
        :param player: "WHITE" or "BLACK"
        :param i: piece bitarray index
        '''
        self.player = player
        self.i = i

        self.array = bitarray('0',endian='little') * 64
        self.array[self.i] = 1

    @abstractmethod
    def generate_pseudolegal_moves(self):
        '''get all pseudolegal moves for piece'''
        return

    def _process_targets(self,targets,enemy_squares,i_en_passant=None):
        '''
        after targets are generated, produce moves dictionary
        :param targets: bitarray of move target squares
        :param enemy_squares: bitarray of enemy squares

        '''
        moves = []
        while targets.count() > 0:
            to_index = targets.index(1)
            if enemy_squares[to_index]:
                move_type = 'attack'
            else:
                move_type = 'quiet'
            if self.piece_type == 'KING':
                if to_index - self.i == 2:
                    move_type = 'kingside_castle'
                elif to_index - self.i == -2:
                    move_type = 'queenside_castle'
            d = {
                'piece':self.piece_type,
                'code':self.piece_code,
                'from':self.i,
                'to':to_index,
                'type':move_type,
                'en_passant':to_index == i_en_passant
            }
            targets.invert(to_index)
            yield d


class Pawn(Piece):
    piece_code = ''
    piece_type = 'PAWN'
    def generate_pseudolegal_moves(self,enemy_squares,unoccupied_squares,i_en_passant):
        '''
        get all pseudolegal moves for pawn
        :param enemy_squares: bitarray containing enemy piece locations +
        en passant square
        :param unoccupied_squares: bitarray containing open squares
        '''
        if self.player == 'WHITE':
            empty_4th_rank = ss.RANK[3] & unoccupied_squares

            single_push = ss.shift_north_one(self.array) & unoccupied_squares
            double_push = ss.shift_north_one(single_push) & empty_4th_rank

            attack_east = ss.shift_northeast_one(self.array) & enemy_squares
            attack_west = ss.shift_northwest_one(self.array) & enemy_squares
            targets = single_push | double_push | attack_east | attack_west

            moves = self._process_targets(targets,enemy_squares,i_en_passant)

        elif self.player == 'BLACK':
            empty_5th_rank = ss.RANK[4] & unoccupied_squares

            single_push = ss.shift_south_one(self.array) & unoccupied_squares
            double_push = ss.shift_south_one(single_push) & empty_5th_rank

            attack_east = ss.shift_southeast_one(self.array) & enemy_squares
            attack_west = ss.shift_southwest_one(self.array) & enemy_squares
            targets = single_push | double_push | attack_east | attack_west

            moves = self._process_targets(targets,enemy_squares,i_en_passant)

        return moves

class Knight(Piece):
    piece_code = 'N'
    piece_type = 'KNIGHT'
    def generate_pseudolegal_moves(self,enemy_squares,unoccupied_squares):
        '''
        generates all pseudolegal moves for the knight piece

        :param enemy_squares: squareset with enemy piece locations
        :param unoccupied_squares: squareset with empty squares
        '''
        east_one = ss.shift_east_one(self.array)
        west_one = ss.shift_west_one(self.array)

        # 1 horizontal 2 vertical
        one_shift = east_one | west_one
        targets = one_shift << 16
        targets |= one_shift >> 16

        # 2 horizontal 2 vertical
        two_shift = ss.shift_east_one(east_one) | ss.shift_west_one(west_one)
        targets |= two_shift << 8
        targets |= two_shift >> 8

        # filter to valid squares
        valid_target = enemy_squares | unoccupied_squares
        targets &= valid_target

        return self._process_targets(targets,enemy_squares)

class Bishop(Piece):
    piece_code = 'B'
    piece_type = 'BISHOP'
    def generate_pseudolegal_moves(self,enemy_squares,unoccupied_squares):
        northeast = ss.northeast_fill(self.array,unoccupied_squares)
        northeast |= (ss.shift_northeast_one(northeast) & enemy_squares)

        southeast = ss.southeast_fill(self.array,unoccupied_squares)
        southeast |= (ss.shift_southeast_one(southeast) & enemy_squares)

        northwest = ss.northwest_fill(self.array,unoccupied_squares)
        northwest |= (ss.shift_northwest_one(northwest) & enemy_squares)

        southwest = ss.southwest_fill(self.array,unoccupied_squares)
        southwest |= (ss.shift_southwest_one(southwest) & enemy_squares)

        targets = northeast | southeast | northwest | southwest
        targets[self.i] = 0 # fills include self, so let's remove it

        return self._process_targets(targets,enemy_squares)

class Rook(Piece):
    piece_code = 'R'
    piece_type = 'ROOK'
    def generate_pseudolegal_moves(self,enemy_squares,unoccupied_squares):
        north = ss.north_fill(self.array,unoccupied_squares)
        north |= (ss.shift_north_one(north) & enemy_squares)

        east = ss.east_fill(self.array,unoccupied_squares)
        east |= (ss.shift_east_one(east) & enemy_squares)

        south = ss.south_fill(self.array,unoccupied_squares)
        south |= (ss.shift_south_one(south) & enemy_squares)

        west = ss.west_fill(self.array,unoccupied_squares)
        west |= (ss.shift_west_one(west) & enemy_squares)

        targets = north | east | south | west
        targets[self.i] = 0 # fills include self, so let's remove it

        return self._process_targets(targets,enemy_squares)

class Queen(Piece):
    piece_code = 'Q'
    piece_type = 'QUEEN'
    def generate_pseudolegal_moves(self,enemy_squares,unoccupied_squares):
        north = ss.north_fill(self.array,unoccupied_squares)
        north |= (ss.shift_north_one(north) & enemy_squares)

        northeast = ss.northeast_fill(self.array,unoccupied_squares)
        northeast |= (ss.shift_northeast_one(northeast) & enemy_squares)

        east = ss.east_fill(self.array,unoccupied_squares)
        east |= (ss.shift_east_one(east) & enemy_squares)

        southeast = ss.southeast_fill(self.array,unoccupied_squares)
        southeast |= (ss.shift_southeast_one(southeast) & enemy_squares)

        south = ss.south_fill(self.array,unoccupied_squares)
        south |= (ss.shift_south_one(south) & enemy_squares)

        southwest = ss.southwest_fill(self.array,unoccupied_squares)
        southwest |= (ss.shift_southwest_one(southwest) & enemy_squares)

        west = ss.west_fill(self.array,unoccupied_squares)
        west |= (ss.shift_west_one(west) & enemy_squares)

        northwest = ss.northwest_fill(self.array,unoccupied_squares)
        northwest |= (ss.shift_northwest_one(northwest) & enemy_squares)

        targets = north | northeast | east | southeast | \
                  south | southwest | west | northwest
        targets[self.i] = 0 # fills include self, so let's remove it

        return self._process_targets(targets,enemy_squares)

class King(Piece):
    piece_code = 'K'
    piece_type = 'KING'
    def __init__(self,player,i,castling):
        '''castling[color]["queenside"|"kingside"]'''
        self.castling = castling
        super().__init__(player,i)

    def generate_pseudolegal_moves(self,enemy_squares,unoccupied_squares):
        valid_target = enemy_squares | unoccupied_squares
        targets = ss.shift_north_one(self.array) & valid_target
        targets |= ss.shift_northeast_one(self.array) & valid_target

        east = ss.shift_east_one(self.array) & valid_target
        targets |= east
        targets |= ss.shift_southeast_one(self.array) & valid_target
        targets |= ss.shift_south_one(self.array) & valid_target
        targets |= ss.shift_southwest_one(self.array) & valid_target
        west = ss.shift_west_one(self.array) & valid_target
        targets |= west
        targets |= ss.shift_northwest_one(self.array) & valid_target

        if self.castling['KINGSIDE']:
            targets |= ss.shift_east_one(east) & valid_target
        if self.castling['QUEENSIDE']:
            targets |= ss.shift_west_one(west) & valid_target

        return self._process_targets(targets,enemy_squares)
