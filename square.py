
import piece

class Square:
    def __init__(self, owner='NA', type='_'):
        """
        Type can be one of the following:
        B = Blank:   These are unplayable regions
        N = Neutral: These are regions any piece can be in
        R = Red:     White pieces can't be in this region
        W = White:   Red pieces can't be in this region
        """
        self.type = type

        """
        These are yet to be implemented, but they would represent
        which flower piece is currently on the piece.
        Type can be one of the following:
        P1 - Player 1's piece
        P2 - Player 2's piece
        NA - No piece
        """
        if(owner != 'NA'):
            self.piece = piece.Piece(owner)
        else:
            self.piece = None
    
    # Removes a piece from this square
    def remove(self):
        if self.occupied():
            self.piece.disharmonize()
            self.piece = None
        else:
            raise Exception("There is no piece to remove")

    # Adds a piece to this square
    def add(self, owner):
        if not self.occupied():
            self.piece = piece.Piece(owner)
            return self.piece
        else:
            raise Exception("This space already has a piece")
        
    # Return if this square has a piece
    def occupied(self):
        return not self.piece == None
    
    # Returns the piece that is on this square
    def piece(self):
        if self.occupied:
            return self.piece
        else: raise Exception("There is no piece on this square.")

    # Returns printable info
    def stats(self):
        if self.occupied():
            return self.piece.type
        else:
            return self.type
