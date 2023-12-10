# Bespoke functions and classes relating to the AI and the minmax tree

# Given a game state and a player, calculates the utility for that player
# The utility function has a number of components:

import PaiSho

import numpy as np


class AI:

    def __init__(self, pieceBonus = 1, crossoverBonus = 5, harmonyBonus = 1):
        self.pieceBonus = pieceBonus
        self.harmonyBonus = harmonyBonus
        self.crossoverBonus = crossoverBonus
        
    # we can modify the piece utility via this value

    def utilRecur(self, parent, currentPiece, viewed, crossovers):
        
        score = 0
        
        if not currentPiece in viewed:
            viewed.append(currentPiece)
            
            score += self.harmonyBonus

            score += self.pieceBonus

            if currentPiece.x * parent.x < 0:
                if (currentPiece.y * parent.y > 0):
                    if (not "N" in crossovers) and (parent.y > 0):
                        score += self.crossoverBonus
                        crossovers.append("N")
                    if (not "S" in crossovers) and (parent.y < 0):
                        score += self.crossoverBonus
                        crossovers.append("S")

            if currentPiece.y * parent.y < 0:
                if (currentPiece.x * parent.x > 0):
                    if (not "W" in crossovers) and (parent.x < 0):
                        score += self.crossoverBonus
                        crossovers.append("W")
                    if (not "E" in crossovers) and (parent.x > 0):
                        score += self.crossoverBonus
                        crossovers.append("E")

            for i in currentPiece.harmonized:
                score += self.utilRecur(currentPiece, i, viewed, crossovers)
            
        return score

    # The selected player will be deemed "more winning" if utility is positive
    def calculate_utility(self, game, player = 0):
        if self.terminal_test(game):
            return np.inf * (game.winner * 2 - 1)
        utility = 0 
        viewed = [] #A list of viewed pieces
        for currentPiece in game.placed:

            
            # Do we want to create a new instance 
            #   Check if we've made a utility tuple for this owner
            '''
            currentPieceOwner = currentPiece.owner
            ignore = False 
            for i in utility:
                if i.player == currentPieceOwner:
                    ignore = True
                    currUtil = utility.index(i)
                    break
            if not ignore:
                utility.append(PlayerUtil(currentPieceOwner))
                currUtil = len(utility)-1
            '''

            
            
            if not currentPiece in viewed:
                multiplier = (currentPiece.owner == player) * 2 - 1        
                viewed.append(currentPiece)
                utility += multiplier
                for i in currentPiece.harmonized:
                    utility += multiplier * self.utilRecur(currentPiece, i, viewed, [])

        print(utility)

        pass

# Checks if this game state is a terminal node
    def terminal_test(game):
        if game.game_over == 1:
            return True
        pass

    def minmax_decision(state, game):
        '''
        Given a state in a game, calculate the best move by searching
        forward all the way to the terminal states. [Figure 5.3]
        '''
        maxDepth = 3
        player = game.current_player

        def max_value(state, depth):
            if game.terminal_test(state) or depth > maxDepth:
                return game.utility(state, player)
            v = -np.inf
            for a in game.actions(state):
                v = max(v, min_value(game.result(state, a), depth))
            return v

        def min_value(state, depth):
            if game.terminal_test(state) or depth > maxDepth:
                return game.utility(state, player)
            v = np.inf
            for a in game.actions(state):
                v = min(v, max_value(game.result(state, a)))
            return v

        # Body of minmax_decision:
        return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))