# Sudoku Solver v0.2
# Authored by Kyle Smith, Pete Williams, and Ted

import sys 
sys.path.append('utils') # Allows us to import modules from utils directory.
import manager  # Project module

VERSION = "v0.2" # For quick-and-easy changing
AUTHORS = "Kyle Smith, Peter Williams, Tom Harrison" # Ditto
INPUT_FILE = None # Holds the name of the file to read from
OUTPUT_FILE = None  # In case no output file is specified, default null
LOG_LEVEL = 0  # Verbosity of the logger; default none
ALGORITHM = 0 # Dictates the type of solution algorithm to run
DIFFICULTY = None # What difficulty level should the random board be?
TO_SCREEN = False  # Should the logger print to screen instead of file?

# If number of arguments is invalid, print usage and exit
if len(sys.argv) < 2 or len(sys.argv) > 10 : 
    print "usage: python", sys.argv[0], "< -i INPUT_FILE | -r >, [OPTIONS]..."
    print "  use \'-h\' or \'--help\' for more info."
    sys.exit(0)


# Have to define the function before the call if not class method =-\
def print_help() :
    print "\nSudoku Solver "+ VERSION  
    print "Written by " + AUTHORS
    print "\nUsage: python", sys.argv[0], "<input_file> [OPTION]..."
    print "\n  -h, --help               Show this message.\n"
    print "  -l, --log-level          Control verbosity of logging system."
    print "                           Level 0: No log file will be created."
    print "                           Level 1: Error-level logging."
    print "                           Level 2: Warning-level logging."
    print "                           Level 3: Info-level logging."
    print "                           Level 4: Debug-level logging."
    print "                             !Generates enormous log files (>1000 lines)!"
    print "                           Level 5: Extreme-level logging"
    print "                             !Over twice as verbose as level 4!\n"
    print "  -s, --solution-strategy  Dicatates the algorithm(s) used to solve puzzle."
    print "                           0 (default): Use logic and \'smart search\'."
    print "                           1: Use logic only (Not guaranteed to find solution)."
    print "                           2: Use \'ac3\' guess-and-check only.\n"
    print "  -i, --input-file         Name an input file to read the problem from\n"
    print "  -o, --output-file        Name an output file to write solution to"
    print "                           Solution will print to screen if unspecified"
    print "                           By convention, this should end with \".out\"\n"
    print "  -t, --to-screen          Redirect log output to the screen; no log file\n"
    print "  -r, --random             Generate, and solve, a random puzzle."
    print "                              OPTIONS: Easy, Medium, Hard.\n"
    print "Input file should be a 9x9 grid of whitespace-separated numbers."
    print "Each number corresponds to the corresponding value on the board."
    print "Any unknown value is represented by a zero (0)."
    print "For an example, refer to the file \'Example.board\'.\n"
    sys.exit(0)


# Parse input arguments
for i in range(1, len(sys.argv)) :
    if sys.argv[i] == "-h" or sys.argv[i] == "--help" :
        print_help()
    elif sys.argv[i] == "-i" or sys.argv[i] == "--input-file" :
        INPUT_FILE = sys.argv[i+1]
    elif sys.argv[i] == "-l" or sys.argv[i] == "--log-level" :
        try : 
            LOG_LEVEL = int(sys.argv[i+1])
        except ValueError :
            message = "[WARN]: Log-level value must be an integer."
            message += " Continuing at log-level " + repr(LOG_LEVEL)
            print message
    elif sys.argv[i] == "-s" or sys.argv[i] == "--solution-strategy" :
        try :
            ALGORITHM = int(sys.argv[i+1])
        except ValueError :
            message = "[WARN]: Solve-with value must be an integer."
            message += " Continuing with strategy " + repr(ALGORITHM)
            print message
    elif sys.argv[i] == "-r" or sys.argv[i] == "--random" :
        a = sys.argv[i+1].lower()
        if a == "easy" or a == "medium" or a == "hard" :
            DIFFICULTY = a
        else :
            message = "[WARN]: difficulty improperly specified; defaulting to medium."
            print message
            DEFFICULTY = "medium"
    elif sys.argv[i] == "-o" or sys.argv[i] == "--output-file" :
        OUTPUT_FILE = sys.argv[i+1]
    elif sys.argv[i] == "-t" or sys.argv[i] == "--to-screen" :
        TO_SCREEN = True

if DIFFICULTY is None and INPUT_FILE is None :
    message = "[ERROR]: Neither an input file nor random board difficulty has been specified.\n"
    message += "Nothing to solve. Exiting."
    print message
    sys.exit(0)

if DIFFICULTY is not None and INPUT_FILE is not None :
    message = "[ERROR]: Both an input file and random board difficulty have been specified.\n"
    message = "Can only solve one. Exiting"
    print message
    sys.exit(0)

# Initialize the manager, which will take over from here.
mngr = manager.Manager(INPUT_FILE, LOG_LEVEL, ALGORITHM, DIFFICULTY, TO_SCREEN, OUTPUT_FILE)
mngr.run()
