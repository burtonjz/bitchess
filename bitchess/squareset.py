'''base functions for manipulating squaresets'''

from bitarray import bitarray, util as bitutil
from .exceptions import InvalidSquareSetError
import enum

# Define reference squaresets

UNIVERSE = 64 * bitarray('1',endian='little')
EMPTY = 64 * bitarray('0',endian='little')

SQUARES = {}
for i in range(0,64):
    SQUARES[i] = bitutil.hex2ba('1000000000000000',endian='little') >> i

FILE = [
    8 * bitarray('10000000',endian='little'),
    8 * bitarray('01000000',endian='little'),
    8 * bitarray('00100000',endian='little'),
    8 * bitarray('00010000',endian='little'),
    8 * bitarray('00001000',endian='little'),
    8 * bitarray('00000100',endian='little'),
    8 * bitarray('00000010',endian='little'),
    8 * bitarray('00000001',endian='little')
]
NOT_FILE = [ x ^ UNIVERSE for x in FILE ]


RANK = [
    bitutil.hex2ba('FF00000000000000',endian='little'),
    bitutil.hex2ba('00FF000000000000',endian='little'),
    bitutil.hex2ba('0000FF0000000000',endian='little'),
    bitutil.hex2ba('000000FF00000000',endian='little'),
    bitutil.hex2ba('00000000FF000000',endian='little'),
    bitutil.hex2ba('0000000000FF0000',endian='little'),
    bitutil.hex2ba('000000000000FF00',endian='little'),
    bitutil.hex2ba('00000000000000FF',endian='little')
]
END_RANKS = RANK[0] | RANK[7]
NOT_RANK = [ x ^ UNIVERSE for x in RANK ]

# DIAGONAL ROTATION ALGORITHM
_DIAG_K1 = bitutil.hex2ba('0055005500550055',endian='little')
_DIAG_K2 = bitutil.hex2ba('0000333300003333',endian='little')
_DIAG_K4 = bitutil.hex2ba('00000000F0F0F0F0',endian='little')

# ANTIDIAGONAL ROTATION ALGORITHM
_AD_K1 = bitutil.hex2ba('00AA00AA00AA00AA',endian='little')
_AD_K2 = bitutil.hex2ba('0000CCCC0000CCCC',endian='little')
_AD_K4 = bitutil.hex2ba('F0F0F0F00F0F0F0F',endian='little')


def print_squareset(arr: bitarray) -> bitarray:
    '''
    prints a simple representation of the bitboard to terminal
    '''
    x = arr.to01().replace('0','. ').replace('1','x ')
    for i in range(112,-1,-16):
        print(x[i:i+16])
    print()

def rotate_left(arr:bitarray,n:int) -> bitarray:
    '''
    rotate (shift with rollover) the bitarray by n spaces leftward
    '''
    return (arr<<n)|(arr>>(64-n))

def rotate_right(arr:bitarray,n:int) -> bitarray:
    '''
    rotate bitarray by n spaces rightward
    '''
    return (arr>>n)|(arr>>(64-n))

def flip_vertical(arr: bitarray) -> bitarray:
    '''
    flips bitboard vertically about the center ranks.
    '''
    arr = arr.copy()
    arr.reverse()
    arr.bytereverse()
    return arr

def flip_horizontal(arr: bitarray) -> bitarray:
    '''
    flips bitboard horizontally about the center files.
    '''
    arr = arr.copy()
    arr.bytereverse()
    return arr

def flip_diagonal(arr: bitarray) -> bitarray:
    '''
    flips bitboard diagonally abx the a1-h8 diagonal
    '''
    arr = arr.copy()
    t = _DIAG_K4 & (arr ^ (arr >> 28))
    arr ^= t ^ (t << 28)
    t = _DIAG_K2 & (arr ^ (arr >> 14))
    arr ^= t ^ (t << 14)
    t = _DIAG_K1 & (arr ^ (arr >>  7))
    arr ^= t ^ (t <<  7)
    return arr

def flip_antidiagonal(arr: bitarray) -> bitarray:
    '''
    flips bitboard diagonally about the a8-h1 diagonal
    '''
    arr = arr.copy()
    t = arr ^ (arr >> 36)
    arr ^= _AD_K4 & (t ^ (arr << 36))
    t = _AD_K2 & (arr ^ (arr >> 18))
    arr ^= t ^ (t << 18)
    t = _AD_K1 & (arr ^ (arr >>  9))
    arr ^= t ^ (t <<  9)
    return arr

def rotate90(arr: bitarray) -> bitarray:
    '''
    rotate bitboard by 90 degrees clockwise
    '''
    return SquareSet.flip_antidiagonal(SquareSet.flip_vertical(arr))

