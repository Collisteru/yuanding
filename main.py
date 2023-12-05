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
            radius = arg

    game = PaiSho.PaiSho(int(radius)) 
    
    # Testing suites below

    # # Add piece
    # '''
    # game.add(2,1,1)
    # game.add(2,-1,1)
    # game.add(-1,1,1)
    # game.add(-1,-1,1)
    # game.add(3,1,0)
    # game.add(3,-1,0)
    # game.add(4,1,0)
    # game.add(4,-1,0)
    # '''
    # game.play()
    # game.display_harmony_chains()

    # game.display_board()
    
    # game.check_win_condition()

    # # Move piece one square up
    # game.move(2,1,2,2)
    # game.display_board()

    # # Move piece up one and to the right diagonally
    # game.move(2,2,3,3)
    # game.display_board()

    # Testing capture
    ## Successful Capture

    # game = PaiSho.PaiSho(3) 

    # game.add(0,3, 0)
    # game.add(0,0, 1)

    # # Guest moves to capture opponent piece

    # game.play()

    # Unsuccessful Capture

    game = PaiSho.PaiSho(3) 

    game.add(0,3, 0)
    game.add(0,0, 0)

    # Guest moves to attempt to capture own piece

    game.play()

if __name__ == "__main__":
    main(sys.argv[1:])

'''test game (Host win)
p
r

p
u

a
5
0
5
0

p
d

a
5
0
5
0

a
0
5
1
4

a
5
0
5
0

a
0
-5
1
-4

a
5
0
5
0

p
d

a
5
0
5
0

p
u

a
5
0
5
0

a
0
5
-1
4

a
5
0
5
0

a
0
-5
-1
-4
'''

'''test game 2 (guest win)
p
u

p
r

p
d

a
5
0
5
0

a
0
5
1
4

a
5
0
5
0

a
0
-5
1
-4

a
5
0
5
0

p
d

a
5
0
5
0

p
u

a
5
0
5
0

a
0
5
-1
4

a
5
0
5
0

a
0
-5
-1
-4
'''