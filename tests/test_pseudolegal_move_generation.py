import pytest
from bitchess import core, squareset as ss
from bitchess.board import Board
from bitchess.move import Move

def move_in_list(target_move,moves):
    for m in moves:
        if target_move == m:
            return True
    return False

def test_simple_pseudolegal_pawn_push_white():
    '''pawn on d2 can push to d3'''
    fen = '4k2r/8/8/8/8/8/3P4/4K3 w k - 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[11],ss.SQUARES[19],'quiet')
    assert move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))

def test_simple_pseudolegal_double_pawn_push_white():
    '''pawn on d2 can push to d4'''
    fen = '4k2r/8/8/8/8/8/3P4/4K3 w k - 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[11],ss.SQUARES[27],'quiet')
    assert move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))

def test_simple_pseudolegal_pawn_push_black():
    '''pawn on e7 can push to e6'''
    fen = '4k2r/4p3/8/8/8/8/3P4/4K3 w k - 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.BLACK,ss.SQUARES[52],ss.SQUARES[44],'quiet')
    assert move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK))

def test_simple_pseudolegal_double_pawn_push_black():
    '''pawn on e7 can push to e5'''
    fen = '4k2r/4p3/8/8/8/8/3P4/4K3 w k - 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.BLACK,ss.SQUARES[52],ss.SQUARES[36],'quiet')
    assert move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK))

def test_simple_pseudolegal_pawn_cant_push_white():
    '''king is behind pawn'''
    fen = '4k2r/4P3/8/8/8/8/8/4K3 w k - 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[52],ss.SQUARES[60],'quiet')
    assert not(move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE)))

def test_simple_pseudolegal_pawn_cant_push_black():
    '''king is behind pawn'''
    fen = '4k2r/8/8/8/8/8/4p3/4K3 w k - 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.BLACK,ss.SQUARES[12],ss.SQUARES[4],'quiet')
    assert not(move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK)))

def test_simple_pseudolegal_pawn_attacks_white():
    '''can attack northwest, cant attack northeast'''
    errors = []
    fen = '4k2r/8/8/8/8/3b1B2/4P3/4K3 w k - 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[12],ss.SQUARES[19],'attack')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))):
        errors.append('no northwest attack')
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[12],ss.SQUARES[21],'attack')
    if move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE)):
        errors.append('invalid northeast attack')
    assert not errors, '\n'+'\n'.join(errors)

def test_simple_pseudolegal_pawn_attacks_black():
    '''cant attack southwest, can attack southeast'''
    errors = []
    fen = '4k3/4p3/3b1B2/8/8/5B2/4P3/4K3 b - - 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.BLACK,ss.SQUARES[52],ss.SQUARES[45],'attack')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK))):
        errors.append('no southeast attack')
    move = Move('PAWN',core.Color.BLACK,ss.SQUARES[52],ss.SQUARES[43],'attack')
    if move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK)):
        errors.append('invalid southwest attack')
    assert not errors, '\n'+'\n'.join(errors)

def test_enpassant_pseudolegal_pawn_attack_white():
    '''white enpassant take on e6'''
    fen = '4k3/8/8/3Pp3/8/8/8/4K3 w - e6 0 2'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.WHITE,ss.SQUARES[35],ss.SQUARES[44],'attack')
    assert move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))

def test_enpassant_pseudolegal_pawn_attack_black():
    '''white enpassant take on e6'''
    fen = '4k3/8/8/8/3pP3/8/8/4K3 b - e3 0 1'
    b = Board(fen=fen)
    move = Move('PAWN',core.Color.BLACK,ss.SQUARES[27],ss.SQUARES[20],'attack')
    assert move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK))

def test_knight_pseudolegal_moves():
    '''knight takes bishop on h3, can't move to other occupied positions'''
    errors = []
    fen = 'r2k4/p7/8/8/8/6b1/5K2/7N w - - 0 1'
    b = Board(fen=fen)
    move = Move('KNIGHT',core.Color.WHITE,ss.SQUARES[7],ss.SQUARES[22],'attack')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))):
        errors.append('Knight capture not present')
    move = Move('KNIGHT',core.Color.WHITE,ss.SQUARES[7],ss.SQUARES[13],'attack')
    if move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE)):
        errors.append('Knight invalid attack on own king')
    assert not errors, '\n'+'\n'.join(errors)

def test_bishop_pseudolegal_moves():
    '''bishop to h2, can't move to other occupied positions'''
    errors = []
    fen = 'r2k4/p7/8/8/8/8/5K2/6B1 w - - 0 1'
    b = Board(fen=fen)
    move = Move('BISHOP',core.Color.WHITE,ss.SQUARES[6],ss.SQUARES[15],'quiet')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))):
        errors.append('Bishop move not present')
    move = Move('BISHOP',core.Color.WHITE,ss.SQUARES[6],ss.SQUARES[13],'attack')
    if move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE)):
        errors.append('Bishop invalid attack on own king')
    assert not errors, '\n'+'\n'.join(errors)

def test_rook_pseudolegal_moves():
    '''rook to b7,a7, can't move to c8'''
    errors = []
    fen = 'r1k5/8/p7/8/8/8/5K2/8 b - - 0 1'
    b = Board(fen=fen)
    move = Move('ROOK',core.Color.BLACK,ss.SQUARES[56],ss.SQUARES[57],'quiet')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK))):
        errors.append('Rb8 not present')
    move = Move('ROOK',core.Color.BLACK,ss.SQUARES[56],ss.SQUARES[48],'quiet')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK))):
        errors.append('Ra7 not present')
    move = Move('ROOK',core.Color.BLACK,ss.SQUARES[56],ss.SQUARES[58],'attack')
    if move_in_list(move,b.get_pseudolegal_moves(core.Color.BLACK)):
        errors.append('Rc8 is invalid')
    assert not errors, '\n'+'\n'.join(errors)

def test_king_pseudolegal_moves():
    '''all moves from h1 corner are pseudolegal'''
    errors = []
    fen = '8/8/8/8/8/8/5k1p/7K w - - 0 1'
    b = Board(fen=fen)
    move = Move('KING',core.Color.WHITE,ss.SQUARES[7],ss.SQUARES[6],'quiet')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))):
        errors.append('Kg1 not present')
    move = Move('KING',core.Color.WHITE,ss.SQUARES[7],ss.SQUARES[15],'attack')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))):
        errors.append('Kxh2 not present')
    move = Move('KING',core.Color.WHITE,ss.SQUARES[7],ss.SQUARES[14],'quiet')
    if not(move_in_list(move,b.get_pseudolegal_moves(core.Color.WHITE))):
        errors.append('Kg2 not present')
    assert not errors, '\n'+'\n'.join(errors)