def rotate180(arr: bitarray) -> bitarray:
    '''
    rotate bitboard by 180 degrees
    '''
    arr = arr.copy()
    arr.reverse()
    return arr

def rotate270(arr: bitarray) -> bitarray:
    '''
    rotate bitboard by 270 degrees clockwise
    '''
    arr = arr.copy()
    return SquareSet.flip_diagonal(SquareSet.flip_vertical(arr))

def north_fill(arr:bitarray,unoccupied:bitarray=UNIVERSE) -> bitarray:
    '''northward fill of <arr> until stopping point'''
    arr,unoccupied = arr.copy(),unoccupied.copy()
    arr |= unoccupied & (arr >> 8)
    unoccupied &= unoccupied >> 8
    arr |= unoccupied & (arr >> 16)
    unoccupied &= unoccupied >> 16
    arr |= unoccupied & (arr >> 32)
    return arr

def northeast_fill(arr:bitarray,unoccupied:bitarray=UNIVERSE) -> bitarray:
    '''northeast fill of <arr> until stopping point'''
    arr,prop = arr.copy(),(unoccupied & NOT_FILE[0])
    arr |= prop & (arr >> 9)
    prop &= prop >> 9
    arr |= prop & (arr >> 18)
    prop &= prop >> 18
    arr |= prop & (arr >> 18)
    return arr

def east_fill(arr:bitarray,unoccupied:bitarray=UNIVERSE) -> bitarray:
    '''eastward fill of arr until stopping point'''
    arr,prop = arr.copy(),(unoccupied & NOT_FILE[0])
    arr |= prop & (arr >> 1)
    prop &= prop >> 1
    arr |= prop & (arr >> 2)
    prop &= prop >> 2
    arr |= prop & (arr >> 4)
    return arr

def southeast_fill(arr:bitarray,unoccupied:bitarray=UNIVERSE) -> bitarray:
    '''southeast fill of <arr> until stopping point'''
    arr,prop = arr.copy(),(unoccupied & NOT_FILE[0])
    arr |= prop & (arr << 7)
    prop &= prop << 7
    arr |= prop & (arr << 14)
    prop &= prop << 14
    arr |= prop & (arr << 28)
    return arr

def south_fill(arr:bitarray,unoccupied:bitarray=UNIVERSE) -> bitarray:
    '''northward fill of <arr> until stopping point'''
    arr,unoccupied = arr.copy(),unoccupied.copy()
    arr |= unoccupied & (arr << 8)
    unoccupied &= unoccupied << 8
    arr |= unoccupied & (arr << 16)
    unoccupied &= unoccupied << 16
    arr |= unoccupied & (arr << 32)
    return arr

def southwest_fill(arr:bitarray,unoccupied:bitarray=UNIVERSE) -> bitarray:
    '''southwest fill of <arr> until stopping point'''
    arr,prop = arr.copy(),(unoccupied & NOT_FILE[7])
    arr |= prop & (arr << 9)
    prop &= prop << 9
    arr |= prop & (arr << 18)
    prop &= prop << 18
    arr |= prop & (arr << 27)
    return arr

def west_fill(arr:bitarray,unoccupied:bitarray=UNIVERSE) -> bitarray:
    '''westward fill of <arr> until stopping point'''
    arr,prop = arr.copy(),(unoccupied & NOT_FILE[7])
    arr |= prop & (arr << 1)
    prop &= prop << 1
    arr |= prop & (arr << 2)
    prop &= prop << 2
    arr |= prop & (arr << 4)
    return arr

def northwest_fill(arr:bitarray,unoccupied:bitarray=UNIVERSE) -> bitarray:
    '''northwest fill of <arr> until stopping point'''
    arr,prop = arr.copy(),(unoccupied & NOT_FILE[7])
    arr |= prop & (arr >> 7)
    prop &= prop >> 7
    arr |= prop & (arr >> 14)
    prop &= prop >> 14
    arr |= prop & (arr >> 28)
    return arr

def shift_north_one(arr:bitarray) -> bitarray:
    '''shifts set north one square'''
    return arr >> 8

def shift_northeast_one(arr:bitarray) -> bitarray:
    '''shifts set north one square'''
    return (arr >> 9) & NOT_FILE[0]

def shift_east_one(arr:bitarray) -> bitarray:
    '''shifts set north one square'''
    return (arr >> 1) & NOT_FILE[0]

def shift_southeast_one(arr:bitarray) -> bitarray:
    '''shifts set north one square'''
    return (arr << 7) & NOT_FILE[0]

def shift_south_one(arr:bitarray) -> bitarray:
    '''shifts set north one square'''
    return arr << 8

