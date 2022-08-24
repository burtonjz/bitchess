class InvalidSquareSetError(Exception):
    '''square set is wrong length or datatype'''

class InvalidAlgebraicNotationError(Exception):
    '''algebraic notation is not formatted properly (e.g., "e4")'''

class InvalidIndexError(Exception):
    '''square set index must be between 0 and 63'''
    def __str__(self):
        return 'Squareset index must be between 0 and 63'

class IllegalMoveError(Exception):
    '''requested move is illegal'''

class AmbiguousMoveError(Exception):
    '''ambiguous move string (matches more than one viable move)'''

class NoValidMoveError(Exception):
    '''no valid moves. Used to get stalemate/checkmate'''
