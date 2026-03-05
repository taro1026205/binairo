import copy

class Binairo:
    def __init__(self, initial_grid, enable_log = False):
        self.grid = copy.deepcopy(initial_grid)
        self.n = len(initial_grid)
        self.half = self.n // 2

        self.enable_log = enable_log
        if self.enable_log:
            self.history = [copy.deepcopy(self.grid)]

    def is_valid(self, grid_state, r, c, val):
        row = grid_state[r][:]
        row[c] = val
        for i in range(self.n - 2):
            if row[i] != -1 and row[i+1] != -1 and row[i+2] != -1:
                if row[i] == row[i+1] == row[i+2]:
                    return False

        col = [grid_state[i][c] for i in range(self.n)]
        col[r] = val
        for i in range(self.n - 2):
            if col[i] != -1 and col[i+1] != -1 and col[i+2] != -1:
                if col[i] == col[i+1] == col[i+2]:
                    return False

        if sum(1 for x in row if x == val) > self.half:
            return False
        if sum(1 for x in col if x == val) > self.half:
            return False

        return True

    def is_complete_valid(self, grid_state):
        rows = [tuple(grid_state[r]) for r in range(self.n)]
        if len(rows) != len(set(rows)):
            return False
        
        cols = [tuple(grid_state[r][c] for r in range(self.n)) for c in range(self.n)]
        if len(cols) != len(set(cols)):
            return False
            
        return True

    def print_grid(self, grid_state=None, title=""):
        if grid_state is None:
            grid_state = self.grid
            
        if title:
            print(f"\n{'='*30}")
            print(f"  {title}")
            print(f"{'='*30}")
            
        separator = "+" + ("-" * (self.n * 2 + 1)) + "+"
        print(separator)
        for row in grid_state:
            cells = " ".join(str(x) if x != -1 else "." for x in row)
            print(f"| {cells} |")
        print(separator)

    def log_step(self): #log state for visual display 
        if self.enable_log:
            self.history.append(copy.deepcopy(self.grid))