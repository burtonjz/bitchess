import pytest
from bitchess import core, squareset as ss
from bitchess.board import Board
from bitchess.move import Move


def all_squaresets_equal(b1,b2):
    for k in b1.squaresets.keys():
        if b1.squaresets[k] != b2.squaresets[k]:
            ss.print_squareset(b1.squaresets[k])
            ss.print_squareset(b2.squaresets[k])
            return False, f'squareset {k} does not match'
    return True, ''


def test_place_piece_at():
    '''place Queen on A1'''
    in_fen = '4k3/8/8/8/8/8/8/4K3 w - - 0 1'
    out_fen = '4k3/8/8/8/8/8/8/Q3K3 w - - 0 1'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    in_board.place_piece_at(ss.SQUARES[0],'QUEEN',core.Color.WHITE)
    assert all_squaresets_equal(in_board,out_board)

def test_remove_piece_at():
    '''remove Queen from A1'''
    in_fen = '4k3/8/8/8/8/8/8/Q3K3 w - - 0 1'
    out_fen = '4k3/8/8/8/8/8/8/4K3 w - - 0 1'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    in_board.remove_piece_at(ss.SQUARES[0])
    assert all_squaresets_equal(in_board,out_board)

def test_place_piece_at_overwrite():
    '''replace black rook on A1 with white queen on A1'''
    in_fen = '4k3/8/8/8/8/8/8/r3K3 w - - 0 1'
    out_fen = '4k3/8/8/8/8/8/8/Q3K3 w - - 0 1'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    in_board.place_piece_at(ss.SQUARES[0],'QUEEN',core.Color.WHITE)
    assert all_squaresets_equal(in_board,out_board)

def test_basic_quiet_move():
    '''quiet move Ra1 -> Ra4'''
    in_fen = '4k3/8/8/8/8/8/8/R3K3 w - - 0 1'
    out_fen =  '4k3/8/8/8/8/8/8/3RK3 b - - 1 1'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('ROOK',core.Color.WHITE,ss.SQUARES[0],ss.SQUARES[3],'quiet')
    in_board.make_move(move)
    squaretest = all_squaresets_equal(in_board,out_board)
    assert squaretest[0],squaretest[1]

def test_basic_attack_move():
    '''attack move Ra1xa4'''
    in_fen = '4k3/8/8/8/8/8/8/R2qK3 w Q - 0 1'
    out_fen = '4k3/8/8/8/8/8/8/3RK3 b - - 0 1'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('ROOK',core.Color.WHITE,ss.SQUARES[0],ss.SQUARES[3],'attack')
    in_board.make_move(move)
    squaretest = all_squaresets_equal(in_board,out_board)
    assert squaretest[0],squaretest[1]

def test_en_passant_attack_white():
    '''white en passant capture on e6 (pawn on e5 removed)'''
    in_fen = '4k3/8/8/3Pp3/8/8/8/4K3 w - e6 0 2'
    out_fen = '4k3/8/4P3/8/8/8/8/4K3 b - - 0 2'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[35],ss.SQUARES[44],'attack')
    in_board.make_move(move)
    squaretest = all_squaresets_equal(in_board,out_board)
    assert squaretest[0],squaretest[1]

def test_en_passant_attack_black():
    '''white en passant capture on e3 (pawn on e4 removed)'''
    in_fen = '4k3/8/8/8/3pP3/8/8/4K3 b - e3 0 2'
    out_fen = '4k3/8/8/8/8/4p3/8/4K3 w - - 0 3'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('PAWN',core.Color.BLACK,ss.SQUARES[27],ss.SQUARES[20],'attack')
    in_board.make_move(move)
    squaretest = all_squaresets_equal(in_board,out_board)
    ss.print_squareset(in_board.squaresets['PAWN'])
    ss.print_squareset(out_board.squaresets['PAWN'])
    assert squaretest[0],squaretest[1]

def test_promotion_to_queen():
    '''white promotes to queen on d8'''
    in_fen = '7k/3P4/8/8/8/8/8/4K3 w - - 0 3'
    out_fen = '3Q3k/8/8/8/8/8/8/4K3 b - - 0 3'
    in_board = Board(fen=in_fen)
    out_board = Board(fen=out_fen)
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[51],ss.SQUARES[59],'quiet','QUEEN')
    in_board.make_move(move)
    squaretest = all_squaresets_equal(in_board,out_board)
    ss.print_squareset(in_board.squaresets['QUEEN'])
    ss.print_squareset(out_board.squaresets['QUEEN'])
    assert squaretest[0],squaretest[1]
