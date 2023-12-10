
import piece

class Square:
    def __init__(self, x, y, owner='NA', type='_',):
        """
        Type can be one of the following:
        B = Blank:   These are unplayable regions
        N = Neutral: These are regions any piece can be in
        R = Red:     White pieces can't be in this region
        W = White:   Red pieces can't be in this region
        """
        self.type = type

        # The coordinates of the square
        self.x = x
        self.y = y
        
        # Indicates whether there is a harmony going across this square
        # -1 is the default and means no
        # 0 means there is a horizontal harmony from the Guest (Player 0)
        # 1 means there is a horizontal harmony from the Host (Player 1)
        # 2 means there is a vertical harmony from the Guest
        # 3 means there is a vertical harmony from the Host

        self.harmony = -1
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
    def add(self, owner, x, y):
        if not self.occupied():
            self.piece = piece.Piece(owner, x, y)
            return self.piece
        else:
            raise Exception("This space already has a piece")
        
    # Return if this square has a piece
    def occupied(self):
        return not (self.piece == None)
    
    # Returns the piece that is on this square
    def piece(self):
        if self.occupied:
            return self.piece
        else: 
            return 0
