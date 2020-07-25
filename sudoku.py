## define a class for sudoku board
class Sudoku(object):
    def __init__(self, board):
        """
        :param board->Dict: a dictionary representation of location and sudoku
        values
        """
        self.board = board
        self.RV = self.getRV()
        self.domain = self.buildDom()
        self.neighbors = self.makeNeighbor()
        self.checked = {v: list() for v in self.RV}


    def getRV(self):
        """get a list of remaining values of the board"""
        rv = list()
        for loc, val in self.board.items():
            if val == 0:
                rv.append(loc)
        return rv


    def getBlock(self, loc):
        """given a location, get the indices that are in the same block"""
        row = loc[0]
        col = loc[1]
        block_row = (ord(row)-ord('A')) //3
        block_col = (int(col)-1) //3
        r_ind = ['ABC', 'DEF', 'GHI']
        c_ind = ['123', '456', '789']
        ind = [r + c for r in r_ind[block_row] for c in c_ind[block_col]]
        return ind


    def makeNeighbor(self):
        """build a dictionary for remaining values and their neighbors"""
        neighbors = dict()
        for loc in self.RV:
            neighbors[loc] = list()
            for key in self.RV:
                if key != loc and (key[0] == loc[0] or key[1] == loc[1] or key \
                                   in self.getBlock(loc)):
                    neighbors[loc].append(key)
        return neighbors


    def getConstraint(self, loc):
        """use loc, eg. "A1", to determin constrained values for unassigned"""
        row = loc[0]
        col = loc[1]
        constraint = list()
        for key, val in self.board.items():
            if val != 0:
                r = key[0]
                c = key[1]
                if r == row or c == col or key in self.getBlock(loc):
                    constraint.append(self.board[key])
        return constraint

    def buildDom(self):
        """put remaining values and their possible moves in a dict"""
        domain = dict()
        for rv in self.RV:
            constraint = self.getConstraint(rv)
            domain[rv] = [i for i in range(1, 10) if i not in constraint]
        return domain


    def getConflicts(self, loc, val):
        """get number of conflicts of given location - value"""
        count = 0
        block = self.getBlock(loc)
        for k, v in self.domain.items():
            if val in v and (k[0] == loc[0] or k[1] == loc[1] or k in block) and k != loc:
                count += 1
        return count


    def unassign(self, loc, val, assignment):
        """put the previously checked values back into domain"""
        for (neighbor, val) in self.checked[loc]:
            self.domain[neighbor].append(val)
        self.checked[loc] = list()
        del assignment[loc]



    def forwardChecking(self, loc, val, assignment):
        """Apply Forward checking on a given assignment: remove
        assigned value from possible remaining values """
        for neighbor in self.neighbors[loc]:
            if neighbor not in assignment:
                if val in self.domain[neighbor]:
                    self.domain[neighbor] = [i for i in self.domain[neighbor] if i != val]
                    self.checked[loc].append((neighbor, val))
