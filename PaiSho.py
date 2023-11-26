import math

class Square:
    def __init__(self, piece='NA', type='N'):
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
        self.piece = piece
    
    def stats(self):
        if not self.type == 'NA':
            return self.piece
        else:
            return self.type

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
                        self.board[i][j].type = 'W'
                    if(ycord*xcord > 0):
                        self.board[i][j].type = "R"
                #Sets the unplayable region
                elif((abs(ycord)+abs(xcord))>(self.radius+math.floor(self.radius/2))):
                    self.board[i][j].type = 'B'                    

        self.board[self.radius][0].type = 'G'
        self.board[0][self.radius].type = 'G'
        self.board[self.radius][self.radius*2].type = 'G'
        self.board[self.radius*2][self.radius].type = 'G'
        
        

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        output = ""
        for i in range(self.radius*2+1):
            for j in range(self.radius*2+1):
                output += "["+self.board[j][i].type+"]"
            output += "\n"
        print(output)
        
game = PaiSho()
game.display_board()

# Example of setting specific values:
game.board[5][1].type = "#"
game.display_board()
