import math
import square
import piece
from colorama import just_fix_windows_console
from termcolor import colored
from termcolor import cprint
import sys

from exceptions import MoveException

    
class PaiSho:
    def __init__(self, radius):
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
        self.current_player = 0
        self.placed = [] # Stores placed pieces
        self.moves = []
        self.game_over = 0
        self.round = 1
        self.winner = -1 # This usage mans that the host is by default the winner. Make sure to change this!

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

    # returns a square of the board based on the given x and y value seen by the player
    def get_square(self, x: int, y: int):
        return self.board[self.radius+x][self.radius-y]
    
    # Add a piece to the associated pai sho coordinate
    def add(self, x, y, owner):
        self.placed.append(self.board[self.radius+x][self.radius-y].add(owner,x,y))
        self.checkHarmonies()
                
    # Remove a piece from the associated pai sho coordinate
    def remove(self, x, y):
        for i in self.placed:
            if i.x == x and i.y == y:
                self.placed.remove(i)
        self.board[self.radius+x][self.radius-y].remove()
        self.checkHarmonies()

    # Move piece from one coordinate to another
    def move(self, oldx, oldy, newx, newy):

        old_square = self.board[self.radius+oldx][self.radius-oldy]
        new_square = self.board[self.radius+newx][self.radius-newy]

        # Check that there's a piece on (oldx, oldy)
        if not old_square.occupied(): raise MoveException("That square doesn't have a piece on it!")
        else: owner = old_square.piece.owner

        # Check that the piece belongs to the current player
        print("Owner: ", owner)
        print("self.current_player: ", self.current_player)
        if not (owner == self.current_player): raise MoveException("That's not your piece to move!")

        # Check that the new square is within the range of the piece
        piecerange = int(old_square.piece.type)
        accessible = (abs(newx-oldx) + abs(newy-oldy) <= piecerange)
        if not accessible: raise MoveException("Out of range")

        # Check if the new square is occupied
        occupied = new_square.occupied()
        if occupied:
            # If the owner of the piece that's moving in is the same
            # as the owner of the piece that's already there:
            if new_square.piece.owner == owner:
                raise MoveException("Occupied by another one of your pieces!")
            else:
                # A capture occurs
                self.remove(newx,newy)
                self.add(newx,newy, owner)
                self.remove(oldx,oldy)
                return


        # Remove the piece from the old square and add it to the new square
        self.remove(oldx,oldy)
        self.add(newx, newy, owner)
        return
        
    # Check the board state for any new harmonies and removed harmonies
    # Update whether every square on the board should have a harmony on it
    def checkHarmonies(self):

        for j in self.placed:
            j.disharmonize()

        # Have a list of lists that have all pieces on a specific x= line
        vertical = []
        for i in range(self.diameter):
            vertical.append([])
            for j in self.placed:
                if self.radius+j.x == i:
                    vertical[i].append(j)
        
        # Have a list of lists that have all pieces on a specific y = line
        horizontal = []
        for i in range(self.diameter):
            horizontal.append([])
            for j in self.placed:
                if self.radius+j.y == i:
                    horizontal[i].append(j)

        # Harmonize along verticals
        for i in vertical:
            if not i == []:
                for j in i:
                    smallestAbove = (None,self.diameter)
                    smallestBelow = (None,self.diameter)
                    for k in i:
                        diff = j.y-k.y
                        if diff > 0:
                            if diff < smallestBelow[1]:
                                smallestBelow = (k,diff)
                        elif diff < 0:
                            if abs(diff) < smallestAbove[1]:
                                smallestAbove = [k,abs(diff)]
                    toTop = smallestAbove[0]
                    toBot = smallestBelow[0]
                    if(not toBot == None):
                        if toBot.owner == j.owner:
                            j.harmonize(toBot)
                    if(not toTop == None):
                        if toTop.owner == j.owner:
                            j.harmonize(toTop)

        # Harmonize along horizontals
        for i in horizontal:
            if not i == []:
                for j in i:
                    smallestRight = (None,self.diameter)
                    smallestLeft = (None,self.diameter)
                    for k in i:
                        diff = j.x-k.x
                        if diff > 0:
                            if diff < smallestLeft[1]:
                                smallestLeft = (k,diff)
                        elif diff < 0:
                            if abs(diff) < smallestRight[1]:
                                smallestRight = [k,abs(diff)]
                    toRight = smallestLeft[0]
                    toLeft = smallestRight[0]
                    if(not toLeft == None):
                        if toLeft.owner == j.owner:
                            j.harmonize(toLeft)
                    if(not toRight == None):
                        if toRight.owner == j.owner:
                            j.harmonize(toRight)
        self.update_square_harmonies()


    # Updates the self.harmony value of every square on the board.
    def update_square_harmonies(self):
        harmony_chains = []
        for i in self.placed:
            for j in i.harmonized:
                newPair = (i,j)
                if not (j,i) in harmony_chains:
                    harmony_chains.append(newPair)
        
        # Update the tiles on the board for each harmony chain
        harmonized_squares = set()
        for i in harmony_chains:
            pieceOne = i[0]
            pieceTwo = i[1]

            # Get the piece's owner (they should both be owned by the same person)
            owner = pieceOne.owner
        
            firstx = pieceOne.x
            secondx = pieceTwo.x

            firsty = pieceOne.y
            secondy = pieceTwo.y

    	    # Vertical Harmony
            if firstx == secondx:
                # We must update the tiles that are in the correct row and between the two harmonizing tiles
                # Generate the range of y values
                if firsty < secondy:
                    y_range = list(range(firsty + 1, secondy))
                else:
                    y_range = list(range(secondy + 1, firsty))

                for y in y_range:

                    # If the guest owns this harmony, label this as a vertical guest harmony
                    if owner == 0:
                        self.get_square(firstx, y).harmony = 2
                    else: # Otherwise, label this as a vertical host harmony
                        self.get_square(firstx, y).harmony = 3

                    harmonized_squares.add(self.get_square(firstx,y))
    
            # Horizontal Harmony
            if firsty == secondy:
                # We must update the tiles that are in the correct column and between the two harmonizing tiles
                # Generate the range of x values
                if firstx < secondx:
                    x_range = list(range(firstx + 1, secondx))
                else:
                    x_range = list(range(secondx + 1, firstx))

                for x in x_range:

                    # If the guest owns this harmony, label this as a horizontal guest harmony
                    if owner == 0:
                        self.get_square(x, firsty).harmony = 0
                    else: # Otherwise, label this as a horizontal host harmony
                        self.get_square(x, firsty).harmony = 1

                    harmonized_squares.add(self.get_square(x,firsty))
        
        # Deharmonize all other squares
        # For all squares, if they're not among the harmonized squares, deharmonize them
        # This keeps the marks on the board from lingering after hte harmonies that made them have been broken
        for row in self.board:
            for square in row:
                if square not in harmonized_squares:
                    # Deharmonize this specific square
                    square.harmony = -1

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
        emDash = u'\u2014'
        output = ""

        # Generate alignment gridline
        gridline =  [i for i in range(-self.radius, self.radius + 1)]
        x_gridline = ""

        # Print the x gridline
        x_gridline += "   " # Offset the x gridline to make room for the y gridline
        x_gridline = x_gridline
        for i in gridline:
                if i < 0:
                    x_gridline += colored("{0} ".format(i), 'blue')
                else:
                    x_gridline += colored(" {0} ".format(i), 'blue')

        y_gridline = gridline[::-1]
        # Render the spaces
        for i in range(self.radius*2+1):
            # Render an entry in the y gridline
            if y_gridline[i] < 0:
                output += colored("{0} ".format(y_gridline[i]), 'blue')
            else:
                output += colored(" {0} ".format(y_gridline[i]), 'blue')

            # Render each line of spaces
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
                
                # Add piece if one should be added
                if self.board[j][i].piece != None:
                    piece = self.board[j][i].piece
                    piece_owner = piece.owner
                    piece_type = piece.type
                    if piece.owner == 0:
                        # The Guest has dark pieces
                        piece_string = colored(piece_type, 'yellow', 'on_grey', attrs=['blink'])
                    else:
                        # The Host has light pieces
                        piece_string = colored(piece_type, 'black', 'on_white', attrs=['blink', 'bold'])
                    
                    squarestring = colored("[", color) + piece_string + colored("]", color)
                # Add a harmony if one should be added
                elif self.board[j][i].harmony != -1:
                    harmony = self.board[j][i].harmony
                    if harmony == 0:
                        # Horizontal Guest Harmony
                        harmony_string = colored('{0}'.format(emDash), 'yellow')
                    elif harmony == 1:
                        # Horizontal Host Harmony
                        harmony_string = colored('{0}'.format(emDash), 'white')
                    elif harmony == 2:
                        # Vertical Guest Harmony
                        harmony_string = colored('|', 'yellow')
                    elif harmony == 3:
                        # Vertical Host Harmony
                        harmony_string = colored('|', 'white')

                    squarestring = colored("[", color) + harmony_string + colored("]", color)
                output += squarestring
            output += "\n"

        
        # print("Harmony Chains: ")
        # self.display_harmony_chains()


        print("Board: \n")
        print(x_gridline)
        print(output)


    def take_turn(self, player):
        # Input loop
        while True:
            player_string = "Host" if player else "Guest"
            # Ask the player what they want to do
            input_string = input("Round {1}: It's your turn, {0}. Do you want to Plant or Arrange? Press P to Plant, A to arrange. Press X to quit the game. \n".format(player_string, self.round))

            if (input_string == 'p' or input_string == 'P'):
                move_type = 'P'
            elif (input_string == 'a' or input_string == 'A'):
                move_type = 'A'
            elif (input_string == 'x' or input_string == 'X'):
                print("Goodbye!")
                sys.exit(0)
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
            
            # Process Arranging
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

                # The move function has some error handling of its own
                try:
                    self.move(int(oldx), int(oldy), int(newx), int(newy))
                except MoveException as e:
                    print("Error in requested move: ", end='')
                    print(e)
                    continue
                break

        # Display the results of the action
        print("Turn played successfully.")
        self.display_board()

    # Takes a (<starting node>, <visited nodes: nodes>, <current node>)
    def traversal(self, start, visited, current, depth, cycles, crossings):

        # Mark the current node as visited
        visited.add(current)
        isIn = False
        bonus = 0

        # Base case (cycle found)
        looped = (start in current.harmonized) and depth > 1
        if looped:
            # A cycle can be identified later by all of the elements visited during the loop
            cycles.add(frozenset(visited))
            if (current.y >=0) and (start.y < 0):
                crossings += 1
            elif (current.y < 0) and (start.y >= 0):
                crossings += 1
            #print(f' - Looking at ({visited}) ')
            #print(f' - crossings: {crossings}')
            isIn = (((crossings))%2 == 1)
            if isIn:
                if current.owner == 1 and self.winner != 0:
                    self.winner = 1
                else:
                    self.winner = 0
            #print(isIn)
            if (current.y >=0) and (start.y < 0):
                crossings -= 1
            elif (current.y < 0) and (start.y >= 0):
                crossings -= 1
            
            
            
        # Traverse each available unvisited node
        for i in current.harmonized:
            
            #rint(f'{current.x > 0}, {current.y >=0}, {i.y < 0}')
            
            
            if i not in visited:
                #print(f'currently at {current}')
                if (current.x > 0) and (current.x == i.x):
                        #print(f'Looking at ({current.x}, {current.y}) and ({i.x}, {i.y}):')
                        if (current.y >=0) and (i.y < 0):
                            #print(f'   - Current crossings: {crossings}. \n   - Looking at ({current.x}, {current.y}) and ({i.x}, {i.y}):')
                            bonus = 1
                        elif (current.y < 0) and (i.y >= 0):
                            bonus = 1
                            #print(f'   - Current crossings: {crossings}. \n   - Looking at ({current.x}, {current.y}) and ({i.x}, {i.y}):')
                        #print(bonus)
                else:
                    bonus = 0
                
                
                subCycles, bool = self.traversal(start, visited.copy(), i, depth+1, cycles, crossings + bonus)
                #print(f'     - backtracking to {current} which had {crossings} crossings')
                for j in subCycles:
                    cycles.add(j)
                #if bool:
                #    print(f'Looking at ({current.x}, {current.y}) and ({i.x}, {i.y}):')
                isIn = bool or isIn
        #print(f'---Returning {isIn}---')
        return cycles, isIn

    # Check whether the current state of the board fulfills the win condition
    # If it does, set self.game_over to 1
    def check_win_condition(self):
        self.game_over = 0
        ended = False
        cycleSet = set()
        for i in self.placed:
            #print(f'**************{i}**************')
            subCycles, returnedBool = self.traversal(i,set(),i,0,set(), 0)
            '''
            for j in subCycles:
                cycleSet.add(j)
            '''
            ended = ended or returnedBool

            # Update self.winner()
            

        self.game_over = ended
            
        # Go through each node of the graph that represents the harmonies
        
        '''
        print(cycleSet)
        
        for i in cycleSet:
            print("\n")
            inChecker = 0 #if there are an odd number of lines to the right, (0,0) would be in.
            for j in i:
                print(f'{j.x},{j.y} ')

                # find a point in the bottom right quadrant
                if (j.x > 0) and (j.y<0):

                    # find a point in the top right quadrant of the same x
                    for k in i:
                        if (k.x == j.x) and (k.y >= 0) and (not k == j):
                            inChecker += 1
                            print(f'Line from ({j.x},{j.y}) to ({k.x},{k.y}) ')
                            break
            print(f'{inChecker}')
        '''

        pass
        

    # Start a game of Skud Pai Sho
    def play(self):
        print("Come in and have a cup of tea. Let's play a game of Skud Pai Sho.")
        
        # The Host plays with light tiles and the Guest plays with dark tiles. The Guest plays first.
        # Internally we represent the Guest as 0 and the Host as 1

        self.display_board()

        while not self.game_over:
            self.take_turn(self.current_player)
            
            self.check_win_condition()

            if self.current_player == 1:
                self.round += 1

            self.current_player = (self.current_player + 1) % 2

        # Display end of game message
        print("Just as the seasons pass away, so must this game of Skud Pai Sho end.")

        if self.winner == 1:
            print(f'The Host emerges victorious.')
        elif self.winner == 0:
            print(f'The Guest emerges victorious.')
        

        sys.exit()