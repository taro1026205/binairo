from utils.binairo import Binairo

class DFSBinairo(Binairo):
    def __init__(self, initial_grid, enable_log = False):
        super().__init__(initial_grid, enable_log)

    def solve(self, r=0, c=0):
        if r == self.n:
            return self.is_complete_valid(self.grid)

        if c == self.n:
            return self.solve(r + 1, 0)

        if self.grid[r][c] != -1:
            return self.solve(r, c + 1)

        for val in [0, 1]:
            if self.is_valid(self.grid, r, c, val):
                self.grid[r][c] = val
                self.log_step() #log state for visual display 
                if self.solve(r, c + 1):
                    return True
                self.grid[r][c] = -1  
                self.log_step() #log state for visual display 
        return False