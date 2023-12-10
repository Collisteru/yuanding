import PaiSho
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

    print("All of the valid moves for the Guest:")
    print(game.get_valid_moves(0))

    print("All of the valid moves for the Host:")
    print(game.get_valid_moves(1))



if __name__ == "__main__":
    main(sys.argv[1:])

