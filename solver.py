## define a class for sudoku solver that using backtracking
class Solver(object):
    def __init__(self, sudoku):
        self.board = sudoku.board


    def backtracking(self, sudoku, assignment):
        if len(assignment) == len(sudoku.RV):
            for k, v in assignment.items():
                sudoku.board[k] = v
            return sudoku.board
        var = self.getMRV(sudoku, assignment)
        for val in self.getOrderDomain(var, sudoku):
            if self.isConsistent(var, val, sudoku, assignment):
                assignment[var] = val
                sudoku.forwardChecking(var, val, assignment)
                res = self.backtracking(sudoku, assignment)
                if res:
                    return res
                sudoku.unassign(var, val, assignment)
        return False



    def getMRV(self, sudoku, assignment):
        """choose MRV"""
        unassigned = [k for k in sudoku.RV if k not in assignment]
        return min(unassigned, key = lambda x: len(sudoku.domain[x]) )


    def getOrderDomain(self, var, sudoku):
        """LCV: choose values that cause the least amount of conflicts"""
        vals = sudoku.domain[var]
        vals.sort(key = lambda x: sudoku.getConflicts(var, x))
        return vals


    def isConsistent(self, loc, val, sudoku, assignment):
        """check if the current value is consistent with the rest of assignment"""
        row = loc[0]
        col = loc[1]
        for k, v in assignment.items():
            if v == val and (k in sudoku.getBlock(loc) or k[0] == row or k[1] == col):
                return False
        return True
    
