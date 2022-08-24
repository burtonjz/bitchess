import pytest
from bitchess import core, squareset as ss
from bitchess.board import Board
from bitchess.move import Move

def get_board_matching_move(target_move,legal_moves):
    for move,board in legal_moves:
        if move == target_move:
            return board

def is_move_legal(move,legal_moves):
    for m,board in legal_moves:
        if move == m:
            return True
    return False

def test_simple_pseudolegal_move_results_in_check():
    '''pawn on d2 can't push to d3'''
    fen = '7k/8/8/8/8/8/2KP3r/8 w - - 0 3'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[11],ss.SQUARES[19],'quiet')
    assert not(is_move_legal(move,b.get_legal_moves(move.piece_color)))

def test_simple_kingside_castle_white():
    '''make sure simple kingside castle works'''
    fen = 'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1'
    b = Board(fen=fen)
    move = Move('KING',core.Color.WHITE,ss.SQUARES[4],ss.SQUARES[6],'castle')
    assert is_move_legal(move,b.get_legal_moves(move.piece_color))

def test_simple_kingside_castle_boardstate_white():
    '''verify that simple kingside castle results in proper boardstate'''
    in_fen = 'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1'
    out_fen = 'r3k2r/8/8/8/8/8/8/R4RK1 b kq - 1 1'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('KING',core.Color.WHITE,ss.SQUARES[4],ss.SQUARES[6],'castle')
    legal_moves = in_board.get_legal_moves(core.Color.WHITE)
    board = get_board_matching_move(move,legal_moves)
    assert board == out_board

def test_simple_queenside_castle_white():
    '''make sure simple queenside castle works'''
    fen = 'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1'
    b = Board(fen=fen)
    move = Move('KING',core.Color.WHITE,ss.SQUARES[4],ss.SQUARES[2],'castle')
    assert is_move_legal(move,b.get_legal_moves(move.piece_color))

def test_simple_queenside_castle_boardstate_white():
    '''verify that simple queenside castle results in proper boardstate'''
    in_fen = 'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1'
    out_fen = 'r3k2r/8/8/8/8/8/8/2KR3R b kq - 1 1'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('KING',core.Color.WHITE,ss.SQUARES[4],ss.SQUARES[2],'castle')
    legal_moves = in_board.get_legal_moves(core.Color.WHITE)
    board = get_board_matching_move(move,legal_moves)
    assert board == out_board

def test_simple_kingside_castle_black():
    '''make sure simple kingside castle works'''
    fen = 'r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1'
    b = Board(fen=fen)
    move = Move('KING',core.Color.BLACK,ss.SQUARES[60],ss.SQUARES[62],'castle')
    assert is_move_legal(move,b.get_legal_moves(move.piece_color))

def test_simple_kingside_castle_boardstate_black():
    '''verify that simple kingside castle results in proper boardstate'''
    in_fen = 'r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1'
    out_fen = 'r4rk1/8/8/8/8/8/8/R3K2R w KQ - 1 2'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('KING',core.Color.BLACK,ss.SQUARES[60],ss.SQUARES[62],'castle')
    legal_moves = in_board.get_legal_moves(core.Color.BLACK)
    board = get_board_matching_move(move,legal_moves)
    assert board == out_board

def test_simple_queenside_castle_black():
    '''make sure simple queenside castle works'''
    fen = 'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1'
    b = Board(fen=fen)
    move = Move('KING',core.Color.BLACK,ss.SQUARES[60],ss.SQUARES[58],'castle')
    assert is_move_legal(move,b.get_legal_moves(move.piece_color))

def test_simple_queenside_castle_boardstate_black():
    '''verify that simple queenside castle results in proper boardstate'''
    in_fen = 'r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1'
    out_fen = '2kr3r/8/8/8/8/8/8/R3K2R w KQ - 1 2'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('KING',core.Color.BLACK,ss.SQUARES[60],ss.SQUARES[58],'castle')
    legal_moves = in_board.get_legal_moves(core.Color.BLACK)
    board = get_board_matching_move(move,legal_moves)
    assert board == out_board

def test_castling_squares_under_attack():
    '''kingside castling should be unavailable due to the F1 square being under
    attack'''
    fen = '4k3/8/8/8/8/8/6p1/4K2R w K - 0 1'
    b = Board(fen=fen)
    move = Move('KING',core.Color.WHITE,ss.SQUARES[4],ss.SQUARES[6],'castle')
    legal_moves = b.get_legal_moves(core.Color.WHITE)
    assert not(is_move_legal(move,b.get_legal_moves(move.piece_color)))

def test_castling_squares_enemy_occupied():
    '''
    kingside castling is unavailable because the F8 square has a knight on it
    '''
    fen = '4kN1r/8/8/8/8/8/8/4K3 b k - 0 1'
    b= Board(fen=fen)
    move = Move('KING',core.Color.BLACK,ss.SQUARES[60],ss.SQUARES[62],'castle')
    legal_moves = b.get_legal_moves(core.Color.BLACK)
    assert not(is_move_legal(move,b.get_legal_moves(move.piece_color)))

def test_castling_squares_friendly_occupied():
    '''
    kingside castling is unavailable because the castling squares are occupied
    '''
    fen = '4kb1r/8/8/8/8/8/8/4K3 b k - 0 1'
    b = Board(fen=fen)
    move = Move('KING',core.Color.BLACK,ss.SQUARES[60],ss.SQUARES[62],'castle')
    legal_moves = b.get_legal_moves(core.Color.BLACK)
    assert not(is_move_legal(move,b.get_legal_moves(move.piece_color)))
