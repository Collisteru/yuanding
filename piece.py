class Piece:
    def __init__(self, owner):
        self.type = "3"
        self.owner = owner
        self.connected = [] # List of harmonizing pieces

    # Remove all harmonies attached to this piece
    def disharmonize(self):
        for piece in self.connected:
            piece.connected.remove(self)    

    # Harmonize the current piece with another piece
    def harmonize(self, piece):
        self.piece.connected.append(piece)