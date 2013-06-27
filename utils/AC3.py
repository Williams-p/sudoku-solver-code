import itertools, re

class CSP(object):

    def __init__(self, vars, domains, neighbors, constraints):
        self.vars = vars or domains.keys()
        self.domains=domains
        self.neighbors=neighbors
        self.constraints=constraints
        self.curr_domains=None
        self.nassigns=0

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = dict((v, list(self.domains[v]))for v in self.vars)

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None: removals.append((var, value))

    def infer_assignment(self):
        self.support_pruning()
        return dict((v, self.curr_domains[v][0])for v in self.vars if 1 == len(self.curr_domains[v]))

# ========================================================================================
# Constraint Propagation with AC-3

def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xi:
                    queue.append((Xk, Xi))
    return True

def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every(lambda y: not csp.constraints(Xi, x, Xj, y),
                 csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

def every(predicate, seq):
    for x in seq:
        if not predicate(x): return False
    return True

# =====================================================================================

def flatten(seqs): return sum(seqs, [])

class Sudoku(CSP):
    R3 = range(3)
    Cell = itertools.count().next
    bgrid = [[[[Cell() for x in R3] for y in R3] for bx in R3] for by in R3]
    boxes = flatten([map(flatten, brow)       for brow in bgrid])
    rows  = flatten([map(flatten, zip(*brow)) for brow in bgrid])
    cols  = zip(*rows)

    neighbors = dict([(v, set()) for v in flatten(rows)])
    for unit in map(set, boxes + rows + cols):
        for v in unit:
            neighbors[v].update(unit - set([v]))

    def different_values_constraint(self, A, a, B, b):
        return a != b

    def __init__(self, grid):
        squares = iter(re.findall(r'\d|\.', grid))

        domains = dict((var, self.if_(ch in '123456789', [ch], '123456789'))
                       for var, ch in zip(flatten(self.rows), squares))
        
        for _ in squares:
            raise ValueError("Not a Sudoku grid", grid)
        CSP.__init__(self, None, domains, self.neighbors, self.different_values_constraint)

    def if_(self, test, result, alternative):
        if test:
            if callable(result): return result()
            return result
        else:
            if callable(alternative): return alternative()
            return alternative

    def display(self, assignment):
        def show_box(box): return [' '.join(map(show_cell, row)) for row in box]
        def show_cell(cell): return str(assignment.get(cell, '.'))
        def abut(lines1, lines2): return map(' | '.join, zip(lines1, lines2))
        print '\n------+-------+------\n'.join('\n'.join(reduce(abut, map(show_box, brow))) for brow in self.bgrid)

    def get(self, assignment):
        def show_box(box): return [' '.join(map(show_cell, row)) for row in box]
        def show_cell(cell): return str(assignment.get(cell, '.'))
        def abut(lines1, lines2): return map(' | '.join, zip(lines1, lines2))
        return '\n------+-------+------\n'.join('\n'.join(reduce(abut, map(show_box, brow))) for brow in self.bgrid)

# ================================================================================================
# run for mincon

def run(board) :
    l = ""
    for row in board.grid :
        for col in row :
            l += repr(col)

    e = Sudoku(l)
    #print "before AC3"
    #e.display(e.infer_assignment())
    AC3(e)
    #print "after AC3"
    #e.display(e.infer_assignment())
    return e.get(e.infer_assignment())










