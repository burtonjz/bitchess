import pytest
from bitchess import core, squareset as ss
from bitchess.board import Board
from bitchess.move import Move
from bitchess.game import Game
from bitchess.negamax import Negamax
import numpy as np

def test_get_fen_board():
    fen = 'r7/pp1npp2/3pk2B/2p3p1/3P3p/2N1K3/P3PP2/R7 w - - 0 1'
    board = Board(fen=fen)
    out_fen = board.get_fen_board()
    assert fen.split()[0] == out_fen

def test_get_fen_full():
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    game = Game(fen=fen)
    assert game.get_fen() == fen
    print('test 1 okay')
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Kkq - 0 1'
    game = Game(fen=fen)
    assert game.get_fen() == fen
    print('test 2 okay')

### TESTING ALGEBRAIC TO MOVE

def test_from_move_match():
    '''when converting algebraic to move, need to be able to determine if a
    prospective Move object with potentially multiple from_squares matches a
    legal move.
    '''
    m = Move('QUEEN',core.Color.WHITE,ss.SQUARES[0],ss.SQUARES[1],'quiet')
    m2 = Move('QUEEN',core.Color.WHITE,ss.RANK[0],ss.SQUARES[1],'quiet')
    assert m2._from_square_match(m)

def test_from_move_doesnt_match_wrong_from():
    '''
    won't match because from_squares do not intersect
    '''
    m = Move('QUEEN',core.Color.WHITE,ss.SQUARES[0],ss.SQUARES[1],'quiet')
    m2 = Move('QUEEN',core.Color.WHITE,ss.RANK[7],ss.SQUARES[1],'quiet')
    assert not(m2._from_square_match(m))

def test_from_move_doesnt_match_wrong_data():
    '''
    won't match because other data don't match
    '''
    m = Move('QUEEN',core.Color.WHITE,ss.SQUARES[0],ss.SQUARES[1],'quiet')
    m2 = Move('ROOK',core.Color.WHITE,ss.RANK[7],ss.SQUARES[1],'quiet')
    assert not(m2._from_square_match(m))

# converting algebraic strings to valid move case
def test_str_to_move_quiet_full_notation():
    '''
    full quiet move notation
    '''
    fen = '4k3/8/8/8/8/8/8/Q1Q1K3 w - - 0 1'
    move_str = 'Qa1c3'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is not None

def test_str_to_move_quiet_rank_notation():
    '''
    short quiet move notation, specify rank, not file
    '''
    fen = '4k3/8/8/8/8/Q7/8/Q3K3 w - - 0 1'
    move_str = 'Q1c3'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is not None

def test_str_to_move_quiet_file_notation():
    '''
    short quiet move notation, specify rank, not file
    '''
    fen = '4k3/8/8/8/8/8/8/Q1Q1K3 w - - 0 1'
    move_str = 'Qcc3'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is not None

def test_str_to_move_quiet_short_notation():
    '''
    short quiet move notation
    '''
    fen = '4k3/8/8/8/8/8/8/Q3K3 w - - 0 1'
    move_str = 'Qc3'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is not None

def test_str_to_move_quiet_ambiguous_notation():
    '''
    could be either queen!
    '''
    fen = '4k3/8/8/8/8/8/8/Q1Q1K3 w - - 0 1'
    move_str = 'Qc3'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is None

def test_str_to_move_attack_full_notation():
    '''
    queen attack full notation
    '''
    fen = '4k3/8/8/8/8/8/8/Q1Q1K3 w - - 0 1'
    move_str = 'Qa1xe5'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is None

def test_str_to_move_attack_short_notation():
    '''
    queen attack short notation
    '''
    fen = '4k3/8/8/8/8/8/8/Q1Q1K3 w - - 0 1'
    move_str = 'Qxe5'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is None

