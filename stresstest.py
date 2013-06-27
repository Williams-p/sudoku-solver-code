import sys, time, math
sys.path.append('utils')
import manager

NUM = -1 # Number of boards to solve
DIFFICULTY = None # Difficulty of the boards
STRNG_DIFF = None # Difficulty, in String form
ALGORITHM = 0 # Dictates the type of algorithm to run

def print_help() :
    print "\nUsage: python", sys.argv[0], "<-n NUMBER_TO_SOLVE> <-d DIFFICULTY> [-s STRATEGY]"
    print "  -n, --number             Number of boards to solve.\n"
    print "  -d, --difficulty         Difficulty of generated boards."
    print "                           OPTIONS: Easy, Medium, Hard.\n"
    print "  -s, --solution-strategy  Dictates the algorithm(s) used to solve the puzzles."
    print "                             0 (default): Combined logic and \'Smart Search\'."
    print "                             1: Logic only; unlikely to find hard solutions!"
    print "                             2: Use \'ac3\' guess-and-check only.\n"
    sys.exit(0)

for i in range(1, len(sys.argv)) :
    if sys.argv[i] == "-h" or sys.argv[i] == "--help" :
        print_help()

if len(sys.argv) < 5 or len(sys.argv) > 7 :
    print "usage: python", sys.argv[0], "<-n NUMBER_TO_SOLVE> <-d DIFFICULTY> [-s STRATEGY]"
    print "  use \'-h\' or \'--help\' for more info."
    sys.exit(0)

for i in range(1, len(sys.argv)) :
    if sys.argv[i] == "-n" or sys.argv[i] == "--number" :
        try :
            NUM = int(sys.argv[i+1])
        except ValueError :
            message = "[ERROR]: Number of board to solve must be an integer. Exiting."
            print message
            sys.exit(0)
    elif sys.argv[i] == "-d" or sys.argv[i] == "--difficulty" :
        a = sys.argv[i+1].lower()
        STRNG_DIFF = sys.argv[i+1]
        if a == "easy" or a == "medium" or a == "hard" :
            DIFFICULTY = a
        else :
            message = "[ERROR]: Difficulty \'" + repr(sys.argv[i+1]) + "\' unrecognized. "
            message += "Exiting after info."
            print message
            print_help()
    elif sys.argv[i] == "-s" or sys.argv[i] == "--solution-strategy" :
        try :
            ALGORITHM = sys.argv[i+1]
        except ValueError :
            message = "[ERROR]: Solution Strategy must be an integer. Exiting after info."
            print message
            print_help()

togo = NUM
t1 = time.time()
while togo > 0 :
    mngr = manager.Manager(None, 0, ALGORITHM, DIFFICULTY, False, None)
    mngr.run
    togo -= 1
t2 = time.time()
sec = (t2-t1) % 60
minu = math.floor((t2-t1) / 60)
print "Solving", NUM, STRNG_DIFF, "puzzles took", int(minu), "minutes,", sec, "seconds."
print "On average, each solution took ", (t2-t1)*1000/NUM, "milliseconds."
