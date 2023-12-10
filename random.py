# Bespoke functions and classes relating to the Random playser

# Given a game state and a player, calculates the utility for that player
# The utility function has a number of components:

import PaiSho

# class PaiShoYuanDing(PaiSho):
#     def calculate_utility(game, player):
#         pass

# # Checks if this game state is a terminal node
#     def terminal_test(game):
#         pass



# This represents the random player
class RandPlayer:

    player = 0
    
    def __init__(self, player: int):
        if player != 0 and player != 1:
            raise Exception("Random player must either be player 0 (Guest) or player 1 (Host)")
        else:  
            self.player = player

    # Take turn as a given player
    def take_turn(self, player, game):
        if player == 0:
            print("The Guest takes a random turn.")
            self.random_move(game)
        elif player == 1:
            print("The Host takes a random turn.")
            self.random_move(game)
        pass 

    def random_move(self, game):
        # Generates a random move given the game state
        pass

    pass