from copy import deepcopy
import test_grids

class Checker:

    def check_valid(self, grid):
        for row in grid:
            if not self.check_row(row):
                return False
        for i in range(9):
            if not self.check_row(self.col_to_row(grid, i)):
                return False
        for i in range(3):
            for j in range(3):
                if not self.check_row(self.box_to_row(grid, i, j)):
                    return False
        return True

    def check_row(self, row):
        count = set()
        for item in row:
            if item in count:
                return False
            else:
                count.add(item)
        return True

    def col_to_row(self, grid, col):
        result = []
        for row in grid:
            result.append(row[col])
        return result

    def box_to_row(self, grid, row, col):
        result = []
        for i in range(3):
            for j in range(3):
                result.append(grid[i+row][j+col])
        return result


    def is_well_formed(self, grid):
        if len(grid) != 9:
            return False
        for row in grid:
            if len(row) != 9:
                return False
        return True

    def check_victory(self, grid):
        for row in grid:
            for col in row:
                if col == 0:
                    return False
        return True

class Cell:

    def __init__(self, row, col, grid):
        self.row = row
        self.col = col
        self.value = 0
        self.row_offset = int(row/3)
        self.col_offset = int(col/3)
        self.grid = grid
        self.possible = set([1,2,3,4,5,6,7,8,9])
        self.check_possible()

    def check_possible(self):
        for item in self.grid[self.row]:
            if item in self.possible:
                self.possible.remove(item)
        for i in range(9):
            item = self.grid[i][self.col]
            if item in self.possible:
                self.possible.remove(item)
        for i in range(3):
            for j in range(3):
                item = self.grid[i + self.row_offset][j + self.col_offset]
                if item in self.possible:
                    self.possible.remove(item)

class Sudoku:

    def __init__(self, grid, checker):
        self.grid = grid
        self.checker = checker
        self.blanks = []
        self.rows = [[],[],[],[],[],[],[],[],[]]
        self.cols = [[],[],[],[],[],[],[],[],[]]
        self.boxes = [[[],[],[]],[[],[],[]],[[],[],[]]]
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    c = Cell(i, j, self.grid)
                    self.blanks.append(c)
                    self.rows[i].append(c)
                    self.cols[j].append(c)
                    self.boxes[int(i/3)][int(j/3)].append(c)
        self.last_blanks = len(self.blanks)

    def run(self):
        while True:
            self.step()
            if self.checker.check_victory(self.grid):
                print(self)
                return True
            if len(self.blanks) == self.last_blanks:
                return self.guess()
            self.last_blanks = len(self.blanks)

    def step(self):
        self.update_decided_cells()
        assert self.checker.check_valid(self.grid), str(self)
        self.update_decided_digits()
        self.clean_blanks()
        
        return len(self.blanks) == 0

    def sort_blanks(self):
        self.blanks.sort(key=lambda c: len(c.possible))
        self.blanks.reverse()

    def update_decided_cells(self):
        for i in range(len(self.blanks) -1, 0, -1):
            c = self.blanks[i]
            if len(c.possible) == 1:
                x = c.possible.pop()
                self.grid[c.row][c.col] = x
                c.value = x

    def update_decided_digits(self):
        for i in range(len(self.blanks) - 1, 0, -1):
            c = self.blanks[i]
            # Check row
            self.update_decided_list(self.rows[c.row])
            # Check col
            self.update_decided_list(self.cols[c.col])
            # Check box
            self.update_decided_list(self.boxes[c.row_offset][c.col_offset])

    def update_decided_list(self, li):
        count = {}
        for cell in li:
            for number in cell.possible:
                if number in count:
                    count[number].append(cell)
                else:
                    count[number] = [cell]
        for key, val in count.items():
            if len(val) == 1:
                item = val[0]
                self.grid[item.row][item.col] = key
                item.value = key
                for item in li:
                    item.check_possible()

    def clean_blanks(self):
        for i in range(len(self.blanks) - 1, 0, -1):
            if self.blanks[i].value != 0:
                self.blanks.pop(i)

    def guess(self):
        for cell in self.blanks:
            for value in cell.possible:
                cell.value = value
                self.grid[cell.row][cell.col] = value
                s = Sudoku(deepcopy(self.grid), self.checker)            
                result = s.run()
                if result:
                    return True
            cell.value = 0
            self.grid[cell.row][cell.col] = 0
        print(self)
        return False

    def __str__(self):
        result = "Sudoku:\n"
        for row in self.grid:
            for col in row:
                if col == 0:
                    result += "_ "
                else:
                    result += str(col) + " "
            result += "\n"
        result += "Blanks: " + str(len(self.blanks))
        return result

if __name__ == '__main__':
    c = Checker()
    for grid in test_grids.tests:
        print(grid)
        if c.is_well_formed(grid):
            s = Sudoku(grid, c)
            result = s.run()
            if result:
                print("Grid Passed")
            else:
                print("Grid failed")
        else:
            print("Grid malformed")
        






