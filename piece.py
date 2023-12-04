class Piece:
    def __init__(self, owner, x, y):
        self.x = x
        self.y = y
        self.type = "3"
        self.owner = owner #will be either 0 (guest) or 1 (host)
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

    def __repr__(self):
        return(f'{self.owner}: ({self.x}, {self.y})')