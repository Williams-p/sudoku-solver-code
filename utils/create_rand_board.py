import sys, random

def print_help() :
    print "\n Random Board Generator usage:"
    print "python ", sys.argv[0], "<OPTION> [OUTPUT_FILE]\n"
    print "OPTIONS:"
    print "  --hard        Generate a hard-difficulty puzzle."
    print "  --medium      Generate a medium-difficulty puzzle."
    print "  --easy        Generate an easy-difficulty puzzle."

def get_subgraph(i, j) :
        if i >=0 and i <= 2 :
            starti = 0
            endi = 2
        elif i >= 3 and i <= 5 :
            starti = 3
            endi = 5
        else :
            starti = 6
            endi = 8

        if j >=0 and j <= 2 :
            startj = 0
            endj = 2
        elif j >= 3 and j <= 5 :
            startj = 3
            endj = 5
        else :
            startj = 6
            endj = 8
        return starti, endi, startj, endj

def is_valid(row, col, val) :
    result = is_valid_rows(row, col, val)
    if result :
        result = is_valid_cols(row, col, val)
    if result :
        result = is_valid_subgrid(row, col, val)
    return result

def is_valid_rows(row, col, val) :
    result = True
    for i in range(9) :
        if grid[i][col] == val and i != row :
            result = False
            break
    return result

def is_valid_cols(row, col, val) :
    result = True
    for i in range(9) :
        if grid[row][i] == val and i != col :
            result = False
            break
    return result

def is_valid_subgrid(row, col, val) :
    result = True
    starti, endi, startj, endj = get_subgraph(row, col)
    for x in range(starti, endi + 1) :
        for y in range(startj, endj + 1) :
            if grid[x][y] == val :
                result = False
                break
    return result

def print_board() :
    output = ""
    for i in range(9) :
        for j in range(9) :
            output += repr(grid[i][j])
        output += "\n"
    print output

def print_to_file(outfile) :
    output = open(outfile, 'w')
    for i in range(9) :
        for j in range(9) :
            output.write(repr(grid[i][j]))
            output.write(" ")
        output.write("\n")
    output.close()


#MAIN
if len(sys.argv) < 2 or len(sys.argv) > 3 :
    print_help()
    sys.exit(0)

num = 38
if sys.argv[1] == "--hard" or sys.argv[1] == "hard" :
    num = random.randint(18, 22)
elif sys.argv[1] == "--medium" or sys.argv[1] == "medium" :
    num = random.randint(23, 30)
elif sys.argv[1] == "--easy" or sys.argv[1] == "hard" :
    num = random.randint(30, 40)
else :
    print_help()
    sys.exit(0)

grid = []
for i in range(9) :
    row = [0]*9
    grid.append(row)

while num > 0 :
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    if not grid[row][col] == 0 :
        continue
    val = random.randint(1, 9)
    if is_valid(row, col, val) :
        grid[row][col] = val
        num -= 1

outfile = "random_board"
if len(sys.argv) > 2 :
    outfile = sys.argv[2]

print_to_file(outfile)
