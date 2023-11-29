import math
import square
import piece

        
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
        self.diameter = 2*radius + 1
        self.board = [[square.Square() for i in range(self.diameter)] for j in range(self.diameter)] 
        self.players = 2
        self.current_player = 1
        self.placed = [] # Stores placed pieces as [(x,y,piece)]
        self.moves = []

        for i in range(self.diameter):        
            xcord = self.radius-i
            for j in range(self.diameter):
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

    # Add a piece to the associated pai sho coordinate
    def add(self, x, y, owner):
        self.placed.append((x,y,self.board[self.radius+x][self.radius-y].add(owner)))
        self.checkHarmonies()
                
    # Remove a piece from the associated pai sho coordinate
    def remove(self, x, y):
        self.board[self.radius+x][self.radius-y].remove()
        self.checkHarmonies()

    # Check the board state for any new harmonies and removed harmonies
    def checkHarmonies(self):

        for j in self.placed:
            j[2].disharmonize()

        vertical = []
        for i in range(self.diameter):
            vertical.append([])
            for j in self.placed:
                if self.radius+j[0] == i:
                    vertical[i].append(j)
        
        horizontal = []
        for i in range(self.diameter):
            horizontal.append([])
            for j in self.placed:
                if j[1]+self.radius == i:
                    horizontal[i].append(j)
        
        # print(vertical)
        # print(horizontal)

        for i in vertical:
            if not i == []:
                for j in i:
                    smallestAbove = (None,self.diameter)
                    smallestBelow = (None,self.diameter)
                    for k in i:
                        diff = j[1]-k[1]
                        if diff > 0:
                            if diff < smallestBelow[1]:
                                smallestBelow = (k[2],diff)
                        elif diff < 0:
                            if abs(diff) < smallestAbove[1]:
                                smallestAbove = [k[2],abs(diff)]
                    if(not smallestBelow[0] == None):
                        j[2].harmonize(smallestBelow[0])
                        print(j[2].harmonized)
                    if(not smallestAbove[0] == None):
                        j[2].harmonize(smallestAbove[0])
                        print(j[2].harmonized)

        for i in horizontal:
            if not i == []:
                for j in i:
                    smallestAbove = (None,self.diameter)
                    smallestBelow = (None,self.diameter)
                    for k in i:
                        diff = j[1]-k[1]
                        if diff > 0:
                            if diff < smallestBelow[1]:
                                smallestBelow = (k[2],diff)
                        elif diff < 0:
                            if abs(diff) < smallestAbove[1]:
                                smallestAbove = [k[2],abs(diff)]
                    if(not smallestBelow[0] == None):
                        j[2].harmonize(smallestBelow[0])
                        print(j[2].harmonized)
                    if(not smallestAbove[0] == None):
                        j[2].harmonize(smallestAbove[0])
                        print(j[2].harmonized)

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        output = ""
        for i in range(self.radius*2+1):
            for j in range(self.radius*2+1):
                output += "["+self.board[j][i].stats()+"]"
            output += "\n"
        print(output)