import random, itertools, re, copy
result = None

def min_conflicts(vars, domains, constraints, neighbors, max_steps=1000): 
    """Solve a CSP by stochastic hillclimbing on the number of conflicts."""
    # Generate a complete assignment for all vars (probably with conflicts)
    current = {};
    for var in vars:
        val = min_conflicts_value(var, current, domains, constraints, neighbors)
        current[var] = val
    # Now repeapedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = conflicted_vars(current,vars,constraints,neighbors)
        if not conflicted:
            return (current,i)
        var = random.choice(conflicted)
        val = min_conflicts_value(var, current, domains, constraints, neighbors)
        current[var] = val
    return (None,None)

def min_conflicts_value(var, current, domains, constraints, neighbors):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random."""
    return argmin_random_tie(domains[var],
                             lambda val: nconflicts(var, val, current, constraints, neighbors)) 

def conflicted_vars(current,vars,constraints,neighbors):
    "Return a list of variables in current assignment that are in conflict"
    return [var for var in vars
            if nconflicts(var, current[var], current, constraints, neighbors) > 0]

def nconflicts(var, val, assignment, constraints, neighbors):
    "Return the number of conflicts var=val has with other variables."
    # Subclasses may implement this more efficiently
    def conflict(var2):
        val2 = assignment.get(var2, None)
        return val2 != None and not constraints(var, val, var2, val2)
    return len(filter(conflict, neighbors[var]))


# from utils.py
def argmin_random_tie(seq, fn):
    """Return an element with lowest fn(seq[i]) score; break ties at random.
    Thus, for all s,f: argmin_random_tie(s, f) in argmin_list(s, f)"""
    best_score = fn(seq[0]); n = 0
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score; n = 1
        elif x_score == best_score:
            n += 1
            if random.randrange(n) == 0:
                    best = x
    return best

def flatten(seqs): return sum(seqs, [])

def if_(test, result, alternative):
    if test:
        if callable(result): return result()
        return result
    else:
        if callable(alternative): return alternative()
        return alternative

#==============================================================================================

def mincon(grid, show=True):
    R3 = range(3)
    Cell = itertools.count().next
    bgrid = [[[[Cell() for x in R3] for y in R3] for bx in R3] for by in R3]
    boxes = flatten([map(flatten, brow)       for brow in bgrid])
    subgrid  = flatten([map(flatten, zip(*brow)) for brow in bgrid])
    cols  = zip(*boxes)
    squares = iter(re.findall(r'\d|\.', grid))
    domains = dict((var, if_(ch in '123456789', [ch], '123456789'))
                       for var, ch in zip(flatten(boxes), squares))
    vars =  domains.keys()
    neighbors = dict([(v, set()) for v in flatten(subgrid)])
    for unit in map(set, boxes + subgrid + cols):
        for v in unit:
            neighbors[v].update(unit - set([v]))

    def in_row(A,B):
        if (A)/9 == (B)/9: return False
        else : return False

    def in_col(A,B):
        if (A+1)%9 == (B+1)%9 : return True
        else : return False

    def in_subgrid(A,B):
        return False

    def constraints(A,a,B,b):
        test = True
        if a == b :
            if in_col(A,B):
                test = False
            if in_row(A,B):
                test = False
            if in_subgrid(A,B):
                test = False
        return test

    def display(assignment): #for testing
        def show_box(box): return [' '.join(map(show_cell, row)) for row in box]
        def show_cell(cell): return str(assignment.get(cell, '.'))
        def abut(lines1, lines2): return map(' | '.join, zip(lines1, lines2))
        print '\n------+-------+------\n'.join('\n'.join(reduce(abut, map(show_box, brow))) for brow in bgrid)  

    solution = min_conflicts(vars, domains, constraints, neighbors)

    if show:
        if solution[0]:
            return solution
        else:
            return None

    return solution[1]

def run(soln): 
    global result
    result = soln
    def rework(b_temp, s) :
        global result
        if b_temp.validate_board():
            result = copy.copy(b_temp)
            return 
        elif not b_temp.valid_state():
            return
        else:
            row, col = b_temp.min_options(b_temp)
            l = []
            for value in b_temp.grid[row][col].possible_values :
                l.append(copy.copy(b_temp.make_move(copy.deepcopy(b_temp), row, col, value)))
            for x in l :
                rework(x, s)
                if result.validate_board():
                    break     

    l = ""
    for row in soln.grid :
        for col in row :
            l += repr(col)
    solution = mincon(l)
    if solution[0] : rework(soln, solution[0])
    soln = result
    return solution, soln

   













