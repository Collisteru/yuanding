class Piece:
    def __init__(self, owner):
        self.type = "3"
        self.owner = owner
        self.harmonized = [] # List of harmonizing pieces

    # Remove all harmonies attached to this piece
    def disharmonize(self):
        for piece in self.harmonized:
            try:
                piece.harmonized.remove(self)   
            except: pass
        self.harmonized = [] 

    # Harmonize the current piece with another piece
    def harmonize(self, piece):
        self.harmonized.append(piece)