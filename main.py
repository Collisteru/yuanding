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

    # radius = 6

    game = PaiSho.PaiSho(6)

    # Add Guest pieces

    game.add(-4,4,0)

    game.add(0,4,0)

    game.add(2,4,0)

    game.add(4,4,0)

    game.add(2,2,0)

    game.add(4,2,0)

    game.add(-4,-2,0)

    game.add(0,-2,0)

    # Add Host pieces

    game.add(-2,4,1)

    game.add(-4,2,1)

    game.add(-2,2,1)

    game.add(-4,0,1)

    game.add(2,0,1)

    game.add(4,0,1)

    game.add(2,-2,1)

    game.add(4,-2,1)

    # Check the harmonies created.
    # There should be 8 Host harmonies and 7 Guest harmonies.
    # There should be one Guest harmony circle and one Host harmony circle; neither should win.


    game.play()



if __name__ == "__main__":
    main(sys.argv[1:])

