import paisho
import termcolor
import sys, getopt


def main(argv):
    opts, args = getopt.getopt(argv, "hr:")

    for opt, arg in opts:
        if opt == '-h':
            print("python main.py -r <board radius>")
            sys.exit()
        elif opt == '-r':
            radius = arg

    game = paisho.PaiSho(int(radius)) 
    game.display_board()

    # # Add piece
    # game.add(2,1,"P1")
    # game.display_board()

    # # Move piece one square up
    # game.move(2,1,2,2)
    # game.display_board()

    # # Move piece up one and to the right diagonally
    # game.move(2,2,3,3)
    # game.display_board()



if __name__ == "__main__":
    main(sys.argv[1:])