from copy import deepcopy
from collections import defaultdict

class DynamicSampleSpace:

    def __init__(self, uniform_sample_space: list):
        self.size = len(uniform_sample_space)
        self.ss = deepcopy(uniform_sample_space)

    def mask(self, i: int):
        self.size -= 1
        self.ss[i], self.ss[self.size] = self.ss[self.size], self.ss[i]

    def unmask(self, i: int):
        self.ss[i], self.ss[self.size] = self.ss[self.size], self.ss[i]
        self.size += 1

    def __len__(self):
        return len(self.ss)

    def __getitem__(self, i: int):
        return self.ss[i]

    def __repr__(self):
        return "size: " + str(self.size) + " | %s" % self.ss


# only works when we are ensured that the columns we are masking are 0
class DynamicColumnSampleSpace(DynamicSampleSpace):
    def mask(self, i: int):
        self.size -= 1
        self.ss[i] = self.ss[self.size]

    def unmask(self, i: int):
        self.ss[i] = 0
        self.size += 1



class ValsingLinks:

    def __init__(self, input_grid: list):
        self.grid = [DynamicColumnSampleSpace(row) for row in deepcopy(input_grid)]
        self.header_row = DynamicSampleSpace([i for i in range(0, len(self.grid))])
        self.grid_length = self[0].size

        self.swap_stack = []
        self.solutions = set()

    def __getitem__(self, i: int):
        return self.grid[i]

    def solve(self, res=[]):

        # MASK OVERLAPPING ROWS FROM BEING INCLUDED IN THE SOLUTION
        def mask():
            nonlocal populated_cols
            nonlocal prospective_row_i
            nonlocal grid_height_before_cover

            for header_row_i in range(grid_height_before_cover - 1, -1, -1):

                # GET ROW INDEX
                row_i = initial_header_row[header_row_i]

                # MASK OVERLAPPING ROWS
                if row_i == prospective_row_i or any(self[row_i][j] for j in populated_cols):
                    self.header_row.mask(header_row_i)
                    self.swap_stack.append(header_row_i)
                    continue

                # MASK ELIMINATED COLUMNS
                for j in populated_cols:
                    self[row_i].mask(j)

            self.grid_length -= len(populated_cols)

        # UNMASK OVERLAPPING ROWS TO CONSIDER OTHER SOLUTIONS
        def unmask():
            nonlocal populated_cols
            nonlocal grid_height_before_cover

            # UNMASK PREVIOUSLY ELIMINATED COLUMNS
            for header_row_i in range(0, self.header_row.size):
                row_i = self.header_row[header_row_i]
                for j in reversed(populated_cols):
                    self[row_i].unmask(j)

            # UNMASK PREVIOUSLY MATCHING ROws
            for _ in range(self.header_row.size, grid_height_before_cover):
                old_index = self.swap_stack.pop()
                self.header_row.unmask(old_index)

            self.grid_length += len(populated_cols)

        # BASE CASE
        # CHECK IF CURRENT SOLUTION SET ACHIEVES EXACT COVER
        if not self.grid_length:
            self.solutions.add(tuple(sorted(res)))
            return

        # RECORD HEADER ROW AND GRID HEIGHT
        initial_header_row = self.header_row.ss
        grid_height_before_cover = self.header_row.size

        # EXPLORE RANDOMLY -JUST TO MAKE A POINT (better explore rows with fewest populated columns first)
        rows_left = [initial_header_row[i] for i in range(grid_height_before_cover)]

        # SEARCH RECURSIVELY
        while rows_left:

            # PICK ROW
            prospective_row_i = rows_left.pop()
            populated_cols = [j for j in range(self.grid_length) if self[prospective_row_i][j]]

            # APPEND TO PROSPECTIVE SOLUTION
            res.append(prospective_row_i)
            mask()

            # CONTINUE SOLVING
            self.solve(res)

            # POP FROM PROSPECTIVE SOLUTION
            unmask()
            res.pop()