def test_str_to_move_quiet_promotion_notation():
    '''
    pawn promotes to queen
    '''
    fen = '4k3/P7/8/8/8/8/8/4K3 w - - 0 1'
    move_str = 'a8=Q'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is not None

def test_str_to_move_capture_promotion_notation():
    '''
    pawn promotes to queen
    '''
    fen = '1r2k3/P7/8/8/8/8/8/7K w - - 0 1'
    move_str = 'axb8=Q'
    g = Game(fen=fen)
    legal_moves = g.current_board.get_legal_moves(g._current_player)
    assert g._str_to_move(move_str,legal_moves) is not None

### TESTING STATUSES

def test_is_not_check():
    fen = '4k2r/8/8/8/8/8/3R4/4K3 w k - 0 1'
    b = Board(fen=fen)
    assert not(b.is_check(core.Color.BLACK))

def test_is_check():
    fen = '4k2r/8/8/8/8/8/4R3/4K3 b k - 0 1'
    b = Board(fen=fen)
    assert b.is_check(core.Color.BLACK)

def test_is_checkmate():
    fen = 'rnbqkbnr/ppppp2p/5p2/6pQ/4P3/3P4/PPP2PPP/RNB1KBNR w KQkq - 0 1'
    board = Board(fen=fen)
    assert board.is_checkmate(core.Color.BLACK)
    
def test_is_not_checkmate():
    board = Board()
    assert not(board.is_checkmate(core.Color.WHITE))

def test_is_stalemate():
    fen = '8/8/8/8/8/5n1p/5k2/7K w - - 0 1'
    board = Board(fen=fen)
    assert board.is_stalemate(core.Color.WHITE)

def test_is_not_stalemate():
    board = Board()
    assert not(board.is_stalemate(core.Color.WHITE))

def test_is_threefold_repetition():
    '''shuffle kings back and forth'''
    fen = 'k7/q7/8/8/8/8/Q7/K7 w - - 0 1'
    game = Game(fen=fen)
    moves = ['Kb1','Kb8','Ka1','Ka8','Kb1','Kb8','Ka1','Ka8']
    for move in moves:
        game.play_str_move(move)
    assert game.is_threefold_repetition()

def test_is_fifty_moves():
    '''shuffle kings around until half-move 100'''
    fen = '7k/8/8/5p1p/5PpP/6P1/8/7K w - - 97 63'
    game = Game(fen=fen)
    moves = ['Kg2','Kg7','Kf2']
    for move in moves:
        game.play_str_move(move)
    assert game.is_fifty_move_rule()

def test_count_material():
    '''material counts correctly calculated'''
    fen = '7k/3n1pp1/4b3/8/2P5/1P6/Q3R3/7K w - - 0 1'
    game = Game(fen=fen)
    assert game.current_board.count_material() == {
        core.Color.WHITE:16,
        core.Color.BLACK:8
    }

def test_get_material_advantage():
    # 1: Black up three pawns
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/P3PPPP/RNBQKBNR w KQkq - 0 1'
    game = Game(fen=fen)
    assert game.get_material_advantage() == -3
    print('test 1 okay')
    # 2: White Checkmate (should be -inf)
    fen = 'rnbqkbnr/ppppp2p/5p2/6pQ/4P3/3P4/PPP2PPP/RNB1KBNR w KQkq - 0 1'
    game = Game(fen=fen)
    assert game.get_material_advantage() == np.inf
    print('test 2 okay')
    # 3: Black Checkmate
    fen = 'rnb1kbnr/ppp2ppp/4p3/3p4/6Pq/P4P2/1PPPP2P/RNBQKBNR b KQkq - 0 1'
    game = Game(fen=fen)
    assert game.get_material_advantage() == -np.inf
    print('test 3 okay')
    # 4: stalemate
    fen = '8/8/8/8/8/1k6/p7/K7 w - - 0 1'
    game = Game(fen=fen)
    print(game.current_board.is_stalemate(0))

    assert game.get_material_advantage() == 0
