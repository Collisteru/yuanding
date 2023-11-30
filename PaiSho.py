import math
import square
import piece
from colorama import just_fix_windows_console
from termcolor import colored
        
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
        self.game_over = 0
        self.round = 1

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

    # Move piece from one coordinate to another
    def move(self, oldx, oldy, newx, newy):
        # Check that there's a piece on (oldx, oldy)
        piece = self.board[self.radius+oldx][self.radius-oldy].piece # This will raise an exception if there's no piece
        owner = piece.owner

        # Check that the new square is within the range of the piece
        piecerange = int(piece.type)
        accessible = (abs(newx-oldx) + abs(newy-oldy) <= piecerange)
        if not accessible: raise Exception("Out of range")

        # Remove the piece from the old square and add it to the new square
        self.remove(oldx,oldy)
        self.add(newx, newy, owner)

        
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
                    if(not smallestAbove[0] == None):
                        j[2].harmonize(smallestAbove[0])

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
                    if(not smallestAbove[0] == None):
                        j[2].harmonize(smallestAbove[0])

    # Prints a list of which gates are open
    # And returns a dictionary of which gates are open (key value = 1)
    def check_open_gates(self):
        up_open = not self.board[self.radius][0].occupied()
        down_open = not self.board[self.radius][2 * self.radius].occupied()

        left_open = not self.board[0][self.radius].occupied()
        right_open = not self.board[2 * self.radius][self.radius].occupied()

        if not (up_open or down_open or left_open or right_open):
            print("There are no open gates.")
            return 0
    
        up_string = "Up" if up_open else ""
        down_string = "Down" if down_open else ""
        left_string = "Left" if left_open else "" 
        right_string = "Right" if right_open else ""
    
        print("The following gates are open: {0} {1} {2} {3}".format(up_string, right_string, down_string, left_string))
        return {"Up": up_open, "Right": right_open, "Down": down_open, "Left": left_open}

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        output = ""
        for i in range(self.radius*2+1):
            for j in range(self.radius*2+1):
                square_type = self.board[j][i].type
                squarestring = ""
                if square_type == "G":
                    color = 'red'
                elif square_type == "W":
                    color = 'white'
                elif square_type == "R":
                    color = 'red'
                else:
                    color = 'grey'

                if square_type == "B":
                    squarestring = "   "
                else:
                    squarestring = colored("[ ]", color)
                
                if self.board[j][i].piece != None:
                    piece = self.board[j][i].piece
                    piece_owner = piece.owner
                    piece_type = piece.type
                    if piece.owner == "P1":
                        piece_color = 'red'
                    else:
                        piece_color = 'white'
                    piece_string = colored(piece_type, piece_color)
                    
                    squarestring = colored("[", color) + piece_string + colored("]", color)
                output += squarestring
            output += "\n"
        print(output)

    def take_turn(self, player):
        

        # Input loop
        while True:
            player_string = "Host" if player else "Guest"
            # Ask the player what they want to do
            input_string = input("Round {1}: It's your turn, {0}. Do you want to Plant or Arrange? Press P to Plant, A to arrange. \n".format(player_string, self.round))

            if (input_string == 'p' or input_string == 'P'):
                move_type = 'P'
            elif (input_string == 'a' or input_string == 'A'):
                move_type = 'A'
            else:
                print("Unrecognized input format, try again.")
                continue

            # Process Planting
            if (move_type == 'P'):
                open_gates = self.check_open_gates()
                if open_gates:
                    chosen_gate = input("Choose which gate you want to plant at. Type U, R, D, or L. These mean Up, Right, Down, and Left respectively. \n")
                    
                    if (chosen_gate == "U" or chosen_gate == "u"):
                        if open_gates["Up"]:
                            self.add(0, self.radius, player)
                            break
                        else:
                            print("The upper gate already has a piece in it.")
                            continue
                    elif (chosen_gate == "D" or chosen_gate == "d"):
                        if open_gates["Down"]:
                            self.add(0, -self.radius, player)
                            break
                        else:
                            print("The lower gate already has a piece in it.")
                            continue
                    elif (chosen_gate == "R" or chosen_gate == "r"):
                        if open_gates["Right"]:
                            self.add(self.radius, 0, player)
                            break
                        else:
                            print("The right gate already has a piece in it.")
                            continue
                    elif (chosen_gate == "L" or chosen_gate == "l"):
                        if open_gates["Left"]:
                            self.add(-self.radius, 0, player)
                            break
                        else:
                            print("The left gate already has a piece in it.")
                            continue
                    else:
                        print("Unrecognized input! Try again.\n")
                        continue
                    
                else:
                    print("There aren't any open gates! Try arranging.")
                    continue
            
            if (move_type == 'A'):


                oldx = input("Type in the first coordinate (x value) of the piece you want to move. \n")                

                oldy = input("Type in the second coordinate (y value) of the piece you want to move.\n")

                newx = input("Type in the first corrdinate (x value) of the new poistion you want your piece to be in. \n")
        
                newy = input("Type in the second coordinate (y value) of the new position your piece to be in. \n")

                try:
                    int(oldx) ; int(oldy) ; int(newx) ; int(newy)
                except:
                    print("One of your coordinate inputs isn't an integer!")
                    continue

                # The Move function should handle the remaining edge cases
                self.move(int(oldx), int(oldy), int(newx), int(newy))
                break

        # Display the results of the action
        print("Turn played successfully.")
        self.display_board()

    # Check whether the current state of the board fulfills the win condition
    # If it does, set self.game_over to 1
    # TODO: Implement this
    def check_win_condition(self):    
        self.game_over = 0
        pass

    # Start a game of Skud Pai Sho
    def play(self):
        print("Come in and have a cup of tea. Let's play a relaxing game of Skud Pai Sho.")
        
        # The Host plays with light tiles and the Guest plays with dark tiles. The Guest plays first.
        # Internally we represent the Guest as 0 and the Host as 1

        self.display_board()
        curr_player = 0
        while not self.game_over:
            self.take_turn(curr_player)
            
            self.check_win_condition()

            if curr_player == 1:
                self.round += 1

            curr_player = (curr_player + 1) % 2

        sys.exit()