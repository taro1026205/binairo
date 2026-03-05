from utils.binairo import Binairo

class HeuristicBinairo(Binairo):

    def __init__(self, initial_grid, enable_log = False):
        super().__init__(initial_grid, enable_log)
        self.row_cnt = [[0, 0] for _ in range(self.n)]
        self.col_cnt = [[0, 0] for _ in range(self.n)]

        for r in range(self.n):
            for c in range(self.n):
                v = self.grid[r][c]
                if v != -1:
                    self.row_cnt[r][v] += 1
                    self.col_cnt[c][v] += 1


    def is_valid(self, grid_state, r, c, val):
        if self.row_cnt[r][val] + 1 > self.half:
            return False
        if self.col_cnt[c][val] + 1 > self.half:
            return False

        g = grid_state
        for i in (c - 2, c - 1, c):
            if 0 <= i <= self.n - 3:
                v0 = val if i   == c else g[r][i]
                v1 = val if i+1 == c else g[r][i+1]
                v2 = val if i+2 == c else g[r][i+2]
                if v0 != -1 and v1 != -1 and v2 != -1:
                    if v0 == v1 == v2:
                        return False

        for i in (r - 2, r - 1, r):
            if 0 <= i <= self.n - 3:
                v0 = val if i   == r else g[i][c]
                v1 = val if i+1 == r else g[i+1][c]
                v2 = val if i+2 == r else g[i+2][c]
                if v0 != -1 and v1 != -1 and v2 != -1:
                    if v0 == v1 == v2:
                        return False

        return True


    def assign(self, r, c, val, changed_cells):
        self.grid[r][c] = val
        self.row_cnt[r][val] += 1   
        self.col_cnt[c][val] += 1  
        changed_cells.append((r, c, val))
        self.log_step() #log state for visual display 

    def undo_all(self, changed_cells):
        for r, c, val in reversed(changed_cells):
            self.grid[r][c] = -1
            self.row_cnt[r][val] -= 1   
            self.col_cnt[c][val] -= 1   
            self.log_step() #log state for visual display 
        changed_cells.clear()


    def get_domain(self, r, c):
        if self.grid[r][c] != -1:
            return []
        domain = []
        for val in [0, 1]:
            if self.is_valid(self.grid, r, c, val):
                domain.append(val)
        return domain

    def propagate(self, changed_cells, dirty_rows=None, dirty_cols=None):
        if dirty_rows is None:
            dirty_rows = set(range(self.n))
            dirty_cols = set(range(self.n))

        while dirty_rows or dirty_cols:
            next_rows, next_cols = set(), set()

            for r in dirty_rows:
                for c in range(self.n):
                    if self.grid[r][c] != -1:
                        continue
                    domain = self.get_domain(r, c)
                    if not domain:
                        return False                
                    if len(domain) == 1:
                        self.assign(r, c, domain[0], changed_cells)
                        next_rows.add(r)            
                        next_cols.add(c)            

            for c in dirty_cols:
                for r in range(self.n):
                    if self.grid[r][c] != -1:
                        continue
                    domain = self.get_domain(r, c)
                    if not domain:
                        return False
                    if len(domain) == 1:
                        self.assign(r, c, domain[0], changed_cells)
                        next_rows.add(r)
                        next_cols.add(c)

            dirty_rows, dirty_cols = next_rows, next_cols

        return True


    def check_unique(self, grid_state):
        for r1 in range(self.n):
            if -1 in grid_state[r1]:
                continue
            for r2 in range(r1 + 1, self.n):
                if grid_state[r1] == grid_state[r2]:
                    return False

        for c1 in range(self.n):
            col1_complete = True
            for r in range(self.n):
                if grid_state[r][c1] == -1:
                    col1_complete = False
                    break
            
            if not col1_complete:
                continue

            for c2 in range(c1 + 1, self.n):
                match = True
                for r in range(self.n):
                    if grid_state[r][c2] == -1 or grid_state[r][c1] != grid_state[r][c2]:
                        match = False
                        break
                if match:
                    return False

        return True

    def degree(self, grid_state, r, c):
        filled_row = self.row_cnt[r][0] + self.row_cnt[r][1]
        empty_row  = self.n - filled_row - 1

        filled_col = self.col_cnt[c][0] + self.col_cnt[c][1]
        empty_col  = self.n - filled_col - 1

        return empty_row + empty_col


    def select_mrv_cell(self, grid_state):
        best = None
        best_degree = -1

        for r in range(self.n):
            for c in range(self.n):
                if grid_state[r][c] == -1:
                    deg = self.degree(grid_state, r, c)
                    if deg > best_degree:
                        best_degree = deg
                        best = (r, c)

        if best:
            r, c = best
            return (r, c, self.get_domain(r, c)) 
        
        return None


    def solve(self):
        changed_cells = []
        if not self.propagate(changed_cells):
            self.undo_all(changed_cells)
            return False

        if not self.check_unique(self.grid):
            self.undo_all(changed_cells)
            return False

        cell = self.select_mrv_cell(self.grid)
        if cell is None:
            return True                             

        r, c, domain = cell
        if not domain:
            self.undo_all(changed_cells)
            return False

        for val in domain:
            start_len = len(changed_cells)
            self.assign(r, c, val, changed_cells)         

            if self.propagate(changed_cells, dirty_rows=[r], dirty_cols=[c]):
                if self.solve():
                    return True

            while len(changed_cells) > start_len:
                ur, uc, uval = changed_cells.pop()
                self.grid[ur][uc] = -1
                self.row_cnt[ur][uval] -= 1
                self.col_cnt[uc][uval] -= 1
                self.log_step() #log state for visual display 

        self.undo_all(changed_cells)
        return False