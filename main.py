import paisho

def main(): 
    game = paisho.PaiSho()
    game.display_board()

    # Example of setting specific values:
    game.add(2,1,"P1")
    game.display_board()

    # Example of setting specific values:
    game.remove(2,1)
    game.display_board()

    # game.add(2,-1,"P1")
    game.display_board()

    # Example of setting specific values:
    game.checkHarmonies()


main()
