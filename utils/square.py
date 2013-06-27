# Square object used by Sudoku Board
# Used to store information about each square
# on a standard sudoku board

class Square(object) :
    def __init__(self, logger) :
        self.value = 0   # Final value; 0 = unknown
        self.possible_values = []   # List of numbers this square could be
        self.guess = False   # Was the value a guess (for recursive guessing)?
        self.logger = logger  # Pass in logger
    def __repr__(self):
        return str(self.value)

    # Not a guess! Clear other data.
    def set_value(self, val) :
        if self.possible_values.count(val) == 0 :
            message = "[DEBUG]: !!\n[DEBUG]: Value being ascribed"
            message += "(" + repr(val) + ") is not a calculated possibilityi!!\n"
            message += "[DEBUG]: !!(ignore if at beginning of log)\n!!"
            self.logger.log(message, 4)
        self.value = val
        self.possible_values = []
        self.guess = False

    # Guess incoming! Leave possible moves as-is for now.
    def guess_value(self, val) :
        self.value = val
        self.guess = True

    # Add a value to the list of possible values
    def add_possible_value(self, val) :
        if self.possible_values.count(val) > 0 :
            pass
        else :
            self.possible_values.append(val)

    # Inverse of the above... duh! =-P
    def remove_possible_value(self, val) :
        if self.possible_values.count(val) > 0 :
            self.possible_values.remove(val)
