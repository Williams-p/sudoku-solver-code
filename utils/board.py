# A board class used by the Sudoku Solver AI
# It encapsulates 81 'Square' objects, and contains methods
# to interrogate and manipulate these Square objects.

import sys, os, random
import square
class Board(object) :
    def __init__(self, infile, outfile, difficulty, logger) :
        self.grid = [] # Abstract board object; list of lists containing Squares
        self.num_unknown = 0 # How many open places on the board?
        self.one_possible_move = []  # List of squares with only one possible move
        self.logger = logger # Logger object; enormous debug utility!
        self.difficulty = difficulty # How hard should the random board be (if specified)?
        self.outfile = outfile # File to write output to; may be None

        message = "[INFO]: Board class initialized. Beginning file import."
        logger.log(message, 3)  

        # Read the input file.
        if infile is not None :
            self.read_from_file(infile)
        elif self.difficulty is not None :
            self.make_random_board(self.difficulty)
        else :
            message = "[ERROR]: No method to construct board specified! Exiting."
            self.logger.log(message, 1)
            sys.exit(1)

        # Run initial analysis on our new board; count unknown values and
        # construct data on possible move values for each square
        self.process_board_state()


    # Return string representing board; different format than input file!
    def __repr__(self) :
        message = "[DEBUG]: Entering Board.__repr__()"
        self.logger.log(message, 4)
        output = ''
        m = 0
        for i in self.grid :
            n = 0
            output = output + " "
            for j in i :
                n = n + 1
                if j.value == 0 :
                    output = output + "` "
                else :
                    output = output + repr(j.value) + " "
                if n % 3 == 0 and n != 9 :
                    output = output + "| "
            output = output + "\n"
            m = m + 1
            if m % 3 == 0 and m != 9 :
                output = output + "-------+-------+------\n"
        message = "[DEBUG]: Leaving Board.__repr__(). Result:"
        self.logger.log(message, 4)
        messages = output.split('\n')
        for message in messages :
            message = "[DEBUG]:  " + message
            self.logger.log(message, 4)
        return output

    

    def read_from_file(self, infile) :
        message = "[DEBUG]: Entering Board.read_from_file()"
        self.logger.log(message, 4)
        if not os.path.isfile(infile) :
            message = "[ERROR]: The file \'" + infile + "\' does not exist. Exiting."
            self.logger.log(message, 1)
            sys.exit(1)
        file_handler = open(infile)
        value_counter = 0 # Count number of values in input file
        for line in file_handler :
            values = line.split()
            newlist = []
            for value in values :
                newSquare = square.Square(self.logger)
                newSquare.set_value(int(value))
                newlist.append(newSquare)
                value_counter += 1
            self.grid.append(newlist)

        if value_counter < 81 :
            message = "[ERROR]: Too few values in the input file. Exiting."
            self.logger.log(message, 1)
            sys.exit(1)
        if value_counter > 81 :
            message = "[WARN]: Too many values in input file."
            self.logger.log(message, 2)
        message = "[INFO]: Completed reading from file. Running initial analysis."
        self.logger.log(message, 3)

    def make_random_board(self, diff) :
        message = "[DEBUG]: Entering Board.make_random_board()."
        self.logger.log(message, 4)
        num_to_place = -1
        if diff == "easy" :
            num_to_place = random.randint(30, 40)
        elif diff == "medium" :
            num_to_place = random.randint(23, 30)
        elif diff == "hard" :
            num_to_place = random.randint(18, 22)
        else :
            message = "[ERROR]: Random board difficulty improperly specified: "
            message += repr(diff) + ". Exiting."
            self.logger.log(message, 1)
            sys.exit(1)

        for i in range(9) : # Initialize grid 
            newlist = []
            for j in range(9) :
                newSquare = square.Square(self.logger)
                newSquare.set_value(0)
                newlist.append(newSquare)
            self.grid.append(newlist)

        while num_to_place > 0 :
            row = random.randint(0,8)
            col = random.randint(0,8)
            if not self.grid[row][col].value == 0 :
                continue
            val = random.randint(1, 9)
            if not self.is_number_connected(row, col, val) :
                self.grid[row][col].set_value(val)
                num_to_place -= 1

    def process_board_state(self) :
        # Count number of unknowns on board; update counter (num_unknown)
        message = "[DEBUG]: Entering Board.process_board_state()."
        self.logger.log(message, 4)

        self.num_unknown = 0   # Should already be set to 0; being pedantic
        for i in range(9) :  # For all rows
            for j in range(9) :  # For all columns
                if self.grid[i][j].value == 0 :  # Check if value is unknown
                    message = "[XTRME]: Empty value found at [" + repr(i)
                    message += "][" + repr(j) + "]."
                    self.logger.log(message, 5)
                    self.num_unknown += 1

        message = "[INFO]: Number of unknowns counted(" + repr(self.num_unknown)
        message += " found). Checking possible moves."
        self.logger.log(message, 3)

        # Figure out possible values for each unmarked square
        for i in range(9) : # For all rows
            for j in range(9) :  # For all columns
                if self.grid[i][j].value == 0 :
                    for k in range(1, 10) : # For all values 1-9
                        if not self.is_number_connected(i, j, k) :
                            self.grid[i][j].add_possible_value(k)
                            message = "[XTRME]: Found possible value (" + repr(k)
                            message += ") at location [" + repr(i) + "][" + repr(j)
                            message += "]."
                            self.logger.log(message, 5)
                    # Only 1 potential value? We know it must be placed here.
                    if len(self.grid[i][j].possible_values) == 1 :
                        newlist = [i, j]
                        self.one_possible_move.append(newlist)
                        message = "[XTRME]: Found square with one possible move ("
                        message += repr(k) + ") at location [" + repr(i) + "]["
                        message += repr(j) + "]"
                        self.logger.log(message, 5)
        # Uncomment to see possible move diagram
        # self.output_possible_moves()


    def place_knowns(self) :
        message = "[DEBUG]: Entering place_knowns()."
        self.logger.log(message, 4)

        result = False # Return value; was any progress made (values written)?

        while len(self.one_possible_move) > 0 :
            if not self.valid_state():
                break
            new_move = self.one_possible_move.pop()
            i = new_move[0]
            j = new_move[1]
            value = self.grid[i][j].possible_values[0]
            message = "[XTRME]: Ascribing " + repr(value) + " to ["
            message += repr(i) + "][" + repr(j) + "]."
            self.logger.log(message, 5)
            self.grid[i][j].set_value(value)
            result = True            
            self.update_possible_moves(i, j, value)
        return result


    # Value 'k' was written at (i, j); no connected squares should have 
    # 'k' as possible value
    def update_possible_moves(self, i, j, k) :
        message = "[DEBUG]: Entering update_possible_moves()."
        self.logger.log(message, 4)

        result = False # Return value; true if we removed possible values
        for m in range(9) : 
            # Check along the column
            if m != i and self.grid[m][j].possible_values.count(k) > 0 :
                message = "[XTRME]: Removing possible move " + repr(k)
                message += " from [" + repr(m) + "][" + repr(j) + "]."
                self.logger.log(message, 5)
                self.grid[m][j].remove_possible_value(k)
                # Check if we've isolated another single possible value
                if len(self.grid[m][j].possible_values) == 1 :
                    newlist = [m, j]
                    self.one_possible_move.append(newlist)
                result = True
            # Check along the row
            if m != j and self.grid[i][m].possible_values.count(k) > 0 :
                message = "[XTRME]: Removing possible move " + repr(k)
                message += " from [" + repr(i) + "][" + repr(m) + "]."
                self.logger.log(message, 5)
                self.grid[i][m].remove_possible_value(k)
                if len(self.grid[i][m].possible_values) == 1 :
                    newlist = [i, m]
                    self.one_possible_move.append(newlist)
                result = True
        starti, endi, startj, endj = self.get_subgraph(i, j)
        # Check the subgrid
        for x in range(starti, endi + 1) :
            for y in range(startj, endj + 1) :
                if x != i and y != j :
                    if self.grid[x][y].possible_values.count(k) > 0 :
                        message = "[XTRME]: Removing possible move " + repr(k)
                        message += " from [" + repr(x) + "][" + repr(y) + "]."
                        self.grid[x][y].remove_possible_value(k)
                        if len(self.grid[x][y].possible_values) == 1 :
                            newlist = [x, y]
                            self.one_possible_move.append(newlist)
                        result = True
        return result

    # Is 'k' connected to (i, j) by row, column, or subgrid?
    def is_number_connected(self, i, j, k) :
        message = "[DEBUG]: Entering Board.is_number_connected()."
        self.logger.log(message, 4)

        result = False
        for n in range(9) : # Check the column
            if n != i and self.grid[n][j].value == k :
                result = True
                message = "[XTRME]: Value \'" + repr(k) + "\' connected to ["
                message += repr(i) + "][" + repr(j) + "] via column at location ["
                message += repr(n) + "][" + repr(j) + "]."
                self.logger.log(message, 5)
                break
        if not result : # Not found in columns?
            for n in range(9) : # Check row
                if n != j and self.grid[i][n].value == k :
                    result = True
                    message = "[XTRME]: Value \'" + repr(k) + "\' connected to ["
                    message += repr(i) + "][" + repr(j) + "] via row at location ["
                    message += repr(i) + "][" + repr(n) + "]."
                    self.logger.log(message, 5)
                    break
        if not result : # Still not found?
            result = self.subgrid_has_number(i, j, k)

        return result


    def subgrid_has_number(self, i, j, k) :
        message = "[DEBUG]: Entering Board.subgrid_has_number()."
        self.logger.log(message, 4)

        result = False
        starti, endi, startj, endj = self.get_subgraph(i, j)
        for x in range(starti, endi + 1) :
            for y in range(startj, endj + 1) :
                if x != i and y != j :
                    if self.grid[x][y].value == k :
                        result = True
                        message = "[XTRME]: Value \'" + repr(k) + "\' connected to ["
                        message += repr(i) + "][" + repr(j) + "] via subgrid at ["
                        message += repr(x) + "][" + repr(y) + "]."
                        self.logger.log(message, 5)
        return result

    # Figuring out the subgraph for (i, j) sucks; call this
    # ADD +1 TO ENDI/J IF USING RANGE()!!
    def get_subgraph(self, i, j) :
        message = "[DEBUG]: Entering Board.get_subgraph()."
        self.logger.log(message, 4)

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

        message = "[XTRME]: Leaving Board.get_subgraph(). Coordinates [" + repr(i)
        message += "][" + repr(j) + "] yield i(" + repr(starti) + "-" + repr(endi)
        message += "), j(" + repr(startj) + "-" + repr(endj) + ")."
        self.logger.log(message, 5)

        return starti, endi, startj, endj

    def valid_state(self) :
        message = "[DEBUG]: Entering Board.valid_state()."
        self.logger.log(message, 4)
        result = True
        # checks to see if each spot that does not have a value assigned has a possible value
        for row in range(9) :
            for col in range(9) :
                if self.grid[row][col].value == 0:
                    if len(self.grid[row][col].possible_values) < 1 :
                        result = False
        return result

    def validate_board(self) :
        message = "[DEBUG]: Entering Board.validate_board()."
        self.logger.log(message, 4)

        result = self.validate_rows()
        if result is True :
            result = self.validate_columns()
        if result is True :
            result = self.validate_subgrids()
        return result

    def validate_rows(self) :
        message = "[DEBUG]: Entering Board.validate_rows()."
        self.logger.log(message, 4)

        result = True
        for i in range(9) :   # For each row
            for k in range(1, 10) :    # For each value 1-9
                foundk = False   # Have we found k?
                for j in range(9) :   # For each square in the row
                    if self.grid[i][j].value == k :   # Test connectivity
                        foundk = True   
                if foundk == False :   # Did we find 'k' along row 'i'?
                    message = "[XTRME]: Board invalid! Cannot find " + repr(k)
                    message += " at [ " + repr(i) + "][" + repr(j) + "] "
                    message += "along the row."
                    self.logger.log(message, 5)
                    result = False
        return result

    # Almost a carbon-copy of validate_rows()
    def validate_columns(self) :
        message = "[DEBUG]: Entering Board.validate_columns()."
        self.logger.log(message, 4)

        result = True
        for j in range(9) :
            for k in range(1, 10) :
                foundk = False
                for i in range(9) :
                    if self.grid[i][j].value == k :
                        foundk = True
                if foundk == False :
                    message = "[XTRME]: Board invalid! Cannot find " + repr(k)
                    message += " at [ " + repr(i) + "][" + repr(j) + "] "
                    message += "along the column."
                    self.logger.log(message, 5)
                    result = False
        return result

    def validate_subgrids(self) :
        message = "[DEBUG]: Entering Board.validate_subgrids()."
        self.logger.log(message, 4)

        result = True
        subgrid_markers = [0, 3, 6]
        for i in subgrid_markers :
            for j in subgrid_markers :
                for k in range(1, 10) :
                    foundk = False
                    starti, endi, startj, endj = self.get_subgraph(i, j)
                    for x in range(starti, endi + 1) :
                        for y in range(startj, endj + 1) :
                            if self.grid[x][y].value == k :
                                foundk = True
                    if foundk == False :
                        message = "[XTRME]: Board invalid! Cannot find " + repr(k)
                        message += " at [" + repr(i) + "][" + repr(j) + "] in subgrid."
                        self.logger.log(message, 5)
                        result = False
                        break
        return result

    # Output the board to a file in the same format as the input files 
    def write_to_file(self) :
        message = "DEBUG]: Entering Board.write_to_file()."
        self.logger.log(message, 4)
        output = ''
        m = 0
        for i in range(9) :
            n = 0
            for j in range(9) :
                output = output + repr(self.grid[i][j].value)
                n = n + 1
                if n != 9 :
                    output = output + " "
            m = m + 1
            if m != 9 :
                output = output + "\n"
        outfile = open(self.outfile, 'w')
        outfile.write(output)
        message = "[DEBUG]: Leaving Board.write_to_file()."
        self.logger.log(message, 4)

    # Outputs possible move table to screen. Pretty large output dimensions, so make that terminal big!
    def output_possible_moves(self) :
        message = "[DEBUG]: Entering Board.output_possible_moves()."
        self.logger.log(message, 4)
        result = ""
        left_side = [0, 3, 6]
        for i in range(9) :
            for j in left_side :
                for k in range(9) :
                    for l in range(1, 4) :
                        if self.grid[i][k].possible_values.count(j+l) > 0 :
                            result += " " + repr(j+l)
                        else :
                            result += " -"
                    if (k + 1) % 3 == 0 and k != 8 :
                        result += " ||"
                    elif k == 8 :
                        result += "\n"
                    else :
                        result += " |"
            if (i+1) % 3 == 0 and i != 8 :
                result += "=========================================================================\n"
            elif i != 8 :
                result += "-------------------------------------------------------------------------\n"
        return result

    # Logs possible move table to log (level 5). This log is so going to break 5 digit lengths...
    def log_possible_moves(self) :
        inputa = self.output_possible_moves()
        messages = inputa.split("\n")
        msg = "\n[XTRME]: POSSIBLE MOVE TABLE:\n"
        for message in messages :
            msg = "[XTRME]: " + message
            self.logger.log(msg, 5)
        
    # returns the row and col of the position with the smallest number of possible moves
    def min_options(self, b):
        best = 9001
        
        message = "[DEBUG]: Entering min_options()."
        self.logger.log(message, 4)

        for row in range(9) :
            for col in range(9) :
                for value in range(1, 10):
                    if b.grid[row][col].possible_values.count(value) > 0 :
                       if b.grid[row][col].possible_values.count(value) < best :
                           result = b.grid[row][col].possible_values.count(value)
                           row_val = row
                           col_val = col
        return row_val, col_val

    # makes a move on a temp board and returns the temp board with the move made and the possible_values and possible_moves have been updated
    def make_move(self, temp, row, col, value):
        message = "[DEBUG]: Entering make_move()."
        self.logger.log(message, 4)

        temp.grid[row][col].value = value
        temp.grid[row][col].possible_values = []
        temp.update_possible_moves(row, col, value)
        return temp



