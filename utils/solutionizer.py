# solutionizer.py
# Affects the first and easiest line of reasoning against 
# the Sudoku problem

import board

class Solutionizer(board.Board) :

    #####################################################################################
    # Isolated Possibilities Algorithm:
    # If there exists a possibile move on a square which is not a possibility anywhere
    # else on the row, column, or subgrid, we know that possibility must be placed there.
    #####################################################################################
    def isolated_possibilites(self) :
        message = "[DEBUG]: Entering Solutionizer.isolated_possibilities()."
        self.logger.log(message, 4)

        result = False # Return value: was progress made?
        for row in range(9) :
            for col in range(9) :
                for value in range(1, 10):
                    if self.grid[row][col].possible_values.count(value) > 0 :
                        #print self.output_possible_moves()
                        if self.is_isolated_possibility(row, col, value) :
                            newlist = [row, col]
                            self.one_possible_move.append(newlist)
                            self.grid[row][col].possible_values = [value]
                            result = True
                            message = "[DEBUG]: Isolated Possibilities adding (" + repr(row)
                            message += "," + repr(col) + ") to one_possible_move (" + repr(value) + ")."
                            message += " Possible moves at (" + repr(row) + "," + repr(col) + "): " + repr(self.grid[row][col].possible_values)
                            self.logger.log(message, 4)
                            self.log_possible_moves()
                            break
        return result


    def is_isolated_possibility(self, row, col, value) :
        message = "[DEBUG]: Entering Solutionizer.is_isolated_possibility()."
        self.logger.log(message, 4)

        result = self.is_isolated_on_row(row, col, value)
        if result :
            message = "[DEBUG]: " + repr(value) + " isolated on row " + repr(row)
            message += ", at column " + repr(col)
            self.logger.log(message, 4)
            return result
        if not result :
            result = self.is_isolated_on_column(row, col, value) 
        if result :
            message = "[DEBUG]: " + repr(value) + " isolated on column " + repr(col)
            message += ", at row " + repr(row)
            self.logger.log(message, 4)
            return result
        if not result :
            result = self.is_isolated_on_subgrid(row, col, value) 
        if result :
            message = "[DEBUG]: " + repr(value) + " isolated at position (" + repr(row)
            message += ", " + repr(col) + ") on subgrid."
            self.logger.log(message, 4)
            return result
        return result


    def is_isolated_on_row(self, row, col, value) :
        message = "[DEBUG]: Entering Solutionizer.is_isolated_on_row()."
        self.logger.log(message, 4)

        result = True
        for x in range(9) :
            if x != col and self.grid[row][x].possible_values.count(value) > 0 :
                message = "[XTRME]: Possible value '" + repr(value) + "' (" + repr(row)
                message += "," + repr(col) + ") also found at (" + repr(row) + ","
                message += repr(x) + ")."
                self.logger.log(message, 5)

                result = False
                break
        return result


    def is_isolated_on_column(self, row, col, value) :
        message = "[DEBUG]: Entering Solutionizer.is_isolated_on_column()."
        self.logger.log(message, 4)

        result = True
        for y in range(9) :
            if y != row and self.grid[y][col].possible_values.count(value) > 0 :
                message = "[XTRME]: Possible value '" + repr(value) + "' (" + repr(row)
                message += "," + repr(col) + ") also found at (" + repr(y) + ","
                message += repr(col) + ")."
                self.logger.log(message, 5)

                result = False
                break
        return result


    def is_isolated_on_subgrid(self, row, col, value) :
        message = "[DEBUG]: Entering Solutionizer.is_isolated_on_subgrid()."
        self.logger.log(message, 4)

        result = True
        start_row, end_row, start_col, end_col = self.get_subgraph(row, col)
        for x in range(start_row, end_row+1) :
            for y in range(start_col, end_col+1) :
                if x != row or y != col and self.grid[x][y].possible_values.count(value) > 0 :
                    message = "[XTRME]: Possible value '" + repr(value) + "' (" + repr(row)
                    message += "," + repr(col) + ") also found at (" + repr(x) + ","
                    message += repr(y) + ")."
                    self.logger.log(message, 5)

                    result = False
                    break
        return result

