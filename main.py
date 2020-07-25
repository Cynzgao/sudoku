if __name__ == '__main__':
    # run_time = []
    line = sys.argv[1]

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")
    board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}
    assert(len(line) == 81)
    sudoku = Sudoku(board)
    solver = Solver(sudoku)
    solved_board = solver.backtracking(sudoku, dict())

    # Write board to file
    outfile.write(board_to_string(solved_board))
    outfile.write('\n')
    outfile.close()
