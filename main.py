import paisho
import termcolor


game = paisho.PaiSho()
game.display_board()

# Add piece
game.add(2,1,"P1")
game.display_board()

# Move piece one square up
game.move(2,1,2,2)
game.display_board()

# Move piece up one and to the right diagonally
game.move(2,2,3,3)
game.display_board()

# Try to move piece out of range. An exception should result
game.move(3,3,-1,3)
game.display_board()

# Other Examples:

# # Example of setting specific values:
# game.add(2,1,"P1")
# game.display_board()

# # Example of setting specific values:
# game.remove(2,1)
# game.display_board()

# # game.add(2,-1,"P1")
# game.display_board()

# # Example of setting specific values:
# game.checkHarmonies()