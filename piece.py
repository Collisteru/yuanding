class Piece:
    def __init__(self, owner):
        self.type = "3"
        self.owner = owner
        self.harmonized = [] # List of harmonizing pieces

    # Remove all harmonies attached to this piece
    def disharmonize(self):
        for piece in self.harmonized:
            piece.harmonized.remove(self)    

    # Harmonize the current piece with another piece
    def harmonize(self, piece):
        self.piece.harmonized.append(piece)