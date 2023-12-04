import paisho
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
            radius = arg

    game = paisho.PaiSho(int(radius)) 
    


    # 


    # Testing suites below

    # # Add piece
    game.add(2,1,"P1")
    game.add(2,-1,"P1")
    game.add(-1,1,"P1")
    game.add(-1,-1,"P1")
    game.add(3,1,"P1")
    game.add(3,-1,"P1")
    game.add(4,1,"P1")
    game.add(4,-1,"P1")
    game.play()
    game.display_harmony_chains()

    game.display_board()
    
    game.check_win_condition()

    # # Move piece one square up
    # game.move(2,1,2,2)
    # game.display_board()

    # # Move piece up one and to the right diagonally
    # game.move(2,2,3,3)
    # game.display_board()



if __name__ == "__main__":
    main(sys.argv[1:])