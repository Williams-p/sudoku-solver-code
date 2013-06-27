# Manger class

import logger, board
import solutionizer
import copy
import AC3
import min_conflicts as mc

class Manager(object) :
    # Self-explanitory...
    def __init__(self, infile, level, algorithm, difficulty, toscreen, outfile) :
        message = "[INFO]: Manager class instantiated. Beginning solution."
        self.log_manager = logger.Logger(level, toscreen)
        self.algorithm = algorithm
        self.difficulty = difficulty
        self.outfile = outfile
        self.soln = solutionizer.Solutionizer(infile, outfile, difficulty, self.log_manager)


    # Logic driver of the program
    def run(self) :
        if self.algorithm == 0 :
            self.combined(self.soln)
        if self.algorithm == 1 :
            self.logic(self.soln)
        if self.algorithm == 2 :
            self.bfs(self.soln)
        if self.algorithm == 3 :
            self.ac3()
        if self.algorithm == 4 :
            self.min_conflicts()
        is_valid = self.soln.validate_board() # Ensure the result is valid
        #print "is_valid = " + repr(is_valid) # TODO Remove this eventually
        if is_valid == False : 
            message = "[WARN]: Board failed validation step!"
            self.log_manager.log(message, 2)

        #Print to screen / file appropriatly.
        if self.outfile == None :
            print repr(self.soln)
        else :
            self.soln.write_to_file()

    def combined(self, b_temp) :
        self.logic(b_temp)
        if b_temp.validate_board():
            self.soln = copy.copy(b_temp)
            return
        elif not b_temp.valid_state():
            return
        else:
            row, col = b_temp.min_options(b_temp)
            l = []
            for value in b_temp.grid[row][col].possible_values :
                l.append(copy.copy(b_temp.make_move(copy.deepcopy(b_temp), row, col, value)))
            for x in l :
                self.combined(x)
                               
                if self.soln.validate_board():
                    break     

    def bfs(self, b_temp) :
        if b_temp.validate_board():
            self.soln = copy.copy(b_temp)
            return
        elif not b_temp.valid_state():
            return
        else:
            row, col = b_temp.min_options(b_temp)
            l = []
            for value in b_temp.grid[row][col].possible_values :
                l.append(copy.copy(b_temp.make_move(copy.deepcopy(b_temp), row, col, value)))
            for x in l :
                self.bfs(x)
                               
                if self.soln.validate_board():
                    break     

    def logic(self, b) :
        self.progress_made = True

        # Primary Logic loop!
        while self.progress_made == True :
            if not b.valid_state():
                break
            # Logging printouts each loop
            message = "[INFO]: !! manager.run() loop going for another round."
            self.log_manager.log(message, 3)
            b.log_possible_moves() # Prints possible-move table to logger
            message = "[XTRME]: List of one_possible_move:\n"
            message += repr(b.one_possible_move)
            self.log_manager.log(message, 5)

            # Add algorithms to this bit, testing for progress made at each
            self.progress_made=b.place_knowns()
            if not self.progress_made :
                print "naked twins"
                self.progress_made = b.naked_twins()
            
            self.progress_made = b.place_knowns()
            if not self.progress_made :
                print "isolated poss"
                self.progress_made = b.isolated_possibilites()

          # END Primary logic loop

    def ac3(self) :
        result = AC3.run(self.soln)
        print result
        #self.soln = result #this is a string need to make board from it.

    def min_conflicts(self) :
        solution, temp = mc.run(self.soln)
        print "Solution took",solution[1],"steps"
        self.soln = temp









