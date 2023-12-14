# IMPLEMENTATION OF A PLAYER VS. PLAYER DEMO FOR THE AI

import PaiSho
import randomplayer
import ai
import termcolor
import sys, getopt


def main(argv):
    
    game = PaiSho.PaiSho(6)

    game.play(4)


if __name__ == "__main__":
    main(sys.argv[1:])