#########################################################################################

##########################################
#Naked twins alghorithm:
#
#If there is a set of squares with two identicle possibilities in the same row, column, or subgrid,     
#    then we can remove either on of thos possibilities in the other squares partaining to those twins 
##########################################

    def naked_twins(self):
        ''' Naked twins Driver'''
        result= False
        for row in range (9):
            for col in range (9):
                if self.grid[row][col].possible_values.__len__()==2:
                    # gets all squares partaining to row columns and subgrids besides that element discovered
                    row_pos=self.getrow(self.grid[row][col],row)
                    col_pos=self.getcol(self.grid[row][col],col)
                    sub_pos=self.getsub(self.grid[row][col],row,col)
                    #print row_pos
                    #print col_pos
                    #print sub_pos
                    # sends each list of to the workhorse
                    progress_r=self.nt_workhorse(row_pos,self.grid[row][col])
                    progress_c=self.nt_workhorse(col_pos,self.grid[row][col])
                    progress_s=self.nt_workhorse(sub_pos,self.grid[row][col])
                    result=progress_r or progress_c or progress_s or result # if any progress was made that turn or in previouse turns
                    #print result 
        return result       

    def nt_workhorse(self,p_vals,square):
        '''Checks if there is a another twin corresponding to the square in question if so...
        remove all ements in the row, col, or sub graph'''
        has_twin=False # is there a set of twins?
        to_remove=None # the second twin to be remove from the set
        made_progress=False # general progress
        for item in p_vals:
            if item.possible_values.__len__()==2: # another square with 2 possibilities is discovered
                if (square.possible_values[0] in item.possible_values) and (square.possible_values[1] in item.possible_values):
                    # the item has identicle possibilities to the first twin
                    has_twin=True
                    to_remove=item

        if has_twin==True:
            p_vals.remove(item) # remove the second twin... there should be no more twins in the subgraph.
            for item in p_vals:
                if square.possible_values[0] in item.possible_values: #item one is found in one squares possibilities 
                    item.possible_values.remove(square.possible_values[0])
                    made_progress=True
                if square.possible_values[1] in item.possible_values: #item one is found in one squares possibilities 
                    item.possible_values.remove(square.possible_values[1])
                    made_progress=True
        return made_progress     


    def getrow(self,square,row):
        '''gets list of squares in the row of the square given besides the actual square in question'''
        temp=[]

        for y in range (9):
            if not (self.grid[row][y]==square):
                temp.append(self.grid[row][y])

        #print len(temp)  #should be 8
        return temp

    def getcol(self,square,col):
        '''gets list of squares in the col of the square given besides the actual square in question'''
        temp=[]
        for x in range (9):
            if not (self.grid[x][col]==square):
                temp.append(self.grid[x][col])

        #print len(temp)  #shold be 8
        return temp

    def getsub(self,square,row,col):
        '''gets list of squares in the subgraph of the square given besides the actual square in question'''
        temp=[]
        if row >=0 and row<= 2:
            r_min=0
            r_max=2
        if row >=3 and row<= 5:
            r_min=3
            r_max=5
        if row >=6 and row<= 8:
            r_min=6
            r_max=8    
        if col >=0 and col<= 2:
            c_min=0
            c_max=2
        if col >=3 and col<= 5:
            c_min=3
            c_max=5
        if col >=6 and col<= 8:
            c_min=6
            c_max=8
        for r in range(r_min,r_max+1):
            for c in range(c_min,c_max+1):
                if not(self.grid[r][c]==square):
                    temp.append(self.grid[r][c])
        #print len(temp) # should be 8
        return temp


