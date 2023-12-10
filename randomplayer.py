# Bespoke functions and classes relating to the Random playser

import PaiSho
import random

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

    # Randomly choose to make an arrangement move or a planting move
    # Make this move
    def random_move(self, game):
        
        valid_moves = game.get_valid_moves(self.player)

        # Can we Plant?
        ogates = valid_moves[0]
        can_plant = (ogates['Up'] or ogates['Right'] or ogates['Down'] or ogates['Left'])

        # Can we arrange?
        can_arrange = 1 if len(valid_moves[1] != 0) else 0

        # First, the random player chooses whether to plant or to arrange.
        # If it can only plant, it does that. If it can only arrange, it does that.
        # If it can't do either, it returns a message saying that the random player can't move.
        # If it can do both, it will plant 25% of the time and arrange 75% of the time

        if not can_arrange and not can_plant:
            print("The Guest can't make any moves.") if self.player == 0 else print("The Host can't make any moves.")

        if can_arrange and not can_plant:
            self.random_arrange(game)

        if can_plant and not can_arrange:
            self.random_plant(game)

        if can_plant and can_arrange:
            # In this case, the player plants 25% of the time and arranges 75% of the time.
            if random.random() < 0.75:
                self.random_arrange(game, valid_moves)
            else:
                self.random_plant(game, valid_moves)


        print("The Guest has made a random move.") if self.player == 0 else print("The Host has made a random move.")

    # Make a random arrangement move
    def random_arrange(self, game, valid_moves):
        arrangements = valid_moves[1]

        chosen_arrangement = random.choice(arrangements)

        # Parse given arrangement (all required checks should have already been made)
        game.move(valid_moves[0], valid_moves[1], valid_moves[2], valid_moves[3])

    # Make a random planting move
    def random_plant(self, game, valid_moves):

        ogates = []
        open_gates = valid_moves[0]

        if open_gates['Up']:
            ogates.append("Up")

        if open_gates['Down']:
            ogates.append("Down")
        
        if open_gates['Left']:
            ogates.append("Left")
        
        if open_gates['Right']:
            ogates.append("Right")

        chosen_gate = random.choice(ogates)

        # TODO: There should be a specific function for putting pieces in gates
        if chosen_gate == 'Up':
            if open_gates["Up"]:
                game.add(0, self.radius, self.player)

            if open_gates["Down"]:
                game.add(0, -self.radius, self.player)

            if open_gates["Right"]:
                game.add(self.radius, 0, self.player)

            if open_gates["Left"]:
                game.add(-self.radius, 0, self.player)
