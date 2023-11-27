import math

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
            self.piece = Piece(owner)
        else:
            self.piece = None
    
    # Removes a piece from this square
    def remove(self):
        if self.occupied():
            self.piece.disconnect()
            self.piece = None
        else:
            raise Exception("There is no piece to remove")

    # Adds a piece to this square
    def add(self, owner):
        if not self.occupied():
            self.piece = Piece(owner)
        else:
            raise Exception("This space already has a piece")
        
    # Return if this square has a piece
    def occupied(self):
        return not self.piece == None

    # Returns printable info
    def stats(self):
        if self.occupied():
            return self.piece.type
        else:
            return self.type

class Piece:
    def __init__(self, owner):
        self.type = "3"
        self.owner = owner
        self.connected = [] # List of harmonizing pieces

    # Remove all harmonies attached to this piece
    def disconnect(self):
        for piece in self.connected:
            piece.connected.remove(self)    

    # Harmonize the current piece with another piece
    def connect(self, piece):
        self.piece.connected.append(piece)
        
class PaiSho:
    def __init__(self, radius=7):
        """
        The constructor for the PaiSho class defines several instance variables:

        radius: This variable stores the radius of the board.
        board: This data structure is responsible for managing the PaiSho board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        """

        self.radius = radius
        self.board = [[Square() for i in range(self.radius*2+1)] for j in range(self.radius*2+1)] 
        self.players = 2
        self.current_player = 1
        self.moves = []

        for i in range(self.radius*2+1):        
            xcord = self.radius-i
            for j in range(self.radius*2+1):
                ycord = j-self.radius
                
                #Sets the non-neutral region
                if((abs(ycord)+abs(xcord))<(self.radius-1)):
                    if(ycord*xcord < 0):
                        # Set White Region
                        self.board[i][j].type = '='
                    if(ycord*xcord > 0):
                        # Set Red Region
                        self.board[i][j].type = "+"
                #Sets the unplayable region
                elif((abs(ycord)+abs(xcord))>(self.radius+math.floor(self.radius/2))):
                    self.board[i][j].type = 'X'                    

        self.board[self.radius][0].type = 'G'
        self.board[0][self.radius].type = 'G'
        self.board[self.radius][self.radius*2].type = 'G'
        self.board[self.radius*2][self.radius].type = 'G'

    # Add a piece to the associated pai sho coordinate
    def add(self, x, y, owner):
        self.board[self.radius+x][self.radius-y].add(owner)
        
    # Remove a piece from the associated pai sho coordinate
    def remove(self, x, y):
        self.board[self.radius+x][self.radius-y].remove()

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        output = ""
        for i in range(self.radius*2+1):
            for j in range(self.radius*2+1):
                square = self.board[i][j]
                if square.type == 'X':
                    # Handle possibility of an empty tile.
                    output += "   "
                else:
                    output += "["+square.stats()+"]"
            output += "\n"
        print(output)
        
game = PaiSho()
game.display_board()

# Example of setting specific values:
game.add(2,1,"P1")
game.display_board()

# Example of setting specific values:
game.remove(2,1)
game.display_board()
