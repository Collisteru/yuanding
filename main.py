import PaiSho
import randomplayer
import termcolor
import sys, getopt


def main(argv):
    opts, args = getopt.getopt(argv, "hr:")

    # Default radius
    radius = 5

    for opt, arg in opts:
        if opt == '-h':
            print("python main.py -r <board radius>")
            sys.exit()
        elif opt == '-r':
            try: int(arg)
            except: 
                print("Second argument needs to be an integer.")
                sys.exit()
        radius = int(arg)


    # # Replace this with a test?
    # game = PaiSho.PaiSho(radius)
    # game.play()

    # Host Should be able to win in one Turn

    game = PaiSho.PaiSho(3)


    game.add(-1,-0,1)

    game.add(0,0,1)

    game.add(1,1,0)
  

    game.display_board()

    # Let's spin up a new random player to play as the Guest
    randplay = randomplayer.RandPlayer(0)

    randplay.random_move(game)
    
    game.display_board()





if __name__ == "__main__":
    main(sys.argv[1:])

