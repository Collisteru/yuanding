import PaiSho
import randomplayer
import ai
import termcolor
import sys, getopt


def main(argv):
    opts, args = getopt.getopt(argv, "hr:")

    # Default radius
    radius = 3

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


    game = PaiSho.PaiSho(radius)

    game.display_board()

    # Start a game of two AIs against each other
    game.play(6)

    


if __name__ == "__main__":
    main(sys.argv[1:])

