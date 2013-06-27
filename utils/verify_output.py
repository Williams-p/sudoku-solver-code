# Verification program used to test two sudoku boards against each other
# using asserts; pretty straightforward...

import sys, os

if len(sys.argv) < 2 or len(sys.argv) > 3 :
    print "\nusage: python " + sys.argv[0] + " <file_1> <file_2>\n"
    sys.exit(0)
if not os.path.isfile(sys.argv[1]) :
    raise ValueError, 'the file \'' + sys.argv[1] + '\' does not exist.\n'
if not os.path.isfile(sys.argv[2]) :
    raise ValueError, 'the file \'' + sys.argv[2] + '\' does not exist.\n'
file_one = open(sys.argv[1])
file_two = open(sys.argv[2])
gridOne = []
gridTwo = []

for line in file_one :
    values = line.split()
    newlist = []
    for value in values :
        newlist.append(int(value))
    gridOne.append(newlist)

for line in file_two :
    values = line.split()
    newlist = []
    for value in values :
        newlist.append(int(value))
    gridTwo.append(newlist)

for i in range(9) :
    for j in range(9) :
        assert gridOne[i][j] == gridTwo[i][j]