def shift_southwest_one(arr:bitarray) -> bitarray:
    '''shifts set north one square'''
    return (arr << 9) & NOT_FILE[7]

def shift_west_one(arr:bitarray) -> bitarray:
    '''shifts set north one square'''
    return (arr << 1) & NOT_FILE[7]

def shift_northwest_one(arr:bitarray) -> bitarray:
    '''shifts set north one square'''
    return (arr >> 7)  & NOT_FILE[7]

# targets
# Generate pseudo-legal targets for each piece

def get_knight_targets(square: bitarray,
                     enemy_squares: bitarray,
                     unoccupied_squares: bitarray) -> bitarray:
    east_one = shift_east_one(square)
    west_one = shift_west_one(square)
    # 1 horizontal 2 vertical
    one_shift = east_one | west_one
    targets = one_shift << 16
    targets |= one_shift >> 16
    # 2 horizontal 2 vertical
    two_shift = shift_east_one(east_one) | shift_west_one(west_one)
    targets |= two_shift << 8
    targets |= two_shift >> 8
    # filter to valid squares
    return targets & (enemy_squares | unoccupied_squares)

def get_bishop_targets(square: bitarray,
                     enemy_squares: bitarray,
                     unoccupied_squares: bitarray) -> bitarray:
    northeast = northeast_fill(square,unoccupied_squares)
    northeast |= (shift_northeast_one(northeast) & enemy_squares)
    southeast = southeast_fill(square,unoccupied_squares)
    southeast |= (shift_southeast_one(southeast) & enemy_squares)
    northwest = northwest_fill(square,unoccupied_squares)
    northwest |= (shift_northwest_one(northwest) & enemy_squares)
    southwest = southwest_fill(square,unoccupied_squares)
    southwest |= (shift_southwest_one(southwest) & enemy_squares)
    targets = northeast | southeast | northwest | southwest
    targets ^= square # remove self from targets
    return targets

def get_rook_targets(square: bitarray,
                   enemy_squares: bitarray,
                   unoccupied_squares: bitarray) -> bitarray:
    north = north_fill(square,unoccupied_squares)
    north |= (shift_north_one(north) & enemy_squares)
    east = east_fill(square,unoccupied_squares)
    east |= (shift_east_one(east) & enemy_squares)
    south = south_fill(square,unoccupied_squares)
    south |= (shift_south_one(south) & enemy_squares)
    west = west_fill(square,unoccupied_squares)
    west |= (shift_west_one(west) & enemy_squares)
    targets = north | east | south | west
    targets ^= square # remove self from targets
    return targets

def get_queen_targets(square: bitarray,
                    enemy_squares: bitarray,
                    unoccupied_squares: bitarray) -> bitarray:
    return get_rook_targets(square,enemy_squares,unoccupied_squares) | \
        get_bishop_targets(square,enemy_squares,unoccupied_squares)

def get_pawn_targets(square: bitarray,
                   enemy_squares: bitarray,
                   unoccupied_squares: bitarray,
                   color: bool) -> bitarray:
    '''enemy_squares must include en passant square here'''
    if color: # white
        empty_for_double_push = RANK[3] & unoccupied_squares
        single_push = shift_north_one(square) & unoccupied_squares
        double_push = shift_north_one(single_push) & empty_for_double_push
        attack_east = shift_northeast_one(square) & enemy_squares
        attack_west = shift_northwest_one(square) & enemy_squares
        return single_push | double_push | attack_east | attack_west
    else: #black
        empty_for_double_push = RANK[4] & unoccupied_squares
        single_push = shift_south_one(square) & unoccupied_squares
        double_push = shift_south_one(single_push) & empty_for_double_push
        attack_east = shift_southeast_one(square) & enemy_squares
        attack_west = shift_southwest_one(square) & enemy_squares
        return single_push | double_push | attack_east | attack_west

def get_king_targets(square: bitarray,
                   enemy_squares: bitarray,
                   unoccupied_squares: bitarray) -> bitarray:
    targets = shift_north_one(square)
    targets |= shift_northeast_one(square)
    targets |= shift_east_one(square)
    targets |= shift_southeast_one(square)
    targets |= shift_south_one(square)
    targets |= shift_southwest_one(square)
    targets |= shift_west_one(square)
    targets |= shift_northwest_one(square)
    return targets & (enemy_squares | unoccupied_squares)

def get_queenside_castle(king_square: bitarray) -> bitarray:
    return (king_square << 2),(king_square << 1)

def get_kingside_castle(king_square: bitarray) -> bitarray:
    return (king_square >> 2),(king_square >> 1)
