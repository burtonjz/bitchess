"""
static bitarrays useful for quickly performing squareset operations
"""
from bitarray import bitarray
import bitarray.util as bitutil

EMPTY = bitarray('0',endian='little')*64
UNIVERSE = bitarray('1',endian='little')*64

#RANKS
RANK0 = bitutil.hex2ba('FF00000000000000',endian='little')
RANK1 = bitutil.hex2ba('00FF000000000000',endian='little')
RANK2 = bitutil.hex2ba('0000FF0000000000',endian='little')
RANK3 = bitutil.hex2ba('000000FF00000000',endian='little')
RANK4 = bitutil.hex2ba('00000000FF000000',endian='little')
RANK5 = bitutil.hex2ba('0000000000FF0000',endian='little')
RANK6 = bitutil.hex2ba('000000000000FF00',endian='little')
RANK7 = bitutil.hex2ba('00000000000000FF',endian='little')

RANKS_ODD = bitutil.hex2ba('00FF00FF00FF00FF',endian='little')
RANKS_EVEN = bitutil.hex2ba('FF00FF00FF00FF00',endian='little')
RANKS_MIDDLE2 = bitutil.hex2ba('0000FFFFFFFF0000',endian='little')
RANKS_MIDDLE4 = bitutil.hex2ba('000000FFFF000000',endian='little')
RANKS_OUTER2 = bitutil.hex2ba('F0000000000F',endian='little')
RANKS_OUTER4 = bitutil.hex2ba('FF00000000FF',endian='little')
RANKS_2OFF2ON = bitutil.hex2ba('0000FFFF0000FFFF',endian='little')
RANKS_2ON2OFF = bitutil.hex2ba('FFFF0000FFFF0000',endian='little')
RANKS_BOTTOM = bitutil.hex2ba('FFFFFFFF00000000',endian='little')
RANKS_TOP = bitutil.hex2ba('00000000FFFFFFFF',endian='little')

# FILES
FILE0 = 8 * bitarray('10000000',endian='little')
FILE1 = 8 * bitarray('01000000',endian='little')
FILE2 = 8 * bitarray('00100000',endian='little')
FILE3 = 8 * bitarray('00010000',endian='little')
FILE4 = 8 * bitarray('00001000',endian='little')
FILE5 = 8 * bitarray('00000100',endian='little')
FILE6 = 8 * bitarray('00000010',endian='little')
FILE7 = 8 * bitarray('00000001',endian='little')

NOT_FILE0 = FILE0.copy()
NOT_FILE0.invert()
NOT_FILE1 = FILE1.copy()
NOT_FILE1.invert()
NOT_FILE2 = FILE2.copy()
NOT_FILE2.invert()
NOT_FILE3 = FILE3.copy()
NOT_FILE3.invert()
NOT_FILE4 = FILE4.copy()
NOT_FILE4.invert()
NOT_FILE5 = FILE5.copy()
NOT_FILE5.invert()
NOT_FILE6 = FILE6.copy()
NOT_FILE6.invert()
NOT_FILE7 = FILE7.copy()
NOT_FILE7.invert()

FILES_EVEN = bitutil.hex2ba('5555555555555555',endian='little')
FILES_ODD = bitutil.hex2ba('AAAAAAAAAAAAAAAA',endian='little')
FILES_MIDDLE2 = bitutil.hex2ba('8181818181818181',endian='little')
FILES_MIDDLE4 = bitutil.hex2ba('C3C3C3C3C3C3C3C3',endian='little')
FILES_OUTER2 = bitutil.hex2ba('1818181818181818',endian='little')
FILES_OUTER4 = bitutil.hex2ba('3C3C3C3C3C3C3C3C',endian='little')
FILES_2ON2OFF = bitutil.hex2ba('3333333333333333',endian='little')
FILES_2OFF2ON = bitutil.hex2ba('CCCCCCCCCCCCCCCC',endian='little')
FILES_LEFT = bitutil.hex2ba('F0F0F0F0F0F0F0F0',endian='little')
FILES_RIGHT = bitutil.hex2ba('0F0F0F0F0F0F0F0F',endian='little')

#DIAGONALS
A1_DIAGONAL = bitutil.hex2ba('1020408001020408',endian='little')
A2_DIAGONAL = bitutil.hex2ba('0010204080010204',endian='little')
A3_DIAGONAL = bitutil.hex2ba('0000102040800102',endian='little')
A4_DIAGONAL = bitutil.hex2ba('0000001020408001',endian='little')
A5_DIAGONAL = bitutil.hex2ba('0000000010204080',endian='little')
A6_DIAGONAL = bitutil.hex2ba('0000000000102040',endian='little')
A7_DIAGONAL = bitutil.hex2ba('0000000000001020',endian='little')
A8_DIAGONAL = bitutil.hex2ba('0000000000000010',endian='little')

B1_DIAGONAL = bitutil.hex2ba('2040800102040800',endian='little')
C1_DIAGONAL = bitutil.hex2ba('4080010204080000',endian='little')
D1_DIAGONAL = bitutil.hex2ba('8001020408000000',endian='little')
E1_DIAGONAL = bitutil.hex2ba('0102040800000000',endian='little')
F1_DIAGONAL = bitutil.hex2ba('0204080000000000',endian='little')
G1_DIAGONAL = bitutil.hex2ba('0408000000000000',endian='little')
H1_DIAGONAL = bitutil.hex2ba('8000000000000000',endian='little')

H1_ANTIDIAGONAL = bitutil.hex2ba('0804020180402010',endian='little')
H2_ANTIDIAGONAL = bitutil.hex2ba('0008040201804020',endian='little')
H3_ANTIDIAGONAL = bitutil.hex2ba('0000080402018040',endian='little')
H4_ANTIDIAGONAL = bitutil.hex2ba('0000000804020180',endian='little')
H5_ANTIDIAGONAL = bitutil.hex2ba('0000000008040201',endian='little')
H6_ANTIDIAGONAL = bitutil.hex2ba('0000000000080402',endian='little')
H7_ANTIDIAGONAL = bitutil.hex2ba('0000000000000804',endian='little')
H8_ANTIDIAGONAL = bitutil.hex2ba('0000000000000008',endian='little')

G1_ANTIDIAGONAL = bitutil.hex2ba('0402018040201000',endian='little')
F1_ANTIDIAGONAL = bitutil.hex2ba('0201804020100000',endian='little')
E1_ANTIDIAGONAL = bitutil.hex2ba('0180402010000000',endian='little')
D1_ANTIDIAGONAL = bitutil.hex2ba('8040201000000000',endian='little')
C1_ANTIDIAGONAL = bitutil.hex2ba('4020100000000000',endian='little')
B1_ANTIDIAGONAL = bitutil.hex2ba('2010000000000000',endian='little')
A1_ANTIDIAGONAL = bitutil.hex2ba('1000000000000000',endian='little')

# DIAGONAL ROTATION ALGORITHM
FUNC_DIAG_K1 = bitutil.hex2ba('0055005500550055',endian='little')
FUNC_DIAG_K2 = bitutil.hex2ba('0000333300003333',endian='little')
FUNC_DIAG_K4 = bitutil.hex2ba('00000000F0F0F0F0',endian='little')

# ANTIDIAGONAL ROTATION ALGORITHM
FUNC_AD_K1 = bitutil.hex2ba('00AA00AA00AA00AA',endian='little')
FUNC_AD_K2 = bitutil.hex2ba('0000CCCC0000CCCC',endian='little')
FUNC_AD_K4 = bitutil.hex2ba('F0F0F0F00F0F0F0F',endian='little')
